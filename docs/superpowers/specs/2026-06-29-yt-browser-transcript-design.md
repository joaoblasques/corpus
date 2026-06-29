# Browser-UI YouTube transcript tier — design

> Date: 2026-06-29 · Status: approved (brainstorm) · Repo: corpus (software layer)

## Problem

YouTube transcript collection is fragile. Every current path in
`youtube_client.extract_transcript` ultimately hits YouTube's **backend** endpoints:

1. `youtube_transcript_api` — IP-blocked / `RequestBlocked` (403), especially from the cloud.
2. `yt-dlp` VTT subtitles (browser cookies) — bot-gated ("Sign in to confirm you're not a
   bot") after ~44 rapid pulls.
3. `yt-dlp` audio → Groq Whisper — same yt-dlp bot-gate on the audio download, plus Groq cost.

The result is a rate-limited, self-poisoning cascade: the cheap API call that fires first is
exactly what triggers the block, after which everything downstream also fails. The corpus
stays mostly healthy (~235/250 `ok`) only because of layered rescue machinery and slow nightly
recovery.

## Insight

The YouTube **watch-page UI** exposes a "Show transcript" panel that is **public** (no login
required) and rendered by the front-end. Scraping it is a *different, harder-to-detect surface*
than the bot-gated backend endpoints. A real (even logged-out) browser loading the page looks
like a viewer, not a scraper.

## Goals

Solve scope **C** — build a backlog drainer first, designed so the same core slots into the
nightly collector as a permanent tier.

Decisions locked during brainstorm:
- **Session model: logged-out.** A fresh Playwright Chromium, never touching the user's Google
  account (zero account risk). The transcript panel is public, so login is unnecessary.
  Escalation to a logged-in / throwaway-account session is explicitly *out of scope* for v1;
  revisit only if logged-out proves to get gated.
- **Placement: browser-primary.** The browser scrape becomes the *first* path tried. The old
  API / yt-dlp paths are demoted to deep fallbacks, so the common case never touches the
  surfaces that get the IP blocked.
- **Runs on the Mac.** Nightly YouTube collection runs locally via `com.corpus.daily.plist`
  (launchd), not in the cloud nightly (which is still github-only). Headless logged-out
  Chromium runs invisibly under launchd. *Future risk:* if YouTube collection later moves to
  the cloud per the migration roadmap, a browser tier gets materially harder — flagged, not
  solved here.

## Architecture

### Component 1 — `bin/yt_browser_transcript.py` (new, isolated)

Single public function:

```python
browser_transcript(video_id: str) -> tuple[str, str]   # (markdown_body, status)
```

Behaviour (headless, logged-out):
1. Launch a logged-out Playwright Chromium. **One persistent browser context per run**,
   reused across many videos (cheap; avoids relaunch cost and looks like one session).
2. Navigate to `https://www.youtube.com/watch?v=<id>`; dismiss the consent/cookie interstitial.
3. Open the transcript panel: click "...more" in the description → "Show transcript", with a
   fallback to the description-area "Show transcript" button (YouTube relocates it).
4. Scrape rendered segments. Each panel line carries a timestamp (`1:23  text`); parse into
   `[{start: <seconds>, text: <str>}]` and feed the **existing** `cy.transcript_to_markdown`
   so output format + timestamp anchors are identical to today's transcripts.
5. Prepend provenance marker: `> _Transcript source: YouTube UI (browser)_`.

**Status contract:**
- `ok` — transcript scraped.
- `no_panel` — no transcript panel (captions genuinely don't exist) → caller tries Whisper.
- `blocked` — page itself gated (captcha / consent wall / "not a bot") → stop, don't hammer.
- `failed` — timeout / navigation / parse error.

The module owns *only* browser scraping. It depends on `collect_youtube` (`cy`) solely for
`transcript_to_markdown`. It does not know about stubs, the waterfall, or the nightly run —
those are the callers' concern.

### Component 2 — waterfall integration (`youtube_client.extract_transcript`)

Reordered, browser-primary:

```
browser_transcript(video_id)
  ok        -> return (body, "ok")
  no_panel  -> Whisper (yt-dlp audio -> Groq)           # caption-less videos
  blocked   -> DEEP fallback: youtube_transcript_api -> yt-dlp VTT   (last-resort insurance)
  failed    -> DEEP fallback: same as blocked
```

The current `_caption_transcript` / `_ytdlp_transcript` logic is **kept** but demoted below the
browser path. Whisper trigger conditions are unchanged except they now key off the browser
path's `no_panel`/exhaustion rather than the API's `none_found`/`disabled`.

A feature flag `CORPUS_YT_BROWSER` (default `1`) lets the browser tier be disabled to fall back
to today's behaviour, mirroring the existing `CORPUS_YT_WHISPER` switch.

### Component 3 — backlog drainer (extend `bin/whisper_rescue.py`)

Add a **browser mode** to the existing rescue tool rather than forking a near-duplicate. The
tool already walks `blocked`/non-`ok` stubs and the `.whisper_keepers.tsv` keeper list and
upgrades each stub in place — only the per-video fetch call changes. New flag:

```
whisper_rescue.py --browser        # use browser_transcript first (default for already-blocked stubs)
```

Browser-first is the sensible default here: these stubs are *already* blocked, so re-poking the
API is pointless. Whisper remains available as the fallback for caption-less stubs.

## Pacing & anti-detection (logged-out survivability)

Logged-out is the most fingerprintable session, so survivability rests on *behaviour*, not auth:

- One reused browser context per run.
- Realistic user-agent + viewport; light scroll before scraping.
- Randomized human delay between videos (3–8 s).
- **Nightly per-run cap** (config, default ~15–20 videos) so a launchd run never looks like a
  bulk scraper.
- **Graceful stop on `blocked`**: the first captcha/gate signal ends the run; never hammer.
- The attended **backlog drainer** may use a larger batch, since the user watches for gating.

## Data flow

```
playlist item / blocked stub
   -> browser_transcript(video_id)            [Component 1]
        -> Playwright watch page -> "Show transcript" panel
        -> [{start, text}] -> cy.transcript_to_markdown
   -> extract_transcript waterfall            [Component 2]   (nightly)
      or whisper_rescue --browser             [Component 3]   (backlog)
   -> raw/youtube/<slug>.md  (transcript_status: ok)
```

No change to downstream: stamped files flow into the existing ingest pipeline unchanged.

## Error handling

- Any Playwright exception inside `browser_transcript` is caught and mapped to `failed` (no
  partial transcripts written — same discipline as the Whisper path).
- `blocked` propagates up so the nightly loop can stop early (consistent with the existing
  HttpError 403/429/503 early-stop).
- Browser context is always torn down in a `finally` (no leaked Chromium processes under launchd).

## Testing

- **Unit**: timestamp-line parser (`1:23` / `1:02:03` → seconds; malformed → skipped); status
  mapping; markdown output matches `transcript_to_markdown` shape. Pure functions, no browser.
- **Integration (gated, opt-in)**: a `@pytest.mark.network` test that scrapes one known
  stable video end-to-end, skipped by default in CI (mirrors how network-dependent paths are
  already handled).
- **Drainer**: stub-upgrade idempotency (an `ok` stub is skipped); `--browser` selects the
  browser fetch; in-place rewrite preserves frontmatter.

## Dependencies

Adds **Playwright + a bundled Chromium** (~few hundred MB) to the toolchain — heavier than the
current `yt-dlp` / `ffmpeg` / `requests` set, but the price of a real browser. Pinned in the
project's dependency manifest; `playwright install chromium` documented in setup. Runs headless
under the existing launchd job.

## Out of scope (v1)

- Logged-in / throwaway-account sessions.
- Running the browser tier in the cloud nightly environment.
- Proxy rotation.
- Replacing Whisper for genuinely caption-less videos (browser tier handles only videos that
  *have* a transcript panel).

## Open risks

1. **YouTube DOM churn** — the "...more" → "Show transcript" path and panel markup change
   periodically; the scrape needs resilient selectors and will need occasional maintenance.
   Mitigated by isolating all DOM knowledge in Component 1.
2. **Logged-out gating** — YouTube may still throttle logged-out automated browsers; pacing +
   per-run cap are the first defense, with logged-in escalation held in reserve.
3. **Cloud migration** — a future move of YouTube collection to the cloud nightly invalidates
   the Mac-local assumption; noted as a known future cost.

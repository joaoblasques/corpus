---
module: youtube
tags: [transcript, playwright, anti-bot]
problem_type: rate-limit
---

# YouTube Browser Transcript Tier (Anti-Rate-Limit Scraper)

## Problem

YouTube's public API (`youtube.googleapis.com`) rate-limits transcript requests after ~30–50 rapid pulls in a single run, even with valid API keys and quota. The corpus's nightly ingest regularly hits this limit when processing 50+ new YouTube videos in one pass (e.g., from a subscribed playlist dump or a discovery batch).

Response: HTTP 429 (Too Many Requests) or quota exhaustion. Backend fallback is necessary.

## Solution: Logged-Out Browser Scraper

A headless Chromium browser (via Playwright) logs into YouTube as an *anonymous* user and extracts the transcript from the DOM panel visible to casual browsers. This path **does not hit the API quota** — it scrapes the UI directly.

### Activation Strategy

The browser tier activates in this order (see `bin/youtube_client.py`'s `run` method):

1. **API path first** (fast, quota-efficient for small batches)
   - Try `transcripts.list()` via the API.
   - On success → return immediately.

2. **Browser fallback** (when API fails or rate-limits)
   - Only if `CORPUS_YT_BROWSER=1` (default is off, disabled in nightly CI to save time/resources).
   - Launch headless Chromium, navigate to the video, extract transcript from the DOM.
   - On success → return; on failure → continue to next tier.

3. **Whisper rescue** (last resort, slow but always works)
   - Download the audio and run OpenAI's Whisper transcription.
   - Only in explicit backlog drains (e.g., `bin/whisper_rescue.py --browser` mode).

### Status Contract

`browser_transcript(video_id: str) -> (body: str, status: str)`

Four outcomes:

| Status | Meaning | Body | Next Step |
|--------|---------|------|-----------|
| `ok` | Panel found, rows extracted, provenance added | full markdown transcript | use it |
| `no_panel` | Page loaded, no transcript panel visible | empty string | fall through to Whisper |
| `blocked` | Early signal: YouTube returned bot-detection page, access denied | empty string | fail fast; wait or IP-cycle before retry |
| `failed` | Any exception during browser/DOM work (timeout, crash, etc.) | empty string | fall through to Whisper |

**Key rule**: never return partial transcripts. If rows are extracted but parsing fails, downgrade to `no_panel` (same as Whisper input: empty, move on).

## Configuration

### Environment Variables

- **`CORPUS_YT_BROWSER=1`** — enable browser tier in nightly/batch runs (off by default for speed).
  - Set in `bin/scheduled_run.py` or in the `.env` for manual testing.

- **`CORPUS_YT_LIVE=1`** — enable the *live smoke test* (`test_live_browser_transcript_known_video`).
  - Test is skipped by default to avoid spinning up real browsers in CI.
  - Used for manual end-to-end validation: `CORPUS_YT_LIVE=1 pytest tests/test_yt_browser_transcript.py -k live -v`

### Playwright Installation

```bash
python3 -m pip install playwright
python3 -m playwright install chromium
```

Without the browser binary, the module fails at import time if any function tries to use it. The tests mock `_fetch_panel`, so unit tests pass; live tests will skip if the browser is missing.

## Anti-Detection Strategy

The scraper mimics a casual user, not a bot:

- **Logged-out**: no credentials. YouTube serves the full UI including the transcript panel to anonymous visitors (as of 2026).
- **Full browser context**: Playwright emulates a real Chromium instance with timings, User-Agent, and viewport matching a desktop browser.
- **Human delays**: `human_delay()` adds 0.5–2.0 second pauses between page load, locator query, and text extraction, with small random variance. This avoids the "instant scrape" timing signature that triggers bot mitigation.
- **One browser per run**: context is reused across multiple videos within a single nightly ingest. A new browser launches only if the Corpus starts a fresh ingest run.

## Maintenance Risk: DOM Churn

YouTube redesigns the transcript panel periodically. When they do, the CSS selectors in `bin/yt_browser_transcript.py` (`_extract_panel_rows`) will return empty rows or fail outright.

**No automatic recovery.** The selector is hardcoded:

```python
def _extract_panel_rows(page):
    panel_rows = page.locator("yt-formatted-string.segment-start-time")
    # ... parse inner_text() for "MM:SS\ntext"
```

If this selector breaks:

1. The live test fails: `test_live_browser_transcript_known_video` will see `status == "no_panel"`.
2. **Manual fix required**: inspect YouTube's current panel HTML, update the selector in `_extract_panel_rows`, re-run the live test.
3. **No schema change**: the `ok|no_panel|blocked|failed` contract and the `browser_transcript()` signature stay stable; only the internal DOM parsing changes.

**Monitoring**: the nightly ingest logs each browser-tier result. If a spike in `no_panel` outcomes appears after a YouTube redesign, investigate the selectors.

## Pacing and Rate Limits

- **Per-run cap**: the nightly `run` (via `bin/youtube_client.py`) accepts `--max N` (default 50 videos). The browser tier respects this; it won't scrape more than N videos in one run.
- **No request queuing**: the corpus does not rate-limit between videos within a run. Playwright handles the timing via `human_delay()`.
- **Multi-run cadence**: nightly ingest runs once per day. YouTube's rolling window (typically per-minute or per-hour buckets) resets; next night's run starts fresh.

If a run exceeds YouTube's toleration (rare at ≤50 videos/night), the browser will receive a bot-detection page; status returns `blocked`, and the corpus stops scraping. Retry the next night.

## Testing

### Unit Tests (No Network)

Existing tests in `tests/test_yt_browser_transcript.py` (Tasks 1–3) mock `_fetch_panel` and test:
- Timestamp parsing (`parse_ts`)
- Line-to-snippet conversion (`lines_to_snippets`)
- Status passthrough (`ok`, `no_panel`, `blocked`, `failed`)
- Provenance injection

Run: `pytest tests/test_yt_browser_transcript.py -q`

### Gated Live Test

A single end-to-end smoke test, gated to opt-in:

```python
@pytest.mark.skipif(os.environ.get("CORPUS_YT_LIVE") != "1",
                    reason="set CORPUS_YT_LIVE=1 to run the real browser smoke test")
def test_live_browser_transcript_known_video():
    body, status = bt.browser_transcript("jNQXAC9IVRw")  # "Me at the zoo" (first YT video)
    bt.shutdown()
    assert status in ("ok", "no_panel")  # blocked/failed = browser misconfigured
    if status == "ok":
        assert body.startswith(bt.PROVENANCE)  # provenance marker present
```

**Normally skipped** (no browser overhead in CI):
```bash
pytest tests/test_yt_browser_transcript.py -k live -v
# 1 skipped (test skipped due to CORPUS_YT_LIVE not set)
```

**Manual validation** (requires browser + network):
```bash
CORPUS_YT_LIVE=1 pytest tests/test_yt_browser_transcript.py -k live -v
# 1 passed (scrapes "Me at the zoo", checks provenance)
```

The video `jNQXAC9IVRw` (Me at the zoo) is stable, has captions, and is YouTube's canonical first video — ideal for this smoke test.

## Integration with the Corpus

- **Nightly ingest** (`bin/scheduled_run.py`, runs daily at 02:00 UTC):
  - Collects new YouTube URLs from configured sources (feed, playlist, discovery).
  - Queues videos to `raw/youtube/` with metadata.
  - Runs `ingest` → calls `youtube_client.py run --max 50 --model sonnet`.
  - YouTube client tries API first, falls back to browser if enabled (`CORPUS_YT_BROWSER=1`).

- **Manual backlog drain** (`bin/whisper_rescue.py --browser`):
  - Admin tool to reprocess past videos that failed or timed out.
  - Forces browser tier (ignores API).
  - Feeds results into corpus for re-ingest.

- **Fallback to Whisper** (always available):
  - If browser returns `no_panel` or `failed`, and Whisper is available, the corpus falls back to audio transcription.
  - No transcript at all → stub page created, manual review queued.

---

## References

- `bin/yt_browser_transcript.py` — scraper implementation (DOM selector, human delays, status logic)
- `bin/youtube_client.py` — three-tier routing (API → browser → Whisper)
- `bin/whisper_rescue.py` — backlog drainer
- `tests/test_yt_browser_transcript.py` — unit + live tests
- `README.md` — setup instructions (Playwright install)

---

## Status: EXPERIMENTAL — default OFF (2026-06-29)

The tier is built, tested, and merged, but **`CORPUS_YT_BROWSER` defaults to `0` (off)** because live validation showed the watch-page scrape is not yet reliable enough for unattended nightly runs. Opt in with `CORPUS_YT_BROWSER=1` while hardening. With the flag off, `extract_transcript` uses the proven legacy caption/yt-dlp/Whisper waterfall unchanged.

### Live findings (what breaks, and the working recipe)

Validated end-to-end against real YouTube (logged-out, headless Chromium). Two blockers that the v1 selectors did not handle, plus one open item:

1. **IP-localized UI.** YouTube serves the watch page in the browser's geo language (Portuguese here), so English-only selectors (`"...more"`, `"Show transcript"`) never match → `no_panel` on every video. **Fix:** force English — append `&hl=en` to the watch URL AND create the context with `locale="en-US"` + `extra_http_headers={"Accept-Language": "en-US,en;q=0.9"}`.

2. **EU consent wall (`ytd-consent-bump-v2-lightbox`).** A "Before you continue to YouTube" modal with a `tp-yt-iron-overlay-backdrop` overlays the page and **intercepts every click** until dismissed — this is the real reason the expander/transcript clicks time out. Stale `CONSENT`/`SOCS` cookies did NOT suppress it. **Fix:** after navigation, click the consent button by visible text (`button:has-text("Reject all")` inside `tp-yt-paper-dialog`/`ytd-consent-bump-v2-lightbox`); its `aria-label` is the long form ("Reject the use of cookies…"), so match on text, not aria-label. Confirm `tp-yt-iron-overlay-backdrop.opened` is gone before proceeding.

3. **Transcript open flow that works (verified — panel renders with timestamped segments):**
   - dismiss consent (above)
   - `page.mouse.wheel(0, 900)` to lazy-load the description area
   - click `#description-inline-expander tp-yt-paper-button#expand` (the "...more" expander; a plain click works *once consent is gone*)
   - click `[aria-label="Show transcript"]:visible` (there are 2 in the DOM; the `:visible` one is the live control — the other is hidden in the collapsed description). NB it is NOT `role=button`, so `get_by_role("button", name="Show transcript")` finds nothing — use the aria-label CSS selector.

### OPEN — must resolve before flipping default on

- **Segment selector unconfirmed.** With the panel visibly populated, `ytd-transcript-segment-renderer` returned 0 — the current DOM uses a different element for transcript lines. Capture the real selector (walk up from a known line) and update `_extract_panel_rows`.
- **Flakiness.** Consent-timing and expander-interception vary run-to-run; the flow needs explicit waits (`wait_for` on the consent backdrop disappearing, on the panel) and a small retry, not fixed `wait_for_timeout` sleeps, before it is safe for unattended use.
- All DOM knowledge stays isolated in `bin/yt_browser_transcript.py` (`_open_transcript`, `_extract_panel_rows`, `_fetch_panel`), so hardening touches that one file.

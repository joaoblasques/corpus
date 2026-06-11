# Spec: bounded link-following for `collect-email`

- **Date:** 2026-06-11
- **Status:** approved design (pre-implementation)
- **Sub-project:** B (collection layer) — enhancement to the `collect-email` collector
- **Builds on:** `docs/superpowers/specs/2026-06-09-email-collector-design.md`
- **Author:** brainstormed with user; this doc is the validated design

## Context

The `collect-email` collector captures starred Gmail messages into `raw/_inbox/`
as markdown and then de-stars/archives them (see the 2026-06-09 spec). v1
explicitly deferred *following the links inside emails*. Many starred emails are
newsletters that link out to articles/videos — the real value is the linked
content, not the email body. This spec adds **bounded link-following**: fetch and
capture the content behind qualifying links as their own corpus source files,
strictly bounded so it can never cascade into an unbounded crawl.

## Goals

1. For each collected email, follow links **in the email body** and capture their
   content into `raw/web/` (articles) or `raw/youtube/` (videos).
2. Rank links by **knowledge/learning utility** and keep only the most useful —
   practical/educational content (concepts, how-tos, tutorials, GitHub repos,
   tools) over ephemeral news (product launches, funding, announcements).
3. Stay **strictly bounded**: depth-1 only, noise-filtered, quality-floored, and
   capped per email. No link discovered inside a fetched page is ever followed.
4. Preserve the v1 safety model: the email body is written and archived first;
   enrichment is best-effort and never blocks collection or archiving.

## Non-goals (v1)

- Depth > 1 (following links found *inside* fetched pages). Structurally excluded.
- PDF / attachment text extraction (PDFs recorded as links, not fetched).
- Paywall bypass or JS rendering.
- Re-ranking links by their *fetched* content (ranking uses email-provided text).
- robots.txt parsing (personal archival use; a per-link timeout + UA is enough).

## The selection pipeline (per email)

Runs **after** the email body is written and the message archived.

```
1 EXTRACT   every URL in the body, with the description text the email gives each
2 FILTER    drop structural noise: unsubscribe, view-in-browser, mailto:, social/
            share (twitter/x, linkedin, facebook), and bare tracking/redirect hosts
3 RESOLVE   unwrap redirect wrappers (e.g. substack.com/redirect/… → real URL)
4 DEDUP     collapse duplicates by resolved URL (incl. against already-collected
            raw/web, raw/youtube, raw/_inbox files — fetch any URL at most once)
5 RANK      LLM scores each surviving link 0–10 for LEARNING UTILITY (url + desc)
6 FLOOR     drop score < 4  → recorded reason: low-utility   (quality floor, always)
7 CAP       keep top 10 by score → the rest recorded reason: over-cap
8 FETCH     survivors → raw/web/<slug>.md | raw/youtube/<slug>.md
```

Steps 1–4 and the heuristic fallback (step 5) are **pure Python**, unit-tested.

### Ranking (step 5)

- A single Anthropic API call per email (model: `claude-haiku-4-5-20251001`).
  Input: the candidate list as `[{index, url, description}]`. Output (structured):
  a utility score 0–10 per index. News/announcements score low; concepts,
  how-tos, GitHub repos, tutorials score high.
- The API key is read from a gitignored `.env` (`ANTHROPIC_API_KEY`) via a small
  manual loader (no new dependency).
- **Fallback:** if the key is absent or the API call fails, a deterministic
  keyword/domain heuristic produces the scores (boost `github.com`, docs hosts,
  `guide|tutorial|how-to|explained`; penalize `announces|raises|launches|
  acquires|$NNm|news`). The floor and cap still apply. The collector never
  hard-fails on ranking.

### Quality floor (step 6) and cap (step 7)

- **Floor:** score `< 4` → dropped, recorded `reason: low-utility`. Applied
  regardless of how many links exist (a short newsletter's lone news link is
  still skipped).
- **Cap:** of the links clearing the floor, fetch the top 10 by score;
  configurable via `--max-links N`. Links above the floor but beyond the cap are
  recorded `reason: over-cap`. Nothing is silently dropped — every candidate ends
  up in the email's `links:` frontmatter with a disposition.

## Content fetching (step 8)

- **Articles** → `httpx` GET (10s timeout, 1 retry, ~2 MB cap, descriptive UA) →
  `trafilatura` extraction → markdown → `raw/web/<slug>.md`.
- **YouTube** (youtube.com/watch, youtu.be) → `youtube_transcript_api` →
  timestamped transcript → `raw/youtube/<slug>.md`.
- **PDF / unsupported** → not fetched; recorded `reason: unsupported`.
- Per-link failure (HTTP error, empty extraction, transcript unavailable) →
  recorded `reason: fetch-failed`, skipped; the run continues.

### Storage & provenance

Each fetched link becomes its own raw file with frontmatter:

```yaml
channel: web            # or youtube
source_url: https://newsletter.example.com/agentic-ai-flywheels
via_email: 19eb5113f19d9b57    # parent gmail_message_id
utility_score: 9
collected_at: 2026-06-11
```

The parent email file records every candidate link and its disposition:

```yaml
links:
  - {url: …/agentic-ai-flywheels, fetched: true,  file: raw/web/agentic-ai-flywheels.md, score: 9}
  - {url: …/new-data-center,      fetched: false, reason: low-utility, score: 2}
  - {url: …/11th-good-article,    fetched: false, reason: over-cap,    score: 5}
  - {url: …/report.pdf,           fetched: false, reason: unsupported}
```

## Modules

| Module | Responsibility | Network | Tested |
|---|---|---|---|
| `bin/collect_email.py` | + `select_links(body)` (extract+filter+associate description) and `heuristic_score(url, desc)` — pure. `build_document`/`write_collected` gain an optional `links:` list. | No | pytest |
| `bin/rank_links.py` *(new)* | `.env` loader; `rank(candidates)` → scores via Anthropic API, heuristic fallback; applies floor + cap; returns dispositions. | API | pytest (mock API) |
| `bin/fetch_link.py` *(new)* | `classify(url)`, `resolve(url)`, `fetch(url)` → `{title, text, channel}`. | Yes | pytest (HTML/transcript fixtures) |
| `bin/gmail_client.py` | `run` orchestrates: write email → archive → enrich (select → rank → fetch → write files → update parent `links:`). New flags `--no-links`, `--max-links N`. | — | — |

## Dependencies & setup

- `pip install trafilatura youtube_transcript_api` (`anthropic` already installed).
- `ANTHROPIC_API_KEY` in gitignored `.env` (done + verified). Heuristic fallback
  if absent.

## Error handling & safety

- Email body write + archive happen first and are unchanged — enrichment runs
  after and is best-effort. A slow/failed fetch or ranking error never blocks
  collection or leaves mail un-archived.
- `run` tally gains: `links_captured`, `links_skipped` (by reason).
- Idempotent: URL-level dedup means re-running never double-fetches.

## Testing

- Pure logic (no network): extract, noise filter, redirect-host detection,
  description association, `heuristic_score`, floor + cap dispositioning.
- `rank_links`: ranking with a **mocked** Anthropic client; fallback path when key
  absent; floor/cap math.
- `fetch_link`: `classify` (article vs youtube vs unsupported), youtube-id
  parsing, article extraction against an HTML fixture, transcript against a
  fixture. No live network in tests.
- The existing 39 tests stay green.

## Open soft spots (acknowledged, intentional)

- **Description association** is heuristic (text near each URL). For oddly
  formatted newsletters the ranking input may be thin; ranking degrades to
  URL-only, which is acceptable for v1.
- **Heuristic fallback** is deliberately crude — it exists for robustness when the
  API is unavailable, not as a co-equal ranker.

# Blog / Series Deep-Scraper — Design Spec

> Date: 2026-06-24
> Status: **design approved**; ready for implementation plan
> Extends the existing Obsidian url-list flow (`TO SCRAPE.md` → fetch → strike) with deep scraping.

## 1. Problem

The user drops URLs in `00_Inbox/Clippings/TO SCRAPE.md`. Today the Obsidian collector fetches
each as a **single page** and strikes it after ingest. The user wants **tagged** blog/series URLs
deep-scraped — **all posts** of a blog or all parts of a series — into the corpus, striking the
seed URL only once **all** its posts are collected **and** ingested.

## 2. Decisions (confirmed with user)

- **Routing = tags.** Untagged URL → existing single-page fetch (unchanged). `<url> [blog]` /
  `<url> [blog:N]` → deep-scrape a blog. `<url> [series]` → scrape a series.
- **`[blog]`:** enumerate post URLs via the site's **`sitemap.xml`** (RSS/Atom fallback → recent
  only when no sitemap); filter to real posts; **cap 200** (raisable via `[blog:N]`; pages over
  runs when more posts than the cap remain).
- **`[series]`:** fetch the index page, extract the part-links (same-path heuristic), fetch all —
  always full (a series is small).
- **Per post:** a raw source, channel `web` → `raw/web`, tagged `scrape_seed: <seed url>`. **Dedup
  by post URL** — re-scraping a blog later only adds new posts.
- **Strike:** the seed URL leaves `TO SCRAPE.md` only when **all** its `scrape_seed` posts are
  `corpus_ingested` (extends the existing `_strike_url` reaper).
- **Files:** `bin/scrape_blog.py` (discovery + per-post) + a routing hook in `collect_obsidian.py`;
  strike reuses `_strike_url`. Wired into the 2 AM job.

## 3. Scope

In: tag parsing, sitemap/RSS blog enumeration, series-index extraction, per-post fetch+write
(dedup), seed-strike gating, scheduled wiring, `_config.md` docs, tests. Out: JS-rendered blogs
with no sitemap/RSS (need browser automation — deferred); perfect series detection (heuristic);
media download; the X/Substack collectors (separate specs).

## 4. Design

### 4.1 Tag parsing — `bin/collect_obsidian.py`
A URL-list line may carry a trailing tag: `https://blog.example.com [blog]`, `… [blog:500]`,
`https://site.com/the-series [series]`. Add `parse_scrape_tag(line) -> {url, mode, cap}` where
`mode ∈ {None, "blog", "series"}` (None = untagged → existing single-page path), `cap` = the
`[blog:N]` number or the default 200. Untagged URLs keep `extract_inline_links` / single fetch.

### 4.2 `bin/scrape_blog.py` (all HTTP via an injectable `_fetch`/`_session` seam)
- `discover_blog_posts(seed_url, cap=200, *, _session=None) -> list[str]`:
  - Try `<seed-origin>/sitemap.xml` (and a sitemap-index → child sitemaps); collect `<loc>` URLs;
    keep post-like ones (drop `/tag/ /category/ /author/ /page/ /about` + the bare origin); dedup
    preserving order; truncate to `cap`.
  - Fallback (no/empty sitemap): discover the feed (`<link rel=alternate type=application/rss+xml>`
    in the seed page, else `/feed`, `/rss.xml`, `/atom.xml`); collect `<item><link>` / `<entry>`
    `<link href>`; truncate to `cap`.
- `discover_series_parts(index_url, *, _session=None) -> list[str]`:
  - Fetch the index; extract `<a href>` absolute URLs **under the index's path prefix**; dedup,
    preserve document order (the part order).
- `scrape_seed(seed, mode, cap, *, collected_at, inbox=None, dedup_dirs=None, _session=None, _fetch=None) -> dict`:
  - `urls = discover_blog_posts(seed, cap)` if mode=="blog" else `discover_series_parts(seed)`.
  - For each `url` not `cx_already_collected(url)`: `content = _fetch(url)` (default `fetch_link.fetch`);
    if it has text → `write_post(seed, url, content, collected_at, inbox)` (channel `web`,
    `scrape_seed: seed`, `source_url: url`). Returns `{seed, found, written, duplicate, capped}`.
- `_post_collected(url, dirs) / write_post(...)` mirror the established collector helpers
  (dedup by `source_url`, slug from the URL).

### 4.3 Strike gating — extend `collect_obsidian.reapable`
A seed line in `TO SCRAPE.md` is **strikeable** only when every raw source carrying
`scrape_seed: <seed>` has `corpus_ingested: true`, AND the seed produced ≥1 such source (don't
strike a seed that scraped nothing). `reapable()` returns those seed URLs for the existing
`_strike_url` path. Until then the seed stays (safe for multi-run / paged scrapes).

### 4.4 Scheduled wiring
The Obsidian collect leg already runs; route its `TO SCRAPE.md` tagged lines to `scrape_blog`
(untagged lines keep the single-page path). The strike happens in the Obsidian reaper. Surface a
`scraped=N` count in the run summary.

## 5. Testing
- `parse_scrape_tag`: `[blog]` / `[blog:50]` / `[series]` / untagged → correct `{url, mode, cap}`.
- `discover_blog_posts`: parses a sitemap + sitemap-index, filters tag/author/page URLs, caps;
  RSS fallback when sitemap is absent (mock `_session`).
- `discover_series_parts`: same-path link extraction, order preserved (mock `_session`).
- `scrape_seed`: writes one source per new post with `scrape_seed`/`source_url`, dedups already-
  collected, honors `cap` (mock `_fetch`).
- strike gating: a seed is reapable only when ALL its `scrape_seed` sources are `corpus_ingested`.
- All HTTP/fetch injected — no network in tests.

## 6. Risks & mitigations
| Risk | Mitigation |
|---|---|
| Giant blog floods the corpus | cap 200 default; pages over runs; per-blog `[blog:N]` |
| No sitemap | RSS/Atom fallback (recent only); logged |
| Series heuristic over/under-includes | same-path rule; user re-tags/curates; blogs are the reliable path |
| Seed struck before all posts land | strike only when ALL `scrape_seed` posts are `corpus_ingested` |
| Re-scraping re-fetches posts | dedup by `source_url` |
| JS-only blog (no sitemap/RSS) | out of scope; logged as `scraped: 0`, seed kept |

## 7. Decisions locked
1. Tag-based routing; untagged = existing single-page (unchanged).
2. `[blog]` sitemap-first (RSS fallback), cap 200 raisable; `[series]` heuristic, full.
3. Per-post raw sources (channel `web`, `scrape_seed`); dedup by `source_url`.
4. Strike the seed only when all its posts are `corpus_ingested`.
5. `bin/scrape_blog.py` + a `collect_obsidian` routing hook; injectable HTTP; wired into the 2 AM job.

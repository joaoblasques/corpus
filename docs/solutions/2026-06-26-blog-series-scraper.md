---
module: collectors
tags: [obsidian, blog, scraping, reaping]
problem_type: feature
---

# Blog / series deep-scraper (per-list default mode)

The vault has two url-list files; each sets its own default mode for UNTAGGED lines (an
explicit `[blog]`/`[series]` tag on a line always overrides the list default):

- `00_Inbox/Clippings/blogs to scrape.md` — **every line is a blog by default**
  (deep-scrape, no tag needed). Renamed from the old `TO SCRAPE.md` (2026-06-27); the user
  asked to treat the whole file as blogs so no per-line `[blog]` tag is required.
- `00_Inbox/Clippings/articles to process.md` — every line is a **single-page fetch** by
  default (unchanged behavior).

Per-line tags still work and override the list default:

- `https://blog.example.com [blog]` — scrape ALL posts (sitemap.xml first; RSS/Atom
  fallback). Default cap 200 posts; raise with `[blog:500]`. Posts over the cap page in
  over later runs.
- `https://site.com/the-guide [series]` — scrape the parts linked under the index's path.
- `https://one-article.com/post` — untagged: inherits the **list** default (blog for
  `blogs to scrape.md`, single-page for `articles to process.md`).

Code: `URL_LIST_DEFAULT_MODE` + `list_default_mode()` in `bin/collect_obsidian.py` key the
default off the file's basename; `iter_scrape_targets(text, default_mode)` applies it to
untagged lines; `obsidian_client.cmd_collect` passes the list's default through.

Each post becomes a `raw/_inbox/web-*.md` source tagged `scrape_seed: <seed>`. Dedup is
by `source_url` — re-scraping a blog only adds genuinely new posts (`scrape_seed`'s
dedup check runs BEFORE fetching, so re-runs are cheap: re-read the sitemap, fetch only
new URLs).

## Watch-mode vs consume-mode lists (2026-06-27)

A url-list is either **watch-mode** or **consume-mode**, keyed by basename in
`collect_obsidian.WATCH_LISTS`:

- `blogs to scrape.md` — **watch-mode**: blog seeds STAY in the file permanently. Every
  scheduled collect re-scrapes them and picks up new posts. `reapable()` never adds a
  watch-list seed to `seed_strikes`, even when all its current posts are
  `corpus_ingested` (`is_watch_list()` guard). This is how the corpus keeps collecting
  new articles from a blog as they're published.
- `articles to process.md` — **consume-mode**: a line IS struck once its source is
  `corpus_ingested` (the seed line is struck only when EVERY one of a seed's posts is
  ingested). One-and-done.

So for a watch list, "remove the processed line" is intentionally NOT done — removing a
blog would stop watching it. To stop watching a blog, delete its line by hand.

## Backfill control: seen-URL ledger + low cap (2026-06-28)

A watch list catches *new* posts; it should not dump every blog's back-catalogue into
the corpus. Two guards keep it incremental:

- **Per-blog cap `DEFAULT_BLOG_CAP = 25`** (down from 200) — the scrape depth per blog on
  any run. Explicit `[blog:N]` still overrides. Adding a new blog backfills ~25 posts, not
  its whole archive.
- **Seen-URL ledger `raw/.blog_seen_urls.txt`** (gitignored) — `scrape_blog.load_seen()` +
  `_post_collected()` treat a URL as collected if it's in the ledger OR on disk. This lets
  a one-time archive dump be **shelved**: write its URLs to the ledger, delete the content
  files from `raw/_inbox`, and forward-watch still skips them (no re-scrape) while only
  genuinely new posts get ingested.

**Precedent (2026-06-28):** a watch-list grew ~22→~101 seeds; one collect run scraped
**8,818** posts (→ ~10k un-ingested in `raw/_inbox`, ~175 nights at `--max 50`). Decision:
shelve the whole backfill (10,040 URLs → ledger, files deleted; `raw/_inbox` 11,104→1,064),
keep forward-watch, lower the cap. Reversible — to backfill a specific blog, remove its
URLs from the ledger and re-scrape.

> **Known limitation (follow-up):** discovery is sitemap-first in document order, which is
> not guaranteed newest-first. With a low cap this can keep the *wrong* slice (oldest) for
> a blog whose sitemap is oldest-first. An RSS/feed-first (newest-first) discovery order
> would make the cap reliably keep the most recent posts — not yet implemented.

Reaping (the strike, plus staging ingested vault-note deletions) runs nightly via
`scheduled_run.py` → `obsidian_client.py reap`. JS-only blogs with no sitemap/RSS scrape 0
posts and keep their seed (logged), pending browser-automation support.

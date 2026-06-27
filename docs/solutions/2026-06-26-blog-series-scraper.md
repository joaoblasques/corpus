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

Each post becomes a `raw/_inbox/web-*.md` source tagged `scrape_seed: <seed>`. The seed
line is struck from its list file only once EVERY one of its posts is `corpus_ingested`
(so multi-run / paged scrapes are safe). Dedup is by `source_url` — re-tagging a blog
later only adds new posts.

Reaping (the strike, plus staging ingested vault-note deletions) runs nightly via
`scheduled_run.py` → `obsidian_client.py reap`. JS-only blogs with no sitemap/RSS scrape 0
posts and keep their seed (logged), pending browser-automation support.

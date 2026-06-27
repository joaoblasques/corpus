---
module: collectors
tags: [obsidian, blog, scraping, reaping]
problem_type: feature
---

# Blog / series deep-scraper (TO SCRAPE tags)

Lines in the vault's `00_Inbox/Clippings/TO SCRAPE.md` accept an optional trailing tag:

- `https://blog.example.com [blog]` — scrape ALL posts (sitemap.xml first; RSS/Atom
  fallback). Default cap 200 posts; raise with `[blog:500]`. Posts over the cap page in
  over later runs.
- `https://site.com/the-guide [series]` — scrape the parts linked under the index's path.
- `https://one-article.com/post` — untagged: single-page fetch (unchanged).

Each post becomes a `raw/_inbox/web-*.md` source tagged `scrape_seed: <seed>`. The seed
line is struck from `TO SCRAPE.md` only once EVERY one of its posts is `corpus_ingested`
(so multi-run / paged scrapes are safe). Dedup is by `source_url` — re-tagging a blog
later only adds new posts.

Reaping (the strike, plus staging ingested vault-note deletions) runs nightly via
`scheduled_run.py` → `obsidian_client.py reap`. JS-only blogs with no sitemap/RSS scrape 0
posts and keep their seed (logged), pending browser-automation support.

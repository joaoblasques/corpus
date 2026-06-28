---
module: collectors
tags: [github, discovery, reaping, search-api]
problem_type: feature
---

# GitHub discover-and-star front-end

The GitHub collector now has a discovery front-end. Each nightly run, BEFORE the
collect leg, `github_client.py discover`:

1. searches GitHub (`/search/repositories`, sorted by stars desc) for each topic
   in `collect_github.DOMAIN_TOPICS` (ai-engineering / data-engineering / mlops /
   software-engineering; ai-business / trading / blockchain / productivity are
   excluded as noisier);
2. filters to repos with `stars >= 500` and `pushed` within 365 days;
3. drops repos already in the corpus (github ledger via `already_collected`) or
   already starred;
4. ranks the rest by stars and **stars** the top `DISCOVER_LIMIT` (10).

The existing pipeline finishes the loop the same run: collect (`cmd_run` sees the
new stars) -> ingest -> `github_client.py reap` un-stars them. So discovered repos
flow in and end up un-starred; the ledger remembers them, so they're never
re-discovered.

Defaults are constants in `collect_github.py`: `DISCOVER_MIN_STARS=500`,
`DISCOVER_PUSHED_WITHIN_DAYS=365`, `DISCOVER_LIMIT=10`, `DISCOVER_PER_TOPIC=15`.
`star()` mirrors `unstar()` (PUT vs DELETE /user/starred/{repo}); the `-X METHOD`
HTTPS transport already supported both. Failure-isolated in the nightly; fails
closed (stars nothing) when gh is unavailable. Run `github_client.py discover
--dry-run` to preview picks without starring.

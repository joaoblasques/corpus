# GitHub Discover-and-Star — Design

**Date:** 2026-06-28
**Status:** approved (design)

## Goal

Add a **discovery front-end** to the GitHub collector: before the existing
collect step, search GitHub for the most-starred repos in topics aligned to the
corpus's technical domains, **star** up to ~10 new ones, and let the existing
pipeline (collect → ingest → un-star reaper) carry them the rest of the way.

The user's manual workflow today is: star a repo → the nightly collects it →
ingests it → the reaper un-stars it. This feature automates the *front* of that
loop (find + star), reusing the entire back half unchanged.

## Decisions (locked with the user)

- **Search scope:** topics derived from the corpus's active technical domains
  (not globally-most-starred, which is generic bootcamp lists).
- **Volume/cadence:** ~10 new repos per run, in the nightly 2am `scheduled_run`.
- **Loop:** fully automated — search → star → collect → ingest → un-star, same run.
  Stars are momentary; the user's star list stays clean.
- **Quality bar (defaults):** skip repos already in the corpus; require
  `pushed` within ~12 months; `stars >= 500`.
- **Excluded domains:** ai-business, trading, blockchain, productivity are NOT
  auto-searched (noisier on GitHub). Map covers ai-engineering, data-engineering,
  mlops, software-engineering.

## Architecture

All new logic lives in the two existing GitHub modules; the nightly gains one
pre-step. No new long-lived state — dedup rides the existing **github ledger**
(`automation/state/github_digested.txt`, durable across un-starring) plus the
live starred list.

### `bin/collect_github.py` (pure logic + config)

```python
# Curated domain -> GitHub topics map. Editable; tracks active technical domains.
DOMAIN_TOPICS = {
    "ai-engineering": ["llm", "large-language-models", "ai-agents", "rag",
                       "prompt-engineering", "mcp", "agentic-ai", "llmops"],
    "data-engineering": ["data-engineering", "dbt", "apache-spark",
                         "apache-airflow", "etl", "data-pipeline", "duckdb"],
    "mlops": ["mlops", "model-serving", "feature-store", "machine-learning-operations"],
    "software-engineering": ["distributed-systems", "developer-tools", "observability"],
}
DISCOVER_MIN_STARS = 500
DISCOVER_PUSHED_WITHIN_DAYS = 365
DISCOVER_LIMIT = 10          # new repos to star per run
DISCOVER_PER_TOPIC = 15      # top results pulled per topic before global dedup/rank

def discover_topics(topic_map=None) -> list[str]:
    """Flat, sorted, deduped topic list from the domain map."""

def rank_candidates(candidates: dict, starred: set, already) -> list[tuple[str, int]]:
    """candidates {full_name: stars} -> [(full_name, stars)] sorted by stars desc,
    dropping repos already in the corpus (already(full_name) True) or already
    starred. `already` is a callable (collect_github.already_collected)."""
```

### `bin/github_client.py` (transport + CLI)

```python
def search_repos(topic, *, min_stars, pushed_after, per_page=DISCOVER_PER_TOPIC, _run=None) -> list[dict]:
    """GET /search/repositories?q=topic:<t> stars:>=<min> pushed:>=<date>&sort=stars&order=desc.
    Returns [{full_name, stars, pushed_at}]; [] on error. q is URL-encoded."""

def star(full_name, *, _run=None) -> bool:
    """PUT /user/starred/{owner}/{repo} -> 204. Mirror of unstar(). Idempotent."""

def cmd_discover(args) -> int:
    """gh_available gate; for each topic search_repos(); merge into {full_name: max stars};
    rank_candidates() against list_starred() + cg.already_collected; star the top
    DISCOVER_LIMIT; print {"discovered","fresh","count","starred":[...],"dry_run"}.
    --dry-run stars nothing."""
```

`_http_api` already supports `-X METHOD` (added for the un-star DELETE), so the
PUT for `star()` needs no transport change.

### `bin/scheduled_run.py` (nightly wiring)

In `run_collectors`, immediately **before** the existing GitHub collect block,
add a `github_discover` step (its own try/except; failure isolated, never aborts
the run). Result stored under `results["github_discover"]`, which is already
surfaced via `build_summary`'s `collectors` passthrough.

## Data flow (one nightly run)

1. `run_collectors` → **discover**: search topics → star ≤10 new repos.
2. `run_collectors` → **github collect** (`cmd_run`): the freshly-starred repos
   are now in `list_starred()` and not `already_collected` → digested to `raw/_inbox`.
3. ingest: digests → corpus pages + `corpus_ingested` stamp.
4. `run_github_reap` (`cmd_reap`): un-stars the now-ingested repos.

Net: discovered repos flow in and end up un-starred; the github ledger remembers
them, so they're never re-discovered.

## Edge cases

- **Dedup durability:** a repo discovered→starred→ingested→un-starred in a past
  run is `is_digested` in the ledger forever → `already_collected` True → never
  re-picked. Survives raw-file pruning.
- **Ingest failure:** a discovered repo collected but not yet ingested stays
  starred (reaper gates on `corpus_ingested`) until a later run ingests it. Fine.
- **Search rate limit:** authenticated search is 30 req/min; ~25 topic searches/run
  is well under. No throttling expected.
- **Idempotent star:** re-`star()`ing an in-flight repo is a no-op 204; harmless.
- **No candidates / search down:** stars nothing, returns count 0. Fails closed.

## Testing

- `search_repos`: mock `_gh` → search JSON → assert parsed `{full_name, stars}`.
- `star`: assert PUT to `user/starred/{fn}`, True on rc 0 / False on rc 1.
- `_http_api` PUT: assert method PUT + 204 → rc 0 (mirror the DELETE test).
- `discover_topics` / `rank_candidates`: pure-function unit tests (dedup across
  topics, drop already-collected + already-starred, sort by stars, limit).
- `cmd_discover`: stars top-N fresh; skips already-collected + already-starred;
  `--dry-run` stars nothing; not-configured gate.
- `run_collectors`: `github_discover` leg invoked before the github collect leg.

## Out of scope (v1)

- Per-domain or env-tunable limits/floors (constants for now).
- A user-maintained queries file (the "Both" option) — can layer on later.
- Trending/recency-weighted ranking beyond stars + the pushed filter.

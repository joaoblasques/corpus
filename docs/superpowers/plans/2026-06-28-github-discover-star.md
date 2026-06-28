# GitHub Discover-and-Star Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Have the GitHub collector auto-discover the most-starred repos in the corpus's technical domains, star up to ~10 new ones each nightly run, and let the existing collect → ingest → un-star pipeline carry them the rest of the way.

**Architecture:** Two new pure functions + a config map in `bin/collect_github.py`; two new transport functions + a `discover` CLI subcommand in `bin/github_client.py`; one new pre-step wired into `run_collectors` in `bin/scheduled_run.py`, ahead of the existing github collect leg. Dedup rides the existing github ledger (durable across un-starring) plus the live starred set. No new persistent state.

**Tech Stack:** Python 3 stdlib (`urllib`, `json`, `datetime`, `argparse`); the existing `_gh`/`_http_api` transport (already supports `-X METHOD`); pytest with injected `_run`/`_opener`/monkeypatch seams (no network in tests).

## Global Constraints

- **No network in tests.** Every test injects `_run=` (gh-CLI subprocess seam), `_opener=` (HTTPS seam), or monkeypatches module-level functions. Never hit GitHub.
- **Fail closed.** Search/transport errors return `[]`/`False`/`0`; `cmd_discover` stars nothing rather than raising. The nightly leg is failure-isolated (its own try/except) and never aborts the run.
- **Dedup is durable.** A repo already in the corpus (github ledger `is_digested` via `cg.already_collected`) or already starred is never re-picked.
- **Defaults (constants, not tunable in v1):** `DISCOVER_MIN_STARS = 500`, `DISCOVER_PUSHED_WITHIN_DAYS = 365`, `DISCOVER_LIMIT = 10`, `DISCOVER_PER_TOPIC = 15`.
- **Existing patterns:** mirror `unstar()` for `star()`; mirror `cmd_reap`/`reap` subparser for `cmd_discover`/`discover`; mirror the github collect leg for the discover leg. Match surrounding style (no new deps, `# noqa: BLE001` on broad excepts).
- Run the repo's tests with `python -m pytest` from the repo root `/Users/jonasblasques/Dev/corpus`.

---

### Task 1: Domain→topics map + pure ranking helpers (`collect_github.py`)

**Files:**
- Modify: `bin/collect_github.py` (add constants + two functions after `reapable`, ~line 71)
- Test: `tests/test_collect_github.py`

**Interfaces:**
- Consumes: nothing new.
- Produces:
  - `DOMAIN_TOPICS: dict[str, list[str]]`
  - `DISCOVER_MIN_STARS = 500`, `DISCOVER_PUSHED_WITHIN_DAYS = 365`, `DISCOVER_LIMIT = 10`, `DISCOVER_PER_TOPIC = 15`
  - `discover_topics(topic_map=None) -> list[str]` — flat, sorted, deduped topics
  - `rank_candidates(candidates: dict, starred: set, already) -> list[tuple[str, int]]` — `(full_name, stars)` sorted by stars desc, dropping `fn in starred` or `already(fn)` truthy. `already` is a callable (in production `already_collected`).

- [ ] **Step 1: Write the failing tests**

Add to `tests/test_collect_github.py`:

```python
def test_discover_topics_flat_sorted_deduped():
    tm = {"a": ["llm", "rag"], "b": ["rag", "mlops"]}
    assert cg.discover_topics(tm) == ["llm", "mlops", "rag"]   # deduped + sorted


def test_discover_topics_defaults_to_domain_map():
    out = cg.discover_topics()
    assert "llm" in out and out == sorted(set(out))   # uses DOMAIN_TOPICS, sorted/deduped


def test_rank_candidates_sorts_by_stars_desc():
    cands = {"o/a": 100, "o/b": 900, "o/c": 500}
    out = cg.rank_candidates(cands, starred=set(), already=lambda fn: False)
    assert out == [("o/b", 900), ("o/c", 500), ("o/a", 100)]


def test_rank_candidates_drops_starred_and_already_collected():
    cands = {"o/a": 100, "o/b": 900, "o/c": 500}
    out = cg.rank_candidates(cands, starred={"o/b"}, already=lambda fn: fn == "o/a")
    assert out == [("o/c", 500)]   # o/b starred, o/a already in corpus
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest tests/test_collect_github.py -k "discover_topics or rank_candidates" -v`
Expected: FAIL with `AttributeError: module 'collect_github' has no attribute 'discover_topics'`.

- [ ] **Step 3: Add the constants + functions**

In `bin/collect_github.py`, after the `reapable(...)` function (after line 71), add:

```python
# --- Discovery: find the most-starred repos in the corpus's technical domains ---
# Curated domain -> GitHub topics map. Editable; tracks active technical domains.
# ai-business / trading / blockchain / productivity are intentionally excluded
# (noisier on GitHub).
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


def discover_topics(topic_map=None) -> list:
    """Flat, sorted, deduped topic list from the domain map."""
    tm = topic_map if topic_map is not None else DOMAIN_TOPICS
    return sorted({t for topics in tm.values() for t in topics})


def rank_candidates(candidates: dict, starred: set, already) -> list:
    """`{full_name: stars}` -> `[(full_name, stars)]` sorted by stars desc, dropping
    repos already starred or already in the corpus. `already` is a callable
    (full_name -> bool); in production it is `already_collected`."""
    fresh = [(fn, stars) for fn, stars in candidates.items()
             if fn not in starred and not already(fn)]
    fresh.sort(key=lambda t: t[1], reverse=True)
    return fresh
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python -m pytest tests/test_collect_github.py -k "discover_topics or rank_candidates" -v`
Expected: PASS (4 tests).

- [ ] **Step 5: Commit**

```bash
git add bin/collect_github.py tests/test_collect_github.py
git commit -m "feat(github): domain-topics map + discover_topics/rank_candidates helpers"
```

---

### Task 2: `star()` + `_http_api` PUT transport (`github_client.py`)

**Files:**
- Modify: `bin/github_client.py` (add `star()` directly after `unstar()`, ~line 167)
- Test: `tests/test_github_client.py`

**Interfaces:**
- Consumes: existing `_gh`, `_http_api`, `_Resp`.
- Produces: `star(full_name: str, *, _run=None) -> bool` — `PUT /user/starred/{full_name}`, True iff returncode 0. Idempotent (GitHub returns 204).

Note: `_http_api`/`_parse_api_args` already pass `-X METHOD` through (added for `unstar`'s DELETE); the PUT test confirms it.

- [ ] **Step 1: Write the failing tests**

Add to `tests/test_github_client.py`:

```python
def test_star_issues_put_and_returns_true():
    calls = {}

    def fake_run(argv, **kw):
        calls["argv"] = argv
        return gc._Resp(0, "")

    assert gc.star("owner/repo", _run=fake_run) is True
    assert calls["argv"] == ["gh", "api", "-X", "PUT", "user/starred/owner/repo"]


def test_star_returns_false_on_failure():
    assert gc.star("owner/repo", _run=lambda argv, **kw: gc._Resp(1, "")) is False


def test_http_api_put_sends_put_method_and_handles_204():
    seen = {}

    class _Ctx:
        def __enter__(self_):
            class _R:
                headers = {}
                def read(self_inner):
                    return b""        # 204: empty body
            return _R()
        def __exit__(self_, *a):
            return False

    def fake_opener(req):
        seen["method"] = req.method
        seen["url"] = req.full_url
        return _Ctx()

    resp = gc._http_api(["api", "-X", "PUT", "user/starred/owner/repo"],
                        "tok", _opener=fake_opener)
    assert seen["method"] == "PUT"
    assert seen["url"].endswith("/user/starred/owner/repo")
    assert resp.returncode == 0 and resp.stdout == ""
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest tests/test_github_client.py -k "star or http_api_put" -v`
Expected: the `star` tests FAIL with `AttributeError: ... has no attribute 'star'`; `test_http_api_put_...` PASSES already (transport supports `-X` — that's the regression guard).

- [ ] **Step 3: Add `star()`**

In `bin/github_client.py`, directly after `unstar()` (after line 166), add:

```python
def star(full_name: str, *, _run=None) -> bool:
    """Star a repo: PUT /user/starred/{owner}/{repo}. GitHub returns 204 on success
    and is idempotent (starring an already-starred repo also succeeds). Mirror of
    unstar(). Returns True iff the call returned 0."""
    p = _gh(["api", "-X", "PUT", f"user/starred/{full_name}"], _run=_run)
    return getattr(p, "returncode", 1) == 0
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python -m pytest tests/test_github_client.py -k "star or http_api_put" -v`
Expected: PASS (3 tests).

- [ ] **Step 5: Commit**

```bash
git add bin/github_client.py tests/test_github_client.py
git commit -m "feat(github): star() (PUT /user/starred) + PUT transport guard"
```

---

### Task 3: `search_repos()` (`github_client.py`)

**Files:**
- Modify: `bin/github_client.py` (add `import urllib.parse` near the other imports ~line 23; add `search_repos()` after `star()`)
- Test: `tests/test_github_client.py`

**Interfaces:**
- Consumes: existing `_gh`; `cg.DISCOVER_PER_TOPIC` (Task 1).
- Produces: `search_repos(topic, *, min_stars, pushed_after, per_page=cg.DISCOVER_PER_TOPIC, _run=None) -> list[dict]` — each dict `{"full_name", "stars", "pushed_at"}`. `[]` on any error.

- [ ] **Step 1: Write the failing tests**

Add to `tests/test_github_client.py`:

```python
import json as _json

def test_search_repos_builds_query_and_parses_items():
    calls = {}

    def fake_run(argv, **kw):
        calls["argv"] = argv
        body = _json.dumps({"items": [
            {"full_name": "o/big", "stargazers_count": 900, "pushed_at": "2026-06-01T00:00:00Z"},
            {"full_name": "o/small", "stargazers_count": 600, "pushed_at": "2026-05-01T00:00:00Z"},
        ]})
        return gc._Resp(0, body)

    out = gc.search_repos("llm", min_stars=500, pushed_after="2025-06-28",
                          per_page=15, _run=fake_run)
    assert out == [
        {"full_name": "o/big", "stars": 900, "pushed_at": "2026-06-01T00:00:00Z"},
        {"full_name": "o/small", "stars": 600, "pushed_at": "2026-05-01T00:00:00Z"},
    ]
    # endpoint carries the search path + qualifiers (URL-encoded) + sort
    endpoint = calls["argv"][2]
    assert endpoint.startswith("search/repositories?q=")
    assert "topic" in endpoint and "stars" in endpoint and "pushed" in endpoint
    assert "sort=stars" in endpoint and "order=desc" in endpoint and "per_page=15" in endpoint


def test_search_repos_returns_empty_on_error():
    assert gc.search_repos("llm", min_stars=500, pushed_after="2025-06-28",
                           _run=lambda argv, **kw: gc._Resp(1, "")) == []


def test_search_repos_returns_empty_on_garbage_json():
    assert gc.search_repos("llm", min_stars=500, pushed_after="2025-06-28",
                           _run=lambda argv, **kw: gc._Resp(0, "not json")) == []
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest tests/test_github_client.py -k search_repos -v`
Expected: FAIL with `AttributeError: ... has no attribute 'search_repos'`.

- [ ] **Step 3: Add the import + `search_repos()`**

In `bin/github_client.py`, add to the import block (after `import urllib.request` ~line 24):

```python
import urllib.parse
```

Then add after `star()`:

```python
def search_repos(topic, *, min_stars, pushed_after, per_page=cg.DISCOVER_PER_TOPIC,
                 _run=None) -> list:
    """Top repos for one GitHub topic, sorted by stars desc:
    GET /search/repositories?q=topic:<t> stars:>=<min> pushed:>=<date>.
    Returns [{full_name, stars, pushed_at}]; [] on any error."""
    q = f"topic:{topic} stars:>={min_stars} pushed:>={pushed_after}"
    qs = ("q=" + urllib.parse.quote(q) +
          f"&sort=stars&order=desc&per_page={per_page}")
    p = _gh(["api", f"search/repositories?{qs}"], _run=_run)
    if getattr(p, "returncode", 1) != 0:
        return []
    try:
        data = json.loads(p.stdout)
    except Exception:  # noqa: BLE001
        return []
    out = []
    for it in (data.get("items") or []) if isinstance(data, dict) else []:
        fn = it.get("full_name")
        if fn:
            out.append({"full_name": fn, "stars": it.get("stargazers_count") or 0,
                        "pushed_at": it.get("pushed_at") or ""})
    return out
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python -m pytest tests/test_github_client.py -k search_repos -v`
Expected: PASS (3 tests).

- [ ] **Step 5: Commit**

```bash
git add bin/github_client.py tests/test_github_client.py
git commit -m "feat(github): search_repos() — top repos per topic via Search API"
```

---

### Task 4: `cmd_discover()` + `discover` subparser (`github_client.py`)

**Files:**
- Modify: `bin/github_client.py` (add `cmd_discover()` after `cmd_reap`, ~line 308; register the subparser in `_build_parser` after the `reap` parser, ~line 326)
- Test: `tests/test_github_client.py`

**Interfaces:**
- Consumes: `gh_available`, `search_repos`, `list_starred`, `star` (this module); `cg.discover_topics`, `cg.rank_candidates`, `cg.already_collected`, `cg.DISCOVER_*` (Tasks 1+3).
- Produces: `cmd_discover(args) -> int` (args has `.dry_run`). Prints JSON `{"discovered","fresh","count","starred":[...],"dry_run"}`. The `discover` subcommand: `github_client.py discover [--dry-run]`.

- [ ] **Step 1: Write the failing tests**

Add to `tests/test_github_client.py`:

```python
def test_cmd_discover_stars_top_fresh_and_skips_seen(monkeypatch, capsys):
    monkeypatch.setattr(gc, "gh_available", lambda *a, **k: True)
    # one search result set, reused per topic — dedup must collapse duplicates
    monkeypatch.setattr(gc, "search_repos", lambda topic, **kw: [
        {"full_name": "o/top", "stars": 900, "pushed_at": ""},
        {"full_name": "o/mid", "stars": 700, "pushed_at": ""},
        {"full_name": "o/seen", "stars": 800, "pushed_at": ""},     # already in corpus
        {"full_name": "o/starred", "stars": 950, "pushed_at": ""},  # already starred
    ])
    monkeypatch.setattr(gc, "list_starred", lambda *a, **k: [{"full_name": "o/starred"}])
    monkeypatch.setattr(gc.cg, "already_collected", lambda fn, *a, **k: fn == "o/seen")
    starred = []
    monkeypatch.setattr(gc, "star", lambda fn, **kw: starred.append(fn) or True)
    # limit to 2 picks so we assert ordering + cap
    monkeypatch.setattr(gc.cg, "DISCOVER_LIMIT", 2)

    rc = gc.cmd_discover(type("A", (), {"dry_run": False})())
    out = _json.loads(capsys.readouterr().out)
    assert rc == 0
    assert starred == ["o/top", "o/mid"]        # by stars desc, seen+starred dropped, capped at 2
    assert out["count"] == 2 and out["starred"] == ["o/top", "o/mid"]


def test_cmd_discover_dry_run_stars_nothing(monkeypatch, capsys):
    monkeypatch.setattr(gc, "gh_available", lambda *a, **k: True)
    monkeypatch.setattr(gc, "search_repos", lambda topic, **kw: [
        {"full_name": "o/a", "stars": 600, "pushed_at": ""}])
    monkeypatch.setattr(gc, "list_starred", lambda *a, **k: [])
    monkeypatch.setattr(gc.cg, "already_collected", lambda fn, *a, **k: False)
    called = []
    monkeypatch.setattr(gc, "star", lambda fn, **kw: called.append(fn) or True)

    gc.cmd_discover(type("A", (), {"dry_run": True})())
    out = _json.loads(capsys.readouterr().out)
    assert called == []                          # dry-run stars nothing
    assert out["count"] == 1 and out["dry_run"] is True and out["starred"] == ["o/a"]


def test_cmd_discover_not_configured(monkeypatch, capsys):
    monkeypatch.setattr(gc, "gh_available", lambda *a, **k: False)
    gc.cmd_discover(type("A", (), {"dry_run": False})())
    out = _json.loads(capsys.readouterr().out)
    assert out["status"] == "not configured" and out["count"] == 0


def test_discover_subcommand_parses():
    args = gc._args(["discover", "--dry-run"])
    assert args.func is gc.cmd_discover and args.dry_run is True
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest tests/test_github_client.py -k "cmd_discover or discover_subcommand" -v`
Expected: FAIL with `AttributeError: ... has no attribute 'cmd_discover'`.

- [ ] **Step 3: Add `cmd_discover()` + register the subparser**

In `bin/github_client.py`, after `cmd_reap` (after line 308), add:

```python
def cmd_discover(args) -> int:
    """Pre-collect: search GitHub for the most-starred repos in the corpus's
    technical domains and star up to DISCOVER_LIMIT new ones, so the existing
    collect -> ingest -> un-star pipeline picks them up this same run. Skips repos
    already in the corpus (github ledger) or already starred. Fails closed: if gh
    is unavailable, stars nothing."""
    if not gh_available():
        print(json.dumps({"status": "not configured", "starred": [], "count": 0}))
        return 0
    pushed_after = (datetime.date.today()
                    - datetime.timedelta(days=cg.DISCOVER_PUSHED_WITHIN_DAYS)).isoformat()
    candidates: dict = {}
    for topic in cg.discover_topics():
        for repo in search_repos(topic, min_stars=cg.DISCOVER_MIN_STARS,
                                 pushed_after=pushed_after):
            fn = repo["full_name"]
            candidates[fn] = max(candidates.get(fn, 0), repo["stars"])
    starred = {r["full_name"] for r in list_starred() if r.get("full_name")}
    fresh = cg.rank_candidates(candidates, starred, cg.already_collected)
    picks = fresh[:cg.DISCOVER_LIMIT]
    done = []
    for fn, _ in picks:
        if args.dry_run or star(fn):
            done.append(fn)
    print(json.dumps({"discovered": len(candidates), "fresh": len(fresh),
                      "count": len(done), "starred": done,
                      "dry_run": bool(args.dry_run)}))
    return 0
```

Then in `_build_parser`, after the `reap` parser block (after line 326, before `return p`), add:

```python
    pd = sub.add_parser("discover",
                        help="Search corpus-domain topics; star up to ~10 new top repos.")
    pd.add_argument("--dry-run", action="store_true",
                    help="List repos that would be starred; star nothing.")
    pd.set_defaults(func=cmd_discover)
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python -m pytest tests/test_github_client.py -k "cmd_discover or discover_subcommand" -v`
Expected: PASS (4 tests).

- [ ] **Step 5: Commit**

```bash
git add bin/github_client.py tests/test_github_client.py
git commit -m "feat(github): discover subcommand — star top corpus-domain repos"
```

---

### Task 5: Wire the discover leg into the nightly (`scheduled_run.py`)

**Files:**
- Modify: `bin/scheduled_run.py` (insert a `github_discover` block in `run_collectors` immediately before the `# --- GitHub: collect ...` block at line 288)
- Test: `tests/test_scheduled_run.py`

**Interfaces:**
- Consumes: in-scope `_run`, `results`, `BIN`, `COLLECTOR_TIMEOUT` (all already used by the adjacent github collect leg).
- Produces: `results["github_discover"]` = `{"status": "ok"|"failed", ...}`. It rides inside `run_collectors`'s return dict, which `build_summary` already surfaces under `collectors` — no `build_summary` change needed.

Ordering matters: discover stars new repos, then the github collect leg (which calls `list_starred`) picks them up the same run.

- [ ] **Step 1: Write the failing test**

Add to `tests/test_scheduled_run.py` (mirror the existing `run_collectors` github test style — find how other collector legs are tested in that file and match the `_run` dispatch fake):

```python
def test_run_collectors_runs_github_discover_before_collect():
    """The github_discover leg invokes `github_client.py discover` and runs before
    the github collect leg (so freshly-starred repos are collected the same run)."""
    order = []

    def fake_run(argv, **kw):
        # argv = [python, ".../<script>.py", subcommand, ...]
        script = Path(argv[1]).name
        sub = argv[2] if len(argv) > 2 else ""
        key = f"{script}:{sub}"
        order.append(key)
        payloads = {
            "github_client.py:discover": {"count": 3, "starred": ["o/a", "o/b", "o/c"]},
            "github_client.py:run": {"written": 1},
        }
        return types.SimpleNamespace(returncode=0,
                                     stdout=json.dumps(payloads.get(key, {})),
                                     stderr="")

    results = sr.run_collectors(_run=fake_run)
    assert results["github_discover"]["status"] == "ok"
    assert results["github_discover"]["starred"] == 3
    # discover precedes collect
    assert order.index("github_client.py:discover") < order.index("github_client.py:run")
```

(If `test_scheduled_run.py` lacks `import types`, add it. Confirm `run_collectors`'s signature accepts `_run=` — it does; other collector tests in this file already pass it.)

- [ ] **Step 2: Run the test to verify it fails**

Run: `python -m pytest tests/test_scheduled_run.py -k run_collectors_runs_github_discover -v`
Expected: FAIL with `KeyError: 'github_discover'`.

- [ ] **Step 3: Insert the discover leg**

In `bin/scheduled_run.py`, immediately before line 288 (`# --- GitHub: collect ...`), insert:

```python
    # --- GitHub: discover + star top repos in corpus domains (before collect) ---
    try:
        proc = _run(
            [sys.executable, str(BIN / "github_client.py"), "discover"],
            capture_output=True,
            text=True,
            timeout=COLLECTOR_TIMEOUT,
        )
        if proc.returncode != 0:
            results["github_discover"] = {
                "status": "failed",
                "error": proc.stderr.strip() or f"exit {proc.returncode}",
            }
        else:
            try:
                starred = json.loads(proc.stdout).get("count", 0)
            except (json.JSONDecodeError, AttributeError):
                starred = 0
            results["github_discover"] = {"status": "ok", "starred": starred}
    except Exception as exc:  # noqa: BLE001
        results["github_discover"] = {"status": "failed", "error": str(exc)}

```

- [ ] **Step 4: Run the test (and the github-collect regression test) to verify they pass**

Run: `python -m pytest tests/test_scheduled_run.py -k "github" -v`
Expected: PASS (the new discover test + the existing github collect tests still green).

- [ ] **Step 5: Commit**

```bash
git add bin/scheduled_run.py tests/test_scheduled_run.py
git commit -m "feat(github): wire discover leg into nightly run_collectors (pre-collect)"
```

---

### Task 6: Docs — record the discover front-end

**Files:**
- Modify: `docs/solutions/2026-06-26-blog-series-scraper.md`? No — github. Create: `docs/solutions/2026-06-28-github-discover-star.md`

**Interfaces:** none (docs only).

- [ ] **Step 1: Write the solution note**

Create `docs/solutions/2026-06-28-github-discover-star.md`:

```markdown
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
```

- [ ] **Step 2: Commit**

```bash
git add docs/solutions/2026-06-28-github-discover-star.md
git commit -m "docs(github): record the discover-and-star front-end"
```

---

## Self-Review

- **Spec coverage:** DOMAIN_TOPICS + discover_topics/rank_candidates (Task 1) ✓; star() + PUT transport (Task 2) ✓; search_repos (Task 3) ✓; cmd_discover + subparser, fail-closed gate, dry-run (Task 4) ✓; nightly wiring before collect (Task 5) ✓; defaults as constants ✓; dedup via ledger + starred set ✓; docs ✓. All spec sections map to a task.
- **Placeholder scan:** none — every step carries real code/commands.
- **Type consistency:** `search_repos` returns `{full_name, stars, pushed_at}`; `cmd_discover` reads `repo["full_name"]`/`repo["stars"]` ✓. `rank_candidates(candidates, starred, already)` signature identical in Task 1 and its Task 4 call ✓. `cg.DISCOVER_*` names identical across tasks ✓. `cmd_discover` prints `count` (read by the Task 5 wiring) ✓.

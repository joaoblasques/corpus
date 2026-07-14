# Diagnostic-Driven Deepen-Existing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Execute consolidation's deepen-existing path — integrate a coherent source-cluster into deepening its existing concept page (Opus writer that preserves existing cited claims + adds cited material), prioritized thinnest-page-first, fully reversible and provenance-guarded.

**Architecture:** Reuse the consolidation machinery. Add `consolidate.rank_deepen_candidates` (deterministic: clusters whose topic matches an existing page, scored `size/word_count`), `consolidate_prompts.deepen_prompt`, and in `consolidate_run.py` a `deepen_page` core (writer → deterministic citation-superset guard → fail-closed `gardener._critic_call` → stamp-or-restore) driven by a `run_deepen` pass exposed via `run --mode deepen`. Revert restores a saved pre-image of the page (no git dependency). The weekly cron stays unwired pending a supervised first run.

**Tech Stack:** Python 3.12 stdlib (re, json, subprocess, pathlib) + pytest. Headless `claude` via the existing `_headless` seam. No new dependencies.

## Global Constraints

- **Stdlib only**; no new deps.
- **PROVENANCE (§7):** every new claim in a deepened page cites a member source; ≤25-word quotes; never invent a claim absent from the members.
- **NEVER DROP EXISTING CONTENT:** the deepened page's set of footnote definitions (`[^id]:`) must be a SUPERSET of the original's — a deterministic guard rejects any deepen that drops one. The writer only ADDS/weaves; it must not rewrite away existing cited claims.
- **FULLY REVERSIBLE:** `deepen_page` saves the page's exact bytes before editing; on ANY failure (writer no-op, superset violation, critic reject, critic error) it restores those bytes and un-stamps members. No destructive state.
- **FAIL CLOSED:** superset violation OR critic reject/error/unparseable ⇒ restore + queue for human, never keep the edit.
- **No deletion of members** — they gain `consolidated_into: <target_page>` (kept). Reuses the existing `stamp_members`/`unstamp_members`/`_CONSOLIDATED_RE`.
- **Main-branch only; weekly/Opus** — deepen runs only via `run --mode deepen`; the weekly call site is NOT wired in this plan (gated on a supervised first run). No `scheduled_run.py` change here.
- **Writer/critic models:** writer `CONSOLIDATE_MODEL` (opus); critic `gardener._critic_call` (sonnet). Both already defined.
- **Tests never touch the real corpus or `claude`** — injected `_run`/`_critic` + `tmp_path` fixtures.

---

## File Structure

| File | Responsibility |
|---|---|
| `bin/consolidate.py` | ADD `rank_deepen_candidates(corpus, domain)` (+ `_find_target_page`, `_page_wordcount`). Pure; deterministic target matching + thinness score. |
| `bin/consolidate_prompts.py` | ADD `deepen_prompt(target_page_rel, topic, member_rel_paths)` (preserve-existing + integrate-new). Pure. |
| `bin/consolidate_run.py` | ADD `_footnote_targets`, `deepen_page` (core), `run_deepen` (ranked pass); extend `main` with `--mode {synthesize,deepen}`. |
| `tests/test_consolidate.py` | APPEND `rank_deepen_candidates` tests. |
| `tests/test_consolidate_prompts.py` | APPEND `deepen_prompt` tests. |
| `tests/test_consolidate_run.py` | APPEND `deepen_page` + `run_deepen` + `--mode deepen` tests. |

Existing signatures this plan builds on (do not change):
```python
# consolidate.py
build_clusters(corpus, domain, min_cluster=5) -> list[dict]      # {topic,domain,members,size}
existing_topic_keys(corpus, domain) -> set[str]                  # normalized concept/entity/synthesis keys
_norm(s) -> str
# consolidate_run.py
_headless(prompt, model, tools, *, _run=None) -> str
stamp_members(cluster, rel, corpus) -> int
unstamp_members(cluster, corpus) -> int
_member_sources_text(cluster, corpus) -> str
queue_reject(cluster, verdict, review_path) -> None
CONSOLIDATE_MODEL, CORPUS, REVIEW, LOCK
import gardener as gd  # gd._critic_call(page_path: Path, sources_text: str, *, _run=None) -> (bool, list)
```

---

### Task 1: `rank_deepen_candidates` (`consolidate.py`)

**Files:**
- Modify: `bin/consolidate.py` (append helpers + function)
- Test: `tests/test_consolidate.py` (append)

**Interfaces:**
- Consumes: `build_clusters`, `existing_topic_keys`, `_norm`, `_H1_RE`, `_TYPE_RE`.
- Produces: `rank_deepen_candidates(corpus: Path, domain: str, min_cluster: int = 4) -> list[dict]` — one dict per cluster whose topic matches an existing concept/entity/synthesis page: `{"topic","domain","members":[rel],"size","target_page":rel,"page_words","score"}` where `score = size / max(page_words, 1)`, sorted by `score` descending (thin page + big cluster first).

- [ ] **Step 1: Write the failing test**

```python
# tests/test_consolidate.py  (append)
def test_rank_deepen_candidates_matches_pages_and_scores_thin_first(tmp_path):
    corpus = tmp_path / "corpus"
    d = corpus / "ai-engineering"
    (d / "sources").mkdir(parents=True)
    # existing pages: 'openai' is THIN, 'prompt-engineering' is DEEP
    (d / "openai.md").write_text("---\ntype: entity\n---\n# OpenAI\n\n" + "word " * 40, encoding="utf-8")
    (d / "prompt-engineering.md").write_text(
        "---\ntype: concept\n---\n# Prompt Engineering\n\n" + "word " * 400, encoding="utf-8")
    # 3 sources tagged OpenAI, 3 tagged Prompt Engineering
    for i in range(3):
        (d / "sources" / f"o{i}.md").write_text(
            "---\ntype: source\ntags:\n  - source\n  - OpenAI\n---\n# s\nbody", encoding="utf-8")
        (d / "sources" / f"p{i}.md").write_text(
            "---\ntype: source\ntags:\n  - source\n  - Prompt Engineering\n---\n# s\nbody", encoding="utf-8")

    cands = co.rank_deepen_candidates(corpus, "ai-engineering", min_cluster=3)
    topics = [c["topic"] for c in cands]
    assert "openai" in topics and "prompt engineering" in topics
    # thin page (openai, ~40 words) outranks the deep page (prompt-engineering, ~400 words)
    assert topics[0] == "openai"
    top = cands[0]
    assert top["target_page"] == "ai-engineering/openai.md"
    assert top["size"] == 3 and top["page_words"] >= 40
    assert top["score"] > cands[topics.index("prompt engineering")]["score"]


def test_rank_deepen_skips_clusters_without_an_existing_page(tmp_path):
    corpus = tmp_path / "corpus"
    d = corpus / "ai-engineering"
    (d / "sources").mkdir(parents=True)
    for i in range(3):   # a cluster with NO matching page
        (d / "sources" / f"x{i}.md").write_text(
            "---\ntype: source\ntags:\n  - source\n  - Nonesuch\n---\n# s\nbody", encoding="utf-8")
    assert co.rank_deepen_candidates(corpus, "ai-engineering", min_cluster=3) == []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/Dev/corpus && python3 -m pytest tests/test_consolidate.py -k deepen -q -p no:cacheprovider`
Expected: FAIL — `AttributeError: module 'consolidate' has no attribute 'rank_deepen_candidates'`.

- [ ] **Step 3: Implement**

Append to `bin/consolidate.py`:
```python
def _page_wordcount(path: Path) -> int:
    t = path.read_text(encoding="utf-8", errors="ignore")
    body = t.split("---", 2)[-1] if t.startswith("---") else t
    return len(body.split())


def _find_target_page(corpus: Path, domain: str, topic: str) -> Path | None:
    """The concept/entity/synthesis page whose slug OR H1 title normalizes to `topic`."""
    key = _norm(topic)
    root = corpus / domain
    if not root.exists():
        return None
    for p in root.rglob("*.md"):
        if p.name == "README.md":
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        tm = _TYPE_RE.search(text)
        if not tm or tm.group(1) not in ("concept", "entity", "synthesis"):
            continue
        if _norm(p.stem) == key:
            return p
        body = text.split("---", 2)[-1] if text.startswith("---") else text
        hm = _H1_RE.search(body)
        if hm and _norm(hm.group(1)) == key:
            return p
    return None


def rank_deepen_candidates(corpus: Path, domain: str, min_cluster: int = 4) -> list[dict]:
    """Clusters whose topic already has a concept/entity/synthesis page, scored thinnest-first
    (score = cluster size / target page word count). These feed the deepen-existing pass."""
    existing = existing_topic_keys(corpus, domain)
    out = []
    for c in build_clusters(corpus, domain, min_cluster=min_cluster):
        if _norm(c["topic"]) not in existing:
            continue
        page = _find_target_page(corpus, domain, c["topic"])
        if page is None:
            continue
        words = _page_wordcount(page)
        out.append({"topic": c["topic"], "domain": domain, "members": c["members"],
                    "size": c["size"], "target_page": str(page.relative_to(corpus)),
                    "page_words": words, "score": c["size"] / max(words, 1)})
    out.sort(key=lambda c: c["score"], reverse=True)
    return out
```
(`_H1_RE` and `_TYPE_RE` already exist in `consolidate.py`.)

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ~/Dev/corpus && python3 -m pytest tests/test_consolidate.py -q -p no:cacheprovider`
Expected: PASS (all consolidate tests, incl. the 2 new).

- [ ] **Step 5: Real-data sanity + commit**

Run: `cd ~/Dev/corpus && python3 -c "import sys;sys.path.insert(0,'bin');import consolidate as co;from pathlib import Path; \
c=co.rank_deepen_candidates(Path('corpus'),'ai-engineering'); print('candidates',len(c)); \
print('top', c[0]['topic'], c[0]['target_page'], c[0]['page_words'],'words', c[0]['size'],'sources')"`
Expected: prints a non-zero candidate count; the top is a thin page with several sources (e.g. `openai`).
```bash
cd ~/Dev/corpus
git add bin/consolidate.py tests/test_consolidate.py
git commit -m "feat(consolidate): rank_deepen_candidates — thin-page-first deepen targets"
```

---

### Task 2: `deepen_prompt` (`consolidate_prompts.py`)

**Files:**
- Modify: `bin/consolidate_prompts.py` (append)
- Test: `tests/test_consolidate_prompts.py` (append)

**Interfaces:**
- Consumes: nothing.
- Produces: `deepen_prompt(target_page_rel: str, topic: str, member_rel_paths: list[str]) -> str`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_consolidate_prompts.py  (append)
def test_deepen_prompt_preserves_existing_and_integrates_new():
    p = cp.deepen_prompt("ai-engineering/openai.md", "openai",
                         ["ai-engineering/sources/o1.md", "ai-engineering/sources/o2.md"])
    assert "corpus/ai-engineering/openai.md" in p            # the exact file to edit
    assert "o1.md" in p and "o2.md" in p                      # member sources listed
    # must instruct: preserve existing, integrate new, cite, don't drop, don't invent
    low = p.lower()
    assert "preserve" in low or "keep" in low
    assert "do not" in low or "never" in low                 # a prohibition (drop/invent)
    assert "cite" in low and "footnote" in low
    assert "25" in p                                          # quote length limit
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/Dev/corpus && python3 -m pytest tests/test_consolidate_prompts.py -k deepen -q -p no:cacheprovider`
Expected: FAIL — `AttributeError: module 'consolidate_prompts' has no attribute 'deepen_prompt'`.

- [ ] **Step 3: Implement**

Append to `bin/consolidate_prompts.py`:
```python
def deepen_prompt(target_page_rel: str, topic: str, member_rel_paths: list[str]) -> str:
    members = "\n".join(f"- corpus/{m}" for m in member_rel_paths)
    return (
        f"Deepen the EXISTING corpus page on \"{topic}\" by integrating additional source-summary "
        f"pages into it. Edit EXACTLY this file in place: corpus/{target_page_rel}\n\n"
        f"Read the current page first, then read these member sources and weave their material in:\n"
        f"{members}\n\n"
        "Rules (from CLAUDE.md):\n"
        "- PRESERVE every existing claim and every existing footnote citation on the page — you may "
        "reorganize or expand prose, but do NOT remove or weaken any existing cited claim, and do "
        "NOT delete any existing [^footnote] definition.\n"
        "- ADD the new material from the member sources, each new non-trivial claim carrying a "
        "footnote [^n] citing the member it came from (reuse the members' own source citations). "
        "NEVER invent a claim absent from the page or the members. Keep any verbatim quote to 25 "
        "words max.\n"
        "- Keep the frontmatter (type/domain/etc.) and the page's H1 title. Impersonal, reference-"
        "dense. Do NOT edit any file other than this one page."
    )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ~/Dev/corpus && python3 -m pytest tests/test_consolidate_prompts.py -q -p no:cacheprovider`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
cd ~/Dev/corpus
git add bin/consolidate_prompts.py tests/test_consolidate_prompts.py
git commit -m "feat(consolidate): deepen_prompt — preserve existing claims, integrate new sources"
```

---

### Task 3: `deepen_page` core — writer + superset guard + critic + pre-image revert (`consolidate_run.py`)

**Files:**
- Modify: `bin/consolidate_run.py` (append)
- Test: `tests/test_consolidate_run.py` (append)

**Interfaces:**
- Consumes: `_headless`, `cp.deepen_prompt`, `CONSOLIDATE_MODEL`, `stamp_members`, `unstamp_members`, `_member_sources_text`, `queue_reject`, `gd._critic_call`.
- Produces:
  - `_footnote_targets(text: str) -> set[str]` — the set of footnote-definition ids (`[^id]:`) in a page.
  - `deepen_page(cluster: dict, target_rel: str, corpus: Path, review_path: Path, *, _run=None, _critic=None) -> dict` — `cluster` = `{topic,domain,members}`. Saves the page pre-image; runs the Opus writer on the target; then the citation-superset guard + critic; on pass → `stamp_members(cluster, target_rel, corpus)` and return `{"status":"deepened","page":target_rel,...}`; on writer-no-op → restore + `{"status":"no_change"}`; on superset-violation OR critic-fail/error → restore pre-image bytes, `unstamp_members`, `queue_reject`, return `{"status":"reverted",...}`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_consolidate_run.py  (append)
def _page(corpus, rel, text):
    p = corpus / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p

_ORIG = "---\ntype: entity\ndomain: ai-engineering\n---\n# OpenAI\n\nExisting claim.[^a]\n\n[^a]: [s](../x.md)\n"

def test_deepen_page_commits_on_pass(tmp_path):
    corpus = tmp_path / "corpus"
    _page(corpus, "ai-engineering/openai.md", _ORIG)
    _write_member(corpus, "ai-engineering/sources/o1.md")           # helper from earlier tasks
    cluster = {"topic": "openai", "domain": "ai-engineering",
               "members": ["ai-engineering/sources/o1.md"]}

    def fake_writer(cmd, **kw):
        # simulate the writer ADDING a cited claim while keeping [^a]
        pg = corpus / "ai-engineering/openai.md"
        pg.write_text(_ORIG.rstrip() + "\n\nNew claim.[^b]\n\n[^b]: [s](../y.md)\n", encoding="utf-8")
        p = type("P", (), {})(); p.stdout = json.dumps({"result": "ok"}); p.returncode = 0
        return p

    res = cr.deepen_page(cluster, "ai-engineering/openai.md", corpus, tmp_path / "rev.md",
                         _run=fake_writer, _critic=lambda pg, src: (True, []))
    assert res["status"] == "deepened"
    txt = (corpus / "ai-engineering/openai.md").read_text()
    assert "[^a]" in txt and "[^b]" in txt                          # kept old, added new
    assert "consolidated_into:" in (corpus / "ai-engineering/sources/o1.md").read_text()

def test_deepen_page_reverts_and_restores_on_dropped_citation(tmp_path):
    corpus = tmp_path / "corpus"
    _page(corpus, "ai-engineering/openai.md", _ORIG)
    _write_member(corpus, "ai-engineering/sources/o1.md")
    cluster = {"topic": "openai", "domain": "ai-engineering",
               "members": ["ai-engineering/sources/o1.md"]}

    def dropping_writer(cmd, **kw):
        # BAD: rewrites the page and DROPS the existing [^a] footnote
        (corpus / "ai-engineering/openai.md").write_text(
            "---\ntype: entity\n---\n# OpenAI\n\nOnly new stuff.[^b]\n\n[^b]: [s](../y.md)\n", encoding="utf-8")
        p = type("P", (), {})(); p.stdout = json.dumps({"result": "ok"}); p.returncode = 0
        return p

    res = cr.deepen_page(cluster, "ai-engineering/openai.md", corpus, tmp_path / "rev.md",
                         _run=dropping_writer, _critic=lambda pg, src: (True, []))
    assert res["status"] == "reverted"
    assert (corpus / "ai-engineering/openai.md").read_text() == _ORIG   # restored byte-for-byte
    assert "consolidated_into:" not in (corpus / "ai-engineering/sources/o1.md").read_text()

def test_deepen_page_reverts_on_critic_fail(tmp_path):
    corpus = tmp_path / "corpus"
    _page(corpus, "ai-engineering/openai.md", _ORIG)
    _write_member(corpus, "ai-engineering/sources/o1.md")
    cluster = {"topic": "openai", "domain": "ai-engineering",
               "members": ["ai-engineering/sources/o1.md"]}

    def ok_writer(cmd, **kw):
        (corpus / "ai-engineering/openai.md").write_text(
            _ORIG.rstrip() + "\n\nFabricated.[^b]\n\n[^b]: [s](../y.md)\n", encoding="utf-8")
        p = type("P", (), {})(); p.stdout = json.dumps({"result": "ok"}); p.returncode = 0
        return p

    res = cr.deepen_page(cluster, "ai-engineering/openai.md", corpus, tmp_path / "rev.md",
                         _run=ok_writer, _critic=lambda pg, src: (False, ["fabricated"]))
    assert res["status"] == "reverted"
    assert (corpus / "ai-engineering/openai.md").read_text() == _ORIG   # restored
```

(Note: `_write_member` is the helper defined in the existing `tests/test_consolidate_run.py`; reuse it. `json` is already imported there.)

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/Dev/corpus && python3 -m pytest tests/test_consolidate_run.py -k deepen -q -p no:cacheprovider`
Expected: FAIL — `AttributeError: module 'consolidate_run' has no attribute 'deepen_page'`.

- [ ] **Step 3: Implement**

Append to `bin/consolidate_run.py`:
```python
_FOOTNOTE_DEF_RE = re.compile(r"^\[\^([^\]]+)\]:", re.M)


def _footnote_targets(text: str) -> set:
    """The set of footnote-definition ids (`[^id]:`) declared in a page."""
    return set(_FOOTNOTE_DEF_RE.findall(text))


def deepen_page(cluster: dict, target_rel: str, corpus: Path, review_path: Path,
                *, _run=None, _critic=None) -> dict:
    target = corpus / target_rel
    if not target.exists():
        return {"status": "no_change", "reason": "target missing"}
    pre = target.read_text(encoding="utf-8", errors="ignore")   # saved pre-image for revert

    prompt = cp.deepen_prompt(target_rel, cluster["topic"], cluster["members"])
    _headless(prompt, CONSOLIDATE_MODEL, ["Read", "Write", "Edit"], _run=_run)
    post = target.read_text(encoding="utf-8", errors="ignore")

    if post == pre:                                             # writer did nothing
        return {"status": "no_change", "page": target_rel}

    def _restore(reason):
        target.write_text(pre, encoding="utf-8")               # byte-for-byte restore
        unstamp_members(cluster, corpus)
        queue_reject({**cluster, "size": len(cluster["members"])},
                     {"mode": "deepen-existing", "reason": reason}, review_path)
        return {"status": "reverted", "reason": reason}

    # deterministic guard: the deepened page must keep every original footnote
    dropped = _footnote_targets(pre) - _footnote_targets(post)
    if dropped:
        return _restore("dropped citations: " + ", ".join(sorted(dropped))[:120])

    critic = _critic if _critic is not None else (lambda pg, src: gd._critic_call(Path(pg), src))
    try:
        ok, issues = critic(str(target), _member_sources_text(cluster, corpus))
    except Exception as exc:  # noqa: BLE001 — fail CLOSED
        ok, issues = False, [f"critic error: {exc}"]
    if not ok:
        return _restore("critic: " + "; ".join(issues)[:140])

    stamped = stamp_members(cluster, target_rel, corpus)
    return {"status": "deepened", "page": target_rel, "members_stamped": stamped,
            "added_words": len(post.split()) - len(pre.split())}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ~/Dev/corpus && python3 -m pytest tests/test_consolidate_run.py -q -p no:cacheprovider`
Expected: PASS (all prior + the 3 new).

- [ ] **Step 5: Commit**

```bash
cd ~/Dev/corpus
git add bin/consolidate_run.py tests/test_consolidate_run.py
git commit -m "feat(consolidate): deepen_page — writer + citation-superset guard + critic + pre-image revert"
```

---

### Task 4: `run_deepen` + `--mode deepen` CLI (`consolidate_run.py`)

**Files:**
- Modify: `bin/consolidate_run.py` (append `run_deepen`; extend `main`)
- Test: `tests/test_consolidate_run.py` (append)

**Interfaces:**
- Consumes: `co.rank_deepen_candidates`, `deepen_page`, `sr._on_main/acquire_lock/release_lock`.
- Produces:
  - `run_deepen(corpus: Path, domain: str, max_candidates: int, *, dry_run: bool = False, _run=None, _critic=None, review_path: Path | None = None) -> dict` — ranks deepen candidates; for the top `max_candidates`, calls `deepen_page`; returns `{"status":"ok","deepened","reverted","no_change","candidates_seen"}`.
  - `main` gains `--mode {synthesize,deepen}` (default `synthesize`): `deepen` routes to `run_deepen`, else the existing `run_consolidation`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_consolidate_run.py  (append)
def test_run_deepen_dry_run_ranks_without_writing(tmp_path, monkeypatch):
    corpus = tmp_path / "corpus"
    d = corpus / "ai-engineering"; (d / "sources").mkdir(parents=True)
    d.joinpath("openai.md").write_text("---\ntype: entity\n---\n# OpenAI\n\n" + "w " * 30, encoding="utf-8")
    for i in range(4):
        (d / "sources" / f"o{i}.md").write_text(
            "---\ntype: source\ntags:\n  - source\n  - OpenAI\n---\n# s\nbody", encoding="utf-8")
    res = cr.run_deepen(corpus, "ai-engineering", 3, dry_run=True)
    assert res["status"] == "ok" and res["candidates_seen"] >= 1
    assert res["deepened"] == 0                          # dry-run writes nothing
    assert "# OpenAI\n\nw w" in (d / "openai.md").read_text()   # page untouched

def test_main_mode_deepen_skips_when_not_on_main(monkeypatch, capsys):
    monkeypatch.setattr(cr.sr, "_on_main", lambda *a, **k: False)
    rc = cr.main(["run", "--mode", "deepen"])
    assert rc == 0 and json.loads(capsys.readouterr().out)["reason"] == "not_on_main"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/Dev/corpus && python3 -m pytest tests/test_consolidate_run.py -k "run_deepen or mode_deepen" -q -p no:cacheprovider`
Expected: FAIL — `AttributeError: module 'consolidate_run' has no attribute 'run_deepen'`.

- [ ] **Step 3: Implement**

Append `run_deepen` to `bin/consolidate_run.py`:
```python
def run_deepen(corpus: Path, domain: str, max_candidates: int, *, dry_run: bool = False,
               _run=None, _critic=None, review_path: Path | None = None) -> dict:
    review = review_path if review_path is not None else REVIEW
    ranked = co.rank_deepen_candidates(corpus, domain)
    t = {"status": "ok", "deepened": 0, "reverted": 0, "no_change": 0,
         "candidates_seen": len(ranked)}
    for cand in ranked[:max_candidates]:
        if dry_run:
            continue
        cluster = {"topic": cand["topic"], "domain": cand["domain"], "members": cand["members"]}
        res = deepen_page(cluster, cand["target_page"], corpus, review,
                          _run=_run, _critic=_critic)
        t[res["status"]] = t.get(res["status"], 0) + 1
    return t
```

Replace the `main` function's argparse + dispatch to add `--mode`:
```python
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Consolidate source clusters (synthesize | deepen).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    pr = sub.add_parser("run")
    pr.add_argument("--domain", default="ai-engineering")
    pr.add_argument("--max-clusters", type=int, default=3)
    pr.add_argument("--mode", choices=["synthesize", "deepen"], default="synthesize")
    pr.add_argument("--dry-run", action="store_true")
    pr.add_argument("--lock-path", default=LOCK, type=Path)
    args = ap.parse_args(argv)

    def _go(dry):
        if args.mode == "deepen":
            return run_deepen(CORPUS, args.domain, args.max_clusters, dry_run=dry)
        return run_consolidation(CORPUS, args.domain, args.max_clusters, dry_run=dry)

    if not sr._on_main():
        print(json.dumps({"status": "skipped", "reason": "not_on_main"})); return 0
    if args.dry_run:
        print(json.dumps(_go(True))); return 0
    if not sr.acquire_lock(args.lock_path):
        print(json.dumps({"status": "skipped", "reason": "lock_held"})); return 0
    try:
        print(json.dumps(_go(False))); return 0
    finally:
        sr.release_lock(args.lock_path)
```

- [ ] **Step 4: Run tests + full suite**

Run: `cd ~/Dev/corpus && python3 -m pytest tests/test_consolidate_run.py tests/test_consolidate.py tests/test_consolidate_prompts.py -q -p no:cacheprovider`
Expected: PASS (all green).
Run: `cd ~/Dev/corpus && python3 bin/consolidate_run.py run --mode deepen --dry-run` (on a feature branch this prints `{"status":"skipped","reason":"not_on_main"}` — the on-main guard; that's correct). To see the real dry-run, call the function directly:
`cd ~/Dev/corpus && python3 -c "import sys;sys.path.insert(0,'bin');import consolidate_run as cr;from pathlib import Path;print(cr.run_deepen(Path('corpus'),'ai-engineering',3,dry_run=True))"`
Expected: `candidates_seen` non-zero, `deepened: 0`.

- [ ] **Step 5: Commit**

```bash
cd ~/Dev/corpus
git add bin/consolidate_run.py tests/test_consolidate_run.py
git commit -m "feat(consolidate): run_deepen pass + run --mode deepen CLI"
```

---

## Supervised first run (after the plan is implemented + reviewed)

Do NOT wire the weekly cron until one supervised real run passes. On `main`:
```bash
cd ~/Dev/corpus
python3 bin/consolidate_run.py run --domain ai-engineering --mode deepen --max-clusters 1
git diff -- corpus/                     # inspect: existing claims + footnotes intact, new cited material added
python3 bin/okf_lint.py                 # must stay 0 violations
```
Inspect the deepened page's diff by eye: every original `[^footnote]` still present, new material carries citations, no existing claim weakened. If anything looks off, `git checkout -- corpus/<page>.md` and refine the prompt. Only once several deepens are trustworthy, add the weekly (Tue Opus) `--mode deepen` call site — a separate change.

---

## Self-Review

**1. Spec coverage:**
- Deepen-existing execution (writer → critic → stamp/revert) → Task 3 (`deepen_page`). ✅
- Preserve-existing + integrate-new writer → Task 2 (`deepen_prompt`). ✅
- Two-sided critic (provenance + citation-superset) → Task 3 (superset guard + `gd._critic_call`). ✅
- Reversible via restore → Task 3 (pre-image restore; simpler+safer than git checkout, spec allowed "or a saved pre-image"). ✅
- Diagnostic prioritization (thinnest-first score) → Task 1 (`rank_deepen_candidates`). ✅
- Ranked deepen pass + `--mode deepen` → Task 4. ✅
- Members flagged not deleted → Task 3 (reuse `stamp_members`/`unstamp_members`). ✅
- Weekly call site deferred; supervised first run → the "Supervised first run" section; no `scheduled_run.py` task. ✅
- Distinct from Gardener → deepen is its own pass under `.consolidate.lock`; no Gardener change. ✅
- Fail-closed on all failure modes → Task 3 (`_restore` on superset/critic/error). ✅

**2. Placeholder scan:** No TBD/TODO; complete code in every code step; commands have expected output. ✅

**3. Type consistency:** `rank_deepen_candidates` dict keys (`topic/domain/members/size/target_page/page_words/score`) consistent Task 1→4; `deepen_page(cluster, target_rel, corpus, review_path, *, _run, _critic)` signature consistent Task 3→4; `run_deepen` return keys (`deepened/reverted/no_change/candidates_seen`) consistent Task 4; reuses existing `stamp_members`/`unstamp_members`/`_member_sources_text`/`queue_reject`/`CONSOLIDATE_MODEL`/`gd._critic_call` as read. ✅
</content>

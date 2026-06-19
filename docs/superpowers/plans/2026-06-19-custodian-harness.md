# Custodian Harness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `bin/custodian.py` — the shared toolkit (Budget, Caps, fingerprint, verify_gate, govern, enqueue_review, write_digest, run_loop) that every Custodian mode plugs into, plus a smoke mode proving the loop end-to-end.

**Architecture:** A flat module of helper functions + small dataclasses, in the style of `bin/scheduled_run.py` (no class hierarchy). It reuses `scheduled_run`'s lock/branch/subscription-headless helpers. `run_loop(next_action, execute, …)` drives a guarded iteration loop; governance reverts-and-queues on verifier failure so `main` stays clean. Spec: `docs/superpowers/specs/2026-06-19-custodian-harness-design.md`.

**Tech Stack:** Python 3.12, pytest, stdlib only (hashlib, dataclasses, subprocess, json, math, datetime, pathlib). Tests under `tests/`, run with `python3 -m pytest`. All external effects (subprocess/git, lint, headless Claude) injected via `_`-prefixed seams.

## Global Constraints

- Module: `bin/custodian.py`. Tests: `tests/test_custodian.py`. Tests prepend `bin/` to `sys.path` (see existing tests).
- Reuse from `scheduled_run` (import as `sr`): `acquire_lock`, `release_lock`, `current_branch`, `_on_main`, `CLAUDE_BIN`, `ROOT`. Do NOT duplicate them.
- Budget unit = `output_tokens` from a headless result's `usage` block.
- Default `Caps`: `max_iterations=25`, `max_pages_touched=40`, `wall_clock_s=3600`.
- Governance: corpus/ change passes `verify_gate` + reversible → commit (main-only); fails → `git checkout -- <changed_paths>` + `enqueue_review`; `proposals` → `enqueue_review` (never committed as rules).
- Control-surface files are committed catalog files: `corpus/_review_queue.md`, `corpus/_digest.md` (append-only, newest-last).
- Every git/commit path is main-only via `sr._on_main()` (TOCTOU re-check before committing).
- All effectful functions take an injectable `_run`/`_lint`/`_now` seam defaulting to the real one, so tests need no network/git.

---

### Task 1: Data types + Budget

**Files:**
- Create: `bin/custodian.py`
- Test: `tests/test_custodian.py`

**Interfaces:**
- Produces: `Budget(max_output_tokens: int | None)` with `.add(usage: dict)`, `.spent()->int`, `.remaining()->int|float`, `.exhausted()->bool`; dataclasses `Caps(max_iterations=25, max_pages_touched=40, wall_clock_s=3600)`, `Verdict(ok, broken_citations, broken_wikilinks, notes)`, `Result(changed_paths, usage, proposals, errors)`.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_custodian.py`:
```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import custodian as c  # noqa: E402


def test_budget_accumulates_output_tokens():
    b = c.Budget(100)
    b.add({"output_tokens": 30})
    b.add({"output_tokens": 25})
    assert b.spent() == 55
    assert b.remaining() == 45
    assert b.exhausted() is False


def test_budget_exhausted_at_cap():
    b = c.Budget(50)
    b.add({"output_tokens": 50})
    assert b.exhausted() is True


def test_budget_none_cap_is_infinite():
    import math
    b = c.Budget(None)
    b.add({"output_tokens": 10_000})
    assert b.remaining() == math.inf and b.exhausted() is False


def test_budget_add_tolerates_missing_usage_key():
    b = c.Budget(10)
    b.add({})            # no output_tokens
    assert b.spent() == 0


def test_caps_defaults():
    caps = c.Caps()
    assert (caps.max_iterations, caps.max_pages_touched, caps.wall_clock_s) == (25, 40, 3600)
```

- [ ] **Step 2: Run to verify they fail**

Run: `python3 -m pytest tests/test_custodian.py -q`
Expected: FAIL (`No module named custodian`).

- [ ] **Step 3: Implement the module header + types**

Create `bin/custodian.py`:
```python
#!/usr/bin/env python3
"""custodian.py — shared toolkit for guarded, looping corpus agents.

A flat set of helpers + run_loop(), in the style of scheduled_run.py. Every Custodian
mode (Gardener, Adaptive Ingest, Dreamer) plugs in by supplying next_action/execute;
the harness carries the guardrails (caps, budget, fingerprint stop, verifier gate,
tiered governance, drift reinforcement, digest). Verify-fail reverts + queues so main
stays clean. Spec: docs/superpowers/specs/2026-06-19-custodian-harness-design.md
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
import math
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import scheduled_run as sr  # noqa: E402
import corpus_lint  # noqa: E402

ROOT = sr.ROOT
GIT_BIN = "git"
REVIEW_QUEUE = ROOT / "corpus" / "_review_queue.md"
DIGEST = ROOT / "corpus" / "_digest.md"


class Budget:
    """Output-token budget vs a cap. Unit = output_tokens (dominant cost driver)."""

    def __init__(self, max_output_tokens: int | None):
        self._max = max_output_tokens
        self._spent = 0

    def add(self, usage: dict) -> None:
        self._spent += int((usage or {}).get("output_tokens", 0) or 0)

    def spent(self) -> int:
        return self._spent

    def remaining(self):
        return math.inf if self._max is None else self._max - self._spent

    def exhausted(self) -> bool:
        return self._max is not None and self._spent >= self._max


@dataclasses.dataclass
class Caps:
    max_iterations: int = 25
    max_pages_touched: int = 40       # generalizes §13's "20+ pages" alarm
    wall_clock_s: int = 3600


@dataclasses.dataclass
class Verdict:
    ok: bool
    broken_citations: int = 0
    broken_wikilinks: int = 0
    notes: list = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class Result:
    changed_paths: list                # corpus/ files this iteration wrote
    usage: dict                        # headless "usage" block (for Budget)
    proposals: list = dataclasses.field(default_factory=list)
    errors: list = dataclasses.field(default_factory=list)
```

- [ ] **Step 4: Run to verify pass**

Run: `python3 -m pytest tests/test_custodian.py -q`
Expected: PASS (5 tests).

- [ ] **Step 5: Commit**

```bash
git add bin/custodian.py tests/test_custodian.py
git commit -m "feat(custodian): data types + Budget"
```

---

### Task 2: `fingerprint`

**Files:**
- Modify: `bin/custodian.py`
- Test: `tests/test_custodian.py`

**Interfaces:**
- Produces: `fingerprint(changed_paths: list[str], errors: list[str]) -> str` — stable, order-insensitive over paths.

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_custodian.py`:
```python
def test_fingerprint_stable_and_order_insensitive():
    a = c.fingerprint(["corpus/x.md", "corpus/y.md"], [])
    b = c.fingerprint(["corpus/y.md", "corpus/x.md"], [])
    assert a == b and isinstance(a, str)


def test_fingerprint_differs_on_different_effect():
    assert c.fingerprint(["corpus/x.md"], []) != c.fingerprint(["corpus/y.md"], [])
    assert c.fingerprint(["corpus/x.md"], []) != c.fingerprint(["corpus/x.md"], ["err"])


def test_fingerprint_empty_changes_is_stable():
    assert c.fingerprint([], []) == c.fingerprint([], [])
```

- [ ] **Step 2: Run to verify they fail**

Run: `python3 -m pytest tests/test_custodian.py -k fingerprint -q`
Expected: FAIL (`fingerprint` not defined).

- [ ] **Step 3: Implement**

Add to `bin/custodian.py`:
```python
def fingerprint(changed_paths: list, errors: list) -> str:
    """Stable hash of an iteration's EFFECT — sorted changed paths + sorted error
    classes. Two consecutive identical fingerprints (or empty changes) ⇒ no progress."""
    payload = json.dumps(
        {"paths": sorted(changed_paths or []), "errors": sorted(errors or [])},
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]
```

- [ ] **Step 4: Run to verify pass**

Run: `python3 -m pytest tests/test_custodian.py -k fingerprint -q`
Expected: PASS (3 tests).

- [ ] **Step 5: Commit**

```bash
git add bin/custodian.py tests/test_custodian.py
git commit -m "feat(custodian): fingerprint (no-progress detection)"
```

---

### Task 3: `verify_gate`

**Files:**
- Modify: `bin/custodian.py`
- Test: `tests/test_custodian.py`

**Interfaces:**
- Consumes: `corpus_lint.lint()` (injectable as `_lint`), `Verdict`.
- Produces: `verify_gate(changed_paths: list[str], *, _lint=None) -> Verdict`. `ok=False` ONLY when a CHANGED path is the source of a broken citation/wikilink; pre-existing breakage in unchanged pages does not fail.

- [ ] **Step 0: Confirm the lint report shape**

Read `bin/corpus_lint.py` to confirm what `lint()` returns for `broken_citations` / `broken_wikilinks` (item shape). The normalizer below handles dict, tuple, and string items; adjust `_broken_sources` if the real shape differs (e.g. the source-page key name).

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_custodian.py`:
```python
def _fake_lint(broken_cites=(), broken_links=()):
    return lambda: {"broken_citations": list(broken_cites),
                    "broken_wikilinks": list(broken_links),
                    "orphans": [], "stubs": []}


def test_verify_gate_ok_when_changed_pages_clean():
    v = c.verify_gate(["corpus/data-engineering/x.md"], _lint=_fake_lint())
    assert v.ok is True and v.broken_citations == 0


def test_verify_gate_fails_when_changed_page_sources_broken_citation():
    lint = _fake_lint(broken_cites=["corpus/data-engineering/x.md -> ../../raw/web/missing.md"])
    v = c.verify_gate(["corpus/data-engineering/x.md"], _lint=lint)
    assert v.ok is False and v.broken_citations == 1


def test_verify_gate_ignores_breakage_in_unchanged_pages():
    lint = _fake_lint(broken_cites=["corpus/other/y.md -> ../../raw/web/missing.md"])
    v = c.verify_gate(["corpus/data-engineering/x.md"], _lint=lint)
    assert v.ok is True   # the broken page is not in changed_paths
```

- [ ] **Step 2: Run to verify they fail**

Run: `python3 -m pytest tests/test_custodian.py -k verify_gate -q`
Expected: FAIL (`verify_gate` not defined).

- [ ] **Step 3: Implement**

Add to `bin/custodian.py`:
```python
def _source_of(item) -> str:
    """Extract the SOURCE corpus page from a lint broken-item, tolerant of shape:
    dict {'source'/'page': ...}, tuple/list (first element), or 'corpus/..md -> target'."""
    if isinstance(item, dict):
        return str(item.get("source") or item.get("page") or "")
    if isinstance(item, (list, tuple)) and item:
        return str(item[0])
    s = str(item)
    return s.split(" -> ")[0].split(" ->")[0].strip()


def verify_gate(changed_paths: list, *, _lint=None) -> Verdict:
    """Run the corpus linter and attribute failures: ok=False only if a CHANGED path
    is the source of a broken citation/wikilink. Pre-existing breakage in unchanged
    pages does not fail an unrelated iteration."""
    lint = _lint if _lint is not None else corpus_lint.lint
    report = lint()
    changed = {str(p) for p in (changed_paths or [])}
    cites = [it for it in report.get("broken_citations", []) if _source_of(it) in changed]
    links = [it for it in report.get("broken_wikilinks", []) if _source_of(it) in changed]
    notes = [f"broken citation: {_source_of(it)}" for it in cites] + \
            [f"broken wikilink: {_source_of(it)}" for it in links]
    return Verdict(ok=not (cites or links), broken_citations=len(cites),
                   broken_wikilinks=len(links), notes=notes)
```

- [ ] **Step 4: Run to verify pass**

Run: `python3 -m pytest tests/test_custodian.py -k verify_gate -q`
Expected: PASS (3 tests).

- [ ] **Step 5: Commit**

```bash
git add bin/custodian.py tests/test_custodian.py
git commit -m "feat(custodian): verify_gate (lint + changed-page attribution)"
```

---

### Task 4: `enqueue_review` + `govern`

**Files:**
- Modify: `bin/custodian.py`
- Test: `tests/test_custodian.py`

**Interfaces:**
- Consumes: `Verdict`, `sr._on_main`.
- Produces: `enqueue_review(kind: str, detail: dict, *, path=None) -> None` (appends to `corpus/_review_queue.md`); `govern(verdict: Verdict, changed_paths: list[str], *, reversible: bool, _run=None, _queue=None) -> dict` returning `{"action": "committed"|"reverted+queued"|"skipped-not-main", ...}`.

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_custodian.py`:
```python
import types


def test_enqueue_review_appends_entry(tmp_path):
    q = tmp_path / "_review_queue.md"
    c.enqueue_review("proposal", {"summary": "add dbt routing rule"}, path=q)
    c.enqueue_review("verify-failed", {"page": "corpus/x.md"}, path=q)
    text = q.read_text()
    assert "proposal" in text and "add dbt routing rule" in text and "verify-failed" in text


def test_govern_commits_when_ok_and_reversible(monkeypatch):
    monkeypatch.setattr(c.sr, "_on_main", lambda *a, **k: True)
    calls = []
    def run(cmd, **k):
        calls.append(" ".join(cmd))
        return types.SimpleNamespace(returncode=0, stdout="", stderr="")
    out = c.govern(c.Verdict(ok=True), ["corpus/x.md"], reversible=True, _run=run)
    assert out["action"] == "committed"
    assert any("commit" in s for s in calls) and any("add" in s for s in calls)


def test_govern_reverts_and_queues_on_failure(monkeypatch, tmp_path):
    monkeypatch.setattr(c.sr, "_on_main", lambda *a, **k: True)
    calls = []
    def run(cmd, **k):
        calls.append(cmd)
        return types.SimpleNamespace(returncode=0, stdout="", stderr="")
    queued = []
    out = c.govern(c.Verdict(ok=False, broken_citations=1, notes=["broken citation: corpus/x.md"]),
                   ["corpus/x.md"], reversible=True, _run=run,
                   _queue=lambda kind, detail: queued.append((kind, detail)))
    assert out["action"] == "reverted+queued"
    assert ["git", "checkout", "--", "corpus/x.md"] in calls   # reverted exactly the changed path
    assert not any("commit" in " ".join(cmd) for cmd in calls)  # never committed
    assert queued and queued[0][0] == "verify-failed"


def test_govern_skips_off_main(monkeypatch):
    monkeypatch.setattr(c.sr, "_on_main", lambda *a, **k: False)
    out = c.govern(c.Verdict(ok=True), ["corpus/x.md"], reversible=True,
                   _run=lambda *a, **k: types.SimpleNamespace(returncode=0, stdout="", stderr=""))
    assert out["action"] == "skipped-not-main"
```

- [ ] **Step 2: Run to verify they fail**

Run: `python3 -m pytest tests/test_custodian.py -k "enqueue_review or govern" -q`
Expected: FAIL (`enqueue_review`/`govern` not defined).

- [ ] **Step 3: Implement**

Add to `bin/custodian.py`:
```python
def enqueue_review(kind: str, detail: dict, *, path=None) -> None:
    """Append a structured entry to corpus/_review_queue.md (the review tier surface)."""
    p = Path(path) if path is not None else REVIEW_QUEUE
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        p.write_text("# Custodian Review Queue\n\n> Items needing your decision. Clear as you go.\n",
                     encoding="utf-8")
    with p.open("a", encoding="utf-8") as fh:
        fh.write(f"- [{kind}] {json.dumps(detail, ensure_ascii=False)}\n")


def govern(verdict: Verdict, changed_paths: list, *, reversible: bool,
           _run=None, _queue=None) -> dict:
    """Tiered governance: pass+reversible ⇒ commit (main-only); fail ⇒ revert the changed
    paths + queue a note. Never commits a verifier-failing change. Caller routes proposals."""
    run = _run if _run is not None else subprocess.run
    queue = _queue if _queue is not None else enqueue_review
    if not sr._on_main():
        return {"action": "skipped-not-main"}
    paths = [str(p) for p in (changed_paths or [])]
    if verdict.ok and reversible:
        if paths:
            run([GIT_BIN, "add"] + paths, cwd=str(ROOT), capture_output=True, text=True)
        msg = f"chore(custodian): apply verified change ({len(paths)} page(s))"
        c_ = run([GIT_BIN, "commit", "-m", msg], cwd=str(ROOT), capture_output=True, text=True)
        return {"action": "committed", "returncode": c_.returncode, "pages": len(paths)}
    if paths:
        run([GIT_BIN, "checkout", "--"] + paths, cwd=str(ROOT), capture_output=True, text=True)
    queue("verify-failed", {"paths": paths, "notes": verdict.notes})
    return {"action": "reverted+queued", "pages": len(paths)}
```

- [ ] **Step 4: Run to verify pass**

Run: `python3 -m pytest tests/test_custodian.py -k "enqueue_review or govern" -q`
Expected: PASS (4 tests).

- [ ] **Step 5: Commit**

```bash
git add bin/custodian.py tests/test_custodian.py
git commit -m "feat(custodian): enqueue_review + tiered govern (commit | revert+queue)"
```

---

### Task 5: `write_digest`

**Files:**
- Modify: `bin/custodian.py`
- Test: `tests/test_custodian.py`

**Interfaces:**
- Produces: `write_digest(run_id: str, label: str, entries: list[dict], *, path=None, _now=None) -> None` (appends a dated block to `corpus/_digest.md`).

- [ ] **Step 1: Write the failing test**

Append to `tests/test_custodian.py`:
```python
def test_write_digest_appends_block(tmp_path):
    d = tmp_path / "_digest.md"
    c.write_digest("run-1", "gardener", [{"action": "drain", "result": "ingested 3"}],
                   path=d, _now="2026-06-19T13:00")
    c.write_digest("run-2", "gardener", [], path=d, _now="2026-06-20T13:00")
    text = d.read_text()
    assert "run-1" in text and "gardener" in text and "ingested 3" in text
    assert "2026-06-19T13:00" in text and "2026-06-20T13:00" in text
    assert text.count("## ") >= 2   # two appended blocks, newest last
```

- [ ] **Step 2: Run to verify it fails**

Run: `python3 -m pytest tests/test_custodian.py -k write_digest -q`
Expected: FAIL (`write_digest` not defined).

- [ ] **Step 3: Implement**

Add to `bin/custodian.py`:
```python
def write_digest(run_id: str, label: str, entries: list, *, path=None, _now=None) -> None:
    """Append a 'while you were away' block to corpus/_digest.md (newest last)."""
    p = Path(path) if path is not None else DIGEST
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        p.write_text("# Custodian Digest\n\n> What the autonomous agents did, newest last.\n",
                     encoding="utf-8")
    at = _now if _now is not None else __import__("datetime").datetime.now().isoformat(timespec="minutes")
    lines = [f"\n## [{at}] {label} · {run_id}"]
    for e in entries:
        lines.append(f"- {json.dumps(e, ensure_ascii=False)}")
    if not entries:
        lines.append("- (no actions)")
    with p.open("a", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
```

- [ ] **Step 4: Run to verify pass**

Run: `python3 -m pytest tests/test_custodian.py -k write_digest -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add bin/custodian.py tests/test_custodian.py
git commit -m "feat(custodian): write_digest (the while-you-were-away surface)"
```

---

### Task 6: `run_loop` + `finalize_commit`

**Files:**
- Modify: `bin/custodian.py`
- Test: `tests/test_custodian.py`

**Interfaces:**
- Consumes: everything above + `Result`.
- Produces: `run_loop(*, next_action, execute, constraints, budget, caps, label, _now=None, _run=None, _verify=None, _govern=None, _queue=None, _digest=None) -> dict`. Returns `{"label", "iterations", "stop_reason", "committed", "queued", "spent"}`.

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_custodian.py`:
```python
def _loop_kwargs(**over):
    base = dict(constraints="OBEY §2/§7", budget=c.Budget(None), caps=c.Caps(),
                label="test", _now=lambda: "2026-06-19T13:00",
                _verify=lambda paths: c.Verdict(ok=True),
                _govern=lambda v, paths, **k: {"action": "committed", "pages": len(paths)},
                _queue=lambda *a, **k: None,
                _digest=lambda *a, **k: None,
                _finalize=lambda *a, **k: None)
    base.update(over)
    return base


def test_run_loop_stops_converged_when_worklist_dry():
    actions = iter([{"id": 1}])   # one action then StopIteration→None
    out = c.run_loop(next_action=lambda: next(actions, None),
                     execute=lambda a, ctx: c.Result(["corpus/x.md"], {"output_tokens": 5}),
                     **_loop_kwargs())
    assert out["stop_reason"] == "converged_dry" and out["iterations"] == 1


def test_run_loop_stops_on_budget():
    out = c.run_loop(next_action=lambda: {"id": 1},
                     execute=lambda a, ctx: c.Result(["corpus/x.md"], {"output_tokens": 60}),
                     **_loop_kwargs(budget=c.Budget(50)))
    assert out["stop_reason"] == "budget"


def test_run_loop_stops_on_no_progress_repeat_fingerprint():
    out = c.run_loop(next_action=lambda: {"id": 1},
                     execute=lambda a, ctx: c.Result(["corpus/same.md"], {"output_tokens": 1}),
                     **_loop_kwargs())
    assert out["stop_reason"] == "no_progress"   # 2nd iteration repeats the fingerprint


def test_run_loop_stops_on_max_iterations():
    n = iter(range(1000))
    out = c.run_loop(next_action=lambda: {"id": next(n)},
                     execute=lambda a, ctx: c.Result([f"corpus/{next(n)}.md"], {"output_tokens": 1}),
                     **_loop_kwargs(caps=c.Caps(max_iterations=3)))
    assert out["stop_reason"] == "max_iterations" and out["iterations"] == 3


def test_run_loop_routes_proposals_to_queue():
    queued = []
    out = c.run_loop(
        next_action=lambda: {"id": 1},
        execute=lambda a, ctx: c.Result([], {"output_tokens": 1},
                                        proposals=[{"summary": "new rule"}]),
        **_loop_kwargs(_queue=lambda kind, detail: queued.append((kind, detail))))
    # empty changed_paths ⇒ no_progress stop, but proposals still routed first
    assert queued and queued[0][0] == "proposal"
```

- [ ] **Step 2: Run to verify they fail**

Run: `python3 -m pytest tests/test_custodian.py -k run_loop -q`
Expected: FAIL (`run_loop` not defined).

- [ ] **Step 3: Implement**

Add to `bin/custodian.py`:
```python
def finalize_commit(*, _run=None) -> dict:
    """Commit ONLY the control-surface catalog files so the digest + queued notes always
    persist (even if every content iteration reverted). Main-only."""
    run = _run if _run is not None else subprocess.run
    if not sr._on_main():
        return {"status": "skipped-not-main"}
    paths = [str(REVIEW_QUEUE), str(DIGEST)]
    run([GIT_BIN, "add"] + paths, cwd=str(ROOT), capture_output=True, text=True)
    st = run([GIT_BIN, "status", "--porcelain"], cwd=str(ROOT), capture_output=True, text=True)
    if not (st.stdout or "").strip():
        return {"status": "nothing-to-commit"}
    run([GIT_BIN, "commit", "-m", "chore(custodian): digest + review-queue"],
        cwd=str(ROOT), capture_output=True, text=True)
    return {"status": "committed"}


def run_loop(*, next_action, execute, constraints, budget, caps, label,
             _now=None, _run=None, _verify=None, _govern=None, _queue=None, _digest=None,
             _finalize=None) -> dict:
    """Guarded iteration loop. A mode supplies next_action()/execute()/constraints; the
    harness enforces caps, budget, fingerprint no-progress stop, verifier gate, tiered
    governance, proposal routing, the digest, and a final commit of the control-surface
    files. Returns a run summary."""
    verify = _verify if _verify is not None else verify_gate
    govern_fn = _govern if _govern is not None else govern
    queue = _queue if _queue is not None else enqueue_review
    digest = _digest if _digest is not None else write_digest
    finalize = _finalize if _finalize is not None else finalize_commit
    clock = (lambda: 0.0) if _now is not None else time.monotonic   # _now present ⇒ deterministic test
    started = clock()
    run_id = (_now() if callable(_now) else None) or "run"

    entries, last_fp, touched, committed, queued_n, stop = [], None, 0, 0, 0, "completed"
    for i in range(caps.max_iterations):
        if budget.exhausted():
            stop = "budget"; break
        if caps.wall_clock_s and (clock() - started) > caps.wall_clock_s:
            stop = "wall_clock"; break
        action = next_action()
        if action is None:
            stop = "converged_dry"; break
        result = execute(action, constraints)
        budget.add(result.usage)
        for p in result.proposals:
            queue("proposal", p); queued_n += 1
        touched += len(result.changed_paths)
        fp = fingerprint(result.changed_paths, result.errors)
        if not result.changed_paths or fp == last_fp:
            entries.append({"action": action, "stop": "no_progress"})
            stop = "no_progress"; break
        last_fp = fp
        verdict = verify(result.changed_paths)
        gov = govern_fn(verdict, result.changed_paths, reversible=True)
        if gov.get("action") == "committed":
            committed += 1
        elif gov.get("action") == "reverted+queued":
            queued_n += 1
        entries.append({"action": action, "verdict_ok": verdict.ok, "gov": gov.get("action")})
        if touched >= caps.max_pages_touched:
            stop = "max_pages"; break
    else:
        stop = "max_iterations"

    digest(run_id, label, entries, _now=(_now() if callable(_now) else None))
    finalize()   # commit _digest.md + _review_queue.md so the control surface always persists
    return {"label": label, "iterations": len(entries), "stop_reason": stop,
            "committed": committed, "queued": queued_n, "spent": budget.spent()}
```

Note: `_now` (when a callable) makes the clock deterministic (returns 0.0, so wall-clock never trips in tests) AND supplies the digest timestamp. In production `_now=None` → real `time.monotonic` + real timestamp.

- [ ] **Step 4: Run to verify pass**

Run: `python3 -m pytest tests/test_custodian.py -k run_loop -q`
Expected: PASS (5 tests).

- [ ] **Step 5: Commit**

```bash
git add bin/custodian.py tests/test_custodian.py
git commit -m "feat(custodian): run_loop orchestrator + finalize_commit"
```

---

### Task 7: Smoke mode + CLI + full-suite gate

**Files:**
- Modify: `bin/custodian.py` (add `_smoke_*` + `main`)
- Test: `tests/test_custodian.py`

**Interfaces:**
- Produces: `main(argv=None) -> int` with `--smoke`; a smoke mode that drives `run_loop` to a `converged_dry` stop with no content changes.

- [ ] **Step 1: Write the failing test**

Append to `tests/test_custodian.py`:
```python
def test_smoke_runs_loop_to_convergence_without_commit(monkeypatch, capsys):
    monkeypatch.setattr(c.sr, "acquire_lock", lambda p: True)
    monkeypatch.setattr(c.sr, "release_lock", lambda p: None)
    monkeypatch.setattr(c.sr, "_on_main", lambda *a, **k: True)
    committed = []
    monkeypatch.setattr(c, "write_digest", lambda *a, **k: None)
    monkeypatch.setattr(c, "finalize_commit", lambda *a, **k: {"status": "noop"})
    monkeypatch.setattr(c, "govern", lambda *a, **k: committed.append(1) or {"action": "committed"})
    rc = c.main(["--smoke"])
    out = capsys.readouterr().out
    assert rc == 0
    assert '"stop_reason": "converged_dry"' in out
    assert committed == []   # smoke makes no content changes ⇒ govern never called
```

- [ ] **Step 2: Run to verify it fails**

Run: `python3 -m pytest tests/test_custodian.py -k smoke -q`
Expected: FAIL (`main` not defined).

- [ ] **Step 3: Implement**

Add to `bin/custodian.py`:
```python
def _smoke_run() -> dict:
    """Drive run_loop with a trivial mode whose worklist is empty from the start: the
    first next_action() returns None ⇒ the loop stops `converged_dry` with ZERO executes
    (so govern is never reached). Proves the loop + lock + digest wiring end-to-end."""
    def next_action():
        return None
    def execute(action, constraints):   # never called in smoke; present for shape
        return Result(changed_paths=[], usage={"output_tokens": 0})
    return run_loop(next_action=next_action, execute=execute,
                    constraints="SMOKE — no writes", budget=Budget(1000),
                    caps=Caps(max_iterations=3), label="smoke")


def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="Custodian harness.")
    ap.add_argument("--smoke", action="store_true",
                    help="Run the smoke mode (proves the loop end-to-end; no content changes).")
    ap.add_argument("--lock-path", default=ROOT / "raw" / ".custodian.lock", type=Path)
    args = ap.parse_args(argv)
    if not args.smoke:
        ap.print_help()
        return 0
    if not sr._on_main():
        print(json.dumps({"status": "skipped", "reason": "not_on_main"}))
        return 0
    if not sr.acquire_lock(args.lock_path):
        print(json.dumps({"status": "skipped", "reason": "lock_held"}))
        return 0
    try:
        print(json.dumps(_smoke_run()))
        return 0
    finally:
        sr.release_lock(args.lock_path)


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run to verify pass**

Run: `python3 -m pytest tests/test_custodian.py -k smoke -q`
Expected: PASS.

- [ ] **Step 5: Full-suite gate**

Run: `python3 -m pytest tests/ -q`
Expected: PASS (all custodian tests + the existing suite).

- [ ] **Step 6: Commit**

```bash
git add bin/custodian.py tests/test_custodian.py
git commit -m "feat(custodian): smoke mode + CLI; full-suite green"
```

---

## Notes for the executor

- **Smoke live check (optional, on main):** `python3 bin/custodian.py --smoke` prints a JSON summary with `stop_reason: converged_dry`, makes no commit, and writes a digest block. Safe to run.
- `verify_gate`'s `_source_of` normalizer is written tolerant of the lint item shape — Task 3 Step 0 confirms the real shape; adjust only the extraction if needed.
- Everything is injectable (`_run`/`_lint`/`_verify`/`_govern`/`_queue`/`_digest`/`_now`) so no test touches git, the network, or the real corpus.

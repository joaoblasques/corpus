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


def fingerprint(changed_paths: list, errors: list) -> str:
    """Stable hash of an iteration's EFFECT — sorted changed paths + sorted error
    classes. Two consecutive identical fingerprints (or empty changes) ⇒ no progress."""
    payload = json.dumps(
        {"paths": sorted(changed_paths or []), "errors": sorted(errors or [])},
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


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


def enqueue_review(kind: str, detail: dict, *, path=None) -> None:
    """Append a structured entry to corpus/_review_queue.md (the review tier surface)."""
    p = Path(path) if path is not None else REVIEW_QUEUE
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        p.write_text("# Custodian Review Queue\n\n> Items needing your decision. Clear as you go.\n",
                     encoding="utf-8")
    with p.open("a", encoding="utf-8") as fh:
        fh.write(f"- [{kind}] {json.dumps(detail, ensure_ascii=False)}\n")


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
        # single-writer harness: only the paths staged just above are in the index
        c_ = run([GIT_BIN, "commit", "-m", msg], cwd=str(ROOT), capture_output=True, text=True)
        return {"action": "committed", "returncode": c_.returncode, "pages": len(paths)}
    if paths:
        run([GIT_BIN, "checkout", "--"] + paths, cwd=str(ROOT), capture_output=True, text=True)
    queue("verify-failed", {"paths": paths, "notes": verdict.notes})
    return {"action": "reverted+queued", "pages": len(paths)}


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
                    caps=Caps(max_iterations=3), label="smoke",
                    _digest=lambda *a, **k: None,
                    _finalize=lambda *a, **k: {"status": "noop"})


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

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

#!/usr/bin/env python3
"""gap_resolver.py — demand-driven acquisition: turn logged query gaps into queued sources.

The self-growing loop (docs/strategy/2026-07-06 roadmap): every /query that finds thin
coverage appends a `* **Query (origin: …)**: <question>` gap entry to corpus/log.md. This
tool picks the newest undispatched gap and spawns ONE bounded headless-claude resolver that
WebSearches up to 3 authoritative WRITTEN sources (docs/papers/blogs — never videos) and
queues each via `bin/query.py fetch-and-queue`, so they drain into the corpus through the
normal nightly ingest. The corpus grows where demand proved a hole, not where a firehose
happened to point.

A ledger (raw/.gaps_dispatched.txt, sha1 per line) makes dispatch once-per-gap; a gap is
marked dispatched even when the resolver fails (surfaced in the run report) so a
permanently-failing gap can never wedge the queue.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent
ROOT = BIN.parent
sys.path.insert(0, str(BIN))

LOG_PATH = ROOT / "corpus" / "log.md"
LEDGER = ROOT / "raw" / ".gaps_dispatched.txt"
CLAUDE_BIN = Path.home() / ".claude" / "local" / "claude"

_GAP_RE = re.compile(r"^\* \*\*Query(?: \(origin: ([^)]+)\))?\*\*:\s*(.+)$")

RESOLVER_PROMPT = """You are resolving ONE knowledge gap in a personal knowledge corpus.

Gap question: {question}

Do exactly this:
1. Use WebSearch to find up to 3 authoritative WRITTEN sources that answer the gap —
   official documentation, papers, or high-quality technical blog posts. NEVER videos,
   never social threads, never SEO spam.
2. For each chosen URL, run this command via Bash (from the repo root, one per URL):
   python3 bin/query.py fetch-and-queue --question {question_arg} --url <URL> --origin gap-resolver
3. Do NOT write, edit, or create any other files. Do NOT write corpus pages — the queued
   sources drain into the corpus via the normal nightly ingest.
4. Finish by printing one line: QUEUED <n> sources.
"""


def _hash(question: str) -> str:
    return hashlib.sha1(question.strip().encode("utf-8")).hexdigest()[:16]


def parse_gaps(log_text: str) -> list[dict]:
    """All gap entries, log order (newest-first in the OKF log)."""
    out = []
    for ln in log_text.splitlines():
        m = _GAP_RE.match(ln.strip())
        if m:
            out.append({"origin": m.group(1) or "", "question": m.group(2).strip()})
    return out


def _dispatched() -> set[str]:
    if not LEDGER.exists():
        return set()
    return {ln.split()[0] for ln in LEDGER.read_text(encoding="utf-8").splitlines() if ln.strip()}


def _mark(question: str, status: str) -> None:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(f"{_hash(question)} {status} {question[:120]}\n")


def next_gap(log_text: str, dispatched: set[str]) -> dict | None:
    """Newest gap not yet dispatched (log is newest-first)."""
    for gap in parse_gaps(log_text):
        if _hash(gap["question"]) not in dispatched:
            return gap
    return None


def resolve_gap(question: str, *, model: str, timeout_s: int = 420, _run=None) -> dict:
    """Spawn one bounded headless resolver for the gap. Returns {ok, queued, detail}."""
    run = _run if _run is not None else subprocess.run
    import shlex
    prompt = RESOLVER_PROMPT.format(question=question, question_arg=shlex.quote(question))
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    try:
        proc = run([str(CLAUDE_BIN), "--print", prompt,
                    "--permission-mode", "bypassPermissions",
                    "--allowedTools", "WebSearch", "Bash", "--model", model],
                   capture_output=True, text=True, timeout=timeout_s,
                   cwd=str(ROOT), env=env, stdin=subprocess.DEVNULL)
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "queued": 0, "detail": str(exc)[:200]}
    if proc.returncode != 0:
        return {"ok": False, "queued": 0, "detail": (proc.stderr or "").strip()[:200]}
    m = re.search(r"QUEUED\s+(\d+)", proc.stdout or "")
    return {"ok": True, "queued": int(m.group(1)) if m else 0,
            "detail": (proc.stdout or "").strip()[-200:]}


def cmd_run(args) -> int:
    log_text = LOG_PATH.read_text(encoding="utf-8") if LOG_PATH.exists() else ""
    gap = next_gap(log_text, _dispatched())
    if gap is None:
        print(json.dumps({"status": "ok", "dispatched": 0, "note": "no_pending_gaps"}))
        return 0
    if args.dry_run:
        print(json.dumps({"status": "ok", "dry_run": True, "would_dispatch": gap["question"][:120]}))
        return 0
    model = args.model or os.environ.get("SCHEDULED_RUN_INGEST_MODEL", "claude-sonnet-4-6")
    res = resolve_gap(gap["question"], model=model)
    # Mark even on failure so a permanently-failing gap never wedges the queue; the
    # failure is visible in the run report and the gap stays in log.md for a human.
    _mark(gap["question"], "ok" if res["ok"] else "failed")
    print(json.dumps({"status": "ok" if res["ok"] else "failed", "dispatched": 1,
                      "queued": res["queued"], "question": gap["question"][:120],
                      "detail": res["detail"]}))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Resolve logged corpus query-gaps into queued sources.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    pr = sub.add_parser("run", help="Dispatch a resolver for the newest undispatched gap.")
    pr.add_argument("--model", default=None, help="Model for the headless resolver (default Sonnet).")
    pr.add_argument("--dry-run", action="store_true")
    pr.set_defaults(func=cmd_run)
    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

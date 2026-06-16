#!/usr/bin/env python3
"""ingest_candidates.py — deterministic selection of substantive ingest candidates.

The scheduled ingest's --max budget should target real, un-ingested sources, not
the content-less stubs that bloat raw/_inbox/ (e.g. YouTube transcripts that came
back blocked/disabled). This module filters those out cheaply (no LLM) and returns
the oldest-first bounded candidate list for the agentic ingest to process.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "raw" / "_inbox"

_STAMP_RE = re.compile(r"^corpus_ingested:\s*true\s*$", re.M | re.I)
_STATUS_RE = re.compile(r"^transcript_status:\s*(\S+)", re.M)
# `/ingest-auto` deferral line: "- DEFER <trigger>: <filename> — <reason>"
_DEFER_RE = re.compile(r"^-\s*DEFER\s+\S+:\s*(\S+)", re.M)

REVIEW_FILE = "_REVIEW.md"


def deferred_filenames(review_path) -> set[str]:
    """Filenames already deferred to the review queue (skip re-litigating them)."""
    p = Path(review_path)
    if not p.exists():
        return set()
    try:
        return set(_DEFER_RE.findall(p.read_text(encoding="utf-8")))
    except OSError:
        return set()


def is_ingestable(path: Path) -> bool:
    """True if the source has substantive, un-ingested content worth an ingest pass.

    Skips: already-stamped sources, and YouTube stubs whose transcript_status is
    anything other than ``ok`` (blocked / disabled / error → no body to ingest).
    Email/web sources have no transcript_status and are kept (the agent judges
    promo/empty via the citation gate).
    """
    try:
        head = path.read_text(encoding="utf-8", errors="ignore")[:4000]
    except OSError:
        return False
    if _STAMP_RE.search(head):
        return False
    m = _STATUS_RE.search(head)
    if m and m.group(1).lower() != "ok":
        return False
    return True


def select_candidates(inbox_dir=None, limit: int = 20) -> list[Path]:
    """Return up to `limit` ingestable inbox files, oldest first (by mtime)."""
    inbox = Path(inbox_dir) if inbox_dir is not None else INBOX
    if not inbox.exists():
        return []
    deferred = deferred_filenames(inbox / REVIEW_FILE)
    files = [
        p for p in inbox.glob("*.md")
        if p.name != REVIEW_FILE and p.name not in deferred and is_ingestable(p)
    ]
    files.sort(key=lambda p: p.stat().st_mtime)
    return files[:limit]


def main(argv=None) -> int:
    import argparse

    p = argparse.ArgumentParser(description="List substantive ingest candidates.")
    p.add_argument("--limit", type=int, default=20)
    args = p.parse_args(argv)
    for path in select_candidates(limit=args.limit):
        print(path.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

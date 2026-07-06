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
_POINTER_RE = re.compile(r"^pointer:\s*true\s*$", re.M | re.I)
# A `links:` flow-entry with fetched:true carries `file: raw/web/<name>.md`; both
# keys live in the same `- {…}` line. Match the file only when fetched:true is present.
_FETCHED_FILE_RE = re.compile(r"fetched:\s*true[^}]*?file:\s*([^\s,}]+\.md)")

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


def is_pointer(path: Path) -> bool:
    """True if the source is a pointer email (frontmatter `pointer: true`).

    Pointer emails carry no body of their own — only a URL — and their content
    lives in a fetched `raw/web/` companion (see `fetched_companions`).
    """
    try:
        return bool(_POINTER_RE.search(path.read_text(encoding="utf-8", errors="ignore")[:4000]))
    except OSError:
        return False


def fetched_companions(path: Path, root: Path | None = None) -> list[Path]:
    """Resolved `raw/web/` companion files for a pointer source.

    Returns the on-disk files named by `links:` entries that have BOTH
    `fetched: true` and a `file: raw/web/<name>.md`. Non-pointer sources, unfetched
    links, and named-but-absent files yield nothing — so a pointer with no fetched
    companion returns ``[]`` (the caller defers rather than fabricating).
    """
    base = root if root is not None else ROOT
    try:
        head = path.read_text(encoding="utf-8", errors="ignore")[:8000]
    except OSError:
        return []
    if not _POINTER_RE.search(head):
        return []
    out = []
    for rel in _FETCHED_FILE_RE.findall(head):
        companion = base / rel
        if companion.is_file():
            out.append(companion)
    return out


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


_LABELS_RE = re.compile(r"^gmail_corpus_labels:\s*$", re.M)
_BOOK_CHANNEL_RE = re.compile(r"^channel:\s*(?:book|pdf)\s*$", re.M)


def is_book_source(path: Path) -> bool:
    """True for book / book-scale-PDF chapter stubs (channel: book|pdf) — the highest-signal
    channel. Prioritized in the nightly ingest ahead of the general web/youtube backlog so the
    books-and-PDFs pivot (2026-07-06) actually drains books first instead of parking them at the
    back of the oldest-first queue behind hundreds of low-value metadata stubs."""
    try:
        return bool(_BOOK_CHANNEL_RE.search(path.read_text(encoding="utf-8", errors="ignore")[:4000]))
    except OSError:
        return False


def has_corpus_labels(path: Path) -> bool:
    """True if the source carries a `gmail_corpus_labels` marker — a label-collected
    email awaiting the ingest→reap lifecycle. These are prioritized in selection so the
    bounded nightly ingest drains the labeled backlog instead of starving it (marking a
    source rewrites its mtime, which would otherwise sink it to the bottom of the
    oldest-first queue)."""
    try:
        return bool(_LABELS_RE.search(path.read_text(encoding="utf-8", errors="ignore")[:4000]))
    except OSError:
        return False


def select_candidates(inbox_dir=None, limit: int = 20) -> list[Path]:
    """Return up to `limit` ingestable inbox files. Label-collected sources
    (`gmail_corpus_labels`) come first so the labeled backlog drains; within each
    group, oldest first (by mtime)."""
    inbox = Path(inbox_dir) if inbox_dir is not None else INBOX
    if not inbox.exists():
        return []
    deferred = deferred_filenames(inbox / REVIEW_FILE)
    files = [
        p for p in inbox.glob("*.md")
        if p.name != REVIEW_FILE and p.name not in deferred and is_ingestable(p)
    ]
    # Priority tiers (each oldest-first within tier): labeled emails (must drain to
    # un-label+archive) → books/PDFs (highest signal, the 2026-07-06 pivot) → everything else.
    files.sort(key=lambda p: (not has_corpus_labels(p), not is_book_source(p), p.stat().st_mtime))
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

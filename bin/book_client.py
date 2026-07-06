#!/usr/bin/env python3
"""book_client.py — EPUB book folder → corpus collector (CLI).

collect: split new EPUBs from the watch dir into chapter stubs in raw/_inbox (channel
`book`) — these route to the nightly FULL ingest, never quick-intake.
file:    after ingest, move an EPUB whose chapters are ALL corpus_ingested into the watch
dir's _processed/ subfolder (mirrors the PDF reaper).
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import shutil
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent
sys.path.insert(0, str(BIN))
import collect_books as cb  # noqa: E402


def cmd_collect(args) -> int:
    watch = Path(args.dir) if args.dir else cb.BOOK_WATCH_DIR
    collected_at = datetime.date.today().isoformat()
    t = {"books": 0, "chapters": 0, "skipped": 0, "failed": 0}
    for epub in cb.discover(watch):
        try:
            sha = cb.content_sha(epub)
            if cb.already_collected(sha):
                t["skipped"] += 1
                continue
            book = cb.extract_book(epub)
            if not book["chapters"]:
                t["failed"] += 1
                continue
            if args.dry_run:
                t["books"] += 1
                t["chapters"] += len(book["chapters"])
                continue
            cb.INBOX.mkdir(parents=True, exist_ok=True)
            for ch in book["chapters"]:
                stub = cb.INBOX / cb.stub_filename(book["title"], ch["index"], ch["title"])
                stub.write_text(
                    cb.build_stub(book, ch, source_path=str(epub), sha=sha,
                                  collected_at=collected_at),
                    encoding="utf-8")
            t["books"] += 1
            t["chapters"] += len(book["chapters"])
        except Exception:  # noqa: BLE001 — one bad EPUB must not abort the run
            t["failed"] += 1
    print(json.dumps({**t, "dry_run": bool(args.dry_run)}, indent=2))
    return 0


def cmd_file(args) -> int:
    """Move EPUBs whose chapter stubs are ALL corpus_ingested into _processed/."""
    watch = Path(args.dir) if args.dir else cb.BOOK_WATCH_DIR
    proc_dir = watch / cb.PROCESSED_SUBDIR
    t = {"moved": 0}
    for epub in cb.discover(watch):
        sha = cb.content_sha(epub)
        stubs = cb.stubs_for_sha(sha)
        if not stubs:
            continue
        if not all(re.search(r"^corpus_ingested:\s*true", text, re.M) for _, text in stubs):
            continue
        if args.dry_run:
            t["moved"] += 1
            continue
        rel = epub.relative_to(watch)
        dest = proc_dir / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(epub), str(dest))
        t["moved"] += 1
    print(json.dumps({**t, "dry_run": bool(args.dry_run)}, indent=2))
    return 0


def _args(argv):
    p = argparse.ArgumentParser(description="EPUB book folder → corpus collector.")
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("collect", help="Split new EPUBs into chapter stubs in raw/_inbox.")
    c.add_argument("--dir", default=None)
    c.add_argument("--dry-run", action="store_true")
    c.set_defaults(func=cmd_collect)
    f = sub.add_parser("file", help="Move fully-ingested EPUBs to _processed/.")
    f.add_argument("--dir", default=None)
    f.add_argument("--dry-run", action="store_true")
    f.set_defaults(func=cmd_file)
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = _args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

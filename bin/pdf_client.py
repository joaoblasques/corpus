#!/usr/bin/env python3
"""pdf_client.py — driver for the PDF collector (collect + file).

collect: extract new PDFs from the watch dir into raw/_inbox (channel pdf).
file:    after ingest, move ingested PDFs into the watch dir's _processed/ subfolder.
Pure logic lives in collect_pdf.py.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import shutil
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent
sys.path.insert(0, str(BIN))
import collect_pdf as cp  # noqa: E402


def extract(abs_path: str) -> dict:
    """Seam over collect_pdf.extract so tests can stub the heavy PDF library."""
    return cp.extract(abs_path)


def _under_watch(watch: Path, rel: str) -> bool:
    """Reject traversal / absolute paths escaping the watch dir."""
    if os.path.isabs(rel) or ".." in os.path.normpath(rel).split(os.sep):
        return False
    try:
        return (watch / rel).resolve().is_relative_to(watch.resolve())
    except (OSError, ValueError):
        return False


def cmd_collect(args) -> int:
    watch = Path(args.dir) if args.dir else cp.PDF_WATCH_DIR
    collected_at = datetime.date.today().isoformat()
    found = cp.discover(watch)
    t = {"collected": 0, "skipped": 0, "low_text": 0, "low_text_files": []}
    processed = 0
    for d in found:
        if args.max and processed >= args.max:
            break
        processed += 1
        try:
            sha = cp.content_sha(d["abs_path"])
            if cp.already_collected(sha):
                t["skipped"] += 1
                continue
            meta = extract(d["abs_path"])
            if meta["words"] < cp.MIN_TEXT_WORDS:
                t["low_text"] += 1
                t["low_text_files"].append(d["filename"])
                continue
            if args.dry_run:
                t["collected"] += 1
                continue
            path = cp.pdf_filename(d["filename"])
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(cp.build_pdf_source(
                {"pdf_origin": d["filename"], "source_path": d["abs_path"],
                 "title": meta["title"], "author": meta["author"], "pages": meta["pages"],
                 "content_sha": sha, "collected_at": collected_at},
                meta["markdown"]), encoding="utf-8")
            t["collected"] += 1
        except Exception:  # noqa: BLE001 — a bad/locked file must not abort the batch
            t["skipped"] += 1
    print(json.dumps({**t, "dry_run": bool(args.dry_run), "discovered": len(found)}, indent=2))
    return 0


def cmd_file(args) -> int:
    watch = Path(args.dir) if args.dir else cp.PDF_WATCH_DIR
    proc_dir = watch / cp.PROCESSED_SUBDIR
    t = {"moved": 0}
    for origin in cp.processable():
        if not _under_watch(watch, origin):
            continue
        src = watch / origin
        if not src.exists():
            continue
        if args.dry_run:
            t["moved"] += 1
            continue
        proc_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(proc_dir / Path(origin).name))
        t["moved"] += 1
    print(json.dumps({**t, "dry_run": bool(args.dry_run)}, indent=2))
    return 0


def _args(argv):
    p = argparse.ArgumentParser(description="PDF folder → corpus collector.")
    sub = p.add_subparsers(dest="cmd", required=True)
    pcol = sub.add_parser("collect")
    pcol.add_argument("--dir", default=None)
    pcol.add_argument("--max", type=int, default=None)
    pcol.add_argument("--dry-run", action="store_true")
    pcol.set_defaults(func=cmd_collect)
    pfile = sub.add_parser("file")
    pfile.add_argument("--dir", default=None)
    pfile.add_argument("--dry-run", action="store_true")
    pfile.set_defaults(func=cmd_file)
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = _args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""github_book_client.py — collect CC-licensed GitHub-hosted books into chapter stubs (CLI).

collect: for each book in bin/github_books.yaml, shallow-clone the repo to a temp dir, extract
its chapter files (AsciiDoc/Markdown) into `book`-channel stubs in raw/_inbox, then discard the
clone. Per-chapter sha dedup (shared with the EPUB/PDF book namespace) makes re-runs idempotent,
so a later run only adds new/changed chapters. On-demand (books are static-ish); not nightly-wired.
"""
from __future__ import annotations

import argparse
import datetime
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

BIN = Path(__file__).resolve().parent
sys.path.insert(0, str(BIN))
import collect_github_book as gb  # noqa: E402
import collect_books as cb  # noqa: E402

CONFIG = BIN / "github_books.yaml"
GIT = shutil.which("git") or "/usr/bin/git"


def load_config(path=None) -> dict:
    import yaml
    p = Path(path) if path else CONFIG
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {"books": []}


def _clone(repo: str, ref: str, dest: Path, *, _run=None) -> bool:
    """Shallow-clone repo@ref into dest. Returns True on success."""
    run = _run if _run is not None else subprocess.run
    cmd = [GIT, "clone", "--depth", "1", "--branch", ref, repo, str(dest)]
    try:
        proc = run(cmd, capture_output=True, text=True, timeout=300)
        return proc.returncode == 0
    except Exception:  # noqa: BLE001
        return False


def cmd_collect(args) -> int:
    cfg = load_config(args.config)
    collected_at = datetime.date.today().isoformat()
    t = {"books": 0, "chapters": 0, "skipped": 0, "failed": 0, "failed_books": []}
    for book in cfg.get("books", []):
        tmp = Path(tempfile.mkdtemp(prefix="ghbook-"))
        try:
            repo_dir = tmp / "repo"
            if not (args.no_clone or _clone(book["repo"], book.get("ref", "master"), repo_dir,
                                            _run=getattr(args, "_run", None))):
                if args.no_clone:      # test/offline mode: repo already staged at tmp/repo
                    pass
                else:
                    t["failed"] += 1
                    t["failed_books"].append(book["name"])
                    continue
            chapters = gb.extract_chapters(repo_dir, book["chapter_glob"])
            if not chapters:
                t["failed"] += 1
                t["failed_books"].append(book["name"])
                continue
            new_ch = 0
            for ch in chapters:
                sha = gb.content_sha_text(ch["text"])
                if gb.already_collected(sha):
                    t["skipped"] += 1
                    continue
                if args.dry_run:
                    new_ch += 1
                    continue
                cb.INBOX.mkdir(parents=True, exist_ok=True)
                stub = cb.INBOX / gb.stub_filename(book["title"], ch["index"], ch["title"])
                stub.write_text(gb.build_gh_stub(book, ch, sha=sha, collected_at=collected_at),
                                encoding="utf-8")
                new_ch += 1
            if new_ch:
                t["books"] += 1
                t["chapters"] += new_ch
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    print(json.dumps({**t, "dry_run": bool(args.dry_run)}, indent=2))
    return 0


def _args(argv):
    p = argparse.ArgumentParser(description="Collect CC-licensed GitHub books into chapter stubs.")
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("collect")
    c.add_argument("--config", default=None)
    c.add_argument("--dry-run", action="store_true")
    c.add_argument("--no-clone", action="store_true",
                   help="skip cloning; expect repos already staged at <tmp>/repo (tests/offline)")
    c.set_defaults(func=cmd_collect)
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = _args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

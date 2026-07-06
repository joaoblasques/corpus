#!/usr/bin/env python3
"""arxiv_client.py — collect arXiv papers matching standing domain queries (CLI).

collect: for each feed in bin/arxiv_feeds.yaml, query the arXiv API for the newest matching
papers and write `arxiv`-channel abstract stubs into raw/_inbox (deduped by arXiv id). The
abstracts route through the normal ingest into queryable source pages that point back to the
papers. Bounded (--max total) and polite (sleeps between API calls per arXiv etiquette).
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen

BIN = Path(__file__).resolve().parent
sys.path.insert(0, str(BIN))
import collect_arxiv as ca  # noqa: E402

CONFIG = BIN / "arxiv_feeds.yaml"
_UA = "corpus-arxiv-collector/1.0 (personal knowledge base; polite, low-volume)"


def load_config(path=None) -> dict:
    import yaml
    p = Path(path) if path else CONFIG
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {"feeds": []}


def fetch(url: str, timeout: int = 40) -> str:
    """GET a URL with a descriptive UA. Returns body text ('' on failure)."""
    try:
        with urlopen(Request(url, headers={"User-Agent": _UA}), timeout=timeout) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception:  # noqa: BLE001 — a failed feed must not abort the run
        return ""


def cmd_collect(args) -> int:
    cfg = load_config(args.config)
    collected_at = datetime.date.today().isoformat()
    _fetch = getattr(args, "_fetch", None) or fetch
    t = {"feeds": 0, "papers": 0, "skipped": 0, "failed_feeds": []}
    total = 0
    for feed in cfg.get("feeds", []):
        if args.max and total >= args.max:
            break
        t["feeds"] += 1
        url = ca.build_query_url(feed["query"], feed.get("max_results", 8))
        papers = ca.parse_feed(_fetch(url))
        if not papers:
            t["failed_feeds"].append(feed["name"])
        for paper in papers:
            if args.max and total >= args.max:
                break
            if ca.already_collected(paper["arxiv_id"]):
                t["skipped"] += 1
                continue
            if not args.dry_run:
                ca.INBOX.mkdir(parents=True, exist_ok=True)
                stub = ca.INBOX / ca.stub_filename(paper)
                stub.write_text(ca.build_arxiv_stub(paper, feed["domain"], collected_at),
                                encoding="utf-8")
            t["papers"] += 1
            total += 1
        if args.sleep and not getattr(args, "_fetch", None):
            time.sleep(args.sleep)   # arXiv etiquette: ~3s between calls
    print(json.dumps({**t, "dry_run": bool(args.dry_run)}, indent=2))
    return 0


def _args(argv):
    p = argparse.ArgumentParser(description="Collect arXiv papers into abstract stubs.")
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("collect")
    c.add_argument("--config", default=None)
    c.add_argument("--max", type=int, default=30, help="cap total papers collected this run")
    c.add_argument("--sleep", type=float, default=3.0, help="seconds between API calls (etiquette)")
    c.add_argument("--dry-run", action="store_true")
    c.set_defaults(func=cmd_collect)
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = _args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

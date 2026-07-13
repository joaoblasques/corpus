#!/usr/bin/env python3
"""blog_discover.py — the blog analog of book_discover: propose new blogs for phone review.

Discovery signal = demand-driven, not a generic list: domains the corpus ALREADY CITES (via
raw/web source_urls) ≥N times but that are NOT yet in the scrape list. Those are proven-relevant
blogs the corpus draws from but doesn't watch. Candidates are appended to the vault review queue
`00_Inbox/Clippings/Blogs to review.md` (phone-tickable). `promote` reads the `[x]`-ticked ones and
appends them to `blogs to scrape.md` — which the nightly Obsidian collector already scrapes. A
seen-ledger makes discovery once-per-domain.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

BIN = Path(__file__).resolve().parent
ROOT = BIN.parent
WEB = ROOT / "raw" / "web"
CONFIG = BIN / "blog_discover.yaml"
LEDGER = ROOT / "raw" / ".blogs_discovered.txt"
_CLIP = Path.home() / "Dev" / "second-brain" / "00_Inbox" / "Clippings"
SCRAPE_LIST = Path(os.environ.get("CORPUS_BLOG_SCRAPE", str(_CLIP / "blogs to scrape.md")))
REVIEW = Path(os.environ.get("CORPUS_BLOG_REVIEW", str(_CLIP / "Blogs to review.md")))

# Aggregators / doc hubs / social — not personal or practitioner blogs; never proposed.
DEFAULT_IGNORE = {
    "youtube.com", "youtu.be", "github.com", "twitter.com", "x.com", "reddit.com",
    "news.ycombinator.com", "linkedin.com", "medium.com", "substack.com", "google.com",
    "arxiv.org", "wikipedia.org", "facebook.com", "amazon.com", "stackoverflow.com",
}

_SOURCE_URL_RE = re.compile(r"^source_url:\s*(\S+)", re.M)
_REVIEW_URL_RE = re.compile(r"^- \[[ xX]\]\s+(https?://\S+)")
_REVIEW_CHECKED_RE = re.compile(r"^- \[[xX]\]\s+(https?://\S+)")
_ANY_URL_RE = re.compile(r"https?://[^\s)]+")

REVIEW_HEADER = (
    "# Blogs to review\n\n"
    "Blogs the corpus already cites but doesn't yet scrape (most-cited first). Tick `[x]` the ones\n"
    "worth watching; the nightly then adds them to `blogs to scrape.md` and scrapes their new posts.\n"
)


def _host(url: str) -> str:
    return (urlparse(url).hostname or "").lower().removeprefix("www.")


def load_config(path=None) -> dict:
    import yaml
    p = Path(path) if path else CONFIG
    return yaml.safe_load(p.read_text(encoding="utf-8")) if p.exists() else {}


def _hosts_in(path: Path) -> set:
    if not path.exists():
        return set()
    return {_host(u) for u in _ANY_URL_RE.findall(path.read_text(encoding="utf-8", errors="ignore"))}


def _ledger() -> set:
    if not LEDGER.exists():
        return set()
    return {ln.split()[0] for ln in LEDGER.read_text(encoding="utf-8").splitlines() if ln.strip()}


def _mark(host: str) -> None:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(host + "\n")


def candidate_domains(web_dir: Path, ignore: set, min_cited: int) -> list:
    """[(host, count)] of blog domains cited in raw/web source_urls, ≥min_cited, not ignored.
    Sorted most-cited first."""
    from collections import Counter
    counts: Counter = Counter()
    if web_dir.exists():
        for f in web_dir.glob("*.md"):
            m = _SOURCE_URL_RE.search(f.read_text(encoding="utf-8", errors="ignore"))
            if m:
                h = _host(m.group(1))
                if h and h not in ignore:
                    counts[h] += 1
    return [(h, n) for h, n in counts.most_common() if n >= min_cited]


def cmd_collect(args) -> int:
    cfg = load_config(args.config)
    ignore = DEFAULT_IGNORE | set(cfg.get("ignore_hosts", []))
    min_cited = cfg.get("min_cited", 3)
    max_new = cfg.get("max_new_per_run", 15)
    web_dir = Path(args.web) if args.web else WEB

    seen = _ledger() | _hosts_in(SCRAPE_LIST) | _hosts_in(REVIEW)
    proposed = []
    for host, n in candidate_domains(web_dir, ignore, min_cited):
        if len(proposed) >= max_new:
            break
        if host in seen:
            continue
        seen.add(host)
        proposed.append((host, n))

    if proposed and not args.dry_run:
        REVIEW.parent.mkdir(parents=True, exist_ok=True)
        body = REVIEW.read_text(encoding="utf-8") if REVIEW.exists() else REVIEW_HEADER
        lines = [f"- [ ] https://{h}/ · cited {n}x" for h, n in proposed]
        REVIEW.write_text(body.rstrip() + "\n" + "\n".join(lines) + "\n", encoding="utf-8")
        for h, _ in proposed:
            _mark(h)
    print(json.dumps({"proposed": len(proposed),
                      "top": [f"{h} ({n}x)" for h, n in proposed[:8]],
                      "dry_run": bool(args.dry_run)}, indent=2))
    return 0


def cmd_promote(args) -> int:
    """Append `[x]`-ticked review blogs to the scrape list (deduped by host)."""
    if not REVIEW.exists():
        print(json.dumps({"promoted": 0, "note": "no review file"}))
        return 0
    checked = _REVIEW_CHECKED_RE.findall(REVIEW.read_text(encoding="utf-8", errors="ignore"))
    scraped = _hosts_in(SCRAPE_LIST)
    to_add = []
    for url in checked:
        if _host(url) not in scraped:
            scraped.add(_host(url))
            to_add.append(url)
    if to_add and not args.dry_run:
        SCRAPE_LIST.parent.mkdir(parents=True, exist_ok=True)
        cur = SCRAPE_LIST.read_text(encoding="utf-8") if SCRAPE_LIST.exists() else ""
        SCRAPE_LIST.write_text(cur.rstrip() + "\n" + "\n".join(to_add) + "\n", encoding="utf-8")
    print(json.dumps({"promoted": len(to_add), "urls": to_add[:8],
                      "dry_run": bool(args.dry_run)}, indent=2))
    return 0


def _args(argv):
    p = argparse.ArgumentParser(description="Discover + promote blogs for the scrape list.")
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("collect", help="Propose cited-but-unscraped blogs into the review queue.")
    c.add_argument("--config", default=None)
    c.add_argument("--web", default=None)
    c.add_argument("--dry-run", action="store_true")
    c.set_defaults(func=cmd_collect)
    pr = sub.add_parser("promote", help="Append [x]-ticked review blogs to blogs to scrape.md.")
    pr.add_argument("--dry-run", action="store_true")
    pr.set_defaults(func=cmd_promote)
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = _args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

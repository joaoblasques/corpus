#!/usr/bin/env python3
"""book_fetch.py — auto-download allowlisted legal book PDFs into the PDF pipeline.

Removes the manual "drop a PDF into Google Drive" step for KNOWN-LEGAL books. A manifest
(bin/book_sources.yaml) lists direct URLs to author/publisher/CC-hosted book PDFs; this
collector downloads any not-yet-fetched ones into the CorpusInbox/PDFs/_auto/ landing folder,
where the existing PDF collector chunks + ingests them and the PDF reaper files them away.

SAFETY (non-negotiable): a URL is only downloaded if its host is on the trusted allowlist
(arXiv, university/author domains, CC GitHub, specific publisher giveaway hosts). This is NOT
an open-web crawler — it never searches for or downloads from arbitrary "free book" sites,
which are where pirated copies and malware live. Untrusted hosts are refused and reported, not
fetched. A once-per-URL ledger makes re-runs cheap and prevents re-downloading.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

BIN = Path(__file__).resolve().parent
ROOT = BIN.parent
CONFIG = BIN / "book_sources.yaml"
# The review queue lives INSIDE the Obsidian vault (00_Inbox/Clippings) so the user can tick it
# from their phone — it syncs via their vault sync. Overridable via env for tests.
REVIEW = Path(os.environ.get(
    "CORPUS_BOOK_REVIEW",
    str(Path.home() / "Dev" / "second-brain" / "00_Inbox" / "Clippings" / "Books to review.md")))
LEDGER = ROOT / "raw" / ".books_fetched.txt"
# Matches a CHECKED review line: `- [x] [Title](url) · ...`
_REVIEW_CHECKED_RE = re.compile(r"^- \[[xX]\]\s+\[([^\]]+)\]\((https?://[^)]+)\)")
LANDING = Path(
    "/Users/jonasblasques/Library/CloudStorage/GoogleDrive-tilakapash@gmail.com/"
    "My Drive/CorpusInbox/PDFs/_auto"
)
_UA = "corpus-book-fetch/1.0 (personal knowledge base; allowlist-only, low-volume)"

# Trusted hosts: author/university pages, arXiv, CC GitHub, specific publisher giveaways.
# A URL's host must equal one of these or be a subdomain of one. `.edu` is trusted broadly.
DEFAULT_ALLOWLIST = [
    "arxiv.org", "d2l.ai", "mml-book.github.io", "mml-book.com", "statlearning.com",
    "hastie.su.domains", "databookuw.com", "aosabook.org", "sre.google",
    "pages.cs.wisc.edu", "raw.githubusercontent.com", "github.com",
    "info.microsoft.com", "microsoft.com",
]


def _url_hash(url: str) -> str:
    return hashlib.sha1(url.strip().encode("utf-8")).hexdigest()[:16]


def _name_slug(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", (title or "").lower()).strip("-")[:50] or "book"


def review_approved(review_path=None) -> list:
    """Parse `[x]`-checked entries from the review queue → [{name, title, url}].

    A checked entry is APPROVED for download: either a trusted-host find that book_discover
    pre-checked, or one a human ticked. Approval is the gate here, so these bypass the host
    allowlist (book_discover never pre-checks an untrusted host, and a manual tick is a
    deliberate human authorization for that specific URL)."""
    p = Path(review_path) if review_path else REVIEW
    if not p.exists():
        return []
    out = []
    for line in p.read_text(encoding="utf-8", errors="ignore").splitlines():
        m = _REVIEW_CHECKED_RE.match(line)
        if m:
            out.append({"name": _name_slug(m.group(1)), "title": m.group(1).strip(),
                        "url": m.group(2).strip()})
    return out


def host_allowed(url: str, allowlist) -> bool:
    """True if the URL's host is on the allowlist (exact or subdomain), or ends in .edu."""
    host = (urlparse(url).hostname or "").lower()
    if not host:
        return False
    if host.endswith(".edu"):
        return True
    return any(host == d or host.endswith("." + d) for d in allowlist)


def load_config(path=None) -> dict:
    import yaml
    p = Path(path) if path else CONFIG
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}


def _ledger() -> set:
    if not LEDGER.exists():
        return set()
    return {ln.split()[0] for ln in LEDGER.read_text(encoding="utf-8").splitlines() if ln.strip()}


def _mark(url: str, name: str) -> None:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(f"{_url_hash(url)} {name}\n")


def _download(url: str, dest: Path, timeout: int = 180) -> bool:
    """Stream a URL to dest; keep it only if it's a real PDF (%PDF magic). Returns success."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        with urlopen(Request(url, headers={"User-Agent": _UA}), timeout=timeout) as r, \
                open(dest, "wb") as fh:
            shutil.copyfileobj(r, fh)
    except Exception:  # noqa: BLE001
        dest.unlink(missing_ok=True)
        return False
    try:
        with open(dest, "rb") as fh:
            if fh.read(5) != b"%PDF-":
                dest.unlink(missing_ok=True)
                return False
    except OSError:
        return False
    return True


def cmd_collect(args) -> int:
    cfg = load_config(args.config)
    allowlist = cfg.get("allowlist", DEFAULT_ALLOWLIST)
    landing = Path(args.dir) if args.dir else LANDING
    done = _ledger()
    _dl = getattr(args, "_download", None) or _download
    # Two fetch sources: (1) the hand-curated manifest — gated by the host allowlist;
    # (2) `[x]`-approved review-queue entries — gated by approval (trusted-host pre-check or a
    # human tick), so the allowlist is waived for those specific, vouched-for URLs.
    manifest = [{**b, "gate": "allowlist"} for b in cfg.get("books", [])]
    approved = [{**r, "gate": "approved"} for r in review_approved()]
    t = {"fetched": 0, "skipped": 0, "refused": 0, "failed": 0, "refused_urls": []}
    for book in manifest + approved:
        url = book.get("url", "")
        if _url_hash(url) in done:
            t["skipped"] += 1
            continue
        if book["gate"] == "allowlist" and not host_allowed(url, allowlist):
            t["refused"] += 1
            t["refused_urls"].append(url)
            continue
        if args.dry_run:
            t["fetched"] += 1
            continue
        dest = landing / f"{book['name']}.pdf"
        if _dl(url, dest):
            _mark(url, book["name"])
            t["fetched"] += 1
        else:
            t["failed"] += 1
    print(json.dumps({**t, "dry_run": bool(args.dry_run)}, indent=2))
    return 0


def _args(argv):
    p = argparse.ArgumentParser(description="Auto-download allowlisted legal book PDFs.")
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("collect")
    c.add_argument("--config", default=None)
    c.add_argument("--dir", default=None, help="landing dir (default CorpusInbox/PDFs/_auto)")
    c.add_argument("--dry-run", action="store_true")
    c.set_defaults(func=cmd_collect)
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = _args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

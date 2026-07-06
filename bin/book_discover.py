#!/usr/bin/env python3
"""book_discover.py — scan a curated LEGAL book index, propose relevant new books for review.

Reads a specific, trusted, CC-licensed index (the EbookFoundation free-programming-books list),
filters to the corpus's domains, and appends new PDF candidates to a review queue
(raw/_book_review.md). Trusted-host finds are pre-checked `[x]` (they auto-download via
book_fetch); untrusted-host finds are left `[ ]` for the user to approve with a tick. A
seen-ledger prevents re-proposing. This is the ONLY discovery surface — it never searches the
open web; it reads one curated legal index and proposes, it does not autonomously download from
untrusted hosts.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

BIN = Path(__file__).resolve().parent
ROOT = BIN.parent
sys.path.insert(0, str(BIN))
import book_fetch as bf  # noqa: E402 — reuse host_allowed + the trusted allowlist

CONFIG = BIN / "book_discover.yaml"
REVIEW = ROOT / "raw" / "_book_review.md"
LEDGER = ROOT / "raw" / ".books_discovered.txt"
_UA = "corpus-book-discover/1.0 (personal knowledge base; read-only curated-index scan)"

_SECTION_RE = re.compile(r"^#{2,4}\s+(.+?)\s*$")
_ENTRY_RE = re.compile(r"^\s*[-*]\s+\[([^\]]+)\]\((https?://[^)\s]+)\)(.*)$")
_REVIEW_URL_RE = re.compile(r"^- \[[ xX]\]\s+\[[^\]]+\]\((https?://[^)]+)\)")

REVIEW_HEADER = (
    "# Book discovery — review queue\n\n"
    "Machine-generated candidates from a curated **legal** index (free-programming-books, CC BY).\n"
    "Tick `[x]` to approve a book for auto-download into the corpus PDF pipeline; leave `[ ]` to skip.\n"
    "Trusted-host finds are pre-approved. The nightly `book_fetch` downloads every `[x]` entry once.\n"
)


def _url_hash(url: str) -> str:
    return hashlib.sha1(url.strip().encode("utf-8")).hexdigest()[:16]


def fetch(url: str, timeout: int = 40) -> str:
    try:
        with urlopen(Request(url, headers={"User-Agent": _UA}), timeout=timeout) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        return ""


def load_config(path=None) -> dict:
    import yaml
    p = Path(path) if path else CONFIG
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}


def _pdfish(url: str, tail: str) -> bool:
    return url.lower().endswith(".pdf") or "pdf" in tail.lower()


def parse_index(md: str, section_keywords) -> list:
    """Yield {title, url, tail} for PDF-ish book entries under a relevant section heading."""
    out, section = [], ""
    for line in md.splitlines():
        sm = _SECTION_RE.match(line)
        if sm:
            section = sm.group(1).lower()
            continue
        if not any(k in section for k in section_keywords):
            continue
        em = _ENTRY_RE.match(line)
        if em and _pdfish(em.group(2), em.group(3)):
            out.append({"title": em.group(1).strip(), "url": em.group(2).strip()})
    return out


def _ledger() -> set:
    if not LEDGER.exists():
        return set()
    return {ln.split()[0] for ln in LEDGER.read_text(encoding="utf-8").splitlines() if ln.strip()}


def _mark(url: str) -> None:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(f"{_url_hash(url)} {url}\n")


def _existing_review_urls() -> set:
    if not REVIEW.exists():
        return set()
    return {_url_hash(m.group(1)) for line in REVIEW.read_text(encoding="utf-8").splitlines()
            if (m := _REVIEW_URL_RE.match(line))}


def _manifest_url_hashes() -> set:
    """URLs already in the hand-curated fetch manifest — don't re-propose those."""
    try:
        cfg = bf.load_config()
    except Exception:  # noqa: BLE001
        return set()
    return {_url_hash(b.get("url", "")) for b in cfg.get("books", [])}


def _append_review(trusted_lines: list, review_lines: list, today: str) -> None:
    REVIEW.parent.mkdir(parents=True, exist_ok=True)
    body = REVIEW.read_text(encoding="utf-8") if REVIEW.exists() else REVIEW_HEADER
    block = [f"\n## Discovered {today}"]
    if trusted_lines:
        block.append("### Auto-approved (trusted host)")
        block += trusted_lines
    if review_lines:
        block.append("### Needs your review (tick [x] to approve)")
        block += review_lines
    REVIEW.write_text(body.rstrip() + "\n" + "\n".join(block) + "\n", encoding="utf-8")


def cmd_collect(args) -> int:
    cfg = load_config(args.config)
    keywords = [k.lower() for k in cfg.get("relevant_sections", [])]
    allowlist = bf.load_config().get("allowlist", bf.DEFAULT_ALLOWLIST)
    max_new = cfg.get("max_new_per_run", 15)
    _fetch = getattr(args, "_fetch", None) or fetch

    seen = _ledger() | _existing_review_urls() | _manifest_url_hashes()
    trusted_lines, review_lines, marks = [], [], []
    for url in cfg.get("index_urls", []):
        if not bf.host_allowed(url, allowlist):       # the index itself must be a trusted host
            continue
        for cand in parse_index(_fetch(url), keywords):
            if len(trusted_lines) + len(review_lines) >= max_new:
                break
            h = _url_hash(cand["url"])
            if h in seen:
                continue
            seen.add(h)
            host = (urlparse(cand["url"]).hostname or "?").lower()
            trusted = bf.host_allowed(cand["url"], allowlist)
            line = (f"- [{'x' if trusted else ' '}] [{cand['title']}]({cand['url']}) · "
                    f"{host} · {'trusted' if trusted else 'review'}")
            (trusted_lines if trusted else review_lines).append(line)
            marks.append(cand["url"])

    t = {"proposed": len(marks), "auto_trusted": len(trusted_lines),
         "needs_review": len(review_lines)}
    if not args.dry_run and marks:
        _append_review(trusted_lines, review_lines, args.today or datetime.date.today().isoformat())
        for u in marks:
            _mark(u)
    print(json.dumps({**t, "dry_run": bool(args.dry_run)}, indent=2))
    return 0


def _args(argv):
    p = argparse.ArgumentParser(description="Propose relevant new legal books for review.")
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("collect")
    c.add_argument("--config", default=None)
    c.add_argument("--today", default=None)
    c.add_argument("--dry-run", action="store_true")
    c.set_defaults(func=cmd_collect)
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = _args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

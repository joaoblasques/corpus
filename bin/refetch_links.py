#!/usr/bin/env python3
"""refetch_links.py — retry high-score `fetch-failed` email links (self-healing).

The Gmail collector fetches each useful link once at collection time; a transient
failure (timeout, rate-limit, flaky host) leaves a `links:` entry marked
`fetched: false, reason: fetch-failed`. That strands the content: the inbox-only
ingest selector never re-fetches it, so the pointer email it belongs to has no
companion and defers forever (see ingest_candidates.fetched_companions).

This module re-fetches those *transient* failures for links above a score floor —
mirroring `collect_youtube --refetch-blocked`. It does NOT re-fetch `over-cap`
(a deliberate per-email budget skip), `low-utility`, `duplicate`, or `unsupported`
links — those skips are intentional, not transient. On success it writes the
companion file and rewrites the link entry to `fetched: true, file: …`; on repeated
failure it leaves the `fetch-failed` marker for a future retry.
"""
from __future__ import annotations

import argparse
import datetime
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import collect_email as ce  # noqa: E402
import fetch_link as fl  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "raw" / "_inbox"
WEB_DIR = ROOT / "raw" / "web"
YT_DIR = ROOT / "raw" / "youtube"

# One `links:` flow entry per line: `  - {url: …, fetched: …, score: …, …}`.
_ENTRY_RE = re.compile(r"^\s*-\s*\{(.*)\}\s*$", re.M)
_URL_RE = re.compile(r'url:\s*("(?:[^"\\]|\\.)*"|[^,}]+)')
_FETCHED_RE = re.compile(r"fetched:\s*(true|false)")
_SCORE_RE = re.compile(r"score:\s*(\d+)")
_FILE_RE = re.compile(r"file:\s*([^\s,}]+)")
_REASON_RE = re.compile(r"reason:\s*([^\s,}]+)")
_BLOCK_RE = re.compile(r"\nlinks:\n(?:[ ]+-[ ]\{[^\n]*\}\n)+", re.M)


def _unquote(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith('"') and raw.endswith('"'):
        return raw[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    return raw


def parse_links(content: str) -> list[dict]:
    """Parse the `links:` frontmatter block into ordered dicts.

    Each dict carries url, fetched (bool), score (int), and optional file/reason —
    the same shape collect_email.add_links_frontmatter consumes, so the list can be
    round-tripped back into the file after edits.
    """
    links = []
    for body in _ENTRY_RE.findall(content):
        m_url = _URL_RE.search(body)
        if not m_url:
            continue
        d: dict = {"url": _unquote(m_url.group(1))}
        m_f = _FETCHED_RE.search(body)
        d["fetched"] = (m_f.group(1) == "true") if m_f else False
        m_s = _SCORE_RE.search(body)
        d["score"] = int(m_s.group(1)) if m_s else 0
        m_file = _FILE_RE.search(body)
        if m_file:
            d["file"] = m_file.group(1)
        m_r = _REASON_RE.search(body)
        if m_r:
            d["reason"] = m_r.group(1)
        links.append(d)
    return links


def _is_retryable(d: dict, min_score: int) -> bool:
    return (not d.get("fetched")
            and not d.get("file")
            and d.get("reason") == "fetch-failed"
            and d.get("score", 0) >= min_score)


def _fetch_and_store(url, message_id, score, collected_at, web_dir, yt_dir, root, fetcher) -> str | None:
    """Resolve, fetch, and write a companion file. Returns the root-relative path
    on success, or None on unsupported/failed fetch."""
    try:
        resolved = fetcher.resolve(url)
        kind = fetcher.classify(resolved)
        if kind == "unsupported":
            return None
        base = web_dir if kind == "article" else yt_dir
        base.mkdir(parents=True, exist_ok=True)
        content = fetcher.fetch(resolved)
        target = ce.link_target(content["title"], base, resolved)
        doc = ce.build_link_document(
            {"channel": content["channel"], "source_url": resolved,
             "via_email": message_id, "score": score, "collected_at": collected_at},
            content["text"],
        )
        target.write_text(doc, encoding="utf-8")
        return str(target.relative_to(root))
    except Exception:
        return None


def _message_id(content: str) -> str:
    m = re.search(r"^gmail_message_id:\s*(\S+)", content, re.M)
    return m.group(1) if m else "unknown"


def refetch_file(path: Path, *, min_score: int = 7, max_refetch: int = 9999,
                 web_dir: Path | None = None, yt_dir: Path | None = None,
                 root: Path | None = None, collected_at: str | None = None,
                 fetcher=None) -> dict:
    """Retry the retryable `fetch-failed` links in one email file (in place)."""
    web_dir = web_dir if web_dir is not None else WEB_DIR
    yt_dir = yt_dir if yt_dir is not None else YT_DIR
    root = root if root is not None else ROOT
    fetcher = fetcher if fetcher is not None else fl
    collected_at = collected_at or datetime.date.today().isoformat()

    try:
        content = path.read_text(encoding="utf-8")
    except OSError:
        return {"refetched": 0, "failed": 0}
    links = parse_links(content)
    if not links:
        return {"refetched": 0, "failed": 0}

    message_id = _message_id(content)
    refetched = failed = attempts = 0
    changed = False
    for d in links:
        if attempts >= max_refetch:  # bound network ATTEMPTS, not just successes
            break
        if not _is_retryable(d, min_score):
            continue
        attempts += 1
        rel = _fetch_and_store(d["url"], message_id, d.get("score", 0),
                               collected_at, web_dir, yt_dir, root, fetcher)
        if rel:
            d["file"] = rel
            d.pop("reason", None)  # success → drop the fetch-failed marker
            refetched += 1
            changed = True
        else:
            failed += 1  # leave fetch-failed marker for a future retry

    if changed:
        stripped = _BLOCK_RE.sub("\n", content, count=1)
        path.write_text(stripped, encoding="utf-8")
        ce.add_links_frontmatter(str(path), links)
    return {"refetched": refetched, "failed": failed}


def refetch_inbox(inbox_dir: Path | None = None, *, min_score: int = 7,
                  max_total: int = 15, web_dir: Path | None = None,
                  yt_dir: Path | None = None, root: Path | None = None,
                  collected_at: str | None = None, fetcher=None) -> dict:
    """Scan an inbox and re-fetch retryable links across all emails, up to max_total."""
    inbox = inbox_dir if inbox_dir is not None else INBOX
    if not inbox.exists():
        return {"refetched": 0, "failed": 0, "files_scanned": 0}
    refetched = failed = scanned = 0
    for p in sorted(inbox.glob("*.md")):
        if p.name == "_REVIEW.md":
            continue
        scanned += 1
        attempts = refetched + failed
        if attempts >= max_total:  # attempt budget spent — keep scanning is pointless
            continue
        res = refetch_file(p, min_score=min_score, max_refetch=max_total - attempts,
                           web_dir=web_dir, yt_dir=yt_dir, root=root,
                           collected_at=collected_at, fetcher=fetcher)
        refetched += res["refetched"]
        failed += res["failed"]
    return {"refetched": refetched, "failed": failed, "files_scanned": scanned}


def main(argv=None) -> int:
    import json
    p = argparse.ArgumentParser(description="Retry high-score fetch-failed email links.")
    p.add_argument("--min-score", type=int, default=7,
                   help="Only retry links at or above this utility score (default 7).")
    p.add_argument("--max", type=int, default=15,
                   help="Max fetch attempts this run, bounding network cost (default 15).")
    args = p.parse_args(argv)
    print(json.dumps(refetch_inbox(min_score=args.min_score, max_total=args.max)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

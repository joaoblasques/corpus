#!/usr/bin/env python3
"""collect_x.py — pure logic for the X (Twitter) bookmarks collector."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "raw" / "_inbox"
DEDUP_DIRS = [ROOT / "raw" / "_inbox", ROOT / "raw" / "x"]
_ID_RE = re.compile(r"^tweet_id:\s*(\S+)\s*$", re.M)
_INGESTED_RE = re.compile(r"^corpus_ingested:\s*true\s*$", re.M)
_CHANNEL_X_RE = re.compile(r"^channel:\s*x\s*$", re.M)


def slugify(tweet_id) -> str:
    return f"x-{tweet_id}"


def _scalar(s) -> str:
    s = (str(s) if s is not None else "").replace("\n", " ").strip()
    if s and (any(c in s for c in ":#") or s[0] in "\"'[{-@`"):
        return '"' + s.replace('"', '\\"') + '"'
    return s


def already_collected(tweet_id, dirs=None) -> bool:
    for d in (dirs if dirs is not None else DEDUP_DIRS):
        p = Path(d)
        if not p.exists():
            continue
        for md in p.glob("*.md"):
            try:
                head = md.read_text(encoding="utf-8", errors="ignore")[:800]
            except OSError:
                continue
            m = _ID_RE.search(head)
            if m and m.group(1) == str(tweet_id):
                return True
    return False


def build_document(post: dict, *, collected_at: str) -> str:
    tid = post["id"]
    links = post.get("links") or []
    lines = [
        "---", "channel: x", "source: x",
        f"tweet_id: {tid}",
        f"url: {post.get('url', '')}",
        f"author: {post.get('author', '')}",
        f"created_at: {post.get('created_at', '')}",
        f"links: [{', '.join(links)}]",
        f"collected_at: {collected_at}",
        "---", "",
        f"# X post by @{post.get('author', '')}",
        "", (post.get("text") or "").strip(),
    ]
    arts = post.get("articles") or []
    if arts:
        lines.append("\n## Linked articles")
        for a in arts:
            lines += [f"### {a.get('url', '')}", (a.get("text") or "").strip(), ""]
    return "\n".join(lines) + "\n"


def write_collected(post: dict, *, collected_at: str, inbox=None, dedup_dirs=None) -> dict:
    tid = post["id"]
    if already_collected(tid, dedup_dirs):
        return {"status": "duplicate", "path": None}
    ib = Path(inbox) if inbox is not None else INBOX
    ib.mkdir(parents=True, exist_ok=True)
    path = ib / f"{slugify(tid)}.md"
    path.write_text(build_document(post, collected_at=collected_at), encoding="utf-8")
    return {"status": "written", "path": str(path)}


def reapable(dirs=None) -> list:
    out = []
    for d in (dirs if dirs is not None else DEDUP_DIRS):
        p = Path(d)
        if not p.exists():
            continue
        for md in p.glob("*.md"):
            try:
                head = md.read_text(encoding="utf-8", errors="ignore")[:800]
            except OSError:
                continue
            if _CHANNEL_X_RE.search(head) and _INGESTED_RE.search(head):
                m = _ID_RE.search(head)
                if m:
                    out.append(m.group(1))
    return out

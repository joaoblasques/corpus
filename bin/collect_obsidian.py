#!/usr/bin/env python3
"""collect_obsidian.py — deterministic core for the collect-obsidian collector.

Pure functions: path policy, URL-list parsing, source-frontmatter building, dedup,
discovery, and the reaper selector. All I/O (copies, fetch, git) lives in
obsidian_client.py. Reuses helpers from collect_email (DRY).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent
ROOT = BIN.parent
INBOX = ROOT / "raw" / "_inbox"
DEDUP_DIRS = [ROOT / "raw" / "_inbox", ROOT / "raw" / "notes", ROOT / "raw" / "web"]

VAULT_ROOT = Path("/Users/jonasblasques/Dev/second-brain")
INCLUDE_DIRS = [
    "03_Resources/Articles", "03_Resources/Books", "03_Resources/Study Notes",
    "03_Resources/Snippets", "03_Resources/Prompt Templates", "00_Inbox/Clippings",
]
EXCLUDE_DIRS = ["03_Resources/llm-wiki-system"]
EXCLUDE_FILE_RE = re.compile(r"(?i)(_processed\.md$|(^|/)README\.md$)")
URL_LIST_NAMES = {"articles to process.md", "TO SCRAPE.md"}

sys.path.insert(0, str(BIN))
from collect_email import slugify, yaml_scalar, URL_RE  # noqa: E402


def is_included(rel_path: str) -> bool:
    rel = rel_path.replace("\\", "/")
    if any(rel == e or rel.startswith(e + "/") for e in EXCLUDE_DIRS):
        return False
    if not rel.endswith(".md"):
        return False
    if EXCLUDE_FILE_RE.search(rel):
        return False
    return any(rel.startswith(i + "/") for i in INCLUDE_DIRS)


def classify(rel_path: str) -> str:
    return "url-list" if rel_path.rsplit("/", 1)[-1] in URL_LIST_NAMES else "note"


def parse_url_list(text: str) -> list:
    seen, out = set(), []
    for m in URL_RE.finditer(text or ""):
        u = m.group(0).rstrip(".,)")
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def read_note(abs_path: str):
    """Return (title, tags, body) — splits the note's own frontmatter off the body."""
    t = Path(abs_path).read_text(encoding="utf-8", errors="replace")
    title, tags, body = "", [], t
    if t.startswith("---"):
        end = t.find("\n---", 3)
        if end != -1:
            fm, body = t[3:end], t[end + 4:].lstrip("\n")
            tm = re.search(r"^title:\s*(.+)$", fm, re.M)
            if tm:
                title = tm.group(1).strip().strip('"')
            tg = re.search(r"^tags:\s*\n((?:\s*-\s*.+\n?)+)", fm, re.M)
            if tg:
                tags = [re.sub(r"^\s*-\s*", "", ln).strip() for ln in tg.group(1).splitlines() if ln.strip()]
    if not title:
        title = Path(abs_path).stem
    return title, tags, body

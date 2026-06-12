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


def note_filename(rel_path: str, base=None) -> Path:
    base = base if base is not None else INBOX
    stem = rel_path.rsplit("/", 1)[-1]
    if stem.endswith(".md"):
        stem = stem[:-3]
    return base / f"notes-{slugify(stem)}.md"


def url_filename(url: str, title: str, base=None) -> Path:
    base = base if base is not None else INBOX
    return base / f"web-{slugify(title or url)}.md"


def build_note_source(meta: dict, body: str) -> str:
    lines = [
        "---", "channel: notes", "source: obsidian",
        f"vault_origin: {meta['vault_origin']}",
        f"title: {yaml_scalar(meta.get('title', ''))}",
    ]
    tags = meta.get("tags") or []
    if tags:
        lines.append("tags:")
        lines += [f"  - {t}" for t in tags]
    lines += [f"collected_at: {meta['collected_at']}", "---", "", body.strip(), ""]
    return "\n".join(lines)


def build_url_source(meta: dict, body: str) -> str:
    lines = [
        "---", "channel: web", "source: obsidian-list",
        f"source_url: {meta['source_url']}",
        f"via_vault_list: {meta['via_vault_list']}",
        f"title: {yaml_scalar(meta.get('title', ''))}",
        f"collected_at: {meta['collected_at']}", "---", "", body.strip(), "",
    ]
    return "\n".join(lines)


def fm_field(text: str, key: str):
    m = re.search(rf"^{re.escape(key)}:\s*(.+)$", text, re.M)
    return m.group(1).strip() if m else None


def is_vault_note_ingested(abs_path: str) -> bool:
    try:
        t = Path(abs_path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    return "corpus_ingested: true" in t


def _raw_sources(dirs=None):
    for d in (dirs if dirs is not None else DEDUP_DIRS):
        p = Path(d)
        if not p.exists():
            continue
        for md in p.glob("*.md"):
            try:
                yield md, md.read_text(encoding="utf-8", errors="replace")
            except (OSError, UnicodeDecodeError):
                continue


def already_collected_vault(rel_path: str, dirs=None) -> bool:
    needle = f"vault_origin: {rel_path}\n"
    return any(needle in t for _, t in _raw_sources(dirs))


def url_already_collected(url: str, dirs=None) -> bool:
    needle = f"source_url: {url}\n"
    return any(needle in t for _, t in _raw_sources(dirs))

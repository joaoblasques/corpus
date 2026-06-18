#!/usr/bin/env python3
"""collect_pdf.py — deterministic core for the PDF collector.

Pure functions: discovery, sha dedup, source-frontmatter building, and the
move-selector. All heavy I/O (extraction, file moves) is driven from pdf_client.py.
Reuses helpers from collect_email (DRY).
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent
ROOT = BIN.parent
INBOX = ROOT / "raw" / "_inbox"
DEDUP_DIRS = [ROOT / "raw" / "_inbox", ROOT / "raw" / "pdf"]

PDF_WATCH_DIR = Path(
    "/Users/jonasblasques/Library/CloudStorage/GoogleDrive-tilakapash@gmail.com/"
    "My Drive/CorpusInbox/PDFs"
)
PROCESSED_SUBDIR = "_processed"
MIN_TEXT_WORDS = 50

sys.path.insert(0, str(BIN))
from collect_email import slugify, yaml_scalar  # noqa: E402

_SKIP_RE = re.compile(r"^(\.|~\$)")  # hidden / office temp files


def discover(watch_dir=None) -> list:
    root = Path(watch_dir) if watch_dir is not None else PDF_WATCH_DIR
    if not root.exists():
        return []
    out = []
    for p in sorted(root.iterdir()):
        if not p.is_file():
            continue
        if p.suffix.lower() != ".pdf":
            continue
        if _SKIP_RE.match(p.name):
            continue
        out.append({"abs_path": str(p), "filename": p.name})
    return out


def content_sha(abs_path: str) -> str:
    h = hashlib.sha256()
    with open(abs_path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def pdf_filename(filename: str, base=None) -> Path:
    base = base if base is not None else INBOX
    stem = filename[:-4] if filename.lower().endswith(".pdf") else filename
    return base / f"pdf-{slugify(stem)}.md"


def build_pdf_source(meta: dict, body: str) -> str:
    lines = [
        "---", "channel: pdf", "source: pdf",
        f"pdf_origin: {meta['pdf_origin']}",
        f"source_path: {meta['source_path']}",
        f"title: {yaml_scalar(meta.get('title', ''))}",
        f"author: {yaml_scalar(meta.get('author', ''))}",
        f"pages: {meta.get('pages', 0)}",
        f"content_sha: {meta['content_sha']}",
        f"collected_at: {meta['collected_at']}", "---", "", body.strip(), "",
    ]
    return "\n".join(lines)


def _frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    return text[3:end] if end != -1 else ""


def fm_field(text: str, key: str):
    m = re.search(rf"^{re.escape(key)}:\s*(.+)$", _frontmatter(text), re.M)
    return m.group(1).strip() if m else None


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


def already_collected(sha: str, dirs=None) -> bool:
    for _, text in _raw_sources(dirs):
        if fm_field(text, "content_sha") == sha:
            return True
    return False

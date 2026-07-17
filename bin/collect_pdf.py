#!/usr/bin/env python3
"""collect_pdf.py — deterministic core for the PDF collector.

Pure functions: discovery, sha dedup, source-frontmatter building, and the
move-selector. All heavy I/O (extraction, file moves) is driven from pdf_client.py.
Reuses helpers from collect_email (DRY).
"""
from __future__ import annotations

import contextlib
import hashlib
import os
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
# Book-scale PDFs: one 250k-word stub would choke the headless ingest. Above the
# threshold, split into part-stubs at paragraph boundaries (~CHUNK_WORDS each).
CHUNK_THRESHOLD_WORDS = 12000
CHUNK_WORDS = 8000


def split_for_ingest(markdown: str, chunk_words: int = CHUNK_WORDS) -> list:
    """Split long extracted text into ~chunk_words parts at paragraph boundaries."""
    paras = markdown.split("\n\n")
    parts, cur, n = [], [], 0
    for para in paras:
        w = len(para.split())
        if cur and n + w > chunk_words:
            parts.append("\n\n".join(cur)); cur, n = [], 0
        cur.append(para); n += w
    if cur:
        parts.append("\n\n".join(cur))
    return parts

sys.path.insert(0, str(BIN))
from collect_email import slugify, yaml_scalar  # noqa: E402

_SKIP_RE = re.compile(r"^(\.|~\$)")  # hidden / office temp files


def discover(watch_dir=None) -> list:
    root = Path(watch_dir) if watch_dir is not None else PDF_WATCH_DIR
    if not root.exists():
        return []
    out = []
    for p in sorted(root.rglob("*")):   # recurse into subfolders
        if not p.is_file():
            continue
        if p.suffix.lower() != ".pdf":
            continue
        # Skip the _processed reaper folder (already-filed PDFs) and any hidden/dot
        # subfolder — recursing into them would re-collect already-processed files.
        if any(part == "_processed" or part.startswith(".")
               for part in p.relative_to(root).parts[:-1]):
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
        *([f"pdf_part: {meta['pdf_part']}"] if meta.get("pdf_part") else []),
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


@contextlib.contextmanager
def _suppress_fd_stdout():
    """Silence fd-level (C library) writes to stdout during PDF parsing so the
    library's parser/OCR chatter never pollutes a JSON-on-stdout caller."""
    saved = os.dup(1)
    devnull = os.open(os.devnull, os.O_WRONLY)
    try:
        os.dup2(devnull, 1)
        yield
    finally:
        os.dup2(saved, 1)
        os.close(devnull)
        os.close(saved)


def processable(dirs=None) -> list:
    """(source_path, pdf_origin) for raw copies that are corpus_ingested (ready to move).

    source_path is the full absolute path recorded at collection time — it carries the
    watch-dir SUBFOLDER, which discover() recurses into. The reaper must use it (not the
    bare pdf_origin basename) or subfolder PDFs can never be located and moved out."""
    out = []
    for _, text in _raw_sources(dirs):
        if "corpus_ingested: true" not in text:
            continue
        origin = fm_field(text, "pdf_origin")
        src = fm_field(text, "source_path")
        if origin or src:
            out.append((src, origin))
    return out


def extract(abs_path: str) -> dict:
    """Extract a PDF to markdown + metadata. Seam over pymupdf4llm/fitz (stubbable)."""
    import pymupdf4llm
    import fitz
    # pymupdf4llm ≥1.27 routes to a layout parser that OCRs every image-based page by
    # default (Tesseract). On digital PDFs that adds nothing, and one image-heavy slide
    # deck can wedge the whole batch for tens of minutes — so disable OCR. Older versions
    # lack the kwarg (and don't OCR by default): fall back to the plain call.
    with _suppress_fd_stdout():
        try:
            markdown = pymupdf4llm.to_markdown(abs_path, use_ocr=False) or ""
        except TypeError:
            markdown = pymupdf4llm.to_markdown(abs_path) or ""
    doc = fitz.open(abs_path)
    meta = doc.metadata or {}
    pages = doc.page_count
    doc.close()
    title = (meta.get("title") or "").strip() or Path(abs_path).stem
    author = (meta.get("author") or "").strip()
    return {"markdown": markdown, "title": title, "author": author,
            "pages": pages, "words": len(markdown.split())}

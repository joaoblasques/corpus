#!/usr/bin/env python3
"""collect_github_book.py — CC-licensed books hosted as GitHub AsciiDoc/Markdown → chapter stubs.

Some of the best free books are authored openly on GitHub under Creative Commons (Mastering
Bitcoin, Mastering Ethereum, The Architecture of Open Source Applications). Their chapters are
plain AsciiDoc/Markdown — the CLEANEST possible ingest: no PDF text extraction, no OCR, just
lightly-normalized prose. Each chapter becomes a `book`-channel stub routed to the nightly
FULL §8.1 ingest, exactly like an EPUB chapter.

Pure functions here (extraction + stub building); the clone/orchestration lives in
bin/github_book_client.py. Dedup is by per-chapter content sha, shared with the EPUB pipeline.
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent
sys.path.insert(0, str(BIN))
import collect_books as cb  # noqa: E402 — reuse INBOX, dedup, slug/filename helpers

_MIN_CHAPTER_WORDS = 200   # skip errata/BIP-list/glossary scaffolding


def _clean_asciidoc(text: str) -> str:
    """Normalize AsciiDoc markup to readable prose+markdown for LLM ingest.

    Strips index-term macros ((( ... ))), block anchors [[...]], attribute/admonition
    lines ([role=...], [TIP], [source,python]), and block delimiters (====, ----);
    converts `= / == / ===` headings to markdown `#`. Content is preserved; only
    non-semantic markup is removed.
    """
    # index-term macros: (((...))) — may attach to a word; drop the macro, keep the words
    text = re.sub(r"\(\(\(.*?\)\)\)", "", text)
    # block anchors and attribute/admonition lines on their own line
    text = re.sub(r"^\[\[[^\]]*\]\]\s*$", "", text, flags=re.M)
    text = re.sub(r"^\[[a-zA-Z][^\]]*\]\s*$", "", text, flags=re.M)
    # AsciiDoc headings -> markdown (= Title, == Section, ...)
    text = re.sub(r"^(=+)\s+(.+?)\s*$",
                  lambda m: "#" * len(m.group(1)) + " " + m.group(2), text, flags=re.M)
    # block delimiters: runs of ==== ---- .... ++++ **** ____ on their own line
    text = re.sub(r"^([=\-.+*_])\1{3,}\s*$", "", text, flags=re.M)
    # cross-reference macros <<anchor,Text>> -> Text ; <<anchor>> -> ""
    text = re.sub(r"<<[^,>]*,\s*([^>]*)>>", r"\1", text)
    text = re.sub(r"<<[^>]*>>", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chapter_title(raw: str) -> str | None:
    """First AsciiDoc/Markdown level-1 heading (== Title or # Title)."""
    m = re.search(r"^(?:==|#)\s+(.+?)\s*$", raw, re.M)
    return m.group(1).strip() if m else None


def content_sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def extract_chapters(repo_dir, chapter_glob: str) -> list:
    """Extract [{index, title, text, src_file}] from a repo's chapter files (spine = sorted glob)."""
    files = sorted(Path(repo_dir).glob(chapter_glob))
    chapters = []
    for f in files:
        try:
            raw = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        text = _clean_asciidoc(raw)
        if len(text.split()) < _MIN_CHAPTER_WORDS:
            continue
        chapters.append({
            "index": len(chapters) + 1,
            "title": chapter_title(raw) or f.stem,
            "text": text,
            "src_file": f.name,
        })
    return chapters


def build_gh_stub(book: dict, chapter: dict, *, sha: str, collected_at: str) -> str:
    """A `book`-channel chapter stub with GitHub provenance (repo, license, source URL)."""
    blob = f"{book['repo'].rstrip('/')}/blob/{book.get('ref', 'master')}/{chapter['src_file']}"
    fm = "\n".join([
        "---",
        "channel: book",
        "source: github-book",
        f"book_title: {book['title']}",
        f"author: {book.get('author', '')}",
        f"chapter_index: {chapter['index']}",
        f"chapter_title: {chapter['title']}",
        f"repo: {book['repo']}",
        f"license: {book.get('license', '')}",
        f"source_path: {blob}",
        f"content_sha: {sha}",
        f"collected_at: {collected_at}",
        "---",
    ])
    header = f"# {book['title']} — {chapter['title']}\n"
    return f"{fm}\n\n{header}\n{chapter['text']}\n"


def stub_filename(book_title: str, index: int, chapter_title_: str) -> str:
    # reuse the EPUB pipeline's naming so both live in one book-*.md namespace + dedup set
    return cb.stub_filename(book_title, index, chapter_title_)


def already_collected(sha: str, dirs=None) -> bool:
    return cb.already_collected(sha, dirs)

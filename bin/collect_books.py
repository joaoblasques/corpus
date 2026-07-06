#!/usr/bin/env python3
"""collect_books.py — EPUB books → chapter-level markdown stubs (pure functions).

Books are the corpus's highest-signal channel (docs/strategy/2026-07-06 roadmap): curated,
edited, dense. A whole book is far too large for one inbox stub, so each EPUB is split into
CHAPTER stubs (channel `book`) that the nightly FULL ingest (§8.1 cascade) processes a few
at a time — books deserve the expensive tier, never the 3-sentence quick-intake path.

Zero external dependencies: an EPUB is a zip of XHTML — parsed with zipfile + xml.etree +
html.parser. Dedup is by file sha256 in stub frontmatter, mirroring the PDF pipeline.
"""
from __future__ import annotations

import hashlib
import posixpath
import re
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "raw" / "_inbox"
DEDUP_DIRS = [ROOT / "raw" / "_inbox", ROOT / "raw" / "book"]

BOOK_WATCH_DIR = Path(
    "/Users/jonasblasques/Library/CloudStorage/GoogleDrive-tilakapash@gmail.com/"
    "My Drive/CorpusInbox/Books"
)
PROCESSED_SUBDIR = "_processed"

_MIN_CHAPTER_WORDS = 60   # spine items below this are covers/title pages/toc — skip
_BLOCK_TAGS = {"p", "div", "section", "blockquote", "li", "tr", "br",
               "h1", "h2", "h3", "h4", "h5", "h6"}
_SKIP_TAGS = {"script", "style", "head", "svg"}


class _TextExtractor(HTMLParser):
    """XHTML → readable markdown-ish text: headings kept as `## …`, blocks separated."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._skip_depth = 0
        self._heading: str | None = None
        self.headings: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in _SKIP_TAGS:
            self._skip_depth += 1
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._heading = tag
            self.parts.append("\n\n" + "#" * min(int(tag[1]) + 1, 6) + " ")
        elif tag == "li":
            self.parts.append("\n- ")
        elif tag in _BLOCK_TAGS:
            self.parts.append("\n\n")

    def handle_endtag(self, tag):
        if tag in _SKIP_TAGS and self._skip_depth:
            self._skip_depth -= 1
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._heading = None
            self.parts.append("\n\n")

    def handle_data(self, data):
        if self._skip_depth:
            return
        if self._heading and data.strip():
            self.headings.append(data.strip())
        self.parts.append(data)

    def text(self) -> str:
        raw = "".join(self.parts)
        lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in raw.splitlines()]
        out: list[str] = []
        for ln in lines:
            if ln:
                out.append(ln)
            elif out and out[-1] != "":
                out.append("")
        return "\n".join(out).strip()


def html_to_text(html: str) -> tuple[str, list[str]]:
    """Return (text, headings-in-order) for one XHTML document."""
    p = _TextExtractor()
    p.feed(html)
    return p.text(), p.headings


def content_sha(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def extract_book(epub_path) -> dict:
    """Parse an EPUB → {title, author, chapters: [{index, title, text}]}.

    Chapters follow the OPF spine order; tiny spine items (cover/title/toc) are skipped.
    """
    with zipfile.ZipFile(epub_path) as z:
        container = ElementTree.fromstring(z.read("META-INF/container.xml"))
        opf_path = next(el.get("full-path") for el in container.iter()
                        if _local(el.tag) == "rootfile")
        opf_dir = posixpath.dirname(opf_path)
        opf = ElementTree.fromstring(z.read(opf_path))

        title, author = "", ""
        manifest: dict[str, str] = {}
        spine: list[str] = []
        for el in opf.iter():
            ln = _local(el.tag)
            if ln == "title" and not title:
                title = (el.text or "").strip()
            elif ln == "creator" and not author:
                author = (el.text or "").strip()
            elif ln == "item" and el.get("id") and el.get("href"):
                manifest[el.get("id")] = el.get("href")
            elif ln == "itemref" and el.get("idref"):
                spine.append(el.get("idref"))

        chapters = []
        for idref in spine:
            href = manifest.get(idref)
            if not href:
                continue
            full = posixpath.normpath(posixpath.join(opf_dir, href)) if opf_dir else href
            try:
                html = z.read(full).decode("utf-8", errors="replace")
            except KeyError:
                continue
            text, headings = html_to_text(html)
            if len(text.split()) < _MIN_CHAPTER_WORDS:
                continue
            chapters.append({"index": len(chapters) + 1,
                             "title": headings[0] if headings else f"Chapter {len(chapters) + 1}",
                             "text": text})
    return {"title": title or Path(str(epub_path)).stem, "author": author, "chapters": chapters}


def _slug(s: str, max_len: int = 50) -> str:
    return re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")[:max_len] or "untitled"


def stub_filename(book_title: str, index: int, chapter_title: str) -> str:
    return f"book-{_slug(book_title, 40)}-{index:02d}-{_slug(chapter_title, 40)}.md"


def build_stub(book: dict, chapter: dict, *, source_path: str, sha: str, collected_at: str) -> str:
    fm = "\n".join([
        "---",
        "channel: book",
        "source: book",
        f"book_title: {book['title']}",
        f"author: {book['author']}",
        f"chapter_index: {chapter['index']}",
        f"chapter_title: {chapter['title']}",
        f"source_path: {source_path}",
        f"content_sha: {sha}",
        f"collected_at: {collected_at}",
        "---",
    ])
    header = f"# {book['title']} — {chapter['title']}\n"
    return f"{fm}\n\n{header}\n{chapter['text']}\n"


def _stub_texts(dirs=None):
    for d in (dirs if dirs is not None else DEDUP_DIRS):
        p = Path(d)
        if not p.exists():
            continue
        for md in p.glob("book-*.md"):
            try:
                yield md, md.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue


def already_collected(sha: str, dirs=None) -> bool:
    return any(f"content_sha: {sha}" in text for _, text in _stub_texts(dirs))


def stubs_for_sha(sha: str, dirs=None) -> list:
    return [(p, t) for p, t in _stub_texts(dirs) if f"content_sha: {sha}" in t]


def discover(watch_dir=None) -> list:
    root = Path(watch_dir) if watch_dir is not None else BOOK_WATCH_DIR
    if not root.exists():
        return []
    out = []
    for p in sorted(root.rglob("*")):
        if not p.is_file() or p.suffix.lower() != ".epub":
            continue
        if any(part == PROCESSED_SUBDIR or part.startswith(".")
               for part in p.relative_to(root).parts[:-1]):
            continue
        out.append(p)
    return out

#!/usr/bin/env python3
"""collect_arxiv.py — arXiv open-access papers → abstract stubs (pure functions).

arXiv is the highest-signal recurring feed for the technical domains (docs/strategy Phase 3):
free, open-access, redistributable metadata + PDFs, with a clean Atom API. Each matching paper
becomes an `arxiv`-channel abstract stub (title + authors + abstract + categories + links). An
abstract is genuinely dense content, so the normal ingest turns it into a real, queryable source
page that points back to the paper — and a query can later pull the full PDF if the paper matters.

Zero external deps beyond stdlib (urllib + xml.etree). The fetch/orchestration lives in
bin/arxiv_client.py; dedup is by arXiv id.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import quote
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "raw" / "_inbox"
ARXIV_CHANNEL = ROOT / "raw" / "arxiv"
DEDUP_DIRS = [INBOX, ARXIV_CHANNEL]

API = "http://export.arxiv.org/api/query"
_NS = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}


def build_query_url(query: str, max_results: int = 10, start: int = 0) -> str:
    """arXiv API URL for a search query, newest first."""
    return (f"{API}?search_query={quote(query)}&start={start}"
            f"&max_results={int(max_results)}&sortBy=submittedDate&sortOrder=descending")


def _text(el, path: str) -> str:
    node = el.find(path, _NS)
    return " ".join((node.text or "").split()) if node is not None and node.text else ""


def _bare_id(entry_id: str) -> str:
    """`http://arxiv.org/abs/2607.02383v1` -> `2607.02383` (version-stripped, stable dedup key)."""
    tail = entry_id.rstrip("/").split("/abs/")[-1]
    return re.sub(r"v\d+$", "", tail)


def parse_feed(atom_xml: str) -> list:
    """Parse an arXiv Atom response into paper dicts. Malformed XML -> []."""
    try:
        root = ET.fromstring(atom_xml)
    except ET.ParseError:
        return []
    papers = []
    for e in root.findall("a:entry", _NS):
        eid = _text(e, "a:id")
        if not eid:
            continue
        pdf = [l.get("href") for l in e.findall("a:link", _NS) if l.get("title") == "pdf"]
        papers.append({
            "arxiv_id": _bare_id(eid),
            "title": _text(e, "a:title"),
            "authors": [a.find("a:name", _NS).text for a in e.findall("a:author", _NS)
                        if a.find("a:name", _NS) is not None],
            "abstract": _text(e, "a:summary"),
            "categories": [c.get("term") for c in e.findall("a:category", _NS) if c.get("term")],
            "published": _text(e, "a:published")[:10],
            "abs_url": eid,
            "pdf_url": pdf[0] if pdf else eid.replace("/abs/", "/pdf/"),
        })
    return papers


def _slug(s: str, n: int = 50) -> str:
    return re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")[:n] or "paper"


def stub_filename(paper: dict) -> str:
    return f"arxiv-{paper['arxiv_id'].replace('.', '-')}-{_slug(paper['title'], 40)}.md"


def _yaml_scalar(s: str) -> str:
    s = (s or "").replace("\n", " ").strip()
    return '"' + s.replace('"', "'") + '"' if s and re.search(r"[:#\[\]{}&*!|>'\"%@`]", s) else s


def build_arxiv_stub(paper: dict, domain: str, collected_at: str) -> str:
    """An `arxiv`-channel abstract stub: dense enough to ingest into a real source page that
    points back to the paper. `domain` is a routing hint from the feed config."""
    authors = ", ".join(paper["authors"][:8])
    cats = ", ".join(paper["categories"])
    fm = "\n".join([
        "---",
        "channel: arxiv",
        "source: arxiv",
        f"arxiv_id: {paper['arxiv_id']}",
        f"title: {_yaml_scalar(paper['title'])}",
        f"authors: {_yaml_scalar(authors)}",
        f"categories: {_yaml_scalar(cats)}",
        f"domain_hint: {domain}",
        f"published: {paper['published']}",
        f"abs_url: {paper['abs_url']}",
        f"pdf_url: {paper['pdf_url']}",
        f"collected_at: {collected_at}",
        "---",
    ])
    body = (f"# {paper['title']}\n\n"
            f"> **arXiv paper** ({cats}) · {authors} · {paper['published']}. "
            f"[abstract]({paper['abs_url']}) · [pdf]({paper['pdf_url']})\n\n"
            f"## Abstract\n\n{paper['abstract']}\n")
    return f"{fm}\n\n{body}"


def _stub_texts(dirs=None):
    for d in (dirs if dirs is not None else DEDUP_DIRS):
        p = Path(d)
        if not p.exists():
            continue
        for md in p.glob("arxiv-*.md"):
            try:
                yield md, md.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue


def already_collected(arxiv_id: str, dirs=None) -> bool:
    needle = f"arxiv_id: {arxiv_id}"
    return any(needle in text for _, text in _stub_texts(dirs))

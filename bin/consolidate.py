#!/usr/bin/env python3
"""consolidate.py — pure topic-clustering of shallow source pages (no LLM, no writes).

Builds (domain, topic) clusters from source-page topics/tags so the consolidation runner can
synthesize each cluster into one cited page. Spec: docs/superpowers/specs/2026-07-11-consolidation-job-design.md
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent
ROOT = BIN.parent
CORPUS = ROOT / "corpus"

_TYPE_RE = re.compile(r"^type:\s*(\w+)", re.M)
_TAGS_BLOCK_RE = re.compile(r"^tags:\s*$((?:\n\s+-\s+.+)+)", re.M)
_TAG_ITEM_RE = re.compile(r"^\s+-\s+(.+?)\s*$", re.M)
_TOPICS_BULLET_RE = re.compile(r"\*\*Key topics\*\*\s*((?:\n-\s+.+)+)", re.M)
_BULLET_RE = re.compile(r"^-\s+(.+?)\s*$", re.M)
# tags that carry no topical signal
_GENERIC_TAG_RE = re.compile(r"^(corpus/|source$|hub$|entity$|concept$|synthesis$|.*-quick-intake$)")


def page_type(text: str) -> str:
    m = _TYPE_RE.search(text)
    return m.group(1) if m else ""


def read_topics(text: str) -> list[str]:
    """Lowercased, de-duped topics from a source page's Key-topics bullets + non-generic tags."""
    topics: list[str] = []
    tb = _TAGS_BLOCK_RE.search(text)
    if tb:
        for t in _TAG_ITEM_RE.findall(tb.group(1)):
            t = t.strip()
            if not _GENERIC_TAG_RE.match(t):
                topics.append(t)
    kt = _TOPICS_BULLET_RE.search(text)
    if kt:
        topics += [b.strip() for b in _BULLET_RE.findall(kt.group(1))]
    seen, out = set(), []
    for t in topics:
        k = t.lower().strip()
        if k and k not in seen:
            seen.add(k)
            out.append(k)
    return out


def iter_source_pages(corpus: Path, domain: str | None = None) -> list[Path]:
    roots = [corpus / domain] if domain else [corpus]
    out = []
    for root in roots:
        if not root.exists():
            continue
        for p in root.rglob("*.md"):
            if p.name == "README.md":
                continue
            if page_type(p.read_text(encoding="utf-8", errors="ignore")) == "source":
                out.append(p)
    return sorted(out)

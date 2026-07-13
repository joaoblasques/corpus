#!/usr/bin/env python3
"""consolidate.py — pure topic-clustering of shallow source pages (no LLM, no writes).

Builds (domain, topic) clusters from source-page topics/tags so the consolidation runner can
synthesize each cluster into one cited page. Spec: docs/superpowers/specs/2026-07-11-consolidation-job-design.md
"""
from __future__ import annotations

import argparse
import json
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


_H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.M)


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def existing_topic_keys(corpus: Path, domain: str) -> set[str]:
    """Normalized titles + slugs of concept/entity/synthesis pages in the domain."""
    keys: set[str] = set()
    root = corpus / domain
    if not root.exists():
        return keys
    for p in root.rglob("*.md"):
        if p.name == "README.md":
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        if page_type(text) in ("concept", "entity", "synthesis"):
            keys.add(_norm(p.stem))
            body = text.split("---", 2)[-1] if text.startswith("---") else text
            hm = _H1_RE.search(body)
            if hm:
                keys.add(_norm(hm.group(1)))
    return keys


def build_clusters(corpus: Path, domain: str, min_cluster: int = 5) -> list[dict]:
    index: dict[str, list[str]] = {}
    for p in iter_source_pages(corpus, domain):
        rel = str(p.relative_to(corpus))
        for topic in read_topics(p.read_text(encoding="utf-8", errors="ignore")):
            index.setdefault(topic, []).append(rel)
    clusters = []
    for topic, members in index.items():
        members = sorted(set(members))
        if len(members) >= min_cluster:
            clusters.append({"topic": topic, "domain": domain,
                             "members": members, "size": len(members)})
    return clusters


def rank_clusters(clusters: list[dict], existing: set[str]) -> list[dict]:
    out = []
    for c in clusters:
        c = dict(c)
        c["has_existing_page"] = _norm(c["topic"]) in existing
        out.append(c)
    out.sort(key=lambda c: (c["has_existing_page"], -c["size"], c["topic"]))
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="List consolidation clusters (dry-run, no writes).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("clusters")
    c.add_argument("--corpus", default=None)
    c.add_argument("--domain", default="ai-engineering")
    c.add_argument("--min", type=int, default=5)
    args = ap.parse_args(argv)

    corpus = Path(args.corpus) if args.corpus else CORPUS
    clusters = build_clusters(corpus, args.domain, min_cluster=args.min)
    ranked = rank_clusters(clusters, existing_topic_keys(corpus, args.domain))
    print(json.dumps({
        "domain": args.domain, "count": len(ranked),
        "clusters": [{"topic": c["topic"], "size": c["size"],
                      "has_existing_page": c["has_existing_page"],
                      "members": c["members"][:5]} for c in ranked],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

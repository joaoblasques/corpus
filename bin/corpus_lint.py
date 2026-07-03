#!/usr/bin/env python3
"""corpus_lint.py — deterministic corpus health checks (CLAUDE.md §8.3 mechanics).

Catches integrity issues fast and repeatably as the corpus grows (incl. via the
unattended daily ingest): broken wikilinks, broken source citations, orphan
pages (not linked from their domain hub), and stub pages. Judgment-heavy checks
(duplicate entities, contradictions) stay with the agent.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import okf_lint

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "corpus"
_META = {"index.md", "log.md", "_domains.md", "_config.md", "_REVIEW.md"}

# target stops at ] | or \ (a `\|` escaped pipe appears in markdown-table wikilinks)
_WIKILINK_RE = re.compile(r"\[\[([^\]|\\]+)")
_CITATION_RE = re.compile(r"\]\((\.\./[^)#]+?\.md)")
_STATUS_RE = re.compile(r"^status:\s*(\S+)", re.M)


def _domain_dirs(corpus: Path) -> list[Path]:
    return [d for d in corpus.iterdir() if d.is_dir()]


def content_pages(corpus: Path) -> list[Path]:
    """All corpus pages except the hub READMEs and the root meta files."""
    pages = []
    for d in _domain_dirs(corpus):
        for p in d.rglob("*.md"):
            if p.name != "README.md":
                pages.append(p)
    return pages


def find_broken_wikilinks(corpus: Path) -> list[tuple[str, str]]:
    """[[domain/page|...]] links whose target corpus/domain/page.md is missing.

    Only checks links whose first segment is an existing corpus domain dir
    (skips PARA-native vault links like [[03_Resources/...]]).
    """
    domains = {d.name for d in _domain_dirs(corpus)}
    broken = []
    for p in list(corpus.rglob("*.md")):
        if p.name in _META:
            continue
        for target in _WIKILINK_RE.findall(p.read_text(encoding="utf-8", errors="ignore")):
            target = target.strip()
            seg0 = target.split("/", 1)[0]
            if seg0 not in domains:
                continue  # not a corpus link
            if not (corpus / f"{target}.md").exists():
                broken.append((str(p.relative_to(corpus.parent)), target))
    return broken


def find_broken_citations(corpus: Path) -> list[tuple[str, str]]:
    """Relative `](../../raw/...md)` citations whose target file does not exist."""
    broken = []
    for p in content_pages(corpus):
        for rel in _CITATION_RE.findall(p.read_text(encoding="utf-8", errors="ignore")):
            target = (p.parent / rel).resolve()
            if not target.exists():
                broken.append((str(p.relative_to(corpus.parent)), rel))
    return broken


def find_orphans(corpus: Path) -> list[str]:
    """Content pages whose slug is not referenced from their domain's README hub."""
    orphans = []
    for d in _domain_dirs(corpus):
        readme = d / "README.md"
        hub = readme.read_text(encoding="utf-8", errors="ignore") if readme.exists() else ""
        for p in d.rglob("*.md"):
            if p.name == "README.md":
                continue
            slug = p.stem
            # linked as [[domain/slug...]] or [[domain/sources/slug...]]
            if slug not in hub:
                orphans.append(str(p.relative_to(corpus.parent)))
    return orphans


def find_stubs(corpus: Path) -> list[str]:
    stubs = []
    for p in content_pages(corpus):
        m = _STATUS_RE.search(p.read_text(encoding="utf-8", errors="ignore"))
        if m and m.group(1) == "stub":
            stubs.append(str(p.relative_to(corpus.parent)))
    return stubs


def lint(corpus: Path | None = None) -> dict:
    corpus = corpus if corpus is not None else CORPUS
    return {
        "broken_wikilinks": find_broken_wikilinks(corpus),
        "broken_citations": find_broken_citations(corpus),
        "orphans": find_orphans(corpus),
        "stubs": find_stubs(corpus),
        "okf_violations": len(okf_lint.lint_bundle(corpus)["violations"]),
    }


def main(argv=None) -> int:
    report = lint()
    integrity = report["broken_wikilinks"] + report["broken_citations"]
    print(f"corpus lint — {len(report['broken_wikilinks'])} broken wikilinks · "
          f"{len(report['broken_citations'])} broken citations · "
          f"{len(report['orphans'])} orphans · {len(report['stubs'])} stubs")
    for label in ("broken_wikilinks", "broken_citations"):
        for src, tgt in report[label]:
            print(f"  [{label}] {src} -> {tgt}")
    for label in ("orphans", "stubs"):
        for src in report[label]:
            print(f"  [{label}] {src}")
    # Non-zero exit only on integrity issues (orphans/stubs are advisory).
    return 1 if integrity else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

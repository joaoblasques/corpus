#!/usr/bin/env python3
"""Tests for bin/corpus_lint.py — deterministic corpus health checks."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import corpus_lint as cl  # noqa: E402


def _corpus(tmp_path: Path) -> Path:
    c = tmp_path / "corpus"
    (c / "ai-engineering").mkdir(parents=True)
    return c


def test_broken_wikilink_detected(tmp_path):
    c = _corpus(tmp_path)
    (c / "ai-engineering" / "README.md").write_text("# AI\n[[ai-engineering/llm|LLM]]\n", encoding="utf-8")
    (c / "ai-engineering" / "llm.md").write_text(
        "links to [[ai-engineering/missing|Missing]] and [[ai-engineering/llm|self]]\n", encoding="utf-8")
    broken = cl.find_broken_wikilinks(c)
    targets = [t for _, t in broken]
    assert "ai-engineering/missing" in targets
    assert "ai-engineering/llm" not in targets  # exists


def test_para_native_wikilink_skipped(tmp_path):
    c = _corpus(tmp_path)
    (c / "ai-engineering" / "README.md").write_text("# AI\n", encoding="utf-8")
    (c / "ai-engineering" / "p.md").write_text("[[03_Resources/Articles/foo|Foo]]\n", encoding="utf-8")
    assert cl.find_broken_wikilinks(c) == []  # not a corpus domain → skipped


def test_broken_citation_detected(tmp_path):
    c = _corpus(tmp_path)
    (c / "ai-engineering" / "README.md").write_text("# AI\n", encoding="utf-8")
    (c / "ai-engineering" / "p.md").write_text(
        "cite [src](../../raw/web/does-not-exist.md)\n", encoding="utf-8")
    broken = cl.find_broken_citations(c)
    assert broken and broken[0][1] == "../../raw/web/does-not-exist.md"


def test_orphan_detected_and_linked_not(tmp_path):
    c = _corpus(tmp_path)
    (c / "ai-engineering" / "README.md").write_text("# AI\n[[ai-engineering/linked|x]]\n", encoding="utf-8")
    (c / "ai-engineering" / "linked.md").write_text("body\n", encoding="utf-8")
    (c / "ai-engineering" / "orphan.md").write_text("body\n", encoding="utf-8")
    orphans = cl.find_orphans(c)
    assert any("orphan.md" in o for o in orphans)
    assert not any("linked.md" in o for o in orphans)


def test_stub_detected(tmp_path):
    c = _corpus(tmp_path)
    (c / "ai-engineering" / "README.md").write_text("# AI\n", encoding="utf-8")
    (c / "ai-engineering" / "s.md").write_text("---\nstatus: stub\n---\nbody\n", encoding="utf-8")
    (c / "ai-engineering" / "m.md").write_text("---\nstatus: mature\n---\nbody\n", encoding="utf-8")
    stubs = cl.find_stubs(c)
    assert any("s.md" in s for s in stubs)
    assert not any("m.md" in s for s in stubs)


def test_lint_aggregates(tmp_path):
    c = _corpus(tmp_path)
    (c / "ai-engineering" / "README.md").write_text("# AI\n", encoding="utf-8")
    (c / "ai-engineering" / "x.md").write_text("body\n", encoding="utf-8")
    report = cl.lint(c)
    assert set(report) == {"broken_wikilinks", "broken_citations", "orphans", "stubs", "okf_violations"}


def test_okf_violations_typeless_page_detected(tmp_path):
    """A page with no `type` field in frontmatter yields okf_violations >= 1."""
    c = _corpus(tmp_path)
    (c / "ai-engineering" / "README.md").write_text("# AI\n", encoding="utf-8")
    (c / "ai-engineering" / "typeless.md").write_text(
        "---\nstatus: stub\n---\nbody\n", encoding="utf-8")
    report = cl.lint(c)
    assert "okf_violations" in report
    assert report["okf_violations"] >= 1


def test_okf_violations_conformant_page_clean(tmp_path):
    """All pages with valid `type` fields yield okf_violations == 0."""
    c = _corpus(tmp_path)
    # README.md is also a concept page for OKF; give it type: hub so it's conformant.
    (c / "ai-engineering" / "README.md").write_text(
        "---\ntype: hub\n---\n# AI\n", encoding="utf-8")
    (c / "ai-engineering" / "good.md").write_text(
        "---\ntype: concept\nstatus: mature\n---\nbody\n", encoding="utf-8")
    report = cl.lint(c)
    assert report["okf_violations"] == 0


def test_meta_set_uses_okf_reserved_names():
    """_META must contain OKF reserved names (index.md / log.md) not the old underscore forms."""
    assert "index.md" in cl._META, "_META should contain 'index.md' (OKF reserved)"
    assert "log.md" in cl._META, "_META should contain 'log.md' (OKF reserved)"
    assert "_index.md" not in cl._META, "_META should NOT contain old '_index.md'"
    assert "_log.md" not in cl._META, "_META should NOT contain old '_log.md'"


def test_index_and_log_not_checked_for_broken_wikilinks(tmp_path):
    """index.md and log.md at the corpus root must be skipped (not checked for broken links)."""
    c = _corpus(tmp_path)
    (c / "ai-engineering" / "README.md").write_text("# AI\n", encoding="utf-8")
    # Place files with wikilinks at the corpus root — they should be skipped
    (c / "index.md").write_text("[[ai-engineering/does-not-exist|X]]\n", encoding="utf-8")
    (c / "log.md").write_text("[[ai-engineering/also-missing|Y]]\n", encoding="utf-8")
    broken = cl.find_broken_wikilinks(c)
    # Neither index.md nor log.md should produce broken-wikilink reports
    paths = [src for src, _ in broken]
    assert not any("index.md" in p for p in paths), "index.md should be skipped"
    assert not any("log.md" in p for p in paths), "log.md should be skipped"

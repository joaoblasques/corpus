#!/usr/bin/env python3
"""Tests for corpus_heal hub auto-index — preserves hand content, groups pages, zeroes orphans."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import corpus_heal as ch  # noqa: E402
import corpus_lint as cl  # noqa: E402


def _corpus(root: Path) -> Path:
    corpus = root / "corpus"
    d = corpus / "ai-engineering"
    (d / "sources").mkdir(parents=True)
    (d / "README.md").write_text("# AI Engineering\n\nHand-written overview I must keep.\n",
                                 encoding="utf-8")
    (d / "context-engineering.md").write_text("---\ntype: concept\n---\n# Context Engineering\n\nx",
                                              encoding="utf-8")
    (d / "anthropic.md").write_text("---\ntype: entity\n---\n# Anthropic\n\nx", encoding="utf-8")
    (d / "sources" / "yt-abc123.md").write_text("---\ntype: source\n---\n# A Talk on Agents\n\nx",
                                                encoding="utf-8")
    return corpus


def test_index_groups_and_collapses_sources(tmp_path):
    corpus = _corpus(tmp_path)
    section = ch.build_hub_index(corpus / "ai-engineering", corpus)
    assert "### Concepts (1)" in section
    assert "- [Context Engineering](/ai-engineering/context-engineering.md)" in section
    assert "### Entities (1)" in section
    assert "- [Anthropic](/ai-engineering/anthropic.md)" in section
    # sources collapsed in a <details> block
    assert "<summary>Source summaries (1)</summary>" in section
    assert "- [A Talk on Agents](/ai-engineering/sources/yt-abc123.md)" in section


def test_update_hub_preserves_handwritten_content(tmp_path):
    corpus = _corpus(tmp_path)
    readme = corpus / "ai-engineering" / "README.md"
    section = ch.build_hub_index(corpus / "ai-engineering", corpus)
    assert ch.update_hub(readme, section, apply=True) is True
    out = readme.read_text()
    assert "Hand-written overview I must keep." in out       # prose preserved
    assert ch.AUTO_START in out and ch.AUTO_END in out

    # idempotent + preserves prose on re-run (no change second time)
    section2 = ch.build_hub_index(corpus / "ai-engineering", corpus)
    assert ch.update_hub(readme, section2, apply=True) is False
    assert readme.read_text().count(ch.AUTO_START) == 1       # exactly one block


def test_indexing_zeroes_orphans(tmp_path):
    corpus = _corpus(tmp_path)
    assert len(cl.find_orphans(corpus)) == 3                  # all 3 pages orphaned initially
    ch.index_hubs(corpus, apply=True)
    assert cl.find_orphans(corpus) == []                     # every page now linked from its hub


def test_dry_run_writes_nothing(tmp_path, capsys):
    corpus = _corpus(tmp_path)
    original = (corpus / "ai-engineering" / "README.md").read_text()
    ch.cmd_hubs(ch._args(["hubs", "--corpus", str(corpus)]))
    out = json.loads(capsys.readouterr().out)
    assert out["applied"] is False and out["domains_changed"] == 1
    assert (corpus / "ai-engineering" / "README.md").read_text() == original

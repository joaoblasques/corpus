#!/usr/bin/env python3
"""Tests for corpus_heal cross-domain linker — symmetric, cross-domain-only, reversible."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import corpus_heal as ch  # noqa: E402


def _page(dir_: Path, slug: str, typ: str, tags: list[str], title: str) -> Path:
    dir_.mkdir(parents=True, exist_ok=True)
    tagblock = "\n".join(f"  - {t}" for t in tags)
    p = dir_ / f"{slug}.md"
    p.write_text(f"---\ntype: {typ}\ntags:\n  - source\n{tagblock}\n---\n# {title}\n\nbody\n",
                 encoding="utf-8")
    return p


def _corpus(root: Path) -> Path:
    """Exactly ONE cross-domain pair: rag-agents (ai) ↔ retrieval-pipelines (data)."""
    c = root / "corpus"
    _page(c / "ai-engineering", "rag-agents", "concept", ["Retrieval", "Agents"], "RAG Agents")
    _page(c / "data-engineering", "retrieval-pipelines", "concept", ["Retrieval", "Agents"],
          "Retrieval Pipelines")
    _page(c / "mlops", "kubernetes", "concept", ["Orchestration"], "Kubernetes")  # unrelated
    return c


def test_build_related_is_cross_domain_and_symmetric(tmp_path):
    corpus = _corpus(tmp_path)
    # add a SAME-domain page sharing the same signals — it must not link to rag-agents
    _page(corpus / "ai-engineering", "agent-memory", "concept", ["Retrieval", "Agents"], "Agent Memory")
    rel, nodes = ch.build_related(corpus, min_shared=2)
    # the two cross-domain pages relate, both directions
    assert "data-engineering/retrieval-pipelines" in [r[0] for r in rel["ai-engineering/rag-agents"]]
    assert "ai-engineering/rag-agents" in [r[0] for r in rel["data-engineering/retrieval-pipelines"]]
    # rag-agents never links its same-domain sibling agent-memory
    assert "ai-engineering/agent-memory" not in [r[0] for r in rel.get("ai-engineering/rag-agents", [])]
    # no relation is ever same-domain
    for node, links in rel.items():
        for other, *_ in links:
            assert other.split("/")[0] != node.split("/")[0]
    assert "mlops/kubernetes" not in rel


def test_index_related_writes_symmetric_reversible_block(tmp_path):
    corpus = _corpus(tmp_path)
    t = ch.index_related(corpus, apply=True, min_shared=2)
    assert t["pairs"] == 1 and t["pages_linked"] == 2

    a = (corpus / "ai-engineering" / "rag-agents.md").read_text()
    b = (corpus / "data-engineering" / "retrieval-pipelines.md").read_text()
    assert "## Related across domains" in a
    assert "[Retrieval Pipelines](/data-engineering/retrieval-pipelines.md)" in a
    assert "[RAG Agents](/ai-engineering/rag-agents.md)" in b     # symmetric
    assert ch.RELATED_START in a and ch.RELATED_END in a

    # idempotent: re-run makes no change
    assert ch.index_related(corpus, apply=True, min_shared=2)["pages_linked"] == 0

    # reversible: raise the bar so nothing relates -> the block is removed
    t2 = ch.index_related(corpus, apply=True, min_shared=99)
    assert t2["blocks_removed"] == 2
    assert "## Related across domains" not in (corpus / "ai-engineering" / "rag-agents.md").read_text()


def test_skips_already_linked_pairs(tmp_path):
    corpus = _corpus(tmp_path)
    # make rag-agents already link to retrieval-pipelines in prose
    p = corpus / "ai-engineering" / "rag-agents.md"
    p.write_text(p.read_text() + "\nSee [pipelines](/data-engineering/retrieval-pipelines.md).\n",
                 encoding="utf-8")
    rel, _ = ch.build_related(corpus, min_shared=2)
    # already linked -> not re-proposed either direction
    assert "ai-engineering/rag-agents" not in rel
    assert "data-engineering/retrieval-pipelines" not in rel


def test_related_dry_run_writes_nothing(tmp_path, capsys):
    corpus = _corpus(tmp_path)
    before = (corpus / "ai-engineering" / "rag-agents.md").read_text()
    ch.cmd_related(ch._args(["related", "--corpus", str(corpus)]))
    out = json.loads(capsys.readouterr().out)
    assert out["applied"] is False and out["pairs"] == 1
    assert (corpus / "ai-engineering" / "rag-agents.md").read_text() == before

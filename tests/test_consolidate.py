import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import consolidate as co  # noqa: E402

SOURCE = """---
type: source
domain: ai-engineering
tags:
  - corpus/ai-engineering
  - source
  - youtube-quick-intake
  - Claude Code
  - RAG
---

# A Talk

Body text.

**Key topics**
- Claude Code
- context windows
- RAG
"""

def test_read_topics_merges_bullets_and_tags_drops_generic():
    topics = co.read_topics(SOURCE)
    assert "claude code" in topics
    assert "context windows" in topics
    assert "rag" in topics
    # generic tags are dropped
    assert "source" not in topics
    assert "corpus/ai-engineering" not in topics
    assert "youtube-quick-intake" not in topics
    # de-duped (Claude Code appears in both tags and bullets)
    assert topics.count("claude code") == 1

def test_page_type_reads_frontmatter():
    assert co.page_type(SOURCE) == "source"
    assert co.page_type("no frontmatter") == ""

def test_iter_source_pages_filters_type_and_domain(tmp_path):
    corpus = tmp_path / "corpus"
    (corpus / "ai-engineering" / "sources").mkdir(parents=True)
    (corpus / "data-engineering").mkdir(parents=True)
    (corpus / "ai-engineering" / "sources" / "s1.md").write_text(SOURCE, encoding="utf-8")
    (corpus / "ai-engineering" / "concept.md").write_text("---\ntype: concept\n---\n", encoding="utf-8")
    (corpus / "data-engineering" / "s2.md").write_text(SOURCE.replace("ai-engineering", "data-engineering"), encoding="utf-8")
    all_src = co.iter_source_pages(corpus)
    assert len(all_src) == 2  # both source pages, concept excluded
    ai_only = co.iter_source_pages(corpus, domain="ai-engineering")
    assert [p.name for p in ai_only] == ["s1.md"]

def _src(topics):
    tags = "\n".join(f"  - {t}" for t in topics)
    return f"---\ntype: source\ndomain: ai-engineering\ntags:\n  - source\n{tags}\n---\n# t\nbody\n"

def test_build_clusters_groups_by_topic_and_min_size(tmp_path):
    corpus = tmp_path / "corpus"
    d = corpus / "ai-engineering" / "sources"
    d.mkdir(parents=True)
    for i in range(5):
        (d / f"s{i}.md").write_text(_src(["RAG", "context"]), encoding="utf-8")
    for i in range(2):
        (d / f"o{i}.md").write_text(_src(["obscure"]), encoding="utf-8")
    clusters = co.build_clusters(corpus, "ai-engineering", min_cluster=5)
    topics = {c["topic"]: c for c in clusters}
    assert "rag" in topics and topics["rag"]["size"] == 5          # 5 sources share RAG
    assert "context" in topics                                      # also shared by 5
    assert "obscure" not in topics                                  # only 2 -> below min
    assert topics["rag"]["members"][0].startswith("ai-engineering/sources/")

def test_existing_topic_keys_and_ranking(tmp_path):
    corpus = tmp_path / "corpus"
    (corpus / "ai-engineering" / "sources").mkdir(parents=True)
    (corpus / "ai-engineering" / "rag.md").write_text(
        "---\ntype: concept\n---\n# RAG\n", encoding="utf-8")
    existing = co.existing_topic_keys(corpus, "ai-engineering")
    assert "rag" in existing
    clusters = [
        {"topic": "rag", "domain": "ai-engineering", "members": ["a", "b"], "size": 8},
        {"topic": "agents", "domain": "ai-engineering", "members": ["c"], "size": 6},
    ]
    ranked = co.rank_clusters(clusters, existing)
    # 'agents' has no existing page -> ranks before 'rag' despite smaller size
    assert ranked[0]["topic"] == "agents" and ranked[0]["has_existing_page"] is False
    assert ranked[1]["topic"] == "rag" and ranked[1]["has_existing_page"] is True

def test_clusters_cli_prints_ranked_json(tmp_path, capsys):
    import json
    corpus = tmp_path / "corpus"
    d = corpus / "ai-engineering" / "sources"
    d.mkdir(parents=True)
    for i in range(5):
        (d / f"s{i}.md").write_text(_src(["RAG"]), encoding="utf-8")
    rc = co.main(["clusters", "--corpus", str(corpus), "--domain", "ai-engineering", "--min", "5"])
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out["domain"] == "ai-engineering"
    assert out["count"] == 1
    assert out["clusters"][0]["topic"] == "rag" and out["clusters"][0]["size"] == 5


def test_read_topics_drops_none_extracted_placeholder():
    src = ("---\ntype: source\ntags:\n  - source\n  - RAG\n---\n# t\n\n"
           "**Key topics**\n- (none extracted)\n- RAG\n")
    topics = co.read_topics(src)
    assert "rag" in topics
    assert "(none extracted)" not in topics and "none extracted" not in topics


def test_rank_deepen_candidates_matches_pages_and_scores_thin_first(tmp_path):
    corpus = tmp_path / "corpus"
    d = corpus / "ai-engineering"
    (d / "sources").mkdir(parents=True)
    # existing pages: 'openai' is THIN, 'prompt-engineering' is DEEP
    (d / "openai.md").write_text("---\ntype: entity\n---\n# OpenAI\n\n" + "word " * 40, encoding="utf-8")
    (d / "prompt-engineering.md").write_text(
        "---\ntype: concept\n---\n# Prompt Engineering\n\n" + "word " * 400, encoding="utf-8")
    # 3 sources tagged OpenAI, 3 tagged Prompt Engineering
    for i in range(3):
        (d / "sources" / f"o{i}.md").write_text(
            "---\ntype: source\ntags:\n  - source\n  - OpenAI\n---\n# s\nbody", encoding="utf-8")
        (d / "sources" / f"p{i}.md").write_text(
            "---\ntype: source\ntags:\n  - source\n  - Prompt Engineering\n---\n# s\nbody", encoding="utf-8")

    cands = co.rank_deepen_candidates(corpus, "ai-engineering", min_cluster=3)
    topics = [c["topic"] for c in cands]
    assert "openai" in topics and "prompt engineering" in topics
    # thin page (openai, ~40 words) outranks the deep page (prompt-engineering, ~400 words)
    assert topics[0] == "openai"
    top = cands[0]
    assert top["target_page"] == "ai-engineering/openai.md"
    assert top["size"] == 3 and top["page_words"] >= 40
    assert top["score"] > cands[topics.index("prompt engineering")]["score"]


def test_rank_deepen_skips_clusters_without_an_existing_page(tmp_path):
    corpus = tmp_path / "corpus"
    d = corpus / "ai-engineering"
    (d / "sources").mkdir(parents=True)
    for i in range(3):   # a cluster with NO matching page
        (d / "sources" / f"x{i}.md").write_text(
            "---\ntype: source\ntags:\n  - source\n  - Nonesuch\n---\n# s\nbody", encoding="utf-8")
    assert co.rank_deepen_candidates(corpus, "ai-engineering", min_cluster=3) == []

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

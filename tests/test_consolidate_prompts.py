import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import consolidate_prompts as cp  # noqa: E402

def test_triage_prompt_asks_for_json_mode_and_lists_titles():
    p = cp.triage_prompt("rag", "ai-engineering", ["Talk A", "Post B"])
    assert "rag" in p and "ai-engineering" in p
    assert "Talk A" in p and "Post B" in p
    # must request a strict JSON verdict with the three modes
    assert "new-synthesis" in p and "deepen-existing" in p and "reject" in p
    assert "JSON" in p or "json" in p

def test_synthesis_prompt_enforces_provenance_and_paths():
    p = cp.synthesis_prompt("rag", "ai-engineering", "rag-patterns",
                            ["ai-engineering/sources/s1.md", "ai-engineering/sources/s2.md"])
    assert "corpus/ai-engineering/rag-patterns.md" in p          # exact output path
    assert "s1.md" in p and "s2.md" in p                          # member pages listed
    assert "cite" in p.lower() and "type: synthesis" in p        # provenance + type
    assert "consolidates:" in p                                   # required frontmatter field
    assert "25" in p                                              # quote length limit

def test_deepen_prompt_preserves_existing_and_integrates_new():
    p = cp.deepen_prompt("ai-engineering/openai.md", "openai",
                         ["ai-engineering/sources/o1.md", "ai-engineering/sources/o2.md"])
    assert "corpus/ai-engineering/openai.md" in p            # the exact file to edit
    assert "o1.md" in p and "o2.md" in p                      # member sources listed
    # must instruct: preserve existing, integrate new, cite, don't drop, don't invent
    low = p.lower()
    assert "preserve" in low or "keep" in low
    assert "do not" in low or "never" in low                 # a prohibition (drop/invent)
    assert "cite" in low and "footnote" in low
    assert "25" in p                                          # quote length limit

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "website" / "hooks"))
import corpus_graph as cg  # noqa: E402


def _corpus(tmp_path):
    d = tmp_path / "ai-engineering"
    d.mkdir()
    (d / "README.md").write_text("# AI Engineering\nhub page", encoding="utf-8")
    (d / "transformer.md").write_text("# Transformer\nUses [[ai-engineering/attention|attention]].", encoding="utf-8")
    (d / "attention.md").write_text("# Attention\nbody", encoding="utf-8")
    (d / "_orphan.md").write_text("# skip me", encoding="utf-8")  # underscore → skipped
    meta = tmp_path / "_meta"
    meta.mkdir()
    (meta / "x.md").write_text("# catalog", encoding="utf-8")     # underscore dir → skipped
    return tmp_path


def test_nodes_pages_and_hub(tmp_path):
    g = cg.build_graph(_corpus(tmp_path))
    ids = {n["id"] for n in g["nodes"]}
    assert "ai-engineering/transformer" in ids
    assert "ai-engineering/attention" in ids
    assert "ai-engineering" in ids                    # domain hub node
    assert "ai-engineering/_orphan" not in ids        # underscore page skipped
    assert not any(n["id"].startswith("_meta") for n in g["nodes"])  # underscore dir skipped


def test_label_from_h1_and_group(tmp_path):
    g = cg.build_graph(_corpus(tmp_path))
    t = next(n for n in g["nodes"] if n["id"] == "ai-engineering/transformer")
    assert t["label"] == "Transformer" and t["group"] == "ai-engineering"
    hub = next(n for n in g["nodes"] if n["id"] == "ai-engineering")
    assert hub.get("hub") is True


def test_edges_wikilink_and_spoke(tmp_path):
    g = cg.build_graph(_corpus(tmp_path))
    pairs = {tuple(sorted((e["from"], e["to"]))) for e in g["edges"]}
    assert tuple(sorted(("ai-engineering/transformer", "ai-engineering/attention"))) in pairs  # wikilink
    assert tuple(sorted(("ai-engineering/transformer", "ai-engineering"))) in pairs            # spoke to hub
    # no duplicate edges
    assert len(g["edges"]) == len(pairs)

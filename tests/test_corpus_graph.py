import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "website" / "hooks"))
import corpus_graph as cg  # noqa: E402


def _page(corpus: Path, domain: str, slug: str, typ: str, body: str, links=()):
    d = corpus / domain
    d.mkdir(parents=True, exist_ok=True)
    link_md = "".join(f"\nSee [x](/{t}.md)." for t in links)
    (d / f"{slug}.md").write_text(
        f"---\ntype: {typ}\ndomain: {domain}\nstatus: draft\n---\n# {slug.title()}\n\n{body}{link_md}\n",
        encoding="utf-8")


def test_depth_is_body_word_count_excluding_frontmatter(tmp_path):
    corpus = tmp_path / "corpus"
    _page(corpus, "ai-engineering", "rag", "concept", "one two three four five")
    g = cg.build_graph(corpus)
    node = next(n for n in g["nodes"] if n["id"] == "ai-engineering/rag")
    # body is "# Rag" + blank + "one two three four five" => 5 content words + heading words.
    # frontmatter (type/domain/status) must NOT be counted.
    assert node["depth"] >= 5
    assert "status" not in str(node)              # status value never leaks into the node
    # a deeper page has a strictly larger depth
    _page(corpus, "ai-engineering", "big", "concept", "word " * 200)
    g2 = cg.build_graph(corpus)
    big = next(n for n in g2["nodes"] if n["id"] == "ai-engineering/big")
    assert big["depth"] > node["depth"]


def test_degree_counts_incident_edges(tmp_path):
    corpus = tmp_path / "corpus"
    # rag links to pipelines; both also spoke to their hubs
    _page(corpus, "ai-engineering", "rag", "concept", "body", links=["data-engineering/pipelines"])
    _page(corpus, "data-engineering", "pipelines", "concept", "body")
    g = cg.build_graph(corpus)
    deg = {n["id"]: n["degree"] for n in g["nodes"]}
    # rag: spoke(->ai-engineering hub) + link(->pipelines) = 2
    assert deg["ai-engineering/rag"] == 2
    # pipelines: spoke + the incoming link = 2
    assert deg["data-engineering/pipelines"] == 2
    # a hub's degree >= number of its pages (each page spokes to it)
    assert deg["ai-engineering"] >= 1


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


def _source(corpus: Path, domain: str, slug: str):
    d = corpus / domain / "sources"
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{slug}.md").write_text(
        f"---\ntype: source\ndomain: {domain}\n---\n# {slug}\n\nsummary\n", encoding="utf-8")


def test_hub_sources_counts_source_pages_in_domain(tmp_path):
    corpus = tmp_path / "corpus"
    _page(corpus, "data-engineering", "pipelines", "concept", "body")   # knowledge, not a source
    _source(corpus, "data-engineering", "s1")
    _source(corpus, "data-engineering", "s2")
    g = cg.build_graph(corpus)
    hub = next(n for n in g["nodes"] if n["id"] == "data-engineering" and n.get("hub"))
    assert hub["sources"] == 2                        # two source pages; the concept isn't counted


def test_bridge_flag_only_on_cross_domain_page_edges(tmp_path):
    corpus = tmp_path / "corpus"
    _page(corpus, "ai-engineering", "rag", "concept", "b", links=["data-engineering/pipelines"])
    _page(corpus, "data-engineering", "pipelines", "concept", "b")
    _page(corpus, "ai-engineering", "agents", "concept", "b", links=["ai-engineering/rag"])
    g = cg.build_graph(corpus)

    def edge(a, b):
        return next(e for e in g["edges"]
                    if {e["from"], e["to"]} == {a, b})
    # cross-domain page->page: bridge
    assert edge("ai-engineering/rag", "data-engineering/pipelines").get("bridge") is True
    # same-domain page->page: NOT a bridge
    assert edge("ai-engineering/agents", "ai-engineering/rag").get("bridge") is not True
    # spoke (page->hub): NOT a bridge
    assert edge("ai-engineering/rag", "ai-engineering").get("bridge") is not True


def test_node_carries_created_and_aliases(tmp_path):
    corpus = tmp_path / "corpus"; d = corpus / "ai-engineering"; d.mkdir(parents=True)
    (d / "openai.md").write_text(
        "---\ntype: entity\ncreated: 2026-06-17\naliases:\n  - GPT-4\n  - o4-mini\n---\n# OpenAI\nbody",
        encoding="utf-8")
    g = cg.build_graph(corpus)
    n = next(x for x in g["nodes"] if x["id"] == "ai-engineering/openai")
    assert n["created"] == "2026-06-17"
    assert n["aliases"] == ["GPT-4", "o4-mini"]


def test_node_without_created_or_aliases_is_safe(tmp_path):
    corpus = tmp_path / "corpus"; d = corpus / "ai-engineering"; d.mkdir(parents=True)
    (d / "bare.md").write_text("---\ntype: concept\n---\n# Bare\nbody", encoding="utf-8")
    g = cg.build_graph(corpus)
    n = next(x for x in g["nodes"] if x["id"] == "ai-engineering/bare")
    assert n.get("created") is None
    assert n["aliases"] == []

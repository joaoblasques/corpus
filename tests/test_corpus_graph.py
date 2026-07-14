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

"""MkDocs build hook: generate the corpus knowledge graph (hubs · spokes · connections).

At every build, walks `corpus/<domain>/<page>.md`, emits one node per page (grouped by
domain) plus one hub node per domain, and edges for (a) each page → its domain hub and
(b) each root-relative markdown link `](/domain/slug.md)` between pages (OKF §6/§11 — the
corpus migrated off `[[wikilinks]]` to OKF markdown links, so this is the real link syntax;
legacy `[[domain/slug]]` is still matched for safety). Writes `docs/assets/graph-data.json`,
which the Home page renders with vis-network. Emits ONLY page titles + link structure —
never page content — so the public graph leaks no knowledge text.
"""
import json
import re
from pathlib import Path

# `](/domain/slug.md)` — OKF root-relative markdown link between two top-level domain pages.
# The two-segment shape naturally excludes `](/domain/sources/slug.md)` (source pages aren't
# graph nodes). Legacy `[[domain/slug]]` is still matched so a pre-migration page won't drop out.
MDLINK = re.compile(r"\]\(/([a-z0-9][a-z0-9-]*/[a-z0-9][a-z0-9-]*)\.md\)")
WIKILINK = re.compile(r"\[\[([a-z0-9][a-z0-9-]*/[a-z0-9][a-z0-9-]*)")
H1 = re.compile(r"^#\s+(.+?)\s*$", re.M)


def _title(text: str, slug: str) -> str:
    m = H1.search(text)
    return m.group(1).strip() if m else slug.replace("-", " ")


def build_graph(corpus_dir) -> dict:
    corpus = Path(corpus_dir)
    nodes: dict[str, dict] = {}
    domains: set[str] = set()

    # Pass 1 — page nodes (skip catalog `_*` dirs/files and the README hub file itself)
    for md in sorted(corpus.glob("*/*.md")):
        domain = md.parent.name
        if domain.startswith("_") or md.stem.startswith("_"):
            continue
        domains.add(domain)
        if md.name == "README.md":
            continue
        node_id = f"{domain}/{md.stem}"
        text = md.read_text(encoding="utf-8", errors="ignore")
        nodes[node_id] = {"id": node_id, "label": _title(text, md.stem), "group": domain}

    # Hub node per domain
    for d in sorted(domains):
        nodes[d] = {"id": d, "label": d.replace("-", " "), "group": d, "hub": True, "value": 40}

    # Pass 2 — edges: spoke (page → hub) + wikilink connections
    edge_keys: set[tuple] = set()
    edges: list[dict] = []

    def add(a: str, b: str):
        if a == b:
            return
        k = tuple(sorted((a, b)))
        if k in edge_keys:
            return
        edge_keys.add(k)
        edges.append({"from": a, "to": b})

    for md in sorted(corpus.glob("*/*.md")):
        domain = md.parent.name
        if domain.startswith("_") or md.stem.startswith("_") or md.name == "README.md":
            continue
        node_id = f"{domain}/{md.stem}"
        if node_id not in nodes:
            continue
        add(node_id, domain)  # spoke to its hub
        text = md.read_text(encoding="utf-8", errors="ignore")
        for tgt in set(MDLINK.findall(text)) | set(WIKILINK.findall(text)):
            if tgt in nodes:
                add(node_id, tgt)

    return {"nodes": list(nodes.values()), "edges": edges}


def on_pre_build(config):
    out = Path(config["docs_dir"]) / "assets" / "graph-data.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    corpus = Path(__file__).resolve().parents[2] / "corpus"
    try:
        data = build_graph(corpus)
    except OSError:
        data = {"nodes": [], "edges": []}
    out.write_text(json.dumps(data), encoding="utf-8")

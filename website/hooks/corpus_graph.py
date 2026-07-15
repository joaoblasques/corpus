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
_TYPE_RE = re.compile(r"^type:\s*(\w+)", re.M)
_CREATED_RE = re.compile(r"^created:\s*(\S+)", re.M)
_ALIASES_BLOCK_RE = re.compile(r"^aliases:\s*\n((?:[ \t]*-[ \t]*.+\n?)+)", re.M)


def _created(text: str) -> str | None:
    """The page's `created:` frontmatter date (ISO string), or None. Content-safe (a date)."""
    fm = text.split("---", 2)[1] if text.startswith("---") else ""
    m = _CREATED_RE.search(fm)
    return m.group(1).strip().strip('"\'') if m else None


def _aliases(text: str) -> list:
    """The page's `aliases:` list (short alternate names), or []. Content-safe (labels)."""
    fm = text.split("---", 2)[1] if text.startswith("---") else ""
    m = _ALIASES_BLOCK_RE.search(fm)
    if not m:
        return []
    out = []
    for line in m.group(1).splitlines():
        line = line.strip()
        if line.startswith("-"):
            out.append(line[1:].strip().strip('"\''))
    return [a for a in out if a]


def _body_wordcount(text: str) -> int:
    """Word count of the page BODY (frontmatter stripped) — a depth signal, never the text."""
    body = text.split("---", 2)[-1] if text.startswith("---") else text
    return len(body.split())


def _source_count(domain_dir: Path) -> int:
    """Count `type: source` pages anywhere under a domain dir (incl. its sources/ subdir)."""
    n = 0
    if domain_dir.exists():
        for p in domain_dir.rglob("*.md"):
            m = _TYPE_RE.search(p.read_text(encoding="utf-8", errors="ignore"))
            if m and m.group(1) == "source":
                n += 1
    return n


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
        nodes[node_id] = {"id": node_id, "label": _title(text, md.stem), "group": domain,
                          "depth": _body_wordcount(text),
                          "created": _created(text), "aliases": _aliases(text)}

    # Hub node per domain (+ content-safe per-domain aggregates: page count, mean depth)
    for d in sorted(domains):
        dom_pages = [n for n in nodes.values() if not n.get("hub") and n.get("group") == d]
        avg_depth = round(sum(p["depth"] for p in dom_pages) / len(dom_pages)) if dom_pages else 0
        nodes[d] = {"id": d, "label": d.replace("-", " "), "group": d, "hub": True,
                    "value": 40, "sources": _source_count(corpus / d),
                    "pages": len(dom_pages), "avg_depth": avg_depth}

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
        edge = {"from": a, "to": b}
        # bridge = a link between two PAGE nodes (ids contain "/") in DIFFERENT domains.
        if "/" in a and "/" in b and a.split("/")[0] != b.split("/")[0]:
            edge["bridge"] = True
        edges.append(edge)

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

    # degree = incident-edge count per node (orphans -> 1: their lone spoke to the hub)
    degree: dict[str, int] = {}
    for e in edges:
        degree[e["from"]] = degree.get(e["from"], 0) + 1
        degree[e["to"]] = degree.get(e["to"], 0) + 1
    for n in nodes.values():
        n["degree"] = degree.get(n["id"], 0)

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

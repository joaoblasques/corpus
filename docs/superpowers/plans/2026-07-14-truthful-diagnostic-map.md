# Truthful Diagnostic Map Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Enrich the public knowledge graph so every visual channel is truthful — node size = connection count, lightness = page depth, hub labels show source-backing, cross-domain bridges distinct, orphans tiny.

**Architecture:** Two files. `website/hooks/corpus_graph.py` (pure-Python data builder, run at every MkDocs build) gains four new computed fields on the graph JSON — per-node `depth` and `degree`, per-hub `sources`, per-edge `bridge`. `website/docs/assets/graph.js` (front-end renderer) maps those fields to vis-network visuals. The data builder is TDD'd (its first tests); the renderer is validated by a local build + screenshot.

**Tech Stack:** Python 3.12 stdlib (re, pathlib, json) + pytest; vis-network (already vendored) in a plain-JS MkDocs hook. No new dependencies.

## Global Constraints

- **Stdlib only** — no new Python deps; `graph.js` stays dependency-free plain JS.
- **Additive only:** do NOT change which nodes/edges exist, the node/edge id scheme, `on_pre_build`, or the deploy path. Only ADD attributes + rendering.
- **Never emit page content** — only titles, counts, and link/structure fields (the graph is public; leaking body text is forbidden). `depth` is a word COUNT, not text.
- **Shade by depth (word count), NOT the `status` field** — status is 97% "draft" and uninformative.
- **Source pages are not nodes** — surfaced only as an aggregate `sources` count on hub nodes.
- **Node/edge JSON contract (after this plan):**
  - page node: `{id, label, group, depth, degree}`
  - hub node: `{id, label, group, hub: true, value, sources, degree}`
  - edge: `{from, to}` plus `bridge: true` ONLY on cross-domain page-to-page edges.
- **Tests never read the real corpus** — every test uses a `tmp_path` fixture corpus.

---

## File Structure

| File | Responsibility |
|---|---|
| `website/hooks/corpus_graph.py` | MODIFY `build_graph()`: add `depth`+`degree` (nodes), `sources` (hubs), `bridge` (edges). Pure; the testable core. |
| `tests/test_corpus_graph.py` | CREATE: unit tests for the four new fields against a fixture corpus (this module has no tests today). |
| `website/docs/assets/graph.js` | MODIFY the renderer: size=degree, lightness=depth bucket, hub label +sources, bridge edge color, orphan dashed border. |

Note on `corpus_graph.py` as it exists today (do not remove any of this):
```python
WIKILINK = re.compile(r"\[\[([a-z0-9][a-z0-9-]*/[a-z0-9][a-z0-9-]*)")
MDLINK = re.compile(r"\]\(/([a-z0-9][a-z0-9-]*/[a-z0-9][a-z0-9-]*)\.md\)")
H1 = re.compile(r"^#\s+(.+?)\s*$", re.M)

def _title(text, slug): ...                       # first H1 or slug
def build_graph(corpus_dir) -> dict:
    # Pass 1: page nodes  {id, label, group}   (skip _dirs/_files + README.md)
    # Hub node per domain: {id, label, group, hub: True, value: 40}
    # Pass 2: edges via add(a,b) — spoke (page->domain hub) + MDLINK/WIKILINK page->page
    return {"nodes": list(nodes.values()), "edges": edges}
def on_pre_build(config): ...                      # writes docs/assets/graph-data.json
```

---

### Task 1: `depth` + `degree` node fields (`corpus_graph.py`)

**Files:**
- Modify: `website/hooks/corpus_graph.py` (add `_TYPE_RE`; add `depth` in Pass 1; add a degree pass before `return`)
- Test: `tests/test_corpus_graph.py` (create)

**Interfaces:**
- Consumes: existing `build_graph(corpus_dir)->dict`.
- Produces: every page node gains `depth` (int, body word count, frontmatter excluded); every node (page AND hub) gains `degree` (int, count of incident edges).

- [ ] **Step 1: Write the failing test**

```python
# tests/test_corpus_graph.py
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/Dev/corpus && python3 -m pytest tests/test_corpus_graph.py -q -p no:cacheprovider`
Expected: FAIL — `KeyError: 'depth'` (nodes have no `depth`/`degree` yet).

- [ ] **Step 3: Add `_TYPE_RE`, `depth` in Pass 1, and a degree pass**

In `website/hooks/corpus_graph.py`, add this regex next to the others (below `H1 = ...`):
```python
_TYPE_RE = re.compile(r"^type:\s*(\w+)", re.M)


def _body_wordcount(text: str) -> int:
    """Word count of the page BODY (frontmatter stripped) — a depth signal, never the text."""
    body = text.split("---", 2)[-1] if text.startswith("---") else text
    return len(body.split())
```

In Pass 1, where the page node dict is built, add `depth`:
```python
        nodes[node_id] = {"id": node_id, "label": _title(text, md.stem), "group": domain,
                          "depth": _body_wordcount(text)}
```

Immediately before `return {"nodes": list(nodes.values()), "edges": edges}`, add the degree pass:
```python
    # degree = incident-edge count per node (orphans -> 1: their lone spoke to the hub)
    degree: dict[str, int] = {}
    for e in edges:
        degree[e["from"]] = degree.get(e["from"], 0) + 1
        degree[e["to"]] = degree.get(e["to"], 0) + 1
    for n in nodes.values():
        n["degree"] = degree.get(n["id"], 0)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ~/Dev/corpus && python3 -m pytest tests/test_corpus_graph.py -q -p no:cacheprovider`
Expected: PASS (2 passed).

- [ ] **Step 5: Commit**

```bash
cd ~/Dev/corpus
git add website/hooks/corpus_graph.py tests/test_corpus_graph.py
git commit -m "feat(graph): emit per-node depth (word count) + degree"
```

---

### Task 2: hub `sources` + edge `bridge` (`corpus_graph.py`)

**Files:**
- Modify: `website/hooks/corpus_graph.py` (add `_source_count`; set `sources` on hub nodes; set `bridge` on cross-domain edges via the `add()` helper)
- Test: `tests/test_corpus_graph.py` (append)

**Interfaces:**
- Consumes: `build_graph` with Task 1's fields.
- Produces: each hub node gains `sources` (int = count of `type: source` pages under `corpus/<domain>/`, including its `sources/` subdir); each cross-domain page-to-page edge gains `bridge: true` (absent/false otherwise).

- [ ] **Step 1: Write the failing test**

```python
# tests/test_corpus_graph.py  (append)
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/Dev/corpus && python3 -m pytest tests/test_corpus_graph.py -q -p no:cacheprovider`
Expected: FAIL — `KeyError: 'sources'` (and the bridge assertions fail).

- [ ] **Step 3: Implement `sources` + `bridge`**

Add a source-counter helper near `_body_wordcount`:
```python
def _source_count(domain_dir: Path) -> int:
    """Count `type: source` pages anywhere under a domain dir (incl. its sources/ subdir)."""
    n = 0
    if domain_dir.exists():
        for p in domain_dir.rglob("*.md"):
            m = _TYPE_RE.search(p.read_text(encoding="utf-8", errors="ignore"))
            if m and m.group(1) == "source":
                n += 1
    return n
```

In the hub-node loop, add `sources`:
```python
    for d in sorted(domains):
        nodes[d] = {"id": d, "label": d.replace("-", " "), "group": d, "hub": True,
                    "value": 40, "sources": _source_count(corpus / d)}
```

Mark bridges when building edges. The `add(a, b)` helper appends `{"from": a, "to": b}`; make a
page-to-page edge in two different domains carry `bridge: true`. Replace the edge-append line
inside `add` so it reads:
```python
        edge = {"from": a, "to": b}
        # bridge = a link between two PAGE nodes (ids contain "/") in DIFFERENT domains.
        if "/" in a and "/" in b and a.split("/")[0] != b.split("/")[0]:
            edge["bridge"] = True
        edges.append(edge)
```
(Spoke edges have a hub endpoint whose id has no `/`, so they never get `bridge`.)

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ~/Dev/corpus && python3 -m pytest tests/test_corpus_graph.py -q -p no:cacheprovider`
Expected: PASS (4 passed).

- [ ] **Step 5: Verify the real graph still builds + inspect the new fields**

Run:
```bash
cd ~/Dev/corpus && python3 -c "import sys; sys.path.insert(0,'website/hooks'); import corpus_graph as cg, json; \
g=cg.build_graph('corpus'); \
print('nodes', len(g['nodes']), 'edges', len(g['edges'])); \
print('sample page', next(n for n in g['nodes'] if not n.get('hub'))); \
print('a hub', next(n for n in g['nodes'] if n.get('hub'))); \
print('bridges', sum(1 for e in g['edges'] if e.get('bridge')))"
```
Expected: prints a page node with `depth`+`degree`, a hub with `sources`, and a non-zero bridge count (~110).

- [ ] **Step 6: Commit**

```bash
cd ~/Dev/corpus
git add website/hooks/corpus_graph.py tests/test_corpus_graph.py
git commit -m "feat(graph): emit per-hub source counts + per-edge cross-domain bridge flag"
```

---

### Task 3: Renderer — size, depth-shade, hub labels, bridges, orphans (`graph.js`)

**Files:**
- Modify: `website/docs/assets/graph.js` (the node/edge mapping in `render()`)

**Interfaces:**
- Consumes: `graph-data.json` nodes with `depth`/`degree`/`sources` and edges with `bridge` (Tasks 1–2).
- Produces: rendered visuals — no code consumes this; validated by local build.

There is no unit test for front-end JS here; validation is a local `mkdocs build` + eyeball (Step 3).

- [ ] **Step 1: Replace the node + edge mapping**

In `website/docs/assets/graph.js`, replace the `data.nodes.forEach(...)` block (currently lines
22–34) with this — it keeps hue = domain, adds a `_lighten` helper, and maps the new fields:
```javascript
        function _lighten(hex, f) {              // mix a hex color toward the page bg (#faf8f2)
          var b = { r: 250, g: 248, b: 242 };
          var r = parseInt(hex.slice(1, 3), 16), g = parseInt(hex.slice(3, 5), 16), bl = parseInt(hex.slice(5, 7), 16);
          function mix(c, t) { return Math.round(c + (t - c) * f); }
          function h2(x) { return ("0" + x.toString(16)).slice(-2); }
          return "#" + h2(mix(r, b.r)) + h2(mix(g, b.g)) + h2(mix(bl, b.b));
        }
        function _depthTier(d) {                  // 0=thin ... 3=deep -> lighten fraction
          if (d < 300) return 0.6;
          if (d < 800) return 0.4;
          if (d < 1800) return 0.2;
          return 0.0;
        }
        data.nodes.forEach(function (n) {
          var base = GROUP_COLORS[n.group] || "#8a8a7a";
          if (n.hub) {
            n.color = { background: base, border: base, highlight: { background: base, border: "#c8862a" } };
            n.shape = "dot";
            n.value = n.value || 52;
            n.label = n.label + " · " + (n.sources || 0) + " sources";
            n.font = { size: 22, face: "Lora, Georgia, serif", color: "#3a3a32", strokeWidth: 5, strokeColor: "#faf8f2" };
            n.borderWidth = 3;
          } else {
            var c = _lighten(base, _depthTier(n.depth || 0));   // pale = thin page, saturated = deep
            n.color = { background: c, border: c, highlight: { background: c, border: "#c8862a" } };
            n.shape = "dot";
            n.value = Math.max(n.degree || 1, 1);               // size = real connection count
            n.font = { size: 13, face: "Inter, sans-serif", color: "#4a4a42" };
            if ((n.degree || 0) <= 1) {                          // orphan: only its spoke to the hub
              n.borderWidth = 1;
              n.shapeProperties = { borderDashes: [2, 3] };
              n.color.border = "#b8b0a0";
            }
          }
        });
```

Then replace the edges mapping (currently lines 36–38) so bridge edges are visually distinct:
```javascript
        var edges = new vis.DataSet(data.edges.map(function (e) {
          var col = e.bridge
            ? { color: "rgba(200,134,42,0.55)", highlight: "#c8862a" }   // cross-domain bridge: warm accent
            : { color: "rgba(120,120,105,0.22)", highlight: "#c8862a" };  // same-domain: faint grey
          return { from: e.from, to: e.to, color: col, width: e.bridge ? 1.2 : 0.6 };
        }));
```

Leave the `new vis.Network(...)` options block (physics/scaling/interaction) unchanged — the
`scaling: { min: 9, max: 52 }` still maps the new `value` (degree) range correctly.

- [ ] **Step 2: Sanity-check the JS parses (no build tool needed)**

Run: `cd ~/Dev/corpus && node --check website/docs/assets/graph.js && echo "JS OK"`
Expected: prints `JS OK` (syntax valid). If `node` is unavailable, skip — Step 3's build catches errors.

- [ ] **Step 3: Local build + eyeball, then screenshot**

Run: `cd ~/Dev/corpus/website && mkdocs build --strict 2>&1 | tail -5`
Expected: builds with no errors; `website/site/assets/graph-data.json` exists and its page nodes
carry `depth`/`degree`, hubs carry `sources`, and some edges carry `bridge`.
Open `website/site/index.html` (or serve with `mkdocs serve`) and confirm by eye: node sizes vary
(orphans tiny, hubs large), thinner pages look paler, hub labels read "domain · N sources",
cross-domain links are warm-colored. Capture a screenshot to attach before merge.

- [ ] **Step 4: Full-suite regression (data builder didn't break anything)**

Run: `cd ~/Dev/corpus && python3 -m pytest tests/ -q -p no:cacheprovider`
Expected: whole suite green (the 4 new `test_corpus_graph.py` tests included).

- [ ] **Step 5: Commit**

```bash
cd ~/Dev/corpus
git add website/docs/assets/graph.js
git commit -m "feat(graph): render size=degree, shade=depth, hub source counts, bridge edges, orphan markers"
```

---

## Self-Review

**1. Spec coverage** (against `docs/superpowers/specs/2026-07-14-truthful-diagnostic-map-design.md`):
- Size = degree → Task 1 (`degree`) + Task 3 (`value = degree`). ✅
- Shade = depth (word count, NOT status) → Task 1 (`depth`) + Task 3 (`_depthTier`/`_lighten`). ✅
- Source-backing on hub labels → Task 2 (`sources`) + Task 3 (label). ✅
- Bridge + orphan highlighting → Task 2 (`bridge`) + Task 3 (edge color + dashed orphan border). ✅
- `corpus_graph.py` gains its first tests → `tests/test_corpus_graph.py` (Tasks 1–2). ✅
- Additive-only / no pipeline change / no content leak (depth is a count) → Global Constraints, honored. ✅
- Testing: builder unit-tested; renderer validated by build + screenshot → Task 3 Steps 2–4. ✅

**2. Placeholder scan:** No TBD/TODO; every code step has complete code; commands have expected output. ✅

**3. Type consistency:** Node fields `depth`/`degree`/`sources` and edge `bridge` are named identically across Tasks 1–2 (producers) and Task 3 (consumer). `_body_wordcount`/`_source_count`/`_TYPE_RE` defined in Task 1–2 before use. `value`/`scaling` untouched so degree maps through the existing 9→52 range. ✅

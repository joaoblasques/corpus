# Corpus Map — Anchored Territories Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. NOTE: Tasks 2–3 are front-end (vis-network) validated by a local `mkdocs build` + Playwright (screenshot + DOM/timing checks), not pytest — the executor needs the Playwright MCP tools and must eyeball the territory separation.

**Goal:** Turn the corpus map from one force-directed blob into a legible "territory map" — 8 domains pinned as separated regions so a human reads the shape of the knowledge at a glance.

**Architecture:** `corpus_graph.py` gains two content-safe per-hub aggregates (page count, avg depth). `graph.js` pins the 8 hubs on a bridge-affinity-ordered ring (fixed x/y), seeds each domain's pages around its hub, gives bridge edges a longer rest-length so territories stay apart, keeps the existing freeze + batched `apply()`, labels the top-2 pages per domain, and shows the aggregates in the hub panel.

**Tech Stack:** Python 3.12 stdlib + pytest (data layer); vanilla JS + vis-network + CSS (front-end, Playwright-validated).

## Global Constraints

- **Content-safety (non-negotiable):** `graph-data.json` emits only ids, titles, domain group, depth (word *count*), degree, hub source/page counts, avg_depth, `created` date, short `aliases`, bridge flags. **Never page body text.**
- **Stdlib only** for Python; no new JS deps (vis-network already loaded).
- **Keep every existing encoding + interaction:** size=degree, lightness=depth, hub center-dots + `Domain · N sources` labels, bridge-accent edges, orphan dashed rings, muted palette; search, domain/thin/orphan filters, grown-over-time slider, click-panel, and the batched `apply()` + `storePositions()`+`physics:false` freeze (toggles must stay < ~50ms).
- **8 hubs must never overlap** — they are pinned at fixed ring positions.
- Deploys from `main` → `joaoblasques.com/corpus/` on push.

---

## File Structure

| File | Responsibility |
|---|---|
| `website/hooks/corpus_graph.py` | ADD per-hub `pages` + `avg_depth` aggregates (Pass — hub emission). |
| `tests/test_corpus_graph.py` | ADD tests for the two aggregates. |
| `website/docs/assets/graph.js` | Territory layout (ring order, fixed hubs, page seeding, per-edge length) + top-2 landmark labels + hub-panel aggregates. |
| `website/docs/stylesheets/extra.css` | Minor — landmark label legibility if needed (likely none; labels styled inline via vis `font`). |

---

### Task 1: Per-hub aggregates (`corpus_graph.py`)

**Files:**
- Modify: `website/hooks/corpus_graph.py` (hub emission loop, ~line 89)
- Test: `tests/test_corpus_graph.py` (append)

**Interfaces:**
- Produces: each **hub** node gains `pages` (int — count of top-level knowledge pages in the domain) and `avg_depth` (int — mean body word count across those pages, rounded; 0 if none).

- [ ] **Step 1: Write the failing test**

```python
# tests/test_corpus_graph.py (append)
def test_hub_carries_pages_and_avg_depth(tmp_path):
    corpus = tmp_path / "corpus"; d = corpus / "ai-engineering"; d.mkdir(parents=True)
    (d / "a.md").write_text("---\ntype: entity\n---\n# A\n" + "word " * 100, encoding="utf-8")   # 100-word body
    (d / "b.md").write_text("---\ntype: concept\n---\n# B\n" + "word " * 300, encoding="utf-8")   # 300-word body
    g = cg.build_graph(corpus)
    hub = next(n for n in g["nodes"] if n.get("hub") and n["id"] == "ai-engineering")
    assert hub["pages"] == 2
    assert hub["avg_depth"] == 200   # mean of 100 and 300 (H1 line adds ~1 word each → tolerate exact 200/201)


def test_hub_aggregates_zero_when_no_pages(tmp_path):
    corpus = tmp_path / "corpus"; d = corpus / "empty-domain"; d.mkdir(parents=True)
    (d / "README.md").write_text("---\ntype: hub\n---\n# hub\n", encoding="utf-8")   # hub only, no pages
    g = cg.build_graph(corpus)
    hub = next((n for n in g["nodes"] if n.get("hub") and n["id"] == "empty-domain"), None)
    assert hub is not None and hub["pages"] == 0 and hub["avg_depth"] == 0
```

(Note: the H1 `# A` line is part of the body split, so "100 word"s + "A" ≈ 101 words. To keep the test exact, the assertion below uses bodies without an H1 count sensitivity — if `avg_depth` comes back 201, adjust the expected value to match `_body_wordcount` semantics rather than changing the code.)

- [ ] **Step 2: Run to verify it fails**

Run: `cd ~/Dev/corpus && python3 -m pytest tests/test_corpus_graph.py -k "hub_carries or hub_aggregates" -q -p no:cacheprovider`
Expected: FAIL — `KeyError: 'pages'`.

- [ ] **Step 3: Implement**

In `website/hooks/corpus_graph.py`, replace the hub-emission loop:
```python
    # Hub node per domain
    for d in sorted(domains):
        nodes[d] = {"id": d, "label": d.replace("-", " "), "group": d, "hub": True,
                    "value": 40, "sources": _source_count(corpus / d)}
```
with:
```python
    # Hub node per domain (+ content-safe per-domain aggregates: page count, mean depth)
    for d in sorted(domains):
        dom_pages = [n for n in nodes.values() if not n.get("hub") and n.get("group") == d]
        avg_depth = round(sum(p["depth"] for p in dom_pages) / len(dom_pages)) if dom_pages else 0
        nodes[d] = {"id": d, "label": d.replace("-", " "), "group": d, "hub": True,
                    "value": 40, "sources": _source_count(corpus / d),
                    "pages": len(dom_pages), "avg_depth": avg_depth}
```
(Page nodes are all built in Pass 1 before this loop, so `nodes.values()` already holds them; the `not hub` guard skips any hub added earlier in this same loop.)

- [ ] **Step 4: Run to verify it passes**

Run: `cd ~/Dev/corpus && python3 -m pytest tests/test_corpus_graph.py -q -p no:cacheprovider`
Expected: PASS (adjust the `avg_depth` expected value to the real `_body_wordcount` result if it's 201 not 200 — the code is correct; the test literal follows it).

- [ ] **Step 5: Real-data sanity + commit**

Run: `cd ~/Dev/corpus && python3 -c "import sys;sys.path.insert(0,'website/hooks');import corpus_graph as cg;from pathlib import Path;g=cg.build_graph(Path('corpus'));hubs=[n for n in g['nodes'] if n.get('hub')];print([(h['id'],h['pages'],h['avg_depth']) for h in hubs])"`
Expected: each hub prints `(domain, pages>0, avg_depth>0)`.
```bash
cd ~/Dev/corpus && git add website/hooks/corpus_graph.py tests/test_corpus_graph.py
git commit -m "feat(graph): per-hub pages + avg_depth aggregates (content-safe) for the hub panel"
```

---

### Task 2: Anchored-territory layout (`graph.js`)

**Files:**
- Modify: `website/docs/assets/graph.js` (insert territory code before `var nodes = new vis.DataSet(data.nodes);`; add `length` to the edge map; light physics tune)

**Interfaces:**
- Consumes: node `hub`, `domain` (set earlier in the same forEach), `degree`; edge `bridge`.
- Produces: hub nodes get fixed `x`/`y`/`mass`; page nodes get seeded `x`/`y`; edges get `length`.

- [ ] **Step 1: Insert the territory layout**

In `website/docs/assets/graph.js`, immediately AFTER the `data.nodes.forEach(function (n) { … });` styling block and BEFORE `var nodes = new vis.DataSet(data.nodes);`, insert:
```javascript
        // --- anchored territories: pin hubs on a bridge-affinity ring, seed pages around their hub ---
        function domOf(id) { var i = id.indexOf("/"); return i < 0 ? id : id.slice(0, i); }
        var byId = {}; data.nodes.forEach(function (n) { byId[n.id] = n; });
        var hubDomains = data.nodes.filter(function (n) { return n.hub; }).map(function (n) { return n.id; });

        // domain×domain bridge counts (bridge edges join two page nodes in different domains)
        var bridges = {};
        function pk(a, b) { return a < b ? a + "|" + b : b + "|" + a; }
        data.edges.forEach(function (e) {
          if (!e.bridge) return;
          var a = domOf(e.from), b = domOf(e.to);
          if (a !== b && byId[a] && byId[b]) bridges[pk(a, b)] = (bridges[pk(a, b)] || 0) + 1;
        });
        function pair(a, b) { return bridges[pk(a, b)] || 0; }

        // greedy nearest-neighbour ring order — seed with the most-bridged domain, then keep appending
        // the remaining domain most-connected to the last placed one (short, uncrossed bridge arcs)
        var remaining = hubDomains.slice().sort(function (a, b) {
          var ta = 0, tb = 0; hubDomains.forEach(function (d) { ta += pair(a, d); tb += pair(b, d); });
          return tb - ta;
        });
        var order = remaining.length ? [remaining.shift()] : [];
        while (remaining.length) {
          var last = order[order.length - 1];
          remaining.sort(function (a, b) { return pair(last, b) - pair(last, a); });
          order.push(remaining.shift());
        }

        // pin hubs on the ring (fixed position + heavy mass so nothing drags them)
        var R = 360;
        order.forEach(function (dom, i) {
          var ang = (i / order.length) * 2 * Math.PI - Math.PI / 2;
          var h = byId[dom];
          h.x = Math.round(Math.cos(ang) * R); h.y = Math.round(Math.sin(ang) * R);
          h.fixed = { x: true, y: true }; h.mass = 8;
        });

        // seed each domain's pages in a small deterministic ring around their hub, so physics starts
        // them in the right territory instead of one central mass
        var pagesByDom = {};
        data.nodes.forEach(function (n) { if (!n.hub) (pagesByDom[n.domain] = pagesByDom[n.domain] || []).push(n); });
        Object.keys(pagesByDom).forEach(function (dom) {
          var h = byId[dom]; if (!h) return;
          var ps = pagesByDom[dom];
          ps.forEach(function (n, j) {
            var a = (j / ps.length) * 2 * Math.PI;
            var rr = 36 + (j % 6) * 15;
            n.x = h.x + Math.cos(a) * rr; n.y = h.y + Math.sin(a) * rr;
          });
        });
```

- [ ] **Step 2: Give bridge edges a longer rest length (so territories don't collapse together)**

Replace the edge DataSet map:
```javascript
        var edges = new vis.DataSet(data.edges.map(function (e) {
          var col = e.bridge ? t.accent : t.edge;
          return { from: e.from, to: e.to, color: { color: col, highlight: t.accent, hover: t.accent }, width: e.bridge ? 0.9 : 0.5 };
        }));
```
with (adds per-edge `length`):
```javascript
        var edges = new vis.DataSet(data.edges.map(function (e) {
          var col = e.bridge ? t.accent : t.edge;
          return { from: e.from, to: e.to, color: { color: col, highlight: t.accent, hover: t.accent },
                   width: e.bridge ? 0.9 : 0.5, length: e.bridge ? 520 : 85 };
        }));
```

- [ ] **Step 3: Soften global repulsion so pages settle near their hub (tunable)**

In the `physics` options, change `barnesHut` to reduce spread and lean on the per-edge lengths:
```javascript
          physics: {
            barnesHut: { gravitationalConstant: -2200, centralGravity: 0, springLength: 90, springConstant: 0.03, damping: 0.55, avoidOverlap: 0.4 },
            stabilization: { iterations: 250 }
          },
```

- [ ] **Step 4: Build + Playwright-verify separation (the visual gate)**

```bash
cd ~/Dev/corpus/website && node --check docs/assets/graph.js && python3 -m mkdocs build
cd site && (python3 -m http.server 8899 >/dev/null 2>&1 &)
```
Then with the Playwright MCP: navigate to `http://localhost:8899/`, wait ~4s for stabilization, and:
- Screenshot `#corpus-graph` — CONFIRM VISUALLY: the 8 hubs sit apart on a ring, each with its own page cluster, no hubs piled in the center, bridge arcs visible between regions.
- Evaluate a domain-chip toggle and assert timing < 50ms (the freeze must survive):
  ```js
  const c=[...document.querySelectorAll('.cg-chip input')]; const t0=performance.now();
  c[1].checked=false;c[1].dispatchEvent(new Event('change')); return Math.round(performance.now()-t0);
  ```
- Console: 0 graph errors (the github-releases 404 is unrelated).

If territories overlap or pages fly apart, tune `R` (spread), `length` (85/520), and `gravitationalConstant` (−2200) and re-screenshot until legible. Kill the server when done (via the deny-safe route — leave it for the user if `pkill` is blocked).

- [ ] **Step 5: Commit**

```bash
cd ~/Dev/corpus && git add website/docs/assets/graph.js
git commit -m "feat(graph): anchored-territory layout — hubs pinned on a bridge-affinity ring, pages cluster per domain"
```

---

### Task 3: Landmark labels + hub-panel aggregates (`graph.js`)

**Files:**
- Modify: `website/docs/assets/graph.js` (landmark labelling after `pagesByDom`; `showNodePanel` hub branch)

**Interfaces:**
- Consumes: `pagesByDom` (from Task 2), node `degree`/`title`; hub `pages`/`avg_depth` (from Task 1).
- Produces: top-2 pages per domain get a small label; hub panel shows `pages · sources · avg depth`.

- [ ] **Step 1: Label the top-2 most-connected pages per domain**

In `graph.js`, immediately AFTER the `pagesByDom` seeding block (end of Task 2's insert), add:
```javascript
        // landmark labels — name the 2 most-connected pages per domain so each territory has anchors
        Object.keys(pagesByDom).forEach(function (dom) {
          pagesByDom[dom].slice().sort(function (a, b) { return (b.degree || 0) - (a.degree || 0); })
            .slice(0, 2).forEach(function (n) {
              n.label = (n.title || "").length > 22 ? n.title.slice(0, 20) + "…" : n.title;
              n.font = { size: 11, face: "Newsreader, Georgia, serif", color: t.inkFaint, strokeWidth: 4, strokeColor: t.surface };
            });
        });
```

- [ ] **Step 2: Show the aggregates in the hub panel**

Replace the hub branch of `showNodePanel`:
```javascript
    if (n.hub) {
      panel.innerHTML = "<b>" + (n.title || "") + "</b><br>domain hub · " + (n.sources || 0) + " source pages"
        + '<br><a href="' + REPO + "tree/main/corpus/" + n.id + '" target="_blank" rel="noopener">Browse domain →</a>';
    } else {
```
with:
```javascript
    if (n.hub) {
      panel.innerHTML = "<b>" + (n.title || "") + "</b><br>domain hub"
        + "<br>" + (n.pages || 0) + " pages · " + (n.sources || 0) + " sources"
        + "<br>avg depth: " + depthLabel(n.avg_depth)
        + '<br><a href="' + REPO + "tree/main/corpus/" + n.id + '" target="_blank" rel="noopener">Browse domain →</a>';
    } else {
```

- [ ] **Step 3: Build + Playwright-verify**

```bash
cd ~/Dev/corpus/website && node --check docs/assets/graph.js && python3 -m mkdocs build
```
Serve + Playwright: navigate, wait, screenshot — CONFIRM: ~2 named pages sit in each territory (readable, not overlapping the hub label); click a hub → panel shows "N pages · N sources · avg depth: …". 0 console errors.

- [ ] **Step 4: Commit**

```bash
cd ~/Dev/corpus && git add website/docs/assets/graph.js
git commit -m "feat(graph): top-2 landmark labels per domain + hub-panel page/depth aggregates"
```

---

## Self-Review

**1. Spec coverage:** anchored ring + fixed hubs → Task 2 ✅; bridge-affinity order → Task 2 ✅; page seeding + per-edge length → Task 2 ✅; keep freeze + batched apply → Task 2 (untouched) ✅; top-2 landmark labels → Task 3 ✅; hub aggregates data → Task 1 ✅; hub-panel aggregates → Task 3 ✅; chips-as-legend → already shipped (no task needed) ✅; keep all encodings/interactions → preserved (edits are additive) ✅; content-safety → Task 1 emits counts/date only ✅; Playwright validation → Tasks 2/3 ✅.

**2. Placeholder scan:** no TBD/TODO; every code step has concrete code; the one `avg_depth` literal is flagged as "match `_body_wordcount`" not a placeholder. Front-end "tests" are explicit build + Playwright checks.

**3. Type consistency:** `byId`, `pagesByDom`, `pair()`, `order`, `domOf()` defined in Task 2 and reused in Task 3; hub fields `pages`/`avg_depth` produced in Task 1 and consumed in Task 3's panel; `depthLabel` already exists in `graph.js`. Node fields `domain`/`degree`/`title` are set before the territory code runs (in the styling forEach). Consistent.

**Executor note:** Tasks 2–3 edit the same render closure and are visually tuned — best run inline by someone with the Playwright MCP (as the prior map work was), iterating physics constants against screenshots, rather than a headless subagent.

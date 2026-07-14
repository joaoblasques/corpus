# Map Interactivity/UX Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the public knowledge graph interactive — click-for-summary, search, filter, and a grown-over-time slider — with no backend and no content leak, AND restore #1's diagnostic encodings that the Archive-theme restyle regressed.

**Architecture:** `corpus_graph.py` emits two content-safe additions per page node (`created`, `aliases`). `graph.js` first restores #1's truthful encodings (size=degree, depth shading, hub source label, bridge edges, orphan border — all dropped by commit `b9b98dd`), then adds a small function-split interaction layer (`showNodePanel`, `search`, `applyFilters`, `timeFilter`) driven by one shared `applyVisibility()` so filters and the slider compose. `extra.css` styles the controls in the Archive theme.

**Tech Stack:** Python 3.12 stdlib (re, json, pathlib) + pytest for the data layer; vanilla JS + vis-network + CSS for the front-end (validated by `mkdocs build` + screenshot, no JS unit tests).

## Global Constraints

- **Content-safety (non-negotiable):** `graph-data.json` carries only id, title, domain group, depth (word *count*), degree, hub source count, `created` date, short `aliases`. **Never page body text.** The click panel shows metadata + a link to the already-published page.
- **Stdlib only** for the Python change; no new JS deps (vis-network already loaded).
- **Keep the Archive theme** — restore #1's *data encodings*, do not revert the visual restyle. Muted warm palette, serif hub labels, thin edges all stay.
- **Additive data contract:** `node(page): {id,label,group,depth,degree,created?,aliases?}`; hubs have no `created` (always visible). Nothing removed from the existing contract.
- **Hubs are the frame:** never hidden by filters or the slider.
- **Build sequencing:** `graph.js`/`extra.css` are edited by a concurrent website-writer; do this on a feature branch when that tree is quiet, and merge carefully.

---

## File Structure

| File | Responsibility |
|---|---|
| `website/hooks/corpus_graph.py` | ADD `_created(text)` + `_aliases(text)` helpers; emit `created` + `aliases` on page nodes (Pass 1). |
| `tests/test_corpus_graph.py` | ADD tests for `created`/`aliases` emission + missing-field handling; keep #1 field tests green. |
| `website/docs/assets/graph.js` | RESTORE #1 encodings; ADD controls container + `showNodePanel`/`search`/`applyFilters`/`timeFilter`/`applyVisibility`. |
| `website/docs/stylesheets/extra.css` | ADD styles for controls panel, chips, summary panel, slider (Archive theme). |

---

### Task 1: Emit `created` + `aliases` (data layer)

**Files:**
- Modify: `website/hooks/corpus_graph.py` (Pass 1 node dict + 2 helpers)
- Test: `tests/test_corpus_graph.py` (append)

**Interfaces:**
- Produces: page node dict gains `created` (ISO string or None) and `aliases` (list[str], `[]` when absent). Helpers `_created(text)->str|None`, `_aliases(text)->list[str]`.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_corpus_graph.py (append)
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
```

- [ ] **Step 2: Run to verify fail**

Run: `cd ~/Dev/corpus && python3 -m pytest tests/test_corpus_graph.py -k "created_and_aliases or without_created" -q -p no:cacheprovider`
Expected: FAIL (KeyError / assertion — fields not emitted).

- [ ] **Step 3: Implement**

In `website/hooks/corpus_graph.py`, add near the other regexes:
```python
_CREATED_RE = re.compile(r"^created:\s*(\S+)", re.M)
_ALIASES_BLOCK_RE = re.compile(r"^aliases:\s*\n((?:[ \t]*-[ \t]*.+\n?)+)", re.M)


def _created(text: str) -> str | None:
    fm = text.split("---", 2)[1] if text.startswith("---") else ""
    m = _CREATED_RE.search(fm)
    return m.group(1).strip().strip('"\'') if m else None


def _aliases(text: str) -> list:
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
```
Then in Pass 1 where the page node dict is built, add the two fields:
```python
        nodes[node_id] = {"id": node_id, "label": _title(text, md.stem), "group": domain,
                          "depth": _body_wordcount(text),
                          "created": _created(text), "aliases": _aliases(text)}
```

- [ ] **Step 4: Run to verify pass**

Run: `cd ~/Dev/corpus && python3 -m pytest tests/test_corpus_graph.py -q -p no:cacheprovider`
Expected: PASS (new + all #1 tests).

- [ ] **Step 5: Real-data sanity + commit**

Run: `cd ~/Dev/corpus && python3 -c "import sys;sys.path.insert(0,'website/hooks');import corpus_graph as cg;from pathlib import Path;g=cg.build_graph(Path('corpus'));ns=[n for n in g['nodes'] if not n.get('hub')];print('pages',len(ns),'with created',sum(1 for n in ns if n.get('created')),'with aliases',sum(1 for n in ns if n.get('aliases')))"`
Expected: most pages have `created`; some have `aliases`.
```bash
cd ~/Dev/corpus && git add website/hooks/corpus_graph.py tests/test_corpus_graph.py
git commit -m "feat(graph): emit per-node created date + aliases (content-safe) for interactivity"
```

---

### Task 2: Restore #1's diagnostic encodings in `graph.js`

**Files:**
- Modify: `website/docs/assets/graph.js` (the `data.nodes.forEach` block + edge map)

**Interfaces:**
- Consumes: node fields `degree`, `depth`, `sources` (hubs), and edge `bridge` — all already emitted by `corpus_graph.py` (#1).
- Produces: nodes sized by degree, shaded by depth, hub labels show source counts, bridge edges colored, orphan nodes get a dashed border. Preserves the Archive theme (palette, serif hub labels, thin edges).

Context: the restyle (`b9b98dd`) hard-coded `n.value = 6` (pages) / `46` (hubs), flat colors, uniform edges, `borderWidth = 0`. Restore the data-driven encodings WITHOUT reverting the theme.

- [ ] **Step 1: Add depth-shading + degree-size helpers**

In `graph.js`, inside the IIFE (near `tokens`), add:
```javascript
  function lighten(hex, frac) {                 // mix hex toward the surface for thin pages
    var s = tokens().surface;
    function rgb(h){ h=h.replace('#',''); return [parseInt(h.slice(0,2),16),parseInt(h.slice(2,4),16),parseInt(h.slice(4,6),16)]; }
    var a = rgb(hex), b = rgb(s);
    var m = a.map(function(v,i){ return Math.round(v + (b[i]-v)*frac); });
    return "rgb(" + m[0] + "," + m[1] + "," + m[2] + ")";
  }
  function depthFrac(depth) {                    // thin => more lightening (paler)
    if (!depth || depth < 300) return 0.55;
    if (depth < 800) return 0.35;
    if (depth < 1800) return 0.15;
    return 0.0;
  }
```

- [ ] **Step 2: Restore data-driven node styling**

Replace the `data.nodes.forEach(function (n) { … })` body with:
```javascript
        data.nodes.forEach(function (n) {
          var base = GROUP_COLORS[n.group] || t.inkFaint;
          n.shape = "dot";
          n.title = n.label;
          if (n.hub) {
            n.value = 46;
            n.label = (n.label || "").replace(/\b\w/g, function (m) { return m.toUpperCase(); })
                      + (n.sources ? "  ·  " + n.sources + " sources" : "");
            n.font = { size: 19, face: "Newsreader, Georgia, serif", color: t.ink, strokeWidth: 6, strokeColor: t.surface };
            n.color = { background: base, border: base, highlight: { background: base, border: t.accent }, hover: { background: base, border: t.accent } };
            n.borderWidth = 0;
          } else {
            n.value = Math.max(n.degree || 1, 1);                 // size = degree (restored)
            var shaded = lighten(base, depthFrac(n.depth));       // lightness = depth (restored)
            n.color = { background: shaded, border: shaded, highlight: { background: shaded, border: t.accent }, hover: { background: shaded, border: t.accent } };
            n.label = undefined;
            if ((n.degree || 0) <= 1) {                           // orphan marker (restored)
              n.borderWidth = 1.5;
              n.shapeProperties = { borderDashes: [2, 2] };
              n.color.border = t.inkFaint;
            } else {
              n.borderWidth = 0;
            }
          }
        });
```

- [ ] **Step 3: Restore bridge edge coloring**

Replace the `edges` DataSet map with:
```javascript
        var edges = new vis.DataSet(data.edges.map(function (e) {
          var col = e.bridge ? t.accent : t.edge;                // cross-domain bridges stand out
          return { from: e.from, to: e.to, color: { color: col, highlight: t.accent, hover: t.accent },
                   width: e.bridge ? 0.9 : 0.5 };
        }));
```
Keep the existing `nodes: { scaling: { min: 6, max: 46 } }` — degree now drives size between those bounds.

- [ ] **Step 4: Build + visually verify**

Run: `cd ~/Dev/corpus/website && mkdocs build 2>&1 | tail -5`
Expected: build succeeds, no errors. Open `site/index.html`, confirm: page dots vary in size (degree), thin pages look paler, hub labels read "Domain · N sources", cross-domain edges are warm-accent, orphans have a faint dashed ring. Take a screenshot.

- [ ] **Step 5: Commit**

```bash
cd ~/Dev/corpus && git add website/docs/assets/graph.js
git commit -m "fix(graph): restore #1 diagnostic encodings regressed by the Archive restyle (size=degree, depth shade, hub sources, bridges, orphans)"
```

---

### Task 3: Click-node summary panel + deep-link

**Files:**
- Modify: `website/docs/assets/graph.js` (controls container + `showNodePanel`, wire `network.on("click")`)
- Modify: `website/docs/stylesheets/extra.css` (panel styles)

**Interfaces:**
- Consumes: node fields `label, group, depth, degree, sources, hub, id`.
- Produces: a `#corpus-graph-panel` overlay; a `showNodePanel(node)` / `hideNodePanel()`.

- [ ] **Step 1: Inject the panel container (once, in `render`, after `el.innerHTML=""`)**

```javascript
    var panel = document.createElement("div");
    panel.id = "corpus-graph-panel";
    panel.style.display = "none";
    el.appendChild(panel);
```

- [ ] **Step 2: Implement `showNodePanel` + depth label**

Inside the IIFE:
```javascript
  function depthLabel(d) { return !d || d < 300 ? "thin" : d < 800 ? "medium" : d < 1800 ? "deep" : "very deep"; }
  function showNodePanel(panel, n) {
    var url = "../" + n.id + "/";                                  // published page: /<domain>/<slug>/
    var rows = n.hub
      ? "<b>" + n.label + "</b><br>domain hub<br>" + (n.sources || 0) + " source pages"
      : "<b>" + (n.title || n.label) + "</b><br>" + n.group +
        "<br>depth: " + depthLabel(n.depth) + " (" + (n.depth || 0) + " words)" +
        "<br>connections: " + (n.degree || 0) +
        '<br><a href="' + url + '">Open page →</a>';
    panel.innerHTML = rows;
    panel.style.display = "block";
  }
```
(Note: `n.title` holds the original label — the renderer sets `n.title = n.label` before clearing page labels. For hubs use `n.label`.)

- [ ] **Step 3: Wire the click handler (after `network` is created)**

```javascript
        network.on("click", function (params) {
          if (params.nodes.length) {
            var n = nodes.get(params.nodes[0]);
            showNodePanel(panel, n);
          } else {
            panel.style.display = "none";
          }
        });
```

- [ ] **Step 4: Style the panel (extra.css)**

```css
#corpus-graph { position: relative; }
#corpus-graph-panel {
  position: absolute; top: .6rem; right: .6rem; max-width: 15rem; z-index: 5;
  background: var(--md-default-bg-color); border: 1px solid rgba(120,112,96,.35);
  border-radius: .3rem; padding: .6rem .7rem; font-size: .74rem; line-height: 1.5;
  box-shadow: 0 2px 10px rgba(0,0,0,.12);
}
#corpus-graph-panel a { color: #a9762a; font-weight: 600; }
```

- [ ] **Step 5: Build, verify click shows panel + working link, screenshot, commit**

Run: `cd ~/Dev/corpus/website && mkdocs build 2>&1 | tail -3`. Open built site, click a node, confirm panel + that "Open page →" navigates to the page.
```bash
cd ~/Dev/corpus && git add website/docs/assets/graph.js website/docs/stylesheets/extra.css
git commit -m "feat(graph): click-node summary panel with deep-link to the page"
```

---

### Task 4: Search by label + alias

**Files:**
- Modify: `website/docs/assets/graph.js` (controls + `search`)
- Modify: `website/docs/stylesheets/extra.css` (search input)

**Interfaces:**
- Consumes: node `label`/`title` + `aliases`. Produces: a search input that emphasizes matches, dims non-matches; shares the `nodes` DataSet.

- [ ] **Step 1: Add a controls bar container (in `render`, after the panel)**

```javascript
    var controls = document.createElement("div");
    controls.id = "corpus-graph-controls";
    el.appendChild(controls);
    var searchBox = document.createElement("input");
    searchBox.type = "search"; searchBox.placeholder = "search…";
    searchBox.id = "corpus-graph-search";
    controls.appendChild(searchBox);
```

- [ ] **Step 2: Implement `search` (dim non-matches via node opacity)**

```javascript
  function nodeMatches(n, q) {
    if (!q) return true;
    q = q.toLowerCase();
    var hay = [(n.title || n.label || "")].concat(n.aliases || []).join(" ").toLowerCase();
    return hay.indexOf(q) !== -1;
  }
```
Wire (after `network` + `nodes` exist):
```javascript
        searchBox.addEventListener("input", function () {
          var q = searchBox.value.trim();
          nodes.forEach(function (n) {
            var on = n.hub || nodeMatches(n, q);
            nodes.update({ id: n.id, opacity: q ? (on ? 1 : 0.12) : 1 });
          });
        });
```

- [ ] **Step 3: Style (extra.css)**

```css
#corpus-graph-controls { position: absolute; top: .6rem; left: .6rem; z-index: 5; display: flex; flex-wrap: wrap; gap: .35rem; align-items: center; }
#corpus-graph-search { font-size: .74rem; padding: .25rem .5rem; border: 1px solid rgba(120,112,96,.35); border-radius: .3rem; background: var(--md-default-bg-color); color: var(--md-default-fg-color); }
```

- [ ] **Step 4: Build, verify typing a name/alias emphasizes matches, screenshot, commit**

```bash
cd ~/Dev/corpus && git add website/docs/assets/graph.js website/docs/stylesheets/extra.css
git commit -m "feat(graph): search nodes by title + alias (dim non-matches)"
```

---

### Task 5: Filters (domain / depth / orphan) + shared `applyVisibility`

**Files:**
- Modify: `website/docs/assets/graph.js` (filter controls, `applyFilters`, `applyVisibility`)
- Modify: `website/docs/stylesheets/extra.css` (chips)

**Interfaces:**
- Produces: `applyVisibility()` — the single source of truth that sets each node's `hidden` from (domain filters ∧ depth filter ∧ orphan toggle ∧ time cutoff). Filters call it. Hubs never hidden.

- [ ] **Step 1: Add filter state + controls**

```javascript
    var state = { domains: {}, thinOnly: false, orphanOnly: false, cutoff: null };
    // domain chips
    var domains = Array.from(new Set(data.nodes.filter(function(n){return !n.hub;}).map(function(n){return n.group;}))).sort();
    domains.forEach(function (dm) {
      state.domains[dm] = true;
      var chip = document.createElement("label"); chip.className = "cg-chip";
      chip.style.borderColor = GROUP_COLORS[dm] || "#999";
      var cb = document.createElement("input"); cb.type = "checkbox"; cb.checked = true;
      cb.addEventListener("change", function () { state.domains[dm] = cb.checked; applyVisibility(); });
      chip.appendChild(cb); chip.appendChild(document.createTextNode(dm));
      controls.appendChild(chip);
    });
    // thin-only + orphan-only toggles
    ["thinOnly", "orphanOnly"].forEach(function (key) {
      var lab = document.createElement("label"); lab.className = "cg-chip";
      var cb = document.createElement("input"); cb.type = "checkbox";
      cb.addEventListener("change", function () { state[key] = cb.checked; applyVisibility(); });
      lab.appendChild(cb); lab.appendChild(document.createTextNode(key === "thinOnly" ? "thin only" : "orphans"));
      controls.appendChild(lab);
    });
```

- [ ] **Step 2: Implement `applyVisibility` (the composition point)**

```javascript
    function applyVisibility() {
      nodes.forEach(function (n) {
        if (n.hub) { nodes.update({ id: n.id, hidden: false }); return; }
        var show = state.domains[n.group] !== false;
        if (state.thinOnly && (n.depth || 0) >= 300) show = false;
        if (state.orphanOnly && (n.degree || 0) > 1) show = false;
        if (state.cutoff && n.created && n.created > state.cutoff) show = false;
        nodes.update({ id: n.id, hidden: !show });
      });
    }
```
(`applyVisibility` is defined inside the `.then` where `nodes`/`state` live; the earlier task callbacks reference it.)

- [ ] **Step 3: Build, verify each filter hides the right nodes + they compose, screenshot, commit**

```bash
cd ~/Dev/corpus && git add website/docs/assets/graph.js website/docs/stylesheets/extra.css
git commit -m "feat(graph): domain/depth/orphan filters via shared applyVisibility"
```

Style (extra.css):
```css
.cg-chip { font-size: .68rem; padding: .12rem .4rem; border: 1px solid #999; border-radius: 1rem; background: var(--md-default-bg-color); display: inline-flex; gap: .25rem; align-items: center; cursor: pointer; }
.cg-chip input { margin: 0; }
```

---

### Task 6: Grown-over-time slider

**Files:**
- Modify: `website/docs/assets/graph.js` (slider + play, feeds `state.cutoff` → `applyVisibility`)
- Modify: `website/docs/stylesheets/extra.css` (slider row)

**Interfaces:**
- Consumes: node `created`. Produces: a date range slider that sets `state.cutoff` and calls `applyVisibility()`; a play button that auto-advances. Nodes without `created` and hubs always visible.

- [ ] **Step 1: Build the slider from the created-date range**

```javascript
    var dates = data.nodes.filter(function(n){return n.created;}).map(function(n){return n.created;}).sort();
    if (dates.length) {
      var minD = dates[0], maxD = dates[dates.length - 1];
      var row = document.createElement("div"); row.id = "corpus-graph-time";
      var slider = document.createElement("input");
      slider.type = "range"; slider.min = 0; slider.max = dates.length - 1; slider.value = dates.length - 1;
      var lbl = document.createElement("span"); lbl.textContent = maxD;
      var play = document.createElement("button"); play.textContent = "▶"; play.type = "button";
      slider.addEventListener("input", function () {
        state.cutoff = dates[+slider.value]; lbl.textContent = state.cutoff; applyVisibility();
      });
      var timer = null;
      play.addEventListener("click", function () {
        if (timer) { clearInterval(timer); timer = null; play.textContent = "▶"; return; }
        play.textContent = "⏸"; if (+slider.value >= +slider.max) slider.value = 0;
        timer = setInterval(function () {
          if (+slider.value >= +slider.max) { clearInterval(timer); timer = null; play.textContent = "▶"; return; }
          slider.value = +slider.value + 1; slider.dispatchEvent(new Event("input"));
        }, 180);
      });
      row.appendChild(play); row.appendChild(slider); row.appendChild(lbl);
      controls.appendChild(row);
    }
```

- [ ] **Step 2: Style (extra.css)**

```css
#corpus-graph-time { display: flex; gap: .4rem; align-items: center; width: 100%; margin-top: .3rem; font-size: .68rem; }
#corpus-graph-time input[type=range] { flex: 1; }
#corpus-graph-time button { border: 1px solid rgba(120,112,96,.4); border-radius: .25rem; background: var(--md-default-bg-color); cursor: pointer; padding: 0 .4rem; }
```

- [ ] **Step 3: Build, verify dragging hides newer nodes + play animates growth + composes with filters, screenshot, commit**

```bash
cd ~/Dev/corpus && git add website/docs/assets/graph.js website/docs/stylesheets/extra.css
git commit -m "feat(graph): grown-over-time slider (created-date derived) + play"
```

---

## Self-Review

**1. Spec coverage:** data `created`+`aliases` → Task 1 ✅; restore #1 (spec Non-goal "restore regressions") → Task 2 ✅; click panel+deep-link → Task 3 ✅; search label+alias → Task 4 ✅; domain/depth/orphan filters → Task 5 ✅; time slider → Task 6 ✅; content-safety (metadata only) → Tasks 1/3 ✅; `applyVisibility` composition → Task 5 ✅.

**2. Placeholder scan:** no TBD/TODO; every code step has concrete code; each front-end task ends with build + screenshot + commit.

**3. Type consistency:** `state` shape (`domains/thinOnly/orphanOnly/cutoff`) consistent Tasks 5–6; `applyVisibility` defined in Task 5, referenced by Task 6's slider and (opacity, separate) Task 4's search; node fields `created`/`aliases`/`degree`/`depth`/`sources`/`bridge` all emitted by Task 1 or #1. Panel URL `../<domain>/<slug>/` matches the published docs layout.

**Note for the executor:** Tasks 3–6 all edit the same `.then(function(data){…})` closure in `graph.js`; keep `panel`, `controls`, `state`, `nodes`, `network`, and `applyVisibility` in that scope. Because these are front-end (no unit tests), the review gate per task is the `mkdocs build` success + screenshot, not pytest. Run the whole build after Task 6 and confirm no console errors.

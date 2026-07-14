# Map Interactivity/UX — design spec (2026-07-14)

> Status: **proposed, for review.** Sub-project #3 of the "improve the graph and/or corpus" effort
> (#1 = truthful diagnostic map, shipped; #2 = diagnostic-driven deepen-existing, shipped + wired).
> Turns the now-truthful static map into an explorable one: click, search, filter, and watch it grow.

## Goal

Make the public knowledge graph **interactive** without adding a backend or leaking page content:
click a node for a metadata summary + link to its page; search by name/alias; filter by domain,
depth, and orphan status; and drag a time slider to watch the corpus grow. All four ride the
existing static build (`graph-data.json` emitted from `corpus/` at every build) and stay
content-safe — only titles, domains, dates, aliases, and structure ever leave `corpus/`.

## Grounding (measured 2026-07-14)

- `created:` frontmatter is present on **375/374** top-level knowledge pages (universal) → the time
  slider can derive "when a node appeared" from `created:` with no new pipeline.
- `graph.js` is currently **85 lines** (rewritten by a parallel "Archive theme" restyle, commit
  `b9b98dd`). #3 builds on that current version. **Open risk to verify at build time:** the restyle
  may have dropped #1's visual encodings (size=degree, depth shading, bridge-edge color, orphan
  dashed border). #3 must confirm they survived and restore any that regressed (see Non-goals).
- Graph: 8 domain hubs + ~370 page nodes, ~1,843 edges. Source pages remain non-nodes.

## Data layer — `website/hooks/corpus_graph.py` (2 content-safe additions)

Pure additions to the Pass-1 page-node dict; nothing else changes, no body text emitted:

- **`created`** — the page's `created:` frontmatter value (ISO date string, e.g. `2026-06-17`).
  Omitted when absent (front-end treats a missing `created` as "always present"). Powers the slider.
- **`aliases`** — the page's `aliases:` list (short alternate names, already in frontmatter), so
  search matches "GPT-4"/"o4-mini" → the `openai` node. Emitted as a list of short strings; `[]`
  when absent. These are labels, not content — leak-safe.

Contract additions (everything else unchanged from #1):
```
node (page): {id, label, group, depth, degree, created?, aliases?}
node (hub):  {id, label, group, hub: true, value, sources, degree}   # no `created` → always visible
edge: {from, to, bridge?}
```
Parsing: reuse the existing frontmatter read in Pass 1 (the file is already read for the title).
Add small helpers `_created(text) -> str|None` and `_aliases(text) -> list[str]` (regex on the
frontmatter block, same style as the existing `_TYPE_RE`). Tested in `tests/test_corpus_graph.py`.

## Front-end — `website/docs/assets/graph.js` (4 interactions)

A small control layer, function-split for isolation. `graph.js` injects a controls container (or a
minimal `<div id="corpus-graph-controls">` added to the Home template) and styles it via
`extra.css`. All interaction is client-side on the vis-network already built.

### 1. Click node → summary panel (`showNodePanel`)
On `network.on("click", …)`: if a node is hit, show a small overlay panel with — title, domain,
**depth** (word-count tier label, e.g. "deep / medium / thin"), **degree** (N connections), and for
hubs the **source count**; plus an **"Open page →"** link deep-linking to that page's published
docs URL (`/<domain>/<slug>/`). Clicking empty canvas hides the panel. Content-safe: metadata +
a link to an already-public page (no body text in the graph payload).

### 2. Search (`search`)
A text input. On input, case-insensitive substring match over each node's `label` + `aliases`.
Matching nodes are emphasized (selected/focused via `network.selectNodes` + `focus`), non-matching
nodes dimmed (lowered opacity). Enter cycles through matches. Empty input restores full opacity.

### 3. Filters (`applyFilters`, compose with AND)
- **Domain toggles** — one colored chip per domain; unchecking hides that domain's page nodes (and
  their incident edges).
- **Depth filter** — reuse #1's depth tiers; a control to show "thin pages only" ↔ "all" (spotlights
  the weak spots the map exists to reveal).
- **Orphan toggle** — show only `degree === 1` nodes (disconnected knowledge).
Implemented by setting a `hidden` flag on the vis `DataSet` (update, not rebuild), so filters and
the slider compose. Hubs are never hidden by filters (they are the frame).

### 4. Grown-over-time slider (`timeFilter`)
A range slider from the earliest node `created` to today. Dragging sets a cutoff date; nodes with
`created > cutoff` get `hidden: true`; an edge hides when either endpoint is hidden. A small **play**
button auto-advances the cutoff (setInterval, simple) to animate growth; pause stops it. A label
shows the current cutoff date + count of visible nodes. Nodes lacking `created` and all hubs stay
visible at every position. Composes with the filters (a node is shown only if it passes filters AND
the time cutoff).

## Architecture / isolation

- `corpus_graph.py`: additive, pure, testable — the only Python change.
- `graph.js`: keep the restyle's theme; add the control layer as small named functions
  (`buildControls`, `showNodePanel`, `search`, `applyFilters`, `timeFilter`) so each interaction is
  understandable and editable in isolation. A single shared `applyVisibility()` recomputes each
  node's `hidden` from (filters ∧ time) to avoid the interactions fighting each other.
- `extra.css`: styles for the controls container, panel, chips, slider — matching the Archive theme.
- Optional minimal template hook: a `<div id="corpus-graph-controls">` beside `#corpus-graph` on the
  Home page if injecting via JS proves awkward.

## Data flow & rollout

Unchanged: `on_pre_build` regenerates `graph-data.json` from `corpus/` every build; docs CI rebuilds
+ redeploys on every push to main; the nightly pushes. Enriched data + new JS appear on the next
build, and stay current as the corpus grows — no new machinery.

## Testing

- **`tests/test_corpus_graph.py`** (extend): (1) `created` equals the frontmatter `created:` value;
  (2) a page with no `created:` omits the field (or emits null) and does not crash; (3) `aliases`
  equals the frontmatter list, `[]` when absent; (4) existing #1 field tests still pass (regression
  guard that the additions didn't disturb depth/degree/sources/bridge).
- **`graph.js`**: front-end — validate with a local `cd website && mkdocs build`, open the built
  graph, exercise each of the 4 interactions, and attach a screenshot before shipping (as in #1).

## Content-safety (non-negotiable)

`graph-data.json` after #3 contains only: node id, title, domain group, depth (word *count*, not
text), degree, source count, `created` date, and short `aliases`. **No page body text.** The click
panel shows this metadata and links to the already-published page. This preserves #1's guarantee
that the public graph leaks no knowledge text.

## Non-goals

- **No snapshot pipeline** — the slider derives from `created:` dates, not git history.
- **No backend / server** — pure static site + client JS.
- **No change to what counts as a node/edge** — only new node attributes + the interaction layer.
- **Not a restyle** — keep the current Archive theme; #3 only *verifies* #1's diagnostic encodings
  survived the restyle and restores any that regressed (in scope precisely because #3 edits the same
  file and a diagnostic map with dead encodings would undercut the interactions built on them).

## Build sequencing (operational)

The design/spec/plan are safe to write anytime. The **build edits `graph.js`/`extra.css`, which the
concurrent website-writer (the nightly/parallel actor behind `b9b98dd`) also touches** — so the
build should run when that tree is quiet, on a feature branch, to avoid clobbering. This is a
scheduling note, not a design constraint.

## Success criteria

- `graph-data.json` carries `created` + `aliases` per page node; the whole test suite stays green;
  content-safety preserved (no body text).
- On the built site: clicking a node shows its metadata + working "Open page" link; search
  emphasizes matches by name/alias; domain/depth/orphan filters compose; the slider animates the
  corpus's growth by `created` date; #1's diagnostic encodings are intact.
- No regression to the deploy pipeline; the map still regenerates on every build.

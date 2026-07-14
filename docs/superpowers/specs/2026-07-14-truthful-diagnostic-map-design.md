# Truthful Diagnostic Map — design spec (2026-07-14)

> Status: **proposed, for review.** Sub-project #1 of a 3-part "improve the graph and/or corpus"
> effort (this = a truthful diagnostic map; #2 = diagnostic-driven knowledge improvement; #3 =
> map interactivity/UX — both deferred to their own specs).

## Goal

Turn the public knowledge graph from a decorative picture into a **truthful, self-diagnosing map**:
every visual channel (node size, lightness, hub label, edge color) carries real signal about the
corpus's shape, so a glance reveals where knowledge is well-connected vs isolated, deep vs thin,
and where domains actually bridge. Enrich the EXISTING public map in place — richer signal reads
as a feature, weak spots are visible to a careful eye but never labelled "shallow."

## Grounding (measured 2026-07-14)

- Graph: 378 nodes (8 domain hubs + 370 top-level knowledge pages; source pages are intentionally
  not nodes), ~1,843 edges. Corpus: 372 knowledge pages : 1,071 source pages (depth ratio 1:2.9,
  up from 1:6.6 — the book pipeline is deepening it).
- **The `status:` field is useless as a maturity signal**: 362/372 knowledge pages are `draft`,
  8 `stub`, 2 `mature` (nobody maintains it). **Word count is a real depth signal**: median 907,
  range 131–14,688, only 0% thin (<150w). → shade by **depth (word count)**, not `status`.

## Non-goals

- No separate private view; no interactivity (click/search/filter/time-slider) — that's sub-project #3.
- Source pages are NOT added as nodes (would add 1,071 dots + leak content); they're surfaced only
  as an aggregate count on hub labels.
- No change to the graph's data pipeline or deploy path (already rebuilds on every push to main).
- No change to what counts as a node/edge — only NEW attributes on existing nodes/edges + renderer.

## The six visual channels

| Channel | Today | New (truthful) |
|---|---|---|
| Node **size** | binary hub(52)/page(9) | **connection count (degree)**, scaled; orphans → tiny, hubs stay large (naturally high-degree) |
| Node **hue** | domain group color | unchanged (domain) |
| Node **lightness** | flat | **page depth** (word count, bucketed) — pale = thin, saturated = deep |
| **Hub label** | domain name | `domain name · N sources` (surfaces the ~1,071 hidden source pages as an aggregate) |
| **Edge color** | all faint grey | **cross-domain "bridge" edges in a distinct color**; same-domain edges stay grey |
| **Orphans** | invisible | emerge as tiny dots (degree 1 = spoke-only) + a subtle marker (faint dashed border) |

## Architecture — 2 files

### 1. `website/hooks/corpus_graph.py` (data builder, pure Python — the testable core)
Extend `build_graph(corpus_dir) -> dict` to compute and emit new attributes. No change to which
nodes/edges exist; only additions:
- **Per page node:** `depth` = word count of the page body (frontmatter stripped). Computed in
  Pass 1 (the read already happens there for the title).
- **Per node (after edges built, new Pass 3):** `degree` = number of edges incident to the node
  (hubs and pages alike). Orphan pages are those with `degree == 1`.
- **Per hub node:** `sources` = count of `type: source` pages under `corpus/<domain>/` (rglob;
  the sources live in `<domain>/sources/`). Emitted on the hub node only.
- **Per edge:** `bridge: true` when the two endpoints are page nodes in DIFFERENT domains
  (domain = node-id prefix before `/`). Spoke edges (page↔hub) are never bridges.

Contract additions (everything else unchanged):
```
node (page): {id, label, group, depth}
node (hub):  {id, label, group, hub: true, value, sources}
node (any, added): degree
edge: {from, to, bridge?}   # bridge present+true only for cross-domain page-to-page edges
```
This file currently has **no tests** — this sub-project adds `tests/test_corpus_graph.py`.

### 2. `website/docs/assets/graph.js` (renderer, front-end — validated by eye)
Map the new attributes to vis-network visuals:
- **Size:** set each node's `value = degree` (with a small floor, e.g. `max(degree, 1)`, so
  orphans remain clickable dots). Keep the existing `nodes.scaling.min/max` (currently 9→52) so
  hubs stay largest and pages scale between. Remove the hard-coded `value: 52` / `value: 9` binary.
- **Lightness (depth):** bucket `depth` into ~4 tiers (e.g. <300, <800, <1800, ≥1800 words) and
  lighten the domain's `GROUP_COLORS[group]` toward the page background for thinner pages (mix
  fraction per tier). Hubs keep full saturation.
- **Hub label:** `n.label + " · " + n.sources + " sources"` when `n.hub`.
- **Bridge edges:** if `e.bridge`, use a distinct edge color (e.g. a translucent accent that reads
  as a "connection between fields") instead of the default grey; keep the highlight color.
- **Orphan marker:** for a page node with `degree === 1`, add a faint dashed border.

## Data flow & rollout

Unchanged: `on_pre_build` regenerates `docs/assets/graph-data.json` from `corpus/` at every build;
the docs CI (`.github/workflows/docs.yml`) rebuilds + redeploys on every push to main; the nightly
pushes nightly. So once merged, the enriched map appears on the next build — no new machinery, and
it stays current automatically as the corpus grows.

## Testing

- **`tests/test_corpus_graph.py`** (new): against a tiny fixture corpus —
  1. `depth` equals the body word count (frontmatter excluded);
  2. `degree` counts incident edges (a page linked to its hub + one other page has degree 2);
  3. hub `sources` counts `type: source` pages in that domain (incl. `sources/` subdir), excludes
     knowledge pages;
  4. an edge between two different-domain page nodes has `bridge: true`; a same-domain edge and a
     spoke edge do not;
  5. an orphan page (only its spoke edge) has `degree == 1`.
- **`graph.js`**: no unit test (front-end). Validate with a local `cd website && mkdocs build`,
  open the built graph, and attach a screenshot to the PR/branch before shipping.

## Open decisions (minor — sensible defaults chosen, tune in review)

- **Depth buckets:** default `<300 / <800 / <1800 / ≥1800` words → 4 lightness tiers. Tunable.
- **Bridge edge color:** default a translucent warm accent (matches the existing highlight
  `#c8862a` family) so bridges read as "links between fields." Tunable in review.
- **Degree scaling:** reuse the existing `scaling.min/max` (9→52); if hubs end up too dominant we
  can dampen with a sqrt on degree. Decide by eye on the local build.

## Success criteria

- Every node's size reflects its real degree; orphans are visibly tiny, well-connected pages
  visibly larger — verifiable from `graph-data.json` (`value == degree`).
- Thin vs deep pages are distinguishable by lightness; hub labels show source counts; cross-domain
  bridges are visually distinct from intra-domain links.
- `corpus_graph.py` has tests for all four new fields (depth, degree, sources, bridge); the whole
  test suite stays green; the built map renders without console errors.
- No regression to the deploy pipeline; the map still regenerates on every build.

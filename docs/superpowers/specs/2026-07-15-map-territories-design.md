# Corpus Map — Anchored Territories (readability) design spec (2026-07-15)

> Status: **proposed, for review.** Follow-on to the map interactivity work. Turns the single
> force-directed blob into a legible "territory map" so a human can read the *shape of the
> knowledge* at a glance — which domains are big/deep, how they bridge, where the gaps are.

## Goal

The map's job (chosen with the user) is **"shape of the knowledge"**: read structure at a glance —
domain sizes, inter-domain connections, orphans/gaps, growth. The current layout defeats this: one
force-directed blob pulls all 8 domain hubs into the center where they overlap and the structure is
an indistinct mass. Fix = give each domain its own spatial **territory**.

## The core: anchored territories

- **Pin the 8 domain hubs at fixed, evenly-spaced positions on a large ring** (`x`/`y` set,
  `fixed:{x:true,y:true}`, higher `mass`). Fixed hubs can never overlap or drift into the center.
- **Each domain's pages cluster around their own hub.** Seed each page's initial position at its
  hub's position + small jitter, then run the existing physics pass with two tweaks:
  - intra-domain edges keep a short rest length (pages pull toward their region);
  - **cross-domain (bridge) edges get a longer rest length** (per-edge `length`) so bridges draw
    the connection without yanking territories back into a blob.
  Then freeze as today (`storePositions()` + `physics:false`) so it's stable and interaction is instant.
- **Ring order minimizes bridge crossings**: order the 8 hubs around the ring so the most-bridged
  domain pairs sit adjacent (greedy nearest-neighbour over the domain×domain bridge-count matrix).
  Deterministic per build. Bigger domains may get proportionally more arc spacing.
- *Chosen over* a fully deterministic spiral placement: light physics keeps the meaningful
  intra-domain clustering (which pages clump together), which a spiral would flatten.

Result: 8 clearly separated regions, each visibly sized by its page count, with bridge arcs between
them and orphans as dashed nodes at the edges.

## Legibility aids

- **Chips = legend.** The existing filter chips are already colored + labeled + always visible, so
  they double as the domain color legend. No separate legend element.
- **Landmark labels.** Label the **top ~2 most-connected pages per domain** (small serif label) so
  each territory has recognizable anchors instead of only anonymous dots. Everything else stays
  title-on-hover + the click-panel. Tunable count.
- **Keep** every diagnostic encoding already shipped: size = degree, lightness = depth, hub
  center-dot + `Domain · N sources` label, bridge-accent edges, orphan dashed rings, muted palette,
  and all interactivity (search, domain/thin/orphan filters, grown-over-time slider, click-panel).

## Data / encoding

No new page-level data. Two optional additions to `website/hooks/corpus_graph.py`, emitted on the
**hub node only** (still content-safe — counts + a date, never page text), to enrich the hub
click-panel ("Ai-Engineering — 47 pages · avg depth 'deep' · 181 sources"):

- `pages`: count of top-level knowledge pages in the domain.
- `avg_depth`: mean body word count across the domain's pages (a depth signal, not text).

Contract (hub node gains): `{…, pages, avg_depth}`. Everything else unchanged.

## Architecture / surface

- **`website/docs/assets/graph.js`** (most of the work): compute ring positions for hubs + fix them;
  seed page start positions per domain; set per-edge `length` (short intra-domain, long bridge);
  compute the bridge-affinity ring order; pick + label top-N pages per domain; hub click-panel shows
  the new aggregates. All within the existing render closure; keep the batched `apply()` + freeze.
- **`website/hooks/corpus_graph.py`**: add `pages` + `avg_depth` on hub nodes (small helpers, unit-
  tested).
- **`website/docs/stylesheets/extra.css`**: minor — landmark-label styling if needed.
- Deploys from `main` → `joaoblasques.com/corpus/` on push, as now.

## Testing

- **`tests/test_corpus_graph.py`**: hub `pages` = count of that domain's knowledge pages; `avg_depth`
  = mean body word count (frontmatter excluded); pages with no body handled; existing field tests
  stay green.
- **`graph.js`** (front-end, no unit test): Playwright verification on a local build — 8 hubs at
  distinct non-overlapping ring positions, each domain's pages in its own region, bridge arcs between
  regions, top-N labels present, filters/search/slider still work and stay fast (< ~50ms toggle),
  no console errors. Screenshot attached before shipping.

## Non-goals

- No collapse-to-domains / drill-down (considered, deferred — territories keep all pages visible).
- No new node/edge semantics; no page-body text ever emitted.
- No change to the deploy pipeline or the data-refresh cadence.

## Success criteria

- The 8 domains render as visually distinct, non-overlapping territories; hubs never pile into the
  center; a first-time viewer can point to "that's the big domain / these two are tightly linked /
  that domain is isolated."
- Filtering/search/slider remain instant (batched updates + frozen layout).
- Content-safety preserved; whole test suite green; map regenerates on every build.

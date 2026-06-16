---
type: concept
domain: software-engineering
status: draft
sources:
  - path: raw/web/how-s-linear-so-fast-a-technical-breakdown.md
    channel: web
    ingested_at: 2026-06-16
aliases:
  - local-first architecture
  - local-first sync
  - sync engine
  - browser-as-database
  - optimistic UI
  - Linear architecture
  - how Linear is so fast
  - client-side rendering performance
tags:
  - corpus/software-engineering
  - concept
created: 2026-06-16
updated: 2026-06-16
---

# Local-First Sync Architecture

**TL;DR.** A web-app architecture where the client holds the canonical working copy of data (in-browser IndexedDB + in-memory store), mutations apply locally and synchronously first, and the server is a *sync target* rather than the UI's source of truth. Reconciliation happens asynchronously in the background. Reverse-engineered from Linear, where this approach makes an issue update take a few milliseconds versus ~300ms for a traditional CRUD app [^src1]. The speed is a system property — local database, optimistic writes, and granular reactivity each fail to deliver speed without the other two [^src1].

## The core inversion

A traditional web app loops: user clicks → browser fires HTTP request → server queries DB → returns → browser repaints, leaving a spinner or skeleton for a few hundred ms [^src1]. Local-first inverts this: the database the UI reads from lives in the browser (IndexedDB); mutations apply locally first, then push to the server asynchronously, which broadcasts deltas back to other clients via WebSocket [^src1].

> "the secret to building incredible web apps is by hiding all the network requests from the user" [^src1]

The guiding principle: UI responsiveness should not depend on network latency, because users perceive speed by how fast the interface reacts, not how fast the server responds [^src1].

## The three pillars of the sync engine

Linear's speed lives downstream of treating the server as a sync target, not a source of truth for the UI [^src1]. Three pillars, which only produce speed *together* [^src1]:

1. **The data is already there.** On boot the app hydrates from IndexedDB into an in-memory MobX object pool; every UI query hits the pool first, so there is no "loading issues" state [^src1]. The two heaviest tables (Issue, Comment) lazy-hydrate on demand — *data-level code splitting* — so a 10,000-issue workspace boots about as fast as a 100-issue one [^src1].
2. **Mutations don't wait for the network.** Changing a status updates the MobX observable (UI reflects it), writes to a durable transaction queue in IndexedDB, and queues for the server — all before the network is touched; if the server rejects, the observable reverts with a brief flicker, which rarely happens [^src1].
3. **One delta, one cell.** A confirmed mutation returns as a small JSON envelope; because every model property is its own observable and every reader is wrapped in `observer()`, a one-field change re-renders exactly the components reading that field. "A 50-issue update is 50 cell re-renders, not a list re-render." [^src1]

Take any pillar away and the app feels slow: a local DB without optimistic writes still spins on save; optimistic writes without granular observables still jank on every update; granular observables without a local DB still wait on initial load [^src1].

## Optimistic mutation as the accessible version

Most teams won't build a custom sync engine and don't need to: libraries like TanStack Query and SWR get close with optimistic updates [^src1]. The high-leverage pattern is to eliminate spinners, update state immediately, validate in the background, and roll back only if needed [^src1]. Linear's co-founder Tuomas wrote the sync engine as literally the first lines of code — uncommon for a startup — committing to the tradeoffs from day one [^src1].

## Making first load feel instant (client-side rendering)

Linear ships a client-side-rendered app — React, TypeScript, MobX, Postgres, a CDN; no edge database, no React Server Components, no exotic framework [^src1]. The build pipeline was rewritten four times (Parcel → Rollup → Vite → Rolldown), each migration cutting JS/CSS shipped and improving DX; claimed results include 50% less code shipped, ~30% smaller after compression, and time-to-first-paint of the active-issues view dropping 59% on Safari [^src1]. The biggest win was dropping legacy-browser support (no polyfills, no ES5 transpilation), with dead-code elimination and aggressive chunking close behind [^src1].

Key loader techniques, all aimed at making network requests fast or eliminating them [^src1]:

- **Per-package vendor chunking** — one chunk per npm package, so bumping one dependency invalidates one chunk rather than the whole `vendor.js` [^src1].
- **`modulepreload`** — the `<head>` lists critical chunks so the browser fires them in parallel before the entry script parses, collapsing the import waterfall into one parallel batch; `crossorigin` on each preload must match the entry script so the browser reuses the cached fetch [^src1].
- **Service worker precache** — a manifest of ~1,200 hashed assets is pulled lazily after first load, so later navigations skip the network entirely and the app works offline (combined with IndexedDB data) [^src1].
- **Font loading** — a single variable woff2 covers the 100–900 weight axis, `font-display: swap` shows the fallback immediately, and `crossorigin="anonymous"` on the preload prevents a double fetch [^src1].
- **Inlined app shell** — just enough CSS and JS inlined in `<head>` to paint a correctly-themed, correctly-sized loading shell from `localStorage` before any bundle parses [^src1].
- **Render first, authenticate second** — the boot script checks whether `localStorage.ApplicationStore` exists ("do we have anything to show you") rather than validating the session; the real session token sits in a cookie and the next request (WebSocket handshake, sync delta) is what fails with a 401 and triggers a login redirect [^src1].

Auth follows the same shape as mutations: assume the happy path, verify in the background — the client trusts what's local, the server is the source of truth for correctness, and the two reconcile asynchronously [^src1].

## Design and animation as speed

Engineering speed makes a single interaction fast; design speed makes the *path* to each interaction short [^src1]. Linear makes the keyboard a primary input — single letters edit the focused issue, the `⌘K` command palette searches the local MobX pool (not the server) over nearly any action [^src1].

Animation can undo all the engineering work [^src1]. Browsers have three property tiers by cost: composited (`transform`, `opacity`) run on the GPU off the main thread; paint-triggering (`color`, `background-color`) redraw pixels; layout-triggering (`width`, `height`, `top`, `margin`) force re-layout of every subsequent element and must *never* be animated [^src1]. Linear keeps animations on composited properties, uses short durations (well below the industry norm of ~200ms Material / ~350ms iOS), and uses asymmetric timing (instant on enter, fade out over ~150ms) [^src1]. Motion references its origin — a popover scales out of the pill it came from — doing spatial work rather than decoration [^src1].

## Relationship to other concepts

- Local-first is a counterpoint to the [[software-engineering/cap-theorem|CAP Theorem]] framing: the local store *uses* eventual reconciliation with the server, trading immediate global consistency for availability and responsiveness on the client.
- The stack uses [[software-engineering/kubernetes|Kubernetes]] (one workload per concern) and Postgres on the backend; the sync server is the reconciliation target, not the UI's read path [^src1].

[^src1]: [How's Linear so fast? A technical breakdown](../../raw/web/how-s-linear-so-fast-a-technical-breakdown.md)

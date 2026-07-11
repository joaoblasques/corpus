# Consolidation job — design spec (2026-07-11)

> Status: **proposed, for review** (user asked to spec the LLM consolidation job).
> Grounding: corpus has ~949 `source` pages vs ~143 knowledge pages (concept/entity/synthesis)
> — a 1:6.6 shallowness ratio; 75 topic-clusters of ≥4 co-topic sources exist (e.g. "claude
> code" = 74 sources, "ai engineering" = 40, "mlops" = 18) with no unifying page.

## Goal

Turn scattered shallow **source-summary** pages into dense, cited **synthesis/concept** pages —
raising the corpus's *depth* (mature knowledge ÷ shallow pages), the real fitness metric behind
the "893 stubs / 67% quick-intake" problem. Deterministic where safe, LLM where judgment is
needed, provenance-preserving and reversible throughout.

## Non-goals

- Not deleting knowledge (supersession only, §7.1). Not touching raw sources.
- Not deepening individual stubs — that's Gardener's job. Consolidation is *cross-page merging*.
- Not embeddings in v1 (a v2 upgrade; v1 uses the topics/tags the corpus already has).
- Not real-time; it's a bounded **weekly** job (Opus economy).

## Architecture — four stages

```
cluster (deterministic)  →  triage (Sonnet)  →  synthesize (Opus)  →  verify (Sonnet critic)
   candidate clusters        real cluster?        write synthesis        faithful + cited?
   from topics+domain        + mode: new/deepen   cite ALL members       └ pass → commit
                                                                          └ fail → revert + queue
```

1. **Cluster (deterministic, no LLM).** Build a `(domain, topic)` inverted index from source-page
   `topics`/tags. A candidate cluster = a domain-topic with ≥`MIN_CLUSTER` (default 5) source
   pages. Rank by size × (no existing concept page for that topic). Emit the top-N candidates.
2. **Triage (Sonnet, cheap).** For each candidate: is it a *coherent* topic (not a grab-bag)? Does
   a concept/entity page for it already exist? → decide **mode**:
   - `new-synthesis` — no existing page → create one.
   - `deepen-existing` — a concept page exists → feed its Gardener-style deepening instead (hand
     off to the existing Gardener path; consolidation just supplies the member set).
   - `reject` — incoherent cluster → drop, log.
3. **Synthesize (Opus, weekly cap).** Writer reads the member source pages (+ their cited raw
   sources) and writes ONE `synthesis` page: TL;DR → mental model → patterns/gotchas, **every
   non-trivial claim cited** to a member's source (§7), short verbatim quotes retained (§7). It
   **links** each member page and carries a `consolidates:` frontmatter list.
4. **Verify (Sonnet fail-closed critic).** Independent check: (a) every claim traceable to a cited
   member; (b) no invented claims; (c) OKF-valid. Pass → commit. Fail → revert the new page and
   queue the cluster to a review file for a human. (Same fail-closed pattern as Gardener.)

## Provenance & supersession (the safety core)

- The synthesis **cites the members' original sources** (footnotes), never replaces provenance.
- Member source pages are **kept** and gain `consolidated_into: <synthesis-path>` frontmatter
  (so they're not re-clustered, and they're now reachable via the synthesis). They are NOT
  deleted — source-summaries are the provenance layer.
- Optional, conservative: a member that is *fully* absorbed (adds nothing beyond the synthesis)
  MAY be marked `superseded_by:` + `status: superseded` (kept as a stale stub with a forward
  link, §7.1) — only when the critic explicitly confirms full absorption. Off by default.
- Everything is reversible: supersession keeps the page; a bad synthesis is a single new file to
  revert. No destructive op in the pipeline.

## Schema touchpoints

- New frontmatter (all optional, additive): `consolidates: [paths]` on the synthesis;
  `consolidated_into: <path>` on members. Reuses existing `supersedes`/`superseded_by` (v0.6).
- OKF stays conformant (synthesis has `type: synthesis`, root-relative links).
- A schema-version bump + `_domains.md`/changelog log entry when merged.

## Components (files)

| File | Responsibility |
|---|---|
| `bin/consolidate.py` | pure: build clusters from source `topics`, rank, dedup vs existing concepts |
| `bin/consolidate_run.py` | orchestrator: cluster → Sonnet triage → Opus synthesize → Sonnet verify → commit/queue (headless-claude subprocesses, mirrors gardener.py) |
| `bin/consolidate_prompts.py` | the triage / synthesis / critic prompts (kept out of the runner) |
| `raw/_consolidation_review.md` | queue of clusters the critic rejected (human decides) |
| `bin/scheduled_run.py` | wire a **weekly** `run_consolidation` (Opus, bounded) into the existing Tue Opus slot |
| tests | cluster math, dedup, frontmatter stamping, critic-revert path, budget bound |

## Economy, cadence, bounds

- **Weekly** (existing Tue 13:00 Opus slot), never nightly — Opus cap protection.
- **Bounded:** `--max-clusters` (default 3/week) → ~3 syntheses/week; each Opus writer + Sonnet
  triage/critic. Scales with the shared token budget if a run sets one.
- Fitness metric added to the run report: **depth ratio** = knowledge ÷ (knowledge + source),
  tracked over time so the weekly synthesis can see progress (1:6.6 → target 1:3 over ~12 weeks).

## Open decisions (your call at review)

1. **Auto-commit vs human-gate.** Recommended: **auto-commit behind the fail-closed critic**
   (matches Gardener; reversible). Alternative: every synthesis goes to a review queue for a tick
   (safer, slower). — *Recommend auto + critic.*
2. **Supersede fully-absorbed source stubs?** Recommended: **off by default** (keep all members;
   only add `consolidated_into`). Turning it on trims the stub count but risks losing granular
   summaries. — *Recommend off; revisit once we trust the critic.*
3. **First-target domain.** Recommended: **pilot on `ai-engineering`** (511 sources, richest
   clusters) for the first few weeks, then widen. — *Recommend ai-engineering pilot.*
4. **Cluster signal v1.** Recommended: **topics+domain overlap** (uses existing frontmatter, zero
   deps). Embeddings (semantic clustering) are a v2 upgrade if topic-overlap proves too coarse.

## Phased build (after spec approval → writing-plans)

1. `consolidate.py` cluster+rank+dedup (pure, fully unit-tested, no LLM). Verifiable alone.
2. `consolidate_run.py` triage+synthesize+verify against the Gardener subprocess pattern; dry-run
   mode prints proposed clusters + modes, writes nothing.
3. Provenance stamping + critic-revert + review-queue.
4. Weekly wiring + depth-ratio metric in the run report.
5. Pilot on ai-engineering (3 clusters), review outputs, tune `MIN_CLUSTER`/prompts, then widen.

## Success criteria (12 weeks)

- Depth ratio 1:6.6 → **≤1:3**; ≥30 mature synthesis pages created.
- Zero provenance regressions (every synthesis claim cites a member source; critic-enforced).
- Zero destructive losses (supersession-only; all reversible).

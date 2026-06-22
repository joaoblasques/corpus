# Roadmap

Corpus is built in layers — each one making the system more self-sustaining without sacrificing auditability. The shipped work laid the foundation: collectors that fill the inbox, a pipeline that turns raw sources into structured knowledge, and a safety harness that keeps unattended runs honest. What comes next pushes the corpus toward a system that can identify its own gaps, strengthen its own reasoning, and (carefully) improve its own operating heuristics.

---

## Shipped

- [x] **Email collector** — reads labeled Gmail threads, ingests, then un-labels and archives processed messages. Full backlog drained on first run; new labeled mail processes nightly.
- [x] **YouTube collector** — downloads transcripts from configured playlists; rate-limited videos retry automatically on the next scheduled run.
- [x] **PDF collector** — monitors a cloud Drive folder; dropped PDFs are picked up on each nightly run.
- [x] **Obsidian collector** — drains configured vault note folders into the corpus; notes are stamped in place and optionally reaped from the vault after confirmed ingestion.
- [x] **GitHub Stars collector** — queues starred repositories with substantive READMEs as web sources.
- [x] **Cluster-based batch-ingest pipeline** — a five-phase coordinator/worker architecture (pre-flight → survey/cluster → global entity registry → per-cluster ingest → integrate/verify) that scales past ~10 heterogeneous sources without structural drift.
- [x] **Custodian safety harness** — a runtime wrapper for all unattended jobs: branch guard, pre-commit checks, abort-on-wrong-branch, structured operation logging.
- [x] **Gardener mode** — stub-filler that promotes `stub` pages to `draft` by pulling in relevant passages from already-ingested sources; uses a model split (strong model writes, cheap model fact-checks).
- [x] **This documentation site** — MkDocs-Material site covering architecture, collectors, the Custodian, and operational guides.

---

## Next

- [ ] **Adaptive Ingest** — dynamic fan-out during batch ingest: the coordinator detects source difficulty (length, domain novelty, conflicting claims) and escalates hard sources to the stronger model tier rather than running all sources at the same level. Includes a completeness critic pass that checks whether extracted entities and concepts match the density of the source material.

- [ ] **Dreamer: idle consolidation** — a weekly (or on-demand) pass that synthesizes across domains rather than within them. Identifies cross-domain concept overlap, generates meta-synthesis pages, and surfaces latent connections the per-source ingest pipeline misses. Runs on leftover Opus budget, timed to the weekly usage window reset.

- [ ] **Dreamer: gated self-improvement** — the Dreamer's second capability: proposing improvements to the agent's own ingestion heuristics (routing rules, domain thresholds, alias matching strategies) based on observed patterns across many runs. Proposals are written as diffs to the schema document and surfaced for human review — they do not apply automatically. The operating manual stays human-owned; heuristics graduate only with explicit sign-off.

- [ ] **Query skill maturation** — the `/query` operation already fetches and queues web sources for gap coverage; next: smarter index-selection (embedding-assisted retrieval over the full page catalog), richer synthesis file-back, and a gap-log dashboard so recurring uncovered topics surface as ingest priorities.

- [ ] **Contradiction dashboard** — a lint-mode report that surfaces all pages where `confidence` is below a threshold or where two pages make claims that the agent flagged as conflicting at ingest time. Today these are handled per-ingest; the dashboard aggregates them into a single review surface.

---

!!! abstract "Design principle: auditability over automation"
    Every capability on the roadmap is constrained by the same rule as everything already shipped: the corpus must remain an auditable record. Automation accelerates ingestion and synthesis; it does not replace the human in the loop for structural decisions (new domains, schema changes, heuristic graduation). The Dreamer's gated self-improvement is the clearest expression of this: the system can *propose* changes to its own operating manual, but it cannot *apply* them.

---

Next: [Under the Hood](under-the-hood.md) — the schema, domain rules, scheduling, and model split explained.

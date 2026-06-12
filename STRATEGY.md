---
name: Corpus
last_updated: 2026-06-12
---

# Corpus Strategy

## Target problem

You consume a high volume of technical and learning content across scattered channels — starred emails and newsletters, YouTube playlists, an Obsidian vault, clipped articles — but it never compounds. It piles up unread, decays, and the connections across sources are never made. The crux: the bookkeeping of synthesizing and cross-referencing it is too tedious to sustain by hand, so the knowledge stays scattered and lossy.

## Our approach

Delegate the tedious bookkeeping — reading, summarizing, cross-referencing, updating many pages, checking contradictions — to an LLM that doesn't get bored, governed by a strict human-authored schema (`CLAUDE.md`) that enforces provenance, dedup, and structure. The human owns sources and schema; the LLM owns the synthesis layer. So scattered intake compounds into a cited, self-organizing knowledge base instead of decaying. (Karpathy's LLM-wiki bet — rules out manual synthesis, capture-only apps, and schema-less chatbots.)

## Who it's for

**Primary:** You — a technical builder and lifelong learner with high-volume, broad intake (AI, data/software engineering, plus personal domains like music and skating). You're hiring the corpus to turn your firehose of saved content into a compounding, cited, queryable knowledge base without doing the synthesis bookkeeping by hand. An honestly-scoped n=1 personal tool for one demanding user.

## Key metrics

- **Backlog drain rate** — sources ingested per week vs. new sources arriving (net backlog change). Regresses when intake outpaces synthesis. Measured from `raw/_inbox/` + `corpus_ingested` stamps.
- **Cross-link density** — average links per corpus page and orphan rate. Measures compounding, not raw page count. Measured via `bin/lint`.
- **Corpus-answered query rate** — share of your questions answered directly from the corpus (with citations) vs. needing external search, plus filed-back syntheses. Qualitative + `_log.md`.
- **Integrity** — lint errors, contradictions, and stale stubs. Quality guardrail. Measured via `bin/lint`.

## Tracks

### Collection

Safe, automated collectors that pull every channel into `raw/` (email, YouTube, Obsidian + future).

_Why it serves the approach:_ feeds the synthesis engine continuously without manual capture.

### Ingestion & synthesis

The v0.6 cluster-based batch pipeline — route, dedup, entity-registry, cross-link — that compounds `raw/` into cited corpus pages.

_Why it serves the approach:_ this is the LLM bookkeeping the whole bet rests on.

### Schema & integrity

`CLAUDE.md` governance plus lint and claim-lifecycle that keep the growing corpus coherent and auditable.

_Why it serves the approach:_ the schema is what makes the LLM disciplined instead of drifting.

### Query & consumption

Turning the corpus into a trustworthy, queryable second brain — filed-back syntheses and reliable recall.

_Why it serves the approach:_ realizes the compounding value; currently the least-developed, highest-leverage track.

## Not working on

- **llm-wiki-system reconciliation** — merging the vault's corpus mirror is deferred to a careful separate pass to avoid duplicating the corpus into itself.
- **Grinding the duplicate/digest tail** — the remaining ~250 low-value backlog sources (dupes, newsletter digests) are diminishing returns vs. fresh collector intake.
- **Publishing / multi-user** — staying an n=1 private tool; no sharing/templating bet for now.

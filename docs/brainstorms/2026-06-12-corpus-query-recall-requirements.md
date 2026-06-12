# Corpus Query & Recall — Requirements

> Date: 2026-06-12 · Track: Query & consumption (`STRATEGY.md`) · Status: ready for `ce-plan`

## Summary

A `/query` operation that turns the corpus into a trustworthy **factual-recall** second brain. You ask "what did I learn about X?"; it answers from **cited corpus pages**. Where the corpus is thin, it **fetches fresh web content to fill the gap** (clearly marked as not-yet-in-corpus), **auto-queues that web content into `raw/_inbox/`** for later ingestion, and **offers to file** a valuable answer back as a synthesis page. Every gap is logged. This completes and operationalizes the thin `CLAUDE.md` §8.2 Query operation, which today has been exercised once (`corpus/ai-engineering/optimizing-claude.md`).

## Problem frame

Three of the four strategy tracks (Collection, Ingestion/Synthesis, Schema/Integrity) are built and proven; the corpus holds ~96 cited pages across 6 domains. But it can't yet be *used* as a second brain — there's no reliable, repeatable way to ask it a question and trust the answer. Without that, the whole compounding bet under-delivers: knowledge goes in but rarely comes back out. This feature closes the loop.

## Key decisions

- **Factual recall is the v1 shape.** Optimize for "what did I learn about X?" (synthesized, cited answer) — the highest-frequency moment. Cross-source synthesis, decision-support, and proactive rediscovery are deferred (they build on this).
- **Self-feeding, not pure read.** A gap doesn't just get logged — it gets *closed*: thin coverage triggers a live web fetch to answer, and those sources are queued for ingestion so the corpus learns from every query.
- **Gap-honest trust boundary.** Corpus-attributed claims are always cited to pages and never sourced from the model's general knowledge; web top-up is always labelled `[fresh — not yet in corpus]`. The user always knows what they actually knew vs. what was just fetched.
- **Frictionless capture, gated synthesis.** Fetched web sources auto-queue to `raw/_inbox/` with no prompt; writing a new corpus *page* (a filed-back synthesis) still requires explicit approval (per §8.2).

## Requirements

### Answering (recall)
- **R1** — `/query` answers a factual-recall question by reading `corpus/_index.md`, selecting and reading the relevant corpus pages, and synthesizing an answer.
- **R2** — Every non-trivial corpus claim in the answer carries an inline citation to the corpus page(s) it came from (per §7 provenance).
- **R3** — If the corpus fully covers the question, no web fetch and no `raw/_inbox/` write occur — it answers purely from corpus pages.

### Gap handling (self-feeding)
- **R4** — When the corpus is missing/thin for the question, `/query` fetches fresh web content (reusing `bin/fetch_link.py` article extraction) to answer, and marks those claims `[fresh — not yet in corpus]`, visually distinct from cited corpus claims.
- **R5** — Web sources fetched to fill a gap are auto-written to `raw/_inbox/` (channel `web`) for later ingestion — **no per-query confirmation** — deduped against already-collected sources (by `source_url`).
- **R6** — Every query that hits a gap appends a `query` entry to `corpus/_log.md` recording the question and what the corpus did not cover.

### Compounding (file-back)
- **R7** — After answering, `/query` **offers** (asks) to file the answer back as a `synthesis` page when the answer is non-trivial/derived; it writes the page only on approval, following the synthesis-page conventions (§3, §8.2) and updating `_index.md`/`_log.md`.

### Trust & resilience
- **R8** — `/query` never presents a corpus-attributed claim that came from the model's general knowledge; any general/web knowledge is labelled.
- **R9** — Web-fetch failures (paywalled/blocked, e.g. LinkedIn/x.com) are handled gracefully: the answer states the gap couldn't be auto-filled, the gap is still logged, and nothing is fabricated or queued for that source.

### Operation
- **R10** — `/query` is an interactive Claude-Code-session operation (needs corpus read + network + the ingest pipeline downstream); it is not headless/scheduled.

## Key flows

1. **Covered question** → read index → select + read relevant pages → synthesize answer with inline page citations → done (no web, no write).
2. **Gap question** → corpus thin → fetch web (`fetch_link`) → answer combining cited corpus claims + `[fresh]`-labelled web claims → auto-queue fetched web sources to `raw/_inbox/` → append gap to `_log.md`.
3. **File-back** → if the answer is non-trivial/derived, offer to save it as a synthesis page → on approval, write the page + update `_index.md`/`_log.md`; on decline, persist nothing beyond the gap log.

## Acceptance examples

- **AE1 (covered)** — Ask about a topic with corpus pages (e.g. "Spark OOM tuning") → cited answer drawn only from corpus pages; no web fetch; no `raw/_inbox/` write.
- **AE2 (gap → web)** — Ask about an uncovered topic → answer notes the corpus doesn't cover it, fetches web, answers with `[fresh]`-labelled claims, queues the web source(s) into `raw/_inbox/`, logs the gap.
- **AE3 (web fails)** — Uncovered topic where web fetch fails → answer states the gap couldn't be auto-filled; gap logged; nothing fabricated or queued.
- **AE4 (file-back offered)** — A non-trivial derived answer → user is offered a synthesis page; on "yes" the page is written + indexed; on "no" nothing is written beyond the gap log.

## Scope boundaries

**Deferred for later**
- Cross-source synthesis mode ("connect/compare what I know about X" as a first-class query).
- Decision-support mode ("given what I know, how should I do X?").
- Proactive rediscovery/push ("what relevant knowledge do I already have for what I'm doing now?").

**Outside this feature's identity (for now)**
- A semantic/vector search index — v1 retrieves via `_index.md` + targeted page reads, not embeddings.
- Headless/scheduled querying.

## Dependencies / assumptions

- **Reuses:** `bin/fetch_link.py` (article extraction), the v0.6 batch ingest pipeline (to later process queued web sources), `corpus/_index.md` (retrieval entry point).
- **Assumption:** the index + targeted page reads are sufficient retrieval for v1 (no embedding search yet). If recall proves unreliable at scale, a retrieval upgrade is a follow-up.
- **Consequence (from the self-feeding choice):** `/query` becomes a **third intake channel** feeding `raw/_inbox/` — it grows the backlog, so the "backlog drain rate" metric must keep pace with query-driven intake.

## Success criteria

- A covered factual-recall question returns an answer with **zero uncited corpus claims** and no spurious web fetch.
- A gap question reliably produces **either** a logged gap + a queued web source, **or** a clean "couldn't auto-fill" when the web fetch fails — never a fabricated answer.
- The **corpus-answered query rate** becomes measurable from `_log.md` query entries (covered vs. gap).

## Outstanding questions

**Deferred to planning**
- Retrieval mechanism: how `/query` selects candidate pages from `_index.md` (alias/keyword match vs. LLM selection over the index).
- Whether to cap web fetches per query (and how many), to bound cost when a gap spans many subtopics.
- The threshold for *offering* a synthesis file-back (what counts as "non-trivial/derived").

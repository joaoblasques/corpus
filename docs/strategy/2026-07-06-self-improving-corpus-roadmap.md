# Corpus source strategy & autonomy roadmap — self-improving, self-healing, self-growing

> Date: 2026-07-06 · Status: proposed (user requested honest strategic assessment)
> Grounding data: corpus at 1,065 pages, 713 (67%) shallow quick-intake, 737 stubs, 727 orphans,
> 117 broken citations; YouTube tech backlog drained to metadata tier; 749 hobby stubs parked in
> raw/_inbox; 8 real query-gaps logged in corpus/log.md.

## Part 1 — Verdict on YouTube as a source

**The honest answer: mostly not worth it, and yes — the same information exists elsewhere in
better form.**

Evidence from our own pipeline:

1. **Information density is poor.** Spoken tech content ≈150 wpm of heavily padded delivery. A
   20-minute video ≈ 3,000 transcript words that compress to a 3-sentence summary — and our
   *transcript-tier* pages prove it: even with the full transcript, the useful residue is ~4
   lines ("3 Boring AI Systems That Sell For $4000+" → "focus on revenue-generating systems").
   The transcript tier and the metadata tier converge on nearly the same value for this genre.
2. **The genre is derivative.** The auto-hoovered playlists are dominated by hype-cycle content
   ("5 NEW Vibe Coding Repos", "Build $10,000 Websites", "AI agents making money on their own?").
   These videos are themselves *downstream* of written primary sources — docs, release notes,
   blog posts, papers — which we can ingest directly, losslessly, and for free.
3. **The friction is uniquely terrible.** This one channel consumed: a Playwright browser scraper
   (built, hardened, then found useless for chapter-videos), caption IP rate-limits (~15-20/window,
   multi-day blocks), yt-dlp audio throttling (~60/day), Whisper cost, API delete quotas (50
   units/removal), and multiple engineering weeks. Meanwhile the docs pipeline ingests 30-80
   written sources/night on free LLMs with ~zero failures.
4. **What YouTube IS worth keeping for** (the exceptions that earn transcripts):
   - Unique primary content: conference talks, long-form interviews, lectures (Karpathy-class).
   - Demos of visual workflows that don't exist in writing.
   - **Deliberate curation**: the `Corpus_queue` playlist — a human explicitly flagged it.

**Policy change (recommended):**
- Default YouTube tier = **metadata pointer-back** (done for the 155-stub backlog). A query can
  still surface the video; the corpus doesn't pretend a 3-line summary is knowledge.
- Full transcript tier only for: `Corpus_queue` + a small channel whitelist (talks/interviews).
- Stop auto-collecting the long tail of tech playlists wholesale; keep collect-remove for the
  curated set. Opportunistic transcript *enrichment* of metadata pages when captions are free.
- Hobby playlists (music/exercise/skate): never collected (already policy). Archive the 749
  parked hobby stubs out of `raw/_inbox` (they are dead weight in every inbox scan).

## Part 2 — The real bottleneck has moved

The corpus does not have a collection problem anymore; it has a **consolidation problem**:
- 67% of pages are shallow 3-sentence stubs; 727 orphans; 117 broken citations.
- Volume is growing ~35-80 pages/night; depth (mature, cited, cross-linked pages) grows ~0-5/week.
- Per CLAUDE.md the corpus's value is *dense reference with provenance* — the current trajectory
  builds a large index of pointers instead.

**Adding more sources is not automatically better. Higher-signal sources + a depth loop are.**

Signal-density ranking (tokens of durable insight per token ingested):
**books ≫ papers > official docs/release notes > good blogs > newsletters > YouTube > social.**

## Part 3 — Roadmap: three loops + one economy

### A. Self-GROWING (demand-driven acquisition, not supply-driven hoovering)
1. **Gap-driven intake** (highest leverage, mostly built): `/query` already logs gaps with origin
   (8 real ones logged — Helix quant methods, healthcare DE, agentic patterns). Wire the gap log
   into an acquisition queue: nightly, top-N unresolved gaps → targeted WebSearch → fetch-and-queue
   (mechanism exists via `bin/query.py`). The corpus grows where demand proved a hole.
2. **Citation-following**: pages referencing not-yet-written concepts (broken internal links are
   OKF-legal and logged) become stub-creation/fetch candidates, bounded per night.
3. **New high-signal channels**:
   - **Books/PDFs** — the pipeline exists and works (CorpusInbox/PDFs, subfolder reap fixed);
     it is simply underfed. Add EPUB→markdown conversion; chapter-level source pages with real
     §8.1 ingest (books deserve the expensive tier).
   - **Papers**: arXiv RSS for the 3-4 topics that recur in gaps (agents, RAG/context, quant).
   - **Release notes/changelogs** of the tools actually used (Claude Code, Spark, dbt, …) — the
     factual layer YouTube videos paraphrase, at near-zero cost.
   - **Curated blog RSS** — `blogs to scrape.md` already seeds this; formalize as recurring feeds.
4. **YouTube demoted** per Part 1.

### B. Self-IMPROVING (the depth loop — the missing piece)
1. **Promotion pipeline** stub→draft→mature: nightly **Gardener quota** (Gardener is built and
   validated — 6/8 fills with fail-closed critic): each night, pick K stubs with the most inbound
   links, deepen them from already-ingested raw sources, with citations.
2. **Consolidation**: weekly job clusters shallow source-pages by topic (embeddings or alias
   overlap) → one synthesis/concept page absorbing N pointers (supersedes machinery exists in
   schema v0.6). Target: quick-intake share shrinking, not growing.
3. **Fitness function** — the corpus measures itself in every run report: stub ratio, orphan
   ratio, citation coverage, query gap-hit rate. The weekly synthesis reads the trend and
   reallocates quotas (more gardening vs more acquisition). That is the actual "self-improving"
   loop: measurement → reallocation, not more collectors.

### C. Self-HEALING (half-built; finish it)
1. Done: okf_lint (0 violations, nightly guard), all channel reapers, quota-safe playlist reap,
   test isolation.
2. Add an **auto-fix tier** to corpus_lint (safe fixes applied nightly, rest reported): orphan →
   link from domain hub; alias-overlap dedupe proposals; broken-citation repair (repoint to the
   moved raw file); staleness sweep (confidence decay when `last_confirmed` is old, per §7.1).
3. Inbox hygiene: archive hobby stubs; `_REVIEW.md` queue kept short.

### D. Economy (route source value → model tier)
- Free LLMs (Groq/OpenRouter): volume triage + quick intake (already live).
- Sonnet nightly (~50): full §8.1 ingest of the *substantive* subset (books, papers, curated).
- Opus weekly: synthesis, consolidation, contradiction resolution.
- Rule: **the more durable/primary the source, the higher the tier.** Never spend Opus on a
  YouTube summary; never let a book chapter go through the 3-sentence path.

## Sequencing (proposed)
1. **Now**: archive hobby stubs from `_inbox`; whitelist config for transcript-tier YouTube.
2. **Week 1**: gap-queue wiring (gap log → nightly targeted fetch); Gardener nightly quota.
3. **Week 2**: EPUB/book intake + "books" channel with full-ingest routing; arXiv/RSS feeds.
4. **Week 3+**: consolidation job; fitness metrics in run report; quota reallocation in weekly
   synthesis.

## Success criteria (12 weeks)
- Quick-intake share of corpus: 67% → <45%; stubs <35%; orphans <25%.
- ≥80% of new `/query` gaps answered from corpus within 7 days of being logged.
- ≥3 books fully ingested chapter-wise; YouTube ingest cost ≈ 0 engineering hours/month.

---

## Addendum (2026-07-06, later): full YouTube demotion + phased source-acquisition plan

User decision: **Corpus_queue also demoted** — no transcript tier remains anywhere; YouTube is
metadata-pointer-back only, clearing itself out via the nightly (collect-as-metadata → quick
intake → playlist reap, quota-bounded). Focus: **books and PDFs**.

### Source acquisition — phases (all automatic once built)

| Phase | Channel | Status | Mechanics |
|---|---|---|---|
| 0 | YouTube wind-down | **live** | all playlists metadata-tier; nightly clears remaining videos + reaps playlists (~1-3 nights, quota-bounded); zero transcript surfaces touched ever again |
| 1 | **Books (EPUB) + PDFs** | **live** | drop files in Drive `CorpusInbox/Books/` (epub) or `CorpusInbox/PDFs/`; nightly splits books into chapter stubs → FULL §8.1 ingest (~50 chapters/night ≈ 1-2 books/week); reaped to `_processed/` when fully ingested. Only manual step in the whole system: acquiring DRM-free files (Manning/PragProg/No Starch/O'Reilly sell DRM-free; Kindle is DRM'd) |
| 2 | Release notes + curated blog RSS | next build | `feeds.yaml` (tool changelogs: Claude Code, Spark, dbt, DuckDB…; blogs: Willison, Karpathy, Osmani, hamel.dev — seeds exist in blogs-to-scrape); nightly fetch new entries → quick-intake or full ingest by substance. Replaces YouTube's "news" function at zero friction |
| 3 | Papers (arXiv) | after 2 | standing arXiv queries derived from domains + gap log (agents, RAG/context, time-series momentum); abstract stubs, LLM triage promotes high-relevance papers to full ingest |
| 4 | Consolidation + fitness | after 3 | merge shallow page clusters into synthesis pages; stub/orphan/gap-hit metrics in the run report reallocate nightly quotas. Gap resolver (live) keeps demand-driven growth running throughout |

Priority routing stands: books/papers → full ingest (Sonnet); feeds/blogs → tiered by substance
(free LLMs for triage); YouTube → metadata only, forever.

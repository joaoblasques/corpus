# About the Corpus

> *A personal knowledge corpus with citation discipline, schema versioning, and synthesis-aware structure.*

Five concepts unpacked.

## Personal

The Corpus is single-author. You are the only writer; LLMs (Claude in chat, Claude Code at the terminal) are collaborators that operate under your authority, not co-authors with independent edit rights.

This isn't a casual detail — it shapes the whole design:

- **No consensus mechanisms.** No edit wars, no talk pages, no community review. The graduation criteria (≥3 sources + qualitative checks) is *your* bar, not a vote.
- **Opinionated structure is fine.** The domain split (ai-engineering / data-engineering / software-engineering) reflects your interests, not a universal taxonomy.
- **Tight discipline becomes possible.** A wiki with 1,000 editors can't enforce strict lint rules because the friction would block contribution. Single-author means schema enforcement has zero coordination cost.

Contrast with: Wikipedia (open editing, NPOV consensus), Confluence/Notion team wikis (collaborative, soft structure), Roam/Logseq personal KBs (personal but typically no schema discipline).

## Knowledge corpus

"Corpus" is the noun phrase head, and it carries specific weight.

- **Etymology**: Latin *corpus* = body. A corpus is a *body of work* — finite, curated, bounded, related-by-purpose.
- **Usage in scholarship**: corpus linguistics studies a defined collection of texts; "the Shakespeare corpus" means his completed works as a unit of study; *corpus juris* = the body of law.
- **What it implies that "wiki" doesn't**: curation, scholarly intent, deliberate boundaries. A wiki accretes; a corpus is composed.
- **What "knowledge" qualifies**: it's not a literary corpus or legal corpus — it's an organized body of factual and conceptual content about a defined set of domains.

In this system: 37 pages across 3 graduated domains, each page a node in a citation-and-derivation graph. Finite, bounded, related by professional interest.

## Citation discipline

Every substantive claim traces to a primary source. This is enforced by schema and lint, not by good intentions.

How it shows up concretely:

- **The `sources:` frontmatter field** lists external references (books, papers, talks) by canonical ID.
- **Graduation gate**: a domain doesn't become real until ≥3 distinct sources back it plus qualitative checks (zero orphans, zero contradictions, draft status, coherence).
- **Lint enforces it**: unsourced claims, orphan pages, and contradictions get flagged in §8.3 checks.
- **Deferred stubs prove the discipline holds**: pages remain deferred precisely when no primary source exists yet — no faking content with secondary aggregators or LLM-generated material.

"Discipline" is the right noun because it costs something. The discipline is saying no — to easy paraphrases of blog posts, to stub pages that won't graduate, to plausible-sounding LLM content that has no grounding.

## Schema versioning

The structure of pages — frontmatter fields, valid status values, lint rules, graduation criteria — is itself a *designed artifact*, versioned like software.

How this differs from typical personal KBs:

- **Most personal KBs evolve structure invisibly.** A field gets added one day, dropped the next, with no record. Cumulative drift, no migration path.
- **The Corpus treats structure as a spec.** v0.5 is the current stable version (committed `b6ab055`). v0.6 is in active design (`derived_from:` field, source-less concept stubs, §9 collision-rule cleanup, domain-rename as first-class).
- **Changes go through phases**: design doc in `raw/proposals/` → lint rules drafted and tested → spec written → retroactive backfill. Not ad-hoc.
- **Additive over breaking**: v0.5 pages stay valid as v0.6 pages. Breaking changes require deliberate migration plans.

The benefit: the system's evolution is reasonable about because there's a record of it. The cost: no adding a field on a whim — every schema change is a small project. That tradeoff is the point.

## Synthesis-aware structure

Pages aren't atomic and independent — they form a graph, and some pages are explicitly *syntheses* of other pages. The schema knows about this.

The mechanics:

- **`sources:`** captures external provenance (what books/papers/talks back this page).
- **`derived_from:`** (incoming in v0.6) captures internal provenance (what *other Corpus pages* this page builds on).
- **These are orthogonal.** A synthesis page can have both: external sources for its own claims, internal `derived_from:` for the upstream pages whose conclusions it composes.

Concrete example: `distributed-systems-fallacies.md` is a synthesis page. It cites three external sources (Deutsch 1994, Rotem-Gal-Oz, Hohpe talk) *and* derives from `microservices.md` and `kubernetes.md` — pages whose distributed-system properties it composes into the eight-fallacies framing.

"Aware" means the system *models* this. "Structure" means it's baked into schema and lint, not informal prose convention. Concrete payoff:

- Synthesis pages become a first-class kind, detectable by `derived_from:` presence
- Impact analysis becomes tractable: if `microservices.md` materially changes, every downstream page is findable
- The graph structure becomes queryable, not just narratively present

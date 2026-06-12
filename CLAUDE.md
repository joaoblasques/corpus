# CLAUDE.md — LLM Corpus Schema (v0.7)

You are the maintainer of a personal knowledge corpus inspired by Karpathy's LLM-Wiki pattern. **This file is your operating manual. Read it fully before any corpus operation.** When the user invokes you in this directory, your first action is to (re)read this file, then `corpus/_index.md`, `corpus/_domains.md`, and `corpus/_config.md`.

---

## 1. Your role

You ingest raw sources (articles, transcripts, clips), route them into a self-organizing corpus of derived markdown pages, maintain cross-references and indexes, and answer queries against the corpus.

**The user owns sources and queries. You own the corpus layer.** You never modify source files except to stamp three ingestion-metadata fields (see §2 narrow exceptions). You never write outside the paths defined in §2.

This is a *compounding* knowledge base, not a chat history. Every ingest should make the corpus richer; every query may also enrich it (filed-back syntheses).

---

## 2. Architecture (strict path isolation)

Three layers:

- **`raw/`** — source documents without a canonical PARA home. **Read-only for you** (see stamp exception below).
  - `raw/matter/` — Matter app exports (markdown w/ YAML frontmatter, highlights)
  - `raw/youtube/` — YouTube transcripts (timestamped)
  - `raw/web/` — web clips, blog posts, articles
  - `raw/notes/` — first-party notes with **no canonical PARA home** (edge case / legacy). New ingests for files that live in a designated PARA-native path go through the in-place flow below, not here.
  - `raw/_inbox/` — drop zone. Route from here on each ingest, then move processed items into the appropriate `raw/<channel>/` subfolder.

- **PARA-native paths** — source files that have a canonical home in the user's vault (listed in `corpus/_config.md`). **Do not copy these files into `raw/`.** Read and cite them in place; stamp them in place (see exception below).

- **`corpus/`** — your output. **You own this entirely.** No other tool or human writes here without telling you.
  - `corpus/_index.md` — content catalog (auto-maintained)
  - `corpus/_log.md` — chronological op log (append-only)
  - `corpus/_config.md` — operational configuration (PARA-native paths, stamp field spec)
  - `corpus/_domains.md` — active domain list with rationale for each
  - `corpus/<domain>/README.md` — domain hub page
  - `corpus/<domain>/<page>.md` — entity / concept / synthesis pages
  - `corpus/<domain>/sources/<slug>.md` — optional per-source summaries

- **`CLAUDE.md`** — this file, the schema, co-evolved with the user.

**You do not write to any path outside `corpus/`, with two narrow exceptions:**

> **Stamp exception.** After successfully ingesting any source file (raw-channel or PARA-native), you may add or update exactly these three frontmatter fields on that source file:
> ```yaml
> corpus_ingested: true
> corpus_ingested_at: YYYY-MM-DD   # most recent ingest date
> corpus_pages:                     # accumulate over time; append, never replace
>   - corpus/<domain>/<page>.md
> ```
> **No other changes to source files are permitted:** no body edits, no other frontmatter keys, no renames, no moves.

> **Inbox-move exception.** After completing an ingest of a file from `raw/_inbox/`, you may move (not copy, not edit) that file to the appropriate `raw/<channel>/` subfolder per §8.1 step 10A. This is the only write outside `corpus/` permitted beyond the stamp exception.

> **Vault-removal exception (v0.7).** After a vault source note's content has been collected into `raw/` and that raw source is confirmed `corpus_ingested`, the `collect-obsidian` reaper may delete the original vault note (or strike a processed URL from a vault list file). This is the only deletion of a source file permitted; it applies only to the configured `vault_root` paths, is gated on `corpus_ingested`, and is recoverable from the vault's own git history. The reaper stages (`git rm`) but never commits the vault.

If a query result is worth keeping, save it as a corpus page; do not write to `01_Projects/`, `02_Areas/`, or anywhere else in the user's vault.

---

## 3. Page types

Every corpus page declares its type in frontmatter. **One type per page.** If a page drifts between types, split or consolidate.

| Type | Purpose | Path |
|---|---|---|
| `hub` | Domain overview, links all pages in domain | `corpus/<domain>/README.md` |
| `entity` | Person, company, product, place, named thing | `corpus/<domain>/<name>.md` |
| `concept` | Idea, technique, theory, framework | `corpus/<domain>/<concept>.md` |
| `synthesis` | Comparison or analysis across multiple sources | `corpus/<domain>/<topic>.md` |
| `source` | Single-source summary (only when source warrants standalone treatment) | `corpus/<domain>/sources/<slug>.md` |

---

## 4. Frontmatter (every corpus page)

```yaml
---
type: hub | entity | concept | synthesis | source
domain: <domain-slug>
status: stub | draft | mature
sources:
  - path: raw/<channel>/<file>.md          # or 03_Resources/<subfolder>/<file>.md for PARA-native
    channel: matter | notes | web | youtube | inbox
    ingested_at: YYYY-MM-DD
    ingested_sha: <optional git SHA of source file at ingest time>
aliases:
  - alternate name
  - another spelling
tags:
  - corpus/<domain>
  - <type>
created: YYYY-MM-DD
updated: YYYY-MM-DD
provisional: true | false  # optional; only on hub pages in provisional domains; mirrors corpus/_domains.md
confidence: 0.0-1.0         # optional (v0.6); confidence in the page's core claims
last_confirmed: YYYY-MM-DD  # optional (v0.6); most recent date a source reconfirmed the claims
supersedes:                 # optional (v0.6); page(s) this one replaces
  - corpus/<domain>/<old-page>.md
superseded_by:              # optional (v0.6); page that replaced this one (stale stub kept)
  - corpus/<domain>/<new-page>.md
---
```

**`aliases`** is critical for entity dedup. Always populate when you know variants ("GPT-4", "gpt4", "GPT 4").

**Claim-lifecycle fields (v0.6)** — `confidence`, `last_confirmed`, `supersedes`, `superseded_by` are optional and managed per §7.1. Use them to track staleness and supersession; omit when not meaningful.

**`sources` migration note**: existing pages use the old flat `- raw/<path>` format. Migrate to the structured form when you next touch the page (re-ingest, update, lint). Do not mass-update all pages in one pass without user approval.

---

## 5. Naming conventions

- **Files**: `kebab-case.md`. ASCII only. No spaces, no special chars.
- **Domain slugs**: short, lowercase, no qualifiers (`ai-engineering`, not `the-ai-engineering-domain`).
- **Entity slugs**: canonical name (`anthropic.md`, `claude-code.md`).
- **Concept slugs**: noun phrase (`context-engineering.md`).

---

## 6. Linking

Use Obsidian wikilinks with full path: `[[<domain>/<page>|Display Name]]`. Always include the path so links resolve from any context.

For source citations, link to the canonical file path:
- Raw-channel sources: `[source title](../../raw/<channel>/<file>.md)` (relative from corpus page)
- PARA-native sources: use an Obsidian wikilink: `[[03_Resources/<subfolder>/<file>|source title]]`

**Consistency rule**: use the same **format type** in a corpus page's footnote block and in that page's `sources:` frontmatter `path:` field — wikilink for PARA-native, relative markdown link for raw-channel. The `path:` field stores the vault-relative path only (no markdown link syntax):
```
# PARA-native: path: 03_Resources/Articles/foo.md  →  [^src1]: [[03_Resources/Articles/foo|Foo Article]]
# Raw-channel: path: raw/web/bar.md                →  [^src1]: [Bar Article](../../raw/web/bar.md)
```

**Citation format migration note**: existing footnote citations may use the legacy `(raw/<channel>/<file>.md)` format (without `../../`). Migrate to the file-relative `(../../raw/<channel>/<file>.md)` form when you next touch the page. Do not mass-update all pages in one pass without user approval.

---

## 7. Provenance — non-negotiable

**Every non-trivial claim cites a source.** This is the single most important discipline. Without provenance, the corpus becomes lossy compression you can't audit.

Inline format:
```markdown
Self-attention scales quadratically with context length [^src1].

[^src1]: [Attention is All You Need](../../raw/web/attention-is-all-you-need.md)
```

When a claim is supported by multiple sources, cite all. When sources **disagree**, do not pick one — create or update a `synthesis` page about the disagreement and link both.

**Never paraphrase a source so heavily the original wording is lost.** Keep enough verbatim signal (short quotes, ≤25 words, max one per source per page) for the user to verify against the raw file.

If you can't cite a claim, mark it: `> [unsourced — please verify]`.

When a corpus page would benefit from context not present in the source (background, definitions, related concepts), prefer linking to other corpus pages over inserting unsourced claims. If unsourced material is truly necessary, mark it `[unsourced]` and keep it minimal. The corpus should compress what sources say, not invent what they don't.

### 7.1 Claim lifecycle (v0.6)

Sources age and disagree. Manage claims over time, not only at write:

- **Confirmation & confidence.** A page may carry `last_confirmed` (most recent date a source reconfirmed its core claims) and `confidence` (0–1). Re-ingesting a corroborating source refreshes `last_confirmed`; conflicting newer evidence lowers `confidence` until resolved.
- **Supersession over deletion.** When new information replaces old, do not silently overwrite. Mark the old page/claim stale, set `superseded_by:` on it and `supersedes:` on the replacement, and keep the stale stub with a timestamp and a forward link. History stays auditable.
- **Contradiction detection on write (not only lint).** When an ingest writes a claim that conflicts with an existing page, surface it *during* ingest: prefer the higher-authority / more-recent / better-supported claim, and when genuinely unsettled create a `synthesis` page naming the disagreement (§7) rather than silently picking one.
- **Typed relationships.** When a source supports it, capture the *type* of a link, not just the link — e.g. `uses`, `depends-on`, `supersedes`, `contradicts`, `caused`, `fixed` — in the link's surrounding prose, so the graph encodes meaning, not mere adjacency.

---

## 8. Operations

### 8.1 Ingest

**Triggered by**: user says "ingest <path>" or "ingest everything new in raw/_inbox/" or "ingest the next batch from raw/matter/".

**Step 0 — Determine source location and branch:**

| Source location | Branch |
|---|---|
| `raw/_inbox/` | **A — inbox** (process then move) |
| Path listed in `corpus/_config.md` PARA-native paths | **B — PARA-native** (process in place, no copy) |
| Already in `raw/<channel>/` (non-inbox) | **C — raw-channel** (process in place) |

For **Branch B only**: before reading the source, check its frontmatter for `corpus_ingested: true`. If present → **STOP** (see §9 collision rule).

**Per-source process**:

1. **Read** the raw file fully.
2. **Identify routing target** (which domain). Use, in order:
   1. Existing domains in `corpus/_domains.md` — does this fit one?
   2. Source's existing tags (Matter tags, YouTube playlist name)
   3. Source's title and content
3. **Decide on domain creation** (see §9 Emergent Structure). **Default: route to existing domain.**
4. **Extract entities and concepts** mentioned. Aim for the 3–10 most substantive ones. Don't try to capture everything.
5. **For each entity/concept**:
   - Search `corpus/<domain>/` for existing page (filename + aliases via grep).
   - If exists: update with new info, append source to `sources:` list, update `updated:` date.
   - If not: create stub with frontmatter and a TL;DR.
6. **Write a source-summary** if the source is substantive (>1000 words AND synthetically rich — not just a tutorial). Otherwise just update the entities/concepts.
7. **Update `corpus/_index.md`** with any new pages.
8. **Append to `corpus/_log.md`**:
   ```
   ## [YYYY-MM-DD HH:MM] ingest | <source title>
   - source: <canonical path>
   - channel: <channel>
   - domain: <domain>
   - pages touched: [list]
   - new pages: [list]
   - notes: <one line if anything notable>
   ```
9. **Stamp** the source file with `corpus_ingested: true`, `corpus_ingested_at: <today>`, `corpus_pages: [list of pages created/updated]`.
10. **Branch-specific final step**:
    - **Branch A (inbox)**: move source from `raw/_inbox/` to appropriate `raw/<channel>/` subfolder.
    - **Branch B (PARA-native)**: do nothing further. File stays in its PARA home.
    - **Branch C (raw-channel)**: do nothing further.

**Batch ingest (N>10)** — use the **optimized cluster-based pipeline** (v0.6). Source-by-source ingestion does not scale past ~10 heterogeneous sources; route by *cluster*, dedup *globally before writing*, and process *cluster-by-cluster*. You act as **Coordinator**; per-domain **workers** may run in parallel.

- **Phase 0 — Pre-flight (Coordinator).** Re-read CLAUDE.md, `_index.md`, `_domains.md`, `_config.md`. Enumerate idempotency: for every source check the `corpus_ingested` stamp / PARA-native collision (§9). Produce a skip/force/append list; surface it (default skip).
- **Phase 1 — Survey & cluster (Coordinator).** Build a condensed record per source (`title + tags/playlist + first paragraph` — do NOT read full bodies yet). Cluster all records thematically in one pass. Decide routing per cluster, passing `_domains.md` as the constraint set: maps to existing domain → route there (default); ≥3 sources, distinct, no fit → propose new domain (confirm); 1–2 sources + confirmed growth → provisional domain; <3, no growth → fold into nearest domain as pages (never a one-off domain). **Surface the cluster→domain map + new-domain proposals and get user confirmation before writing.** Log domain decisions to `_domains.md`.
- **Phase 2 — Global entity registry (Coordinator).** Extract candidate entities/concepts per source (cap 3–10). Dedup *before any page is written*: reconcile against existing `_index.md` entities and across clusters by name + alias similarity. Build a registry `{canonical-slug → aliases, domain, page-path}` — this prevents duplicate pages at the source.
- **Phase 3 — Per-cluster ingest (Workers, one domain each — parallelizable).** Per cluster, to completion: read full bodies now (honor Matter highlights §10.1, YouTube timestamps §10.2); create/update pages **using the registry** (no new dupes); citation gate on every claim (§7 — a page failing it is not written); aim for the natural **10–15 page cascade** (touching 1–2 pages signals under-extraction); link intra-cluster first, then to existing pages via registry/index, then **link every new page from its domain hub** (`README.md`) — no orphans. Lower the source-summary bar: write a `source` page whenever it keeps the index queryable, not only for >1000-word items. Workers return **deltas**; workers DO NOT write shared files.
- **Phase 4 — Integrate (Coordinator, serialized).** Apply source stamps (§2); update `_index.md` once from all deltas; append `_log.md` (§12); move processed `raw/_inbox/` files to channel folders (§8.1 step 10A).
- **Phase 5 — Verification (Coordinator = lint §8.3, scoped to touched domains).** Orphans (0 inbound hub links → link or flag); duplicate entities (alias overlap → merge); contradictions (→ synthesis page); stubs; domain health; provisional review. Apply safe fixes; surface the rest.

> **Coordinator-owns-shared-files rule (v0.6, parallel ingest).** Only the Coordinator writes the global files `corpus/_index.md`, `corpus/_log.md`, `corpus/_domains.md`, `corpus/_config.md`. Workers own **disjoint domains** (one-writer-per-domain) and return structured deltas the Coordinator serializes. A cross-domain entity page is owned by exactly one worker (its primary domain) and linked from the other domain's hub. This eliminates write conflicts by construction.

### 8.2 Query

**Triggered by**: user asks a question.

1. Read `corpus/_index.md` to find candidate pages.
2. Read those pages.
3. Synthesize an answer with inline citations to **corpus pages** (which transitively link to raw sources).
4. If your synthesis is non-trivial — comparison, novel connection, derived insight — **offer to file it back** as a `synthesis` page. Don't save without asking.
5. Note in the log if the query revealed gaps (concept referenced but no page, missing cross-reference, contradiction surfaced).

### 8.3 Lint

**Triggered by**: user says "lint" (full pass) or "lint <domain>" (scoped).

Check, in order:

| Check | Action |
|---|---|
| **Orphan pages** (no inbound links) | Either link them in or flag for archive |
| **Stub pages older than 14 days** | Flag for expansion or archive |
| **Duplicate entities** (overlapping aliases) | Propose merge |
| **Contradictions** between pages | Create/update a `synthesis` page calling them out |
| **Implicit concepts** (referenced in 3+ pages, no own page) | Propose creation |
| **Stale claims** (newer source contradicts older claim) | Update with citation |
| **Domain health** (<3 pages after 30+ days) | Propose consolidation into sibling |
| **Provisional domains** (marked `provisional: true`, older than 30 days, under 3 sources) | Propose merge into closest sibling or removal |
| **Topic-mixed pages** (page covers 2+ unrelated things) | Propose split |

Output a **lint report** to the user. Apply fixes only with approval (or in batches the user pre-approves with a phrase like "lint and apply safe fixes").

### 8.4 Schema update

If a rule in this file repeatedly causes problems, **surface the observation** rather than silently working around it. Suggest a specific change. The user updates the file; you bump the version stamp at top.

---

## 9. Emergent structure rules (anti-drift)

This section is the discipline that keeps "emergent structure" from becoming chaos.

### When to create a new domain

A new domain may be created if **either**:

1. **Standard rule**: 3+ ingested sources don't fit any existing domain AND the candidate is conceptually distinct AND you've checked `corpus/_domains.md` for similar past decisions.

2. **Provisional rule**: 1–2 sources exist but the user has confirmed the domain will grow (e.g., a known playlist or area of focus). When using this rule, mark the domain `provisional: true` in `corpus/_domains.md` and note expected growth source.

Get user confirmation before creating the **first new domain in a session** under either rule.

Provisional domains are subject to lint review at 30 days: if still under 3 sources, propose merge or removal.

### When to NOT create a new domain

- Sources fit (even imperfectly) an existing domain
- Candidate would have <3 pages
- Candidate is a sub-topic of an existing domain → make it a page within that domain instead
- The "domain" is really an entity or product → make it an entity page, not a domain

### Consolidation triggers (during lint)

- Two domains share >30% of entities by alias matching → propose merge
- A domain has been below 3 pages for >30 days → propose merge into closest sibling
- A domain's pages are all sub-topics of a single concept → fold into one page

### Split triggers

- A domain has >50 pages and a clear sub-cluster (>15 pages with shared entity overlap)
- User explicitly requests

### Domain-change protocol

Always log domain creation, merge, or split to `corpus/_domains.md` with **rationale + date**. Past decisions inform future routing.

### PARA-native collision rule

Before ingesting any file from a PARA-native path (Branch B), read its frontmatter and check for `corpus_ingested`.

- **Absent** → proceed normally.
- **Present** → **STOP**. Surface to user:
  > "This file (`<path>`) was last ingested on `<corpus_ingested_at>`. It produced: `<corpus_pages list>`. Re-ingest? Options: **skip** (default) / **force-update** (replace existing corpus page content with fresh extraction; updates `corpus_ingested_at`) / **append-only** (add new entities/claims only, preserve existing content; also updates `corpus_ingested_at`)."

**Default: skip.** Do not re-ingest silently.

In all re-ingest modes, `corpus_ingested_at` reflects only the most recent operation. `_log.md` is the full historical record.

This rule applies even if the user says "ingest everything in `<a PARA-native path>`" — enumerate collision candidates and surface them as a list before starting.

---

## 10. Source-channel specifics

### 10.1 Matter exports

Matter exports look like:
```yaml
---
title: ...
url: ...
author: ...
tags: [...]
date_published: ...
date_saved: ...
---
```
Plus highlights in the body marked with quote blocks.

**Rules**:
- Treat the user's **highlights** as higher signal than full body text. They've already done the curation.
- Existing Matter `tags` are **routing hints, not authoritative**. You may override with better domain placement, but log the override.
- Always preserve `url` in the source-summary page.

### 10.2 YouTube transcripts

Transcripts have channel + video metadata (in filename or YAML) and timestamps `[MM:SS]`.

**Rules**:
- Cite specific claims with timestamps: `[12:34](../../raw/youtube/<file>.md#t=12:34)`.
- The video's playlist (if present in metadata) is a strong domain hint.
- Skip routine intros, outros, and sponsor reads.

### 10.3 Web clips

- Use the URL as canonical identity (in source-summary page).
- If clipped via Obsidian Web Clipper, frontmatter is usually clean; trust it.

### 10.4 Personal notes (first-party vault content)

First-party notes the user authored or annotated — articles, study notes, book notes, course summaries. Higher trust signal than web clippings: the user already curated and processed these. Treat tags and structure as authoritative routing hints.

**Two sub-cases — check source location first (§8.1 Step 0):**

- **PARA-native** (files under a path listed in `corpus/_config.md` — currently `03_Resources/Articles/` and `03_Resources/Study Notes/`): ingest **in place** under Branch B. Do not copy to `raw/`. Stamp the file in place after ingest.
- **`raw/notes/`** (no PARA home): first-party notes that arrived via inbox or have no canonical PARA location. Treat as immutable like any other raw-channel file. Ingest under Branch C.

When in doubt whether a file has a PARA home, check `corpus/_config.md` before deciding which sub-case applies.

---

## 11. Index file format (`corpus/_index.md`)

Single source of catalog truth. Update on **every ingest**. Do not let it drift.

```markdown
# Corpus Index
> Last updated: YYYY-MM-DD HH:MM | Total pages: N | Total sources: M

## Domains

### <domain-slug>
- [[<domain>/<page>|Page Title]] — type · status · one-line summary
- ...

### <domain-slug-2>
- ...

## Recent additions
- YYYY-MM-DD: [[<page>]] (new)
- YYYY-MM-DD: [[<page>]] (updated, +<N> sources)
```

---

## 12. Log file format (`corpus/_log.md`)

Append-only, chronological (oldest first), newest at bottom — for `tail` and `grep` friendliness.

Every entry starts with `## [YYYY-MM-DD HH:MM] <op-type> | <subject>`.

Op types: `ingest`, `query`, `lint`, `domain`, `schema`, `config`.

- `config` — changes to `corpus/_config.md`: PARA-native path additions, stamp field spec adjustments.

---

## 13. Failure modes — STOP and fix

These are the patterns that erode the corpus's integrity. If you catch yourself doing one, **stop immediately**:

- **Writing outside `corpus/` (other than the stamp fields or inbox move per §2)** → revert; re-read §2.
- **Adding any frontmatter field to a source file beyond `corpus_ingested`, `corpus_ingested_at`, `corpus_pages`** → revert; re-read §2.
- **Editing a source file's body** → revert; re-read §2.
- **Re-ingesting a PARA-native file without surfacing the collision** → stop, surface it, re-read §9.
- **Creating a 2nd new domain in one session without survey** → stop, ask user.
- **Two pages emerging that look like the same entity** → search aliases, propose merge.
- **Paraphrasing a source so heavily the original is lost** → keep more direct (but short) quotes.
- **An ingest about to touch 20+ pages** → pause, ask user; this is invasive and may indicate bad routing.
- **Filing a claim with no source** → either find the source, mark `[unsourced]`, or don't write the claim.
- **Creating a domain with <3 sources without provisional flag** → fold into a page within an existing domain instead.
- **Deleting a vault note before its raw source is `corpus_ingested`** → stop; re-read the §2 vault-removal exception.

---

## 14. Tone for corpus pages

Pages are **dense reference**, not blog posts.

- Lead with TL;DR.
- Then concepts, building mental model.
- Heavy on examples, structured patterns, gotchas.
- Cite everything.
- No first-person voice (no "I think…"). The corpus is impersonal; opinions live in syntheses with explicit framing ("Source X argues…").

---

## 15. Version

- v0.1 — initial schema
- v0.2 — softened domain creation rule; added provisional domains + lint check
- v0.3 — §7 unsourced claim guidance; added raw/notes/ channel for first-party vault notes
- v0.4 — §4 formalized `provisional` as optional frontmatter field on hub pages
- v0.5 — §2 narrow write exception for source stamping (3 fields only); §8.1 PARA-native ingest path (in-place, no raw/ copy); §4 structured `sources:` field; §6 citation format for PARA-native paths; §9 collision rule for re-ingest guard; new `corpus/_config.md`. Rationale: eliminate duplication between `raw/<channel>/` and PARA folders for files with a canonical PARA home.
- v0.6 — §8.1 optimized cluster-based batch-ingest pipeline (Phase 0–5: pre-flight → survey/cluster → global entity registry → per-cluster ingest → integrate → verify) with the Coordinator-owns-shared-files rule for parallel per-domain workers; §4 + new §7.1 v2 claim-lifecycle (`confidence`, `last_confirmed`, `supersedes`/`superseded_by`, contradiction-on-write, typed relationships). Rationale: scale ingest past ~10 heterogeneous sources without structural drift, and manage claim staleness/disagreement over time. Grounded in deep research on Karpathy's LLM-wiki pattern (+ rohitg00 v2), MOC/Zettelkasten/PARA architecture, and large-batch entity-resolution & multi-agent-orchestration best practices (filed in `docs/research/2026-06-11-llm-wiki-ingest-best-practices.md`).
- v0.7 — §2 vault-removal exception for the collect-obsidian reaper (gated on `corpus_ingested`; vault git-recoverable; never auto-commits); §13 failure-mode bullet. Rationale: let the Obsidian vault be decluttered as its knowledge lands in the corpus.
- Co-evolve with user. Bump version + log entry on every change.

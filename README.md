# Corpus

*A personal knowledge corpus with citation discipline, schema versioning, and synthesis-aware structure.*

## What this is

**Personal.** The Corpus is single-author. You are the only writer; LLMs are collaborators that operate under your authority, not co-authors with independent edit rights. That single-author premise is what makes the rest of this discipline possible — strict schema enforcement has zero coordination cost when there is no one to coordinate with.

**Knowledge corpus.** A *corpus* is a body of work — finite, curated, bounded, related by purpose. The word is chosen deliberately over "wiki": wikis accrete, corpora are composed. This is an organized body of factual and conceptual content about a defined set of domains (currently: ai-engineering, data-engineering, software-engineering).

**Citation discipline.** Every substantive claim traces to a primary source, enforced by schema and lint rather than good intentions. The `sources:` frontmatter field is mandatory, domain graduation requires ≥3 distinct sources plus qualitative checks, and unsourced claims fail lint. Pages remain stubs rather than fake content from secondary aggregators or LLM-generated material.

**Schema versioning.** The structure of pages — frontmatter fields, valid status values, lint rules, graduation criteria — is a designed artifact, versioned like software. v0.5 is the current stable spec; v0.6 is in active design. Schema changes are additive where possible, go through a design → lint → spec → backfill phase sequence, and are recorded — never ad-hoc drift.

**Synthesis-aware structure.** Pages aren't atomic; they form a graph, and some pages are explicitly *syntheses* of other pages. `sources:` captures external provenance (books, papers, talks); `derived_from:` (v0.6) captures internal provenance — what other Corpus pages a synthesis builds on. The two are orthogonal, both are first-class, and the structure is queryable rather than narratively implicit.

See [`corpus/_about.md`](corpus/_about.md) for the full reasoning behind each of these.

## What this is

You drop sources (Matter exports, YouTube transcripts, blog posts) into `raw/`. Claude Code reads them, decides which topic each belongs to, builds corpus pages, maintains cross-references and indexes, and answers your questions against the accumulated knowledge.

The structure is **emergent**: domains are created as ingestion reveals them. The discipline that prevents drift lives in `CLAUDE.md` (§9 Emergent Structure).

## Directory layout

```
llm-corpus/
├── CLAUDE.md              ← the schema (Claude reads this first, every session)
├── README.md              ← this file (for you)
├── raw/                   ← inputs (immutable; you populate)
│   ├── matter/            ← Matter app exports
│   ├── youtube/           ← YouTube transcripts
│   ├── web/               ← blog posts, articles
│   └── _inbox/            ← drop new stuff here; Claude routes from here
└── corpus/                  ← outputs (Claude owns; you read)
    ├── _index.md          ← auto-maintained catalog
    ├── _log.md            ← chronological op log
    ├── _domains.md        ← active domains + rationale
    └── <domain>/          ← created on first ingest into that domain
        ├── README.md
        └── <page>.md
```

## Where to install in your vault

Recommended: `2-Resources/llm-corpus/`. This keeps PARA discipline — the corpus is reference material.

Alternative: vault root, if you want it cross-cutting and prominent.

## Bootstrap (first run)

### Step 1 — Place this directory in your vault

Unzip into `2-Resources/llm-corpus/` (or wherever you decided).

### Step 2 — Get your Matter export ready

Export from Matter. Drop the markdown files into `raw/matter/`.

If you have hundreds, that's fine — the system batches.

### Step 3 — Open Claude Code in the vault root

```bash
cd ~/path/to/your/vault
claude
```

(Or open a terminal inside Obsidian if you have a terminal plugin.)

### Step 4 — Survey pass

Tell Claude:

> Read `2-Resources/llm-corpus/CLAUDE.md`. Then do a survey pass on `2-Resources/llm-corpus/raw/matter/` — read titles, tags, and first paragraphs only. Propose an initial set of domains based on what's there. Do not ingest yet.

Claude will read the schema, scan your Matter library, and propose domains. **Review, push back, refine.** This is your one chance to anchor the structure cleanly before sources start landing.

When happy:

> Lock these domains into `corpus/_domains.md` with rationale. Then ingest the first batch of 20 sources from `raw/matter/`.

### Step 5 — Watch the first batch

After 20 sources, **stop and review**:
- Open `corpus/_index.md` — does the catalog look reasonable?
- Open `corpus/_log.md` — any flagged anomalies?
- Spot-check 2–3 generated pages — are they citing sources properly?

If something is off, **fix it now** — either by editing `CLAUDE.md` to clarify the rule, or by telling Claude to redo with corrections. Drift is cheapest to fix early.

### Step 6 — Continue in batches

> Ingest the next 20 sources from `raw/matter/`.

Repeat until done. Run a lint pass periodically:

> Run a full lint pass. Output the report; don't apply fixes yet.

## Dependencies

### YouTube browser transcript tier (logged-out Playwright)

The corpus can scrape YouTube transcripts via a logged-out browser when the backend API rate-limits. This requires Playwright and Chromium:

```bash
# Browser transcript tier (logged-out Playwright)
python3 -m pip install playwright
python3 -m playwright install chromium
```

See `docs/solutions/youtube/browser-transcript.md` for details on when this tier activates and how to test it.

## Daily / weekly workflow

### Adding a new source

1. Drop file into `raw/_inbox/` (or directly into `raw/youtube/`, `raw/web/`, etc.)
2. In Claude Code: `Ingest raw/_inbox/<file>.md`

Claude routes it, updates pages, updates index, logs.

### Adding a YouTube transcript

Easy way: use a transcript-fetcher (yt-dlp + whisper, or a YouTube transcript API) to dump `.md` files into `raw/youtube/`. Include the playlist name in the filename or YAML for routing hints.

### Querying

Just ask:
> What did I read about context engineering?

Claude reads the index, finds relevant pages, synthesizes an answer with citations. If the synthesis is non-trivial, it'll offer to file it back as a `synthesis` page.

### Linting (weekly cadence recommended)

> Lint the corpus. Report orphans, stale stubs, duplicate entities, and contradictions. Do not apply fixes.

Review the report; tell Claude which fixes to apply.

## What the schema enforces (and why)

The CLAUDE.md file is doing real work. Key disciplines:

- **Path isolation**: Claude only writes inside `corpus/`. Your vault is otherwise untouched.
- **Provenance**: every claim cites a source. Without this, the corpus becomes lossy compression you can't audit.
- **Anti-drift on emergent structure**: a new domain requires 3+ sources, conceptual distinctness, and (for first-of-session) your confirmation. Without these gates, "self-organizing" becomes "1 domain per source."
- **Survey-first on big ingests**: prevents the first source from anchoring a bad structure.
- **Append-only log**: makes it easy to see what happened and roll back if needed.

Read `CLAUDE.md` yourself — it's the program. Customizing it is how you tune the system to your taste.

## Co-evolving the schema

When a rule causes friction, edit `CLAUDE.md`. Bump the version stamp at the top. Add a log entry to `corpus/_log.md` explaining the change.

Examples of useful customizations:
- Stricter or looser citation requirements
- Adding a new source channel (e.g., `raw/podcasts/`)
- Changing domain-creation thresholds
- Adding domain-specific page templates

## Backup / version control

The corpus is just markdown files. Put it in git:

```bash
cd 2-Resources/llm-wiki
git init
git add .
git commit -m "wiki: initial schema"
```

Now every ingest can be diffed and rolled back. Strongly recommended before doing any large batch ingest.

## Common gotchas

- **Claude wants to create too many domains.** Tighten §9 in `CLAUDE.md`. Bump the threshold from 3 to 5 sources, or require explicit user approval for every new domain.
- **Pages getting too long / mixed-topic.** Run a lint pass with the "topic-mixed pages" check. Split aggressively; the corpus rewards small, focused pages.
- **Claude writes outside `corpus/`.** Re-read §2 of CLAUDE.md to it. Add a hard stop with explicit examples if it recurs.
- **Source-summary pages everywhere.** Most sources don't warrant their own page — they should just update the entity/concept pages they inform. Tighten the criterion in §8.1 step 6.
- **Lint produces a wall of "stub" warnings.** Stubs are fine if they're young. The real signal is stubs >14 days old. Adjust the threshold if needed.

## What this is NOT

- A replacement for your atomic notes / journal / project notes. Those stay in PARA.
- A substitute for reading sources. The corpus is a *compounding index* over what you've read; it doesn't replace the act of reading.
- An automated knowledge-extraction service. You drive the ingestion and ask the questions.

## Karpathy's original gist

For reference, the pattern this is built on:
https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

# Under the Hood

This page explains the architectural decisions and operational mechanics that make Corpus run — the schema that governs it, how it self-organizes, and how unattended jobs keep the pipeline alive without burning through a model budget.

---

## The Schema: a Living Constitution

Everything in Corpus — how pages are typed, how claims are cited, when a new topic area is allowed to form — is encoded in a single document called the schema (stored at the repo root as `CLAUDE.md`). The agent reads this file at the start of every session. It is not code; it is prose that the agent treats as authoritative instructions.

The schema defines:

- **Page types** — every corpus page is exactly one of five types:

  | Type | Purpose |
  |---|---|
  | `hub` | Domain overview; links every page in the domain |
  | `entity` | A named thing: person, company, product, place |
  | `concept` | An idea, technique, theory, or framework |
  | `synthesis` | Comparison or analysis across multiple sources |
  | `source` | Single-source summary for substantive standalone material |

- **Frontmatter contract** — every page carries a standard YAML block: `type`, `domain`, `status` (`stub` / `draft` / `mature`), a structured `sources` list (with channel, ingestion date, and optional git SHA), `aliases`, `tags`, `created`, and `updated`. Optional claim-lifecycle fields (`confidence`, `last_confirmed`, `supersedes`, `superseded_by`) track staleness and supersession over time.

- **Naming rules** — `kebab-case.md`, ASCII only, short noun phrases for concepts, canonical names for entities.

- **Wikilink format** — full-path Obsidian wikilinks everywhere, so links resolve from any context regardless of nesting depth.

- **The provenance rule** — every non-trivial claim must cite a source. Uncited claims are explicitly marked `[unsourced]`. This is described as "the single most important discipline" in the schema, and the agent treats it as non-negotiable.

!!! abstract "Why a single prose document?"
    Code can enforce syntax; it cannot enforce meaning. The schema encodes *intent* — when to merge pages, what counts as a domain, how to handle disagreement between sources. Keeping it in prose means the user can read, audit, and evolve it without touching code.

---

## Self-Organizing Domains

The corpus organizes content into a small number of topic areas called **domains** (currently around seven active ones). A domain maps to a folder under `corpus/` and has a hub page that links every page inside it.

Domains are not free-form tags. The schema enforces strict rules about when one may be created:

- **Standard rule:** 3 or more ingested sources that do not fit any existing domain, and the topic is conceptually distinct.
- **Provisional rule:** 1–2 sources exist, but the user has confirmed the area will grow. The domain is flagged `provisional: true` and reviewed at 30 days; if still under 3 sources it is merged or removed.

Every domain creation, merge, or split is logged to `corpus/_domains.md` with a rationale and date, so past decisions inform future routing. The consolidation triggers are symmetric: two domains sharing more than 30% of entities by alias → propose merge; a domain below 3 pages for more than 30 days → propose merge into the closest sibling.

!!! tip "The key discipline"
    The anti-drift rules exist because "self-organizing" systems tend to proliferate structure. The schema defaults to folding content into existing domains; new structure requires justification.

---

## The Scheduled Pipeline

Two unattended jobs keep the corpus growing without requiring the user to be present:

| Job | Schedule | What it does |
|---|---|---|
| **Nightly collect + ingest** | Daily, ~2 AM | Runs every collector (email, YouTube, PDFs, Obsidian, GitHub), caps ingestion at 50 sources per run, commits and pushes to `main` |
| **Weekly deep pass** | Once per week, timed before the usage window resets | Uses leftover high-end model capacity for deep synthesis work — cross-domain linking, claim consolidation, stub promotion |

The nightly job is gated: it aborts if it detects it is not on the `main` branch, and a pre-commit branch check prevents commits landing on the wrong branch due to race conditions.

---

## The Model Split

Corpus uses two model tiers deliberately:

| Task | Model tier | Rationale |
|---|---|---|
| Bulk ingest, collector runs, fact-checking | Cheaper (Sonnet-class) | High volume; accuracy over depth |
| Interactive sessions, weekly synthesis, hard sources | Stronger (Opus-class) | Nuanced reasoning; used sparingly |
| Gardener (stub-filler) | Split within one task: strong model writes, cheap model fact-checks | Best output per unit of strong-model budget |

This split protects the weekly Opus quota. The nightly jobs run exclusively on the cheaper tier; the stronger model is reserved for work where depth genuinely matters.

---

## Subscription Auth vs. API Billing

The unattended jobs strip the metered API key from the environment before invoking the agent. This means the work bills the flat-rate subscription rather than per-token API charges.

Why that matters: a nightly job that ingests 50 sources could easily consume thousands of tokens across dozens of file reads and writes. On per-token billing that cost is variable and hard to forecast. On the subscription it is effectively prepaid — the unattended pipeline becomes a way of getting value from capacity that would otherwise go unused overnight.

!!! warning "This only works with headless agent invocation"
    The subscription path requires the agent CLI to be invoked with the metered API key **removed from the environment**. If a billable API key is present, the session bills per-token instead of against the subscription.

---

## Claim Lifecycle

The schema tracks claims over time, not just at the moment of ingestion:

- When a corroborating source is re-ingested, `last_confirmed` is refreshed.
- When a newer source contradicts an existing claim, `confidence` is lowered until the conflict is resolved.
- When information is superseded, the old page is kept as a stub with `superseded_by:` pointing forward — history stays auditable.
- When two sources genuinely disagree and neither is clearly wrong, a `synthesis` page is created naming the disagreement rather than silently picking one side.

This makes the corpus an *auditable* record, not just a compressed summary.

---

Next: [Collectors](collectors.md) — how each intake channel works.

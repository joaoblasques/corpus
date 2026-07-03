# CLAUDE.md — LLM Corpus Schema (v2.0)

Personal knowledge corpus (Karpathy LLM-Wiki pattern). **Read this file fully before any operation**, then read `corpus/index.md`, `corpus/_domains.md`, `corpus/_config.md`.

---

## 0. Operating autonomy

Autonomous operation delegated (2026-06-16). Choose the recommended option, state it in one line, proceed — do not ask for approval. Drive arcs to completion; report decisions + what's next. Routine actions (commits, PRs, merges, schema bumps, pushing main) pre-authorized.

**Pause only for:** irreversible/destructive with no recovery · discovery that contradicts task assumptions · real-consequence decision with no defensible default.

---

## 1. Your role

Ingest raw sources → route into self-organizing corpus pages → maintain cross-references and indexes → answer queries. **User owns sources/queries; you own `corpus/`.** Never modify source files except the three stamp fields (§2). Never write outside `corpus/` except as §2 permits. Compounding knowledge base — every ingest/query should enrich it.

---

## 2. Architecture (strict path isolation)

| Layer | Path | Your access |
|---|---|---|
| Raw sources (no PARA home) | `raw/matter/` · `raw/youtube/` · `raw/web/` · `raw/notes/` · `raw/_inbox/` | Read-only + stamp exception |
| PARA-native sources | Listed in `corpus/_config.md` | Read + stamp in place; never copy to `raw/` |
| Your output | `corpus/` (`index.md`, `log.md`, `_config.md`, `_domains.md`, `<domain>/README.md`, `<domain>/<page>.md`, `<domain>/sources/<slug>.md`) | Full ownership |
| Schema | `CLAUDE.md` | Co-evolve with user |

**Write exceptions** (only these, nothing else outside `corpus/`):
- **Stamp**: after ingest, add/update exactly `corpus_ingested: true`, `corpus_ingested_at: YYYY-MM-DD`, `corpus_pages: [...]` on the source file. No body edits, no other fields, no renames.
- **Inbox move**: after Branch A ingest, move (not copy) file from `raw/_inbox/` to `raw/<channel>/`.
- **Vault removal**: `collect-obsidian` reaper only — delete vault note after its raw source is `corpus_ingested`. Gated on stamp; stages `git rm`, never commits vault. Recoverable from vault git history.

Query results worth keeping → corpus page only; never write to `01_Projects/`, `02_Areas/`, or vault.

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

**OKF conformance (v0.1):** `type` is the **OKF-required** field — every page must have a non-empty value. `title`, `description`, `resource`, `tags`, `timestamp` are OKF-recommended-optional (add where cheap; absence is legal). All other fields above (`domain`, `status`, `sources`, `aliases`, `confidence`, `supersedes`, etc.) are OKF-legal producer extensions — preserved on round-trip by any conformant consumer.

**`sources` migration note**: existing pages use the old flat `- raw/<path>` format. Migrate to the structured form when you next touch the page (re-ingest, update, lint). Do not mass-update all pages in one pass without user approval.

---

## 5. Naming conventions

- **Files**: `kebab-case.md`. ASCII only. No spaces, no special chars.
- **Domain slugs**: short, lowercase, no qualifiers (`ai-engineering`, not `the-ai-engineering-domain`).
- **Entity slugs**: canonical name (`anthropic.md`, `claude-code.md`).
- **Concept slugs**: noun phrase (`context-engineering.md`).

---

## 6. Linking

Cross-links are plain markdown links using bundle-root-relative absolute paths: `[Display](/<domain>/<page>.md)`. Do NOT use `[[wikilinks]]`. Links are untyped edges — express the relationship type in prose (§7.1). Broken links are tolerated (a link may point to not-yet-written knowledge).

For source citations, use footnote format with plain markdown links (sources live outside the OKF bundle — tolerated as external references):
- Raw-channel: `[^src1]: [source title](../../raw/<channel>/<file>.md)` (relative from corpus page)
- PARA-native: `[^src1]: [source title](../../../03_Resources/<subfolder>/<file>.md)` (relative from corpus page)

The `sources:` frontmatter `path:` field stores the vault-relative path only (no link syntax):
```
# PARA-native: path: 03_Resources/Articles/foo.md
# Raw-channel: path: raw/web/bar.md
```

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

### 7.1 Claim lifecycle

- `last_confirmed` + `confidence` (0–1) on pages: corroborating re-ingest refreshes `last_confirmed`; conflicting evidence lowers `confidence`.
- **Supersession over deletion**: new info replaces old → set `superseded_by` on old, `supersedes` on new, keep stale stub with forward link.
- **Contradiction on write**: conflict detected during ingest → prefer higher-authority/more-recent claim; if unsettled → synthesis page (§7), not silent pick.
- **Typed relationships**: capture link type in prose (`uses`, `depends-on`, `supersedes`, `contradicts`, `caused`, `fixed`).

---

## 8. Operations

### 8.1 Ingest

**Branch routing** (Step 0 — decide before reading):

| Source | Branch | Rule |
|---|---|---|
| `raw/_inbox/` | A | Process then move to `raw/<channel>/` |
| Path in `corpus/_config.md` PARA-native list | B | In-place; check `corpus_ingested` first — if present → STOP (§9 collision) |
| Already in `raw/<channel>/` | C | In-place, no move |

**Per-source steps** (single source):
1. Read fully → identify domain (existing `_domains.md` first, then tags, then content). Default: route to existing.
2. Extract 3–10 entities/concepts. For each: find existing page (grep aliases) → update, or create stub.
3. Write source-summary page only if >1000w AND synthetically rich.
4. Update `corpus/index.md`. Append to `corpus/log.md` (`## YYYY-MM-DD` date group + `* **Ingest**: …` bullet with source/channel/domain/pages).
5. Stamp source: `corpus_ingested: true`, `corpus_ingested_at: <today>`, `corpus_pages: [...]`.
6. Branch A only: move file to `raw/<channel>/`.

**Batch ingest (N>10) — cluster pipeline** (Coordinator + parallel Workers):

| Phase | Owner | What |
|---|---|---|
| 0 Pre-flight | Coordinator | Re-read CLAUDE.md + index/domains/config. Check stamps/collisions → skip/force/append list. |
| 1 Survey & cluster | Coordinator | Title+tags+¶1 per source (no full reads). Cluster thematically → route to existing domains (default); ≥3 distinct sources with no fit → propose new domain (confirm first); 1–2 sources → provisional; <3 no fit → fold as pages. Surface cluster→domain map for confirmation. |
| 2 Entity registry | Coordinator | Extract 3–10 candidates/source. Dedup against `index.md` + across clusters by name/alias. Build `{slug → aliases, domain, path}` registry before any writes. |
| 3 Per-cluster ingest | Workers (one/domain, parallel) | Read full bodies. Create/update pages via registry (no dupes). Citation gate every claim (§7). Target 10–15 page cascade. Link new pages from domain hub — no orphans. Workers return deltas; never write shared files. |
| 4 Integrate | Coordinator | Stamps, `index.md` update, `log.md` append, inbox moves — all serialized. |
| 5 Verify | Coordinator | Lint scoped to touched domains (orphans, dupes, contradictions, stubs, domain health). Apply safe fixes; surface rest. |

**Coordinator-owns-shared-files:** only Coordinator writes `index.md`, `log.md`, `_domains.md`, `_config.md`. Workers own disjoint domains.

### 8.2 Query (`/query`)

Driven by `query` skill + `bin/query.py`. Steps:
1. Read `index.md` → select candidate pages by topic/aliases → read them.
2. **Coverage gate**: fully covered → answer from corpus only (read-only, no log).
3. Answer with inline citations (§7). Never present model knowledge as corpus claim.
4. **Gap top-up**: thin/missing → WebSearch up to 3 URLs → `bin/query.py fetch-and-queue`. Label fetched claims `[fresh — not yet in corpus]`. Auto-queue to `raw/_inbox/` (channel `web`/`youtube`, `via_query`), deduped by `source_url`. Fetch failure → state plainly, nothing fabricated.
5. Log gap to `log.md` via `bin/query.py log-gap`.
6. Offer synthesis file-back when answer drew on 2+ pages or kept web top-up. Write only on approval.

### 8.3 Lint

**Triggered by**: "lint" (full) or "lint `<domain>`" (scoped). Check in order, output report, apply fixes only with approval:

| Check | Action |
|---|---|
| Orphan pages (0 inbound hub links) | Link or flag for archive |
| Stubs >14 days old | Flag for expansion or archive |
| Duplicate entities (alias overlap) | Propose merge |
| Contradictions between pages | Create/update synthesis page |
| Implicit concepts (3+ page references, no own page) | Propose creation |
| Stale claims (newer source contradicts) | Update with citation |
| Domain health (<3 pages, >30 days) | Propose merge into sibling |
| Provisional domains (>30 days, <3 sources) | Propose merge or removal |
| Topic-mixed pages | Propose split |

### 8.4 Schema update

If a rule repeatedly causes problems, surface it. User updates the file; bump version + log entry.

---

## 9. Emergent structure rules (anti-drift)

**Create a new domain only if:**
- Standard: 3+ sources don't fit any existing domain AND conceptually distinct AND checked `_domains.md`.
- Provisional: 1–2 sources + user confirms growth expected → mark `provisional: true` in `_domains.md`.
- **Always confirm with user before creating the first new domain in a session.**
- Provisional domains: lint review at 30 days — if <3 sources, propose merge or removal.

**Do NOT create a domain if:** sources fit an existing domain (even imperfectly) · candidate has <3 pages · it's a sub-topic (→ page instead) · it's an entity/product (→ entity page).

**Consolidation triggers (lint):** >30% entity overlap between two domains · domain <3 pages for >30 days · all pages are sub-topics of one concept → propose merge/fold.

**Split triggers:** >50 pages with a clear sub-cluster of >15 · user requests.

**Domain-change protocol:** always log creation/merge/split to `corpus/_domains.md` with rationale + date.

**PARA-native collision rule:** Branch B — read frontmatter before ingesting. If `corpus_ingested: true` → **STOP**, surface: "Ingested `<corpus_ingested_at>`, produced `<corpus_pages>`. Re-ingest? skip (default) / force-update / append-only." Apply even for bulk "ingest everything" commands — enumerate collisions first. Default: skip. `corpus_ingested_at` = most recent op only; `log.md` is full history.

---

## 10. Source-channel specifics

See [docs/source-channels.md](docs/source-channels.md).

---

## 11. Index file format + OKF conformance

OKF reserved file: `corpus/index.md`. Bundle root carries `okf_version: "0.1"` in frontmatter. Body: `# Section` headings + `* [Title](/path.md) - desc` bullets (root-relative links, no wikilinks).

**The corpus is a Google OKF v0.1 bundle** ([spec](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)). Validate with `python3 bin/okf_lint.py`. Three conformance rules: (1) every non-reserved `.md` has parseable YAML frontmatter; (2) every frontmatter has a non-empty `type`; (3) reserved files follow the `index.md`/`log.md` format when present.

See [docs/file-formats.md](docs/file-formats.md) for full format spec.

---

## 12. Log file format

OKF reserved file: `corpus/log.md`. Newest-first. `## YYYY-MM-DD` date-group headings. Entries: `* **Op**: …` bullets (op types: `Ingest`, `Schema`, `Config`, `Query`, `Lint`, `Domain`).

See [docs/file-formats.md](docs/file-formats.md) for full format spec.

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

Current: v2.0. Full history → [docs/changelog.md](docs/changelog.md).

Co-evolve with user. Bump version + log entry on every change.

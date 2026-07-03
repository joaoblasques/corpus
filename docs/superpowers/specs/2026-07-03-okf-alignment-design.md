# OKF alignment — making the corpus an Open Knowledge Format v0.1 bundle

> Date: 2026-07-03 · Status: approved (brainstorm) · Repo: corpus

## Problem / goal

Make `corpus/` a **conformant Google OKF v0.1 bundle** so the knowledge is **transferable to
others and follows a published standard** — importable by any OKF-aware tool/agent without a
translation layer, and forward-compatible as the standard evolves.

OKF ([Google Cloud, v0.1 Draft, 2026-06-12](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md);
[annotated](https://okf.md/spec/); [FAQ](https://okf.md/faq/)) **formalizes Karpathy's LLM-wiki
pattern** — the exact pattern this corpus is built on. So this is an **alignment, not a rewrite**.

## OKF v0.1 — the normative rules we must satisfy

Verified against the canonical `SPEC.md`:

- **Bundle** = a directory tree of UTF-8 markdown files. Structure is domain-independent. Best
  distributed as a git repo.
- **Concept doc** = one `.md` = one concept: YAML frontmatter (`---`) + free-form markdown body.
  **Concept ID = file path minus `.md`** (`ai-engineering/anthropic.md` → `ai-engineering/anthropic`).
- **Required frontmatter: exactly one field — `type`** (non-empty free-form string).
- **Recommended-optional:** `title`, `description`, `resource` (a URI for the underlying asset),
  `tags` (list), `timestamp` (ISO-8601). Producers **MAY add any extra keys**; consumers **MUST
  preserve unknown keys** and **MUST NOT reject** unknown fields → all our rich fields are legal.
- **Reserved filenames — exactly two:** `index.md` and `log.md` (allowed at any directory level).
  All other `.md` are concept docs.
  - `index.md`: **no frontmatter, except the bundle-root `index.md` which MAY carry
    `okf_version: "0.1"`**. Body = one or more `# Section` headings, each a bullet list
    `* [Title](/path.md) - short description`.
  - `log.md`: **newest-first**, `## YYYY-MM-DD` date-group headings, entries are prose with an
    optional bold lead word (`**Update**`, `**Creation**`, …).
- **Cross-links = plain markdown links, NOT `[[wikilinks]]`.** Recommended form: bundle-root-
  relative absolute path — `[Anthropic](/ai-engineering/anthropic.md)`. Relative allowed. Links
  are **untyped edges** (relationship in prose). **Consumers MUST tolerate broken links.**
- **Conformance = 3 rules:** (1) every non-reserved `.md` has parseable YAML frontmatter; (2)
  every frontmatter has a non-empty `type`; (3) reserved files follow the `index.md`/`log.md`
  format when present. *"If it has frontmatter with type, it's valid OKF. Full stop."*
- **Versioning:** `<major>.<minor>`; `okf_version: "0.1"` declared only in the root `index.md`.

**Caveat:** OKF is a **v0.1 Draft explicitly designed to evolve** — field names/rules may shift
in minor bumps. We pin to `0.1` and keep the conformance guard so drift is caught.

## Current state — the corpus is already ~90% OKF

| Corpus today | OKF | Status |
|---|---|---|
| 745 concept `.md`, YAML + `type: hub\|entity\|concept\|synthesis\|source` | concept docs need `type` | ✅ **all 745 already have `type`** — the one hard rule is already met |
| rich frontmatter (`confidence`, `aliases`, `sources[]`, `supersedes`…) | extra keys allowed & preserved | ✅ legal extensions, no change |
| typed relations expressed in prose (§7.1) | untyped links + prose | ✅ already aligned |
| `corpus/_index.md` (single root catalog) | `index.md` reserved | ⚠️ rename + add `okf_version` |
| `corpus/_log.md` (oldest-first, `## [YYYY-MM-DD HH:MM] op \| subj`) | `log.md` newest-first, `## YYYY-MM-DD` groups | ⚠️ rename + reorder + regroup |
| `corpus/_config.md`, `corpus/_domains.md` | non-reserved → need `type` | ⚠️ add `type` (keep in place) |
| **4,293 `[[wikilinks]]` across 324 files** | plain markdown root-relative links | ⚠️ **the main migration** |
| provenance footnotes → `../../raw/…` (outside bundle) | broken links tolerated | ✅ ok; also add `resource:` |

**Bundle boundary:** the OKF bundle is **`corpus/`**. `raw/` (sources) and `bin/` (tooling) are
outside it.

## Decisions (resolved)

1. **`_config.md` / `_domains.md`:** **keep them in `corpus/` and give each a `type`** (`type:
   okf-config`, `type: domain-registry`). *(Reversed from the initial "move them out" rec after
   reading the exact spec: moving them breaks the many tooling paths that read
   `corpus/_config.md` / `corpus/_domains.md` for marginal benefit. Tagging them makes `corpus/`
   directly conformant with zero path changes; a consumer can filter them by type. A pristine
   export that drops them can be a later phase.)*
2. **Provenance:** keep the footnote citations (tolerated as external/broken links per OKF) **and**
   populate a per-page **`resource:`** field with the page's canonical source URL where one exists
   — the OKF-recommended field; makes pages self-describing and consumer-portable.
3. **Scope:** **one clean cutover** — schema update + migration script + conformance validator land
   together, so the corpus is conformant immediately and stays conformant.

## Target formats (exact)

**Concept doc frontmatter** (existing fields kept as extensions; `type` already present):
```yaml
---
type: entity            # REQUIRED (already present on all pages)
title: Anthropic        # recommended (add from H1/slug if missing)
description: ...         # recommended (from TL;DR first line)
resource: https://...    # recommended — canonical source URL when known
tags: [corpus/ai-engineering, entity]   # existing
timestamp: 2026-07-03    # recommended — map from existing `updated`
# --- existing rich extensions (all OKF-legal, unchanged) ---
domain: ai-engineering
status: mature
sources: [...]
aliases: [...]
confidence: 0.8
last_confirmed: 2026-07-01
---
```

**Root `corpus/index.md`:**
```yaml
---
okf_version: "0.1"
---
```
```markdown
# ai-engineering
* [Anthropic](/ai-engineering/anthropic.md) - AI safety company behind Claude
...
```

**`corpus/log.md`** (newest-first; regrouped by date):
```markdown
# Corpus Log
## 2026-07-03
* **Ingest**: ...
* **Schema**: OKF v0.1 alignment (see §schema)
## 2026-07-02
* ...
```

**Links:** `[[ai-engineering/anthropic|Anthropic]]` → `[Anthropic](/ai-engineering/anthropic.md)`.

## Architecture — phased plan

**Phase 1 — Schema (`CLAUDE.md` → v2.0, OKF-aligned).** Rewrite §5/§6/§11/§12 and frontmatter
guidance so the corpus **authors OKF by default**: reserved `index.md`/`log.md`; plain-markdown
root-relative links (retire wikilinks); `type` is the load-bearing required field; recommended
fields `title/description/resource/tags/timestamp`; log is newest-first `## YYYY-MM-DD`; note all
existing rich fields are OKF extensions. Add an "OKF conformance" section pointing at the
validator. Bump version; log a `schema` entry.

**Phase 2 — Migration script (`bin/okf_migrate.py`, reversible, one commit).**
- Rename `_index.md`→`index.md` (add root `okf_version: "0.1"` frontmatter; rewrite its bullet
  links to root-relative `/path.md`); `_log.md`→`log.md` (reverse to newest-first, regroup under
  `## YYYY-MM-DD`, preserving all entries).
- Add `type: okf-config` / `type: domain-registry` frontmatter to `_config.md` / `_domains.md`
  (kept in place; also rename-free — they're not reserved names).
- **Rewrite all 4,293 wikilinks** `[[<path>|<text>]]` / `[[<path>]]` → `[<text>](/<path>.md)`
  across the 324 files. Resolve `<path>` to a bundle-root-relative path; where a wikilink omits
  the domain, resolve via the index/aliases. Log any unresolved links (OKF tolerates broken, but
  we record them for cleanup).
- Backfill recommended fields where cheap: `title` (from H1), `timestamp` (from existing
  `updated`), `resource` (from the first `sources[].path`/URL when it's a URL).
- Idempotent + `--dry-run`; emits a report (files touched, links rewritten, unresolved).

**Phase 3 — Tooling emits OKF.** Update writers so new output is born conformant:
`bin/quick_ingest_youtube.py`, `bin/quick_ingest_docs.py` (`_index_append` → root-relative links
+ write to `index.md`), the ingest path, and `bin/scheduled_run.py` (log writer → newest-first
`## YYYY-MM-DD`; run-report lines become log entries). Reference `_index.md`/`_log.md` paths across
`bin/` updated to `index.md`/`log.md`.

**Phase 4 — Conformance guard (`bin/okf_lint.py`).** Implements the 3 rules over `corpus/`:
every non-reserved `.md` has parseable frontmatter; non-empty `type`; `index.md`/`log.md` shape.
Reports (does not delete). Wire into `bin/corpus_lint.py` + the nightly run report. Optionally
cross-check against the third-party Rust validator ([W4G1/okf](https://github.com/W4G1/okf)) as an
independent conformance signal.

**Phase 5 — Transferability proof.** Add a bundle-root `README.md`/`okf.md` note declaring OKF
v0.1 conformance; export a `corpus/`-only copy and load it in the OKF reference visualizer
(GoogleCloudPlatform/knowledge-catalog) to prove portability. Record the result in the log.

## The wikilink rewrite (the crux)

Correctness matters most here (4,293 edits). Rules for `bin/okf_migrate.py`:
- `[[<domain>/<page>|Display]]` → `[Display](/<domain>/<page>.md)`.
- `[[<domain>/<page>]]` → `[<page-as-title>](/<domain>/<page>.md)`.
- Bare `[[<page>]]` (no domain): resolve to a full path via the index (`corpus/_index.md`) /
  filename search / aliases; if ambiguous or unresolved, leave a plain-text `Display` + record it
  in the report (OKF tolerates a missing link, but we prefer a resolved one).
- Never rewrite links already in markdown form. Preserve footnote-definition links (`[^src1]: …`)
  as-is (they point outside the bundle; tolerated).
- Verify with a round-trip test on a sample and a post-run count (`grep -c '\[\['` must reach 0
  except inside fenced code examples, which are skipped).

## Testing

- `bin/okf_migrate.py`: unit tests for each wikilink form (piped, unpiped, bare, ambiguous,
  code-fence skip), the log reorder (oldest→newest, date regroup, no entry loss), the `_index`→
  `index` link rewrite + `okf_version` stamp, and idempotency.
- `bin/okf_lint.py`: a conformant fixture passes; fixtures that (a) miss frontmatter, (b) have an
  empty `type`, (c) malformed `index.md`/`log.md` each fail with a precise message; and a bundle
  with broken links / unknown keys / missing optional fields **passes** (tolerance rules).
- Post-migration: `okf_lint` reports 0 violations over the real `corpus/`; `grep -rc '\[\['`
  outside code fences = 0.

## Risks / open items

1. **v0.1 is a Draft** — pin `okf_version: "0.1"`; the validator + a `schema` log entry make a
   future minor-bump re-alignment cheap.
2. **4,293-link rewrite** is the highest-risk step — mitigated by TDD on the rewriter, `--dry-run`
   + report, unresolved-link logging, and the post-run grep gate. Runs as one reviewable commit.
3. **Two-writer safety:** migration + tooling changes touch `corpus/` and `bin/` — run from this
   code session; the vault is untouched.
4. **`resource` backfill** is best-effort (only where a source URL exists); absence is OKF-legal.

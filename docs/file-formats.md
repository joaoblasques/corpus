# File formats

## 11. Index file format (`corpus/index.md`)

OKF reserved file. Single source of catalog truth. Update on **every ingest**. Do not let it drift.

Bundle-root `corpus/index.md` carries `okf_version: "0.1"` frontmatter. Subdirectory `index.md` files (if any) carry no frontmatter. Body: one or more `# Section` headings, each followed by a bullet list using bundle-root-relative markdown links.

```yaml
---
okf_version: "0.1"
---
```

```markdown
# Corpus Index

> Last updated: YYYY-MM-DD | Total pages: N | Total sources: M

This file is auto-maintained by Claude. Do not edit by hand.

## Domains

### <domain-slug>
- [Page Title](/<domain>/<page>.md) — type · status · one-line summary
- ...

### <domain-slug-2>
- ...

## Recent additions
- YYYY-MM-DD: [Page Title](/<domain>/<page>.md) (new)
- YYYY-MM-DD: [Page Title](/<domain>/<page>.md) (updated, +N sources)
```

---

## 12. Log file format (`corpus/log.md`)

OKF reserved file. Newest-first, grouped by date. Update on every ingest/operation.

```markdown
# Corpus Log

## YYYY-MM-DD
* **Ingest**: <title> — <domain>, N pages touched, N new
* **Schema**: <description>
* **Config**: <description>

## YYYY-MM-DD
* **Query**: <question summary> — gap logged
* **Lint**: <domain> — N issues found, N applied
* **Domain**: <action> — <rationale>
```

Op types: `Ingest`, `Schema`, `Config`, `Query`, `Lint`, `Domain`.

- `Config` — changes to `corpus/_config.md`: PARA-native path additions, stamp field spec adjustments.

---

## Corpus page frontmatter (every page)

*(Full block moved from CLAUDE.md §4, fourth compression pass, Thrift #queued.)*

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
consolidates:                # optional (v2.1), synthesis pages only: member source-page paths consolidated
consolidated_into:            # optional (v2.1), source pages only: path of synthesis that consolidated it (member is KEPT, not deleted)
---
```

`aliases` is critical for entity dedup — always populate when you know variants ("GPT-4", "gpt4", "GPT 4"). Claim-lifecycle fields (`confidence`, `last_confirmed`, `supersedes`, `superseded_by`) are managed per CLAUDE.md §7.1.

**OKF conformance (v0.1):** `type` is the **OKF-required** field — every page must have a non-empty value. `title`, `description`, `resource`, `tags`, `timestamp` are OKF-recommended-optional (add where cheap; absence is legal). All other fields above (`domain`, `status`, `sources`, `aliases`, `confidence`, `supersedes`, etc.) are OKF-legal producer extensions — preserved on round-trip by any conformant consumer.

**`sources` migration note**: existing pages use the old flat `- raw/<path>` format. Migrate to the structured form when you next touch the page (re-ingest, update, lint). Do not mass-update all pages in one pass without user approval.

## Citation link formats

Cross-links between corpus pages: bundle-root-relative absolute markdown paths, `[Display](/<domain>/<page>.md)`. No `[[wikilinks]]`.

Source citations (sources live outside the OKF bundle — tolerated as external references), footnote format:
- Raw-channel: `[^src1]: [source title](../../raw/<channel>/<file>.md)` (relative from corpus page)
- PARA-native: `[^src1]: [source title](../../../03_Resources/<subfolder>/<file>.md)` (relative from corpus page)

The `sources:` frontmatter `path:` field stores the vault-relative path only (no link syntax):
```
# PARA-native: path: 03_Resources/Articles/foo.md
# Raw-channel: path: raw/web/bar.md
```

Inline citation example:
```markdown
Self-attention scales quadratically with context length [^src1].

[^src1]: [Attention is All You Need](../../raw/web/attention-is-all-you-need.md)
```

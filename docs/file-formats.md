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

## §4 frontmatter — externalized detail

*(Moved from CLAUDE.md §4, third compression pass, Thrift #8.)*

**OKF conformance (v0.1):** `type` is the **OKF-required** field — every page must have a non-empty value. `title`, `description`, `resource`, `tags`, `timestamp` are OKF-recommended-optional (add where cheap; absence is legal). All other CLAUDE.md §4 fields (`domain`, `status`, `sources`, `aliases`, `confidence`, `supersedes`, etc.) are OKF-legal producer extensions — preserved on round-trip by any conformant consumer.

**`sources` migration note**: existing pages use the old flat `- raw/<path>` format. Migrate to the structured form when you next touch the page (re-ingest, update, lint). Do not mass-update all pages in one pass without user approval.

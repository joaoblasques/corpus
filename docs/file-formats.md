# File formats

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

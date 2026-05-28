---
type: config
created: 2026-05-20
updated: 2026-05-20
---

# Corpus Config

Operational configuration for the LLM corpus system. Schema-level rules live in `CLAUDE.md`; this file is the data that those rules operate on.

---

## PARA-native ingest paths

Sources found under these paths are ingested **in place** — stamped with wiki metadata but **never copied to `raw/`**. These are the user's canonical notes with a permanent vault home.

| Path | Channel label | Notes |
|---|---|---|
| `03_Resources/Articles/` | `notes` | Obsidian Web Clipper saves, Matter exports already filed in vault, curated article notes |
| `03_Resources/Study Notes/` | `notes` | First-party study notes, course summaries, lecture notes |

All other sources arrive via `raw/_inbox/` (then routed to `raw/<channel>/`) or are dropped directly into a `raw/<channel>/` subfolder. `raw/notes/` is reserved for first-party notes that have no canonical PARA home (edge case / legacy).

**To add a path**: edit this table and append a `config | <change>` log entry to `corpus/_log.md`.

---

## Source file stamp fields

When any source is ingested, exactly these three frontmatter fields are written to the source file. No other edits to source files are permitted.

```yaml
corpus_ingested: true
corpus_ingested_at: YYYY-MM-DD   # most recent ingest date — updated on every successful ingest
corpus_pages:                     # accumulates; append new pages, never remove
  - corpus/<domain>/<page>.md
```

Rules:
- `corpus_pages` accumulates over time — append, never remove.
- `corpus_ingested_at` updates on every successful ingest (first or re-ingest). Full history is in `corpus/_log.md`.
- These are the **only** frontmatter fields you may add to source files. No other edits to source files are permitted.

---

## Channel labels (reference)

| Label | Raw path | PARA path |
|---|---|---|
| `matter` | `raw/matter/` | — |
| `youtube` | `raw/youtube/` | — |
| `web` | `raw/web/` | — |
| `notes` | `raw/notes/` (no PARA home) | `03_Resources/Articles/`, `03_Resources/Study Notes/` |
| `inbox` | `raw/_inbox/` (transient) | — |

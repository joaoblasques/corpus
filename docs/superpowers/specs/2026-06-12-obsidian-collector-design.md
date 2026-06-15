# Spec: `collect-obsidian` — Obsidian vault → corpus source collector

- **Date:** 2026-06-12
- **Status:** approved design (pre-implementation)
- **Sub-project:** collection layer — collector #3 (after `collect-email`, `collect-youtube`)
- **Builds on:** the collect-and-remove pattern of `collect-email`; `bin/fetch_link.py` (article extraction); `collect_email` slugify/frontmatter helpers
- **Author:** brainstormed with user; this doc is the validated design

## Context

The corpus ingests sources from `raw/` into a synthesized knowledge base. The user keeps a large Obsidian "second brain" vault at `/Users/jonasblasques/Dev/second-brain/` (a sibling git repo). This collector pulls **reference-layer** notes from that vault into the corpus pipeline and — per the user's requirement — **removes** each note from the vault once its knowledge is durably in the corpus. Unlike the existing PARA-native in-place ingest (CLAUDE.md §8.1 Branch B), which reads + stamps vault notes without moving them, this collector follows the **collect-and-remove** model of `collect-email`: copy the content into `raw/`, ingest it, then delete the vault original.

## Goals

1. Discover ingest-worthy notes in the configured vault paths and copy each into `raw/_inbox/` (channel `notes`) as a durable, corpus-cited source carrying its `vault_origin` path.
2. For URL-list notes (`articles to process.md`, `TO SCRAPE.md`), fetch each linked article's content (via `fetch_link.py`) and write each as its own `raw/_inbox/` source.
3. After a source is confirmed `corpus_ingested`, **remove** its origin from the vault (delete a note via `git rm`; strike a processed URL from the list and append it to `articles_processed.md`).
4. Idempotent + safe: never re-collect already-collected notes; never delete anything not yet `corpus_ingested`; every removal recoverable from vault git history; `--dry-run` deletes nothing.

## Non-goals (v1)

- `03_Resources/llm-wiki-system` (a literal copy of the corpus) — deferred to a separate, careful reconciliation task; **excluded** here to avoid duplicating the corpus into itself.
- `01_Projects`, `04_Archive`, `02_Areas`, the rest of `00_Inbox` — ephemeral/actionable, not reference knowledge.
- Vault reorganization, two-way sync, link-graph rewriting, binary/PDF ingestion.
- Re-citing/removing the **21 notes already ingested PARA-native** (they keep their vault-path citations and are left in place).

## Scope (paths)

**Vault root:** `/Users/jonasblasques/Dev/second-brain` (configured in `corpus/_config.md`).

**Include:**
- `03_Resources/Articles/`, `03_Resources/Books/`, `03_Resources/Study Notes/`, `03_Resources/Snippets/`, `03_Resources/Prompt Templates/`
- `00_Inbox/Clippings/` — all markdown content notes (clips + the `scrape/` subfolder), plus URL-list files processed as link sources.

**Exclude:**
- `03_Resources/llm-wiki-system/`, `01_Projects/`, `02_Areas/`, `04_Archive/`, the rest of `00_Inbox/`, `node_modules/`, `05_Attachments/`, `06_Metadata/`, `.obsidian/`, `.git/`.
- Non-knowledge files: `*_processed.md` (used as dedup ledgers, not ingested), `*.pdf`/binaries, `README.md`.
- Any note already `corpus_ingested: true` (already in the corpus) OR already collected (its `vault_origin` already present in a `raw/` source).

## Architecture — 4 phases

1. **Discover** — walk include paths, apply exclude filters, drop already-collected/already-ingested. Classify each candidate as a `note` (regular markdown) or a `url-list` (`articles to process.md`, `TO SCRAPE.md`).
2. **Collect** —
   - `note`: copy its body into `raw/_inbox/notes-<slug>.md` with frontmatter `channel: notes`, `vault_origin: <vault-relative path>`, `title`, `tags` (carried from the note), `collected_at`. Original markdown body preserved verbatim.
   - `url-list`: parse URLs; for each not already in `articles_processed.md` or already fetched, `fetch_link.fetch(url)` → write `raw/_inbox/web-<slug>.md` (channel `web`, `source_url`, `via_vault_list: <list path>`). Auth-walled fetch failures (LinkedIn/x.com) are recorded and the URL is left in the list.
3. **Ingest** — the existing v0.6 Branch-A batch ingest turns `raw/_inbox/` → corpus pages and stamps each raw source `corpus_ingested` (+ `corpus_pages`). (Run separately; not part of this collector.)
4. **Reap** (`reap` subcommand) — for each `raw/` source that is now `corpus_ingested` and carries a `vault_origin`/`via_vault_list`: delete the vault note (`git rm` in the vault), or strike the processed URL from `articles to process.md` and append it to `articles_processed.md`. Skips anything not yet `corpus_ingested`. `--dry-run` previews.

## Components

| File | Responsibility | Network | Tested |
|---|---|---|---|
| `bin/collect_obsidian.py` *(new)* | Deterministic core: `discover` (walk+filter+classify), `build_note_source`/`build_url_source` (frontmatter+slug, reuses collect_email helpers), `parse_url_list`, dedup (`already_collected_vault`, URL seen-set), and the reaper selector (`reapable` → list of vault paths / URLs to remove from `corpus_ingested` raw sources). | no (fetch via fetch_link) | pytest |
| `bin/obsidian_client.py` *(new, thin)* | I/O + CLI: resolve vault root, copy notes, call `fetch_link` for URLs, and `reap` (vault `git rm`, list-file edits). Subcommands `collect` (`--dry-run`, `--max`, `--path`), `reap` (`--dry-run`). | yes (git, fetch) | pytest (mock fetch/git) |
| `.claude/skills/collect-obsidian/SKILL.md` *(new)* | Drives `collect` → (corpus ingest) → `reap`. Safety rules. | — | — |
| `corpus/_config.md` *(modify)* | Add `vault_root`, the include/exclude path lists, and a `notes` (vault) collection note. | — | — |
| `CLAUDE.md` *(modify → v0.7)* | Narrow **vault-removal exception**. | — | — |

## CLAUDE.md v0.7 — vault-removal exception

Add to §2 (alongside the stamp + inbox-move exceptions): *after a vault source file's content has been collected into `raw/` and that raw source is confirmed `corpus_ingested`, the `collect-obsidian` reaper may delete the original vault note (or strike a processed URL from a vault list file). This is the only deletion of a source file permitted, applies only to the configured vault paths, and is recoverable from the vault's own git history.* Update §13 failure-mode list accordingly. Bump version + log entry.

## Safety

- **Deletion is gated**: reap removes a vault origin only when its raw source is `corpus_ingested`. Discovery/collect never delete.
- **`--dry-run`** on both `collect` and `reap` performs no writes/deletes.
- **Git-recoverable**: the vault is a git repo; every removal is a `git rm` recoverable from history. (The reaper does NOT `git commit` the vault — it leaves removals staged/unstaged for the user to review and commit.)
- The **21 already-PARA-native notes** are detected (`corpus_ingested: true`) and left untouched — neither re-collected nor removed — preserving their existing vault-path citations.
- Per-note failure never aborts the run; recorded and skipped.

## Dedup / idempotency

- A vault note is skipped if `corpus_ingested: true` (already in corpus) OR its `vault_origin` already appears in a `raw/` source (already collected, awaiting ingest/reap).
- A URL is skipped if present in `articles_processed.md` or already fetched into a `raw/` source (dedup by `source_url`).
- Re-running `collect` only adds newly-appeared notes; re-running `reap` only removes newly-`corpus_ingested` origins.

## Data shapes

Collected note source (`raw/_inbox/notes-<slug>.md`):
```yaml
---
channel: notes
source: obsidian
vault_origin: 03_Resources/Articles/<name>.md
title: <title>
tags: [<carried tags>]
collected_at: 2026-06-12
---
<verbatim note body>
```
Collected URL source (`raw/_inbox/web-<slug>.md`): channel `web`, `source_url`, `via_vault_list`, body = extracted article (reuses `fetch_link` output).

## Testing

- **Pure (no network):** discovery include/exclude matching; note vs url-list classification; `parse_url_list` (extract URLs, ignore prose); `vault_origin` round-trip; dedup (already-ingested, already-collected, processed-URL); `reapable` selection (only `corpus_ingested` sources with an origin). Fixture vault dir under `tmp_path`.
- **Mocked:** `fetch_link.fetch` stubbed; vault `git rm` stubbed; list-file strike/append.
- No live network/git in tests. Existing 85 tests stay green.

## Dependencies

All installed (`httpx`, `trafilatura`, `PyYAML`, git). No new installs. No OAuth (local files).

## Open soft spots (acknowledged)

- **Auth-walled URLs** (LinkedIn, x.com) in `articles to process.md` will fail extraction → recorded, URL left in the list (not struck), surfaced in the report.
- **First collect is large** (~489 resource notes + clips): `collect` discovers all; ingestion + reap drain over multiple v0.6 waves. `--max` caps a run.
- **Reaper does not auto-commit the vault** — the user reviews and commits vault deletions, keeping a human checkpoint on irreversible removal.

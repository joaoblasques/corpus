---
name: collect-obsidian
description: Collect reference-layer notes (and URL-list links) from the user's Obsidian vault into raw/_inbox/, then after they're ingested, remove the originals from the vault. Use when the user wants to pull vault notes into the corpus.
---

# Collect Obsidian

Capture reference-layer notes from the Obsidian vault (`vault_root` in corpus/_config.md)
into `raw/_inbox/` (channel `notes`; URL-list links → channel `web` via fetch_link), then —
after the corpus has ingested them — delete the originals from the vault. Collection only;
never ingest into `corpus/` here.

## Safety rules (non-negotiable)
- `reap` deletes a vault note (or strikes a list URL) ONLY when its raw source is
  `corpus_ingested: true`. Never delete un-ingested content.
- Never touch notes already `corpus_ingested` in the vault (the 21 PARA-native ones) — they
  stay in place with their existing citations.
- `--dry-run` deletes/writes nothing. The reaper STAGES vault deletions (git rm) but does
  NOT commit — the user reviews and commits in the vault.

## Procedure
1. `python3 bin/obsidian_client.py collect --dry-run` — preview discovered notes/URLs. Then
   `collect` (optionally `--max N`, `--path 03_Resources/Articles`).
2. Run the normal corpus Branch-A ingest on `raw/_inbox/` (the v0.6 pipeline) → corpus pages,
   which stamps each raw source `corpus_ingested`.
3. `python3 bin/obsidian_client.py reap --dry-run` — preview removals. Then `reap`.
4. Tell the user to review and commit the vault deletions (`git -C <vault> status`).

## Notes
- Auth-walled URLs (LinkedIn/x.com) in `articles to process.md` fail extraction → recorded,
  URL left in the list.
- llm-wiki-system, 01_Projects, 04_Archive are out of scope (excluded).
- Large first run: collect discovers all ~489 resource notes; ingest + reap drain over waves.

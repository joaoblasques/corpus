# claude-watch — vault-side YouTube deep-analysis layer

**Added:** 2026-06-22 · **Lives in:** the Obsidian vault (claudesidian), not this repo.

## What it is

[claude-watch](https://github.com/taoufik123-collab/claude-watch) is a Claude Code plugin
(`/watch <url>`) that does **per-video deep analysis**: yt-dlp download → ffmpeg scene-change
frames → transcript (native captions, Whisper/Groq fallback) → editorial pacing metrics +
0-10s "hook microscope" → a structured `report.md` that Claude fills in-session.

It is installed in the **vault** environment. Its reports auto-stage into the vault at:

```
00_Inbox/Clippings/youtube_raw/raw/watched/<slug>/report.md
```

(routed via `WATCH_VAULT_DIR`, exported in `~/.zshrc`; Whisper key in `~/.config/watch/.env`).

## How it relates to this corpus's `collect-youtube`

These are **complementary, not competing** — different jobs:

| | corpus `collect-youtube` | vault claude-watch |
|---|---|---|
| Scope | **bulk** — whole playlists | **single** video |
| Transcript | free YouTube captions (`youtube_transcript_api`) + yt-dlp VTT | captions, **+ Whisper/Groq** on audio |
| Visual | none | scene-change frames + hook microscope |
| Output | `raw/_inbox/` (this repo) | vault `00_Inbox/Clippings/youtube_raw/` |
| Driver | OAuth, headless, idempotent | Claude-in-session (frames need an LLM) |

**`collect-youtube` is unchanged by this integration.** No corpus collection behavior was
modified.

## Roadmap (vault-side; tracked in vault `06_Metadata/Plans/2026-06-22-claude-watch-integration-spec.md`)

- **Phase 1 (done):** standalone `/watch` → vault `youtube_raw/`.
- **Phase 2 (done):** corpus-collected videos are auto-queued for claude-watch deep analysis into
  the vault sink. Vault-side deliverables: `.claude/scripts/yt_watch_queue.py` (read-only queue =
  collected − sink), `/yt-deepen [N]` (manual in-session drain), `.claude/scripts/yt_deepen_auto.sh`
  (throttled unattended drain, off by default). Never skips long videos; throttles rate instead.
  Read-only against this repo — no corpus writes.
- **Phase 3:** add a `--deep` mode to the vault's `/yt-batch` routing videos through the engine.
- **Phase 4 (deferred — needs explicit decision):** swap `collect-youtube`'s transcript step to
  claude-watch's `transcribe.py`. Supersedes Phase 2 redundancy and inverts the corpus→vault
  data flow, so it is decided last.

> Note for corpus self-authorship: this doc is a **pointer/reference** only. The vault owns the
> claude-watch integration; the corpus continues to own its own collection pipeline.

---

## Phase 4 (corpus side) — ingest + reap of deep-analysis notes: DONE 2026-06-23

Enabled the corpus to ingest **and** reap the vault's claude-watch deep-analysis `report.md` notes
(sink: `00_Inbox/Clippings/youtube_raw/raw/watched/<slug>/`).

- **Dropped the interim guard** — removed `00_Inbox/Clippings/youtube_raw` from `EXCLUDE_DIRS` in
  `bin/collect_obsidian.py` (was commit `45d6527`). `discover()` (rglob) + `is_included()` now
  surface `youtube_raw/**/report.md`.
- **Folder-aware reap** — `bin/obsidian_client.py` adds `sibling_frames()` + a folder-aware
  `cmd_reap`: reaping a `.../watched/<slug>/report.md` also `git rm`s the sibling `frame_*.jpg`
  (whole-folder reap — no orphan images). Unchanged safety: gated on `corpus_ingested: true`;
  stages `git rm` but **never commits the vault** (Jonas reviews + commits vault deletions). New
  `frames_removed` count in the reap summary. 4 new tests; obsidian/collect suites green (41).
- **Validated one video** (`-h2C65Qd9Mg`, "5 Claude Connectors"): collect `--dry-run` discovers
  the report → ingested (enriched `ai-engineering/claude-cowork` with a cited Connectors section;
  raw source stamped `corpus_ingested: true`, moved to `raw/notes/`) → reap `--dry-run` stages the
  whole `<slug>/` folder (report.md + 5 frames), disk unchanged.
- **No-re-queue gate confirmed:** the durable ledger `~/.config/watch/yt_deepen_done.jsonl` holds
  the video id (`staged_at: backfill`); `yt_watch_queue.py` does not list it. Reaping the sink
  report will not re-trigger analysis.

Left for the vault session (Jonas): run a real `reap` and commit the staged vault deletions when
ready — the ledger gate guarantees no reprocessing.

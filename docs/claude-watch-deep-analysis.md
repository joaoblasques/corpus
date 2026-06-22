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
- **Phase 2:** after `collect-youtube` pulls a playlist, run claude-watch over each collected
  video for richer analysis notes. Accepts the LLM-in-loop cost (analysis needs a Claude
  session per video).
- **Phase 3:** add a `--deep` mode to the vault's `/yt-batch` routing videos through the engine.
- **Phase 4 (deferred — needs explicit decision):** swap `collect-youtube`'s transcript step to
  claude-watch's `transcribe.py`. Supersedes Phase 2 redundancy and inverts the corpus→vault
  data flow, so it is decided last.

> Note for corpus self-authorship: this doc is a **pointer/reference** only. The vault owns the
> claude-watch integration; the corpus continues to own its own collection pipeline.

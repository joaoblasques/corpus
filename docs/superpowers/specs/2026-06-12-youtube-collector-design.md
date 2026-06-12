# Spec: `collect-youtube` — YouTube playlist → corpus source collector

- **Date:** 2026-06-12
- **Status:** approved design (pre-implementation)
- **Sub-project:** collection layer — collector #2 (sibling of `collect-email`)
- **Builds on:** the owned-credential OAuth pattern in `bin/gmail_client.py`; the transcript logic in `bin/fetch_link.py`
- **Author:** brainstormed with user (research-grounded); this doc is the validated design

## Context

The corpus ingests sources from `raw/` into a synthesized knowledge base. The email collector (`collect-email`) captures starred Gmail into `raw/_inbox/`. This adds a second collector for **YouTube playlists**: it captures videos the user has saved into playlists, extracts their transcripts, and deposits normalized markdown into `raw/_inbox/` (channel `youtube`) for later corpus ingestion. For designated "tech" playlists it then removes the collected video from the playlist; other playlists (skateboarding/SkateIQ, music, exercise) are collect-only.

Research (filed inline) established: the YouTube Data API v3 covers read+delete under a single scope (`youtube.force-ssl`); delete requires the **playlistItemId** (not the videoId) and costs 50 quota units (~196 removals/day under the default 10k/day); `youtube_transcript_api` (already installed, used in `fetch_link.py`) is the reliable primary transcript source on a residential IP, with `yt-dlp` as fallback; the official captions API is owner-only and unusable here.

## Goals

1. Collect videos from the user's YouTube playlists into `raw/_inbox/` as normalized markdown (channel `youtube`), one file per video, with the transcript as the body.
2. Per-playlist **policy** — `collect-remove` (tech: capture then remove from playlist), `collect-keep` (capture, never remove), `ignore` — driven by an explicit, safe-by-default config.
3. Remove a collected video from a `collect-remove` playlist **only after** its transcript is durably captured (mirrors the collect-email safety rule).
4. Idempotent: re-runs never double-write (dedup by video ID) and tolerate already-removed items.

## Non-goals (v1)

- Downloading video/audio; summarization (that is corpus-ingest's job).
- "Watch Later" / History playlists (API-inaccessible).
- Comments, subscriptions, or channel-upload sources (only user playlists).
- Removing a video that has **no** transcript (kept + flagged — see policy).

## Components

| File | Responsibility | Network | Tested |
|---|---|---|---|
| `bin/youtube_client.py` *(new)* | OAuth (`youtube.force-ssl`, separate `youtube_token.json`, reuses gmail_client's token/refresh pattern); YouTube Data API calls (list playlists, list items, delete item); the `run` orchestration. Subcommands `auth`, `list-playlists`, `run`. | API | — |
| `bin/collect_youtube.py` *(new)* | Pure core: transcript extraction waterfall + snippet→markdown (dedup/coarsen/strip), dedup-by-video-id, filename, frontmatter, policy resolution. | transcript only | pytest |
| `bin/youtube_playlists.yaml` *(new, gitignored)* | Policy config: `{id, name, policy}` per playlist. Pre-populated via `list-playlists`. | — | — |
| `.claude/skills/collect-youtube/SKILL.md` *(new)* | Thin skill driving `youtube_client.py run`; runnable manually or via `/loop`. | — | — |

## OAuth & setup

- Reuse the existing `bin/credentials.json` OAuth client (same Google Cloud project). **Enable "YouTube Data API v3"** in that project.
- Scope: `https://www.googleapis.com/auth/youtube.force-ssl` (single scope = read + delete).
- Separate token file `bin/youtube_token.json` (collectors stay independent). One-time `python3 bin/youtube_client.py auth`.
- Publish the OAuth app to **Production (unverified)** to avoid the 7-day refresh-token expiry of Testing mode.
- Gitignore: `bin/youtube_token.json` (and `bin/youtube_playlists.yaml`).

## Policy config (`bin/youtube_playlists.yaml`)

```yaml
# Pre-populated by `youtube_client.py list-playlists`; user sets each policy.
playlists:
  - id: PLxxxx
    name: "AI / ML"
    policy: collect-remove      # capture transcript, then remove from playlist
  - id: PLzzzz
    name: "SkateIQ"
    policy: collect-keep        # capture, never remove
  - id: PLbbbb
    name: "Workout"
    policy: collect-keep
default_policy: ignore          # any playlist not listed → ignore (+ surfaced in report)
```

- **Safe by default:** a playlist absent from the file (or new) is `ignore`d — never read for collection and never modified — and is listed in the run report so the user can classify it.
- Deletes happen **only** for `policy: collect-remove`.

## Data flow — `run`

For each configured playlist where `policy != ignore`:

1. **List items** via `playlistItems.list` (paginated; `part=snippet,contentDetails,status`). Each item yields `playlist_item_id` (delete key), `video_id`, `title`, `privacy_status`.
2. For each video, **deduped by `video_id`** (within the run and against already-collected files in `raw/_inbox`, `raw/youtube`):
   - If already collected → skip the write (idempotent); the item is still eligible for removal if `collect-remove` and a transcript exists in the prior file.
   - Else **extract transcript** (waterfall below). Build the markdown and **write** to `raw/_inbox/youtube-<video_id>-<slug>.md`. **Verify** the file exists.
3. **Removal** — only if `policy == collect-remove` AND a transcript was captured AND the file is confirmed: `playlistItems.delete(playlist_item_id)`. `204` = success; `404` = already gone = idempotent success. If no transcript → **do not remove**; flag in the report.
4. `--dry-run` performs steps 1–2 only (never deletes). `--max N` caps videos processed (quota guard). `--playlist <id>` restricts to one playlist.

**Cross-playlist:** the same video in a tech and a music playlist is collected once (dedup by `video_id`), removed from the tech playlist's item, kept in the music playlist's item.

## Transcript extraction (waterfall)

1. `YouTubeTranscriptApi().fetch(video_id, languages=["en"])`.
2. On `NoTranscriptFound` → `.list(video_id)`, pick best track (manual before generated), `.fetch()`.
3. On `RequestBlocked`/`IpBlocked` → `yt-dlp` subtitle fallback (`--skip-download --write-subs --write-auto-subs --sub-langs "en.*" --convert-subs srt`), with VTT/SRT rolling-caption dedup.
4. On `TranscriptsDisabled`/`VideoUnavailable`/total failure → record `transcript_status` reason (`disabled`/`unavailable`/`none_found`/`blocked`), body = a short "no transcript" note.

**Formatting:** drop empty + consecutive-duplicate lines; group snippets into ~20–30s paragraphs anchored by the first snippet's timestamp `[MM:SS](https://youtu.be/<id>?t=<seconds>)` (HH:MM:SS for long videos); strip `[Music]`/`[Applause]`. Pace 1–3s between videos to avoid self-rate-limiting.

## Output file

`raw/_inbox/youtube-<video_id>-<slug>.md`:
```yaml
---
channel: youtube
source: youtube
youtube_video_id: <id>
url: https://youtu.be/<id>
title: <title>
channel_name: <uploader>
published: YYYY-MM-DD
playlist: <playlist name>
transcript_status: ok | disabled | unavailable | none_found | blocked
collected_at: 2026-06-12
---

<timestamp-anchored transcript, or a "no transcript available" note>
```
Dedup key: `youtube_video_id`. Corpus ingest later routes the file to `raw/youtube/`.

## Error handling & resilience

- Private/deleted/region-blocked videos appear as items with no fetchable transcript → metadata stub, `transcript_status: unavailable`, **kept** (not removed).
- `quotaExceeded` / rate-limit → exponential backoff, then **stop gracefully**; the run is idempotent and resumes next invocation.
- `404` on delete → treat as success (already removed).
- A per-video failure never aborts the run; it is recorded and skipped.
- `run` tally: `playlists`, `collected`, `duplicate`, `no_transcript`, `removed`, `kept`, `failed`, plus any newly-seen unlisted playlists.

## Testing

- **Pure (no network):** transcript snippet→markdown (dedup, coarsening, timestamp anchors, `[Music]` stripping); VTT/SRT dedup for the yt-dlp path; `video_id` dedup; filename/slug; frontmatter; policy resolution (`collect-remove`/`collect-keep`/`ignore`, unlisted→default).
- **Mocked:** YouTube API list/delete with a fake `youtube` service object; transcript waterfall with a mocked `YouTubeTranscriptApi` (including each exception branch).
- No live YouTube/network calls in tests. Existing 60 tests stay green.

## Dependencies

All already installed: `google-api-python-client`, `google-auth-oauthlib`, `youtube_transcript_api` (1.2.4), `yt-dlp` (2026.03.03). No new installs. One-time user setup: enable YouTube Data API v3 + authorize.

## Open soft spots (acknowledged)

- **yt-dlp fallback quality** varies; it is a backstop for IP blocks, not the primary path. If it also fails, the video is recorded with `transcript_status: blocked` and kept.
- **Quota ceiling** (~196 removals/day) means a large tech-playlist backlog drains over several days; `run` is built to resume.
- **Playlist renames**: the config keys on playlist `id` (stable), with `name` for human reference; renames don't break policy.

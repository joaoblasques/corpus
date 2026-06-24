---
name: collect-youtube
description: Collect videos from the user's YouTube playlists into raw/_inbox/ as transcript markdown, then remove collected videos only from tech (collect-remove) playlists. Run manually or via /loop. Use when the user wants to pull YouTube playlist videos into the corpus.
---

# Collect YouTube

Capture videos from the user's YouTube playlists into `raw/_inbox/` (channel `youtube`)
with their transcripts, then de-list them — but ONLY from playlists marked
`collect-remove`. Collection only — never ingest into `corpus/`.

## Safety rules (non-negotiable)
- Remove a video from a playlist ONLY if its playlist policy is `collect-remove`,
  a transcript was captured (`transcript_status: ok`), and the markdown file is written.
- Never remove from `collect-keep` (skate/music/exercise) or `ignore` playlists.
- `--dry-run` never deletes. Write only to `raw/_inbox/`.

## Transport: owned YouTube credential
Uses `bin/youtube_client.py` with the user's own OAuth credential (`youtube.force-ssl`,
`bin/youtube_token.json`). One-time setup: enable "YouTube Data API v3" in the same
Google Cloud project as the Gmail collector, then `python3 bin/youtube_client.py auth`.
If `bin/youtube_token.json` is missing, tell the user to run auth first.

## Procedure
1. Preflight: confirm `bin/youtube_token.json` and `bin/youtube_playlists.yaml` exist.
   - No token → user runs `python3 bin/youtube_client.py auth`.
   - No config → run `python3 bin/youtube_client.py list-playlists`, then tell the user
     to set each playlist's `policy` (collect-remove / collect-keep / ignore) in
     `bin/youtube_playlists.yaml`. Do NOT guess policies.
2. Dry run: `python3 bin/youtube_client.py run --dry-run` (collects, no deletes). Review.
3. Real run: `python3 bin/youtube_client.py run` (caps via `--max`, one playlist via
   `--playlist <id>`). Quota ≈ 196 removals/day — large backlogs drain over days; the
   run is idempotent and resumes.
4. Report the JSON tally: `playlists · collected · duplicate · no_transcript · removed ·
   kept · failed`, plus any `ignored_playlists` the user may want to classify.

## Transcript waterfall (captions → yt-dlp VTT → Whisper)
`extract_transcript` tries, in order: native captions → manual/listed transcripts → a yt-dlp
VTT download. If a video is genuinely **caption-less** (`none_found`/`disabled`), it falls
through to a **Groq Whisper** tier: yt-dlp downloads the audio, ffmpeg compresses it to
mono/16k, long audio is **chunked** under Groq's 25 MB limit (40-min segments), each chunk is
transcribed (`whisper-large-v3`) and merged with offset timestamps. Whisper transcripts carry a
marker line `> _Transcript source: Whisper (Groq, auto-generated)_`. Runs off the Claude budget
(Groq ASR); needs `ffmpeg` + a `GROQ_API_KEY` (env or `~/.config/watch/.env`). If either is
missing, or any chunk fails, Whisper is a graceful no-op (`""`) and the video is kept (no partial
transcripts).
- A `blocked` status (transcript-API rate-limit) is normally left to `--refetch-blocked`. On that
  retry, if captions STILL can't be reached, the video falls through to Whisper as a last resort
  (`whisper_on_blocked`) — so caption-less videos behind a persistent IP-block still get transcribed
  and de-listed. Normal runs do NOT whisper `blocked` videos.

## Notes
- Genuinely caption-less videos now get a Whisper transcript (see the waterfall above) and are
  collected + de-listed like any other. Only videos where even Whisper is unavailable/fails are
  recorded as metadata stubs and KEPT in their playlist.
- Watch Later / History are not accessible via the API and are skipped.
- After collection, run the normal corpus ingest on `raw/_inbox/` when you choose;
  ingest routes youtube files to `raw/youtube/`.

---
title: "YouTube transcript collector skips blocked stubs due to state-blind dedup"
date: 2026-06-15
category: logic-errors
module: bin/collect_youtube.py
problem_type: logic_error
component: tooling
symptoms:
  - "1064 videos returned transcript_status: blocked after a burst run, yet were never re-fetched"
  - "raw/_inbox/ fills with sub-1KB stub files whose body is just _No transcript available._"
  - "re-running the collector reports the blocked videos as duplicate and never re-fetches them"
  - "already_collected() returned True for any existing file, ignoring transcript_status"
root_cause: logic_error
resolution_type: code_fix
severity: high
related_components:
  - background_job
tags:
  - youtube
  - transcript
  - dedup
  - rate-limiting
  - retry
  - idempotency
  - collector
---

# YouTube transcript collector skips blocked stubs due to state-blind dedup

## Problem

`collect-youtube` ran over ~77 playlists and fetched 1107 videos in a single burst. YouTube rate-limited the transcript fetcher mid-run, producing 1064 `transcript_status: blocked` stub files (<1 KB each). Because the dedup guard keyed on *file existence* rather than *fetch completeness*, every blocked video was reported as a `duplicate` on all subsequent runs — silently and permanently preventing re-fetch of 1064 recoverable transcripts.

## Symptoms

- Run-summary JSON shows a high failure split, e.g. `collected: 1107`, `ok: 30`, `blocked: 1064`, `disabled: 16`.
- `raw/_inbox/` contains ~1064 stub files under 1 KB; each has `transcript_status: blocked` and a body of `_No transcript available._`.
- Re-running the collector (before the fix) reports those same videos as `duplicate` immediately, increments the `duplicate` counter by ~1064, and never calls `extract_transcript` for them — the `blocked` count does not decrease across repeated runs.
- `already_collected()` returns `True` for any existing file matching the video id, regardless of `transcript_status`.

## What Didn't Work

The naive expectation was that a plain re-run "should just pick them up" — the transcripts were never successfully fetched, so the collector ought to try again. It didn't, because of how `already_collected` was implemented:

```python
# BEFORE — bin/collect_youtube.py
def already_collected(video_id: str, dirs=None) -> bool:
    return _scan(video_id, dirs) is not None
```

`_scan` searches `raw/_inbox/` and `raw/youtube/` for any `.md` whose body contains `youtube_video_id: <id>`. A `blocked` stub satisfies that needle just as well as a fully-fetched file does. The run loop used the check unconditionally:

```python
# BEFORE — bin/youtube_client.py cmd_run
if cy.already_collected(vid):          # True even for blocked stubs
    t["duplicate"] += 1
else:
    body, status = extract_transcript(vid)
    ...
```

Deleting the stub files would restore re-fetch ability but loses the saved metadata (`collected_at`, `channel_name`, `playlist`, title) and is fragile: it requires identifying and deleting exactly the right subset, and could accidentally remove legitimate `disabled` stubs (genuinely no captions — not worth retrying).

## Solution

Add a status-aware dedup predicate in `bin/collect_youtube.py`, switch the run loop to it, and gate the retry behind an opt-in flag (`--refetch-blocked`).

```python
# bin/collect_youtube.py — reads transcript_status from any existing stub
def collected_status(video_id: str, dirs=None):
    t = _scan(video_id, dirs)
    if t is None:
        return None
    m = re.search(r"^transcript_status:\s*(\S+)", t, re.M)
    return m.group(1) if m else None


# bin/collect_youtube.py — replaces existence-only dedup in the run loop
def should_collect(video_id: str, refetch_blocked: bool = False, dirs=None) -> bool:
    """Whether to (re)fetch this video's transcript.

    True when never collected; also True for an existing ``blocked`` stub when
    ``refetch_blocked`` is set (those are rate-limit artifacts worth retrying).
    A ``disabled`` status (genuinely no captions) is never re-fetched.
    """
    status = collected_status(video_id, dirs)
    if status is None:
        return True
    if refetch_blocked and status == "blocked":
        return True
    return False
```

```python
# AFTER — bin/youtube_client.py cmd_run
if not cy.should_collect(vid, args.refetch_blocked):
    t["duplicate"] += 1
    status = cy.collected_status(vid) or "unknown"
else:
    body, status = extract_transcript(vid)   # overwrites the stub in place
    ...
    path.write_text(cy.build_document(meta, body), encoding="utf-8")
```

```python
# bin/youtube_client.py _args — the opt-in flag
pr.add_argument("--refetch-blocked", action="store_true",
                help="re-fetch transcripts for videos previously saved with "
                     "transcript_status: blocked (rate-limit artifacts)")
```

Recovery invocation (note the throttle — see Prevention):

```bash
python3 bin/youtube_client.py run --refetch-blocked --max 50 --sleep 4
```

## Why This Works

The old guard asked only "does a file for this video exist?" — a binary that cannot distinguish a successful fetch from a rate-limited failure. `should_collect` asks "is the existing record in a terminal-success state?" The terminal states are `ok` (full transcript) and `disabled` (YouTube confirmed no captions); both are stable and not worth re-fetching. `blocked` is **transient** — the API refused the request, the video may well have a transcript — so it is retryable.

The `refetch_blocked` flag scopes the retry precisely: a plain run (no flag) stays fully idempotent and cheap no matter how many blocked stubs are on disk; only an explicit opt-in run re-extracts them. Re-fetching overwrites the stub in place, preserving the filename and all original metadata while adding the recovered body and updating `transcript_status`.

## Prevention

1. **Key dedup on success/completeness, not file existence.** Any cache or dedup guard for an expensive, fallible fetch should persist a distinguishable terminal status and base the skip decision on *that*, not on whether any artifact exists. `None → fetch; ok/disabled → skip; blocked → configurable` is the correct idiom. Existence-only dedup is an anti-pattern whenever the guarded operation can persist a partial/failed result.
2. **Throttle bulk re-fetch — bursts re-trigger the rate limit.** Live recovery showed that even `--refetch-blocked --max 50 --sleep 4` re-blocked ~33 of 48 videos; the threshold is well below a 50-item burst. Effective recovery uses small batches (`--max 5`–`20`) with a real `--sleep` (3–5s), spread across days. The scheduled-automation job drains the `blocked` backlog in small daily batches rather than one big run.
3. **Distinguish transient from terminal API failures at write time.** `extract_transcript` records `blocked` (rate-limited, retryable) vs `disabled` (no captions, terminal) as distinct statuses — and that distinction is exactly what makes selective retry possible. When wrapping any external API that can fail both at rate-limit and at capability, record both modes as separate status strings; never collapse them into one "no result" state.
4. **Lock the decision matrix with a test.** The `should_collect` four-case matrix (`never/ok/blocked/disabled × flag`) in `tests/test_collect_youtube.py`, plus the run-loop integration tests in `tests/test_youtube_client.py` (`--refetch-blocked` re-extracts a blocked stub → overwrites to `ok` → removes the video; a default run leaves it untouched), are the guardrail — any future change to dedup logic must keep them green.

## Related Issues

- Fix shipped in PR #3 (`fix/youtube-refetch-blocked`), merged to `main`.
- Files: `bin/collect_youtube.py` (`should_collect`, `collected_status`), `bin/youtube_client.py` (`cmd_run`, `_args`), `tests/test_collect_youtube.py`, `tests/test_youtube_client.py`.
- The scheduled-automation feature (PR #5) is the long-term consumer that drains the `blocked` backlog in small throttled daily batches.

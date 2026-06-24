#!/usr/bin/env python3
"""whisper_rescue.py — re-fetch transcripts for a *selected* set of blocked YouTube
stubs (captions-first, optional Whisper fallback) and upgrade each stub in place from
a `transcript_status: blocked` placeholder to an ingestable transcript.

Targets the curated keeper list (`raw/.whisper_keepers.tsv`: filename\tvideo_id\t…), so
only on-topic playlists are rescued; hobby stubs are left untouched. Reuses the tested
`youtube_client.extract_transcript` (captions → yt-dlp VTT → Whisper). Idempotent: a stub
already `ok` is skipped. raw/ is local-only, so this is a collection-layer operation."""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent
sys.path.insert(0, str(BIN))
import youtube_client as yc  # noqa: E402

INBOX = BIN.parent / "raw" / "_inbox"
KEEPERS = BIN.parent / "raw" / ".whisper_keepers.tsv"


def rescue_one(stub_path: Path, *, whisper: bool, whisper_direct: bool = False) -> str:
    head = stub_path.read_text(encoding="utf-8", errors="ignore")
    if re.search(r"^transcript_status:\s*ok", head, re.M):
        return "already_ok"
    m = re.search(r"^youtube_video_id:\s*(\S+)", head, re.M)
    if not m:
        return "no_id"
    if whisper_direct:
        # captions are known rate-limited for this set — go straight to audio/Whisper,
        # skipping the (slow, doomed) caption attempt.
        body = yc._whisper_transcript(m.group(1))
        status = "ok" if body else "failed"
    else:
        body, status = yc.extract_transcript(m.group(1), whisper_on_blocked=whisper)
    if status != "ok" or not body:
        return status or "failed"
    fm_end = head.find("\n---", 3)
    if fm_end == -1:
        return "no_frontmatter"
    fm = re.sub(r"^transcript_status:\s*blocked", "transcript_status: ok",
                head[:fm_end + 4], flags=re.M)
    via = "whisper" if "Whisper (Groq" in body else "captions"
    stub_path.write_text(fm + "\n\n" + body.strip() + "\n", encoding="utf-8")
    return f"ok:{via}"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Rescue transcripts for curated blocked YouTube stubs.")
    ap.add_argument("--keepers", default=str(KEEPERS))
    ap.add_argument("--max", type=int, default=None, help="cap stubs processed this run")
    ap.add_argument("--whisper", action="store_true",
                    help="allow Whisper fallback for still-blocked videos (slow); off = captions-only probe")
    ap.add_argument("--whisper-direct", action="store_true",
                    help="skip captions entirely, go straight to audio/Whisper (for known rate-limited sets)")
    args = ap.parse_args(argv)

    rows = [l.split("\t") for l in Path(args.keepers).read_text(encoding="utf-8").splitlines() if l]
    if args.max:
        rows = rows[:args.max]
    tally = {"ok_captions": 0, "ok_whisper": 0, "blocked": 0, "already_ok": 0,
             "no_id": 0, "failed": 0}
    for r in rows:
        p = INBOX / r[0]
        if not p.exists():
            tally["failed"] += 1
            continue
        res = rescue_one(p, whisper=args.whisper, whisper_direct=args.whisper_direct)
        key = {"ok:captions": "ok_captions", "ok:whisper": "ok_whisper"}.get(res, res)
        tally[key] = tally.get(key, 0) + 1
        print(json.dumps({"file": r[0], "result": res}), flush=True)
    print(json.dumps({"tally": tally, "processed": len(rows)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""youtube_client.py — owned-credential YouTube transport for collect-youtube."""
from __future__ import annotations

import argparse
import datetime
import json
import os
import sys
import time
from pathlib import Path

BIN = Path(__file__).resolve().parent
ROOT = BIN.parent
CREDENTIALS = BIN / "credentials.json"
YT_TOKEN = BIN / "youtube_token.json"
PLAYLISTS_CFG = BIN / "youtube_playlists.yaml"
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

sys.path.insert(0, str(BIN))
import collect_youtube as cy  # noqa: E402


# --- Whisper transcript fallback (Groq) -----------------------------------
def _groq_key(env_file="~/.config/watch/.env"):
    """Groq API key: GROQ_API_KEY env, else a GROQ_API_KEY= line in env_file, else None."""
    k = os.environ.get("GROQ_API_KEY")
    if k:
        return k
    p = Path(os.path.expanduser(env_file))
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("GROQ_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'") or None
    return None


def _whisper_enabled():
    return os.environ.get("CORPUS_YT_WHISPER", "1") != "0" and _groq_key() is not None


def _merge_chunk_segments(chunk_segment_lists, segment_seconds):
    """Flatten per-chunk [{start,text}] lists, offsetting chunk k by k*segment_seconds."""
    out = []
    for k, segs in enumerate(chunk_segment_lists):
        off = k * segment_seconds
        for s in segs:
            out.append({"start": float(s["start"]) + off, "text": s["text"]})
    return out


SEGMENT_SECONDS = 2400          # 40 min/chunk (~19 MB at mono/16k/64k)
CHUNK_THRESHOLD_BYTES = 24 * 1024 * 1024


def _groq_transcribe(path, key):
    """One audio file → list[{start,text}] via Groq Whisper verbose_json. Raises on failure."""
    import requests
    with open(path, "rb") as f:
        r = requests.post(
            "https://api.groq.com/openai/v1/audio/transcriptions",
            headers={"Authorization": f"Bearer {key}"},
            files={"file": (Path(path).name, f, "audio/mpeg")},
            data={"model": "whisper-large-v3", "response_format": "verbose_json"},
            timeout=300,
        )
    r.raise_for_status()
    return [{"start": s.get("start", 0.0), "text": s.get("text", "")}
            for s in r.json().get("segments", [])]


def _ytdlp_cookie_args() -> list[str]:
    """yt-dlp browser-cookie args to clear YouTube's bot-gate ("Sign in to confirm
    you're not a bot"). Browser is set by CORPUS_YT_COOKIES_BROWSER (default 'chrome');
    set it empty to disable cookies."""
    browser = os.environ.get("CORPUS_YT_COOKIES_BROWSER", "chrome").strip()
    return ["--cookies-from-browser", browser] if browser else []


def _whisper_transcript(video_id: str) -> str:
    """Caption-less fallback: download audio → mono/16k mp3 → (chunk if >24MB) → Groq Whisper.
    Returns markdown with a provenance marker, or "" on any failure (no partial transcripts)."""
    import glob
    import subprocess
    import tempfile
    key = _groq_key()
    if not key:
        return ""
    with tempfile.TemporaryDirectory() as td:
        try:
            subprocess.run(
                ["yt-dlp", "-x", "--audio-format", "mp3", *_ytdlp_cookie_args(),
                 "-o", f"{td}/%(id)s.%(ext)s", f"https://youtu.be/{video_id}"],
                capture_output=True, timeout=600, check=True)
            src = next(iter(glob.glob(f"{td}/*.mp3")), None)
            if not src:
                return ""
            comp = f"{td}/a.mp3"
            subprocess.run(["ffmpeg", "-y", "-i", src, "-vn", "-ac", "1", "-ar", "16000",
                            "-b:a", "64k", comp], capture_output=True, timeout=600, check=True)
            if os.path.getsize(comp) > CHUNK_THRESHOLD_BYTES:
                subprocess.run(["ffmpeg", "-y", "-i", comp, "-f", "segment",
                                "-segment_time", str(SEGMENT_SECONDS), "-c", "copy",
                                f"{td}/chunk_%03d.mp3"], capture_output=True, timeout=600, check=True)
                chunks = sorted(glob.glob(f"{td}/chunk_*.mp3"))
            else:
                chunks = [comp]
            per_chunk = [_groq_transcribe(c, key) for c in chunks]   # raises → abort below
        except Exception:
            return ""
    snips = _merge_chunk_segments(per_chunk, SEGMENT_SECONDS)
    if not snips:
        return ""
    md = cy.transcript_to_markdown(snips, video_id)
    return "> _Transcript source: Whisper (Groq, auto-generated)_\n\n" + md


def get_service():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    creds = None
    if YT_TOKEN.exists():
        creds = Credentials.from_authorized_user_file(str(YT_TOKEN), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS.exists():
                raise SystemExit(
                    f"Missing {CREDENTIALS}. Reuse the Gmail OAuth Desktop client and "
                    "enable 'YouTube Data API v3' in the same Google Cloud project."
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS), SCOPES)
            creds = flow.run_local_server(port=0)
        YT_TOKEN.write_text(creds.to_json(), encoding="utf-8")
    return build("youtube", "v3", credentials=creds, cache_discovery=False)


def list_my_playlists(service):
    req = service.playlists().list(part="snippet,contentDetails", mine=True, maxResults=50)
    while req is not None:
        resp = req.execute()
        for it in resp.get("items", []):
            yield {"id": it["id"], "name": it["snippet"]["title"],
                   "count": it.get("contentDetails", {}).get("itemCount")}
        req = service.playlists().list_next(req, resp)


def list_playlist_items(service, playlist_id):
    req = service.playlistItems().list(
        part="snippet,contentDetails,status", playlistId=playlist_id, maxResults=50)
    while req is not None:
        resp = req.execute()
        for it in resp.get("items", []):
            sn = it.get("snippet", {})
            video_id = sn.get("resourceId", {}).get("videoId")
            if not video_id:
                continue
            yield {
                "playlist_item_id": it.get("id"),
                "video_id": video_id,
                "title": sn.get("title", ""),
                "channel_name": sn.get("videoOwnerChannelTitle", ""),
                "published": (it.get("contentDetails", {}).get("videoPublishedAt", "") or "")[:10],
                "privacy": it.get("status", {}).get("privacyStatus", ""),
            }
        req = service.playlistItems().list_next(req, resp)


def delete_playlist_item(service, item_id) -> bool:
    from googleapiclient.errors import HttpError
    try:
        service.playlistItems().delete(id=item_id).execute()
        return True
    except HttpError as e:
        if getattr(e, "resp", None) is not None and getattr(e.resp, "status", None) == 404:
            return True
        raise


def _transcript_api():
    from youtube_transcript_api import YouTubeTranscriptApi
    return YouTubeTranscriptApi()


def _caption_transcript(video_id: str):
    """Caption waterfall → (markdown_body, status). status: ok|disabled|unavailable|none_found|blocked."""
    import youtube_transcript_api as yta
    errs = yta._errors
    api = _transcript_api()

    def snips(fetched):
        return [{"start": s.start, "text": s.text} for s in fetched]

    try:
        return cy.transcript_to_markdown(snips(api.fetch(video_id, languages=["en"])), video_id), "ok"
    except errs.NoTranscriptFound:
        blocked_errs = tuple(
            c for c in (getattr(errs, "RequestBlocked", None), getattr(errs, "IpBlocked", None))
            if isinstance(c, type)
        )
        try:
            tl = api.list(video_id)
            t = next((x for x in tl if not getattr(x, "is_generated", False)), None) or next(iter(tl), None)
            if t is not None:
                return cy.transcript_to_markdown(snips(t.fetch()), video_id), "ok"
        except blocked_errs:
            body = _ytdlp_transcript(video_id)
            return (body, "ok") if body else ("", "blocked")
        except Exception:
            pass
        return "", "none_found"
    except errs.TranscriptsDisabled:
        return "", "disabled"
    except errs.VideoUnavailable:
        return "", "unavailable"
    except Exception:
        body = _ytdlp_transcript(video_id)
        return (body, "ok") if body else ("", "blocked")


def _browser_enabled() -> bool:
    return os.environ.get("CORPUS_YT_BROWSER", "1") != "0"


def extract_transcript(video_id: str, whisper_on_blocked: bool = False):
    """Waterfall -> (markdown_body, status). Browser-primary.

    Order: browser panel scrape -> (no_panel) Whisper -> (blocked/failed) the legacy
    caption API + yt-dlp VTT deep fallback -> (still none) Whisper per old triggers.
    CORPUS_YT_BROWSER=0 restores the legacy caption-first behaviour.
    """
    if _browser_enabled():
        import yt_browser_transcript as bt
        body, status = bt.browser_transcript(video_id)
        if status == "ok":
            return body, "ok"
        if status == "no_panel" and _whisper_enabled():
            wbody = _whisper_transcript(video_id)
            if wbody:
                return wbody, "ok"
        # blocked / failed / whisper-miss -> fall through to legacy paths below.

    body, status = _caption_transcript(video_id)
    trigger = ("none_found", "disabled", "blocked") if whisper_on_blocked else ("none_found", "disabled")
    if status in trigger and _whisper_enabled():
        wbody = _whisper_transcript(video_id)
        if wbody:
            return wbody, "ok"
    return body, status


def _ytdlp_transcript(video_id: str) -> str:
    import glob
    import subprocess
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        try:
            subprocess.run(
                ["yt-dlp", "--skip-download", "--write-subs", "--write-auto-subs",
                 "--sub-langs", "en.*", "--sub-format", "vtt", *_ytdlp_cookie_args(),
                 "-o", f"{td}/%(id)s.%(ext)s", f"https://youtu.be/{video_id}"],
                capture_output=True, timeout=90, check=False)
            vtts = glob.glob(f"{td}/*.vtt")
            if not vtts:
                return ""
            return cy.transcript_to_markdown(cy.dedup_vtt(Path(vtts[0]).read_text(encoding="utf-8")), video_id)
        except Exception:
            return ""


def load_config() -> dict:
    return cy.load_policy_config(PLAYLISTS_CFG)


def cmd_auth(_args) -> int:
    get_service()
    print(json.dumps({"status": "authorized", "token": str(YT_TOKEN)}))
    return 0


def cmd_list_playlists(_args) -> int:
    import yaml
    service = get_service()
    found = list(list_my_playlists(service))
    cfg = load_config()
    known = {p.get("id") for p in cfg["playlists"]}
    for p in found:
        if p["id"] not in known:
            cfg["playlists"].append({"id": p["id"], "name": p["name"], "policy": "ignore"})
    body = ("# policy per playlist: collect-remove | collect-keep | ignore\n"
            + yaml.safe_dump({"playlists": cfg["playlists"],
                              "default_policy": cfg.get("default_policy", "ignore")},
                             sort_keys=False, allow_unicode=True))
    PLAYLISTS_CFG.write_text(body, encoding="utf-8")
    print(json.dumps({"playlists": len(found), "config": str(PLAYLISTS_CFG),
                      "note": "set each playlist's policy, then run"}))
    return 0


def cmd_run(args) -> int:
    from googleapiclient.errors import HttpError

    service = get_service()
    cfg = load_config()
    collected_at = args.collected_at or datetime.date.today().isoformat()
    t = {"playlists": 0, "collected": 0, "duplicate": 0, "no_transcript": 0,
         "removed": 0, "kept": 0, "failed": 0}
    targets = [p for p in cfg["playlists"] if p.get("policy") in ("collect-remove", "collect-keep")]
    if args.playlist:
        targets = [p for p in targets if p["id"] == args.playlist]
    processed = 0
    refetched = 0  # count of blocked-stub refetches this run (capped by --refetch-max)
    stopped = None
    for pl in targets:
        if stopped:
            break
        policy = pl["policy"]
        t["playlists"] += 1
        for item in list_playlist_items(service, pl["id"]):
            if args.max and processed >= args.max:
                break
            processed += 1
            vid = item["video_id"]
            fetched = False  # only throttle after an actual transcript fetch
            try:
                do_collect = cy.should_collect(vid, args.refetch_blocked)
                # Honor the blocked-refetch cap: once --refetch-max refetches are
                # done, leave further blocked stubs as duplicates for the next run.
                if (do_collect and args.refetch_blocked
                        and args.refetch_max is not None
                        and cy.collected_status(vid) == "blocked"):
                    if refetched >= args.refetch_max:
                        do_collect = False
                    else:
                        refetched += 1
                if not do_collect:
                    t["duplicate"] += 1
                    status = cy.collected_status(vid) or "unknown"
                else:
                    fetched = True
                    # --refetch-blocked last resort: a previously-blocked video that the
                    # caption paths still can't reach falls through to Whisper.
                    whisper_on_blocked = bool(
                        args.refetch_blocked and cy.collected_status(vid) == "blocked")
                    body, status = extract_transcript(vid, whisper_on_blocked=whisper_on_blocked)
                    meta = {"video_id": vid, "title": item["title"],
                            "channel_name": item["channel_name"], "published": item["published"],
                            "playlist": pl["name"], "transcript_status": status,
                            "collected_at": collected_at}
                    path = cy.target_filename(vid, item["title"])
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(cy.build_document(meta, body), encoding="utf-8")
                    if not path.exists():
                        t["failed"] += 1
                        continue
                    t["collected"] += 1
                    if status != "ok":
                        t["no_transcript"] += 1
                # Safety rule: remove ONLY for collect-remove, ONLY with a transcript, never on dry-run.
                if policy == "collect-remove" and status == "ok" and not args.dry_run:
                    if delete_playlist_item(service, item["playlist_item_id"]):
                        t["removed"] += 1
                else:
                    t["kept"] += 1
                # Throttle only the rate-limit-sensitive fetches, not duplicates:
                # a steady-state daily run is mostly duplicates and should be fast.
                if args.sleep and fetched:
                    time.sleep(args.sleep)
            except HttpError as e:
                status_code = getattr(getattr(e, "resp", None), "status", None)
                if status_code in (403, 429, 503):
                    stopped = "quota_or_rate_limit"
                    break
                t["failed"] += 1
            except Exception:
                t["failed"] += 1
    if _browser_enabled():
        import yt_browser_transcript as bt
        bt.shutdown()
    ignored = [p["name"] for p in cfg["playlists"] if p.get("policy") == "ignore"]
    out = {**t, "dry_run": bool(args.dry_run), "ignored_playlists": ignored}
    if stopped:
        out["stopped"] = stopped
    print(json.dumps(out, indent=2))
    return 0


def _args(argv):
    p = argparse.ArgumentParser(description="Owned-credential YouTube playlist collector.")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("auth").set_defaults(func=cmd_auth)
    sub.add_parser("list-playlists").set_defaults(func=cmd_list_playlists)
    pr = sub.add_parser("run")
    pr.add_argument("--dry-run", action="store_true")
    pr.add_argument("--max", type=int, default=None)
    pr.add_argument("--playlist", default=None)
    pr.add_argument("--sleep", type=float, default=2.0)
    pr.add_argument("--collected-at", default=None)
    pr.add_argument("--refetch-blocked", action="store_true",
                    help="re-fetch transcripts for videos previously saved with "
                         "transcript_status: blocked (rate-limit artifacts)")
    pr.add_argument("--refetch-max", type=int, default=None,
                    help="cap the number of blocked-stub refetches this run (only "
                         "meaningful with --refetch-blocked); default unlimited. Keep "
                         "small in scheduled runs to avoid re-triggering the rate limit.")
    pr.set_defaults(func=cmd_run)
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = _args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

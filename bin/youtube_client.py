#!/usr/bin/env python3
"""youtube_client.py — owned-credential YouTube transport for collect-youtube."""
from __future__ import annotations

import argparse
import datetime
import json
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
            sn = it["snippet"]
            yield {
                "playlist_item_id": it["id"],
                "video_id": sn["resourceId"]["videoId"],
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


def extract_transcript(video_id: str):
    """Waterfall → (markdown_body, status). status: ok|disabled|unavailable|none_found|blocked."""
    import youtube_transcript_api as yta
    errs = yta._errors
    api = _transcript_api()

    def snips(fetched):
        return [{"start": s.start, "text": s.text} for s in fetched]

    try:
        return cy.transcript_to_markdown(snips(api.fetch(video_id, languages=["en"])), video_id), "ok"
    except errs.NoTranscriptFound:
        try:
            tl = api.list(video_id)
            t = next((x for x in tl if not getattr(x, "is_generated", False)), None) or next(iter(tl), None)
            if t is not None:
                return cy.transcript_to_markdown(snips(t.fetch()), video_id), "ok"
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


def _ytdlp_transcript(video_id: str) -> str:
    import glob
    import subprocess
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        try:
            subprocess.run(
                ["yt-dlp", "--skip-download", "--write-subs", "--write-auto-subs",
                 "--sub-langs", "en.*", "--sub-format", "vtt",
                 "-o", f"{td}/%(id)s.%(ext)s", f"https://youtu.be/{video_id}"],
                capture_output=True, timeout=90, check=False)
            vtts = glob.glob(f"{td}/*.vtt")
            if not vtts:
                return ""
            return cy.transcript_to_markdown(cy.dedup_vtt(Path(vtts[0]).read_text(encoding="utf-8")), video_id)
        except Exception:
            return ""

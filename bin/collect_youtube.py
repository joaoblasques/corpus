#!/usr/bin/env python3
"""collect_youtube.py — deterministic core for the collect-youtube skill.

Pure functions only: transcript formatting, dedup, filename, frontmatter, and
per-playlist policy resolution. Network I/O lives in youtube_client.py.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

BIN = Path(__file__).resolve().parent
ROOT = BIN.parent
INBOX = ROOT / "raw" / "_inbox"
DEDUP_DIRS = [ROOT / "raw" / "_inbox", ROOT / "raw" / "youtube"]

sys.path.insert(0, str(BIN))
from collect_email import slugify, yaml_scalar  # noqa: E402  (DRY reuse)


def load_policy_config(path) -> dict:
    p = Path(path)
    if not p.exists():
        return {"playlists": [], "default_policy": "ignore"}
    data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    return {
        "playlists": data.get("playlists") or [],
        "default_policy": data.get("default_policy", "ignore"),
    }


def resolve_policy(playlist_id: str, config: dict) -> str:
    for pl in config.get("playlists", []):
        if pl.get("id") == playlist_id:
            return pl.get("policy", "ignore")
    return config.get("default_policy", "ignore")


NOISE_RE = re.compile(r"\[(music|applause|laughter|inaudible)\]", re.I)


def hms(seconds) -> str:
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def ts_anchor(seconds, video_id) -> str:
    return f"[{hms(seconds)}](https://youtu.be/{video_id}?t={int(seconds)})"


def clean_snippets(snippets: list) -> list:
    """Drop empties, strip noise markers, collapse whitespace, drop consecutive dups."""
    out, prev = [], None
    for s in snippets:
        text = NOISE_RE.sub("", s.get("text") or "").replace("\n", " ")
        text = re.sub(r"\s+", " ", text).strip()
        if not text or text == prev:
            continue
        prev = text
        out.append({"start": float(s.get("start", 0)), "text": text})
    return out


def group_snippets(snippets: list, window: int = 25) -> list:
    """Group cleaned snippets into ~window-second paragraphs, anchored by first start."""
    groups, cur = [], None
    for s in snippets:
        if cur is None or s["start"] - cur["start"] >= window:
            cur = {"start": s["start"], "texts": [s["text"]]}
            groups.append(cur)
        else:
            cur["texts"].append(s["text"])
    return groups


def transcript_to_markdown(snippets: list, video_id: str, window: int = 25) -> str:
    groups = group_snippets(clean_snippets(snippets), window)
    return "\n\n".join(
        f"{ts_anchor(g['start'], video_id)} {' '.join(g['texts'])}" for g in groups
    )


_VTT_TS = re.compile(r"(\d{2}):(\d{2}):(\d{2})\.\d{3}\s*-->")


def dedup_vtt(vtt_text: str) -> list:
    """Parse a WebVTT body into [{start,text}], stripping inline tags and rolling dups."""
    snippets, last = [], None
    cur_start, buf = None, []

    def flush():
        nonlocal cur_start, buf, last
        if cur_start is None:
            return
        text = re.sub(r"<[^>]+>", "", " ".join(buf))
        text = re.sub(r"\s+", " ", text).strip()
        if text and text != last:
            snippets.append({"start": cur_start, "text": text})
            last = text
        cur_start, buf = None, []

    for raw in vtt_text.splitlines():
        line = raw.strip()
        m = _VTT_TS.match(line)
        if m:
            flush()
            cur_start = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
        elif line and "WEBVTT" not in line and "-->" not in line and not line.isdigit():
            buf.append(line)
    flush()
    return snippets


def target_filename(video_id: str, title: str, base=None) -> Path:
    base = base if base is not None else INBOX
    return base / f"youtube-{video_id}-{slugify(title)}.md"


def build_document(meta: dict, body: str) -> str:
    lines = [
        "---",
        "channel: youtube",
        "source: youtube",
        f"youtube_video_id: {meta['video_id']}",
        f"url: https://youtu.be/{meta['video_id']}",
        f"title: {yaml_scalar(meta['title'])}",
        f"channel_name: {yaml_scalar(meta.get('channel_name', ''))}",
        f"published: {meta.get('published', '')}",
        f"playlist: {yaml_scalar(meta.get('playlist', ''))}",
        f"transcript_status: {meta['transcript_status']}",
        f"collected_at: {meta['collected_at']}",
        "---",
        "",
        body.strip() if body and body.strip() else "_No transcript available._",
        "",
    ]
    return "\n".join(lines)


def _scan(video_id, dirs):
    needle = f"youtube_video_id: {video_id}\n"
    for d in (dirs if dirs is not None else DEDUP_DIRS):
        if not Path(d).exists():
            continue
        for md in Path(d).glob("*.md"):
            try:
                t = md.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            if needle in t:
                return t
    return None


def already_collected(video_id: str, dirs=None) -> bool:
    return _scan(video_id, dirs) is not None


def collected_status(video_id: str, dirs=None):
    t = _scan(video_id, dirs)
    if t is None:
        return None
    m = re.search(r"^transcript_status:\s*(\S+)", t, re.M)
    return m.group(1) if m else None

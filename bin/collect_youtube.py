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

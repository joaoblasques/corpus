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

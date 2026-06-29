#!/usr/bin/env python3
"""yt_browser_transcript.py — logged-out browser scrape of YouTube's "Show transcript"
panel. Primary transcript source for collect-youtube; isolates all Playwright/DOM
knowledge. Public entry point: browser_transcript(video_id) -> (markdown_body, status)."""
from __future__ import annotations

import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent
sys.path.insert(0, str(BIN))
import collect_youtube as cy  # noqa: E402


def parse_ts(label: str) -> int | None:
    """'1:23'->83, '1:02:03'->3723. None if not a colon-separated mm:ss / hh:mm:ss label."""
    parts = (label or "").strip().split(":")
    if len(parts) not in (2, 3) or not all(p.isdigit() for p in parts):
        return None
    secs = 0
    for p in parts:
        secs = secs * 60 + int(p)
    return secs


def lines_to_snippets(lines: list[tuple[str, str]]) -> list[dict]:
    """[(ts_label, text)] -> [{start, text}], dropping rows with bad label or empty text."""
    out = []
    for label, text in lines:
        secs = parse_ts(label)
        text = (text or "").strip()
        if secs is None or not text:
            continue
        out.append({"start": secs, "text": text})
    return out

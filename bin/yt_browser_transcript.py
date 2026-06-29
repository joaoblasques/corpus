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


PROVENANCE = "> _Transcript source: YouTube UI (browser)_"


def _fetch_panel(video_id: str) -> tuple[list[tuple[str, str]], str]:
    """Drive Playwright to scrape the transcript panel. Returns (lines, status).
    Implemented in Task 3; tests always monkeypatch this. Default real impl raises
    until Task 3 fills it in."""
    raise NotImplementedError


def browser_transcript(video_id: str) -> tuple[str, str]:
    """Primary transcript source: scrape the watch-page transcript panel.
    Returns (markdown_body, status). Never raises (maps errors to 'failed')."""
    try:
        lines, status = _fetch_panel(video_id)
    except Exception:
        return "", "failed"
    if status != "ok":
        return "", status
    snippets = lines_to_snippets(lines)
    if not snippets:
        return "", "no_panel"
    body = cy.transcript_to_markdown(snippets, video_id)
    return PROVENANCE + "\n\n" + body, "ok"

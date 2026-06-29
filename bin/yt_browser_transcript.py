#!/usr/bin/env python3
"""yt_browser_transcript.py — logged-out browser scrape of YouTube's "Show transcript"
panel. Primary transcript source for collect-youtube; isolates all Playwright/DOM
knowledge. Public entry point: browser_transcript(video_id) -> (markdown_body, status)."""
from __future__ import annotations

import random
import sys
import time
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


_PW = None       # playwright instance
_BROWSER = None   # launched browser (reused per run)

_SEGMENT_SEL = "ytd-transcript-segment-renderer"
_NAV_TIMEOUT_MS = 30000
_PANEL_TIMEOUT_MS = 8000


def _extract_panel_rows(page) -> list[tuple[str, str]]:
    """Read open transcript panel -> [(ts_label, text)]. First text line is the
    timestamp, remainder is the caption (segment renderer renders 'M:SS\\ntext')."""
    rows = []
    for seg in page.locator(_SEGMENT_SEL).all():
        parts = seg.inner_text().split("\n", 1)
        if len(parts) == 2:
            rows.append((parts[0].strip(), parts[1].strip()))
    return rows


def _open_transcript(page) -> bool:
    """Open the transcript panel. Try the description '...more' expander then a
    'Show transcript' button; fall back to the direct button. Return True if rows appear."""
    for opener in (
        lambda: page.get_by_role("button", name="...more").click(timeout=3000),
        lambda: page.get_by_role("button", name="Show transcript").click(timeout=3000),
    ):
        try:
            opener()
        except Exception:
            continue
    try:
        page.wait_for_selector(_SEGMENT_SEL, timeout=_PANEL_TIMEOUT_MS)
        return True
    except Exception:
        return False


def _get_page():
    """Lazily launch one logged-out Chromium per run; return a fresh page on it."""
    global _PW, _BROWSER
    if _BROWSER is None:
        from playwright.sync_api import sync_playwright
        _PW = sync_playwright().start()
        _BROWSER = _PW.chromium.launch(headless=True)
    ctx = _BROWSER.new_context(
        viewport={"width": 1280, "height": 900},
        user_agent=("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"),
    )
    return ctx.new_page()


def shutdown() -> None:
    """Tear down the per-run browser. Safe when nothing was launched."""
    global _PW, _BROWSER
    try:
        if _BROWSER is not None:
            _BROWSER.close()
    finally:
        if _PW is not None:
            _PW.stop()
        _PW = _BROWSER = None


def _fetch_panel(video_id: str) -> tuple[list[tuple[str, str]], str]:
    page = _get_page()
    try:
        page.goto(f"https://www.youtube.com/watch?v={video_id}",
                  timeout=_NAV_TIMEOUT_MS, wait_until="domcontentloaded")
        # Consent interstitial (EU): accept if present.
        try:
            page.get_by_role("button", name="Accept all").click(timeout=3000)
        except Exception:
            pass
        body_txt = page.locator("body").inner_text(timeout=5000)
        if "not a bot" in body_txt or "confirm you" in body_txt.lower():
            return [], "blocked"
        if not _open_transcript(page):
            return [], "no_panel"
        return _extract_panel_rows(page), "ok"
    except Exception:
        return [], "failed"
    finally:
        try:
            page.context.close()
        except Exception:
            pass


def human_delay() -> None:
    """Randomized 3-8s pause between videos so a run never looks like a scraper."""
    time.sleep(random.uniform(3.0, 8.0))


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

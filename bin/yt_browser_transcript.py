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

# YouTube migrated transcript lines to a web-component view-model (the old
# ytd-transcript-segment-renderer no longer exists). All DOM knowledge lives here.
_SEGMENT_SEL = "transcript-segment-view-model"
_EXPAND_SEL = "#description-inline-expander tp-yt-paper-button#expand"
_SHOW_TRANSCRIPT_SEL = '[aria-label="Show transcript"]:visible'
_NAV_TIMEOUT_MS = 30000
_PANEL_TIMEOUT_MS = 9000


def _extract_panel_rows(page) -> list[tuple[str, str]]:
    """Read open transcript panel -> [(ts_label, text)]. Each segment renders as
    'M:SS\\n<a11y label>\\n<caption>' (or 'M:SS\\n<caption>'), so the first line is the
    timestamp and the LAST line is the caption (the middle a11y label is skipped)."""
    rows = []
    for seg in page.locator(_SEGMENT_SEL).all():
        lines = [ln for ln in seg.inner_text().split("\n") if ln.strip()]
        if len(lines) >= 2:
            rows.append((lines[0].strip(), lines[-1].strip()))
    return rows


def _dismiss_consent(page) -> None:
    """Dismiss the EU "Before you continue to YouTube" consent modal. Its backdrop
    (tp-yt-iron-overlay-backdrop) intercepts every click until gone. Match by visible
    text ('Reject all'/'Accept all') — the aria-label is a long localized sentence."""
    for name in ("Reject all", "Accept all"):
        loc = page.locator(
            f'tp-yt-paper-dialog button:has-text("{name}"), '
            f'ytd-consent-bump-v2-lightbox button:has-text("{name}")')
        if loc.count():
            try:
                loc.first.click(timeout=3000)
                break
            except Exception:
                pass
    try:
        page.wait_for_selector("tp-yt-iron-overlay-backdrop.opened",
                               state="detached", timeout=5000)
    except Exception:
        pass


def _open_transcript(page) -> bool:
    """Open the transcript panel: expand the description ('...more') then click the
    'Show transcript' control (a view-model, not a role=button). Returns True once
    transcript segments render. Uses condition-based waits (wait_for the control to
    appear) rather than fixed sleeps, since the description renders at varying speeds.
    Retries the flow once for headless flakiness."""
    for attempt in range(2):
        try:
            page.locator(_EXPAND_SEL).first.click(timeout=6000)
        except Exception:
            if attempt == 0:
                page.wait_for_timeout(700)
                continue
            return False
        # Wait for the 'Show transcript' control to render (slower videos miss a fixed
        # sleep). It may be absent entirely (no captions) -> genuine no_panel.
        try:
            page.wait_for_selector(_SHOW_TRANSCRIPT_SEL, timeout=4000)
        except Exception:
            if attempt == 0:
                page.wait_for_timeout(700)
                continue
            return False
        try:
            page.locator(_SHOW_TRANSCRIPT_SEL).first.click(timeout=6000)
            page.wait_for_selector(_SEGMENT_SEL, timeout=_PANEL_TIMEOUT_MS)
            return True
        except Exception:
            if attempt == 0:
                page.wait_for_timeout(700)
                continue
            return False
    return False


def _get_page():
    """Lazily launch one logged-out Chromium per run; return a fresh page on it.
    Forces an English UI (locale + Accept-Language) so the English DOM selectors match
    regardless of the host's geo-location."""
    global _PW, _BROWSER
    if _BROWSER is None:
        from playwright.sync_api import sync_playwright
        _PW = sync_playwright().start()
        _BROWSER = _PW.chromium.launch(headless=True)
    ctx = _BROWSER.new_context(
        viewport={"width": 1280, "height": 1000},
        locale="en-US",
        extra_http_headers={"Accept-Language": "en-US,en;q=0.9"},
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
        # &hl=en forces the English UI even when the host geo-locates elsewhere.
        page.goto(f"https://www.youtube.com/watch?v={video_id}&hl=en",
                  timeout=_NAV_TIMEOUT_MS, wait_until="domcontentloaded")
        page.wait_for_timeout(1500)
        body_txt = page.locator("body").inner_text(timeout=5000)
        if "not a bot" in body_txt or "confirm you" in body_txt.lower():
            return [], "blocked"
        # EU consent modal overlays the page and intercepts clicks until dismissed.
        _dismiss_consent(page)
        # Scroll to lazy-load the description area that holds the transcript control.
        page.mouse.wheel(0, 900)
        page.wait_for_timeout(700)
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

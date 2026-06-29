# Browser-UI YouTube Transcript Tier — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a logged-out browser scrape of YouTube's "Show transcript" panel as the *primary* transcript source, demoting the bot-gated API/yt-dlp paths to deep fallbacks, usable both in the nightly collector and a backlog drainer.

**Architecture:** A new isolated module `bin/yt_browser_transcript.py` owns all Playwright/DOM knowledge and exposes `browser_transcript(video_id) -> (markdown_body, status)`. `youtube_client.extract_transcript` calls it first; `whisper_rescue.py` gains a `--browser` mode. Transcript text is parsed into `[{start, text}]` and rendered with the *existing* `collect_youtube.transcript_to_markdown`, so output is byte-identical in shape to today's transcripts.

**Tech Stack:** Python 3 (system `/usr/local/bin/python3`), Playwright (already importable) + Chromium, pytest. Reuses `collect_youtube` (`cy`) helpers.

## Global Constraints

- Session is **logged-out**: a fresh Playwright Chromium, never the user's Google account.
- Browser scrape is the **primary** path; `youtube_transcript_api` + yt-dlp VTT are **deep fallbacks** only.
- Status contract is exactly: `ok` | `no_panel` | `blocked` | `failed`.
- Provenance marker prepended verbatim: `> _Transcript source: YouTube UI (browser)_`.
- Output rendered via `cy.transcript_to_markdown(snippets, video_id)` — never hand-rolled.
- No partial transcripts: any exception → `("", "failed")`, nothing written.
- Feature flag `CORPUS_YT_BROWSER` (default `"1"`; `"0"` disables the tier), mirroring `CORPUS_YT_WHISPER`.
- One reused browser context per run; always torn down in `finally` (no leaked Chromium under launchd).
- Tests must NOT launch a real browser: monkeypatch the fetch boundary.

---

### Task 1: Timestamp parsing + snippet assembly (pure functions)

**Files:**
- Create: `bin/yt_browser_transcript.py`
- Test: `tests/test_yt_browser_transcript.py`

**Interfaces:**
- Produces:
  - `parse_ts(label: str) -> int | None` — `"1:23"`→`83`, `"1:02:03"`→`3723`, `"0:00"`→`0`; returns `None` for malformed.
  - `lines_to_snippets(lines: list[tuple[str, str]]) -> list[dict]` — `[(ts_label, text), ...]` → `[{"start": int, "text": str}, ...]`, dropping rows whose label fails `parse_ts` or whose text is empty.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_yt_browser_transcript.py
import sys, importlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
bt = importlib.import_module("yt_browser_transcript")


def test_parse_ts_mm_ss():
    assert bt.parse_ts("1:23") == 83
    assert bt.parse_ts("0:00") == 0


def test_parse_ts_hh_mm_ss():
    assert bt.parse_ts("1:02:03") == 3723


def test_parse_ts_malformed_returns_none():
    assert bt.parse_ts("") is None
    assert bt.parse_ts("abc") is None
    assert bt.parse_ts("12") is None


def test_lines_to_snippets_maps_and_drops_bad_rows():
    lines = [("0:00", "hello"), ("0:05", ""), ("bad", "x"), ("1:23", "world")]
    assert bt.lines_to_snippets(lines) == [
        {"start": 0, "text": "hello"},
        {"start": 83, "text": "world"},
    ]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_yt_browser_transcript.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'yt_browser_transcript'`

- [ ] **Step 3: Write minimal implementation**

```python
# bin/yt_browser_transcript.py
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_yt_browser_transcript.py -v`
Expected: PASS (4 tests)

- [ ] **Step 5: Commit**

```bash
git add bin/yt_browser_transcript.py tests/test_yt_browser_transcript.py
git commit -m "feat(youtube): browser transcript — timestamp parse + snippet assembly"
```

---

### Task 2: `browser_transcript` orchestration + status contract

**Files:**
- Modify: `bin/yt_browser_transcript.py`
- Test: `tests/test_yt_browser_transcript.py`

**Interfaces:**
- Consumes: `lines_to_snippets` (Task 1); `cy.transcript_to_markdown`.
- Produces:
  - `_fetch_panel(video_id: str) -> tuple[list[tuple[str, str]], str]` — the ONLY function that drives Playwright. Returns `(lines, status)` with `status` in `ok|no_panel|blocked|failed`. Monkeypatched in tests; never called for real in the suite.
  - `browser_transcript(video_id: str) -> tuple[str, str]` — calls `_fetch_panel`; on `ok` renders `cy.transcript_to_markdown(lines_to_snippets(lines), video_id)` with the provenance marker prepended; for non-`ok` returns `("", status)`. If `ok` but snippets render empty → `("", "no_panel")`.

- [ ] **Step 1: Write the failing test**

```python
def test_browser_transcript_ok_renders_with_marker(monkeypatch):
    monkeypatch.setattr(bt, "_fetch_panel",
                        lambda vid: ([("0:00", "hello"), ("1:23", "world")], "ok"))
    body, status = bt.browser_transcript("ABC")
    assert status == "ok"
    assert body.startswith("> _Transcript source: YouTube UI (browser)_")
    assert "https://youtu.be/ABC?t=0" in body
    assert "hello" in body and "world" in body


def test_browser_transcript_no_panel_passthrough(monkeypatch):
    monkeypatch.setattr(bt, "_fetch_panel", lambda vid: ([], "no_panel"))
    assert bt.browser_transcript("ABC") == ("", "no_panel")


def test_browser_transcript_blocked_passthrough(monkeypatch):
    monkeypatch.setattr(bt, "_fetch_panel", lambda vid: ([], "blocked"))
    assert bt.browser_transcript("ABC") == ("", "blocked")


def test_browser_transcript_ok_but_empty_becomes_no_panel(monkeypatch):
    # panel returned rows but all were noise/unparseable -> nothing to render
    monkeypatch.setattr(bt, "_fetch_panel", lambda vid: ([("bad", "")], "ok"))
    assert bt.browser_transcript("ABC") == ("", "no_panel")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_yt_browser_transcript.py -k browser_transcript -v`
Expected: FAIL — `AttributeError: module 'yt_browser_transcript' has no attribute 'browser_transcript'`

- [ ] **Step 3: Write minimal implementation**

Append to `bin/yt_browser_transcript.py`:

```python
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_yt_browser_transcript.py -v`
Expected: PASS (8 tests total)

- [ ] **Step 5: Commit**

```bash
git add bin/yt_browser_transcript.py tests/test_yt_browser_transcript.py
git commit -m "feat(youtube): browser_transcript orchestration + status contract"
```

---

### Task 3: Playwright `_fetch_panel` + reusable per-run browser session

**Files:**
- Modify: `bin/yt_browser_transcript.py`
- Test: `tests/test_yt_browser_transcript.py`

**Interfaces:**
- Consumes: Playwright (`from playwright.sync_api import sync_playwright`).
- Produces:
  - `_extract_panel_rows(page) -> list[tuple[str, str]]` — given a Playwright page with the transcript panel open, return `[(ts_label, text)]` from `ytd-transcript-segment-renderer` rows. Pure DOM read; tested with a fake page object.
  - `_open_transcript(page) -> bool` — click the "...more" → "Show transcript" affordance (fallback to the description "Show transcript" button); return `True` if the panel opened. Tested with a fake page.
  - real `_fetch_panel(video_id)` — navigates, opens panel, scrapes, classifies status; reuses a module-level singleton browser via `_get_page()`.
  - `shutdown()` — close the singleton browser/playwright; safe to call when none exists.

- [ ] **Step 1: Write the failing test (fake-page DOM extraction, no real browser)**

```python
class _FakeLocator:
    def __init__(self, rows): self._rows = rows
    def all(self): return self._rows


class _FakeRow:
    def __init__(self, ts, text): self._ts, self._text = ts, text
    def inner_text(self): return f"{self._ts}\n{self._text}"


class _FakePage:
    def __init__(self, rows): self._rows = rows
    def locator(self, sel):
        return _FakeLocator([_FakeRow(t, x) for t, x in self._rows])


def test_extract_panel_rows_parses_segments():
    page = _FakePage([("0:00", "intro line"), ("1:23", "next line")])
    assert bt._extract_panel_rows(page) == [("0:00", "intro line"), ("1:23", "next line")]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_yt_browser_transcript.py -k extract_panel_rows -v`
Expected: FAIL — `AttributeError: ... has no attribute '_extract_panel_rows'`

- [ ] **Step 3: Write minimal implementation**

Append to `bin/yt_browser_transcript.py`:

```python
import os
import random
import time

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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_yt_browser_transcript.py -v`
Expected: PASS (9 tests). No browser launched (only `_extract_panel_rows` exercised, with a fake page).

- [ ] **Step 5: Commit**

```bash
git add bin/yt_browser_transcript.py tests/test_yt_browser_transcript.py
git commit -m "feat(youtube): Playwright _fetch_panel + per-run browser session + pacing"
```

---

### Task 4: Make the browser tier primary in `extract_transcript`

**Files:**
- Modify: `bin/youtube_client.py:226-240` (the `extract_transcript` function)
- Test: `tests/test_youtube_client.py`

**Interfaces:**
- Consumes: `yt_browser_transcript.browser_transcript`; existing `_caption_transcript`, `_whisper_transcript`, `_whisper_enabled`.
- Produces: reordered `extract_transcript(video_id, whisper_on_blocked=False) -> (body, status)` — browser-first when `CORPUS_YT_BROWSER != "0"`.

- [ ] **Step 1: Write the failing test**

```python
# add to tests/test_youtube_client.py
def test_browser_primary_ok_skips_caption_and_whisper(monkeypatch):
    import yt_browser_transcript as bt
    monkeypatch.setenv("CORPUS_YT_BROWSER", "1")
    monkeypatch.setattr(bt, "browser_transcript", lambda v: ("BROWSER BODY", "ok"))
    monkeypatch.setattr(yc, "_caption_transcript",
                        lambda v: (_ for _ in ()).throw(AssertionError("captions called")))
    body, status = yc.extract_transcript("VID")
    assert (body, status) == ("BROWSER BODY", "ok")


def test_browser_no_panel_falls_to_whisper(monkeypatch):
    import yt_browser_transcript as bt
    monkeypatch.setenv("CORPUS_YT_BROWSER", "1")
    monkeypatch.setattr(bt, "browser_transcript", lambda v: ("", "no_panel"))
    monkeypatch.setattr(yc, "_whisper_enabled", lambda: True)
    monkeypatch.setattr(yc, "_whisper_transcript", lambda v: "WHISPER BODY")
    body, status = yc.extract_transcript("VID")
    assert (body, status) == ("WHISPER BODY", "ok")


def test_browser_blocked_falls_to_caption_fallback(monkeypatch):
    import yt_browser_transcript as bt
    monkeypatch.setenv("CORPUS_YT_BROWSER", "1")
    monkeypatch.setattr(bt, "browser_transcript", lambda v: ("", "blocked"))
    monkeypatch.setattr(yc, "_caption_transcript", lambda v: ("CAPTION BODY", "ok"))
    body, status = yc.extract_transcript("VID")
    assert (body, status) == ("CAPTION BODY", "ok")


def test_browser_disabled_uses_old_path(monkeypatch):
    import yt_browser_transcript as bt
    monkeypatch.setenv("CORPUS_YT_BROWSER", "0")
    monkeypatch.setattr(bt, "browser_transcript",
                        lambda v: (_ for _ in ()).throw(AssertionError("browser called")))
    monkeypatch.setattr(yc, "_caption_transcript", lambda v: ("CAPTION BODY", "ok"))
    body, status = yc.extract_transcript("VID")
    assert (body, status) == ("CAPTION BODY", "ok")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_youtube_client.py -k "browser_" -v`
Expected: FAIL — old `extract_transcript` ignores the browser tier (e.g. `captions called` AssertionError, or wrong body).

- [ ] **Step 3: Write minimal implementation**

Replace `extract_transcript` in `bin/youtube_client.py` with:

```python
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
```

- [ ] **Step 4: Run the full youtube_client suite**

Run: `python3 -m pytest tests/test_youtube_client.py tests/test_youtube_whisper.py -v`
Expected: PASS — new browser tests pass; pre-existing caption/whisper tests still pass (the legacy block is unchanged, just guarded).

- [ ] **Step 5: Commit**

```bash
git add bin/youtube_client.py tests/test_youtube_client.py
git commit -m "feat(youtube): browser scrape is now the primary transcript path"
```

---

### Task 5: Browser mode in the backlog drainer + per-run teardown/pacing

**Files:**
- Modify: `bin/whisper_rescue.py`
- Modify: `bin/youtube_client.py` (call `bt.shutdown()` + `human_delay` in `cmd_run`)
- Test: `tests/test_youtube_whisper.py`

**Interfaces:**
- Consumes: `yt_browser_transcript.browser_transcript`, `.shutdown`, `.human_delay`; existing `rescue_one`.
- Produces: `rescue_one(stub_path, *, whisper, whisper_direct=False, browser=False)` — when `browser=True`, fetch via `browser_transcript` first; `cmd_run` adds `--browser`.

- [ ] **Step 1: Write the failing test**

```python
# add to tests/test_youtube_whisper.py
import importlib
wr = importlib.import_module("whisper_rescue")


def test_rescue_one_browser_mode_upgrades_stub(monkeypatch, tmp_path):
    import yt_browser_transcript as bt
    stub = tmp_path / "vid.md"
    stub.write_text("---\nyoutube_video_id: VID\ntranscript_status: blocked\n---\nstub\n")
    monkeypatch.setattr(bt, "browser_transcript", lambda v: ("> marker\n\nBODY", "ok"))
    result = wr.rescue_one(stub, whisper=False, browser=True)
    assert result == "ok"
    assert "BODY" in stub.read_text()
    assert "transcript_status: ok" in stub.read_text()


def test_rescue_one_browser_already_ok_skipped(monkeypatch, tmp_path):
    stub = tmp_path / "vid.md"
    stub.write_text("---\nyoutube_video_id: VID\ntranscript_status: ok\n---\nbody\n")
    assert wr.rescue_one(stub, whisper=False, browser=True) == "already_ok"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_youtube_whisper.py -k rescue_one_browser -v`
Expected: FAIL — `rescue_one()` has no `browser` keyword (`TypeError: unexpected keyword argument 'browser'`).

- [ ] **Step 3: Write minimal implementation**

In `bin/whisper_rescue.py`, update `rescue_one` to branch on `browser` before the existing logic:

```python
def rescue_one(stub_path: Path, *, whisper: bool, whisper_direct: bool = False,
               browser: bool = False) -> str:
    head = stub_path.read_text(encoding="utf-8", errors="ignore")
    if re.search(r"^transcript_status:\s*ok", head, re.M):
        return "already_ok"
    m = re.search(r"^youtube_video_id:\s*(\S+)", head, re.M)
    if not m:
        return "no_id"
    if browser:
        import yt_browser_transcript as bt
        body, status = bt.browser_transcript(m.group(1))
    elif whisper_direct:
        body = yc._whisper_transcript(m.group(1))
        status = "ok" if body else "failed"
    else:
        body, status = yc.extract_transcript(m.group(1), whisper_on_blocked=whisper)
    if status != "ok" or not body:
        return status or "failed"
    # ... existing in-place rewrite of the stub (unchanged below) ...
```

Add a `--browser` flag in `whisper_rescue.py`'s argument parser and thread `browser=args.browser` into the `rescue_one` call (mirror the existing `--whisper` wiring). After the rescue loop, call `bt.shutdown()` in a `finally` if `args.browser`.

In `bin/youtube_client.py` `cmd_run`, replace the throttle line so browser runs pace + tear down:

```python
                if args.sleep and fetched:
                    time.sleep(args.sleep)
    # ... after the for-loops, before building `out`:
    if _browser_enabled():
        import yt_browser_transcript as bt
        bt.shutdown()
```

- [ ] **Step 4: Run the suites**

Run: `python3 -m pytest tests/test_youtube_whisper.py tests/test_youtube_client.py -v`
Expected: PASS — browser rescue tests pass; existing whisper-rescue and run tests unaffected.

- [ ] **Step 5: Commit**

```bash
git add bin/whisper_rescue.py bin/youtube_client.py tests/test_youtube_whisper.py
git commit -m "feat(youtube): --browser backlog rescue + per-run browser teardown"
```

---

### Task 6: Dependency + ops docs, and a gated live smoke test

**Files:**
- Modify: `README.md` (or the youtube setup doc) — Playwright install line.
- Create: `docs/solutions/youtube/browser-transcript.md` (engineering note per CLAUDE.md §14.5).
- Test: `tests/test_yt_browser_transcript.py` (one opt-in network test).

**Interfaces:**
- Consumes: everything above.
- Produces: documented setup + an opt-in end-to-end check.

- [ ] **Step 1: Write the gated live test**

```python
import os
import pytest


@pytest.mark.skipif(os.environ.get("CORPUS_YT_LIVE") != "1",
                    reason="set CORPUS_YT_LIVE=1 to run the real browser smoke test")
def test_live_browser_transcript_known_video():
    # 'jNQXAC9IVRw' = "Me at the zoo" (first YouTube video, stable, has captions)
    body, status = bt.browser_transcript("jNQXAC9IVRw")
    bt.shutdown()
    assert status in ("ok", "no_panel")
    if status == "ok":
        assert body.startswith(bt.PROVENANCE)
```

- [ ] **Step 2: Confirm it skips by default**

Run: `python3 -m pytest tests/test_yt_browser_transcript.py -k live -v`
Expected: SKIPPED (1 skipped) — no browser launched in normal/CI runs.

- [ ] **Step 3: Write the docs**

Add to `README.md` setup section:

```bash
# Browser transcript tier (logged-out Playwright)
python3 -m pip install playwright
python3 -m playwright install chromium
```

Create `docs/solutions/youtube/browser-transcript.md` with YAML frontmatter
(`module: youtube`, `tags: [transcript, playwright, anti-bot]`, `problem_type: rate-limit`)
documenting: why the browser tier exists (backend bot-gate), the `ok|no_panel|blocked|failed`
contract, the `CORPUS_YT_BROWSER` / `CORPUS_YT_LIVE` env vars, the logged-out pacing/cap
strategy, and the DOM-churn maintenance risk (selectors live only in `yt_browser_transcript.py`).

- [ ] **Step 4: Manually run the live smoke test once**

Run: `CORPUS_YT_LIVE=1 python3 -m pytest tests/test_yt_browser_transcript.py -k live -v`
Expected: PASS — real Chromium scrapes "Me at the zoo", returns `ok` with the provenance marker (or `no_panel` if YouTube changed the affordance, which signals selector maintenance is needed).

- [ ] **Step 5: Commit**

```bash
git add README.md docs/solutions/youtube/browser-transcript.md tests/test_yt_browser_transcript.py
git commit -m "docs(youtube): browser transcript setup + gated live smoke test"
```

---

## Self-Review

**Spec coverage:**
- Component 1 (`yt_browser_transcript.py`, status contract, timestamp parse, provenance, `transcript_to_markdown` reuse) → Tasks 1–3. ✓
- Component 2 (browser-primary waterfall, `CORPUS_YT_BROWSER` flag, legacy demoted to deep fallback) → Task 4. ✓
- Component 3 (backlog drainer `--browser` on `whisper_rescue.py`) → Task 5. ✓
- Pacing/anti-detection (reused context, UA/viewport, `human_delay`, per-run teardown) → Tasks 3 & 5. ✓
- Per-run cap for nightly → already exists as `--max` on `youtube_client.py run`; reused, no new code (noted here so it isn't mistaken for a gap).
- Error handling (`failed` on any exception, no partials, `blocked` early signal, `finally` teardown) → Tasks 2, 3, 5. ✓
- Testing (unit parser, status mapping, drainer idempotency, gated live) → Tasks 1–6. ✓
- Dependencies (Playwright + Chromium, documented) → Task 6. ✓
- Out-of-scope items (logged-in, cloud, proxies) → not implemented, correct.

**Placeholder scan:** every code step shows complete code; the one prose-only step (Task 6 docs) is documentation content, not code. No TBD/TODO. ✓

**Type consistency:** `browser_transcript -> (str, str)`, `_fetch_panel -> (list[tuple[str,str]], str)`, `parse_ts -> int|None`, `lines_to_snippets -> list[dict]`, `rescue_one(..., browser=False) -> str`, `shutdown() -> None`, `human_delay() -> None` — used consistently across Tasks 1–6. ✓

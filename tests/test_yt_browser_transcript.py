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

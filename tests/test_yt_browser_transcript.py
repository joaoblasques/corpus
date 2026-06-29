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

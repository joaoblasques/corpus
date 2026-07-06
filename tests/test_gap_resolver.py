#!/usr/bin/env python3
"""Tests for bin/gap_resolver.py — gap parsing, once-per-gap ledger, bounded resolver."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import gap_resolver as gr  # noqa: E402

LOG = """# Corpus Log

## 2026-07-05
* **Query (origin: helix)**: Crypto momentum: Sharpe, walk-forward, Kelly sizing
* **Ingest**: something else entirely

## 2026-07-01
* **Query**: Older gap without origin
"""


def test_parse_gaps_order_and_origin():
    gaps = gr.parse_gaps(LOG)
    assert len(gaps) == 2
    assert gaps[0]["origin"] == "helix"
    assert gaps[0]["question"].startswith("Crypto momentum")
    assert gaps[1]["origin"] == ""          # origin-less form still parses


def test_next_gap_skips_dispatched():
    gaps = gr.parse_gaps(LOG)
    dispatched = {gr._hash(gaps[0]["question"])}
    nxt = gr.next_gap(LOG, dispatched)
    assert nxt["question"] == "Older gap without origin"
    # everything dispatched -> None
    assert gr.next_gap(LOG, {gr._hash(g["question"]) for g in gaps}) is None


def test_resolve_gap_parses_queued_count():
    def fake_run(cmd, **kw):
        assert "--allowedTools" in cmd and "WebSearch" in cmd
        p = MagicMock(); p.returncode = 0; p.stdout = "searching...\nQUEUED 3 sources."; p.stderr = ""
        return p

    res = gr.resolve_gap("some question", model="claude-sonnet-4-6", _run=fake_run)
    assert res == {"ok": True, "queued": 3, "detail": res["detail"]}


def test_resolve_gap_failure_recorded_not_raised():
    def fake_run(cmd, **kw):
        p = MagicMock(); p.returncode = 1; p.stdout = ""; p.stderr = "boom"
        return p

    res = gr.resolve_gap("q", model="m", _run=fake_run)
    assert res["ok"] is False and res["queued"] == 0


def test_ledger_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr(gr, "LEDGER", tmp_path / ".gaps.txt")
    assert gr._dispatched() == set()
    gr._mark("question one", "ok")
    gr._mark("question two", "failed")
    d = gr._dispatched()
    assert gr._hash("question one") in d and gr._hash("question two") in d

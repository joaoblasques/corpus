#!/usr/bin/env python3
"""Tests for quick_ingest_docs — OpenRouter rate-limit circuit breaker + wall-clock budget.

Regression for the 2026-07-08..10 DocsQuick timeouts: the free OpenRouter tier began returning
429s with ~30s retry-after, and with no breaker/budget every stub paid that penalty before
falling back to Groq, blowing the 2400s subprocess timeout (run hard-killed, tally lost)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import quick_ingest_docs as qd  # noqa: E402

STUB = "---\ntitle: Test Post\nsource: web\nsource_url: https://x.com/a\n---\n\n" + ("word " * 200)


def test_circuit_breaker_trips_and_skips_openrouter_after_429(tmp_path, monkeypatch):
    calls = []

    def fake_llm(title, source, content, *, backend, model, fallback_domain, attempts):
        calls.append(backend)
        if backend == "openrouter":
            raise qd._RateLimited("429")
        return {"domain": "data-engineering", "summary": "s", "topics": ["t"]}

    monkeypatch.setattr(qd, "_llm_summary", fake_llm)
    state: dict = {}
    f = tmp_path / "web-a.md"

    r1 = qd.process(f, STUB, "web", backend="openrouter", model="m", today="2026-07-10",
                    dry_run=True, state=state)
    assert r1.startswith("DRY")
    assert state["openrouter_disabled"] is True       # breaker tripped
    assert calls == ["openrouter", "groq"]            # tried OR once, fell back to Groq

    calls.clear()
    qd.process(f, STUB, "web", backend="openrouter", model="m", today="2026-07-10",
               dry_run=True, state=state)
    assert calls == ["groq"]                          # OpenRouter skipped for the rest of the run


def test_time_budget_stops_early_and_emits_tally(tmp_path, monkeypatch, capsys):
    stubs = [(tmp_path / f"web-{i}.md", STUB, "web") for i in range(5)]
    monkeypatch.setattr(qd, "iter_stubs", lambda channels, sources: iter(stubs))
    monkeypatch.setattr(qd, "process", lambda *a, **k: "ok:data-engineering")
    # monotonic: start=0, first check=0 (under budget), second check=100 (over 50s budget)
    seq = iter([0.0, 0.0, 100.0, 100.0, 100.0])
    monkeypatch.setattr(qd.time, "monotonic", lambda: next(seq))

    qd.main(["--channel", "web", "--time-budget", "50", "--max", "5", "--sleep", "0"])
    tally_line = [l for l in capsys.readouterr().out.splitlines() if '"tally"' in l][-1]
    d = json.loads(tally_line)
    assert d["stopped_early"] is True
    assert d["processed"] == 1                          # stopped after the first stub


def test_llm_summary_raises_ratelimited_on_pure_429(monkeypatch):
    class Fake429:
        status_code = 429
        headers = {"retry-after": "0"}

        def raise_for_status(self):
            pass

        def json(self):
            return {}

    monkeypatch.setattr(qd, "_openrouter_key", lambda env_file="~/.config/watch/.env": "fake-key")
    monkeypatch.setattr(qd.time, "sleep", lambda *a, **k: None)
    import requests
    monkeypatch.setattr(requests, "post", lambda *a, **k: Fake429())

    with pytest.raises(qd._RateLimited):
        qd._llm_summary("t", "web", "content", backend="openrouter", model="m",
                        fallback_domain="data-engineering", attempts=2)

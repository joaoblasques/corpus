# tests/test_llm.py
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import llm_config as cfg  # noqa: E402


def test_config_has_mechanical_tier_model():
    assert cfg.TIER_MODEL["mechanical"] == "qwen2.5:3b"
    assert cfg.TIER_TIMEOUT["mechanical"] >= 30
    assert cfg.OLLAMA_HOST.startswith("http")
    assert cfg.PREFER_LOCAL is True
    assert cfg.MECHANICAL_HAIKU_FALLBACK is False
    assert cfg.USAGE_LOG.endswith(".jsonl")


import json
from unittest.mock import patch
import llm  # noqa: E402


class _FakeResp:
    """Minimal context-manager stand-in for urllib.request.urlopen()."""
    def __init__(self, payload):
        self._data = json.dumps(payload).encode()
    def __enter__(self):
        return self
    def __exit__(self, *a):
        return False
    def read(self):
        return self._data


def test_complete_mechanical_returns_local_text(tmp_path):
    payload = {"response": '{"scores":[{"index":0,"score":7}]}'}
    with patch.object(llm.urllib.request, "urlopen", return_value=_FakeResp(payload)):
        res = llm.complete("score these", tier="mechanical", task="unit",
                           log_path=tmp_path / "u.jsonl")
    assert res["ok"] is True
    assert res["provider"] == "ollama"
    assert res["model"] == "qwen2.5:3b"
    assert '"scores"' in res["text"]
    assert res["error"] is None


import urllib.error


def test_complete_returns_not_ok_when_ollama_down(tmp_path):
    boom = urllib.error.URLError("Connection refused")
    with patch.object(llm.urllib.request, "urlopen", side_effect=boom):
        res = llm.complete("x", tier="mechanical", task="unit",
                           log_path=tmp_path / "u.jsonl")
    assert res["ok"] is False
    assert res["provider"] is None
    assert "ollama" in res["error"]


def test_complete_returns_not_ok_on_timeout(tmp_path):
    with patch.object(llm.urllib.request, "urlopen", side_effect=TimeoutError("slow")):
        res = llm.complete("x", tier="mechanical", task="unit",
                           log_path=tmp_path / "u.jsonl")
    assert res["ok"] is False
    assert "ollama" in res["error"]


def test_prefer_local_false_skips_ollama(tmp_path, monkeypatch):
    monkeypatch.setattr(llm.cfg, "PREFER_LOCAL", False)
    # urlopen must NOT be called when PREFER_LOCAL is off
    with patch.object(llm.urllib.request, "urlopen", side_effect=AssertionError("called")):
        res = llm.complete("x", tier="mechanical", task="unit",
                           log_path=tmp_path / "u.jsonl")
    assert res["ok"] is False
    assert res["provider"] is None


def test_complete_appends_usage_log(tmp_path):
    log = tmp_path / "u.jsonl"
    payload = {"response": "ok"}
    with patch.object(llm.urllib.request, "urlopen", return_value=_FakeResp(payload)):
        llm.complete("x", tier="mechanical", task="rank_links", log_path=log)
    lines = log.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    rec = json.loads(lines[0])
    assert rec["task"] == "rank_links"
    assert rec["tier"] == "mechanical"
    assert rec["provider"] == "ollama"
    assert rec["ok"] is True
    assert "latency_ms" in rec and "at" in rec


def test_usage_log_records_failures_too(tmp_path):
    log = tmp_path / "u.jsonl"
    with patch.object(llm.urllib.request, "urlopen",
                      side_effect=urllib.error.URLError("down")):
        llm.complete("x", tier="mechanical", task="rank_links", log_path=log)
    rec = json.loads(log.read_text(encoding="utf-8").strip())
    assert rec["ok"] is False
    assert rec["provider"] is None

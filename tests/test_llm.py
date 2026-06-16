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

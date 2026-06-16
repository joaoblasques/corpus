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

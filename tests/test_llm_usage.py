# tests/test_llm_usage.py
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import llm_usage as lu  # noqa: E402


def test_summarize_counts_by_provider(tmp_path):
    log = tmp_path / "u.jsonl"
    rows = [
        {"provider": "ollama", "ok": True, "latency_ms": 800, "tier": "mechanical"},
        {"provider": "ollama", "ok": True, "latency_ms": 1200, "tier": "mechanical"},
        {"provider": "ollama", "ok": False, "latency_ms": 30, "tier": "mechanical"},
        {"provider": "anthropic", "ok": True, "latency_ms": 500, "tier": "mechanical"},
    ]
    log.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    s = lu.summarize(log)
    assert s["total"] == 4
    assert s["by_provider"]["ollama"] == 3
    assert s["by_provider"]["anthropic"] == 1
    assert s["local_ok"] == 2
    assert s["local_fail"] == 1


def test_summarize_missing_file_is_empty(tmp_path):
    s = lu.summarize(tmp_path / "nope.jsonl")
    assert s["total"] == 0

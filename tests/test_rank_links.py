import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import rank_links as rl  # noqa: E402


def _cands(n):
    return [{"url": f"https://x.example.com/{i}", "description": f"item {i}"} for i in range(n)]


def test_rank_applies_floor(monkeypatch):
    monkeypatch.setattr(rl, "score_candidates", lambda c: [9, 2, 7])
    out = rl.rank(_cands(3), max_links=10, floor=4)
    by_url = {d["url"]: d for d in out}
    assert by_url["https://x.example.com/1"]["fetch"] is False
    assert by_url["https://x.example.com/1"]["reason"] == "low-utility"
    assert by_url["https://x.example.com/0"]["fetch"] is True


def test_rank_caps_top_n(monkeypatch):
    monkeypatch.setattr(rl, "score_candidates", lambda c: [8] * 12)
    out = rl.rank(_cands(12), max_links=10, floor=4)
    assert sum(1 for d in out if d["fetch"]) == 10
    assert sum(1 for d in out if d["reason"] == "over-cap") == 2


def test_rank_fallback_used_without_key(monkeypatch):
    monkeypatch.setattr(rl, "load_env", lambda *a, **k: None)
    import llm
    monkeypatch.setattr(
        llm, "complete",
        lambda *a, **k: {"text": "", "provider": None, "model": None,
                         "ok": False, "error": "ollama: down"},
    )
    scores = rl.score_candidates([{"url": "https://github.com/x/y", "description": "tutorial"}])
    assert scores[0] >= 8  # heuristic path


def test_score_candidates_uses_router_local(monkeypatch):
    """When the router returns ok=True with scores JSON, those scores are used."""
    monkeypatch.setattr(rl, "load_env", lambda *a, **k: None)
    import llm
    monkeypatch.setattr(
        llm, "complete",
        lambda *a, **k: {"text": '{"scores":[{"index":0,"score":9}]}',
                         "provider": "ollama", "model": "qwen2.5:3b",
                         "ok": True, "error": None},
    )
    scores = rl.score_candidates([{"url": "https://x/y", "description": "deep tutorial"}])
    assert scores == [9]


def test_score_candidates_falls_back_to_heuristic_when_router_not_ok(monkeypatch):
    """When the router returns ok=False, fall back to the heuristic scorer."""
    monkeypatch.setattr(rl, "load_env", lambda *a, **k: None)
    import llm
    monkeypatch.setattr(
        llm, "complete",
        lambda *a, **k: {"text": "", "provider": None, "model": None,
                         "ok": False, "error": "ollama: down"},
    )
    scores = rl.score_candidates([{"url": "https://github.com/x/y", "description": "tutorial"}])
    assert scores[0] >= 8  # heuristic path for a GitHub tutorial


def test_rank_sorts_by_score_desc(monkeypatch):
    monkeypatch.setattr(rl, "score_candidates", lambda c: [3, 9, 6])
    out = rl.rank(_cands(3), max_links=10, floor=0)
    assert [d["score"] for d in out] == [9, 6, 3]

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
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setattr(rl, "load_env", lambda *a, **k: None)
    scores = rl.score_candidates([{"url": "https://github.com/x/y", "description": "tutorial"}])
    assert scores[0] >= 8  # heuristic path


def test_rank_sorts_by_score_desc(monkeypatch):
    monkeypatch.setattr(rl, "score_candidates", lambda c: [3, 9, 6])
    out = rl.rank(_cands(3), max_links=10, floor=0)
    assert [d["score"] for d in out] == [9, 6, 3]

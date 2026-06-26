from __future__ import annotations
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import collect_github  # noqa: E402


def test_already_collected_consults_ledger(monkeypatch, tmp_path):
    # no raw/ dirs match, but the ledger says it's digested
    monkeypatch.setattr(collect_github.github_ledger, "is_digested", lambda fn, lp=None: fn == "o/n")
    assert collect_github.already_collected("o/n", dirs=[tmp_path]) is True
    assert collect_github.already_collected("o/other", dirs=[tmp_path]) is False


def test_write_collected_marks_ledger(monkeypatch, tmp_path):
    marked = []
    monkeypatch.setattr(collect_github.github_ledger, "is_digested", lambda fn, lp=None: False)
    monkeypatch.setattr(collect_github.github_ledger, "mark_digested", lambda fn, lp=None: marked.append(fn))
    repo = {"full_name": "o/n", "description": "d", "topics": [], "language": "Py", "stars": 1}
    res = collect_github.write_collected(repo, collected_at="2026-06-26", inbox=tmp_path, dedup_dirs=[tmp_path])
    assert res["status"] == "written"
    assert marked == ["o/n"]

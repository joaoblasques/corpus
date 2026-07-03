import datetime
import json
import sys
import types
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import weekly_synthesis as ws  # noqa: E402


def _proc(returncode=0, stdout="", stderr=""):
    return types.SimpleNamespace(returncode=returncode, stdout=stdout, stderr=stderr)


# --- opus_available probe (fails closed) ---
def test_opus_available_true_on_clean_success():
    run = lambda *a, **k: _proc(0, json.dumps({"is_error": False, "result": "OK"}))
    assert ws.opus_available(_subprocess_run=run) is True


def test_opus_available_false_on_is_error():
    run = lambda *a, **k: _proc(0, json.dumps({"is_error": True, "result": "rate limited"}))
    assert ws.opus_available(_subprocess_run=run) is False


def test_opus_available_false_on_nonzero_exit():
    assert ws.opus_available(_subprocess_run=lambda *a, **k: _proc(1, "")) is False


def test_opus_available_false_on_exception():
    def run(*a, **k):
        raise RuntimeError("boom")
    assert ws.opus_available(_subprocess_run=run) is False


# --- recent_pages selection ---
def test_recent_pages_selects_window_and_skips_catalog(tmp_path):
    c = tmp_path / "corpus" / "d"
    c.mkdir(parents=True)
    (c / "fresh.md").write_text("---\ntype: concept\nupdated: 2026-06-18\n---\nx", encoding="utf-8")
    (c / "old.md").write_text("---\ntype: concept\nupdated: 2026-05-01\n---\nx", encoding="utf-8")
    # OKF reserved names at the corpus root: must be skipped even though they have updated: dates
    (tmp_path / "corpus" / "index.md").write_text("---\nupdated: 2026-06-18\n---\nx", encoding="utf-8")
    (tmp_path / "corpus" / "log.md").write_text("---\nupdated: 2026-06-18\n---\nx", encoding="utf-8")
    out = ws.recent_pages(since_days=7, _today=datetime.date(2026, 6, 19),
                          corpus_dir=tmp_path / "corpus")
    assert [p.name for p in out] == ["fresh.md"]   # old excluded; index.md/log.md skipped


def test_recent_pages_skips_okf_reserved_names(tmp_path):
    """recent_pages must explicitly skip index.md and log.md regardless of content."""
    c = tmp_path / "corpus"
    c.mkdir()
    # Add OKF reserved files with recent dates at root level
    (c / "index.md").write_text("---\nokf_version: '0.1'\nupdated: 2026-06-19\n---\ncatalog",
                                 encoding="utf-8")
    (c / "log.md").write_text("---\nupdated: 2026-06-19\n---\nlog entries", encoding="utf-8")
    # A real concept page
    (c / "real.md").write_text("---\ntype: concept\nupdated: 2026-06-19\n---\ncontent",
                               encoding="utf-8")
    out = ws.recent_pages(since_days=7, _today=datetime.date(2026, 6, 19), corpus_dir=c)
    names = [p.name for p in out]
    assert "real.md" in names, "real concept page should be included"
    assert "index.md" not in names, "index.md should be skipped (OKF reserved)"
    assert "log.md" not in names, "log.md should be skipped (OKF reserved)"


# --- run_synthesis short-circuit ---
def test_run_synthesis_no_pages_short_circuits():
    assert ws.run_synthesis([])["note"] == "no_recent_pages"


# --- guarded flow ---
def test_run_guarded_skips_when_opus_unavailable(monkeypatch, capsys):
    monkeypatch.setattr(ws, "opus_available", lambda **k: False)
    args = types.SimpleNamespace(force=False, dry_run=False, since_days=7, timeout=10)
    rc = ws._run_guarded(args)
    out = json.loads(capsys.readouterr().out)
    assert rc == 0 and out["reason"] == "opus_unavailable_or_rate_limited"


def test_run_guarded_dry_run_does_not_invoke_pass(monkeypatch, capsys):
    monkeypatch.setattr(ws, "opus_available", lambda **k: True)
    monkeypatch.setattr(ws, "recent_pages", lambda *a, **k: [Path("a.md"), Path("b.md")])
    called = {"synth": False}
    monkeypatch.setattr(ws, "run_synthesis",
                        lambda *a, **k: called.__setitem__("synth", True) or {})
    args = types.SimpleNamespace(force=False, dry_run=True, since_days=7, timeout=10, max_pages=30)
    rc = ws._run_guarded(args)
    out = json.loads(capsys.readouterr().out)
    assert rc == 0 and out["dry_run"] is True and out["recent_pages"] == 2
    assert called["synth"] is False


def test_commit_synthesis_nothing_to_commit():
    def run(cmd, **k):
        return _proc(0, "")   # clean tree on `status --porcelain`
    assert ws.commit_synthesis("2026-06-19T13:00", _subprocess_run=run)["status"] == "nothing-to-commit"


def test_recent_pages_caps_to_limit_newest_first(tmp_path):
    c = tmp_path / "corpus"
    c.mkdir()
    for i, day in enumerate(["2026-06-15", "2026-06-17", "2026-06-19"]):
        (c / f"p{i}.md").write_text(f"---\nupdated: {day}\n---\nx", encoding="utf-8")
    out = ws.recent_pages(since_days=10, limit=2,
                          _today=datetime.date(2026, 6, 19), corpus_dir=c)
    assert [p.name for p in out] == ["p2.md", "p1.md"]   # newest two, newest first

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import github_discover as gd  # noqa: E402
import types  # noqa: E402


def _args(**kw):
    return types.SimpleNamespace(**kw)


def _wire(monkeypatch, tmp_path, *, starred=(), search=None, meta=None):
    """Point REVIEW/LEDGER at tmp + stub the GitHub calls."""
    monkeypatch.setattr(gd, "REVIEW", tmp_path / "GitHubs to review.md")
    monkeypatch.setattr(gd, "LEDGER", tmp_path / ".github_proposed.txt")
    monkeypatch.setattr(gd.gh, "gh_available", lambda *a, **k: True)
    monkeypatch.setattr(gd.gh, "list_starred", lambda *a, **k: [{"full_name": s} for s in starred])
    monkeypatch.setattr(gd.cg, "discover_topics", lambda: ["t"])
    monkeypatch.setattr(gd.gh, "search_repos", lambda *a, **k: (search or []))
    monkeypatch.setattr(gd, "repo_meta", lambda fn, **k: (meta or {}).get(
        fn, {"full_name": fn, "stars": 0, "language": "Py", "description": "d"}))


def test_propose_writes_tickable_lines_and_skips_starred_and_collected(tmp_path, monkeypatch, capsys):
    _wire(monkeypatch, tmp_path,
          starred=["owner/starred"],
          search=[{"full_name": "owner/new", "stars": 4200},
                  {"full_name": "owner/starred", "stars": 9000},
                  {"full_name": "owner/collected", "stars": 8000}])
    # rank preserves order minus starred/collected; already_collected flags one
    monkeypatch.setattr(gd.cg, "rank_candidates",
                        lambda cands, starred, ac: [(fn, s) for fn, s in
                                                    sorted(cands.items(), key=lambda x: -x[1])
                                                    if fn not in starred and not ac(fn)])
    monkeypatch.setattr(gd.cg, "already_collected", lambda fn, *a, **k: fn == "owner/collected")

    gd.cmd_propose(_args(max=15, dry_run=False))
    txt = gd.REVIEW.read_text()
    assert "- [ ] owner/new · ★4.2k · Py · d" in txt      # tickable, human-readable
    assert "owner/starred" not in txt                      # already starred → skipped
    assert "owner/collected" not in txt                    # already collected → skipped
    assert "owner/new" in gd.LEDGER.read_text()            # marked seen


def test_propose_dedups_against_review_and_ledger(tmp_path, monkeypatch, capsys):
    _wire(monkeypatch, tmp_path, search=[{"full_name": "o/a", "stars": 5000}])
    monkeypatch.setattr(gd.cg, "already_collected", lambda fn, *a, **k: False)
    monkeypatch.setattr(gd.cg, "rank_candidates",
                        lambda cands, starred, ac: sorted(cands.items(), key=lambda x: -x[1]))
    # o/a already in the review file → not re-proposed
    gd.REVIEW.write_text(gd.REVIEW_HEADER + "- [ ] o/a · ★5.0k\n", encoding="utf-8")
    gd.cmd_propose(_args(max=15, dry_run=False))
    assert gd.REVIEW.read_text().count("o/a") == 1


def test_propose_dry_run_writes_nothing(tmp_path, monkeypatch, capsys):
    _wire(monkeypatch, tmp_path, search=[{"full_name": "o/a", "stars": 5000}])
    monkeypatch.setattr(gd.cg, "already_collected", lambda fn, *a, **k: False)
    monkeypatch.setattr(gd.cg, "rank_candidates",
                        lambda cands, starred, ac: sorted(cands.items(), key=lambda x: -x[1]))
    gd.cmd_propose(_args(max=15, dry_run=True))
    assert not gd.REVIEW.exists()
    assert not gd.LEDGER.exists()


def test_promote_collects_only_ticked_repos(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(gd, "REVIEW", tmp_path / "GitHubs to review.md")
    monkeypatch.setattr(gd.gh, "gh_available", lambda *a, **k: True)
    gd.REVIEW.write_text(
        gd.REVIEW_HEADER
        + "- [x] owner/yes · ★9.0k\n"
        + "- [ ] owner/no · ★8.0k\n"
        + "- [x] owner/dup · ★7.0k\n", encoding="utf-8")
    monkeypatch.setattr(gd, "repo_meta", lambda fn, **k: {"full_name": fn, "stars": 1})
    monkeypatch.setattr(gd.gh, "fetch_repo", lambda item, **k: {**item, "readme": "r", "docs": []})
    monkeypatch.setattr(gd.cg, "already_collected", lambda fn, *a, **k: fn == "owner/dup")
    collected = []
    monkeypatch.setattr(gd.cg, "write_collected",
                        lambda repo, **k: (collected.append(repo["full_name"]) or
                                           {"status": "written", "path": "p"}))
    gd.cmd_promote(_args(max_docs=8, dry_run=False))
    assert collected == ["owner/yes"]              # only ticked + not-already-collected
    assert "owner/no" not in collected             # unticked → skipped
    assert "owner/dup" not in collected            # ticked but already collected → skipped


def test_promote_no_review_file_is_safe(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(gd, "REVIEW", tmp_path / "missing.md")
    gd.cmd_promote(_args(max_docs=8, dry_run=False))  # must not raise

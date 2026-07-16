import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import github_discover as gd  # noqa: E402
import types  # noqa: E402


def _args(**kw):
    return types.SimpleNamespace(**kw)


def _wire(monkeypatch, tmp_path, *, starred=(), search=None, meta=None, topics=("llm",)):
    """Point REVIEW/LEDGER at tmp + stub the GitHub calls. `topics` = search topics each repo is
    returned under (default one PRECISE topic so candidates pass the topic-admission rule)."""
    monkeypatch.setattr(gd, "REVIEW", tmp_path / "GitHubs to review.md")
    monkeypatch.setattr(gd, "LEDGER", tmp_path / ".github_proposed.txt")
    monkeypatch.setattr(gd.gh, "gh_available", lambda *a, **k: True)
    monkeypatch.setattr(gd.gh, "list_starred", lambda *a, **k: [{"full_name": s} for s in starred])
    monkeypatch.setattr(gd.cg, "discover_topics", lambda: list(topics))
    monkeypatch.setattr(gd.gh, "search_repos", lambda topic, **k: (search or []))
    monkeypatch.setattr(gd, "repo_meta", lambda fn, **k: (meta or {}).get(
        fn, {"full_name": fn, "stars": 0, "language": "Py", "description": "d", "topics": ["llm"]}))


def test_propose_writes_tickable_lines_and_skips_starred_and_collected(tmp_path, monkeypatch, capsys):
    _wire(monkeypatch, tmp_path,
          starred=["owner/starred"],
          search=[{"full_name": "owner/new", "stars": 4200},
                  {"full_name": "owner/starred", "stars": 9000},
                  {"full_name": "owner/collected", "stars": 8000}])
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
    gd.REVIEW.write_text(gd.REVIEW_HEADER + "- [ ] o/a · ★5.0k\n", encoding="utf-8")
    gd.cmd_propose(_args(max=15, dry_run=False))
    assert gd.REVIEW.read_text().count("o/a") == 1


def test_propose_dry_run_writes_nothing(tmp_path, monkeypatch, capsys):
    _wire(monkeypatch, tmp_path, search=[{"full_name": "o/a", "stars": 5000}])
    monkeypatch.setattr(gd.cg, "already_collected", lambda fn, *a, **k: False)
    gd.cmd_propose(_args(max=15, dry_run=True))
    assert not gd.REVIEW.exists()
    assert not gd.LEDGER.exists()


def test_propose_drops_lone_broad_topic_but_keeps_precise(tmp_path, monkeypatch, capsys):
    """The core handoff fix: apache/dubbo (only distributed-systems = broad) is dropped; a
    data-engineering repo (precise) is kept — even though dubbo has far more stars."""
    monkeypatch.setattr(gd, "REVIEW", tmp_path / "GitHubs to review.md")
    monkeypatch.setattr(gd, "LEDGER", tmp_path / ".github_proposed.txt")
    monkeypatch.setattr(gd.gh, "gh_available", lambda *a, **k: True)
    monkeypatch.setattr(gd.gh, "list_starred", lambda *a, **k: [])
    monkeypatch.setattr(gd.cg, "already_collected", lambda fn, *a, **k: False)
    monkeypatch.setattr(gd.cg, "discover_topics", lambda: ["distributed-systems", "data-engineering"])

    def search(topic, **k):
        return {"distributed-systems": [{"full_name": "apache/dubbo", "stars": 40000}],
                "data-engineering": [{"full_name": "dtc/zoomcamp", "stars": 25000}]}.get(topic, [])
    monkeypatch.setattr(gd.gh, "search_repos", search)
    monkeypatch.setattr(gd, "repo_meta", lambda fn, **k: {"full_name": fn, "stars": 0, "description": "d", "topics": []})

    gd.cmd_propose(_args(max=15, dry_run=False))
    txt = gd.REVIEW.read_text()
    assert "apache/dubbo" not in txt        # lone broad topic → dropped despite 40k stars
    assert "dtc/zoomcamp" in txt            # precise topic → kept


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


def test_topic_admits_precise_or_two_total():
    assert gd._topic_admits({"llm"})                                    # 1 precise
    assert gd._topic_admits({"data-engineering"})                       # 1 precise
    assert not gd._topic_admits({"distributed-systems"})                # 1 broad → dropped (dubbo)
    assert not gd._topic_admits({"developer-tools"})                    # 1 broad → dropped (Files)
    assert gd._topic_admits({"distributed-systems", "developer-tools"}) # 2 broad → kept (system-design)
    assert not gd._topic_admits(set())                                  # nothing matched


def test_is_junk_blocks_only_the_clearest():
    assert gd._is_junk({"full_name": "x/system-prompts-leaks", "topics": ["llm"], "description": "leaked"})
    assert gd._is_junk({"full_name": "x/jailbreak-gpt", "topics": [], "description": "jailbreak prompts"})
    # an in-domain resource list is NOT hard-blocked (relevance is governed by _topic_admits);
    # and it must NOT be language-filtered just for being tagged Java
    assert not gd._is_junk({"full_name": "ashishps1/awesome-system-design-resources",
                            "topics": ["Java"], "description": "learn to design large-scale systems"})

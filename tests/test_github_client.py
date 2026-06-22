import base64
import json
import sys
import types
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import github_client as gh  # noqa: E402


def _proc(rc=0, stdout=""):
    return types.SimpleNamespace(returncode=rc, stdout=stdout, stderr="")


def _b64(s):
    return base64.b64encode(s.encode()).decode()


def test_gh_available():
    assert gh.gh_available(_run=lambda *a, **k: _proc(0)) is True
    assert gh.gh_available(_run=lambda *a, **k: _proc(1)) is False


def test_list_starred_parses_and_caps():
    data = [{"full_name": "a/b", "html_url": "u", "description": "d", "language": "Py",
             "stargazers_count": 5, "topics": ["t"], "default_branch": "main"},
            {"full_name": "c/d", "stargazers_count": 1}]
    run = lambda cmd, **k: _proc(0, json.dumps(data))
    out = gh.list_starred(_run=run)
    assert [r["full_name"] for r in out] == ["a/b", "c/d"]
    assert out[0]["stars"] == 5 and out[0]["topics"] == ["t"]
    assert gh.list_starred(max_n=1, _run=run)[0]["full_name"] == "a/b" and len(gh.list_starred(max_n=1, _run=run)) == 1


def test_fetch_repo_assembles_readme_docs_release():
    item = {"full_name": "a/b", "stars": 5}
    def run(cmd, **k):
        ep = cmd[2]  # ["gh","api","<endpoint>",...]
        if ep == "repos/a/b/readme":
            return _proc(0, json.dumps({"content": _b64("# Title\nbody")}))
        if ep == "repos/a/b/releases/latest":
            return _proc(0, json.dumps({"tag_name": "v1.2"}))
        if ep == "repos/a/b/contents":
            return _proc(0, json.dumps([{"name": "README.md", "path": "README.md", "content": _b64("x")},
                                        {"name": "CONTRIBUTING.md", "path": "CONTRIBUTING.md", "content": _b64("contrib")}]))
        if ep == "repos/a/b/contents/docs":
            return _proc(1, "")   # no docs folder
        return _proc(1, "")
    repo = gh.fetch_repo(item, _run=run)
    assert repo["readme"].startswith("# Title") and repo["latest_release"] == "v1.2"
    assert [d["path"] for d in repo["docs"]] == ["CONTRIBUTING.md"]   # README excluded
    assert repo["stars"] == 5   # metadata carried through from the item


def test_fetch_repo_tolerates_missing_pieces():
    repo = gh.fetch_repo({"full_name": "a/b"}, _run=lambda *a, **k: _proc(1, ""))
    assert repo["readme"] == "" and repo["latest_release"] == "" and repo["docs"] == []


def test_cmd_run_skips_when_gh_unavailable(monkeypatch, capsys):
    monkeypatch.setattr(gh, "gh_available", lambda **k: False)
    rc = gh.cmd_run(gh._args(["run"]))
    assert rc == 0 and "not configured" in capsys.readouterr().out


def test_cmd_run_collects_new_repos_only_no_unstar(monkeypatch, capsys):
    monkeypatch.setattr(gh, "gh_available", lambda **k: True)
    monkeypatch.setattr(gh, "list_starred", lambda mx=None, **k: [{"full_name": "a/b"}, {"full_name": "c/d"}])
    monkeypatch.setattr(gh.cg, "already_collected", lambda fn, dirs=None: fn == "a/b")  # a/b already in corpus
    monkeypatch.setattr(gh, "fetch_repo", lambda item, **k: {**item, "readme": "r"})
    written = []
    monkeypatch.setattr(gh.cg, "write_collected",
                        lambda repo, **k: written.append(repo["full_name"]) or {"status": "written", "path": "/x.md"})
    gh_calls = []
    monkeypatch.setattr(gh, "_gh", lambda args, **k: gh_calls.append(args) or _proc(0))
    rc = gh.cmd_run(gh._args(["run"]))
    out = capsys.readouterr().out
    assert rc == 0 and '"written": 1' in out and written == ["c/d"]   # a/b skipped (dup)
    assert not any("DELETE" in str(a) or "PUT" in str(a) for a in gh_calls)   # never un-stars


def test_cmd_run_dry_run_writes_nothing(monkeypatch, capsys):
    monkeypatch.setattr(gh, "gh_available", lambda **k: True)
    monkeypatch.setattr(gh, "list_starred", lambda mx=None, **k: [{"full_name": "c/d"}])
    monkeypatch.setattr(gh.cg, "already_collected", lambda fn, dirs=None: False)
    wrote = []
    monkeypatch.setattr(gh.cg, "write_collected", lambda *a, **k: wrote.append(1))
    rc = gh.cmd_run(gh._args(["run", "--dry-run"]))
    assert rc == 0 and wrote == [] and '"dry_run": true' in capsys.readouterr().out

import base64
import json
import sys
import types
import urllib.error
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import github_client as gh  # noqa: E402


def _proc(rc=0, stdout=""):
    return types.SimpleNamespace(returncode=rc, stdout=stdout, stderr="")


class _FakeResp:
    """Minimal urlopen() context-manager stand-in."""

    def __init__(self, body, link=None):
        self._body = body.encode() if isinstance(body, str) else body
        self.headers = {"Link": link} if link else {}

    def read(self):
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def test_http_api_single_get():
    out = gh._http_api(["api", "user"], "tok",
                       _opener=lambda req: _FakeResp(json.dumps({"login": "jonas"})))
    assert out.returncode == 0
    assert json.loads(out.stdout)["login"] == "jonas"


def test_http_api_paginates_via_link_header():
    pages = {
        "https://api.github.com/user/starred": _FakeResp(
            json.dumps([{"full_name": "a/b"}]),
            link='<https://api.github.com/user/starred?page=2>; rel="next"'),
        "https://api.github.com/user/starred?page=2": _FakeResp(
            json.dumps([{"full_name": "c/d"}])),
    }
    out = gh._http_api(["api", "user/starred", "--paginate"], "tok",
                       _opener=lambda req: pages[req.full_url])
    assert [x["full_name"] for x in json.loads(out.stdout)] == ["a/b", "c/d"]


def test_http_api_http_error_returns_rc1():
    def opener(req):
        raise urllib.error.HTTPError(req.full_url, 401, "Unauthorized", {}, None)
    assert gh._http_api(["api", "user"], "tok", _opener=opener).returncode == 1


def test_parse_api_args_extracts_method_endpoint_paginate():
    assert gh._parse_api_args(["api", "user"]) == ("GET", "user", False)
    assert gh._parse_api_args(["api", "user/starred", "--paginate"]) == ("GET", "user/starred", True)
    assert gh._parse_api_args(["api", "-X", "DELETE", "user/starred/a/b"]) == ("DELETE", "user/starred/a/b", False)


def test_http_api_delete_sends_delete_method_and_handles_204():
    seen = {}

    def opener(req):
        seen["method"] = req.get_method()
        seen["url"] = req.full_url
        return _FakeResp("")   # 204 No Content -> empty body

    out = gh._http_api(["api", "-X", "DELETE", "user/starred/owner/name"], "tok", _opener=opener)
    assert out.returncode == 0 and out.stdout == ""
    assert seen["method"] == "DELETE"
    assert seen["url"] == "https://api.github.com/user/starred/owner/name"


def test_unstar_issues_delete_and_reports_success():
    calls = []

    def fake_run(cmd, *a, **k):
        calls.append(cmd)
        return _proc(0)

    assert gh.unstar("owner/name", _run=fake_run) is True
    assert calls[0] == ["gh", "api", "-X", "DELETE", "user/starred/owner/name"]


def test_unstar_returns_false_on_failure():
    assert gh.unstar("owner/name", _run=lambda *a, **k: _proc(1)) is False


def test_cmd_reap_not_configured_when_gh_unavailable(monkeypatch, capsys):
    monkeypatch.setattr(gh, "gh_available", lambda **k: False)
    rc = gh.cmd_reap(gh._args(["reap"]))
    assert rc == 0 and "not configured" in capsys.readouterr().out


def test_cmd_reap_unstars_ingested_and_still_starred_only(monkeypatch, capsys):
    monkeypatch.setattr(gh, "gh_available", lambda **k: True)
    # corpus has digests for a/b and c/d ingested; e/f ingested but NO LONGER starred
    monkeypatch.setattr(gh.cg, "reapable", lambda dirs=None: ["a/b", "c/d", "e/f"])
    monkeypatch.setattr(gh, "list_starred",
                        lambda mx=None, **k: [{"full_name": "a/b"}, {"full_name": "c/d"}, {"full_name": "g/h"}])
    unstarred = []
    monkeypatch.setattr(gh, "unstar", lambda fn, **k: unstarred.append(fn) or True)
    rc = gh.cmd_reap(gh._args(["reap"]))
    out = json.loads(capsys.readouterr().out)
    assert rc == 0
    assert sorted(unstarred) == ["a/b", "c/d"]   # e/f not starred anymore; g/h not ingested
    assert out["unstarred"] == 2 and out["candidates"] == 2


def test_cmd_reap_dry_run_unstars_nothing(monkeypatch, capsys):
    monkeypatch.setattr(gh, "gh_available", lambda **k: True)
    monkeypatch.setattr(gh.cg, "reapable", lambda dirs=None: ["a/b"])
    monkeypatch.setattr(gh, "list_starred", lambda mx=None, **k: [{"full_name": "a/b"}])
    called = []
    monkeypatch.setattr(gh, "unstar", lambda fn, **k: called.append(fn) or True)
    rc = gh.cmd_reap(gh._args(["reap", "--dry-run"]))
    out = json.loads(capsys.readouterr().out)
    assert rc == 0 and called == [] and out["unstarred"] == 1 and out["dry_run"] is True


def test_cmd_reap_fails_closed_when_no_ingested(monkeypatch, capsys):
    monkeypatch.setattr(gh, "gh_available", lambda **k: True)
    monkeypatch.setattr(gh.cg, "reapable", lambda dirs=None: [])
    listed = []
    monkeypatch.setattr(gh, "list_starred", lambda mx=None, **k: listed.append(1) or [])
    rc = gh.cmd_reap(gh._args(["reap"]))
    out = json.loads(capsys.readouterr().out)
    assert rc == 0 and out["unstarred"] == 0 and listed == []   # no star-list call when nothing ingested


def test_gh_routes_to_http_when_token_present_and_no_run(monkeypatch):
    monkeypatch.setenv("GH_TOKEN", "tok")
    monkeypatch.setattr(gh, "_http_api", lambda args, token, **k: gh._Resp(0, '{"ok":1}'))
    r = gh._gh(["api", "user"])  # _run is None + token + api call -> HTTP transport
    assert r.returncode == 0 and json.loads(r.stdout)["ok"] == 1


def test_gh_uses_cli_path_when_run_injected_even_with_token(monkeypatch):
    monkeypatch.setenv("GH_TOKEN", "tok")
    calls = []
    gh._gh(["api", "user/starred", "--paginate"],
           _run=lambda cmd, *a, **k: calls.append(cmd) or _proc(0, "[]"))
    assert calls and calls[0][0] == "gh"   # injected seam always exercises the CLI


def test_next_link_parsing():
    h = '<https://api.github.com/x?page=2>; rel="next", <https://api.github.com/x?page=9>; rel="last"'
    assert gh._next_link(h) == "https://api.github.com/x?page=2"
    assert gh._next_link(None) is None


def _b64(s):
    return base64.b64encode(s.encode()).decode()


def test_gh_available():
    assert gh.gh_available(_run=lambda *a, **k: _proc(0)) is True
    assert gh.gh_available(_run=lambda *a, **k: _proc(1)) is False


def test_gh_available_probes_api_not_auth_status():
    # must reflect real API reachability (gh api user), not `gh auth status`,
    # which returns non-zero in a headless env-token sandbox even when api works
    seen = []

    def fake_run(cmd, *a, **k):
        seen.append(cmd)
        return _proc(0)

    gh.gh_available(_run=fake_run)
    assert seen and seen[0][:3] == ["gh", "api", "user"]
    assert "auth" not in seen[0]


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

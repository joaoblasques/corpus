import json
import sys
import types
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import x_client as xc  # noqa: E402


def _resp(status=200, payload=None):
    return types.SimpleNamespace(status_code=status, json=lambda: (payload or {}),
                                 raise_for_status=lambda: None)


def test_pkce_pair_differs_and_urlsafe():
    v, c = xc._pkce_pair()
    assert v and c and v != c and "=" not in c  # base64url, no padding


def test_x_available_false_without_token(monkeypatch):
    monkeypatch.setattr(xc, "_load_token", lambda: None)
    assert xc.x_available() is False


def test_list_bookmarks_parses_and_joins_author(monkeypatch):
    monkeypatch.setattr(xc, "_access_token", lambda **k: "TOK")
    monkeypatch.setattr(xc, "me", lambda **k: "42")
    page = {"data": [
                {"id": "1", "text": "short", "author_id": "9", "created_at": "2026-06-20T00:00:00Z",
                 "entities": {"urls": [{"expanded_url": "https://ex.com/a"}]}},
                {"id": "2", "note_tweet": {"text": "LONG FORM"}, "author_id": "9", "created_at": "x"}],
            "includes": {"users": [{"id": "9", "username": "jack"}]}}
    sess = types.SimpleNamespace(get=lambda url, **k: _resp(200, page))
    out = xc.list_bookmarks(_session=sess)
    assert [p["id"] for p in out] == ["1", "2"]
    assert out[0]["author"] == "jack" and out[0]["url"] == "https://x.com/jack/status/1"
    assert out[0]["links"] == ["https://ex.com/a"]
    assert out[1]["text"] == "LONG FORM"            # note_tweet preferred


def test_delete_bookmark(monkeypatch):
    monkeypatch.setattr(xc, "_access_token", lambda **k: "TOK")
    monkeypatch.setattr(xc, "me", lambda **k: "42")
    seen = {}
    def _del(url, **k):
        seen["url"] = url
        return _resp(200, {"data": {"bookmarked": False}})
    sess = types.SimpleNamespace(delete=_del)
    assert xc.delete_bookmark("1", _session=sess) is True
    assert seen["url"].endswith("/2/users/42/bookmarks/1")


def test_cmd_run_skips_when_unavailable(monkeypatch, capsys):
    monkeypatch.setattr(xc, "x_available", lambda: False)
    assert xc.cmd_run(xc._build_parser().parse_args(["run"])) == 0
    assert "not configured" in capsys.readouterr().out


def test_cmd_run_collects_new_only_never_deletes(monkeypatch, capsys):
    monkeypatch.setattr(xc, "x_available", lambda: True)
    monkeypatch.setattr(xc, "list_bookmarks", lambda mx=None, **k: [{"id": "1", "links": []}, {"id": "2", "links": []}])
    monkeypatch.setattr(xc.cx, "already_collected", lambda t, dirs=None: t == "1")
    written = []
    monkeypatch.setattr(xc.cx, "write_collected",
                        lambda post, **k: written.append(post["id"]) or {"status": "written", "path": "/x.md"})
    dels = []
    monkeypatch.setattr(xc, "delete_bookmark", lambda t, **k: dels.append(t) or True)
    assert xc.cmd_run(xc._build_parser().parse_args(["run"])) == 0
    assert written == ["2"] and dels == []                      # new only; collect never deletes
    assert '"written": 1' in capsys.readouterr().out


def test_cmd_reap_unbookmarks_only_reapable(monkeypatch, capsys):
    monkeypatch.setattr(xc, "x_available", lambda: True)
    monkeypatch.setattr(xc.cx, "reapable", lambda dirs=None: ["7", "8"])
    dels = []
    monkeypatch.setattr(xc, "delete_bookmark", lambda t, **k: dels.append(t) or True)
    assert xc.cmd_reap(xc._build_parser().parse_args(["reap"])) == 0
    assert dels == ["7", "8"] and '"unbookmarked": 2' in capsys.readouterr().out


def test_cmd_reap_dry_run_deletes_nothing(monkeypatch, capsys):
    monkeypatch.setattr(xc, "x_available", lambda: True)
    monkeypatch.setattr(xc.cx, "reapable", lambda dirs=None: ["7"])
    dels = []
    monkeypatch.setattr(xc, "delete_bookmark", lambda t, **k: dels.append(t) or True)
    xc.cmd_reap(xc._build_parser().parse_args(["reap", "--dry-run"]))
    assert dels == [] and '"dry_run": true' in capsys.readouterr().out

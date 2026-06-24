# X Bookmarks Collector Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development. Steps use `- [ ]`.

**Goal:** Collect the user's X (Twitter) bookmarks into the corpus (one doc per post + linked article), deduped by `tweet_id`, and un-bookmark each only after it's `corpus_ingested`.

**Architecture:** `bin/collect_x.py` (pure logic: dedup, document, reapable) + `bin/x_client.py` (X API v2 transport via an injectable `requests.Session` seam: OAuth2 PKCE token mgmt, list/delete bookmarks, CLI) — drained by the normal ingest, wired into the 2 AM job. Spec: `docs/superpowers/specs/2026-06-24-x-bookmarks-collection-design.md`.

**Tech Stack:** Python 3.12, pytest, `requests` (already used), the X API v2. All HTTP injected (`_session`) — no network in tests.

## Global Constraints
- Files: `bin/collect_x.py`, `bin/x_client.py`; tests `tests/test_collect_x.py`, `tests/test_x_client.py`.
- Channel `x`; sources → `raw/_inbox`, dedup against `raw/_inbox` + `raw/x`; dedup key frontmatter `tweet_id:`.
- **Collect never un-bookmarks.** Un-bookmark is a separate `reap` step, gated on `corpus_ingested: true` AND channel `x`.
- Scopes `tweet.read users.read bookmark.read bookmark.write offline.access`; token in `bin/x_token.json` (gitignored), app config `bin/x_app.json` (`client_id`, `redirect_uri`).
- API base `https://api.twitter.com/2`; token endpoint `https://api.twitter.com/2/oauth2/token`. All HTTP through an injectable `_session` (default a module `requests.Session()`).
- `--dry-run` writes/deletes nothing. Missing token → `x_available()` False → graceful skip.

---

### Task 1: `collect_x.py` — pure logic (dedup + document + reapable)

**Files:** Create `bin/collect_x.py`; Test `tests/test_collect_x.py`.

**Interfaces:** Produces `slugify(tweet_id)->str`, `already_collected(tweet_id, dirs=None)->bool`, `build_document(post, *, collected_at)->str`, `write_collected(post, *, collected_at, inbox=None, dedup_dirs=None)->dict`, `reapable(dirs=None)->list`, `DEDUP_DIRS`. `post` keys: `id, url, author, created_at, text, links(list[str]), articles(list[{url,text}])`.

- [ ] **Step 1: Write the failing tests** — `tests/test_collect_x.py`:
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import collect_x as cx  # noqa: E402

POST = {"id": "1810", "url": "https://x.com/jack/status/1810", "author": "jack",
        "created_at": "2026-06-20T10:00:00Z", "text": "A thread about agents.",
        "links": ["https://example.com/a"], "articles": [{"url": "https://example.com/a", "text": "Article body"}]}


def test_slugify():
    assert cx.slugify("1810") == "x-1810"


def test_build_document_frontmatter_and_body():
    d = cx.build_document(POST, collected_at="2026-06-24")
    assert "channel: x" in d and "tweet_id: 1810" in d and "author: jack" in d
    assert "links: [https://example.com/a]" in d
    assert "A thread about agents." in d and "## Linked articles" in d and "Article body" in d


def test_write_then_dedup(tmp_path):
    d = tmp_path / "_inbox"
    r1 = cx.write_collected(POST, collected_at="2026-06-24", inbox=d, dedup_dirs=[d])
    assert r1["status"] == "written" and Path(r1["path"]).name == "x-1810.md"
    r2 = cx.write_collected(POST, collected_at="2026-06-24", inbox=d, dedup_dirs=[d])
    assert r2["status"] == "duplicate"


def test_reapable_gates_on_ingested_and_channel(tmp_path):
    d = tmp_path / "x"; d.mkdir()
    (d / "x-1.md").write_text("---\nchannel: x\ntweet_id: 1\ncorpus_ingested: true\n---\n", encoding="utf-8")
    (d / "x-2.md").write_text("---\nchannel: x\ntweet_id: 2\n---\n", encoding="utf-8")          # not ingested
    (d / "n-3.md").write_text("---\nchannel: notes\ntweet_id: 3\ncorpus_ingested: true\n---\n", encoding="utf-8")  # wrong channel
    assert cx.reapable(dirs=[d]) == ["1"]
```

- [ ] **Step 2: Run → fail** — `python3 -m pytest tests/test_collect_x.py -q` → `No module named collect_x`.

- [ ] **Step 3: Implement** — `bin/collect_x.py`:
```python
#!/usr/bin/env python3
"""collect_x.py — pure logic for the X (Twitter) bookmarks collector."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "raw" / "_inbox"
DEDUP_DIRS = [ROOT / "raw" / "_inbox", ROOT / "raw" / "x"]
_ID_RE = re.compile(r"^tweet_id:\s*(\S+)\s*$", re.M)
_INGESTED_RE = re.compile(r"^corpus_ingested:\s*true\s*$", re.M)
_CHANNEL_X_RE = re.compile(r"^channel:\s*x\s*$", re.M)


def slugify(tweet_id) -> str:
    return f"x-{tweet_id}"


def _scalar(s) -> str:
    s = (str(s) if s is not None else "").replace("\n", " ").strip()
    if s and (any(c in s for c in ":#") or s[0] in "\"'[{-@`"):
        return '"' + s.replace('"', '\\"') + '"'
    return s


def already_collected(tweet_id, dirs=None) -> bool:
    for d in (dirs if dirs is not None else DEDUP_DIRS):
        p = Path(d)
        if not p.exists():
            continue
        for md in p.glob("*.md"):
            try:
                head = md.read_text(encoding="utf-8", errors="ignore")[:800]
            except OSError:
                continue
            m = _ID_RE.search(head)
            if m and m.group(1) == str(tweet_id):
                return True
    return False


def build_document(post: dict, *, collected_at: str) -> str:
    tid = post["id"]
    links = post.get("links") or []
    lines = [
        "---", "channel: x", "source: x",
        f"tweet_id: {tid}",
        f"url: {post.get('url', '')}",
        f"author: {post.get('author', '')}",
        f"created_at: {post.get('created_at', '')}",
        f"links: [{', '.join(links)}]",
        f"collected_at: {collected_at}",
        "---", "",
        f"# X post by @{post.get('author', '')}",
        "", (post.get("text") or "").strip(),
    ]
    arts = post.get("articles") or []
    if arts:
        lines.append("\n## Linked articles")
        for a in arts:
            lines += [f"### {a.get('url', '')}", (a.get("text") or "").strip(), ""]
    return "\n".join(lines) + "\n"


def write_collected(post: dict, *, collected_at: str, inbox=None, dedup_dirs=None) -> dict:
    tid = post["id"]
    if already_collected(tid, dedup_dirs):
        return {"status": "duplicate", "path": None}
    ib = Path(inbox) if inbox is not None else INBOX
    ib.mkdir(parents=True, exist_ok=True)
    path = ib / f"{slugify(tid)}.md"
    path.write_text(build_document(post, collected_at=collected_at), encoding="utf-8")
    return {"status": "written", "path": str(path)}


def reapable(dirs=None) -> list:
    out = []
    for d in (dirs if dirs is not None else DEDUP_DIRS):
        p = Path(d)
        if not p.exists():
            continue
        for md in p.glob("*.md"):
            try:
                head = md.read_text(encoding="utf-8", errors="ignore")[:800]
            except OSError:
                continue
            if _CHANNEL_X_RE.search(head) and _INGESTED_RE.search(head):
                m = _ID_RE.search(head)
                if m:
                    out.append(m.group(1))
    return out
```

- [ ] **Step 4: Run → pass** (4 tests). **Step 5: Commit** `feat(collect-x): pure logic — dedup + post document + reapable`.

---

### Task 2: `x_client.py` — OAuth2 token + bookmarks API

**Files:** Create `bin/x_client.py`; Test `tests/test_x_client.py`.

**Interfaces:** Produces `_pkce_pair()->(verifier,challenge)`, `_load_token()->dict|None`, `_access_token(*, _session=None)->str|None`, `x_available()->bool`, `me(*, _session=None)->str|None`, `list_bookmarks(max_n=None, *, _session=None)->list[dict]`, `delete_bookmark(tweet_id, *, _session=None)->bool`. `_session` defaults to a module session; tests pass a fake with `.get/.post/.delete`.

- [ ] **Step 1: Write failing tests** — `tests/test_x_client.py`:
```python
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
```

- [ ] **Step 2: Run → fail.**

- [ ] **Step 3: Implement** — `bin/x_client.py`:
```python
#!/usr/bin/env python3
"""x_client.py — X (Twitter) API v2 transport for the bookmarks collector (OAuth2 PKCE)."""
from __future__ import annotations
import base64
import hashlib
import json
import os
import secrets
import sys
import time
from pathlib import Path

import requests

BIN = Path(__file__).resolve().parent
APP_CFG = BIN / "x_app.json"        # {"client_id": "...", "redirect_uri": "http://127.0.0.1:8723/callback"}
TOKEN = BIN / "x_token.json"        # {access_token, refresh_token, expires_at}
API = "https://api.twitter.com/2"
TOKEN_URL = "https://api.twitter.com/2/oauth2/token"
SCOPES = "tweet.read users.read bookmark.read bookmark.write offline.access"
_SESSION = requests.Session()

sys.path.insert(0, str(BIN))
import collect_x as cx  # noqa: E402,F401  (used by cmd_run/cmd_reap in Task 3)


def _pkce_pair():
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(64)).rstrip(b"=").decode()
    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    return verifier, challenge


def _load_token():
    if not TOKEN.exists():
        return None
    try:
        return json.loads(TOKEN.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _save_token(tok: dict):
    TOKEN.write_text(json.dumps(tok), encoding="utf-8")


def _client_id():
    try:
        return json.loads(APP_CFG.read_text(encoding="utf-8")).get("client_id")
    except (OSError, json.JSONDecodeError):
        return None


def _access_token(*, _session=None):
    sess = _session or _SESSION
    tok = _load_token()
    if not tok:
        return None
    if tok.get("expires_at", 0) > time.time() + 60:
        return tok["access_token"]
    rt = tok.get("refresh_token")
    cid = _client_id()
    if not rt or not cid:
        return tok.get("access_token")
    r = sess.post(TOKEN_URL, data={"grant_type": "refresh_token", "refresh_token": rt,
                                   "client_id": cid})
    if getattr(r, "status_code", 500) != 200:
        return tok.get("access_token")
    new = r.json()
    tok.update(access_token=new["access_token"],
               refresh_token=new.get("refresh_token", rt),
               expires_at=time.time() + int(new.get("expires_in", 7200)))
    _save_token(tok)
    return tok["access_token"]


def x_available() -> bool:
    return _load_token() is not None and _client_id() is not None


def _auth_get(url, params, token, sess):
    return sess.get(url, params=params, headers={"Authorization": f"Bearer {token}"})


def me(*, _session=None):
    sess = _session or _SESSION
    tok = _access_token(_session=sess)
    if not tok:
        return None
    r = _auth_get(f"{API}/users/me", {}, tok, sess)
    if getattr(r, "status_code", 500) != 200:
        return None
    return r.json().get("data", {}).get("id")


def list_bookmarks(max_n=None, *, _session=None):
    sess = _session or _SESSION
    tok = _access_token(_session=sess)
    uid = me(_session=sess)
    if not tok or not uid:
        return []
    out, page_token = [], None
    while True:
        params = {"max_results": 100,
                  "tweet.fields": "created_at,note_tweet,entities,author_id",
                  "expansions": "author_id", "user.fields": "username"}
        if page_token:
            params["pagination_token"] = page_token
        r = _auth_get(f"{API}/users/{uid}/bookmarks", params, tok, sess)
        if getattr(r, "status_code", 500) != 200:
            break
        body = r.json()
        users = {u["id"]: u.get("username", "") for u in body.get("includes", {}).get("users", [])}
        for t in body.get("data", []):
            uname = users.get(t.get("author_id"), "")
            text = (t.get("note_tweet") or {}).get("text") or t.get("text", "")
            links = [u.get("expanded_url") for u in (t.get("entities", {}).get("urls", []))
                     if u.get("expanded_url")]
            out.append({"id": t["id"], "url": f"https://x.com/{uname}/status/{t['id']}",
                        "author": uname, "created_at": t.get("created_at", ""),
                        "text": text, "links": links})
            if max_n and len(out) >= max_n:
                return out
        page_token = body.get("meta", {}).get("next_token")
        if not page_token:
            break
    return out


def delete_bookmark(tweet_id, *, _session=None) -> bool:
    sess = _session or _SESSION
    tok = _access_token(_session=sess)
    uid = me(_session=sess)
    if not tok or not uid:
        return False
    r = sess.delete(f"{API}/users/{uid}/bookmarks/{tweet_id}",
                    headers={"Authorization": f"Bearer {tok}"})
    if getattr(r, "status_code", 500) != 200:
        return False
    return r.json().get("data", {}).get("bookmarked") is False
```

- [ ] **Step 4: Run → pass** (4 tests). **Step 5: Commit** `feat(x): OAuth2 token mgmt + list/delete bookmarks`.

---

### Task 3: `x_client.py` — `cmd_run` / `cmd_reap` / `cmd_auth` + CLI

**Files:** Modify `bin/x_client.py`; Test `tests/test_x_client.py`.

**Interfaces:** Consumes `list_bookmarks`, `delete_bookmark`, `x_available`, `cx.*`, `fetch_link.fetch`. Produces `cmd_run(args)->int`, `cmd_reap(args)->int`, `cmd_auth(args)->int`, `_build_parser()`, `main(argv=None)->int`.

- [ ] **Step 1: Write failing tests** — append to `tests/test_x_client.py`:
```python
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
```

- [ ] **Step 2: Run → fail.**

- [ ] **Step 3: Implement** — append to `bin/x_client.py`:
```python
import argparse  # noqa: E402
import datetime  # noqa: E402
import urllib.parse  # noqa: E402
import webbrowser  # noqa: E402
from http.server import BaseHTTPRequestHandler, HTTPServer  # noqa: E402

import fetch_link as fl  # noqa: E402


def _fetch_articles(links, cap=3):
    arts = []
    for url in links[:cap]:
        try:
            c = fl.fetch(url)
        except Exception:  # noqa: BLE001
            c = None
        if c and c.get("text"):
            arts.append({"url": url, "text": c["text"][:15000]})
    return arts


def cmd_run(args) -> int:
    if not x_available():
        print(json.dumps({"status": "not configured", "reason": "no X token"}))
        return 0
    at = args.collected_at or datetime.date.today().isoformat()
    found = written = dup = failed = 0
    for post in list_bookmarks(args.max):
        found += 1
        tid = post.get("id")
        if not tid or cx.already_collected(tid):
            dup += 1
            continue
        if args.dry_run:
            continue
        try:
            post["articles"] = _fetch_articles(post.get("links") or [])
            res = cx.write_collected(post, collected_at=at)
        except Exception:  # noqa: BLE001
            failed += 1
            continue
        if res.get("status") == "written":
            written += 1
        elif res.get("status") == "duplicate":
            dup += 1
    print(json.dumps({"found": found, "written": written, "duplicate": dup,
                      "failed": failed, "dry_run": bool(args.dry_run)}))
    return 0


def cmd_reap(args) -> int:
    if not x_available():
        print(json.dumps({"status": "not configured", "unbookmarked": 0}))
        return 0
    n = 0
    for tid in cx.reapable():
        if args.dry_run:
            n += 1
        elif delete_bookmark(tid):
            n += 1
    print(json.dumps({"unbookmarked": n, "dry_run": bool(args.dry_run)}))
    return 0


def cmd_auth(args) -> int:
    cid = _client_id()
    if not cid:
        print("Create bin/x_app.json with your client_id + redirect_uri first.")
        return 1
    cfg = json.loads(APP_CFG.read_text(encoding="utf-8"))
    redirect = cfg["redirect_uri"]
    verifier, challenge = _pkce_pair()
    state = secrets.token_urlsafe(16)
    qs = urllib.parse.urlencode({
        "response_type": "code", "client_id": cid, "redirect_uri": redirect,
        "scope": SCOPES, "state": state,
        "code_challenge": challenge, "code_challenge_method": "S256"})
    code_box = {}

    class H(BaseHTTPRequestHandler):
        def do_GET(self):  # noqa: N802
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            code_box["code"] = (q.get("code") or [None])[0]
            self.send_response(200); self.end_headers()
            self.wfile.write(b"X authorized. You can close this tab.")
        def log_message(self, *a):  # silence
            return

    port = int(urllib.parse.urlparse(redirect).port or 8723)
    httpd = HTTPServer(("127.0.0.1", port), H)
    webbrowser.open(f"https://twitter.com/i/oauth2/authorize?{qs}")
    print("Authorize in the opened browser tab…")
    httpd.handle_request()
    code = code_box.get("code")
    if not code:
        print("No authorization code received."); return 1
    r = _SESSION.post(TOKEN_URL, data={
        "grant_type": "authorization_code", "code": code, "client_id": cid,
        "redirect_uri": redirect, "code_verifier": verifier})
    if r.status_code != 200:
        print("Token exchange failed:", r.text[:200]); return 1
    t = r.json()
    _save_token({"access_token": t["access_token"], "refresh_token": t.get("refresh_token"),
                 "expires_at": time.time() + int(t.get("expires_in", 7200))})
    print(json.dumps({"status": "authorized"}))
    return 0


def _build_parser():
    p = argparse.ArgumentParser(description="X (Twitter) bookmarks collector.")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("auth").set_defaults(func=cmd_auth)
    sub.add_parser("me").set_defaults(func=lambda a: (print(json.dumps({"id": me()})), 0)[1])
    pr = sub.add_parser("run")
    pr.add_argument("--max", type=int, default=None)
    pr.add_argument("--dry-run", action="store_true")
    pr.add_argument("--collected-at", default=None)
    pr.set_defaults(func=cmd_run)
    prp = sub.add_parser("reap")
    prp.add_argument("--dry-run", action="store_true")
    prp.set_defaults(func=cmd_reap)
    return p


def main(argv=None) -> int:
    args = _build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run → pass** (8 tests total). **Step 5: Commit** `feat(x): cmd_run/reap/auth + CLI (collect new, un-bookmark only ingested)`.

---

### Task 4: Wire into the scheduled run

**Files:** Modify `bin/scheduled_run.py`; Test `tests/test_scheduled_run.py`.

- [ ] **Step 1: Write failing test** — append to `tests/test_scheduled_run.py`:
```python
class TestXCollector:
    def test_x_leg_and_channel_dir(self):
        assert scheduled_run._CHANNEL_DIR.get("x") == "x"
        called = []
        def fake_run(cmd, **kw):
            called.append(" ".join(cmd))
            import types
            return types.SimpleNamespace(returncode=0, stdout='{"written": 1}', stderr="")
        res = scheduled_run.run_collectors(_subprocess_run=fake_run)
        assert any("x_client.py" in s and "run" in s for s in called), called
        assert res["x"]["status"] == "ok" and res["x"]["collected"] == 1
```

- [ ] **Step 2: Run → fail.** (NOTE: read `run_collectors` first; mirror the github/pdf leg exactly — same `_run` seam name, returncode check, `data.get("written",0)`.)

- [ ] **Step 3: Implement** — in `bin/scheduled_run.py`: add `"x": "x"` to `_CHANNEL_DIR`; add an x collect leg after the github leg (mirror it: `x_client.py run`, parse `written` → `results["x"]={"status","collected"}`); and an **x reap step** after the ingest+email-relabel (mirror `run_email_relabel`): invoke `x_client.py reap`, record `{"unbookmarked": N}` in the summary. Use the file's actual `_run`/seam names verbatim.

- [ ] **Step 4: Run → pass.** **Step 5: Commit** `feat(scheduled-run): x collect leg + reap step + raw/x channel`.

---

### Task 5: Docs + gitignore + full-suite gate

**Files:** Modify `corpus/_config.md`, `corpus/_log.md`, `.gitignore`.

- [ ] **Step 1:** `.gitignore` — add `bin/x_token.json` and `bin/x_app.json` (secrets; never commit).
- [ ] **Step 2:** `corpus/_config.md` — document the `x` channel: collects the user's X bookmarks via the X API v2 (OAuth2 user-context), one doc per post (+ linked article), deduped by `tweet_id`; **un-bookmarks only after `corpus_ingested`** (separate reap step). One-time setup: `bin/x_app.json` (client_id + redirect) then `python3 bin/x_client.py auth`. Skipped (`not configured`) if no token.
- [ ] **Step 3:** `corpus/_log.md` — append a `config` entry (use the real time).
- [ ] **Step 4:** Full gate `python3 -m pytest tests/ -q` → all green. **Step 5: Commit** `docs(x): document X bookmarks channel + gitignore tokens`.

---

## Notes for the executor
- **Live setup is the user's** (X dev app + `bin/x_app.json` + `python3 bin/x_client.py auth`). Until then `x_available()` is False and the leg reports `not configured` — every test mocks all HTTP, so the suite is green without any X auth.
- `cmd_auth` (browser + local callback server) is not unit-tested; the PKCE/token helpers are. It's validated live once the user sets up the app.
- The reap (un-bookmark) is the ONLY deletion path, gated on `corpus_ingested: true` — confirm collect never calls `delete_bookmark`.

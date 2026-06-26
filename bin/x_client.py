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
import secret_env  # noqa: E402

TOKEN_ENV = "X_TOKEN_JSON"  # cloud/CI supply the token JSON here; else fall back to TOKEN file


def _pkce_pair():
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(64)).rstrip(b"=").decode()
    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    return verifier, challenge


def _load_token():
    try:
        path = secret_env.materialize_secret(TOKEN_ENV, TOKEN)
    except FileNotFoundError:
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
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

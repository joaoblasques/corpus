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

#!/usr/bin/env python3
"""gmail_client.py — owned Gmail transport for the collect-email skill.

Uses the user's OWN Google OAuth credential (gmail.modify scope) so the corpus
can both read starred mail AND de-star/archive it — unlike the hosted, read-only
claude.ai Gmail connector. Credentials live in bin/credentials.json (you provide,
downloaded from Google Cloud Console) and the cached OAuth token in bin/token.json
(created on first `auth`). Both are gitignored — they are secrets.

The deterministic write (slugify, pointer detection, dedup, frontmatter, file
write) is delegated to collect_email.py, which stays transport-agnostic and fully
unit-tested. This module only handles the network: search, fetch, label-modify.

Subcommands:
  auth          One-time browser consent; caches the OAuth token to bin/token.json.
  list-starred  Print JSON of starred messages (id, from, subject, date, body).
  archive       Remove STARRED + INBOX labels from one message id.
  run           Full loop: collect each starred message into raw/_inbox/ via
                collect_email, then de-star/archive it — but only AFTER a
                confirmed write. --dry-run collects without mutating Gmail.
"""
from __future__ import annotations

import argparse
import base64
import datetime
import html as _html
import json
import re
import sys
from email.utils import parsedate_to_datetime
from pathlib import Path

BIN = Path(__file__).resolve().parent
ROOT = BIN.parent
CREDENTIALS = BIN / "credentials.json"
TOKEN = BIN / "token.json"
# gmail.modify = read + add/remove labels (de-star, archive). Least privilege:
# it cannot permanently delete mail or change settings.
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

sys.path.insert(0, str(BIN))
import collect_email as ce  # noqa: E402


# --------------------------------------------------------------------------
# Pure helpers (network-free; unit-tested in tests/test_gmail_client.py)
# --------------------------------------------------------------------------

def header(headers: list[dict], name: str) -> str:
    """Case-insensitive lookup of a header value from a Gmail headers list."""
    name = name.lower()
    for h in headers or []:
        if (h.get("name") or "").lower() == name:
            return h.get("value", "")
    return ""


def _b64(data: str) -> str:
    """Decode Gmail's base64url body data (tolerant of missing padding)."""
    if not data:
        return ""
    return base64.urlsafe_b64decode(data.encode("ascii") + b"===").decode("utf-8", "replace")


_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"[ \t]*\n[ \t]*")


def html_to_text(html: str) -> str:
    """Minimal HTML→text: drop script/style, keep line structure, unescape."""
    text = re.sub(r"(?is)<(script|style).*?</\1>", "", html)
    text = re.sub(r"(?i)<br\s*/?>", "\n", text)
    text = re.sub(r"(?i)</p\s*>", "\n\n", text)
    text = _TAG_RE.sub("", text)
    text = _html.unescape(text)
    text = _WS_RE.sub("\n", text)
    return text.strip()


def _collect_bodies(payload: dict) -> tuple[str, str]:
    """Recursively gather (plain_text, html) from a MIME payload tree."""
    mime = payload.get("mimeType", "")
    data = (payload.get("body") or {}).get("data", "")
    if mime == "text/plain" and data:
        return _b64(data), ""
    if mime == "text/html" and data:
        return "", _b64(data)
    plain_parts, html_parts = [], []
    for part in payload.get("parts") or []:
        p, h = _collect_bodies(part)
        if p:
            plain_parts.append(p)
        if h:
            html_parts.append(h)
    return "\n".join(plain_parts), "\n".join(html_parts)


def extract_body(payload: dict) -> str:
    """Best-effort body text: prefer text/plain, fall back to text/html."""
    plain, html = _collect_bodies(payload or {})
    if plain.strip():
        return plain.strip()
    if html.strip():
        return html_to_text(html)
    return ""


def message_date(msg: dict) -> str:
    """YYYY-MM-DD from the Date header, falling back to internalDate (UTC)."""
    headers = (msg.get("payload") or {}).get("headers", [])
    raw = header(headers, "Date")
    if raw:
        try:
            return parsedate_to_datetime(raw).date().isoformat()
        except (TypeError, ValueError):
            pass
    internal = msg.get("internalDate")
    if internal:
        return datetime.datetime.fromtimestamp(
            int(internal) / 1000, datetime.timezone.utc
        ).date().isoformat()
    return ""


def parse_message(msg: dict) -> dict:
    """Flatten a Gmail `format=full` message into collector fields."""
    headers = (msg.get("payload") or {}).get("headers", [])
    return {
        "message_id": msg.get("id", ""),
        "from": header(headers, "From"),
        "subject": header(headers, "Subject"),
        "date_received": message_date(msg),
        "body": extract_body(msg.get("payload") or {}),
    }


# --------------------------------------------------------------------------
# Gmail service (network)
# --------------------------------------------------------------------------

def get_service():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    creds = None
    if TOKEN.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS.exists():
                raise SystemExit(
                    f"Missing {CREDENTIALS}.\n"
                    "Download an OAuth 'Desktop app' client from Google Cloud "
                    "Console (APIs & Services → Credentials) and save it there."
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN.write_text(creds.to_json(), encoding="utf-8")
    return build("gmail", "v1", credentials=creds, cache_discovery=False)


def list_starred_messages(service, max_results: int | None = None) -> list[dict]:
    """Fetch full `is:starred` messages, paging until done or max_results hit."""
    out: list[dict] = []
    req = service.users().messages().list(userId="me", q="is:starred", maxResults=100)
    while req is not None:
        resp = req.execute()
        for m in resp.get("messages", []):
            full = service.users().messages().get(
                userId="me", id=m["id"], format="full"
            ).execute()
            out.append(full)
            if max_results and len(out) >= max_results:
                return out
        req = service.users().messages().list_next(req, resp)
    return out


def archive_message(service, message_id: str) -> dict:
    """De-star and archive: remove the STARRED and INBOX labels."""
    return service.users().messages().modify(
        userId="me", id=message_id,
        body={"removeLabelIds": ["STARRED", "INBOX"]},
    ).execute()


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def cmd_auth(_args) -> int:
    get_service()
    print(json.dumps({"status": "authorized", "token": str(TOKEN)}))
    return 0


def cmd_list_starred(args) -> int:
    service = get_service()
    msgs = [parse_message(m) for m in list_starred_messages(service, args.max)]
    print(json.dumps(msgs, indent=2))
    return 0


def cmd_archive(args) -> int:
    service = get_service()
    archive_message(service, args.message_id)
    print(json.dumps({"status": "archived", "message_id": args.message_id}))
    return 0


def cmd_run(args) -> int:
    service = get_service()
    collected_at = args.collected_at or datetime.date.today().isoformat()
    messages = list_starred_messages(service, args.max)
    found = len(messages)
    written = dup = failed = archived = 0
    paths: list[str] = []
    for full in messages:
        info = parse_message(full)
        try:
            res = ce.write_collected(
                {
                    "gmail_message_id": info["message_id"],
                    "from": info["from"],
                    "subject": info["subject"],
                    "date_received": info["date_received"],
                    "collected_at": collected_at,
                },
                info["body"],
            )
        except Exception:
            failed += 1
            continue
        status = res.get("status")
        if status == "written":
            written += 1
            paths.append(res["path"])
        elif status == "duplicate":
            dup += 1
        else:
            failed += 1
            continue
        # Safety rule: mutate Gmail ONLY after a confirmed write/duplicate.
        if not args.dry_run:
            try:
                archive_message(service, info["message_id"])
                archived += 1
            except Exception:
                # Write succeeded but archive failed — leave it starred, not fatal.
                pass
    print(json.dumps({
        "found": found, "written": written, "duplicate": dup,
        "failed": failed, "archived": archived,
        "dry_run": bool(args.dry_run), "paths": paths,
    }, indent=2))
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Owned-credential Gmail transport for collect-email.")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("auth", help="One-time OAuth consent; cache token.").set_defaults(func=cmd_auth)

    pl = sub.add_parser("list-starred", help="Print starred messages as JSON.")
    pl.add_argument("--max", type=int, default=None)
    pl.set_defaults(func=cmd_list_starred)

    pa = sub.add_parser("archive", help="De-star + archive one message id.")
    pa.add_argument("--message-id", required=True)
    pa.set_defaults(func=cmd_archive)

    pr = sub.add_parser("run", help="Collect all starred mail, then de-star/archive.")
    pr.add_argument("--max", type=int, default=None, help="Cap messages this run.")
    pr.add_argument("--collected-at", default=None, help="Override YYYY-MM-DD stamp.")
    pr.add_argument("--dry-run", action="store_true", help="Collect but do not mutate Gmail.")
    pr.set_defaults(func=cmd_run)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

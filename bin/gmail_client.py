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
import rank_links as rl  # noqa: E402
import fetch_link as fl  # noqa: E402

WEB_DIR = ROOT / "raw" / "web"
YT_DIR = ROOT / "raw" / "youtube"


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


# Topic labels collected into the corpus (exact Gmail names). Edit to add/remove
# labels; documented in corpus/_config.md.
CORPUS_LABELS = [
    "Data Engineering", "Data Engineering/databricks", "Data Engineering/dbt",
    "Data Engineering/spark", "Ml", "ML Engineering", "MLOps",
    "Productivity", "Prompting",
]


def resolve_label_ids(service, names=None):
    """Map configured label names → Gmail label ids. Returns (name_to_id, missing)."""
    names = names if names is not None else CORPUS_LABELS
    resp = service.users().labels().list(userId="me").execute()
    by_name = {l["name"]: l["id"] for l in resp.get("labels", [])}
    name_to_id = {n: by_name[n] for n in names if n in by_name}
    missing = [n for n in names if n not in by_name]
    return name_to_id, missing


def matched_corpus_labels(message_label_ids, name_to_id) -> list:
    """Corpus label NAMES whose id is present on the message (pure)."""
    id_to_name = {v: k for k, v in name_to_id.items()}
    return [id_to_name[i] for i in message_label_ids if i in id_to_name]


def list_labeled_messages(service, label_ids, max_results=None) -> list:
    """Full messages across the given label ids, deduped by message id."""
    seen, out = set(), []
    for lid in label_ids:
        req = service.users().messages().list(userId="me", labelIds=[lid], maxResults=100)
        while req is not None:
            resp = req.execute()
            for m in resp.get("messages", []):
                mid = m["id"]
                if mid in seen:
                    continue
                seen.add(mid)
                full = service.users().messages().get(userId="me", id=mid, format="full").execute()
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


def enrich_email(email_path: str, message_id: str, body: str,
                 collected_at: str, max_links: int) -> dict:
    """Follow useful links in one email: select -> rank -> fetch -> write +
    patch the parent email's links: frontmatter. Best-effort; never raises."""
    captured = skipped = 0
    try:
        candidates = ce.select_links(body)
        if not candidates:
            return {"captured": 0, "skipped": 0}
        dispositions = rl.rank(candidates, max_links=max_links, floor=4)
        for d in dispositions:
            if not d["fetch"]:
                skipped += 1
                continue
            try:
                resolved = fl.resolve(d["url"])
                kind = fl.classify(resolved)
                if kind == "unsupported":
                    d.update(fetch=False, reason="unsupported")
                    skipped += 1
                    continue
                base = WEB_DIR if kind == "article" else YT_DIR
                base.mkdir(parents=True, exist_ok=True)
                if _url_seen(resolved):
                    d.update(fetch=False, reason="duplicate")
                    skipped += 1
                    continue
                content = fl.fetch(resolved)
                target = ce.link_target(content["title"], base, resolved)
                doc = ce.build_link_document(
                    {"channel": content["channel"], "source_url": resolved,
                     "via_email": message_id, "score": d["score"],
                     "collected_at": collected_at},
                    content["text"],
                )
                target.write_text(doc, encoding="utf-8")
                d["file"] = str(target.relative_to(ROOT))
                captured += 1
            except Exception:
                d.update(fetch=False, reason="fetch-failed")
                skipped += 1
        try:
            ce.add_links_frontmatter(email_path, dispositions)
        except Exception:
            pass
    except Exception:
        return {"captured": captured, "skipped": skipped}
    return {"captured": captured, "skipped": skipped}


def _url_seen(resolved: str) -> bool:
    """Dedup against source_url already written in any raw/web or raw/youtube file."""
    needle = f"source_url: {resolved}\n"
    for d in (WEB_DIR, YT_DIR):
        if not d.exists():
            continue
        for md in d.glob("*.md"):
            try:
                if needle in md.read_text(encoding="utf-8"):
                    return True
            except (OSError, UnicodeDecodeError):
                continue
    return False


def cmd_reap_labels(args) -> int:
    """Post-ingest: for each corpus-labeled email already in the corpus, remove the
    matched corpus label(s) + INBOX (archive). Gated on corpus_ingested; idempotent."""
    items = ce.labeled_reapable()
    if not items:
        print(json.dumps({"relabeled": 0, "archived": 0,
                          "dry_run": bool(args.dry_run), "note": "nothing-to-reap"}))
        return 0
    service = get_service()
    name_to_id, _ = resolve_label_ids(service)
    relabeled = errors = 0
    for it in items:
        ids = [name_to_id[n] for n in it["gmail_corpus_labels"] if n in name_to_id]
        if not ids:
            continue
        if args.dry_run:
            relabeled += 1
            continue
        try:
            service.users().messages().modify(
                userId="me", id=it["gmail_message_id"],
                body={"removeLabelIds": ids + ["INBOX"]}).execute()
            ce.clear_corpus_labels(it["gmail_message_id"])   # un-mark: reap exactly once
            relabeled += 1
        except Exception:  # noqa: BLE001 — one bad message must not abort the batch
            errors += 1
    print(json.dumps({"relabeled": relabeled, "archived": relabeled,
                      "dry_run": bool(args.dry_run), "errors": errors}))
    return 0


def cmd_run(args) -> int:
    service = get_service()
    collected_at = args.collected_at or datetime.date.today().isoformat()
    messages = list_starred_messages(service, args.max)
    found = len(messages)
    written = dup = failed = archived = 0
    links_captured = links_skipped = 0
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
        # Enrich with linked content AFTER archive (best-effort; also runs in dry-run).
        if not args.no_links and status == "written":
            e = enrich_email(res["path"], info["message_id"], info["body"],
                             collected_at, args.max_links)
            links_captured += e["captured"]
            links_skipped += e["skipped"]
    # --- Labeled pass: collect configured corpus labels. NO archive here — the
    # un-label/archive is deferred to `reap-labels`, gated on corpus_ingested. ---
    name_to_id, missing_labels = resolve_label_ids(service)
    labeled_written = labeled_dup = labeled_failed = labeled_marked = 0
    for full in list_labeled_messages(service, list(name_to_id.values()), args.max):
        info = parse_message(full)
        labels = matched_corpus_labels(full.get("labelIds", []), name_to_id)
        try:
            res = ce.write_collected(
                {"gmail_message_id": info["message_id"], "from": info["from"],
                 "subject": info["subject"], "date_received": info["date_received"],
                 "collected_at": collected_at, "gmail_corpus_labels": labels},
                info["body"])
        except Exception:
            labeled_failed += 1
            continue
        status = res.get("status")
        if status == "written":
            labeled_written += 1
            paths.append(res["path"])
        elif status == "duplicate":
            labeled_dup += 1
            # Backlog: an email collected earlier (e.g. as starred) lacks the marker;
            # add it to the existing source so it still flows through the label lifecycle.
            if labels and ce.mark_corpus_labels(info["message_id"], labels):
                labeled_marked += 1
        else:
            labeled_failed += 1
            continue
        if not args.no_links and status == "written":
            e = enrich_email(res["path"], info["message_id"], info["body"],
                             collected_at, args.max_links)
            links_captured += e["captured"]
            links_skipped += e["skipped"]

    print(json.dumps({
        "found": found, "written": written, "duplicate": dup,
        "failed": failed, "archived": archived,
        "labeled_written": labeled_written, "labeled_duplicate": labeled_dup,
        "labeled_failed": labeled_failed, "labeled_marked": labeled_marked, "missing_labels": missing_labels,
        "links_captured": links_captured, "links_skipped": links_skipped,
        "dry_run": bool(args.dry_run), "paths": paths,
    }, indent=2))
    return 0


def _build_parser():
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
    pr.add_argument("--no-links", action="store_true", help="Skip link-following enrichment.")
    pr.add_argument("--max-links", type=int, default=10, help="Max links fetched per email.")
    pr.set_defaults(func=cmd_run)

    prl = sub.add_parser("reap-labels",
                         help="Post-ingest: un-label + archive corpus-labeled emails.")
    prl.add_argument("--dry-run", action="store_true", help="Report only; no Gmail mutation.")
    prl.set_defaults(func=cmd_reap_labels)

    return p


def _args(argv=None):
    """Parse argv via the shared parser; used in tests to build an args namespace."""
    return _build_parser().parse_args(argv)


def main(argv=None) -> int:
    args = _args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

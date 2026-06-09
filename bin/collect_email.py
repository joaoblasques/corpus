#!/usr/bin/env python3
"""collect_email.py — deterministic core for the collect-email skill.

The skill fetches starred Gmail messages via MCP and, for each one, invokes
this script to idempotently write a normalized markdown file into raw/_inbox/.
Gmail mutation (de-star/archive) is performed by the skill only after this
script reports a successful write.
"""
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "raw" / "_inbox"
DEDUP_DIRS = [ROOT / "raw" / "_inbox", ROOT / "raw" / "email"]

URL_RE = re.compile(r"https?://[^\s)>\]]+")
POINTER_MAX_PROSE = 200  # non-URL chars below which a body is "just a link"


def slugify(text: str, max_len: int = 60) -> str:
    text = unicodedata.normalize("NFKD", text or "").encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    if len(text) > max_len:
        text = text[:max_len].rstrip("-")
    return text or "untitled"


def detect_pointer(body: str) -> tuple[bool, str | None]:
    """A body is a 'pointer' if it is dominated by a link (little other prose)."""
    urls = URL_RE.findall(body or "")
    if not urls:
        return False, None
    prose = URL_RE.sub("", body).strip()
    if len(prose) <= POINTER_MAX_PROSE:
        return True, urls[0]
    return False, None


def already_collected(message_id: str, search_dirs: list[Path] | None = None) -> bool:
    dirs = search_dirs if search_dirs is not None else DEDUP_DIRS
    needle = f"gmail_message_id: {message_id}"
    for d in dirs:
        if not d.exists():
            continue
        for md in d.glob("*.md"):
            try:
                if needle in md.read_text(encoding="utf-8"):
                    return True
            except (OSError, UnicodeDecodeError):
                continue
    return False


def yaml_scalar(value: str) -> str:
    value = (value or "").replace("\n", " ").strip()
    needs_quote = (
        value == ""
        or value[:1] in "-?:#&*!|>%@`"
        or bool(re.search(r'[:#\[\]{}",]', value))
    )
    if needs_quote:
        return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return value


def build_document(meta: dict, body: str) -> str:
    lines = [
        "---",
        "channel: email",
        "source: gmail",
        f"gmail_message_id: {meta['gmail_message_id']}",
        f"from: {yaml_scalar(meta['from'])}",
        f"subject: {yaml_scalar(meta['subject'])}",
        f"date_received: {meta['date_received']}",
    ]
    if meta.get("url"):
        lines.append(f"url: {meta['url']}")
    lines.append(f"pointer: {'true' if meta.get('pointer') else 'false'}")
    lines.append(f"collected_at: {meta['collected_at']}")
    lines.append("---")
    lines.append("")
    lines.append(body.strip())
    lines.append("")
    return "\n".join(lines)


def target_filename(date_received: str, subject: str, message_id: str,
                    inbox: Path | None = None) -> Path:
    base = inbox if inbox is not None else INBOX
    slug = slugify(subject)
    candidate = base / f"email-{date_received}-{slug}.md"
    if candidate.exists():
        suffix = re.sub(r"[^a-z0-9]+", "", message_id.lower())[:8] or "x"
        candidate = base / f"email-{date_received}-{slug}-{suffix}.md"
    return candidate


def write_collected(meta: dict, body: str, inbox: Path | None = None,
                    dedup_dirs: list[Path] | None = None) -> dict:
    if already_collected(meta["gmail_message_id"], dedup_dirs):
        return {"status": "duplicate", "gmail_message_id": meta["gmail_message_id"]}
    pointer, url = detect_pointer(body)
    meta = {**meta, "pointer": pointer, "url": url}
    base = inbox if inbox is not None else INBOX
    base.mkdir(parents=True, exist_ok=True)
    path = target_filename(meta["date_received"], meta["subject"],
                           meta["gmail_message_id"], base)
    path.write_text(build_document(meta, body), encoding="utf-8")
    return {"status": "written", "path": str(path), "pointer": pointer, "url": url}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        description="Write a starred Gmail message into raw/_inbox/ (idempotent)."
    )
    p.add_argument("--message-id", required=True)
    p.add_argument("--from", dest="sender", required=True)
    p.add_argument("--subject", required=True)
    p.add_argument("--date", dest="date_received", required=True)
    p.add_argument("--collected-at", required=True)
    p.add_argument("--body-file", required=True)
    args = p.parse_args(argv)
    body = Path(args.body_file).read_text(encoding="utf-8")
    meta = {
        "gmail_message_id": args.message_id,
        "from": args.sender,
        "subject": args.subject,
        "date_received": args.date_received,
        "collected_at": args.collected_at,
    }
    print(json.dumps(write_collected(meta, body)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

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


NOISE_URL_RE = re.compile(
    r"(?i)(unsubscribe|list-manage|mailchi\.mp|/sub/|/profile|update.*profile|"
    r"twitter\.com|x\.com|facebook\.com|linkedin\.com|instagram\.com|t\.me|"
    r"mailto:)"
)
NOISE_TEXT_RE = re.compile(
    r"(?i)(unsubscribe|view (this )?(post|email) (on|in) the web|view in browser|"
    r"manage (your )?subscription|update your profile)"
)
IMG_EXT_RE = re.compile(r"(?i)\.(png|jpe?g|gif|svg|webp|ico)(\?|$)")


def select_links(body: str) -> list[dict]:
    """Pure: extract content links with a nearby description, drop noise, dedup.

    Resolution of redirect wrappers and a second-pass filter happen later in the
    fetch stage (they require the network); this stays deterministic and testable.
    """
    lines = (body or "").splitlines()
    seen: set[str] = set()
    out: list[dict] = []
    for i, line in enumerate(lines):
        for m in URL_RE.finditer(line):
            url = m.group(0).rstrip(").,]>”\"'")
            if url in seen or NOISE_URL_RE.search(url) or IMG_EXT_RE.search(url):
                continue
            desc = re.sub(r"[\[\]]", " ", URL_RE.sub("", line))
            desc = re.sub(r"\s+", " ", desc).strip()
            if len(desc) < 8:
                for j in range(i + 1, min(i + 3, len(lines))):
                    nxt = lines[j].strip()
                    if nxt and not URL_RE.search(nxt):
                        desc = nxt
                        break
            if NOISE_TEXT_RE.search(desc):
                continue
            seen.add(url)
            out.append({"url": url, "description": desc[:300]})
    return out


LEARN_RE = re.compile(
    r"(?i)\b(guide|tutorial|how[\s-]?to|explained?|introduction|deep[\s-]?dive|"
    r"fundamentals|concept|primer|walkthrough|learn|course|patterns?|reference|"
    r"cheat[\s-]?sheet|build(ing)?)\b"
)
NEWS_RE = re.compile(
    r"(?i)(\bannounce[ds]?\b|\blaunch(es|ed)?\b|\braises?\b|\braised\b|\bfunding\b|"
    r"\bseries [a-d]\b|\bacqui(re|res|red|sition)\b|\bvaluation\b|\bhires?\b|"
    r"\bappoints?\b|\$\d+\s?(m|b|million|billion)\b)"
)


def heuristic_score(url: str, description: str) -> int:
    """Pure 0-10 learning-utility score; fallback when LLM ranking is unavailable."""
    text = f"{url} {description}".lower()
    score = 5
    if "github.com" in text:
        score += 3
    if re.search(r"(docs?\.|/docs/|readthedocs|\.dev/)", text):
        score += 1
    if LEARN_RE.search(text):
        score += 2
    if NEWS_RE.search(text):
        score -= 3
    return max(0, min(10, score))


def build_link_document(meta: dict, text: str) -> str:
    lines = [
        "---",
        f"channel: {meta['channel']}",
        f"source_url: {meta['source_url']}",
        f"via_email: {meta['via_email']}",
        f"utility_score: {meta['score']}",
        f"collected_at: {meta['collected_at']}",
        "---",
        "",
        text.strip(),
        "",
    ]
    return "\n".join(lines)


def link_target(title: str, base_dir: Path, message_hint: str = "") -> Path:
    slug = slugify(title)
    candidate = base_dir / f"{slug}.md"
    if candidate.exists():
        suffix = re.sub(r"[^a-z0-9]+", "", message_hint.lower())[:8] or "x"
        candidate = base_dir / f"{slug}-{suffix}.md"
    return candidate


def add_links_frontmatter(path: str, links: list[dict]) -> None:
    """Insert a `links:` block before the closing `---` of an existing file's
    frontmatter. Each entry is a one-line flow mapping for compactness."""
    p = Path(path)
    content = p.read_text(encoding="utf-8")
    block = ["links:"]
    for d in links:
        parts = [
            f"url: {yaml_scalar(d['url'])}",
            f"fetched: {'true' if d.get('file') else 'false'}",
            f"score: {d.get('score', 0)}",
        ]
        if d.get("file"):
            parts.append(f"file: {yaml_scalar(d['file'])}")
        if d.get("reason"):
            parts.append(f"reason: {d['reason']}")
        block.append("  - {" + ", ".join(parts) + "}")
    closing = content.index("\n---", content.index("---") + 3)
    p.write_text(content[:closing] + "\n" + "\n".join(block) + content[closing:],
                 encoding="utf-8")


def already_collected(message_id: str, search_dirs: list[Path] | None = None) -> bool:
    dirs = search_dirs if search_dirs is not None else DEDUP_DIRS
    needle = f"gmail_message_id: {message_id}\n"
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
    value = (value or "").replace("\n", " ").replace("\t", " ").strip()
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
        # gmail_message_id and date_received are trusted alphanumeric/ISO-date values (not routed through yaml_scalar).
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
        # Handles a single collision level; same-id reprocessing is blocked upstream by already_collected.
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
    meta = {
        "gmail_message_id": args.message_id,
        "from": args.sender,
        "subject": args.subject,
        "date_received": args.date_received,
        "collected_at": args.collected_at,
    }
    try:
        body = Path(args.body_file).read_text(encoding="utf-8")
        result = write_collected(meta, body)
    except Exception as e:
        print(json.dumps({"status": "error", "error": str(e)}))
        return 1
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

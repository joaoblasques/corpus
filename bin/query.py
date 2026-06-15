#!/usr/bin/env python3
"""query.py — deterministic core for the /query skill: queue web sources + log gaps.

The skill answers a knowledge question from the corpus. When coverage is thin it
fetches web content and invokes this script to (a) idempotently queue each fetched
source into raw/_inbox/ (deduped by source_url) and (b) append a `query` entry to
corpus/_log.md recording the gap. Writes ONLY to raw/_inbox/ and (append-only) to
corpus/_log.md.
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import collect_email as ce  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "raw" / "_inbox"
LOG_PATH = ROOT / "corpus" / "_log.md"
DEDUP_DIRS = [ROOT / "raw" / "_inbox", ROOT / "raw" / "web", ROOT / "raw" / "youtube"]


def already_queued(source_url: str, search_dirs: list[Path] | None = None) -> bool:
    dirs = search_dirs if search_dirs is not None else DEDUP_DIRS
    # Match the exact serialized line build_web_document writes (yaml_scalar may
    # quote the URL because of its colon), so freshly-written files dedup on re-run.
    needle = f"source_url: {ce.yaml_scalar(source_url)}\n"
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


def build_web_document(meta: dict, text: str) -> str:
    # channel is a trusted literal ("web"/"youtube"), so no yaml_scalar quoting.
    lines = [
        "---",
        f"channel: {meta.get('channel', 'web')}",
        f"source_url: {ce.yaml_scalar(meta['source_url'])}",
        f"via_query: {ce.yaml_scalar(meta['via_query'])}",
        f"fetched_at: {meta['fetched_at']}",
        "---",
        "",
        text.strip(),
        "",
    ]
    return "\n".join(lines)


def queue_source(question: str, fetch_result: dict, source_url: str,
                 inbox: Path | None = None,
                 dedup_dirs: list[Path] | None = None, at: str | None = None) -> dict:
    if already_queued(source_url, dedup_dirs):
        return {"status": "duplicate", "source_url": source_url}
    fetched_at = at or datetime.date.today().isoformat()
    channel = fetch_result.get("channel", "web")
    meta = {"channel": channel, "source_url": source_url,
            "via_query": question, "fetched_at": fetched_at}
    base = inbox if inbox is not None else INBOX
    base.mkdir(parents=True, exist_ok=True)
    path = ce.link_target(fetch_result["title"], base, message_hint=source_url)
    path.write_text(build_web_document(meta, fetch_result["text"]), encoding="utf-8")
    return {"status": "written", "path": str(path), "source_url": source_url}


def log_gap(question: str, uncovered_note: str, queued_paths: list[str], at: str,
            log_path: Path | None = None) -> None:
    path = log_path if log_path is not None else LOG_PATH
    queued = ", ".join(queued_paths) if queued_paths else "none"
    block = (
        f"\n## [{at}] query | {question}\n"
        f"- gap: {uncovered_note}\n"
        f"- queued: {queued}\n"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(block)


def _fetch(url: str) -> dict:
    import fetch_link
    return fetch_link.fetch(url)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        description="Queue fetched web sources into raw/_inbox/ and log corpus gaps."
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    fq = sub.add_parser("fetch-and-queue")
    fq.add_argument("--question", required=True)
    fq.add_argument("--url", required=True)
    fq.add_argument("--inbox")

    lg = sub.add_parser("log-gap")
    lg.add_argument("--question", required=True)
    lg.add_argument("--note", required=True)
    lg.add_argument("--at", required=True)
    lg.add_argument("--queued", default="")

    args = p.parse_args(argv)

    if args.cmd == "fetch-and-queue":
        try:
            fetched = _fetch(args.url)
        except Exception as e:
            print(json.dumps({"status": "error", "error": str(e), "url": args.url}))
            return 1
        inbox = Path(args.inbox) if args.inbox else None
        result = queue_source(args.question, fetched, args.url, inbox=inbox)
        print(json.dumps(result))
        return 0

    if args.cmd == "log-gap":
        queued = [s for s in args.queued.split(",") if s] if args.queued else []
        log_gap(args.question, args.note, queued, args.at)
        print(json.dumps({"status": "logged"}))
        return 0


if __name__ == "__main__":
    raise SystemExit(main())

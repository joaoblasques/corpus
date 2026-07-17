#!/usr/bin/env python3
"""collect_image.py — vision-ingest leg.

Scans the Drive inbox (recursively, same tree as PDFs) for image files, extracts their KNOWLEDGE
with Claude vision (headless `claude` + the Read tool reads the image), and writes a raw source
(channel: image) for the normal ingest pipeline to turn into a cited corpus page. After ingest,
`file` moves processed images into the watch dir's _processed/. Mirrors the PDF collector; reuses
collect_pdf's dedup/frontmatter helpers (DRY).

    collect  — image → Claude-vision transcription → raw/_inbox/image-<slug>.md
    file     — move images now corpus_ingested into <watch>/_processed/
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent
ROOT = BIN.parent
sys.path.insert(0, str(BIN))
import collect_pdf as cp  # noqa: E402 — reuse content_sha, fm_field, _raw_sources
from collect_email import slugify, yaml_scalar  # noqa: E402

INBOX = ROOT / "raw" / "_inbox"
IMG_STORE = ROOT / "raw" / "image"
DEDUP_DIRS = [INBOX, IMG_STORE]
WATCH_DIR = cp.PDF_WATCH_DIR                     # images live alongside PDFs in CorpusInbox/PDFs
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
PROCESSED_SUBDIR = "_processed"
CLAUDE_BIN = Path(os.environ.get("CLAUDE_BIN", str(Path.home() / ".claude" / "local" / "claude")))
VISION_MODEL = os.environ.get("CORPUS_VISION_MODEL", "claude-sonnet-4-6")
_SKIP_RE = re.compile(r"^(\.|~\$)")

_VISION_PROMPT = (
    "Read the image at this exact path: {path}\n\n"
    "It is a diagram / screenshot / notes image from a personal knowledge corpus (data engineering, "
    "AI/ML, software engineering). Produce a dense, FAITHFUL markdown transcription of its knowledge: "
    "a one-line `# ` H1 title; every text label and string it contains; the structure it depicts "
    "(boxes, arrows, layers, flow, tables); and the concepts and relationships it conveys. Do NOT "
    "invent anything not shown; if some text is unreadable, say so. Output ONLY the markdown."
)


def discover(watch_dir=None) -> list:
    root = Path(watch_dir) if watch_dir is not None else WATCH_DIR
    if not root.exists():
        return []
    out = []
    for p in sorted(root.rglob("*")):               # recurse into subfolders
        if not p.is_file() or p.suffix.lower() not in IMAGE_EXTS:
            continue
        if any(part == PROCESSED_SUBDIR or part.startswith(".")
               for part in p.relative_to(root).parts[:-1]):
            continue
        if _SKIP_RE.match(p.name):
            continue
        out.append({"abs_path": str(p), "filename": p.name})
    return out


def image_filename(filename: str, base=None) -> Path:
    base = base if base is not None else INBOX
    stem = re.sub(r"\.[^.]+$", "", filename)
    return base / f"image-{slugify(stem)}.md"


def build_image_source(meta: dict, body: str) -> str:
    lines = ["---", "channel: image", "source: image",
             f"image_origin: {meta['image_origin']}",
             f"source_path: {meta['source_path']}",
             f"title: {yaml_scalar(meta.get('title', ''))}",
             f"content_sha: {meta['content_sha']}",
             f"collected_at: {meta['collected_at']}", "---", "", body.strip(), ""]
    return "\n".join(lines)


def already_collected(sha: str, dirs=None) -> bool:
    for _, text in cp._raw_sources(dirs if dirs is not None else DEDUP_DIRS):
        if cp.fm_field(text, "content_sha") == sha:
            return True
    return False


def processable(dirs=None) -> list:
    """(source_path, image_origin) for image raw copies now corpus_ingested (ready to move)."""
    out = []
    for _, text in cp._raw_sources(dirs if dirs is not None else DEDUP_DIRS):
        if "corpus_ingested: true" not in text or cp.fm_field(text, "channel") != "image":
            continue
        origin, src = cp.fm_field(text, "image_origin"), cp.fm_field(text, "source_path")
        if origin or src:
            out.append((src, origin))
    return out


def _title_from(markdown: str, fallback: str) -> str:
    m = re.search(r"^#\s+(.+)$", markdown, re.M)
    return m.group(1).strip() if m else fallback


def vision_extract(abs_path: str, *, model=None, _run=None) -> str:
    """Headless Claude reads the image (Read tool) and returns a markdown knowledge transcription.
    Subscription auth (ANTHROPIC_API_KEY stripped). '' on any failure."""
    run = _run if _run is not None else subprocess.run
    cmd = [str(CLAUDE_BIN), "--print", _VISION_PROMPT.format(path=abs_path),
           "--output-format", "json", "--permission-mode", "bypassPermissions",
           "--allowedTools", "Read", "--model", model or VISION_MODEL]
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    try:
        proc = run(cmd, capture_output=True, text=True, timeout=300, env=env, stdin=subprocess.DEVNULL)
    except Exception:  # noqa: BLE001
        return ""
    if getattr(proc, "returncode", 1) != 0:
        return ""
    try:
        return (json.loads(proc.stdout).get("result") or "").strip()
    except (json.JSONDecodeError, AttributeError, TypeError):
        return (proc.stdout or "").strip()


def cmd_collect(args) -> int:
    at = args.collected_at or datetime.date.today().isoformat()
    inbox = Path(args.inbox) if args.inbox else INBOX
    dedup_dirs = [inbox, IMG_STORE]                 # dedup against the inbox we actually write to
    found = written = dup = failed = 0
    paths = []
    for d in discover(args.watch):
        found += 1
        try:
            sha = cp.content_sha(d["abs_path"])
        except OSError:
            failed += 1
            continue
        if already_collected(sha, dedup_dirs):
            dup += 1
            continue
        if written >= args.max:                     # cap per run; the rest come next run
            continue
        md = "" if args.dry_run else vision_extract(d["abs_path"], model=args.model)
        if not args.dry_run and len(md.split()) < 12:   # empty/garbage extraction → skip, don't file
            failed += 1
            continue
        if args.dry_run:
            written += 1
            continue
        stem = re.sub(r"\.[^.]+$", "", d["filename"])
        meta = {"image_origin": d["filename"], "source_path": d["abs_path"],
                "title": _title_from(md, stem), "content_sha": sha, "collected_at": at}
        inbox.mkdir(parents=True, exist_ok=True)
        out = image_filename(d["filename"], inbox)
        out.write_text(build_image_source(meta, md), encoding="utf-8")
        paths.append(str(out))
        written += 1
    print(json.dumps({"found": found, "written": written, "duplicate": dup, "failed": failed,
                      "dry_run": bool(args.dry_run), "paths": paths}))
    return 0


def cmd_file(args) -> int:
    """Move images now corpus_ingested into the watch dir's _processed/ (mirrors pdf `file`)."""
    root = Path(args.watch) if args.watch else WATCH_DIR
    dirs = [Path(d) for d in args.dirs] if args.dirs else None
    moved = 0
    for src, _origin in processable(dirs):
        p = Path(src) if src else None
        if not p or not p.exists():
            continue
        try:
            rel = p.relative_to(root)
        except ValueError:
            continue
        dest = root / PROCESSED_SUBDIR / rel
        if not args.dry_run:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(p), str(dest))
        moved += 1
    print(json.dumps({"moved": moved, "dry_run": bool(args.dry_run)}))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Vision-ingest leg: images → raw sources; file processed.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("collect", help="Vision-extract new images into raw/_inbox.")
    c.add_argument("--watch", default=None)
    c.add_argument("--inbox", default=None)
    c.add_argument("--collected-at", default=None)
    c.add_argument("--model", default=None)
    c.add_argument("--max", type=int, default=10)
    c.add_argument("--dry-run", action="store_true")
    c.set_defaults(func=cmd_collect)
    f = sub.add_parser("file", help="Move corpus_ingested images into <watch>/_processed/.")
    f.add_argument("--watch", default=None)
    f.add_argument("--dirs", nargs="*", default=None)
    f.add_argument("--dry-run", action="store_true")
    f.set_defaults(func=cmd_file)
    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

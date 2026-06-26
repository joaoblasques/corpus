#!/usr/bin/env python3
"""obsidian_client.py — I/O + CLI for the collect-obsidian collector."""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import subprocess
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent
sys.path.insert(0, str(BIN))
import collect_obsidian as co  # noqa: E402
import fetch_link as fl  # noqa: E402
import scrape_blog as sb  # noqa: E402


def fetch_url(url: str) -> dict:
    """Seam over fetch_link.fetch so tests can stub it. Returns {} on failure."""
    try:
        return fl.fetch(url)
    except Exception:
        return {}


def cmd_collect(args) -> int:
    vault = Path(args.vault) if args.vault else co.VAULT_ROOT
    collected_at = datetime.date.today().isoformat()
    found = co.discover(vault)
    if args.path:
        found = [d for d in found if d["rel_path"].startswith(args.path)]
    t = {"notes": 0, "urls": 0, "url_failed": 0, "skipped": 0, "scraped": 0,
         "inline_urls": 0, "inline_failed": 0, "inline_skipped_auth": 0, "inline_dropped": 0}
    processed = 0
    for d in found:
        if args.max and processed >= args.max:
            break
        processed += 1
        try:
            if d["kind"] == "note":
                title, tags, source_url, body = co.read_note(d["abs_path"])
                if not args.dry_run:
                    path = co.note_filename(d["rel_path"])
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(co.build_note_source(
                        {"vault_origin": d["rel_path"], "title": title, "tags": tags,
                         "collected_at": collected_at}, body), encoding="utf-8")
                t["notes"] += 1
                il = co.extract_inline_links(body, source_url)
                t["inline_skipped_auth"] += il["auth_skipped"]
                t["inline_dropped"] += il["dropped"]
                for url in il["links"]:
                    if co.url_already_collected(url):
                        t["skipped"] += 1
                        continue
                    if args.dry_run:
                        t["inline_urls"] += 1
                        continue
                    content = fetch_url(url)
                    if not content or not content.get("text"):
                        t["inline_failed"] += 1
                        continue
                    p2 = co.url_filename(url, content.get("title", ""))
                    p2.parent.mkdir(parents=True, exist_ok=True)
                    p2.write_text(co.build_url_source(
                        {"source_url": url, "via_vault_note": d["rel_path"],
                         "title": content.get("title", ""), "collected_at": collected_at},
                        content["text"]), encoding="utf-8")
                    t["inline_urls"] += 1
            else:  # url-list
                text = Path(d["abs_path"]).read_text(encoding="utf-8", errors="replace")
                ledger = Path(d["abs_path"]).parent / "articles_processed.md"
                for tgt in co.iter_scrape_targets(text):
                    url, mode, cap = tgt["url"], tgt["mode"], tgt["cap"]
                    if mode in ("blog", "series"):
                        if args.dry_run:
                            t["scraped"] += 1      # count the seed; no network on dry run
                            continue
                        res = sb.scrape_seed(url, mode, cap, collected_at=collected_at,
                                             via_vault_list=d["rel_path"])
                        t["scraped"] += res["written"]
                        continue
                    # untagged -> existing single-page fetch
                    if co.url_already_collected(url) or co.url_in_ledger(url, ledger):
                        t["skipped"] += 1
                        continue
                    if args.dry_run:
                        t["urls"] += 1
                        continue
                    content = fetch_url(url)
                    if not content or not content.get("text"):
                        t["url_failed"] += 1
                        continue
                    path = co.url_filename(url, content.get("title", ""))
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(co.build_url_source(
                        {"source_url": url, "via_vault_list": d["rel_path"],
                         "title": content.get("title", ""), "collected_at": collected_at},
                        content["text"]), encoding="utf-8")
                    t["urls"] += 1
        except Exception:
            t["skipped"] += 1
    print(json.dumps({**t, "dry_run": bool(args.dry_run), "discovered": len(found)}, indent=2))
    return 0


def remove_vault_note(vault_root: Path, rel_path: str) -> bool:
    """Delete a vault note, returning True iff the file was actually removed.

    Git-tracked notes are removed via `git rm` (staged, NOT committed — recoverable
    from vault history). Notes not tracked in the vault's git are deleted from the
    filesystem (recoverable instead via the raw/notes/ copy, the corpus page, and the
    clipping's source URL). Callers must gate on `_under_vault` before calling.
    """
    target = vault_root / rel_path
    if not target.exists():
        return False
    tracked = subprocess.run(
        ["git", "-C", str(vault_root), "ls-files", "--error-unmatch", rel_path],
        capture_output=True, check=False).returncode == 0
    if tracked:
        subprocess.run(["git", "-C", str(vault_root), "rm", "--quiet", rel_path],
                       capture_output=True, check=False)
    else:
        target.unlink()
    return not target.exists()


def _strike_url(vault_root: Path, list_rel: str, url: str) -> None:
    listf = vault_root / list_rel
    if listf.exists():
        original = listf.read_text(encoding="utf-8").splitlines()
        # List lines often carry a `- ` prefix or trailing punctuation, so the
        # cleaned url won't match exactly — strike any line that CONTAINS it.
        kept = [ln for ln in original if url not in ln]
        if len(kept) != len(original):  # only rewrite if something was removed
            listf.write_text("\n".join(kept) + "\n", encoding="utf-8")
    ledger = listf.parent / "articles_processed.md"
    prev = ledger.read_text(encoding="utf-8") if ledger.exists() else ""
    if url not in prev:  # don't double-append on repeated reap
        ledger.write_text(prev + url + "\n", encoding="utf-8")


def _under_vault(vault: Path, rel: str) -> bool:
    """Defense-in-depth: reject traversal / absolute paths escaping the vault."""
    if os.path.isabs(rel) or ".." in os.path.normpath(rel).split(os.sep):
        return False
    try:
        return (vault / rel).resolve().is_relative_to(vault.resolve())
    except (OSError, ValueError):
        return False


DEEP_REPORT_RE = re.compile(r"^00_Inbox/Clippings/youtube_raw/raw/watched/[^/]+/report\.md$")


def sibling_frames(vault_root: Path, rel_path: str) -> list:
    """For a claude-watch deep-analysis report.md, the sibling frame_*.jpg rel paths in
    its <slug>/ dir — so reaping the report reaps the whole folder (no orphan hero images).
    Returns [] for any other note."""
    rel = rel_path.replace("\\", "/")
    if not DEEP_REPORT_RE.match(rel):
        return []
    slug_dir = (vault_root / rel).parent
    try:
        return [str(f.relative_to(vault_root)) for f in sorted(slug_dir.glob("frame_*.jpg"))]
    except OSError:
        return []


def cmd_reap(args) -> int:
    vault = Path(args.vault) if args.vault else co.VAULT_ROOT
    r = co.reapable()
    t = {"notes_removed": 0, "frames_removed": 0, "urls_struck": 0, "not_removed": []}
    for rel in r["vault_notes"]:
        if not _under_vault(vault, rel):
            continue
        if not (vault / rel).exists():
            continue
        frames = sibling_frames(vault, rel)   # [] unless a deep-analysis report.md
        if args.dry_run:
            t["notes_removed"] += 1
            t["frames_removed"] += len(frames)
        elif remove_vault_note(vault, rel):   # count only actual deletions
            t["notes_removed"] += 1
            for fr in frames:                 # whole-folder reap: hero frames too
                if _under_vault(vault, fr) and remove_vault_note(vault, fr):
                    t["frames_removed"] += 1
        else:
            # Exists + under vault but `git rm` refused: a tracked note with
            # uncommitted local edits. Surface it instead of silently leaving it —
            # forcing the delete would destroy the user's unsaved edit.
            t["not_removed"].append(rel)
    for list_rel, url in r["url_strikes"]:
        if not args.dry_run:
            _strike_url(vault, list_rel, url)
        t["urls_struck"] += 1
    note = ("tracked notes staged via git rm (review & commit in vault); "
            "untracked notes deleted from disk (recoverable via raw/notes/ + corpus); "
            "deep-analysis report.md also stages its sibling frame_*.jpg (whole-folder reap)")
    if t["not_removed"]:
        note += (f"; {len(t['not_removed'])} note(s) NOT removed — git-tracked with "
                 "uncommitted vault edits (commit or discard the edit, then re-reap)")
    print(json.dumps({**t, "dry_run": bool(args.dry_run), "note": note}, indent=2))
    return 0


def _args(argv):
    p = argparse.ArgumentParser(description="Obsidian vault → corpus collector.")
    sub = p.add_subparsers(dest="cmd", required=True)
    pc = sub.add_parser("collect")
    pc.add_argument("--vault", default=None)
    pc.add_argument("--dry-run", action="store_true")
    pc.add_argument("--max", type=int, default=None)
    pc.add_argument("--path", default=None)
    pc.set_defaults(func=cmd_collect)
    pr = sub.add_parser("reap")
    pr.add_argument("--vault", default=None)
    pr.add_argument("--dry-run", action="store_true")
    pr.set_defaults(func=cmd_reap)
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = _args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

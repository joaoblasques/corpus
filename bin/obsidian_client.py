#!/usr/bin/env python3
"""obsidian_client.py — I/O + CLI for the collect-obsidian collector."""
from __future__ import annotations

import argparse
import datetime
import json
import subprocess
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent
sys.path.insert(0, str(BIN))
import collect_obsidian as co  # noqa: E402
import fetch_link as fl  # noqa: E402


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
    t = {"notes": 0, "urls": 0, "url_failed": 0, "skipped": 0}
    processed = 0
    for d in found:
        if args.max and processed >= args.max:
            break
        processed += 1
        try:
            if d["kind"] == "note":
                title, tags, body = co.read_note(d["abs_path"])
                if not args.dry_run:
                    path = co.note_filename(d["rel_path"])
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(co.build_note_source(
                        {"vault_origin": d["rel_path"], "title": title, "tags": tags,
                         "collected_at": collected_at}, body), encoding="utf-8")
                t["notes"] += 1
            else:  # url-list
                urls = co.parse_url_list(Path(d["abs_path"]).read_text(encoding="utf-8", errors="replace"))
                for url in urls:
                    if co.url_already_collected(url):
                        t["skipped"] += 1
                        continue
                    content = fetch_url(url)
                    if not content or not content.get("text"):
                        t["url_failed"] += 1
                        continue
                    if not args.dry_run:
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


def git_rm(vault_root: Path, rel_path: str) -> None:
    """Stage a deletion in the vault (recoverable; NOT committed)."""
    subprocess.run(["git", "-C", str(vault_root), "rm", "--quiet", rel_path],
                   capture_output=True, check=False)


def _strike_url(vault_root: Path, list_rel: str, url: str) -> None:
    listf = vault_root / list_rel
    if listf.exists():
        lines = [ln for ln in listf.read_text(encoding="utf-8").splitlines() if ln.strip() != url]
        listf.write_text("\n".join(lines) + "\n", encoding="utf-8")
    ledger = listf.parent / "articles_processed.md"
    prev = ledger.read_text(encoding="utf-8") if ledger.exists() else ""
    ledger.write_text(prev + url + "\n", encoding="utf-8")


def cmd_reap(args) -> int:
    vault = Path(args.vault) if args.vault else co.VAULT_ROOT
    r = co.reapable()
    t = {"notes_removed": 0, "urls_struck": 0}
    for rel in r["vault_notes"]:
        if (vault / rel).exists() and not args.dry_run:
            git_rm(vault, rel)
            t["notes_removed"] += 1
        elif args.dry_run and (vault / rel).exists():
            t["notes_removed"] += 1
    for list_rel, url in r["url_strikes"]:
        if not args.dry_run:
            _strike_url(vault, list_rel, url)
        t["urls_struck"] += 1
    print(json.dumps({**t, "dry_run": bool(args.dry_run),
                      "note": "vault deletions are staged, not committed — review and commit in the vault"},
                     indent=2))
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

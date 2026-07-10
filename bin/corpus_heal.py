#!/usr/bin/env python3
"""corpus_heal.py — safe, deterministic self-healing for the corpus (no LLM).

The daily ingest accumulates broken source citations: a page cites `](../../raw/_inbox/foo.md)`
but the raw file MOVED to `raw/web/foo.md` when it was ingested (or the page's relative depth is
wrong for its type). Both are fixable without judgment: find the raw file by basename and
recompute the correct relative path from the citing page. Only a UNIQUE basename match is
repointed — ambiguous or truly-missing citations are left for a human (reported, never guessed).

Reuses corpus_lint's page scan + citation regex (single source of truth). Dry-run by default;
--apply writes. Wired into the nightly after ingest, before the integrity lint.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent
ROOT = BIN.parent
sys.path.insert(0, str(BIN))
import corpus_lint as cl  # noqa: E402 — reuse content_pages + _CITATION_RE

RAW = ROOT / "raw"


def build_raw_index(raw_root: Path) -> dict:
    """basename -> [absolute paths] for every raw .md file."""
    idx: dict = {}
    for f in raw_root.rglob("*.md"):
        idx.setdefault(f.name, []).append(f.resolve())
    return idx


def repair_citations(corpus: Path, raw_root: Path, *, apply: bool = False) -> dict:
    """Repoint broken `](../..raw/..md)` citations to the unique moved raw file.

    Returns {repaired, ambiguous, missing, pages_changed, missing_list}.
    """
    idx = build_raw_index(raw_root)
    t = {"repaired": 0, "ambiguous": 0, "missing": 0, "pages_changed": 0, "missing_list": []}
    for p in cl.content_pages(corpus):
        text = p.read_text(encoding="utf-8", errors="ignore")
        new = text
        for rel in cl._CITATION_RE.findall(text):
            if (p.parent / rel).resolve().exists():
                continue                                   # citation is fine
            hits = idx.get(Path(rel).name, [])
            if len(hits) == 1:
                newrel = os.path.relpath(hits[0], p.parent.resolve())
                if newrel != rel:
                    new = new.replace(f"]({rel})", f"]({newrel})")
                    t["repaired"] += 1
            elif len(hits) > 1:
                t["ambiguous"] += 1
            else:
                t["missing"] += 1
                t["missing_list"].append(f"{p.relative_to(corpus.parent)} -> {rel}")
        if new != text:
            t["pages_changed"] += 1
            if apply:
                p.write_text(new, encoding="utf-8")
    return t


def cmd_citations(args) -> int:
    corpus = Path(args.corpus) if args.corpus else ROOT / "corpus"
    raw_root = Path(args.raw) if args.raw else RAW
    t = repair_citations(corpus, raw_root, apply=args.apply)
    print(json.dumps({**t, "missing_list": t["missing_list"][:20],
                      "applied": bool(args.apply)}, indent=2))
    return 0


def _args(argv):
    p = argparse.ArgumentParser(description="Deterministic corpus self-healing.")
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("citations", help="Repoint broken source citations to moved raw files.")
    c.add_argument("--corpus", default=None)
    c.add_argument("--raw", default=None)
    c.add_argument("--apply", action="store_true", help="write changes (default: dry-run)")
    c.set_defaults(func=cmd_citations)
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = _args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

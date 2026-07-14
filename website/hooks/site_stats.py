"""MkDocs-macros hook: inject real corpus stats (aggregate integers only) at build time.

Reads only the aggregate counts from corpus/_index.md — never any page content — so the
published site shows live numbers without leaking knowledge data. Falls back to last-known
constants if the index is unreadable (e.g. a CI checkout without the corpus), so the build
never breaks.
"""
import re
from pathlib import Path

FALLBACK = {"pages": 213, "sources": 568, "domains": 7}
_HEADER = re.compile(r"Total pages:\s*(\d+)\s*\|\s*Total sources:\s*(\d+)")


def read_corpus_stats(index_path=None) -> dict:
    # website/hooks/site_stats.py → parents[2] == repo root → corpus/_index.md
    idx = Path(index_path) if index_path else Path(__file__).resolve().parents[2] / "corpus" / "index.md"
    try:
        text = idx.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return dict(FALLBACK)
    m = _HEADER.search(text)
    if not m:
        return dict(FALLBACK)
    try:
        domains = sum(1 for p in idx.parent.iterdir() if p.is_dir() and not p.name.startswith("_"))
    except OSError:
        domains = 0
    return {
        "pages": int(m.group(1)),
        "sources": int(m.group(2)),
        "domains": domains or FALLBACK["domains"],
    }


def define_env(env):
    @env.macro
    def corpus_stats():
        return read_corpus_stats()

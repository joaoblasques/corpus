#!/usr/bin/env python3
"""okf_migrate.py — one-time migration of corpus/ to OKF v0.1.

Rewrites Obsidian [[wikilinks]] to root-relative markdown links, renames the reserved catalog/
log files, reformats the log newest-first, and stamps okf_version. Idempotent; --dry-run."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUNDLE = ROOT / "corpus"

_WIKILINK = re.compile(r"\[\[([^\]|]+?)(?:\|([^\]]+?))?\]\]")
_FENCE = re.compile(r"```.*?```", re.S)
_LOG_ENTRY = re.compile(r"^## \[(\d{4}-\d{2}-\d{2})[^\]]*\]\s*(\w+)\s*\|\s*(.+)$")


def _titlecase(seg: str) -> str:
    return " ".join(w.capitalize() for w in seg.replace("-", " ").split())


def rewrite_wikilinks(text: str, resolve=None):
    """[[target|display]] -> [display](/target.md); returns (new_text, unresolved). Skips fences."""
    unresolved: list[str] = []
    # protect fenced code blocks
    fences: list[str] = []

    def _stash(m):
        fences.append(m.group(0))
        return f"\x00FENCE{len(fences) - 1}\x00"

    protected = _FENCE.sub(_stash, text)

    def _sub(m):
        target = m.group(1).strip()
        display = (m.group(2) or "").strip()
        if "/" not in target:
            resolved = resolve(target) if resolve else None
            if not resolved:
                unresolved.append(target)
                return display or _titlecase(target)
            target = resolved
        if not display:
            display = _titlecase(target.rsplit("/", 1)[-1])
        return f"[{display}](/{target}.md)"

    out = _WIKILINK.sub(_sub, protected)
    for i, f in enumerate(fences):
        out = out.replace(f"\x00FENCE{i}\x00", f)
    return out, unresolved


def reformat_log(text: str) -> str:
    """Group log entries by date, newest first, under `## YYYY-MM-DD` headings. Lossless."""
    lines = text.splitlines()
    groups: dict[str, list[str]] = {}
    order: list[str] = []
    cur_date = None
    for ln in lines:
        m = _LOG_ENTRY.match(ln)
        if m:
            cur_date, op, subject = m.group(1), m.group(2), m.group(3)
            groups.setdefault(cur_date, [])
            if cur_date not in order:
                order.append(cur_date)
            groups[cur_date].append(f"* **{op.capitalize()}**: {subject.strip()}")
        elif cur_date is not None and ln.strip():
            # continuation lines of the current entry -> nested detail
            groups[cur_date].append(f"  {ln.strip()}")
    out = ["# Corpus Log", "", "> OKF v0.1 change log. Newest first, grouped by date.", ""]
    for d in sorted(order, reverse=True):
        out.append(f"## {d}")
        out.extend(groups[d])
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def stamp_index(text: str) -> str:
    if text.startswith("---\n") and "okf_version:" in text.split("---\n", 2)[1]:
        return text
    return '---\nokf_version: "0.1"\n---\n' + text


def ensure_type(text: str, type_value: str) -> str:
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        return f"---\ntype: {type_value}\n---\n{text}"
    fm, body = m.group(1), m.group(2)
    if re.search(r"^type:", fm, re.M):
        return text
    return f"---\ntype: {type_value}\n{fm}\n---\n{body}"

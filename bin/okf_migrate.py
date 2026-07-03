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

#!/usr/bin/env python3
"""okf_lint.py — check that corpus/ is a conformant OKF v0.1 bundle.

Three rules (SPEC §9): every non-reserved .md has parseable YAML frontmatter; every
frontmatter has a non-empty `type`; reserved files (index.md/log.md) follow their format.
Consumers MUST tolerate broken links, unknown keys, unknown type values, missing optional
fields — so this reports ONLY the three structural rules, nothing else."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUNDLE = ROOT / "corpus"
RESERVED = {"index.md", "log.md"}
_FM = re.compile(r"^---\n(.*?)---\n", re.S)


def parse_frontmatter(text: str):
    m = _FM.match(text)
    if not m:
        return None
    import yaml
    try:
        data = yaml.safe_load(m.group(1))
    except Exception:  # noqa: BLE001
        return None
    return data if isinstance(data, dict) else ({} if data is None else None)


def check_concept(path: Path, text: str) -> list[str]:
    fm = parse_frontmatter(text)
    if fm is None:
        return [f"{path}: no parseable YAML frontmatter"]
    t = fm.get("type")
    if not (isinstance(t, str) and t.strip()):
        return [f"{path}: missing/empty required `type` field"]
    return []


def check_index(path: Path, text: str, is_root: bool) -> list[str]:
    fm = parse_frontmatter(text)
    if fm is None:
        return []  # index.md with no frontmatter is valid
    if not is_root:
        return [f"{path}: non-root index.md must not have frontmatter"]
    extra = set(fm) - {"okf_version"}
    return [f"{path}: root index.md frontmatter may only contain okf_version (found {extra})"] if extra else []


def check_log(path: Path, text: str) -> list[str]:
    out = []
    for ln in text.splitlines():
        if ln.startswith("## ") and not re.match(r"^## \d{4}-\d{2}-\d{2}$", ln):
            out.append(f"{path}: log heading not ISO date group: {ln!r}")
    return out


def lint_bundle(root: Path) -> dict:
    viol, checked, concepts = [], 0, 0
    for p in sorted(root.rglob("*.md")):
        text = p.read_text(encoding="utf-8", errors="replace")
        checked += 1
        if p.name == "index.md":
            viol += check_index(p, text, is_root=(p.parent == root))
        elif p.name == "log.md":
            viol += check_log(p, text)
        else:
            concepts += 1
            viol += check_concept(p, text)
    return {"violations": viol, "checked": checked, "concepts": concepts}


def main(argv=None) -> int:
    import json
    r = lint_bundle(BUNDLE)
    print(json.dumps({"checked": r["checked"], "concepts": r["concepts"],
                      "violations": len(r["violations"]), "detail": r["violations"][:50]}, indent=2))
    return 1 if r["violations"] else 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""collect_github.py — pure logic for the GitHub repo collector.

Builds one "repo digest" markdown source per starred repo (README + docs + a metadata
overview) and dedups by the frontmatter `repo:` full-name. Network I/O lives in
github_client.py. Spec: docs/superpowers/specs/2026-06-22-github-repo-collection-design.md
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "raw" / "_inbox"
DEDUP_DIRS = [ROOT / "raw" / "_inbox", ROOT / "raw" / "github"]
_REPO_RE = re.compile(r"^repo:\s*(\S+)\s*$", re.M)


def slugify(full_name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", full_name.lower()).strip("-")
    return f"github-{s}"


def already_collected(full_name: str, dirs=None) -> bool:
    for d in (dirs if dirs is not None else DEDUP_DIRS):
        p = Path(d)
        if not p.exists():
            continue
        for md in p.glob("*.md"):
            try:
                head = md.read_text(encoding="utf-8", errors="ignore")[:1500]
            except OSError:
                continue
            m = _REPO_RE.search(head)
            if m and m.group(1) == full_name:
                return True
    return False


def _scalar(s) -> str:
    s = (str(s) if s is not None else "").replace("\n", " ").strip()
    if s and (any(c in s for c in ":#") or s[0] in "\"'[{-@`"):
        return '"' + s.replace('"', '\\"') + '"'
    return s


def build_document(repo: dict, *, collected_at: str) -> str:
    fn = repo["full_name"]
    topics = repo.get("topics") or []
    rel = repo.get("latest_release") or ""
    stars = int(repo.get("stars") or 0)
    desc = repo.get("description") or ""
    lang = repo.get("language") or ""
    lines = [
        "---", "channel: github", "source: github",
        f"repo: {fn}",
        f"repo_url: {repo.get('html_url') or ('https://github.com/' + fn)}",
        f"description: {_scalar(desc)}",
        f"language: {lang}",
        f"stars: {stars}",
        f"topics: [{', '.join(topics)}]",
        f"latest_release: {rel}",
        f"collected_at: {collected_at}",
        "---", "",
        f"# {fn}",
        "> " + " · ".join(filter(None, [
            desc, lang, f"★{stars}",
            (f"latest {rel}" if rel else ""),
            (f"topics: {', '.join(topics)}" if topics else ""),
        ])),
        "", "## README", (repo.get("readme") or "").strip(),
    ]
    docs = repo.get("docs") or []
    if docs:
        lines.append("\n## Docs")
        for d in docs:
            lines += [f"### {d.get('path', '')}", (d.get("text") or "").strip(), ""]
    return "\n".join(lines) + "\n"


def write_collected(repo: dict, *, collected_at: str, inbox=None, dedup_dirs=None) -> dict:
    fn = repo["full_name"]
    if already_collected(fn, dedup_dirs):
        return {"status": "duplicate", "path": None}
    ib = Path(inbox) if inbox is not None else INBOX
    ib.mkdir(parents=True, exist_ok=True)
    path = ib / f"{slugify(fn)}.md"
    path.write_text(build_document(repo, collected_at=collected_at), encoding="utf-8")
    return {"status": "written", "path": str(path)}

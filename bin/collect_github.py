#!/usr/bin/env python3
"""collect_github.py — pure logic for the GitHub repo collector.

Builds one "repo digest" markdown source per starred repo (README + docs + a metadata
overview) and dedups by the frontmatter `repo:` full-name. Network I/O lives in
github_client.py. Spec: docs/superpowers/specs/2026-06-22-github-repo-collection-design.md
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import github_ledger  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "raw" / "_inbox"
DEDUP_DIRS = [ROOT / "raw" / "_inbox", ROOT / "raw" / "github"]
_REPO_RE = re.compile(r"^repo:\s*(\S+)\s*$", re.M)
_INGESTED_RE = re.compile(r"^corpus_ingested:\s*true\s*$", re.M)


def slugify(full_name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", full_name.lower()).strip("-")
    return f"github-{s}"


def already_collected(full_name: str, dirs=None, ledger_path=None) -> bool:
    if github_ledger.is_digested(full_name, ledger_path or github_ledger.LEDGER_PATH):
        return True
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


def reapable(dirs=None) -> list:
    """Full-names of starred-repo digests now `corpus_ingested: true`.

    Drives the un-star reaper: once a repo's digest is in the corpus, its star on
    GitHub has served its purpose (it was just a 'to-process' marker) and can be
    removed. Mirrors collect_x.reapable. Gated on corpus_ingested; the caller
    additionally intersects with the still-starred set so DELETE is only sent for
    repos actually still starred (idempotent + quiet once drained)."""
    out, seen = [], set()
    for d in (dirs if dirs is not None else DEDUP_DIRS):
        p = Path(d)
        if not p.exists():
            continue
        for md in p.glob("*.md"):
            try:
                head = md.read_text(encoding="utf-8", errors="ignore")[:1500]
            except OSError:
                continue
            if not _INGESTED_RE.search(head):
                continue
            m = _REPO_RE.search(head)
            if m and m.group(1) not in seen:
                seen.add(m.group(1))
                out.append(m.group(1))
    return out


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


def write_collected(repo: dict, *, collected_at: str, inbox=None, dedup_dirs=None, ledger_path=None) -> dict:
    fn = repo["full_name"]
    led = ledger_path or github_ledger.LEDGER_PATH
    if already_collected(fn, dedup_dirs, ledger_path=led):
        return {"status": "duplicate", "path": None}
    ib = Path(inbox) if inbox is not None else INBOX
    ib.mkdir(parents=True, exist_ok=True)
    path = ib / f"{slugify(fn)}.md"
    path.write_text(build_document(repo, collected_at=collected_at), encoding="utf-8")
    github_ledger.mark_digested(fn, led)
    return {"status": "written", "path": str(path)}

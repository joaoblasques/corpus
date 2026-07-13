#!/usr/bin/env python3
"""consolidate_run.py — orchestrate cluster -> triage -> synthesize -> critic -> stamp/revert.

Mirrors gardener.py (headless claude via scheduled_run.CLAUDE_BIN; fail-closed Sonnet critic
reused from gardener._critic_call). Weekly, Opus writer. Spec: docs/superpowers/specs/
2026-07-11-consolidation-job-design.md
"""
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
import scheduled_run as sr  # noqa: E402
import consolidate as co  # noqa: E402
import consolidate_prompts as cp  # noqa: E402
import gardener as gd  # noqa: E402 — reuse the fail-closed provenance critic

ROOT = sr.ROOT
CORPUS = ROOT / "corpus"
REVIEW = ROOT / "raw" / "_consolidation_review.md"
LOCK = ROOT / "raw" / ".consolidate.lock"
CONSOLIDATE_MODEL = os.environ.get("CONSOLIDATE_MODEL", "claude-opus-4-8")
CONSOLIDATE_TRIAGE_MODEL = os.environ.get("CONSOLIDATE_TRIAGE_MODEL", "claude-sonnet-4-6")


def _headless(prompt: str, model: str, tools: list[str], *, _run=None) -> str:
    """Run a headless claude call; return the JSON-mode `result` string ('' on failure)."""
    run = _run if _run is not None else subprocess.run
    cmd = [str(sr.CLAUDE_BIN), "--print", prompt, "--output-format", "json",
           "--permission-mode", "bypassPermissions", "--allowedTools", *tools,
           "--model", model]
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    try:
        proc = run(cmd, capture_output=True, text=True, timeout=600, env=env,
                   stdin=subprocess.DEVNULL)
        if proc.returncode != 0:
            return ""
        return json.loads(proc.stdout).get("result", "")
    except Exception:  # noqa: BLE001
        return ""


def triage_cluster(cluster: dict, *, _run=None) -> dict:
    titles = [Path(m).stem.replace("-", " ") for m in cluster.get("members", [])]
    prompt = cp.triage_prompt(cluster["topic"], cluster["domain"], titles)
    inner = _headless(prompt, CONSOLIDATE_TRIAGE_MODEL, ["Read"], _run=_run)
    m = re.search(r"\{.*\}", inner, re.S)
    if not m:
        return {"mode": "reject", "title": "", "slug": "", "reason": "unparseable triage"}
    try:
        data = json.loads(m.group(0))
    except json.JSONDecodeError:
        return {"mode": "reject", "title": "", "slug": "", "reason": "bad json"}
    mode = data.get("mode")
    if mode not in ("new-synthesis", "deepen-existing", "reject"):
        return {"mode": "reject", "title": "", "slug": "", "reason": "unknown mode"}
    return {"mode": mode, "title": data.get("title", ""), "slug": data.get("slug", ""),
            "reason": data.get("reason", "")}


def queue_reject(cluster: dict, verdict: dict, review_path: Path) -> None:
    review_path.parent.mkdir(parents=True, exist_ok=True)
    today = datetime.date.today().isoformat()
    line = (f"- [{today}] [{verdict.get('mode')}] {cluster['domain']} · \"{cluster['topic']}\" "
            f"({cluster.get('size', len(cluster.get('members', [])))} sources) — "
            f"{verdict.get('reason', '')}\n")
    with review_path.open("a", encoding="utf-8") as f:
        f.write(line)


_CONSOLIDATED_RE = re.compile(r"^consolidated_into:\s*\S+\s*\n", re.M)


def synthesize(cluster: dict, triage: dict, corpus: Path, *, _run=None) -> Path | None:
    slug = triage.get("slug") or co._norm(cluster["topic"])
    prompt = cp.synthesis_prompt(cluster["topic"], cluster["domain"], slug, cluster["members"])
    _headless(prompt, CONSOLIDATE_MODEL, ["Read", "Write", "Edit"], _run=_run)
    out = corpus / cluster["domain"] / f"{slug}.md"
    return out if out.exists() else None


def stamp_members(cluster: dict, synthesis_rel: str, corpus: Path) -> int:
    n = 0
    for rel in cluster["members"]:
        p = corpus / rel
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        if "consolidated_into:" in text:
            n += 1
            continue
        # insert the flag just before the closing '---' of the frontmatter
        if text.startswith("---"):
            end = text.find("\n---", 3)
            if end != -1:
                text = text[:end] + f"\nconsolidated_into: {synthesis_rel}" + text[end:]
                p.write_text(text, encoding="utf-8")
                n += 1
    return n


def unstamp_members(cluster: dict, corpus: Path) -> int:
    n = 0
    for rel in cluster["members"]:
        p = corpus / rel
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        new = _CONSOLIDATED_RE.sub("", text)
        if new != text:
            p.write_text(new, encoding="utf-8")
            n += 1
    return n

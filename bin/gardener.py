#!/usr/bin/env python3
"""gardener.py — Custodian mode #1: expand stub pages into cited drafts.

Supplies next_action/execute/constraints + a lint+content-critic verifier to
custodian.run_loop. Sonnet (subscription); main-only auto-commit via the harness.
Spec: docs/superpowers/specs/2026-06-19-gardener-design.md
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import custodian as cust  # noqa: E402
import scheduled_run as sr  # noqa: E402

ROOT = sr.ROOT
CORPUS = ROOT / "corpus"
GARDENER_MODEL = os.environ.get("GARDENER_MODEL", "claude-sonnet-4-6")
_STUB_RE = re.compile(r"^status:\s*stub\s*$", re.M)
_CREATED_RE = re.compile(r"^created:\s*(\d{4}-\d{2}-\d{2})", re.M)
_SRC_PATH_RE = re.compile(r"^\s*-\s*path:\s*(\S+)", re.M)


def _frontmatter(path: Path) -> str:
    t = path.read_text(encoding="utf-8", errors="ignore")
    end = t.find("\n---", 3)
    return t[:end] if (t.startswith("---") and end != -1) else t[:2000]


def find_stubs(corpus_dir=None) -> list:
    cdir = Path(corpus_dir) if corpus_dir is not None else CORPUS
    out = []
    for md in cdir.rglob("*.md"):
        if md.name.startswith("_"):
            continue
        if _STUB_RE.search(_frontmatter(md)):
            out.append(md)
    return out


def _sources_of(stub_path: Path) -> list:
    return _SRC_PATH_RE.findall(_frontmatter(stub_path))


def is_expandable(stub_path, root=None) -> bool:
    base = Path(root) if root is not None else ROOT
    for rel in _sources_of(Path(stub_path)):
        f = base / rel
        try:
            if f.is_file() and f.stat().st_size > 0:
                return True
        except OSError:
            continue
    return False


def inbound_count(slug: str, corpus_dir=None) -> int:
    """How many wikilinks across the corpus point at this page slug (domain/name)."""
    cdir = Path(corpus_dir) if corpus_dir is not None else CORPUS
    needle = f"[[{slug}"
    n = 0
    for md in cdir.rglob("*.md"):
        try:
            n += md.read_text(encoding="utf-8", errors="ignore").count(needle)
        except OSError:
            continue
    return n


def _slug_of(stub_path: Path, corpus_dir: Path) -> str:
    rel = stub_path.relative_to(corpus_dir).with_suffix("")
    return str(rel)   # e.g. "ai-engineering/openai"


def rank_stubs(stubs, corpus_dir=None) -> list:
    cdir = Path(corpus_dir) if corpus_dir is not None else CORPUS
    def key(p):
        m = _CREATED_RE.search(_frontmatter(p))
        created = m.group(1) if m else "9999-99-99"
        return (-inbound_count(_slug_of(p, cdir), cdir), created)
    return sorted(stubs, key=key)


def make_worklist(*, corpus_dir=None, root=None, _queue=None):
    cdir = Path(corpus_dir) if corpus_dir is not None else CORPUS
    base = Path(root) if root is not None else ROOT
    queue = _queue if _queue is not None else cust.enqueue_review
    expandable, unexpandable = [], []
    for s in find_stubs(cdir):
        (expandable if is_expandable(s, root=base) else unexpandable).append(s)
    if unexpandable:
        queue("stub-no-source", {"pages": [str(p.relative_to(base)) for p in unexpandable]})
    ranked = rank_stubs(expandable, cdir)
    state = {"i": 0}
    def next_action():
        if state["i"] >= len(ranked):
            return None
        p = ranked[state["i"]]; state["i"] += 1
        return p
    return next_action


def _read_sources(stub_path: Path, base: Path) -> str:
    chunks = []
    for rel in _sources_of(stub_path):
        f = base / rel
        try:
            if f.is_file():
                chunks.append(f"### SOURCE {rel}\n{f.read_text(encoding='utf-8', errors='ignore')[:6000]}")
        except OSError:
            continue
    return "\n\n".join(chunks)


def expand_prompt(stub_path, root=None) -> str:
    base = Path(root) if root is not None else ROOT
    sp = Path(stub_path)
    page = sp.read_text(encoding="utf-8", errors="ignore")
    sources = _read_sources(sp, base)
    return (
        "You are the corpus maintainer. Read CLAUDE.md. Expand this STUB page into a "
        "full `draft` using ONLY the cited sources below. §7-strict: every non-trivial "
        "claim cites its source; ≤25-word quotes (max one per source); NEVER state a claim "
        "not present in the sources. Keep CLAUDE.md §3/§4/§14 form. Flip `status: stub` → "
        f"`status: draft` and bump `updated`. Write the file in place.\n\n"
        f"=== STUB PAGE ({sp.name}) ===\n{page}\n\n=== CITED SOURCES ===\n{sources}\n\n"
        'When done, your FINAL message must be EXACTLY: {"expanded": true}'
    )


def make_execute(*, root=None, _run=None):
    base = Path(root) if root is not None else ROOT
    run = _run if _run is not None else subprocess.run
    def execute(stub_path, constraints):
        sp = Path(stub_path)
        env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
        try:
            cmd = [str(sr.CLAUDE_BIN), "--print", constraints + "\n\n" + expand_prompt(sp, base),
                   "--output-format", "json", "--permission-mode", "bypassPermissions",
                   "--allowedTools", "Read", "Write", "Edit", "--model", GARDENER_MODEL]
            proc = run(cmd, capture_output=True, text=True, timeout=600,
                       cwd=str(base), env=env, stdin=subprocess.DEVNULL)
        except Exception as exc:  # noqa: BLE001
            return cust.Result(changed_paths=[], usage={}, errors=[f"run: {exc}"])
        if proc.returncode != 0:
            return cust.Result(changed_paths=[], usage={}, errors=[(proc.stderr or "").strip()[:200]])
        usage = {}
        try:
            usage = json.loads(proc.stdout).get("usage", {})
        except Exception:  # noqa: BLE001
            pass
        return cust.Result(changed_paths=[str(sp)], usage=usage)
    return execute


def _critic_call(page_path: Path, sources_text: str, *, _run=None):
    """Headless Sonnet: does every new claim trace to a cited source? Returns (ok, notes)."""
    run = _run if _run is not None else subprocess.run
    prompt = (
        "You are a strict fact-checker. Below is a corpus page and the FULL text of the "
        "sources it cites. List EVERY claim on the page that is NOT supported by, is "
        "misattributed to, or is absent from these sources. If all claims are supported, "
        'reply EXACTLY {"ok": true, "issues": []}. Otherwise {"ok": false, "issues": ["..."]}.'
        f"\n\n=== PAGE ===\n{page_path.read_text(encoding='utf-8', errors='ignore')}"
        f"\n\n=== CITED SOURCES ===\n{sources_text}"
    )
    cmd = [str(sr.CLAUDE_BIN), "--print", prompt, "--output-format", "json",
           "--allowedTools", "Read", "--model", GARDENER_MODEL]
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    try:
        proc = run(cmd, capture_output=True, text=True, timeout=300, env=env,
                   stdin=subprocess.DEVNULL)
        inner = json.loads(proc.stdout).get("result", "")
        m = re.search(r"\{.*\}", inner, re.S)
        data = json.loads(m.group(0)) if m else {"ok": False, "issues": ["critic: unparseable"]}
        return bool(data.get("ok")), list(data.get("issues", []))
    except Exception as exc:  # noqa: BLE001 — fail CLOSED: an unverifiable expansion is not trusted
        return False, [f"critic error: {exc}"]


def make_verify(*, root=None, _lint=None, _critic=None):
    base = Path(root) if root is not None else ROOT
    critic = _critic if _critic is not None else \
        (lambda page, src: _critic_call(Path(page), src))
    def gardener_verify(changed_paths):
        # normalize paths to be relative to base for lint matching
        rel_paths = []
        for p in (changed_paths or []):
            try:
                rel_paths.append(str(Path(p).relative_to(base)))
            except ValueError:
                rel_paths.append(str(p))
        v = cust.verify_gate(rel_paths, _lint=_lint)   # lint + attribution
        notes = list(v.notes)
        critic_ok = True
        for p in changed_paths:
            sp = Path(p)
            ok, issues = critic(str(sp), _read_sources(sp, base))
            if not ok:
                critic_ok = False
                notes += [f"critic[{sp.name}]: {i}" for i in issues]
        return cust.Verdict(ok=(v.ok and critic_ok),
                            broken_citations=v.broken_citations,
                            broken_wikilinks=v.broken_wikilinks, notes=notes)
    return gardener_verify

#!/usr/bin/env python3
"""weekly_synthesis.py — leftover-Opus harvester.

Once a week, near the end of the Opus weekly quota window (just before it resets),
spend whatever Opus credits are left on a bounded synthesis + lint pass over the
week's ingests — converting about-to-expire credits into Body-of-Knowledge value.

Guarded by a PROBE: Anthropic exposes no "remaining weekly Opus credits" API, so the
job fires a tiny Opus call first and only runs the full pass if Opus is NOT currently
rate-limited. Near reset that means: spend the leftovers; skip the week if depleted.

Uses the Claude Code SUBSCRIPTION (strips ANTHROPIC_API_KEY) — no metered API billing.
Commits only on main (TOCTOU-guarded), scoped to corpus/.
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

# Reuse the scheduled_run infrastructure (paths, lock, branch guard).
sys.path.insert(0, str(Path(__file__).resolve().parent))
import scheduled_run as sr  # noqa: E402
import corpus_lint  # noqa: E402

ROOT = sr.ROOT
CORPUS = ROOT / "corpus"
GIT_BIN = "git"
# The synthesis pass runs on OPUS deliberately (that is the whole point). Overridable
# via $SYNTHESIS_MODEL; validated to resolve on the subscription at install time.
OPUS_MODEL = os.environ.get("SYNTHESIS_MODEL", "claude-opus-4-8")
SYNTH_LOCK = ROOT / "raw" / ".weekly_synthesis.lock"


def opus_available(*, _subprocess_run=None) -> bool:
    """Probe: is Opus usable right now (subscription, not rate-limited)?

    Fires a minimal Opus call and inspects the JSON result. Returns False on any
    failure (non-zero exit, unparseable output, is_error, or exception) — i.e. it
    fails CLOSED so a rate-limited or degraded Opus never triggers the full pass.
    """
    _run = _subprocess_run if _subprocess_run is not None else subprocess.run
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    try:
        proc = _run(
            [str(sr.CLAUDE_BIN), "--model", OPUS_MODEL, "--print",
             "--output-format", "json", "Reply with exactly: OK"],
            capture_output=True, text=True, timeout=120, env=env,
            stdin=subprocess.DEVNULL,
        )
    except Exception:  # noqa: BLE001 — probe must never raise
        return False
    if proc.returncode != 0:
        return False
    try:
        data = json.loads(proc.stdout)
    except (json.JSONDecodeError, AttributeError, TypeError):
        return False
    return not data.get("is_error", False)


def recent_pages(since_days: int = 7, *, limit=None, _today=None, corpus_dir=None) -> list[Path]:
    """Corpus pages whose `updated:` frontmatter is within the last `since_days`,
    MOST-RECENTLY-UPDATED FIRST, capped to `limit` (None = all). Skips the catalog
    files (_index/_log/_config/_domains). The cap keeps a single Medium pass bounded
    even on an unusually heavy week (else a 180-page window would overflow context)."""
    cdir = Path(corpus_dir) if corpus_dir is not None else CORPUS
    if not cdir.exists():
        return []
    today = _today if _today is not None else datetime.date.today()
    cutoff = today - datetime.timedelta(days=since_days)
    dated: list[tuple] = []
    for md in cdir.rglob("*.md"):
        if md.name.startswith("_") or md.name in {"index.md", "log.md"}:
            continue
        try:
            head = md.read_text(encoding="utf-8", errors="ignore")[:2000]
        except OSError:
            continue
        m = re.search(r"^updated:\s*(\d{4}-\d{2}-\d{2})", head, re.M)
        if not m:
            continue
        try:
            d = datetime.date.fromisoformat(m.group(1))
        except ValueError:
            continue
        if d >= cutoff:
            dated.append((d.isoformat(), md.name, md))
    dated.sort(reverse=True)   # newest updated first; name as deterministic tiebreak
    pages = [t[2] for t in dated]
    return pages[:limit] if limit else pages


def _synthesis_prompt(pages: list[Path]) -> str:
    listing = "\n".join(f"- {p.relative_to(ROOT)}" for p in pages)
    return (
        "You are the corpus maintainer running a WEEKLY Opus synthesis + lint pass. "
        "Read CLAUDE.md first. Scope = MEDIUM. These corpus pages changed in the last "
        f"week:\n{listing}\n\n"
        "Do, in order, staying BOUNDED to these pages and their direct neighbours:\n"
        "1. Fix any broken citations / wikilinks on these pages.\n"
        "2. Add missing cross-links between these and existing related pages — use typed "
        "relationships (§7.1) in the prose where the link's meaning is clear.\n"
        "3. Detect contradictions among them or vs existing pages; resolve per §7.1, or "
        "create a synthesis page that names the disagreement (§7).\n"
        "4. Where the week's pages reveal a cross-source theme, write AT MOST 2 new "
        "synthesis pages (§3/§4 conventions; §7 provenance — every non-trivial claim cited).\n"
        "5. Update corpus/index.md and append a corpus/log.md entry.\n"
        "Do NOT rewrite unrelated pages or survey the whole corpus. Your FINAL message "
        'must be EXACTLY one flat JSON object and nothing else: '
        '{"pages_touched": <int>, "synthesis_pages_created": <int>, "fixes": <int>}'
    )


def run_synthesis(pages: list[Path], *, timeout_s: int = 2400, _subprocess_run=None) -> dict:
    """Headless Opus synthesis+lint pass over the recent pages. Subscription auth."""
    if not pages:
        return {"status": "ok", "note": "no_recent_pages", "pages_reviewed": 0}
    _run = _subprocess_run if _subprocess_run is not None else subprocess.run
    cmd = [
        str(sr.CLAUDE_BIN), "--print", _synthesis_prompt(pages),
        "--output-format", "json", "--permission-mode", "bypassPermissions",
        "--allowedTools", "Read", "Write", "Edit", "Glob", "Grep", "LS",
        "--model", OPUS_MODEL,
    ]
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    try:
        proc = _run(cmd, capture_output=True, text=True, timeout=timeout_s,
                    cwd=str(ROOT), env=env, stdin=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "pages_reviewed": len(pages)}
    result = {"status": "ok", "pages_reviewed": len(pages)}
    try:
        data = json.loads(proc.stdout)
        inner = data.get("result", "") if isinstance(data, dict) else ""
        m = re.search(r"\{[^{}]*\}", inner) if isinstance(inner, str) else None
        if m:
            result.update(json.loads(m.group(0)))
    except Exception:  # noqa: BLE001 — a successful agentic run can still emit odd stdout
        pass
    return result


def commit_synthesis(at: str, *, _subprocess_run=None) -> dict:
    """Stage corpus/ only, commit, push. Caller enforces the main-only guard."""
    _run = _subprocess_run if _subprocess_run is not None else subprocess.run
    _run([GIT_BIN, "add", "corpus/"], cwd=str(ROOT), capture_output=True, text=True)
    st = _run([GIT_BIN, "status", "--porcelain"], cwd=str(ROOT), capture_output=True, text=True)
    if not (st.stdout or "").strip():
        return {"status": "nothing-to-commit"}
    msg = f"chore(synthesis): weekly Opus synthesis+lint pass {at}"
    c = _run([GIT_BIN, "commit", "-m", msg], cwd=str(ROOT), capture_output=True, text=True)
    if c.returncode != 0:
        return {"status": "commit-failed", "error": (c.stderr or "").strip()}
    p = _run([GIT_BIN, "push", "origin", "main"], cwd=str(ROOT), capture_output=True, text=True)
    return {"status": "committed" if p.returncode == 0 else "push-failed",
            "push_error": None if p.returncode == 0 else (p.stderr or "").strip()}


def _on_main() -> bool:
    return bool(os.environ.get("SCHEDULED_RUN_ALLOW_ANY_BRANCH")
                or sr.current_branch() == sr.MAIN_BRANCH)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Weekly leftover-Opus synthesis+lint pass.")
    ap.add_argument("--lock-path", default=SYNTH_LOCK, type=Path)
    ap.add_argument("--timeout", type=int, default=2400)
    ap.add_argument("--since-days", type=int, default=7)
    ap.add_argument("--max-pages", type=int, default=30,
                    help="Cap pages reviewed per pass (newest-updated first) to keep a "
                         "Medium pass bounded on heavy weeks.")
    ap.add_argument("--dry-run", action="store_true",
                    help="Probe + select recent pages only; no Opus pass, no commit.")
    ap.add_argument("--force", action="store_true",
                    help="Skip the Opus-availability probe (run regardless).")
    args = ap.parse_args(argv)

    if not _on_main():
        print(json.dumps({"status": "skipped", "reason": "not_on_main"}))
        return 0
    if not sr.acquire_lock(args.lock_path):
        print(json.dumps({"status": "skipped", "reason": "lock_held"}))
        return 0
    try:
        return _run_guarded(args)
    finally:
        sr.release_lock(args.lock_path)


def _run_guarded(args) -> int:
    """Probe → select recent pages → synthesis pass → lint → commit. Lock is held
    and released by main()."""
    if not args.force and not opus_available():
        print(json.dumps({"status": "skipped",
                          "reason": "opus_unavailable_or_rate_limited"}))
        return 0
    pages = recent_pages(args.since_days, limit=args.max_pages)
    if args.dry_run:
        print(json.dumps({"status": "ok", "dry_run": True, "recent_pages": len(pages)}))
        return 0
    result = run_synthesis(pages, timeout_s=args.timeout)
    try:
        rpt = corpus_lint.lint()
        result["lint"] = {"broken_citations": len(rpt["broken_citations"]),
                          "broken_wikilinks": len(rpt["broken_wikilinks"])}
    except Exception as exc:  # noqa: BLE001
        result["lint"] = {"error": str(exc)}
    at = datetime.datetime.now().isoformat(timespec="minutes")
    if _on_main():  # TOCTOU re-check before committing
        result["commit"] = commit_synthesis(at)
    else:
        result["commit"] = {"status": "skipped", "reason": "branch_changed_during_run"}
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

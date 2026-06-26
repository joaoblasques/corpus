"""Nightly cloud orchestrator.

Defines the ordered steps of the single-cloud-writer nightly run (spec §4.1) and
implements the deterministic ones the routine agent calls around its own ingest:
  - `collect`      run cloud-safe collectors into raw/_inbox/ (Phase 1: github only)
  - `commit-push`  main-guarded `git add corpus/ automation/state/` -> commit -> push

The agent performs the judgment step (ingest) in-session; this module owns only
the mechanical steps. `--dry-run` prints the full planned shape and is the
Phase-0 smoke-test entrypoint (kept stable).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent
ROOT = BIN.parent
GIT_BIN = "git"
COLLECTOR_TIMEOUT = 1200  # s — cap a hung API call; mirrors scheduled_run.COLLECTOR_TIMEOUT

# name -> argv. Phase 1 enables only github (cloud-safe: ledger dedup, no reap).
COLLECTORS = {
    "github": [sys.executable, str(BIN / "github_client.py"), "run"],
}


def plan_steps() -> list[dict]:
    return [
        {"step": "clone_repos", "detail": "clone corpus (main) + second-brain (read-only)"},
        {"step": "collect_sources", "detail": "gmail, github(+ledger), x, pdf(Drive API), obsidian(vault clone)"},
        {"step": "drain_youtube_queue", "detail": "move raw/_pending/youtube/* into raw/_inbox/"},
        {"step": "ingest", "detail": "ingest-auto: route to existing domains, write corpus/ pages"},
        {"step": "reap_and_ledger", "detail": "un-star/un-bookmark/un-label/move; append github+obsidian ledgers"},
        {"step": "commit_and_push", "detail": "commit corpus/ + ledgers; git rm pending youtube; push corpus only"},
    ]


def _maybe_json(text: str):
    try:
        return json.loads(text)
    except (ValueError, TypeError):
        return text


def run_collectors(only=None, *, _run=None) -> dict:
    _run = _run or subprocess.run
    report = {}
    for name, cmd in COLLECTORS.items():
        if only is not None and name not in only:
            continue
        proc = _run(cmd, capture_output=True, text=True, timeout=COLLECTOR_TIMEOUT)
        report[name] = {
            "returncode": proc.returncode,
            "report": _maybe_json(proc.stdout),
        }
    return report


def _git(args, repo, _run):
    return _run([GIT_BIN, "-C", str(repo)] + args, capture_output=True, text=True)


def on_main(repo, *, _run=None) -> bool:
    _run = _run or subprocess.run
    proc = _git(["rev-parse", "--abbrev-ref", "HEAD"], repo, _run)
    return proc.returncode == 0 and proc.stdout.strip() == "main"


def commit_push(repo, *, message=None, _run=None) -> dict:
    _run = _run or subprocess.run
    repo = Path(repo)
    if not on_main(repo, _run=_run):
        return {"status": "aborted", "reason": "not on main"}
    _git(["add", "corpus", "automation/state"], repo, _run)
    staged = _git(["diff", "--cached", "--name-only"], repo, _run).stdout.strip()
    if not staged:
        return {"status": "noop"}
    n = len([s for s in staged.splitlines() if s.strip()])
    msg = message or f"chore(cloud-run): nightly corpus update — {n} file(s)"
    commit = _git(["commit", "-m", msg], repo, _run)
    if commit.returncode != 0:
        return {"status": "commit-failed", "files": n}
    push = _git(["push", "origin", "main"], repo, _run)
    return {"status": "pushed" if push.returncode == 0 else "push-failed", "files": n}


def main(argv=None, *, _run=None) -> int:
    ap = argparse.ArgumentParser(description="Nightly cloud corpus run.")
    ap.add_argument("--dry-run", action="store_true", help="print the planned steps and exit")
    sub = ap.add_subparsers(dest="cmd")

    pc = sub.add_parser("collect", help="run cloud-safe collectors into raw/_inbox/")
    pc.add_argument("--only", action="append", default=None,
                    help="restrict to named collector(s); repeatable")

    pp = sub.add_parser("commit-push", help="main-guarded commit + push of corpus/ and ledgers")
    pp.add_argument("--repo", default=str(ROOT))
    pp.add_argument("--message", default=None)

    args = ap.parse_args(argv)

    if args.cmd == "collect":
        report = run_collectors(only=args.only, _run=_run)
        print(json.dumps({"collected": report}, indent=2))
        return 0 if all(v["returncode"] == 0 for v in report.values()) else 1

    if args.cmd == "commit-push":
        res = commit_push(Path(args.repo), message=args.message, _run=_run)
        print(json.dumps(res, indent=2))
        return 0 if res["status"] in ("pushed", "noop") else 1

    if args.dry_run:
        print(json.dumps({"dry_run": True, "steps": plan_steps()}))
        return 0

    print(json.dumps({"error": "no command: pass --dry-run or a subcommand"}))
    return 1


if __name__ == "__main__":
    sys.exit(main())

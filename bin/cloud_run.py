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
import os
import re
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


def _tokenized_remote(origin_url: str, token: str) -> str:
    """Build an https push URL embedding a PAT, from an origin in either
    https or ssh (git@) form. Used in the cloud to push straight to the main
    ref with our own token (the routine sandbox runs on a claude/* branch and
    its built-in connection can't push the default branch)."""
    s = origin_url.strip()
    if s.startswith("git@"):
        host, _, path = s[4:].partition(":")          # git@github.com:owner/repo.git
    else:
        rest = re.sub(r"^https?://", "", s).split("@")[-1]
        host, _, path = rest.partition("/")            # https://github.com/owner/repo.git
    path = path.rstrip("/")
    if not path.endswith(".git"):
        path += ".git"
    return f"https://x-access-token:{token}@{host}/{path}"


def commit_push(repo, *, message=None, token=None, _run=None) -> dict:
    """Stage corpus/ + ledgers, commit, and publish to origin/main.

    Cloud mode (a GH_TOKEN/GITHUB_TOKEN is present, or `token` passed): push the
    new commit straight to the main ref via the PAT — `git push <token-url>
    HEAD:main` — regardless of the local branch, since the routine sandbox runs
    on a claude/* branch and cannot be on main. The token never enters the
    returned report or stdout (git output is captured, not printed).

    Local mode (no token): keep the strict main-branch guard and `git push
    origin main`, so a stray local run can't publish a feature branch."""
    _run = _run or subprocess.run
    repo = Path(repo)
    if token is None:
        token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""
    cloud = bool(token)
    if not cloud and not on_main(repo, _run=_run):
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
    if cloud:
        origin = _git(["remote", "get-url", "origin"], repo, _run).stdout.strip()
        push = _git(["push", _tokenized_remote(origin, token), "HEAD:main"], repo, _run)
    else:
        push = _git(["push", "origin", "main"], repo, _run)
    return {"status": "pushed" if push.returncode == 0 else "push-failed", "files": n}


def doctor(*, _run=None) -> dict:
    """Headless-readiness probe: are the secrets present and is GitHub reachable?
    Returns booleans/return-codes only — never the token value."""
    _run = _run or subprocess.run

    def _rc(cmd):
        try:
            return getattr(_run(cmd, capture_output=True, text=True), "returncode", 1)
        except Exception:  # noqa: BLE001
            return 1

    branch = _run([GIT_BIN, "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True)
    return {
        "GH_TOKEN_set": bool(os.environ.get("GH_TOKEN")),
        "GITHUB_TOKEN_set": bool(os.environ.get("GITHUB_TOKEN")),
        "SCHEDULED_RUN_INGEST_MODEL": os.environ.get("SCHEDULED_RUN_INGEST_MODEL", ""),
        "gh_auth_status_rc": _rc(["gh", "auth", "status"]),
        "gh_api_user_rc": _rc(["gh", "api", "user"]),
        "branch": getattr(branch, "stdout", "").strip(),
    }


def main(argv=None, *, _run=None) -> int:
    ap = argparse.ArgumentParser(description="Nightly cloud corpus run.")
    ap.add_argument("--dry-run", action="store_true", help="print the planned steps and exit")
    sub = ap.add_subparsers(dest="cmd")

    pc = sub.add_parser("collect", help="run cloud-safe collectors into raw/_inbox/")
    pc.add_argument("--only", action="append", default=None,
                    help="restrict to named collector(s); repeatable")

    pp = sub.add_parser("commit-push", help="commit + push corpus/ and ledgers to origin/main")
    pp.add_argument("--repo", default=str(ROOT))
    pp.add_argument("--message", default=None)

    sub.add_parser("doctor", help="probe headless readiness: secrets present + GitHub reachable")

    args = ap.parse_args(argv)

    # --dry-run is a top-level "print the plan and exit" and wins over any
    # subcommand, so adding a subcommand can never trigger a live collect/push.
    if args.dry_run:
        print(json.dumps({"dry_run": True, "steps": plan_steps()}))
        return 0

    if args.cmd == "doctor":
        print(json.dumps(doctor(_run=_run), indent=2))
        return 0

    if args.cmd == "collect":
        unknown = sorted(set(args.only or []) - set(COLLECTORS))
        if unknown:  # a typo'd collector name must fail loudly, not silently no-op to exit 0
            print(json.dumps({"error": f"unknown collector(s): {unknown}"}))
            return 1
        report = run_collectors(only=args.only, _run=_run)
        print(json.dumps({"collected": report}, indent=2))
        return 0 if all(v["returncode"] == 0 for v in report.values()) else 1

    if args.cmd == "commit-push":
        res = commit_push(Path(args.repo), message=args.message, _run=_run)
        print(json.dumps(res, indent=2))
        return 0 if res["status"] in ("pushed", "noop") else 1

    print(json.dumps({"error": "no command: pass --dry-run or a subcommand"}))
    return 1


if __name__ == "__main__":
    sys.exit(main())

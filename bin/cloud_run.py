"""Nightly cloud orchestrator (Phase 0: --dry-run skeleton only).

Defines the ordered steps of the single-cloud-writer nightly run (spec §4.1).
Later phases implement each step; this phase ships only the plan + a --dry-run
that prints it, so the orchestration shape is locked and testable with no side
effects.
"""
from __future__ import annotations

import argparse
import json
import sys


def plan_steps() -> list[dict]:
    return [
        {"step": "clone_repos", "detail": "clone corpus (main) + second-brain (read-only)"},
        {"step": "collect_sources", "detail": "gmail, github(+ledger), x, pdf(Drive API), obsidian(vault clone)"},
        {"step": "drain_youtube_queue", "detail": "move raw/_pending/youtube/* into raw/_inbox/"},
        {"step": "ingest", "detail": "ingest-auto: route to existing domains, write corpus/ pages"},
        {"step": "reap_and_ledger", "detail": "un-star/un-bookmark/un-label/move; append github+obsidian ledgers"},
        {"step": "commit_and_push", "detail": "commit corpus/ + ledgers; git rm pending youtube; push corpus only"},
    ]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Nightly cloud corpus run.")
    ap.add_argument("--dry-run", action="store_true", help="print the planned steps and exit")
    args = ap.parse_args(argv)
    if args.dry_run:
        print(json.dumps({"dry_run": True, "steps": plan_steps()}))
        return 0
    print(json.dumps({"error": "live run not implemented in Phase 0"}))
    return 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""scheduled_run.py — single-flight orchestrator scaffold for scheduled collection.

Single-flight lock (R2) via atomic O_CREAT|O_EXCL open — no flock (unreliable
on macOS).  Later tasks (U3/U5) add the collector chain, ingest, and commit/push;
this file provides only the lock primitive and a thin CLI stub.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Default lock path lives under raw/ which is covered by .gitignore rules.
# raw/.scheduled_run.lock  — added explicitly to .gitignore (see project root).
# raw/.scheduled_run.log   — also .gitignored (if used by a future U3/U5 task).
# raw/_inbox/_REVIEW.md    — already covered by the existing raw/_inbox/* rule.
LOCK_PATH = ROOT / "raw" / ".scheduled_run.lock"


# ---------------------------------------------------------------------------
# Lock primitive
# ---------------------------------------------------------------------------

def acquire_lock(lock_path: Path) -> bool:
    """Atomically acquire a single-flight lock.

    Uses O_CREAT | O_EXCL so only one process wins the race; the loser gets
    EEXIST and we return False without blocking or raising.

    Returns True on success (caller holds the lock), False if already held.
    """
    try:
        fd = os.open(
            lock_path,
            os.O_CREAT | os.O_EXCL | os.O_WRONLY,
            0o644,
        )
    except FileExistsError:
        return False

    try:
        content = f"pid={os.getpid()}\n"
        os.write(fd, content.encode())
    finally:
        os.close(fd)

    return True


def release_lock(lock_path: Path) -> None:
    """Remove the lock file.  Safe no-op when the file is absent."""
    try:
        lock_path.unlink()
    except FileNotFoundError:
        pass


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Scheduled corpus collection + ingestion orchestrator."
    )
    p.add_argument(
        "--lock-path",
        type=Path,
        default=LOCK_PATH,
        help="Path to the single-flight lock file (default: raw/.scheduled_run.lock).",
    )
    sub = p.add_subparsers(dest="command")

    # 'run' stub — full collector chain added by U3/U5
    run_p = sub.add_parser("run", help="Run the scheduled collection + ingestion pipeline.")
    run_p.add_argument(
        "--dry-run",
        action="store_true",
        help="Acquire the lock and report status without running collectors.",
    )

    return p


def main(argv=None) -> int:
    p = _build_parser()
    args = p.parse_args(argv)

    lock_path: Path = args.lock_path

    if args.command == "run":
        acquired = acquire_lock(lock_path)
        if not acquired:
            print(json.dumps({"status": "skipped", "reason": "lock_held"}))
            return 0
        try:
            # U3/U5 will add collector + ingest chain here.
            print(json.dumps({"status": "ok", "lock": str(lock_path)}))
        finally:
            release_lock(lock_path)
        return 0

    # No subcommand — print help
    p.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

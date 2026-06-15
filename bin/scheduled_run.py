#!/usr/bin/env python3
"""scheduled_run.py — single-flight orchestrator for scheduled collection + ingest.

Single-flight lock (R2) via atomic O_CREAT|O_EXCL open — no flock (unreliable
on macOS).

U3 adds: run_collectors (gmail + obsidian + youtube with per-channel isolation),
run_ingest (bounded headless claude /ingest-auto), write_run_report (append to
corpus/_log.md), and wires them into the `run` CLI subcommand.

U5 (commit/push) will slot in after run_ingest and before write_run_report —
the seam is marked "U5 SEAM" below.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BIN = ROOT / "bin"

# Default lock path lives under raw/ which is covered by .gitignore rules.
LOCK_PATH = ROOT / "raw" / ".scheduled_run.lock"

# Absolute path to the claude binary — launchd has no shell PATH.
CLAUDE_BIN = Path.home() / ".claude" / "local" / "claude"

# Default youtube token path (injectable for tests)
YOUTUBE_TOKEN_PATH = BIN / "youtube_token.json"

# Default log path (injectable via log_path kwarg or CORPUS_LOG_PATH env var for CLI tests)
_LOG_PATH_DEFAULT = ROOT / "corpus" / "_log.md"
LOG_PATH = Path(os.environ["CORPUS_LOG_PATH"]) if "CORPUS_LOG_PATH" in os.environ else _LOG_PATH_DEFAULT


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
    except BaseException:
        os.close(fd)
        lock_path.unlink(missing_ok=True)
        raise
    os.close(fd)
    return True


def release_lock(lock_path: Path) -> None:
    """Remove the lock file.  Safe no-op when the file is absent."""
    try:
        lock_path.unlink()
    except FileNotFoundError:
        pass


# ---------------------------------------------------------------------------
# Collectors
# ---------------------------------------------------------------------------

def run_collectors(
    *,
    youtube_token_path: Path | None = None,
    _subprocess_run=None,
) -> dict:
    """Run gmail, obsidian, and (if token present) youtube collectors.

    Each channel is isolated: a failure in one is recorded and skipped without
    aborting the others.

    Args:
        youtube_token_path: Path to youtube_token.json; defaults to YOUTUBE_TOKEN_PATH.
            Pass a non-existent path (e.g. tmp_path / "no_token") to simulate unconfigured.
        _subprocess_run: Injectable seam for subprocess.run (used in tests to mock calls).

    Returns:
        dict of {channel: {"status": "ok"|"failed"|"not configured", "collected": int}}
    """
    _run = _subprocess_run if _subprocess_run is not None else subprocess.run
    token_path = youtube_token_path if youtube_token_path is not None else YOUTUBE_TOKEN_PATH

    results: dict[str, dict] = {}

    # --- Gmail ---
    try:
        proc = _run(
            [sys.executable, str(BIN / "gmail_client.py"), "run"],
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            results["gmail"] = {
                "status": "failed",
                "collected": 0,
                "error": proc.stderr.strip() or f"exit {proc.returncode}",
            }
        else:
            try:
                data = json.loads(proc.stdout)
                collected = data.get("written", 0)
            except (json.JSONDecodeError, AttributeError):
                collected = 0
            results["gmail"] = {"status": "ok", "collected": collected}
    except Exception as exc:  # noqa: BLE001
        results["gmail"] = {"status": "failed", "collected": 0, "error": str(exc)}

    # --- Obsidian ---
    try:
        proc = _run(
            [sys.executable, str(BIN / "obsidian_client.py"), "collect"],
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            results["obsidian"] = {
                "status": "failed",
                "collected": 0,
                "error": proc.stderr.strip() or f"exit {proc.returncode}",
            }
        else:
            try:
                data = json.loads(proc.stdout)
                collected = data.get("written", 0)
            except (json.JSONDecodeError, AttributeError):
                collected = 0
            results["obsidian"] = {"status": "ok", "collected": collected}
    except Exception as exc:  # noqa: BLE001
        results["obsidian"] = {"status": "failed", "collected": 0, "error": str(exc)}

    # --- YouTube ---
    if not token_path.exists():
        results["youtube"] = {"status": "not configured", "collected": 0}
    else:
        try:
            proc = _run(
                [sys.executable, str(BIN / "youtube_client.py"), "run"],
                capture_output=True,
                text=True,
            )
            if proc.returncode != 0:
                results["youtube"] = {
                    "status": "failed",
                    "collected": 0,
                    "error": proc.stderr.strip() or f"exit {proc.returncode}",
                }
            else:
                try:
                    data = json.loads(proc.stdout)
                    collected = data.get("written", 0)
                except (json.JSONDecodeError, AttributeError):
                    collected = 0
                results["youtube"] = {"status": "ok", "collected": collected}
        except Exception as exc:  # noqa: BLE001
            results["youtube"] = {"status": "failed", "collected": 0, "error": str(exc)}

    return results


# ---------------------------------------------------------------------------
# Ingest
# ---------------------------------------------------------------------------

def run_ingest(
    max_n: int,
    timeout_s: int,
    *,
    claude_bin: Path | None = None,
    _subprocess_run=None,
) -> dict:
    """Invoke the headless claude /ingest-auto skill with a bounded item count.

    Args:
        max_n: Maximum inbox items to ingest in this run.
        timeout_s: Wall-clock timeout in seconds passed to subprocess.run.
        claude_bin: Path to the claude binary (defaults to CLAUDE_BIN).
        _subprocess_run: Injectable seam for subprocess.run (used in tests).

    Returns:
        dict with keys: status ("ok"|"failed"|"timeout"), ingested, deferred, error.
    """
    from rank_links import load_env  # reuse load_env from rank_links.py
    load_env()

    _run = _subprocess_run if _subprocess_run is not None else subprocess.run
    binary = claude_bin if claude_bin is not None else CLAUDE_BIN

    prompt = (
        f"Use the /ingest-auto skill. "
        f"Ingest items from raw/_inbox/ — process at most {max_n} items this run. "
        f"Follow all steps in the skill. When done, output a JSON summary with keys: "
        f"ingested (int), deferred (int), pages_created (list of str)."
    )

    cmd = [
        str(binary),
        "--print", prompt,
        "--output-format", "json",
        "--permission-mode", "bypassPermissions",
        "--allowedTools", "Read", "Write", "Edit", "Glob", "Grep", "LS",
    ]

    try:
        proc = _run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_s,
            cwd=str(ROOT),
        )
    except subprocess.TimeoutExpired:
        # Overflow stays in raw/_inbox/ for the next run — no cleanup needed.
        return {"status": "timeout", "ingested": 0, "deferred": max_n, "error": "timeout"}

    if proc.returncode != 0:
        return {
            "status": "failed",
            "ingested": 0,
            "deferred": 0,
            "error": proc.stderr.strip() or f"claude exit {proc.returncode}",
        }

    # Parse the JSON envelope claude outputs in --output-format json mode.
    try:
        envelope = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {
            "status": "failed",
            "ingested": 0,
            "deferred": 0,
            "error": f"non-JSON claude output: {proc.stdout[:200]}",
        }

    is_error = envelope.get("is_error", False)
    if is_error:
        return {
            "status": "failed",
            "ingested": 0,
            "deferred": 0,
            "error": envelope.get("result", "claude reported is_error=true"),
        }

    # Try to extract structured summary from .result (skill outputs JSON in result).
    result_text = envelope.get("result", "")
    ingested = 0
    deferred = 0
    try:
        # The skill is asked to output JSON — try to parse it from result.
        inner = json.loads(result_text) if isinstance(result_text, str) else result_text
        ingested = int(inner.get("ingested", 0))
        deferred = int(inner.get("deferred", 0))
    except (json.JSONDecodeError, TypeError, ValueError, AttributeError):
        pass  # result wasn't JSON / null / non-dict — still count as ok, counts stay 0

    return {"status": "ok", "ingested": ingested, "deferred": deferred}


# ---------------------------------------------------------------------------
# Run report
# ---------------------------------------------------------------------------

def write_run_report(
    tallies: dict,
    at: str,
    *,
    log_path: Path | None = None,
) -> None:
    """Append a scheduled run summary block to corpus/_log.md.

    Args:
        tallies: dict with keys "collectors" (output of run_collectors) and
                 "ingest" (output of run_ingest).
        at: ISO timestamp string for the log entry header.
        log_path: Path to _log.md (defaults to LOG_PATH); tests pass tmp_path.
    """
    path = log_path if log_path is not None else LOG_PATH

    collectors = tallies.get("collectors", {})
    ingest = tallies.get("ingest", {})

    # Per-channel lines
    channel_lines = []
    for channel, info in collectors.items():
        status = info.get("status", "unknown")
        collected = info.get("collected", 0)
        channel_lines.append(f"  - {channel}: {collected} collected · status={status}")

    ingested = ingest.get("ingested", 0)
    deferred = ingest.get("deferred", 0)
    ingest_status = ingest.get("status", "unknown")
    ingest_error = ingest.get("error", "")
    ingest_line = f"  - ingest: {ingested} ingested · {deferred} deferred · status={ingest_status}"
    if ingest_error:
        ingest_line += f" · error={ingest_error}"

    channels_text = "\n".join(channel_lines)
    block = (
        f"\n## [{at}] config | scheduled run\n"
        f"- collectors:\n{channels_text}\n"
        f"- ingest:\n{ingest_line}\n"
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(block)


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

    # 'run' subcommand
    run_p = sub.add_parser("run", help="Run the scheduled collection + ingestion pipeline.")
    run_p.add_argument(
        "--dry-run",
        action="store_true",
        help="Acquire the lock and report status without running collectors or ingest.",
    )
    run_p.add_argument(
        "--max",
        type=int,
        default=20,
        help="Maximum inbox items to ingest per run (default: 20).",
    )
    run_p.add_argument(
        "--timeout",
        type=int,
        default=600,
        help="Wall-clock timeout in seconds for the ingest subprocess (default: 600).",
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

        tallies: dict = {"collectors": {}, "ingest": {}}
        try:
            if args.dry_run:
                tallies["collectors"] = {"dry_run": {"status": "skipped", "collected": 0}}
                tallies["ingest"] = {"status": "skipped", "ingested": 0, "deferred": 0}
            else:
                tallies["collectors"] = run_collectors()

                tallies["ingest"] = run_ingest(
                    max_n=args.max,
                    timeout_s=args.timeout,
                )

            # U5 SEAM: commit/push goes here (after ingest, before report).

            at = datetime.datetime.now().isoformat(timespec="minutes")
            write_run_report(tallies, at=at)
        finally:
            release_lock(lock_path)

        summary = {
            "status": "ok",
            "dry_run": bool(args.dry_run),
            "collectors": tallies.get("collectors", {}),
            "ingest": tallies.get("ingest", {}),
        }
        print(json.dumps(summary))
        return 0

    # No subcommand — print help
    p.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

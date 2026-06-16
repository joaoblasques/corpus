#!/usr/bin/env python3
"""scheduled_run.py — single-flight orchestrator for scheduled collection + ingest.

Single-flight lock (R2) via atomic O_CREAT|O_EXCL open — no flock (unreliable
on macOS).

U3 adds: run_collectors (gmail + obsidian + youtube with per-channel isolation),
run_ingest (bounded headless claude /ingest-auto), write_run_report (append to
corpus/_log.md), and wires them into the `run` CLI subcommand.

U5 adds: commit_and_push — stages corpus/ only (R10), commits with a clear
revertable message, and pushes to the current branch's remote.  Wired into
`run` between ingest and write_run_report.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import ingest_candidates  # bin/ is on sys.path for callers

ROOT = Path(__file__).resolve().parent.parent
BIN = ROOT / "bin"

# Default lock path lives under raw/ which is covered by .gitignore rules.
LOCK_PATH = ROOT / "raw" / ".scheduled_run.lock"

# Absolute path to the claude binary — launchd has no shell PATH.
CLAUDE_BIN = Path.home() / ".claude" / "local" / "claude"

# Absolute path to git binary — resolved once at import time so that launchd
# (which has no shell PATH) can always find it.
GIT_BIN = shutil.which("git") or "/usr/bin/git"

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
# Branch guard — a scheduled run must operate on main only, never auto-commit
# an ingest onto whatever feature branch happens to be checked out.
# ---------------------------------------------------------------------------

MAIN_BRANCH = "main"


def current_branch(repo=None, *, _subprocess_run=None) -> str | None:
    """Return the current git branch name, or None if it can't be determined."""
    _run = _subprocess_run if _subprocess_run is not None else subprocess.run
    root = repo if repo is not None else ROOT
    try:
        proc = _run([GIT_BIN, "rev-parse", "--abbrev-ref", "HEAD"],
                    capture_output=True, text=True, cwd=str(root))
    except Exception:  # noqa: BLE001
        return None
    if proc.returncode != 0:
        return None
    return proc.stdout.strip() or None


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
                # obsidian emits {"notes": N, "urls": M, ...} — no "written" key
                collected = data.get("notes", 0) + data.get("urls", 0)
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
                # Recover a small, throttled batch of blocked transcripts each run
                # (capped so it doesn't re-trigger the transcript rate limit). The
                # recovered videos become ingest candidates on following runs.
                [sys.executable, str(BIN / "youtube_client.py"), "run",
                 "--refetch-blocked", "--refetch-max", "15"],
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
                    # youtube emits {"collected": N, ...} — no "written" key
                    collected = data.get("collected", 0)
                except (json.JSONDecodeError, AttributeError):
                    collected = 0
                results["youtube"] = {"status": "ok", "collected": collected}
        except Exception as exc:  # noqa: BLE001
            results["youtube"] = {"status": "failed", "collected": 0, "error": str(exc)}

    return results


# ---------------------------------------------------------------------------
# Inbox relocation  (I1)
# ---------------------------------------------------------------------------

# Channel → subdirectory name mapping.
_CHANNEL_DIR: dict[str, str] = {
    "youtube": "youtube",
    "email": "email",
    "web": "web",
    "matter": "matter",
    "notes": "notes",
}


def move_processed_inbox(
    inbox_dir: Path | None = None,
    raw_dir: Path | None = None,
    *,
    _mover=None,
) -> dict:
    """Relocate stamped inbox files to their channel subdirectory under raw/.

    Scans <inbox_dir>/*.md for files whose YAML frontmatter contains
    ``corpus_ingested: true``.  For each match, reads the ``channel:`` field
    and moves the file to ``<raw_dir>/<channel>/<filename>``.

    Files that are unstamped or carry an unknown/missing channel are left in
    place (skipped).  The destination directory is created if absent.

    Args:
        inbox_dir: Directory to scan (default: ROOT/raw/_inbox).
        raw_dir: Parent raw directory (default: ROOT/raw).
        _mover: Injectable callable(src: Path, dst: Path) replacing shutil.move.

    Returns:
        {"moved": int, "by_channel": {channel: count}, "skipped": int}
    """
    _move = _mover if _mover is not None else shutil.move
    inbox = inbox_dir if inbox_dir is not None else ROOT / "raw" / "_inbox"
    raw = raw_dir if raw_dir is not None else ROOT / "raw"

    moved = 0
    skipped = 0
    by_channel: dict[str, int] = {}

    for md_file in sorted(inbox.glob("*.md")):
        stamped = False
        channel = None
        try:
            text = md_file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            skipped += 1
            continue

        # Lightweight YAML frontmatter scan — match on literal lines only.
        in_front = False
        for line in text.splitlines():
            if line.strip() == "---":
                if not in_front:
                    in_front = True
                    continue
                else:
                    break  # end of frontmatter block
            if not in_front:
                break  # no opening --- found
            if line.startswith("corpus_ingested: true"):
                stamped = True
            if line.startswith("channel:"):
                channel = line.split(":", 1)[1].strip()

        if not stamped:
            skipped += 1
            continue

        if channel not in _CHANNEL_DIR:
            skipped += 1
            continue

        dest_dir = raw / _CHANNEL_DIR[channel]
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / md_file.name
        try:
            _move(md_file, dest)
        except OSError:
            skipped += 1
            continue

        moved += 1
        by_channel[channel] = by_channel.get(channel, 0) + 1

    return {"moved": moved, "by_channel": by_channel, "skipped": skipped}


# ---------------------------------------------------------------------------
# Ingest
# ---------------------------------------------------------------------------

def run_ingest(
    max_n: int,
    timeout_s: int,
    *,
    claude_bin: Path | None = None,
    _subprocess_run=None,
    _select_candidates=None,
) -> dict:
    """Invoke the headless claude /ingest-auto skill on a bounded candidate set.

    A deterministic pre-filter (ingest_candidates.select_candidates) drops
    content-less stubs (e.g. blocked/disabled YouTube transcripts) and
    already-ingested sources, so the --max budget targets substantive sources.
    When there are no candidates, the claude call is skipped entirely.

    Args:
        max_n: Maximum inbox items to ingest in this run.
        timeout_s: Wall-clock timeout in seconds passed to subprocess.run.
        claude_bin: Path to the claude binary (defaults to CLAUDE_BIN).
        _subprocess_run: Injectable seam for subprocess.run (used in tests).
        _select_candidates: Injectable seam for candidate selection (tests).

    Returns:
        dict with keys: status ("ok"|"failed"|"timeout"), ingested, deferred, error.
    """
    _run = _subprocess_run if _subprocess_run is not None else subprocess.run
    select = _select_candidates if _select_candidates is not None else ingest_candidates.select_candidates
    binary = claude_bin if claude_bin is not None else CLAUDE_BIN

    candidates = [p.name for p in select(limit=max_n)]
    if not candidates:
        return {"status": "ok", "ingested": 0, "deferred": 0, "note": "no_candidates"}

    listing = "\n".join(f"- {n}" for n in candidates)
    prompt = (
        f"Use the /ingest-auto skill. Process EXACTLY these {len(candidates)} files "
        f"in raw/_inbox/ (already filtered to substantive, un-ingested sources) — "
        f"do NOT survey or process any other inbox files:\n{listing}\n"
        f"Follow all steps in the skill. Your FINAL message must be EXACTLY one flat "
        f'JSON object and nothing else: {{"ingested": <int>, "deferred": <int>, '
        f'"pages_created": <int>, "pages_updated": <int>}}'
    )

    cmd = [
        str(binary),
        "--print", prompt,
        "--output-format", "json",
        "--permission-mode", "bypassPermissions",
        "--allowedTools", "Read", "Write", "Edit", "Glob", "Grep", "LS",
    ]

    # Use the Claude Code subscription (OAuth) for the headless ingest: strip
    # ANTHROPIC_API_KEY from the child env so it does NOT bill metered API
    # credits. stdin=DEVNULL avoids claude's 3s "no stdin" wait.
    child_env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    try:
        proc = _run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_s,
            cwd=str(ROOT),
            env=child_env,
            stdin=subprocess.DEVNULL,
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

    # Extract structured counts from .result (skill ends with a JSON summary).
    ingested, deferred = _parse_ingest_counts(envelope.get("result", ""))
    return {"status": "ok", "ingested": ingested, "deferred": deferred}


def _parse_ingest_counts(result_text) -> tuple[int, int]:
    """Extract (ingested, deferred) from the /ingest-auto skill's result text.

    The skill is instructed to END with a flat JSON object
    ``{"ingested": N, "deferred": M, ...}``. Parse it directly; if the agent
    prefixed prose, fall back to the last ``{...}`` object in the text. Returns
    (0, 0) when nothing parseable is present.
    """
    if isinstance(result_text, dict):
        try:
            return int(result_text.get("ingested", 0)), int(result_text.get("deferred", 0))
        except (TypeError, ValueError):
            return 0, 0
    if not isinstance(result_text, str):
        return 0, 0

    candidates = [result_text.strip()]
    flat_objects = re.findall(r"\{[^{}]*\}", result_text)  # flat JSON objects only
    if flat_objects:
        candidates.append(flat_objects[-1])  # trailing object, when prose precedes it
    for cand in candidates:
        try:
            obj = json.loads(cand)
        except (json.JSONDecodeError, TypeError, ValueError):
            continue
        if isinstance(obj, dict) and ("ingested" in obj or "deferred" in obj):
            try:
                return int(obj.get("ingested", 0)), int(obj.get("deferred", 0))
            except (TypeError, ValueError):
                return 0, 0
    return 0, 0


# ---------------------------------------------------------------------------
# Commit / push  (U5)
# ---------------------------------------------------------------------------

def commit_and_push(
    at: str,
    tallies: dict,
    *,
    repo_root: Path | None = None,
    _subprocess_run=None,
) -> dict:
    """Stage corpus/ changes, commit, and push to the current branch's remote.

    Stages ONLY `corpus/` — never `raw/` or `.` (R10 guarantee).

    Args:
        at: ISO timestamp string used in the commit message.
        tallies: Current run tallies dict (used to build per-channel counts in
                 the commit message).
        repo_root: Root of the git repo (defaults to ROOT).
        _subprocess_run: Injectable seam for subprocess.run (used in tests).

    Returns:
        dict with key "status": "committed" | "nothing-to-commit" | "push-failed".
        On "committed" or "push-failed", also includes "sha" and/or "push_error".
    """
    _run = _subprocess_run if _subprocess_run is not None else subprocess.run
    root = repo_root if repo_root is not None else ROOT

    # --- Detect whether corpus/ has any changes (staged or unstaged) ---
    try:
        status_proc = _run(
            [GIT_BIN, "status", "--porcelain", "--", "corpus/"],
            capture_output=True,
            text=True,
            cwd=str(root),
        )
    except Exception as exc:  # noqa: BLE001
        return {"status": "push-failed", "push_error": f"git status failed: {exc}"}

    if not (status_proc.stdout or "").strip():
        return {"status": "nothing-to-commit"}

    # --- Build human-readable per-channel counts for the commit message ---
    collectors = tallies.get("collectors", {})
    channel_parts = []
    for channel, info in collectors.items():
        n = info.get("collected", 0)
        channel_parts.append(f"{channel}={n}")
    ingest = tallies.get("ingest", {})
    channel_parts.append(f"ingested={ingest.get('ingested', 0)}")
    counts_str = ", ".join(channel_parts) if channel_parts else "no counts"

    commit_msg = f"chore(auto-ingest): scheduled run {at} — {counts_str}"

    # --- Stage ONLY corpus/ (R10: never raw/ or .) ---
    try:
        add_proc = _run(
            [GIT_BIN, "add", "corpus/"],
            capture_output=True,
            text=True,
            cwd=str(root),
        )
    except Exception as exc:  # noqa: BLE001
        return {"status": "push-failed", "push_error": f"git add failed: {exc}"}

    if add_proc.returncode != 0:
        return {
            "status": "push-failed",
            "push_error": f"git add failed (exit {add_proc.returncode}): {add_proc.stderr.strip()}",
        }

    # --- Commit ---
    try:
        commit_proc = _run(
            [GIT_BIN, "commit", "-m", commit_msg],
            capture_output=True,
            text=True,
            cwd=str(root),
        )
    except Exception as exc:  # noqa: BLE001
        return {"status": "push-failed", "push_error": f"git commit failed: {exc}"}

    if commit_proc.returncode != 0:
        return {
            "status": "push-failed",
            "push_error": f"git commit failed (exit {commit_proc.returncode}): {commit_proc.stderr.strip()}",
        }

    # Extract the short SHA from commit output (e.g. "[main abc1234] ...")
    sha = ""
    commit_out = commit_proc.stdout or ""
    m = re.search(r"\[(?:[^\]]+)\s+([0-9a-f]+)\]", commit_out)
    if m:
        sha = m.group(1)

    # --- Push ---
    # Push the current HEAD explicitly to origin so it works even when the
    # branch has no upstream tracking configured (launchd / fresh clones).
    try:
        push_proc = _run(
            [GIT_BIN, "push", "origin", "HEAD"],
            capture_output=True,
            text=True,
            cwd=str(root),
        )
    except Exception as exc:  # noqa: BLE001
        return {"status": "push-failed", "sha": sha, "push_error": f"git push raised: {exc}"}

    if push_proc.returncode != 0:
        return {
            "status": "push-failed",
            "sha": sha,
            "push_error": f"git push exit {push_proc.returncode}: {push_proc.stderr.strip()}",
        }

    return {"status": "committed", "sha": sha}


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
        tallies: dict with keys "collectors" (output of run_collectors),
                 "ingest" (output of run_ingest), and optionally "commit"
                 (output of commit_and_push).
        at: ISO timestamp string for the log entry header.
        log_path: Path to _log.md (defaults to LOG_PATH); tests pass tmp_path.
    """
    path = log_path if log_path is not None else LOG_PATH

    collectors = tallies.get("collectors", {})
    ingest = tallies.get("ingest", {})
    commit = tallies.get("commit", {})

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

    # Include commit/push line when present
    if commit:
        commit_status = commit.get("status", "unknown")
        commit_line = f"  - commit: status={commit_status}"
        sha = commit.get("sha", "")
        if sha:
            commit_line += f" · sha={sha}"
        push_error = commit.get("push_error", "")
        if push_error:
            commit_line += f" · error={push_error}"
        block += f"- commit/push:\n{commit_line}\n"

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
        # A real run must operate on `main` — never auto-commit an ingest onto a
        # feature branch that happens to be checked out. (Dry-run is read-only;
        # set SCHEDULED_RUN_ALLOW_ANY_BRANCH=1 to override for a deliberate run.)
        if (not args.dry_run
                and not os.environ.get("SCHEDULED_RUN_ALLOW_ANY_BRANCH")
                and current_branch() != MAIN_BRANCH):
            print(json.dumps({"status": "skipped", "reason": "not_on_main",
                              "branch": current_branch()}))
            return 0

        acquired = acquire_lock(lock_path)
        if not acquired:
            print(json.dumps({"status": "skipped", "reason": "lock_held"}))
            return 0

        tallies: dict = {"collectors": {}, "ingest": {}, "commit": {}}
        try:
            if args.dry_run:
                tallies["collectors"] = {"dry_run": {"status": "skipped", "collected": 0}}
                tallies["ingest"] = {"status": "skipped", "ingested": 0, "deferred": 0}
                tallies["commit"] = {"status": "skipped"}
            else:
                tallies["collectors"] = run_collectors()

                tallies["ingest"] = run_ingest(
                    max_n=args.max,
                    timeout_s=args.timeout,
                )

                # I1: relocate stamped inbox files — orchestrator does this
                # deterministically (headless agent has no move/bash tool).
                # Failure here must NOT abort the run.
                try:
                    tallies["inbox_move"] = move_processed_inbox()
                except Exception as exc:  # noqa: BLE001
                    tallies["inbox_move"] = {"moved": 0, "by_channel": {}, "skipped": 0,
                                             "error": str(exc)}

                # Write the run report BEFORE committing so it lands in the SAME
                # commit as the ingested pages — no dangling uncommitted _log.md
                # left between runs. (Commit status lives in git history + stdout.)
                at = datetime.datetime.now().isoformat(timespec="minutes")
                write_run_report(tallies, at=at)

                # U5 SEAM: commit/push — scoped to corpus/ only (R10), now also
                # carrying the report block. Push failures are recorded, not raised.
                try:
                    tallies["commit"] = commit_and_push(at=at, tallies=tallies)
                except Exception as exc:  # noqa: BLE001
                    tallies["commit"] = {"status": "push-failed", "push_error": str(exc)}
        finally:
            release_lock(lock_path)

        summary = {
            "status": "ok",
            "dry_run": bool(args.dry_run),
            "collectors": tallies.get("collectors", {}),
            "ingest": tallies.get("ingest", {}),
            "commit": tallies.get("commit", {}),
        }
        print(json.dumps(summary))
        return 0

    # No subcommand — print help
    p.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

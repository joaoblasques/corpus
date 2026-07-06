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

import corpus_lint  # bin/ is on sys.path for callers
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
_LOG_PATH_DEFAULT = ROOT / "corpus" / "log.md"
LOG_PATH = Path(os.environ["CORPUS_LOG_PATH"]) if "CORPUS_LOG_PATH" in os.environ else _LOG_PATH_DEFAULT


# ---------------------------------------------------------------------------
# Lock primitive
# ---------------------------------------------------------------------------

def _read_lock_pid(lock_path: Path) -> int | None:
    """Parse the ``pid=<n>`` recorded in a lock file; None if absent/unparseable."""
    try:
        text = lock_path.read_text(encoding="utf-8")
    except OSError:
        return None
    m = re.search(r"pid=(\d+)", text)
    return int(m.group(1)) if m else None


def _pid_alive(pid: int) -> bool:
    """True if a process with this PID currently exists (signal-0 probe)."""
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True  # exists, owned by another user
    return True


def acquire_lock(lock_path: Path) -> bool:
    """Atomically acquire a single-flight lock.

    Uses O_CREAT | O_EXCL so only one process wins the race; the loser gets
    EEXIST and we return False without blocking or raising.

    Self-healing: if an existing lock records a PID that is no longer alive (a
    previous run that died without releasing — killed, crashed, or the machine
    slept/rebooted mid-run), the lock is treated as stale, reclaimed, and
    acquisition proceeds. A lock whose PID is still alive — or whose content
    can't be parsed (e.g. a lock observed in the microsecond between create and
    pid-write) — is left untouched and we return False, so two runs never
    proceed at once.

    Returns True on success (caller holds the lock), False if already held.
    """
    try:
        fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
    except FileExistsError:
        pid = _read_lock_pid(lock_path)
        if pid is None or _pid_alive(pid):
            return False  # genuinely held, or unparseable (stay conservative)
        # Stale lock owned by a dead PID — reclaim it and retry the exclusive create once.
        lock_path.unlink(missing_ok=True)
        try:
            fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
        except FileExistsError:
            return False  # lost the reclaim race to another process

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
COLLECTOR_TIMEOUT = 1200  # s; cap each collector subprocess so a hung fetch/API call cannot freeze the whole run


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


def _on_main(repo=None, *, _subprocess_run=None) -> bool:
    """Return True if on the main branch, OR if SCHEDULED_RUN_ALLOW_ANY_BRANCH is set
    (the codebase's documented test/escape-hatch override, matching main()'s commit guard)."""
    if os.environ.get("SCHEDULED_RUN_ALLOW_ANY_BRANCH"):
        return True
    branch = current_branch(repo=repo, _subprocess_run=_subprocess_run)
    return branch == MAIN_BRANCH


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
            timeout=COLLECTOR_TIMEOUT,
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
            timeout=COLLECTOR_TIMEOUT,
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

    # --- PDF ---
    try:
        proc = _run(
            [sys.executable, str(BIN / "pdf_client.py"), "collect"],
            capture_output=True,
            text=True,
            timeout=COLLECTOR_TIMEOUT,
        )
        if proc.returncode != 0:
            results["pdf"] = {
                "status": "failed",
                "collected": 0,
                "error": proc.stderr.strip() or f"exit {proc.returncode}",
            }
        else:
            try:
                data = json.loads(proc.stdout)
                collected = data.get("collected", 0)
            except (json.JSONDecodeError, AttributeError):
                collected = 0
            results["pdf"] = {"status": "ok", "collected": collected}
    except Exception as exc:  # noqa: BLE001
        results["pdf"] = {"status": "failed", "collected": 0, "error": str(exc)}

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
                timeout=COLLECTOR_TIMEOUT,
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

    # --- GitHub: discover + star top repos in corpus domains (before collect) ---
    try:
        proc = _run(
            [sys.executable, str(BIN / "github_client.py"), "discover"],
            capture_output=True,
            text=True,
            timeout=COLLECTOR_TIMEOUT,
        )
        if proc.returncode != 0:
            results["github_discover"] = {
                "status": "failed",
                "error": proc.stderr.strip() or f"exit {proc.returncode}",
            }
        else:
            try:
                starred = json.loads(proc.stdout).get("count", 0)
            except (json.JSONDecodeError, AttributeError):
                starred = 0
            results["github_discover"] = {"status": "ok", "starred": starred}
    except Exception as exc:  # noqa: BLE001
        results["github_discover"] = {"status": "failed", "error": str(exc)}

    # --- GitHub: collect new starred repos (README + docs + overview) ---
    try:
        proc = _run(
            [sys.executable, str(BIN / "github_client.py"), "run"],
            capture_output=True,
            text=True,
            timeout=COLLECTOR_TIMEOUT,
        )
        if proc.returncode != 0:
            results["github"] = {
                "status": "failed", "collected": 0,
                "error": proc.stderr.strip() or f"exit {proc.returncode}",
            }
        else:
            try:
                data = json.loads(proc.stdout)
                collected = data.get("written", 0)
            except (json.JSONDecodeError, AttributeError):
                collected = 0
            results["github"] = {"status": "ok", "collected": collected}
    except Exception as exc:  # noqa: BLE001
        results["github"] = {"status": "failed", "collected": 0, "error": str(exc)}

    # --- X: collect new bookmarks ---
    try:
        proc = _run(
            [sys.executable, str(BIN / "x_client.py"), "run"],
            capture_output=True,
            text=True,
            timeout=COLLECTOR_TIMEOUT,
        )
        if proc.returncode != 0:
            results["x"] = {
                "status": "failed", "collected": 0,
                "error": proc.stderr.strip() or f"exit {proc.returncode}",
            }
        else:
            try:
                data = json.loads(proc.stdout)
                collected = data.get("written", 0)
            except (json.JSONDecodeError, AttributeError):
                collected = 0
            results["x"] = {"status": "ok", "collected": collected}
    except Exception as exc:  # noqa: BLE001
        results["x"] = {"status": "failed", "collected": 0, "error": str(exc)}

    # --- Email link re-fetch (self-heal transient fetch-failures) ---
    # Retry high-score links that failed to fetch at collection time so their
    # pointer email gains a companion and becomes ingestable instead of deferring
    # forever. Mirrors the youtube --refetch-blocked self-heal; capped so it never
    # re-triggers a host rate limit. Genuinely-blocked URLs stay marked.
    try:
        proc = _run(
            [sys.executable, str(BIN / "refetch_links.py"), "--min-score", "8", "--max", "10"],
            capture_output=True,
            text=True,
            timeout=COLLECTOR_TIMEOUT,
        )
        if proc.returncode != 0:
            results["links_refetch"] = {
                "status": "failed", "refetched": 0,
                "error": proc.stderr.strip() or f"exit {proc.returncode}",
            }
        else:
            try:
                data = json.loads(proc.stdout)
                refetched = data.get("refetched", 0)
            except (json.JSONDecodeError, AttributeError):
                refetched = 0
            results["links_refetch"] = {"status": "ok", "refetched": refetched}
    except Exception as exc:  # noqa: BLE001
        results["links_refetch"] = {"status": "failed", "refetched": 0, "error": str(exc)}

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
    "pdf": "pdf",
    "github": "github",
    "x": "x",
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


def run_email_relabel(*, _subprocess_run=None) -> dict:
    """Post-ingest: invoke `gmail_client.py reap-labels` to un-label + archive
    corpus-labeled emails now in the corpus. Gated on corpus_ingested inside the
    subcommand. Failure is recorded, never raised."""
    _run = _subprocess_run if _subprocess_run is not None else subprocess.run
    try:
        proc = _run([sys.executable, str(BIN / "gmail_client.py"), "reap-labels"],
                    capture_output=True, text=True)
        if proc.returncode != 0:
            return {"status": "failed", "error": proc.stderr.strip() or f"exit {proc.returncode}"}
        try:
            return json.loads(proc.stdout)
        except (json.JSONDecodeError, AttributeError):
            return {"status": "ok"}
    except Exception as exc:  # noqa: BLE001
        return {"status": "failed", "error": str(exc)}


def run_x_reap(*, _subprocess_run=None) -> dict:
    """Post-ingest: invoke `x_client.py reap` to un-bookmark posts now corpus_ingested.
    Gated on corpus_ingested inside the subcommand. Failure recorded, never raised."""
    _run = _subprocess_run if _subprocess_run is not None else subprocess.run
    try:
        proc = _run([sys.executable, str(BIN / "x_client.py"), "reap"],
                    capture_output=True, text=True)
        if proc.returncode != 0:
            return {"status": "failed", "error": proc.stderr.strip() or f"exit {proc.returncode}"}
        try:
            return json.loads(proc.stdout)
        except (json.JSONDecodeError, AttributeError):
            return {"status": "ok"}
    except Exception as exc:  # noqa: BLE001
        return {"status": "failed", "error": str(exc)}


def run_obsidian_reap(*, _subprocess_run=None) -> dict:
    """Post-ingest: invoke `obsidian_client.py reap` to strike now-ingested URLs
    (single-page AND deep-scrape seeds whose posts are all corpus_ingested) from
    TO SCRAPE.md and stage ingested vault-note deletions (git rm, never committed
    — §2 vault-removal exception). Gated on corpus_ingested inside the subcommand.
    Failure recorded, never raised."""
    _run = _subprocess_run if _subprocess_run is not None else subprocess.run
    try:
        proc = _run([sys.executable, str(BIN / "obsidian_client.py"), "reap"],
                    capture_output=True, text=True)
        if proc.returncode != 0:
            return {"status": "failed", "error": proc.stderr.strip() or f"exit {proc.returncode}"}
        try:
            return json.loads(proc.stdout)
        except (json.JSONDecodeError, AttributeError):
            return {"status": "ok"}
    except Exception as exc:  # noqa: BLE001
        return {"status": "failed", "error": str(exc)}


def run_pdf_reap(*, _subprocess_run=None) -> dict:
    """Post-ingest: invoke `pdf_client.py file` to move PDFs now corpus_ingested
    out of the Drive watch dir into its `_processed/` subfolder (gated on
    corpus_ingested inside the subcommand). Without this the watch dir never
    drains — ingested PDFs are re-scanned (and deduped) every run but never
    removed. Failure recorded, never raised."""
    _run = _subprocess_run if _subprocess_run is not None else subprocess.run
    try:
        proc = _run([sys.executable, str(BIN / "pdf_client.py"), "file"],
                    capture_output=True, text=True)
        if proc.returncode != 0:
            return {"status": "failed", "error": proc.stderr.strip() or f"exit {proc.returncode}"}
        try:
            return json.loads(proc.stdout)
        except (json.JSONDecodeError, AttributeError):
            return {"status": "ok"}
    except Exception as exc:  # noqa: BLE001
        return {"status": "failed", "error": str(exc)}


def run_github_reap(*, _subprocess_run=None) -> dict:
    """Post-ingest: invoke `github_client.py reap` to un-star repos whose digest is
    now corpus_ingested, keeping the user's GitHub stars a clean 'not yet processed
    by Corpus' list. Gated on corpus_ingested ∩ still-starred inside the subcommand.
    Failure recorded, never raised."""
    _run = _subprocess_run if _subprocess_run is not None else subprocess.run
    try:
        proc = _run([sys.executable, str(BIN / "github_client.py"), "reap"],
                    capture_output=True, text=True)
        if proc.returncode != 0:
            return {"status": "failed", "error": proc.stderr.strip() or f"exit {proc.returncode}"}
        try:
            return json.loads(proc.stdout)
        except (json.JSONDecodeError, AttributeError):
            return {"status": "ok"}
    except Exception as exc:  # noqa: BLE001
        return {"status": "failed", "error": str(exc)}


def run_youtube_quick_intake(*, max_n: int = 60, rescue_max: int = 25,
                             whisper: bool = True, timeout_s: int = 5400,
                             _subprocess_run=None) -> dict:
    """Quick-intake tech YouTube stubs into lightweight Groq-summarized source pages.

    A native Python drain (bin/quick_ingest_youtube.py) — NOT the headless-claude ingest.
    Drains BOTH transcript surfaces per night to use their separate ~daily budgets:
    captions first (fast/free, rate-limits ~15-20/window), then Whisper (audio->Groq,
    ~80s/video, uncapped but yt-dlp throttles ~60/day). The tool self-regulates — if a
    limit hasn't reset it skips and those stubs retry next night — so the backlog drains
    steadily and hands-off (~50-60/night). Whisper's ~80s/video is why timeout_s is 90min.
    Groq Whisper cost is modest (~$0.5/night). Failure recorded, never raised."""
    _run = _subprocess_run if _subprocess_run is not None else subprocess.run
    try:
        cmd = [sys.executable, str(BIN / "quick_ingest_youtube.py"),
               "--rescue", "--rescue-max", str(rescue_max), "--max", str(max_n), "--sleep", "1",
               # Tiering (docs/strategy/2026-07-06): non-whitelist playlists land metadata
               # pointer-back pages with zero transcript-surface calls; only transcript-tier
               # playlists (Corpus_queue) take the rescue/Whisper path below.
               "--metadata-fallback"]
        if whisper:
            cmd.append("--whisper")
        proc = _run(cmd, capture_output=True, text=True, timeout=timeout_s)
        if proc.returncode != 0:
            return {"status": "failed", "ingested": 0, "error": (proc.stderr or "").strip()[:200]}
        tally = {}
        for line in (proc.stdout or "").splitlines():
            line = line.strip()
            if line.startswith("{") and '"tally"' in line:
                try:
                    tally = json.loads(line).get("tally", {})
                except json.JSONDecodeError:
                    pass
        ingested = tally.get("ok_transcript", 0) + tally.get("ok_metaonly", 0)
        skipped = (tally.get("skipped_ratelimit", 0) + tally.get("skipped_norescue", 0)
                   + tally.get("skipped_whisperfail", 0))
        return {"status": "ok", "ingested": ingested, "rescued": tally.get("rescued", 0),
                "skipped": skipped}
    except Exception as exc:  # noqa: BLE001
        return {"status": "failed", "ingested": 0, "error": str(exc)}


def run_docs_quick_intake(*, max_n: int = 80, backend: str = "openrouter",
                          timeout_s: int = 2400, _subprocess_run=None) -> dict:
    """Quick-intake content-bearing web/notes stubs into lightweight source pages.

    A native drain (bin/quick_ingest_docs.py) for the raw/_inbox backlog the slow ~6/night
    headless-claude ingest can't keep up with — vault clippings, blog/article scrapes, notes.
    Uses OpenRouter FREE models (Groq free fallback when they 429), so it's free. Bounded by
    max_n to respect free-tier daily limits; the rest drains over successive nights. Thin/
    URL-only stubs are skipped (they need a fetch pass). Failure recorded, never raised."""
    _run = _subprocess_run if _subprocess_run is not None else subprocess.run
    try:
        proc = _run(
            [sys.executable, str(BIN / "quick_ingest_docs.py"),
             "--channel", "web,notes", "--backend", backend, "--max", str(max_n), "--sleep", "0.5"],
            capture_output=True, text=True, timeout=timeout_s)
        if proc.returncode != 0:
            return {"status": "failed", "ingested": 0, "error": (proc.stderr or "").strip()[:200]}
        tally = {}
        for line in (proc.stdout or "").splitlines():
            line = line.strip()
            if line.startswith("{") and '"tally"' in line:
                try:
                    tally = json.loads(line).get("tally", {})
                except json.JSONDecodeError:
                    pass
        return {"status": "ok", "ingested": tally.get("ok", 0),
                "skipped_thin": tally.get("skipped_thin", 0),
                "llm_fail": tally.get("llm_fail", 0)}
    except Exception as exc:  # noqa: BLE001
        return {"status": "failed", "ingested": 0, "error": str(exc)}


def run_youtube_playlist_reap(*, max_removals: int = 120, _subprocess_run=None) -> dict:
    """Remove already-ingested videos from collect-remove (tech) YouTube playlists.

    Runs bin/youtube_client.py reap-ingested, bounded by max_removals because each delete
    costs 50 API quota units (daily quota ~10000; the collector needs some too) — so a large
    backlog drains over successive nights. NEVER touches collect-keep/ignore playlists
    (music, exercise, skateboarding). Failure recorded, never raised."""
    _run = _subprocess_run if _subprocess_run is not None else subprocess.run
    try:
        proc = _run([sys.executable, str(BIN / "youtube_client.py"), "reap-ingested",
                     "--max", str(max_removals)], capture_output=True, text=True, timeout=900)
        if proc.returncode != 0:
            return {"status": "failed", "removed": 0, "error": (proc.stderr or "").strip()[:200]}
        try:
            d = json.loads(proc.stdout)
        except json.JSONDecodeError:
            d = {}
        return {"status": "ok", "removed": d.get("removed", 0),
                "quota_exceeded": bool(d.get("quota_exceeded", False))}
    except Exception as exc:  # noqa: BLE001
        return {"status": "failed", "removed": 0, "error": str(exc)}


def build_summary(tallies: dict, dry_run: bool) -> dict:
    """Assemble the run's stdout summary from the collected tallies. Surfaces the
    post-ingest `email_relabel` (reap-labels), `x_reap`, and `pdf_reap` results
    so counts are visible in the run log, not silently dropped."""
    return {
        "status": "ok",
        "dry_run": bool(dry_run),
        "collectors": tallies.get("collectors", {}),
        "youtube_quick": tallies.get("youtube_quick", {}),
        "docs_quick": tallies.get("docs_quick", {}),
        "youtube_reap": tallies.get("youtube_reap", {}),
        "ingest": tallies.get("ingest", {}),
        "email_relabel": tallies.get("email_relabel", {}),
        "x_reap": tallies.get("x_reap", {}),
        "obsidian_reap": tallies.get("obsidian_reap", {}),
        "pdf_reap": tallies.get("pdf_reap", {}),
        "github_reap": tallies.get("github_reap", {}),
        "commit": tallies.get("commit", {}),
    }


# ---------------------------------------------------------------------------
# Ingest
# ---------------------------------------------------------------------------

def run_ingest(
    max_n: int,
    timeout_s: int,
    *,
    claude_bin: Path | None = None,
    model: str | None = None,
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
        model: Claude model alias for the headless ingest. When None, falls back
            to $SCHEDULED_RUN_INGEST_MODEL, and when that is also unset no --model
            flag is passed (the agent inherits the session default — Opus). Set to
            a cheaper tier (e.g. "claude-haiku-4-5") to cut per-run ingest cost.
        _subprocess_run: Injectable seam for subprocess.run (used in tests).
        _select_candidates: Injectable seam for candidate selection (tests).

    Returns:
        dict with keys: status ("ok"|"failed"|"timeout"), ingested, deferred, error.
    """
    _run = _subprocess_run if _subprocess_run is not None else subprocess.run
    select = _select_candidates if _select_candidates is not None else ingest_candidates.select_candidates
    binary = claude_bin if claude_bin is not None else CLAUDE_BIN

    cand_paths = select(limit=max_n)
    if not cand_paths:
        return {"status": "ok", "ingested": 0, "deferred": 0, "note": "no_candidates"}

    # Deterministically resolve pointer emails to their fetched raw/web companion
    # and hand the agent the companion path, so it extracts from real content
    # instead of fabricating from the bare URL (the load-bearing step stays in
    # tested Python, not agent judgment).
    def _rel(c: Path) -> str:
        try:
            return c.relative_to(ROOT).as_posix()
        except ValueError:
            return c.as_posix()

    lines = []
    for p in cand_paths:
        companions = ingest_candidates.fetched_companions(p)
        if companions:
            comp = ", ".join(_rel(c) for c in companions)
            lines.append(f"- {p.name}  (pointer → extract from its fetched companion: {comp})")
        else:
            lines.append(f"- {p.name}")
    listing = "\n".join(lines)
    prompt = (
        f"Use the /ingest-auto skill. Process EXACTLY these {len(cand_paths)} files "
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

    # Optional cheaper-model override for the (dominant) ingest cost. Unset →
    # no flag → session default (Opus). $SCHEDULED_RUN_INGEST_MODEL lets the
    # unattended job opt into a cheaper tier without a code change.
    effective_model = model if model is not None else os.environ.get("SCHEDULED_RUN_INGEST_MODEL")
    if effective_model:
        cmd += ["--model", effective_model]

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

    # NOTE: `claude --print` can exit NON-ZERO even on a fully successful agentic
    # run (long ingests complete, write pages, is_error=false, yet exit 1). The
    # authoritative signal is the JSON envelope's `is_error`, NOT the exit code.
    # So parse the envelope first; only treat a non-zero exit as failure when
    # there is no parseable envelope (a genuine crash before output).
    try:
        envelope = json.loads(proc.stdout)
    except (json.JSONDecodeError, ValueError):
        return {
            "status": "failed",
            "ingested": 0,
            "deferred": 0,
            "error": (proc.stderr.strip()
                      or f"claude exit {proc.returncode}, no JSON envelope: {proc.stdout[:200]}"),
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
        n = info.get("collected", info.get("refetched", 0))
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
    """Write a scheduled run summary block into corpus/log.md (OKF format).

    Writes newest-first: the new block is INSERTED right after the log's
    title/intro header (before any existing ## date-group entries).  When a
    ``## YYYY-MM-DD`` group for today already sits at the top, the new bullets
    are appended under that existing heading instead of creating a duplicate.

    Args:
        tallies: dict with keys "collectors" (output of run_collectors),
                 "ingest" (output of run_ingest), and optionally "commit"
                 (output of commit_and_push).
        at: ISO timestamp string (YYYY-MM-DD or YYYY-MM-DDTHH:MM etc.); only
            the date part is used for the OKF heading.
        log_path: Path to log.md (defaults to LOG_PATH); tests pass tmp_path.
    """
    path = log_path if log_path is not None else LOG_PATH

    # Extract YYYY-MM-DD from the `at` string (split on T or space)
    today = re.split(r"[T ]", at)[0]
    date_heading = f"## {today}"

    collectors = tallies.get("collectors", {})
    ingest = tallies.get("ingest", {})
    commit = tallies.get("commit", {})

    # --- Build bullet lines ---
    bullets: list[str] = []

    # Collectors summary
    channel_parts = []
    for channel, info in collectors.items():
        n = info.get("refetched", info.get("collected", 0))
        channel_parts.append(f"{channel}={n}")
    collectors_str = ", ".join(channel_parts) if channel_parts else "none"
    bullets.append(f"* **Collectors**: {collectors_str}")

    # Ingest
    ingested = ingest.get("ingested", 0)
    deferred = ingest.get("deferred", 0)
    ingest_status = ingest.get("status", "unknown")
    ingest_error = ingest.get("error", "")
    ingest_str = f"{ingested} ingested · {deferred} deferred · status={ingest_status}"
    if ingest_error:
        ingest_str += f" · error={ingest_error}"
    bullets.append(f"* **Ingest**: {ingest_str}")

    # YouTube quick-intake (native Groq drain of the tech-video backlog)
    yq = tallies.get("youtube_quick")
    if yq:
        yq_str = (f"{yq.get('ingested', 0)} intake · {yq.get('rescued', 0)} rescued · "
                  f"{yq.get('skipped', 0)} skipped · status={yq.get('status', 'unknown')}")
        if yq.get("error"):
            yq_str += f" · error={yq['error']}"
        bullets.append(f"* **YoutubeQuick**: {yq_str}")

    # Web/notes quick-intake (free-LLM drain of the clippings/blog/notes backlog)
    dq = tallies.get("docs_quick")
    if dq:
        dq_str = (f"{dq.get('ingested', 0)} intake · {dq.get('skipped_thin', 0)} thin · "
                  f"{dq.get('llm_fail', 0)} llm_fail · status={dq.get('status', 'unknown')}")
        if dq.get("error"):
            dq_str += f" · error={dq['error']}"
        bullets.append(f"* **DocsQuick**: {dq_str}")

    # YouTube playlist reap (remove ingested videos from tech playlists, quota-bounded)
    yr = tallies.get("youtube_reap")
    if yr:
        yr_str = f"{yr.get('removed', 0)} removed · status={yr.get('status', 'unknown')}"
        if yr.get("quota_exceeded"):
            yr_str += " · quota_exceeded (resumes next run)"
        if yr.get("error"):
            yr_str += f" · error={yr['error']}"
        bullets.append(f"* **YoutubeReap**: {yr_str}")

    # Post-ingest corpus integrity check
    lint = tallies.get("lint")
    if lint:
        if "error" in lint:
            bullets.append(f"* **Lint**: error={lint['error']}")
        else:
            bw, bc = lint.get("broken_wikilinks", 0), lint.get("broken_citations", 0)
            flag = "  ⚠ INTEGRITY ISSUES — run bin/corpus_lint.py" if (bw or bc) else ""
            bullets.append(f"* **Lint**: {bw} broken wikilinks · {bc} broken citations · "
                           f"{lint.get('orphans', 0)} orphans · {lint.get('stubs', 0)} stubs{flag}")
            # OKF conformance guard
            okf_n = lint.get("okf_violations")
            if okf_n is not None:
                okf_flag = " ⚠" if okf_n else ""
                bullets.append(f"* **OKF**: {okf_n} violations{okf_flag}")

    # Commit/push
    if commit:
        commit_status = commit.get("status", "unknown")
        commit_str = f"status={commit_status}"
        sha = commit.get("sha", "")
        if sha:
            commit_str += f" · sha={sha}"
        push_error = commit.get("push_error", "")
        if push_error:
            commit_str += f" · error={push_error}"
        bullets.append(f"* **Commit**: {commit_str}")

    bullets_text = "\n".join(bullets)

    # --- Insert newest-first into the log ---
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    lines = existing.splitlines(keepends=True)

    # Find the first ## heading in the file
    first_h2_idx: int | None = None
    for i, line in enumerate(lines):
        if line.startswith("## "):
            first_h2_idx = i
            break

    if first_h2_idx is not None and lines[first_h2_idx].rstrip() == date_heading:
        # Same-day: find end of today's group and append bullets there
        end = first_h2_idx + 1
        while end < len(lines) and not lines[end].startswith("## "):
            end += 1
        new_lines = lines[:end] + [bullets_text + "\n"] + lines[end:]
    else:
        # New day: prepend a new ## today block before the first existing ## heading
        insert_at = first_h2_idx if first_h2_idx is not None else len(lines)
        new_block = f"{date_heading}\n{bullets_text}\n\n"
        new_lines = lines[:insert_at] + [new_block] + lines[insert_at:]

    path.write_text("".join(new_lines), encoding="utf-8")


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
        default=6,
        help="Maximum inbox items to ingest per run (default: 6). Cost-bounded: "
             "the headless Opus ingest is the dominant per-run cost, so the "
             "unattended default caps any single run's burn. A larger backlog "
             "(e.g. recovered transcripts) drains over successive daily runs.",
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

                # YouTube quick-intake: drain a bounded batch of tech stubs into
                # lightweight source pages (native Groq path, not the claude ingest).
                # Bounded caption-rescue so it stays under the rate-limit; steady
                # nightly drain of the backlog. Failure must NOT abort the run.
                try:
                    tallies["youtube_quick"] = run_youtube_quick_intake()
                except Exception as exc:  # noqa: BLE001
                    tallies["youtube_quick"] = {"status": "failed", "ingested": 0, "error": str(exc)}

                # Web/notes quick-intake: drain content-bearing inbox stubs (clippings,
                # blog scrapes, notes) into source pages via free LLMs, so the backlog
                # doesn't starve behind the slow ~6/night claude ingest. Never aborts.
                try:
                    tallies["docs_quick"] = run_docs_quick_intake()
                except Exception as exc:  # noqa: BLE001
                    tallies["docs_quick"] = {"status": "failed", "ingested": 0, "error": str(exc)}

                # Remove already-ingested videos from collect-remove (tech) playlists — the
                # collect-remove policy's cleanup, quota-bounded so it drains over nights and
                # never touches music/exercise/skate playlists. Never aborts the run.
                try:
                    tallies["youtube_reap"] = run_youtube_playlist_reap()
                except Exception as exc:  # noqa: BLE001
                    tallies["youtube_reap"] = {"status": "failed", "removed": 0, "error": str(exc)}

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

                # Post-ingest: un-label + archive corpus-labeled emails now in the
                # corpus (gated on corpus_ingested). Failure must NOT abort the run.
                try:
                    tallies["email_relabel"] = run_email_relabel()
                except Exception as exc:  # noqa: BLE001
                    tallies["email_relabel"] = {"status": "failed", "error": str(exc)}

                # Post-ingest: un-bookmark X posts now corpus_ingested (gated
                # on corpus_ingested inside the subcommand). Failure must NOT abort the run.
                try:
                    tallies["x_reap"] = run_x_reap()
                except Exception as exc:  # noqa: BLE001
                    tallies["x_reap"] = {"status": "failed", "error": str(exc)}

                # Post-ingest: strike now-ingested obsidian URLs/seeds + stage
                # ingested vault-note deletions (gated on corpus_ingested).
                # Failure must NOT abort the run.
                try:
                    tallies["obsidian_reap"] = run_obsidian_reap()
                except Exception as exc:  # noqa: BLE001
                    tallies["obsidian_reap"] = {"status": "failed", "error": str(exc)}

                # Post-ingest: move now-ingested PDFs out of the Drive watch dir
                # into _processed/ (gated on corpus_ingested). Without this the
                # watch dir never drains. Failure must NOT abort the run.
                try:
                    tallies["pdf_reap"] = run_pdf_reap()
                except Exception as exc:  # noqa: BLE001
                    tallies["pdf_reap"] = {"status": "failed", "error": str(exc)}

                # Post-ingest: un-star GitHub repos now corpus_ingested, so the user's
                # stars stay a clean 'not yet processed' list (gated on corpus_ingested
                # ∩ still-starred). Failure must NOT abort the run.
                try:
                    tallies["github_reap"] = run_github_reap()
                except Exception as exc:  # noqa: BLE001
                    tallies["github_reap"] = {"status": "failed", "error": str(exc)}

                # Post-ingest integrity backstop: deterministically lint the corpus
                # the unattended agent just wrote to, and record any broken
                # links/citations in the run report. Non-blocking — alerts, never
                # aborts (a failed lint must not lose the committed ingest).
                try:
                    report = corpus_lint.lint()
                    tallies["lint"] = {
                        "broken_wikilinks": len(report["broken_wikilinks"]),
                        "broken_citations": len(report["broken_citations"]),
                        "orphans": len(report["orphans"]),
                        "stubs": len(report["stubs"]),
                        "okf_violations": report["okf_violations"],
                    }
                except Exception as exc:  # noqa: BLE001
                    tallies["lint"] = {"error": str(exc)}

                # Write the run report BEFORE committing so it lands in the SAME
                # commit as the ingested pages — no dangling uncommitted _log.md
                # left between runs. (Commit status lives in git history + stdout.)
                at = datetime.datetime.now().isoformat(timespec="minutes")
                write_run_report(tallies, at=at)

                # U5 SEAM: commit/push — scoped to corpus/ only (R10), now also
                # carrying the report block. Push failures are recorded, not raised.
                #
                # TOCTOU guard: the start-of-run branch check (main-only) can pass,
                # then a human checks out a feature branch during the multi-minute
                # collect+ingest. Re-verify we're still on main right before the
                # commit so the auto-commit never lands on a feature branch.
                branch_now = current_branch()
                if (os.environ.get("SCHEDULED_RUN_ALLOW_ANY_BRANCH")
                        or branch_now == MAIN_BRANCH):
                    try:
                        tallies["commit"] = commit_and_push(at=at, tallies=tallies)
                    except Exception as exc:  # noqa: BLE001
                        tallies["commit"] = {"status": "push-failed", "push_error": str(exc)}
                else:
                    tallies["commit"] = {"status": "skipped",
                                         "reason": "branch_changed_during_run",
                                         "branch": branch_now}
        finally:
            release_lock(lock_path)

        summary = build_summary(tallies, args.dry_run)
        print(json.dumps(summary))
        return 0

    # No subcommand — print help
    p.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

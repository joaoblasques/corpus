#!/usr/bin/env python3
"""Tests for bin/scheduled_run.py — lock primitive and CLI stub."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Import the module under test.  Keep it at module level so all tests share
# the same import; if the module is missing pytest will error clearly.
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import scheduled_run  # noqa: E402


# ---------------------------------------------------------------------------
# Lock primitive tests
# ---------------------------------------------------------------------------

class TestAcquireLock:
    def test_acquire_succeeds_when_no_lock_exists(self, tmp_path):
        """acquire_lock returns truthy when no lock file is present."""
        lock = tmp_path / ".test_run.lock"
        result = scheduled_run.acquire_lock(lock)
        assert result, "expected truthy return when lock is free"
        assert lock.exists(), "lock file should be created after acquire"

    def test_acquire_creates_lock_file(self, tmp_path):
        """Lock file is actually written to disk after acquire."""
        lock = tmp_path / ".test_run.lock"
        scheduled_run.acquire_lock(lock)
        assert lock.is_file()

    def test_second_acquire_returns_false_while_held(self, tmp_path):
        """A second acquire while the lock is held returns False (does not block/raise)."""
        lock = tmp_path / ".test_run.lock"
        scheduled_run.acquire_lock(lock)
        result = scheduled_run.acquire_lock(lock)
        assert result is False, "expected False when lock is already held"

    def test_second_acquire_does_not_overwrite_lock_file(self, tmp_path):
        """Lock file contents and mtime are unchanged after a failed second acquire."""
        lock = tmp_path / ".test_run.lock"
        scheduled_run.acquire_lock(lock)
        original_content = lock.read_text(encoding="utf-8")
        original_mtime = lock.stat().st_mtime
        scheduled_run.acquire_lock(lock)
        assert lock.read_text(encoding="utf-8") == original_content
        assert lock.stat().st_mtime == original_mtime


class TestReleaseLock:
    def test_release_removes_lock_file(self, tmp_path):
        """release_lock removes the lock file that was created by acquire."""
        lock = tmp_path / ".test_run.lock"
        scheduled_run.acquire_lock(lock)
        assert lock.exists()
        scheduled_run.release_lock(lock)
        assert not lock.exists(), "lock file should be gone after release"

    def test_release_on_absent_lock_is_noop(self, tmp_path):
        """release_lock on a non-existent path raises no exception."""
        lock = tmp_path / ".no_such.lock"
        assert not lock.exists()
        scheduled_run.release_lock(lock)  # must not raise

    def test_acquire_succeeds_after_release(self, tmp_path):
        """After releasing a lock a new acquire succeeds (round-trip)."""
        lock = tmp_path / ".test_run.lock"
        scheduled_run.acquire_lock(lock)
        scheduled_run.release_lock(lock)
        result = scheduled_run.acquire_lock(lock)
        assert result, "expected truthy return after release clears the lock"
        assert lock.exists()


# ---------------------------------------------------------------------------
# Default lock path
# ---------------------------------------------------------------------------

class TestDefaultLockPath:
    def test_default_lock_path_is_under_raw(self):
        """LOCK_PATH (module constant) must resolve inside the raw/ directory."""
        lock_path = scheduled_run.LOCK_PATH
        raw_dir = scheduled_run.ROOT / "raw"
        assert str(lock_path).startswith(str(raw_dir)), (
            f"LOCK_PATH {lock_path!r} should be under {raw_dir!r}"
        )

    def test_default_lock_path_name(self):
        """LOCK_PATH filename is .scheduled_run.lock."""
        assert scheduled_run.LOCK_PATH.name == ".scheduled_run.lock"


# ---------------------------------------------------------------------------
# CLI smoke test  (thin `run` subcommand)
# ---------------------------------------------------------------------------

class TestCLI:
    def _run_cli(self, *args, lock_path: Path | None = None):
        """Helper: invoke the CLI in a subprocess and return (returncode, stdout)."""
        cmd = [sys.executable, str(Path(__file__).resolve().parent.parent / "bin" / "scheduled_run.py")]
        if lock_path is not None:
            cmd += ["--lock-path", str(lock_path)]
        cmd += list(args)
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode, result.stdout.strip()

    def test_run_subcommand_exits_zero(self, tmp_path):
        """The `run` subcommand exits with code 0."""
        lock = tmp_path / ".cli_test.lock"
        rc, _ = self._run_cli("run", lock_path=lock)
        assert rc == 0

    def test_run_subcommand_prints_json(self, tmp_path):
        """The `run` subcommand prints a JSON line to stdout."""
        lock = tmp_path / ".cli_test.lock"
        _, out = self._run_cli("run", lock_path=lock)
        parsed = json.loads(out)
        assert "status" in parsed

    def test_run_subcommand_releases_lock(self, tmp_path):
        """The `run` subcommand releases the lock on exit (lock file absent after run)."""
        lock = tmp_path / ".cli_test.lock"
        self._run_cli("run", lock_path=lock)
        assert not lock.exists(), "lock file should be cleaned up after CLI run"

    def test_run_subcommand_skips_when_lock_already_held(self, tmp_path):
        """The `run` subcommand exits 0 and reports skipped/lock_held when lock pre-exists."""
        lock = tmp_path / ".cli_test.lock"
        # Simulate a lock already held by another process.
        lock.write_text("pid=99999\n", encoding="utf-8")
        rc, out = self._run_cli("run", lock_path=lock)
        assert rc == 0, f"expected exit 0 when lock is held, got {rc}"
        parsed = json.loads(out)
        assert parsed.get("status") == "skipped", f"expected status='skipped', got {parsed}"
        assert parsed.get("reason") == "lock_held", f"expected reason='lock_held', got {parsed}"

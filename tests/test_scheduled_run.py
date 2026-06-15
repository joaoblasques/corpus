#!/usr/bin/env python3
"""Tests for bin/scheduled_run.py — lock primitive, collectors, ingest, run report, CLI."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from unittest import mock
from unittest.mock import MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# Import the module under test.  Keep it at module level so all tests share
# the same import; if the module is missing pytest will error clearly.
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import scheduled_run  # noqa: E402


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_proc(returncode=0, stdout="", stderr=""):
    """Build a fake CompletedProcess-like object."""
    p = MagicMock()
    p.returncode = returncode
    p.stdout = stdout
    p.stderr = stderr
    return p


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
# CLI smoke test  (thin `run` subcommand — preserved from U2)
# ---------------------------------------------------------------------------

class TestCLI:
    def _run_cli(self, *args, lock_path: Path | None = None, log_path: Path | None = None):
        """Helper: invoke the CLI in a subprocess and return (returncode, stdout).

        log_path is passed via CORPUS_LOG_PATH env var so the subprocess writes
        to a tmp file rather than the real corpus/_log.md.
        """
        cmd = [sys.executable, str(Path(__file__).resolve().parent.parent / "bin" / "scheduled_run.py")]
        if lock_path is not None:
            cmd += ["--lock-path", str(lock_path)]
        cmd += list(args)
        env = dict(__import__("os").environ)
        if log_path is not None:
            env["CORPUS_LOG_PATH"] = str(log_path)
        result = subprocess.run(cmd, capture_output=True, text=True, env=env)
        return result.returncode, result.stdout.strip()

    def test_run_subcommand_exits_zero(self, tmp_path):
        """The `run --dry-run` subcommand exits with code 0."""
        lock = tmp_path / ".cli_test.lock"
        log = tmp_path / "_log.md"
        rc, _ = self._run_cli("run", "--dry-run", lock_path=lock, log_path=log)
        assert rc == 0

    def test_run_subcommand_prints_json(self, tmp_path):
        """The `run --dry-run` subcommand prints a JSON line to stdout."""
        lock = tmp_path / ".cli_test.lock"
        log = tmp_path / "_log.md"
        _, out = self._run_cli("run", "--dry-run", lock_path=lock, log_path=log)
        parsed = json.loads(out)
        assert "status" in parsed

    def test_run_subcommand_releases_lock(self, tmp_path):
        """The `run --dry-run` subcommand releases the lock on exit."""
        lock = tmp_path / ".cli_test.lock"
        log = tmp_path / "_log.md"
        self._run_cli("run", "--dry-run", lock_path=lock, log_path=log)
        assert not lock.exists(), "lock file should be cleaned up after CLI run"

    def test_run_subcommand_skips_when_lock_already_held(self, tmp_path):
        """The `run` subcommand exits 0 and reports skipped/lock_held when lock pre-exists."""
        lock = tmp_path / ".cli_test.lock"
        log = tmp_path / "_log.md"
        # Simulate a lock already held by another process.
        lock.write_text("pid=99999\n", encoding="utf-8")
        rc, out = self._run_cli("run", lock_path=lock, log_path=log)
        assert rc == 0, f"expected exit 0 when lock is held, got {rc}"
        parsed = json.loads(out)
        assert parsed.get("status") == "skipped", f"expected status='skipped', got {parsed}"
        assert parsed.get("reason") == "lock_held", f"expected reason='lock_held', got {parsed}"


# ---------------------------------------------------------------------------
# run_collectors tests
# ---------------------------------------------------------------------------

class TestRunCollectors:
    def test_gmail_and_obsidian_invoked(self, tmp_path):
        """run_collectors calls gmail run and obsidian collect via subprocess."""
        calls = []

        def fake_run(cmd, **kwargs):
            calls.append(cmd)
            return _make_proc(returncode=0, stdout=json.dumps({"written": 1}))

        # Point youtube token at a non-existent path so YouTube is skipped.
        no_token = tmp_path / "no_youtube_token.json"
        result = scheduled_run.run_collectors(
            youtube_token_path=no_token,
            _subprocess_run=fake_run,
        )

        called_scripts = [" ".join(c) for c in calls]
        assert any("gmail_client.py" in s and "run" in s for s in called_scripts), (
            f"gmail_client.py run not found in calls: {called_scripts}"
        )
        assert any("obsidian_client.py" in s and "collect" in s for s in called_scripts), (
            f"obsidian_client.py collect not found in calls: {called_scripts}"
        )

    def test_gmail_failure_recorded_obsidian_still_succeeds(self, tmp_path):
        """A failing gmail leg is recorded as failed while obsidian records success."""
        no_token = tmp_path / "no_token.json"

        def fake_run(cmd, **kwargs):
            script = cmd[1] if len(cmd) > 1 else ""
            if "gmail" in script:
                return _make_proc(returncode=1, stderr="auth error")
            # obsidian succeeds
            return _make_proc(returncode=0, stdout=json.dumps({"written": 3}))

        result = scheduled_run.run_collectors(
            youtube_token_path=no_token,
            _subprocess_run=fake_run,
        )

        assert result["gmail"]["status"] == "failed", f"gmail should be failed: {result['gmail']}"
        assert result["obsidian"]["status"] == "ok", f"obsidian should be ok: {result['obsidian']}"
        assert result["obsidian"]["collected"] == 3

    def test_gmail_exception_recorded_obsidian_still_succeeds(self, tmp_path):
        """A thrown exception in gmail leg is recorded and obsidian still runs."""
        no_token = tmp_path / "no_token.json"
        call_log = []

        def fake_run(cmd, **kwargs):
            script = cmd[1] if len(cmd) > 1 else ""
            if "gmail" in script:
                raise OSError("network error")
            call_log.append("obsidian")
            return _make_proc(returncode=0, stdout=json.dumps({"written": 2}))

        result = scheduled_run.run_collectors(
            youtube_token_path=no_token,
            _subprocess_run=fake_run,
        )

        assert result["gmail"]["status"] == "failed"
        assert "network error" in result["gmail"].get("error", "")
        assert result["obsidian"]["status"] == "ok"
        assert "obsidian" in call_log  # obsidian was called despite gmail failure

    def test_youtube_skipped_when_token_absent(self, tmp_path):
        """run_collectors records youtube as 'not configured' when token file is absent."""
        no_token = tmp_path / "youtube_token.json"  # doesn't exist
        assert not no_token.exists()

        def fake_run(cmd, **kwargs):
            return _make_proc(returncode=0, stdout=json.dumps({"written": 0}))

        result = scheduled_run.run_collectors(
            youtube_token_path=no_token,
            _subprocess_run=fake_run,
        )

        assert "youtube" in result
        assert result["youtube"]["status"] == "not configured"

    def test_youtube_invoked_when_token_present(self, tmp_path):
        """run_collectors invokes youtube_client.py when the token file exists."""
        token = tmp_path / "youtube_token.json"
        token.write_text("{}", encoding="utf-8")

        calls = []

        def fake_run(cmd, **kwargs):
            calls.append(cmd)
            return _make_proc(returncode=0, stdout=json.dumps({"written": 5}))

        result = scheduled_run.run_collectors(
            youtube_token_path=token,
            _subprocess_run=fake_run,
        )

        called_scripts = [" ".join(c) for c in calls]
        assert any("youtube_client.py" in s and "run" in s for s in called_scripts), (
            f"youtube_client.py run not found: {called_scripts}"
        )
        assert result["youtube"]["status"] == "ok"
        assert result["youtube"]["collected"] == 5


# ---------------------------------------------------------------------------
# run_ingest tests
# ---------------------------------------------------------------------------

class TestRunIngest:
    def test_builds_bounded_invocation(self, tmp_path):
        """run_ingest passes --max N in the command and timeout=<timeout_s> to subprocess."""
        captured = {}

        def fake_run(cmd, **kwargs):
            captured["cmd"] = cmd
            captured["kwargs"] = kwargs
            result_json = json.dumps({"ingested": 3, "deferred": 0})
            envelope = json.dumps({"result": result_json, "is_error": False})
            return _make_proc(returncode=0, stdout=envelope)

        with patch("rank_links.load_env"):
            result = scheduled_run.run_ingest(
                max_n=7,
                timeout_s=120,
                _subprocess_run=fake_run,
            )

        cmd = captured["cmd"]
        cmd_str = " ".join(cmd)
        assert "7" in cmd_str, f"expected max bound 7 in cmd: {cmd_str}"
        assert captured["kwargs"].get("timeout") == 120, (
            f"expected timeout=120, got {captured['kwargs']}"
        )
        assert result["status"] == "ok"
        assert result["ingested"] == 3

    def test_timeout_records_failure_queues_nothing(self, tmp_path):
        """A TimeoutExpired records failure status; nothing extra is queued."""
        def fake_run(cmd, **kwargs):
            raise subprocess.TimeoutExpired(cmd, 120)

        with patch("rank_links.load_env"):
            result = scheduled_run.run_ingest(
                max_n=10,
                timeout_s=120,
                _subprocess_run=fake_run,
            )

        assert result["status"] == "timeout"
        assert result["ingested"] == 0
        # deferred shows the max bound (items left in inbox)
        assert result["deferred"] == 10

    def test_non_zero_exit_records_failure(self, tmp_path):
        """A non-zero claude exit records status=failed."""
        def fake_run(cmd, **kwargs):
            return _make_proc(returncode=1, stderr="permission denied")

        with patch("rank_links.load_env"):
            result = scheduled_run.run_ingest(
                max_n=5,
                timeout_s=60,
                _subprocess_run=fake_run,
            )

        assert result["status"] == "failed"
        assert result["ingested"] == 0

    def test_is_error_true_records_failure(self, tmp_path):
        """A claude envelope with is_error=true records status=failed."""
        def fake_run(cmd, **kwargs):
            envelope = json.dumps({"result": "something went wrong", "is_error": True})
            return _make_proc(returncode=0, stdout=envelope)

        with patch("rank_links.load_env"):
            result = scheduled_run.run_ingest(
                max_n=5,
                timeout_s=60,
                _subprocess_run=fake_run,
            )

        assert result["status"] == "failed"

    def test_claude_bin_absolute_path_used(self, tmp_path):
        """run_ingest uses the absolute CLAUDE_BIN path (or injected claude_bin)."""
        fake_bin = tmp_path / "fake_claude"
        captured = {}

        def fake_run(cmd, **kwargs):
            captured["cmd"] = cmd
            envelope = json.dumps({"result": "{}", "is_error": False})
            return _make_proc(returncode=0, stdout=envelope)

        with patch("rank_links.load_env"):
            scheduled_run.run_ingest(
                max_n=5,
                timeout_s=60,
                claude_bin=fake_bin,
                _subprocess_run=fake_run,
            )

        assert captured["cmd"][0] == str(fake_bin), (
            f"expected fake_bin as first cmd arg, got {captured['cmd'][0]!r}"
        )


# ---------------------------------------------------------------------------
# write_run_report tests
# ---------------------------------------------------------------------------

class TestWriteRunReport:
    def _make_tallies(self, gmail_collected=2, obsidian_collected=1, ingested=3, deferred=0):
        return {
            "collectors": {
                "gmail": {"status": "ok", "collected": gmail_collected},
                "obsidian": {"status": "ok", "collected": obsidian_collected},
                "youtube": {"status": "not configured", "collected": 0},
            },
            "ingest": {"status": "ok", "ingested": ingested, "deferred": deferred},
        }

    def test_appends_well_formed_block(self, tmp_path):
        """write_run_report appends a config|scheduled run block with correct counts."""
        log = tmp_path / "_log.md"
        tallies = self._make_tallies(gmail_collected=2, obsidian_collected=1, ingested=3)
        scheduled_run.write_run_report(tallies, at="2026-06-15T10:00", log_path=log)

        text = log.read_text(encoding="utf-8")
        assert "## [2026-06-15T10:00] config | scheduled run" in text
        assert "gmail" in text
        assert "2 collected" in text
        assert "obsidian" in text
        assert "1 collected" in text
        assert "ingested" in text
        assert "3 ingested" in text

    def test_second_call_appends_without_disturbing_first(self, tmp_path):
        """A second write_run_report call appends; the first block is still present."""
        log = tmp_path / "_log.md"
        tallies1 = self._make_tallies(gmail_collected=1)
        tallies2 = self._make_tallies(gmail_collected=5)

        scheduled_run.write_run_report(tallies1, at="2026-06-15T09:00", log_path=log)
        scheduled_run.write_run_report(tallies2, at="2026-06-15T10:00", log_path=log)

        text = log.read_text(encoding="utf-8")
        assert "2026-06-15T09:00" in text, "first block timestamp missing"
        assert "2026-06-15T10:00" in text, "second block timestamp missing"
        # Both blocks present; file not rewritten
        assert text.index("2026-06-15T09:00") < text.index("2026-06-15T10:00")

    def test_appends_to_existing_file(self, tmp_path):
        """write_run_report appends to a pre-existing log file without overwriting."""
        log = tmp_path / "_log.md"
        existing = "# Existing log content\n## [2026-01-01T00:00] ingest | something\n"
        log.write_text(existing, encoding="utf-8")

        tallies = self._make_tallies()
        scheduled_run.write_run_report(tallies, at="2026-06-15T10:00", log_path=log)

        text = log.read_text(encoding="utf-8")
        assert existing in text, "pre-existing content was overwritten"
        assert "scheduled run" in text

    def test_ingest_error_included_in_block(self, tmp_path):
        """When ingest fails, the error is present in the report block."""
        log = tmp_path / "_log.md"
        tallies = {
            "collectors": {"gmail": {"status": "ok", "collected": 0}},
            "ingest": {"status": "timeout", "ingested": 0, "deferred": 5, "error": "timeout"},
        }
        scheduled_run.write_run_report(tallies, at="2026-06-15T10:00", log_path=log)

        text = log.read_text(encoding="utf-8")
        assert "timeout" in text


# ---------------------------------------------------------------------------
# run() / main() integration tests (all external calls mocked)
# ---------------------------------------------------------------------------

class TestRunIntegration:
    """Test the full run() happy path and failure scenarios with all externals mocked."""

    def _mock_collectors(self):
        return {
            "gmail": {"status": "ok", "collected": 2},
            "obsidian": {"status": "ok", "collected": 1},
            "youtube": {"status": "not configured", "collected": 0},
        }

    def _mock_ingest(self):
        return {"status": "ok", "ingested": 3, "deferred": 0}

    def test_happy_path_full_sequence(self, tmp_path):
        """run acquires lock, calls collectors → ingest → report, releases lock."""
        lock = tmp_path / ".test.lock"
        log = tmp_path / "_log.md"

        collector_mock = MagicMock(return_value=self._mock_collectors())
        ingest_mock = MagicMock(return_value=self._mock_ingest())

        with (
            patch.object(scheduled_run, "run_collectors", collector_mock),
            patch.object(scheduled_run, "run_ingest", ingest_mock),
            patch.object(scheduled_run, "LOG_PATH", log),
        ):
            rc = scheduled_run.main(["--lock-path", str(lock), "run", "--max", "10", "--timeout", "30"])

        assert rc == 0
        collector_mock.assert_called_once()
        ingest_mock.assert_called_once()
        assert not lock.exists(), "lock should be released after run"
        log_text = log.read_text(encoding="utf-8")
        assert "scheduled run" in log_text

    def test_lock_released_even_when_step_raises(self, tmp_path):
        """Lock is released in finally even if a step raises an exception."""
        lock = tmp_path / ".test.lock"

        def boom():
            raise RuntimeError("collector exploded")

        with (
            patch.object(scheduled_run, "run_collectors", side_effect=RuntimeError("collector exploded")),
            patch.object(scheduled_run, "run_ingest", return_value=self._mock_ingest()),
            patch.object(scheduled_run, "write_run_report"),
        ):
            with pytest.raises(RuntimeError, match="collector exploded"):
                scheduled_run.main(["--lock-path", str(lock), "run"])

        assert not lock.exists(), "lock file should be gone even after exception"

    def test_exits_skipped_when_lock_already_held(self, tmp_path):
        """run() exits with skipped status when the lock is already held."""
        lock = tmp_path / ".held.lock"
        lock.write_text("pid=99999\n", encoding="utf-8")

        collector_mock = MagicMock()

        with patch.object(scheduled_run, "run_collectors", collector_mock):
            rc = scheduled_run.main(["--lock-path", str(lock), "run"])

        assert rc == 0
        collector_mock.assert_not_called()

    def test_dry_run_skips_collectors_and_ingest(self, tmp_path):
        """--dry-run skips real collectors and ingest calls."""
        lock = tmp_path / ".dry.lock"
        log = tmp_path / "_log.md"

        collector_mock = MagicMock(return_value=self._mock_collectors())
        ingest_mock = MagicMock(return_value=self._mock_ingest())

        with (
            patch.object(scheduled_run, "run_collectors", collector_mock),
            patch.object(scheduled_run, "run_ingest", ingest_mock),
            patch.object(scheduled_run, "LOG_PATH", log),
        ):
            rc = scheduled_run.main(["--lock-path", str(lock), "run", "--dry-run"])

        assert rc == 0
        collector_mock.assert_not_called()
        ingest_mock.assert_not_called()
        assert not lock.exists()

    def test_run_max_and_timeout_forwarded_to_ingest(self, tmp_path):
        """--max and --timeout CLI args are forwarded to run_ingest."""
        lock = tmp_path / ".test.lock"
        log = tmp_path / "_log.md"

        ingest_mock = MagicMock(return_value=self._mock_ingest())

        with (
            patch.object(scheduled_run, "run_collectors", return_value=self._mock_collectors()),
            patch.object(scheduled_run, "run_ingest", ingest_mock),
            patch.object(scheduled_run, "LOG_PATH", log),
        ):
            scheduled_run.main(["--lock-path", str(lock), "run", "--max", "15", "--timeout", "45"])

        call_kwargs = ingest_mock.call_args
        assert call_kwargs.kwargs.get("max_n") == 15 or (
            call_kwargs.args and call_kwargs.args[0] == 15
        ), f"max_n=15 not forwarded: {call_kwargs}"
        assert call_kwargs.kwargs.get("timeout_s") == 45 or (
            call_kwargs.args and call_kwargs.args[1] == 45
        ), f"timeout_s=45 not forwarded: {call_kwargs}"

    def test_run_output_json_contains_summary(self, tmp_path, capsys):
        """The run subcommand prints a JSON summary to stdout."""
        lock = tmp_path / ".test.lock"
        log = tmp_path / "_log.md"

        with (
            patch.object(scheduled_run, "run_collectors", return_value=self._mock_collectors()),
            patch.object(scheduled_run, "run_ingest", return_value=self._mock_ingest()),
            patch.object(scheduled_run, "LOG_PATH", log),
        ):
            scheduled_run.main(["--lock-path", str(lock), "run"])

        captured = capsys.readouterr()
        parsed = json.loads(captured.out)
        assert parsed["status"] == "ok"
        assert "collectors" in parsed
        assert "ingest" in parsed

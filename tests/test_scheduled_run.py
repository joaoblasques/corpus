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
            # obsidian succeeds — emits notes+urls keys (not "written")
            return _make_proc(returncode=0, stdout=json.dumps({"notes": 2, "urls": 1}))

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
            script = cmd[1] if len(cmd) > 1 else ""
            if "youtube_client.py" in script:
                # youtube emits {"collected": N, ...}
                return _make_proc(returncode=0, stdout=json.dumps({"collected": 5}))
            # other clients (gmail, obsidian) — return benign output
            return _make_proc(returncode=0, stdout=json.dumps({"notes": 0, "urls": 0, "written": 0}))

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

    # --- Graceful-degradation contract tests (I1 fix + M3) ---

    def test_result_null_does_not_raise(self, tmp_path):
        """I1: envelope with result=null (JSON null → Python None) must not raise AttributeError.

        Expected: status=ok, ingested=0, deferred=0 (graceful degradation).
        """
        def fake_run(cmd, **kwargs):
            # json.dumps renders None as JSON null
            envelope = json.dumps({"result": None, "is_error": False})
            return _make_proc(returncode=0, stdout=envelope)

        with patch("rank_links.load_env"):
            result = scheduled_run.run_ingest(
                max_n=5,
                timeout_s=60,
                _subprocess_run=fake_run,
            )

        assert result["status"] == "ok", f"expected status=ok, got {result}"
        assert result["ingested"] == 0, f"expected ingested=0, got {result}"
        assert result["deferred"] == 0, f"expected deferred=0, got {result}"

    def test_result_plain_text_degrades_gracefully(self, tmp_path):
        """M3: envelope whose result is plain non-JSON text does not raise and yields ok + zero counts."""
        def fake_run(cmd, **kwargs):
            envelope = json.dumps({"result": "Done. 3 pages.", "is_error": False})
            return _make_proc(returncode=0, stdout=envelope)

        with patch("rank_links.load_env"):
            result = scheduled_run.run_ingest(
                max_n=5,
                timeout_s=60,
                _subprocess_run=fake_run,
            )

        assert result["status"] == "ok", f"expected status=ok for plain-text result, got {result}"
        assert result["ingested"] == 0
        assert result["deferred"] == 0

    def test_empty_stdout_records_failed(self, tmp_path):
        """M3: returncode 0 but empty (non-JSON) stdout → status=failed (outer JSONDecodeError path)."""
        def fake_run(cmd, **kwargs):
            return _make_proc(returncode=0, stdout="")

        with patch("rank_links.load_env"):
            result = scheduled_run.run_ingest(
                max_n=5,
                timeout_s=60,
                _subprocess_run=fake_run,
            )

        assert result["status"] == "failed", f"expected status=failed for empty stdout, got {result}"
        assert result["ingested"] == 0
        assert result["deferred"] == 0


class TestParseIngestCounts:
    """_parse_ingest_counts extracts (ingested, deferred) from the skill result text."""

    def test_pure_json_result(self):
        text = '{"ingested": 2, "deferred": 1, "pages_created": 0, "pages_updated": 2}'
        assert scheduled_run._parse_ingest_counts(text) == (2, 1)

    def test_prose_then_trailing_json(self):
        text = 'Ingested 2 sources, deferred 1.\n{"ingested": 2, "deferred": 1}'
        assert scheduled_run._parse_ingest_counts(text) == (2, 1)

    def test_prose_only_returns_zero(self):
        text = "ingest-auto complete: 2 ingested, 1 deferred"  # no JSON object
        assert scheduled_run._parse_ingest_counts(text) == (0, 0)

    def test_dict_input(self):
        assert scheduled_run._parse_ingest_counts({"ingested": 5, "deferred": 3}) == (5, 3)

    def test_empty_or_non_string(self):
        assert scheduled_run._parse_ingest_counts("") == (0, 0)
        assert scheduled_run._parse_ingest_counts(None) == (0, 0)


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
            patch.object(scheduled_run, "commit_and_push", return_value={"status": "nothing-to-commit"}),
            patch.object(scheduled_run, "LOG_PATH", log),
        ):
            scheduled_run.main(["--lock-path", str(lock), "run"])

        captured = capsys.readouterr()
        parsed = json.loads(captured.out)
        assert parsed["status"] == "ok"
        assert "collectors" in parsed
        assert "ingest" in parsed


# ---------------------------------------------------------------------------
# commit_and_push tests  (U5)
# ---------------------------------------------------------------------------

class TestCommitAndPush:
    """Tests for commit_and_push — git is fully mocked (no live git/network)."""

    AT = "2026-06-15T10:30"

    def _make_tallies(self, gmail=2, obsidian=1, ingested=3):
        return {
            "collectors": {
                "gmail": {"status": "ok", "collected": gmail},
                "obsidian": {"status": "ok", "collected": obsidian},
            },
            "ingest": {"status": "ok", "ingested": ingested, "deferred": 0},
        }

    def _make_proc(self, returncode=0, stdout="", stderr=""):
        p = MagicMock()
        p.returncode = returncode
        p.stdout = stdout
        p.stderr = stderr
        return p

    # ------------------------------------------------------------------
    # Scenario 1: corpus/ has changes → add → commit → push → committed
    # ------------------------------------------------------------------

    def test_changed_corpus_triggers_add_commit_push(self, tmp_path):
        """When corpus/ has changes, git add corpus/ → commit → push are called."""
        calls = []

        def fake_run(cmd, **kwargs):
            calls.append(list(cmd))
            subcmd = cmd[1] if len(cmd) > 1 else ""
            if subcmd == "status":
                return self._make_proc(stdout=" M corpus/_log.md\n")
            if subcmd == "add":
                return self._make_proc()
            if subcmd == "commit":
                return self._make_proc(stdout="[feat/scheduled-automation abc1234] chore(auto-ingest): ...\n")
            if subcmd == "push":
                return self._make_proc()
            return self._make_proc()

        result = scheduled_run.commit_and_push(
            at=self.AT,
            tallies=self._make_tallies(),
            _subprocess_run=fake_run,
        )

        assert result["status"] == "committed", f"expected committed, got {result}"
        # Verify the sequence: status → add → commit → push
        subcommands = [c[1] for c in calls if len(c) > 1]
        assert subcommands == ["status", "add", "commit", "push"], (
            f"expected [status, add, commit, push], got {subcommands}"
        )
        # Push must be explicit (origin HEAD) so it works without upstream tracking.
        push_cmd = next(c for c in calls if len(c) > 1 and c[1] == "push")
        assert push_cmd[2:] == ["origin", "HEAD"], (
            f"expected `git push origin HEAD`, got {push_cmd}"
        )

    def test_commit_message_contains_timestamp_and_counts(self, tmp_path):
        """Commit message contains the AT timestamp and per-channel counts."""
        commit_msgs = []

        def fake_run(cmd, **kwargs):
            subcmd = cmd[1] if len(cmd) > 1 else ""
            if subcmd == "status":
                return self._make_proc(stdout=" M corpus/_log.md\n")
            if subcmd == "add":
                return self._make_proc()
            if subcmd == "commit":
                # -m <message> is at index 3
                commit_msgs.append(cmd[3] if len(cmd) > 3 else "")
                return self._make_proc(stdout="[main abc5678] ...\n")
            if subcmd == "push":
                return self._make_proc()
            return self._make_proc()

        scheduled_run.commit_and_push(
            at=self.AT,
            tallies=self._make_tallies(gmail=2, obsidian=1, ingested=3),
            _subprocess_run=fake_run,
        )

        assert commit_msgs, "no commit message captured"
        msg = commit_msgs[0]
        assert self.AT in msg, f"timestamp {self.AT!r} not in commit message: {msg!r}"
        assert "gmail=2" in msg, f"gmail count not in commit message: {msg!r}"
        assert "ingested=3" in msg, f"ingested count not in commit message: {msg!r}"

    # ------------------------------------------------------------------
    # Scenario 2: corpus/ unchanged → no-op
    # ------------------------------------------------------------------

    def test_unchanged_corpus_returns_nothing_to_commit(self, tmp_path):
        """When corpus/ has no changes, returns nothing-to-commit without add/commit/push."""
        calls = []

        def fake_run(cmd, **kwargs):
            calls.append(list(cmd))
            subcmd = cmd[1] if len(cmd) > 1 else ""
            if subcmd == "status":
                return self._make_proc(stdout="")  # empty = no changes
            return self._make_proc()

        result = scheduled_run.commit_and_push(
            at=self.AT,
            tallies=self._make_tallies(),
            _subprocess_run=fake_run,
        )

        assert result["status"] == "nothing-to-commit", f"expected nothing-to-commit, got {result}"
        # Only status was called; add/commit/push were not
        subcommands = [c[1] for c in calls if len(c) > 1]
        assert "add" not in subcommands, f"git add should not be called when nothing changed: {subcommands}"
        assert "commit" not in subcommands
        assert "push" not in subcommands

    # ------------------------------------------------------------------
    # Scenario 3: R10 — add is SCOPED to corpus/ only
    # ------------------------------------------------------------------

    def test_add_is_scoped_to_corpus_not_raw_or_dot(self, tmp_path):
        """git add args contain 'corpus/' and do NOT contain 'raw/' or '.'  (R10 guarantee)."""
        add_args_captured = []

        def fake_run(cmd, **kwargs):
            subcmd = cmd[1] if len(cmd) > 1 else ""
            if subcmd == "status":
                return self._make_proc(stdout=" M corpus/_log.md\n")
            if subcmd == "add":
                add_args_captured.extend(cmd[2:])  # everything after 'git add'
                return self._make_proc()
            if subcmd == "commit":
                return self._make_proc(stdout="[main abc1234] ...\n")
            if subcmd == "push":
                return self._make_proc()
            return self._make_proc()

        scheduled_run.commit_and_push(
            at=self.AT,
            tallies=self._make_tallies(),
            _subprocess_run=fake_run,
        )

        assert add_args_captured, "git add was never called (R10 test prerequisite failed)"
        assert "corpus/" in add_args_captured, (
            f"'corpus/' not in git add args: {add_args_captured}"
        )
        assert "raw/" not in add_args_captured, (
            f"'raw/' must NOT be in git add args: {add_args_captured}  (R10 violation)"
        )
        assert "." not in add_args_captured, (
            f"'.' must NOT be in git add args: {add_args_captured}  (R10 violation)"
        )

    # ------------------------------------------------------------------
    # Scenario 4: push failure is recorded, does not propagate
    # ------------------------------------------------------------------

    def test_push_failure_recorded_in_result_not_raised(self, tmp_path):
        """A non-zero push exit is recorded as push-failed in the result dict."""

        def fake_run(cmd, **kwargs):
            subcmd = cmd[1] if len(cmd) > 1 else ""
            if subcmd == "status":
                return self._make_proc(stdout=" M corpus/_log.md\n")
            if subcmd == "add":
                return self._make_proc()
            if subcmd == "commit":
                return self._make_proc(stdout="[main abc1234] ...\n")
            if subcmd == "push":
                return self._make_proc(returncode=1, stderr="error: failed to push some refs")
            return self._make_proc()

        result = scheduled_run.commit_and_push(
            at=self.AT,
            tallies=self._make_tallies(),
            _subprocess_run=fake_run,
        )

        assert result["status"] == "push-failed", f"expected push-failed, got {result}"
        assert "push_error" in result, f"push_error missing from result: {result}"

    def test_push_exception_recorded_in_result_not_raised(self, tmp_path):
        """A push call that raises is caught and recorded, not propagated."""

        def fake_run(cmd, **kwargs):
            subcmd = cmd[1] if len(cmd) > 1 else ""
            if subcmd == "status":
                return self._make_proc(stdout=" M corpus/_log.md\n")
            if subcmd == "add":
                return self._make_proc()
            if subcmd == "commit":
                return self._make_proc(stdout="[main abc1234] ...\n")
            if subcmd == "push":
                raise OSError("network unreachable")
            return self._make_proc()

        result = scheduled_run.commit_and_push(
            at=self.AT,
            tallies=self._make_tallies(),
            _subprocess_run=fake_run,
        )

        assert result["status"] == "push-failed", f"expected push-failed, got {result}"
        assert "network unreachable" in result.get("push_error", ""), (
            f"error message not captured: {result}"
        )

    # ------------------------------------------------------------------
    # Scenario 5: --dry-run skips commit_and_push entirely
    # ------------------------------------------------------------------

    def test_dry_run_skips_commit_and_push(self, tmp_path, capsys):
        """--dry-run does not call commit_and_push (consistent with U3 dry-run pattern)."""
        lock = tmp_path / ".dry.lock"
        log = tmp_path / "_log.md"

        commit_mock = MagicMock(return_value={"status": "committed"})

        with (
            patch.object(scheduled_run, "run_collectors"),
            patch.object(scheduled_run, "run_ingest"),
            patch.object(scheduled_run, "commit_and_push", commit_mock),
            patch.object(scheduled_run, "LOG_PATH", log),
        ):
            scheduled_run.main(["--lock-path", str(lock), "run", "--dry-run"])

        commit_mock.assert_not_called()


# ---------------------------------------------------------------------------
# commit_and_push containment in run() — integration
# ---------------------------------------------------------------------------

class TestCommitAndPushRunIntegration:
    """Integration tests verifying commit_and_push wiring inside run()."""

    def _mock_collectors(self):
        return {
            "gmail": {"status": "ok", "collected": 2},
            "obsidian": {"status": "ok", "collected": 1},
            "youtube": {"status": "not configured", "collected": 0},
        }

    def _mock_ingest(self):
        return {"status": "ok", "ingested": 3, "deferred": 0}

    def test_run_happy_path_invokes_commit_and_push(self, tmp_path):
        """run() calls commit_and_push between ingest and write_run_report."""
        lock = tmp_path / ".test.lock"
        log = tmp_path / "_log.md"

        commit_mock = MagicMock(return_value={"status": "committed", "sha": "abc1234"})

        call_order = []

        def collector_side_effect():
            call_order.append("collectors")
            return self._mock_collectors()

        def ingest_side_effect(**kwargs):
            call_order.append("ingest")
            return self._mock_ingest()

        def commit_side_effect(**kwargs):
            call_order.append("commit")
            return {"status": "committed", "sha": "abc1234"}

        def report_side_effect(tallies, at, **kwargs):
            call_order.append("report")

        with (
            patch.object(scheduled_run, "run_collectors", side_effect=collector_side_effect),
            patch.object(scheduled_run, "run_ingest", side_effect=ingest_side_effect),
            patch.object(scheduled_run, "commit_and_push", side_effect=commit_side_effect),
            patch.object(scheduled_run, "write_run_report", side_effect=report_side_effect),
            patch.object(scheduled_run, "LOG_PATH", log),
        ):
            rc = scheduled_run.main(["--lock-path", str(lock), "run"])

        assert rc == 0
        assert call_order == ["collectors", "ingest", "commit", "report"], (
            f"unexpected call order: {call_order}"
        )
        assert not lock.exists(), "lock should be released"

    def test_push_failure_does_not_propagate_out_of_run(self, tmp_path):
        """A push failure inside commit_and_push does not propagate — run still completes."""
        lock = tmp_path / ".test.lock"
        log = tmp_path / "_log.md"

        def commit_raises(**kwargs):
            raise RuntimeError("unexpected internal error in commit_and_push")

        with (
            patch.object(scheduled_run, "run_collectors", return_value=self._mock_collectors()),
            patch.object(scheduled_run, "run_ingest", return_value=self._mock_ingest()),
            patch.object(scheduled_run, "commit_and_push", side_effect=commit_raises),
            patch.object(scheduled_run, "LOG_PATH", log),
        ):
            rc = scheduled_run.main(["--lock-path", str(lock), "run"])

        # run must complete normally (rc=0), report written, lock released
        assert rc == 0, f"expected rc=0 even after commit_and_push raises, got {rc}"
        assert not lock.exists(), "lock should be released even after commit_and_push failure"
        # Report should still have been written
        assert log.exists(), "log should still be written even after commit_and_push raises"

    def test_commit_result_folded_into_tallies_for_report(self, tmp_path):
        """commit result is stored in tallies['commit'] so write_run_report can include it."""
        lock = tmp_path / ".test.lock"
        log = tmp_path / "_log.md"

        tallies_seen = {}

        def report_side_effect(tallies, at, **kwargs):
            tallies_seen.update(tallies)

        with (
            patch.object(scheduled_run, "run_collectors", return_value=self._mock_collectors()),
            patch.object(scheduled_run, "run_ingest", return_value=self._mock_ingest()),
            patch.object(scheduled_run, "commit_and_push", return_value={"status": "committed", "sha": "deadbeef"}),
            patch.object(scheduled_run, "write_run_report", side_effect=report_side_effect),
        ):
            scheduled_run.main(["--lock-path", str(lock), "run"])

        assert "commit" in tallies_seen, f"'commit' key missing from tallies passed to report: {tallies_seen}"
        assert tallies_seen["commit"].get("status") == "committed"
        assert tallies_seen["commit"].get("sha") == "deadbeef"


# ---------------------------------------------------------------------------
# I1 — move_processed_inbox tests
# ---------------------------------------------------------------------------

class TestMoveProcessedInbox:
    """Tests for scheduled_run.move_processed_inbox."""

    def _write_stamped(self, path: Path, channel: str) -> None:
        """Write a minimal inbox markdown file with corpus_ingested stamp."""
        path.write_text(
            f"---\nchannel: {channel}\ncorpus_ingested: true\ncorpus_ingested_at: 2026-06-15\n---\n\nBody.\n",
            encoding="utf-8",
        )

    def _write_unstamped(self, path: Path, channel: str = "web") -> None:
        """Write an inbox file WITHOUT the corpus_ingested stamp."""
        path.write_text(
            f"---\nchannel: {channel}\n---\n\nNot yet ingested.\n",
            encoding="utf-8",
        )

    def test_stamped_youtube_moved_to_raw_youtube(self, tmp_path):
        """A stamped channel=youtube file is moved to raw/youtube/."""
        inbox = tmp_path / "_inbox"
        inbox.mkdir()
        raw = tmp_path / "raw"
        src = inbox / "yt-video.md"
        self._write_stamped(src, "youtube")

        result = scheduled_run.move_processed_inbox(inbox_dir=inbox, raw_dir=raw)

        assert not src.exists(), "source should be gone after move"
        dest = raw / "youtube" / "yt-video.md"
        assert dest.exists(), f"dest not found at {dest}"
        assert result["moved"] == 1
        assert result["by_channel"].get("youtube") == 1
        assert result["skipped"] == 0

    def test_stamped_email_moved_to_raw_email(self, tmp_path):
        """A stamped channel=email file is moved to raw/email/."""
        inbox = tmp_path / "_inbox"
        inbox.mkdir()
        raw = tmp_path / "raw"
        src = inbox / "gmail-msg.md"
        self._write_stamped(src, "email")

        result = scheduled_run.move_processed_inbox(inbox_dir=inbox, raw_dir=raw)

        assert not src.exists()
        assert (raw / "email" / "gmail-msg.md").exists()
        assert result["moved"] == 1
        assert result["by_channel"].get("email") == 1

    def test_unstamped_file_left_in_place(self, tmp_path):
        """An unstamped file (no corpus_ingested: true) is skipped — stays in inbox."""
        inbox = tmp_path / "_inbox"
        inbox.mkdir()
        raw = tmp_path / "raw"
        src = inbox / "pending.md"
        self._write_unstamped(src, "web")

        result = scheduled_run.move_processed_inbox(inbox_dir=inbox, raw_dir=raw)

        assert src.exists(), "unstamped file should remain in inbox"
        assert result["moved"] == 0
        assert result["skipped"] == 1

    def test_stamped_unknown_channel_left_in_place(self, tmp_path):
        """A stamped file with an unrecognised/missing channel is skipped."""
        inbox = tmp_path / "_inbox"
        inbox.mkdir()
        raw = tmp_path / "raw"
        src = inbox / "oddball.md"
        src.write_text(
            "---\ncorpus_ingested: true\ncorpus_ingested_at: 2026-06-15\n---\n\nNo channel field.\n",
            encoding="utf-8",
        )

        result = scheduled_run.move_processed_inbox(inbox_dir=inbox, raw_dir=raw)

        assert src.exists(), "unknown-channel file should remain in inbox"
        assert result["moved"] == 0
        assert result["skipped"] == 1

    def test_mixed_batch_correct_tally(self, tmp_path):
        """Mixed batch: two stamped (youtube, email) + one unstamped + one unknown channel."""
        inbox = tmp_path / "_inbox"
        inbox.mkdir()
        raw = tmp_path / "raw"

        a = inbox / "a.md"
        self._write_stamped(a, "youtube")
        b = inbox / "b.md"
        self._write_stamped(b, "email")
        c = inbox / "c.md"
        self._write_unstamped(c)
        d = inbox / "d.md"
        d.write_text(
            "---\ncorpus_ingested: true\nchannel: galactic\n---\n\nBody.\n",
            encoding="utf-8",
        )

        result = scheduled_run.move_processed_inbox(inbox_dir=inbox, raw_dir=raw)

        assert not a.exists()
        assert not b.exists()
        assert c.exists()
        assert d.exists()
        assert result["moved"] == 2
        assert result["by_channel"] == {"youtube": 1, "email": 1}
        assert result["skipped"] == 2

    def test_destination_dir_created_if_missing(self, tmp_path):
        """Destination raw/<channel>/ directory is created if it does not exist."""
        inbox = tmp_path / "_inbox"
        inbox.mkdir()
        raw = tmp_path / "raw"
        # raw/web/ does NOT pre-exist
        assert not (raw / "web").exists()

        src = inbox / "clip.md"
        self._write_stamped(src, "web")

        scheduled_run.move_processed_inbox(inbox_dir=inbox, raw_dir=raw)

        assert (raw / "web" / "clip.md").exists()

    def test_injectable_mover_called_with_src_and_dest(self, tmp_path):
        """The _mover seam is called with (src_path, dest_path) for each file to move."""
        inbox = tmp_path / "_inbox"
        inbox.mkdir()
        raw = tmp_path / "raw"
        src = inbox / "note.md"
        self._write_stamped(src, "notes")

        moves = []

        def fake_mover(s, d):
            moves.append((s, d))

        scheduled_run.move_processed_inbox(inbox_dir=inbox, raw_dir=raw, _mover=fake_mover)

        assert len(moves) == 1
        assert moves[0][0] == src
        assert moves[0][1] == raw / "notes" / "note.md"

    def test_move_processed_inbox_failure_does_not_propagate_out_of_run(self, tmp_path):
        """If move_processed_inbox raises, run() still completes and releases lock."""
        lock = tmp_path / ".test.lock"
        log = tmp_path / "_log.md"

        def boom(**kwargs):
            raise RuntimeError("disk full")

        with (
            patch.object(scheduled_run, "run_collectors", return_value={
                "gmail": {"status": "ok", "collected": 1},
            }),
            patch.object(scheduled_run, "run_ingest", return_value={
                "status": "ok", "ingested": 1, "deferred": 0,
            }),
            patch.object(scheduled_run, "commit_and_push", return_value={"status": "nothing-to-commit"}),
            patch.object(scheduled_run, "move_processed_inbox", side_effect=RuntimeError("disk full")),
            patch.object(scheduled_run, "LOG_PATH", log),
        ):
            rc = scheduled_run.main(["--lock-path", str(lock), "run"])

        assert rc == 0, f"expected rc=0 even when move_processed_inbox raises, got {rc}"
        assert not lock.exists(), "lock must be released even after move failure"


# ---------------------------------------------------------------------------
# I2 — correct collector keys in run_collectors
# ---------------------------------------------------------------------------

class TestRunCollectorsCorrectKeys:
    """Verify run_collectors extracts the right JSON keys per channel."""

    def test_obsidian_collected_is_notes_plus_urls(self, tmp_path):
        """obsidian collected = notes + urls (not 'written')."""
        no_token = tmp_path / "no_token.json"

        def fake_run(cmd, **kwargs):
            script = cmd[1] if len(cmd) > 1 else ""
            if "obsidian_client.py" in script:
                return _make_proc(returncode=0, stdout=json.dumps(
                    {"notes": 3, "urls": 2, "url_failed": 0, "skipped": 1,
                     "dry_run": False, "discovered": 6}
                ))
            return _make_proc(returncode=0, stdout=json.dumps({"written": 0}))

        result = scheduled_run.run_collectors(
            youtube_token_path=no_token,
            _subprocess_run=fake_run,
        )

        assert result["obsidian"]["status"] == "ok"
        assert result["obsidian"]["collected"] == 5, (
            f"expected notes(3)+urls(2)=5, got {result['obsidian']['collected']}"
        )

    def test_youtube_collected_uses_collected_key(self, tmp_path):
        """youtube collected = data['collected'] (not 'written')."""
        token = tmp_path / "youtube_token.json"
        token.write_text("{}", encoding="utf-8")

        def fake_run(cmd, **kwargs):
            script = cmd[1] if len(cmd) > 1 else ""
            if "youtube_client.py" in script:
                return _make_proc(returncode=0, stdout=json.dumps(
                    {"playlists": 1, "collected": 7, "duplicate": 2, "no_transcript": 0,
                     "removed": 5, "kept": 2, "failed": 0, "dry_run": False,
                     "ignored_playlists": []}
                ))
            return _make_proc(returncode=0, stdout=json.dumps({"written": 0}))

        result = scheduled_run.run_collectors(
            youtube_token_path=token,
            _subprocess_run=fake_run,
        )

        assert result["youtube"]["status"] == "ok"
        assert result["youtube"]["collected"] == 7, (
            f"expected collected=7, got {result['youtube']['collected']}"
        )

    def test_gmail_collected_uses_written_key(self, tmp_path):
        """gmail collected = data['written'] (unchanged)."""
        no_token = tmp_path / "no_token.json"

        def fake_run(cmd, **kwargs):
            script = cmd[1] if len(cmd) > 1 else ""
            if "gmail_client.py" in script:
                return _make_proc(returncode=0, stdout=json.dumps({"written": 4}))
            return _make_proc(returncode=0, stdout=json.dumps({"notes": 0, "urls": 0}))

        result = scheduled_run.run_collectors(
            youtube_token_path=no_token,
            _subprocess_run=fake_run,
        )

        assert result["gmail"]["status"] == "ok"
        assert result["gmail"]["collected"] == 4, (
            f"expected written=4, got {result['gmail']['collected']}"
        )

#!/usr/bin/env python3
"""Tests for bin/pending_review.py — pure-function unit tests + file-path integration."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import pending_review  # noqa: E402


# ---------------------------------------------------------------------------
# count_deferred
# ---------------------------------------------------------------------------

class TestCountDeferred:
    def test_counts_defer_lines_among_mixed_content(self):
        text = (
            "# Pending Review\n"
            "\n"
            "- DEFER G1: source-a.md — duplicate content\n"
            "- DEFER G2: source-b.md — paywalled, no body extracted\n"
            "- some other line\n"
            "- DEFER UNCERTAIN: source-c.md — unclear routing\n"
        )
        assert pending_review.count_deferred(text) == 3

    def test_returns_zero_for_empty_string(self):
        assert pending_review.count_deferred("") == 0

    def test_returns_zero_when_no_defer_lines(self):
        text = "# Review file\n\nNothing deferred today.\n"
        assert pending_review.count_deferred(text) == 0

    def test_does_not_count_partial_match(self):
        # "- DEFER" without trailing space should not match
        text = "- DEFERRED: source.md — note\n"
        assert pending_review.count_deferred(text) == 0

    def test_counts_all_trigger_types(self):
        text = (
            "- DEFER G1: a.md — reason\n"
            "- DEFER G2: b.md — reason\n"
            "- DEFER G3: c.md — reason\n"
            "- DEFER G4: d.md — reason\n"
            "- DEFER UNCERTAIN: e.md — reason\n"
        )
        assert pending_review.count_deferred(text) == 5


# ---------------------------------------------------------------------------
# latest_run_summary
# ---------------------------------------------------------------------------

_MULTI_BLOCK_LOG = """\
# Corpus Log

## [2026-06-14 07:00] config | scheduled run
- collectors:
  - gmail: 5 collected · status=ok
  - obsidian: 2 collected · status=ok
- ingest:
  - ingest: 3 ingested · 1 deferred · status=ok

## [2026-06-15 08:30] config | scheduled run
- collectors:
  - gmail: 3 collected · status=ok
  - obsidian: 1 collected · status=ok
- ingest:
  - ingest: 2 ingested · 0 deferred · status=ok
"""

_SINGLE_BLOCK_LOG = """\
## [2026-06-15 09:00] config | scheduled run
- collectors:
  - gmail: 7 collected · status=ok
- ingest:
  - ingest: 5 ingested · 2 deferred · status=ok
"""


class TestLatestRunSummary:
    def test_returns_none_for_empty_log(self):
        assert pending_review.latest_run_summary("") is None

    def test_returns_none_when_no_scheduled_run_block(self):
        text = "## [2026-06-15] ingest | Some source\n- notes: nothing\n"
        assert pending_review.latest_run_summary(text) is None

    def test_extracts_single_block(self):
        result = pending_review.latest_run_summary(_SINGLE_BLOCK_LOG)
        assert result is not None
        assert result["date"] == "2026-06-15"
        assert result["collected"] == 7
        assert result["ingested"] == 5

    def test_extracts_most_recent_block_when_multiple(self):
        result = pending_review.latest_run_summary(_MULTI_BLOCK_LOG)
        assert result is not None
        assert result["date"] == "2026-06-15"
        # Second block: 3 + 1 = 4 collected
        assert result["collected"] == 4
        assert result["ingested"] == 2

    def test_sums_multiple_channel_collected_counts(self):
        log = (
            "## [2026-06-15 10:00] config | scheduled run\n"
            "- collectors:\n"
            "  - gmail: 5 collected · status=ok\n"
            "  - obsidian: 3 collected · status=ok\n"
            "  - youtube: 2 collected · status=ok\n"
            "- ingest:\n"
            "  - ingest: 8 ingested · 0 deferred · status=ok\n"
        )
        result = pending_review.latest_run_summary(log)
        assert result is not None
        assert result["collected"] == 10
        assert result["ingested"] == 8

    def test_returns_none_on_malformed_text(self):
        # garbage / binary-ish content — should not raise
        result = pending_review.latest_run_summary("\x00\xff binary junk \x00")
        assert result is None

    def test_handles_block_with_zero_counts(self):
        log = (
            "## [2026-06-15 12:00] config | scheduled run\n"
            "- collectors:\n"
            "  - gmail: 0 collected · status=ok\n"
            "- ingest:\n"
            "  - ingest: 0 ingested · 0 deferred · status=ok\n"
        )
        result = pending_review.latest_run_summary(log)
        assert result is not None
        assert result["collected"] == 0
        assert result["ingested"] == 0


# ---------------------------------------------------------------------------
# build_line
# ---------------------------------------------------------------------------

class TestBuildLine:
    def test_returns_empty_string_when_no_summary_and_no_deferred(self):
        assert pending_review.build_line(None, 0) == ""

    def test_includes_awaiting_when_deferred_nonzero(self):
        summary = {"date": "2026-06-15", "collected": 4, "ingested": 2}
        line = pending_review.build_line(summary, 3)
        assert "3 awaiting your decision" in line
        assert "_REVIEW.md" in line

    def test_omits_awaiting_when_deferred_zero(self):
        summary = {"date": "2026-06-15", "collected": 4, "ingested": 2}
        line = pending_review.build_line(summary, 0)
        assert "awaiting" not in line

    def test_line_format_with_summary_and_deferred(self):
        summary = {"date": "2026-06-15", "collected": 7, "ingested": 5}
        line = pending_review.build_line(summary, 2)
        assert line == (
            "Corpus: last auto-run 2026-06-15"
            " — 7 collected · 5 ingested"
            " · 2 awaiting your decision (see raw/_inbox/_REVIEW.md)"
        )

    def test_line_format_with_summary_no_deferred(self):
        summary = {"date": "2026-06-14", "collected": 3, "ingested": 1}
        line = pending_review.build_line(summary, 0)
        assert line == "Corpus: last auto-run 2026-06-14 — 3 collected · 1 ingested"

    def test_no_summary_but_deferred_shows_fallback(self):
        line = pending_review.build_line(None, 5)
        assert "no scheduled run recorded yet" in line
        assert "5 awaiting your decision" in line


# ---------------------------------------------------------------------------
# main() integration — uses tmp_path for real file I/O
# ---------------------------------------------------------------------------

class TestMain:
    def test_clean_state_prints_nothing(self, tmp_path, capsys):
        # No _REVIEW.md, no _log.md
        ret = pending_review.main(
            review_path=tmp_path / "nonexistent_REVIEW.md",
            log_path=tmp_path / "nonexistent_log.md",
        )
        assert ret == 0
        captured = capsys.readouterr()
        assert captured.out.strip() == ""

    def test_prints_line_when_deferred_and_run_exist(self, tmp_path, capsys):
        review = tmp_path / "_REVIEW.md"
        review.write_text(
            "- DEFER G1: source-a.md — paywalled\n"
            "- DEFER G2: source-b.md — duplicate\n"
            "- DEFER UNCERTAIN: source-c.md — unclear\n",
            encoding="utf-8",
        )
        log = tmp_path / "_log.md"
        log.write_text(
            "## [2026-06-15 08:00] config | scheduled run\n"
            "- collectors:\n"
            "  - gmail: 4 collected · status=ok\n"
            "- ingest:\n"
            "  - ingest: 3 ingested · 3 deferred · status=ok\n",
            encoding="utf-8",
        )
        ret = pending_review.main(review_path=review, log_path=log)
        assert ret == 0
        captured = capsys.readouterr()
        line = captured.out.strip()
        assert "3 awaiting your decision" in line
        assert "2026-06-15" in line
        assert "4 collected" in line
        assert "3 ingested" in line

    def test_empty_review_file_is_clean(self, tmp_path, capsys):
        review = tmp_path / "_REVIEW.md"
        review.write_text("", encoding="utf-8")
        log = tmp_path / "_log.md"
        log.write_text("no scheduled run blocks here\n", encoding="utf-8")
        ret = pending_review.main(review_path=review, log_path=log)
        assert ret == 0
        captured = capsys.readouterr()
        assert captured.out.strip() == ""

    def test_malformed_review_file_degrades_gracefully(self, tmp_path, capsys):
        review = tmp_path / "_REVIEW.md"
        # Binary-ish content that can't be decoded as utf-8
        review.write_bytes(b"\xff\xfe garbage")
        log = tmp_path / "_log.md"
        log.write_text("nothing here\n", encoding="utf-8")
        ret = pending_review.main(review_path=review, log_path=log)
        assert ret == 0
        # Should not raise; output is clean-state (empty)
        captured = capsys.readouterr()
        assert captured.out.strip() == ""

    def test_missing_log_but_deferred_shows_fallback(self, tmp_path, capsys):
        review = tmp_path / "_REVIEW.md"
        review.write_text("- DEFER G3: foo.md — reason\n", encoding="utf-8")
        ret = pending_review.main(
            review_path=review,
            log_path=tmp_path / "no_log.md",
        )
        assert ret == 0
        captured = capsys.readouterr()
        line = captured.out.strip()
        assert "1 awaiting your decision" in line

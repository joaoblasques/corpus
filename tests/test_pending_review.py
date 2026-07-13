#!/usr/bin/env python3
"""Tests for bin/pending_review.py — pure-function unit tests + file-path integration."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import pending_review  # noqa: E402


# ---------------------------------------------------------------------------
# OKF conformance: path constants
# ---------------------------------------------------------------------------

def test_log_path_constant_is_log_md():
    """LOG_PATH must point to corpus/log.md (OKF conformant name, not _log.md)."""
    assert pending_review.LOG_PATH.name == "log.md", (
        f"LOG_PATH filename should be 'log.md', got {pending_review.LOG_PATH.name!r}"
    )


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
# latest_run_summary — OKF format fixtures
# ---------------------------------------------------------------------------

# Newest-first: 2026-06-15 is the first (most recent) date group
_OKF_MULTI_DATE_LOG = """\
# Corpus Log

> OKF v0.1 change log. Newest first, grouped by date.

## 2026-06-15
* **Collectors**: gmail=3, obsidian=1
* **Ingest**: 2 ingested · 0 deferred · status=ok

## 2026-06-14
* **Collectors**: gmail=5, obsidian=2
* **Ingest**: 3 ingested · 1 deferred · status=ok
"""

_OKF_SINGLE_DATE_LOG = """\
## 2026-06-15
* **Collectors**: gmail=7
* **Ingest**: 5 ingested · 2 deferred · status=ok
"""


class TestLatestRunSummary:
    def test_returns_none_for_empty_log(self):
        assert pending_review.latest_run_summary("") is None

    def test_returns_none_when_no_scheduled_run_block(self):
        # Regular ingest entries (no Collectors bullet) must return None
        text = (
            "## 2026-06-15\n"
            "* **Ingest**: ingest-auto batch — some sources\n"
        )
        assert pending_review.latest_run_summary(text) is None

    def test_extracts_single_block(self):
        result = pending_review.latest_run_summary(_OKF_SINGLE_DATE_LOG)
        assert result is not None
        assert result["date"] == "2026-06-15"
        assert result["collected"] == 7
        assert result["ingested"] == 5

    def test_extracts_most_recent_block_when_multiple(self):
        # Log is newest-first: 2026-06-15 group appears first → that is the answer
        result = pending_review.latest_run_summary(_OKF_MULTI_DATE_LOG)
        assert result is not None
        assert result["date"] == "2026-06-15"
        # First (newest) block: gmail=3, obsidian=1 → total 4
        assert result["collected"] == 4
        assert result["ingested"] == 2

    def test_sums_multiple_channel_collected_counts(self):
        log = (
            "## 2026-06-15\n"
            "* **Collectors**: gmail=5, obsidian=3, pdf=0, youtube=2\n"
            "* **Ingest**: 8 ingested · 0 deferred · status=ok\n"
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
            "## 2026-06-15\n"
            "* **Collectors**: gmail=0, obsidian=0\n"
            "* **Ingest**: 0 ingested · 0 deferred · status=ok\n"
        )
        result = pending_review.latest_run_summary(log)
        assert result is not None
        assert result["collected"] == 0
        assert result["ingested"] == 0

    def test_does_not_confuse_regular_ingest_with_scheduled_run(self):
        # Date group with a regular ingest (no Collectors bullet) appears BEFORE
        # the date group that has a scheduled run — the first Collectors bullet
        # is in the older group; date must be taken from that group's heading.
        log = (
            "## 2026-06-16\n"
            "* **Ingest**: ingest-auto batch — some sources (10 processed, 5 ingested)\n"
            "\n"
            "## 2026-06-15\n"
            "* **Collectors**: gmail=3, obsidian=1\n"
            "* **Ingest**: 2 ingested · 0 deferred · status=ok\n"
        )
        result = pending_review.latest_run_summary(log)
        assert result is not None
        assert result["date"] == "2026-06-15"
        assert result["collected"] == 4
        assert result["ingested"] == 2

    def test_all_run_channels_parsed(self):
        # Full realistic Collectors line with all channels including links_refetch
        log = (
            "## 2026-07-03\n"
            "* **Collectors**: gmail=3, obsidian=0, pdf=0, youtube=29, "
            "github_discover=0, github=0, x=0, links_refetch=0\n"
            "* **Ingest**: 14 ingested · 0 deferred · status=ok\n"
        )
        result = pending_review.latest_run_summary(log)
        assert result is not None
        assert result["date"] == "2026-07-03"
        # 3+0+0+29+0+0+0+0 = 32
        assert result["collected"] == 32
        assert result["ingested"] == 14


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
        # No _REVIEW.md, no _log.md, no book-review queue
        ret = pending_review.main(
            review_path=tmp_path / "nonexistent_REVIEW.md",
            log_path=tmp_path / "nonexistent_log.md",
            book_review_path=tmp_path / "nonexistent_book_review.md",
            blog_review_path=tmp_path / "nonexistent_blog_review.md",
            stamp_path=tmp_path / "nonexistent_stamp",
        )
        assert ret == 0
        captured = capsys.readouterr()
        assert captured.out.strip() == ""

    def test_weekly_book_reminder_shows_then_silences(self, tmp_path, capsys):
        import datetime
        book = tmp_path / "_book_review.md"
        book.write_text("- [ ] [A](https://x/a.pdf)\n- [x] [B](https://y/b.pdf)\n"
                        "- [ ] [C](https://z/c.pdf)\n", encoding="utf-8")
        stamp = tmp_path / ".reminded"
        empty = tmp_path / "none.md"
        blog = tmp_path / "_blog_review.md"
        blog.write_text("- [ ] https://x.dev/\n", encoding="utf-8")
        kw = dict(review_path=empty, log_path=empty, book_review_path=book,
                  blog_review_path=blog, stamp_path=stamp)

        pending_review.main(**kw, today=datetime.date(2026, 7, 7))
        out1 = capsys.readouterr().out
        assert "2 book(s)" in out1 and "1 blog(s)" in out1
        assert stamp.read_text().strip() == "2026-07-07"

        pending_review.main(**kw, today=datetime.date(2026, 7, 10))   # 3 days later
        assert capsys.readouterr().out.strip() == ""                  # still within the week

        pending_review.main(**kw, today=datetime.date(2026, 7, 14))   # 7 days later
        assert "await your review" in capsys.readouterr().out

    def test_prints_line_when_deferred_and_run_exist(self, tmp_path, capsys):
        review = tmp_path / "_REVIEW.md"
        review.write_text(
            "- DEFER G1: source-a.md — paywalled\n"
            "- DEFER G2: source-b.md — duplicate\n"
            "- DEFER UNCERTAIN: source-c.md — unclear\n",
            encoding="utf-8",
        )
        log = tmp_path / "log.md"
        log.write_text(
            "## 2026-06-15\n"
            "* **Collectors**: gmail=4\n"
            "* **Ingest**: 3 ingested · 3 deferred · status=ok\n",
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


# ---------------------------------------------------------------------------
# OKF date-heading extraction
# ---------------------------------------------------------------------------

class TestOKFDateHeadingExtraction:
    """latest_run_summary must read the date from ## YYYY-MM-DD headings (OKF format)."""

    def test_date_extracted_from_heading(self):
        """## YYYY-MM-DD heading → date field is exactly 'YYYY-MM-DD'."""
        log = (
            "## 2026-06-15\n"
            "* **Collectors**: gmail=3\n"
            "* **Ingest**: 2 ingested · 0 deferred · status=ok\n"
        )
        result = pending_review.latest_run_summary(log)
        assert result is not None
        assert result["date"] == "2026-06-15", (
            f"expected '2026-06-15', got {result['date']!r}"
        )

    def test_build_line_renders_date_only(self):
        """build_line shows only YYYY-MM-DD in the output line (no time component)."""
        summary = {"date": "2026-06-15", "collected": 3, "ingested": 2}
        line = pending_review.build_line(summary, 0)
        assert "2026-06-15" in line
        # No stray time or bracket characters
        assert "[" not in line
        assert "08:00" not in line

    def test_no_heading_returns_none(self):
        """A Collectors bullet with no preceding ## YYYY-MM-DD heading → None."""
        log = "* **Collectors**: gmail=3\n* **Ingest**: 1 ingested · 0 deferred · status=ok\n"
        result = pending_review.latest_run_summary(log)
        assert result is None

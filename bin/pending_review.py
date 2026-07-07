#!/usr/bin/env python3
"""pending_review.py — surface pending-review state at SessionStart.

Reads raw/_inbox/_REVIEW.md (count lines beginning with "- DEFER ") and the
latest "## [...] config | scheduled run" block in corpus/_log.md, then prints
a single human-readable status line — or nothing when the corpus is clean.

Never raises: all file-reads are defensive; exit 0 always.
"""
from __future__ import annotations

import datetime
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REVIEW_PATH = ROOT / "raw" / "_inbox" / "_REVIEW.md"
LOG_PATH = ROOT / "corpus" / "log.md"
# Book-review queue lives in the Obsidian vault (phone-tickable); reading it here is fine.
BOOK_REVIEW_PATH = Path(os.environ.get(
    "CORPUS_BOOK_REVIEW",
    str(Path.home() / "Dev" / "second-brain" / "00_Inbox" / "Clippings" / "Books to review.md")))
BOOK_REMINDER_STAMP = ROOT / "raw" / ".book_review_reminded"
BOOK_REMINDER_INTERVAL_DAYS = 7


def count_unticked_books(text: str) -> int:
    """Count '- [ ]' entries (books awaiting approval) in the book-review queue."""
    return sum(1 for line in text.splitlines() if line.lstrip().startswith("- [ ]"))


def reminder_due(stamp_text: str, today: datetime.date,
                 interval_days: int = BOOK_REMINDER_INTERVAL_DAYS) -> bool:
    """True if the weekly book-review reminder is due (never shown, or >= interval days ago)."""
    m = re.search(r"\d{4}-\d{2}-\d{2}", stamp_text or "")
    if not m:
        return True
    try:
        last = datetime.date.fromisoformat(m.group(0))
    except ValueError:
        return True
    return (today - last).days >= interval_days


# ---------------------------------------------------------------------------
# Pure functions (testable without real files)
# ---------------------------------------------------------------------------

def count_deferred(review_text: str) -> int:
    """Count lines that begin with '- DEFER ' in review_text."""
    count = 0
    for line in review_text.splitlines():
        if line.startswith("- DEFER "):
            count += 1
    return count


def latest_run_summary(log_text: str) -> dict | None:
    """Return a dict with keys 'date', 'collected', 'ingested' from the most
    recent scheduled-run block in log_text (OKF format), or None when no such
    block exists or parsing fails.

    The log uses OKF format (newest first, grouped by ``## YYYY-MM-DD`` date
    headings).  A scheduled-run block is identified by the presence of a
    ``* **Collectors**:`` bullet (only scheduled runs emit this).  The
    enclosing ``## YYYY-MM-DD`` date heading provides the run date.

    Expected block shape (produced by scheduled_run.write_run_report):
        ## YYYY-MM-DD
        * **Collectors**: gmail=3, obsidian=0, pdf=0, youtube=24, ...
        * **Ingest**: 41 ingested · 9 deferred · status=ok
        [* **YoutubeQuick**: ...]  (optional)
        [* **DocsQuick**: ...]     (optional)
        [* **Lint**: ...]          (optional)
        [* **Commit**: ...]        (optional)

    Channel counts in the Collectors bullet use ``channel=N`` format joined by
    ``', '``.  The scheduled-run Ingest bullet starts with ``N ingested``
    (a digit), distinguishing it from regular ingest entries like
    ``* **Ingest**: ingest-auto batch — ...``.
    """
    # Find the first (newest) '* **Collectors**:' bullet — log is newest-first
    collectors_re = re.compile(r"^\* \*\*Collectors\*\*:(.*)$", re.MULTILINE)
    collectors_match = collectors_re.search(log_text)
    if not collectors_match:
        return None

    # Find the enclosing ## YYYY-MM-DD heading by scanning backwards from the bullet
    preamble = log_text[: collectors_match.start()]
    date_re = re.compile(r"^## (\d{4}-\d{2}-\d{2})\s*$", re.MULTILINE)
    date_matches = list(date_re.finditer(preamble))
    if not date_matches:
        return None
    date_display = date_matches[-1].group(1)

    # Parse per-channel counts from the Collectors line: channel=N format
    collectors_line = collectors_match.group(1)
    collected_total = sum(
        int(m.group(1)) for m in re.finditer(r"\b\w+=(\d+)", collectors_line)
    )

    # Slice to just this scheduled-run block: Collectors bullet → next date group
    rest = log_text[collectors_match.start():]
    next_date = re.search(r"\n## \d{4}-\d{2}-\d{2}", rest)
    block_text = rest[: next_date.start()] if next_date else rest

    # Parse '* **Ingest**: N ingested' (scheduled-run format: digit immediately
    # after ': ', not text like 'ingest-auto batch')
    ingest_re = re.compile(r"^\* \*\*Ingest\*\*: (\d+) ingested", re.MULTILINE)
    ingest_match = ingest_re.search(block_text)
    ingested_total = int(ingest_match.group(1)) if ingest_match else 0

    return {
        "date": date_display,
        "collected": collected_total,
        "ingested": ingested_total,
    }


def build_line(summary: dict | None, deferred: int) -> str:
    """Build the single output line, or return '' for clean-state.

    Args:
        summary: output of latest_run_summary (None if no run ever recorded).
        deferred: number of DEFER entries in _REVIEW.md (0 if absent/empty).

    Returns '' when there is nothing to report (no run block, no deferred items).
    """
    if summary is None and deferred == 0:
        return ""

    if summary is not None:
        date = summary["date"]
        collected = summary["collected"]
        ingested = summary["ingested"]
        line = (
            f"Corpus: last auto-run {date}"
            f" — {collected} collected · {ingested} ingested"
        )
    else:
        # deferred > 0 but no run block found
        line = "Corpus: no scheduled run recorded yet"

    if deferred > 0:
        line += f" · {deferred} awaiting your decision (see raw/_inbox/_REVIEW.md)"

    return line


# ---------------------------------------------------------------------------
# Main — reads real paths; overridable for tests via keyword args
# ---------------------------------------------------------------------------

def main(
    *,
    review_path: Path | None = None,
    log_path: Path | None = None,
    book_review_path: Path | None = None,
    stamp_path: Path | None = None,
    today: datetime.date | None = None,
) -> int:
    _review_path = review_path if review_path is not None else REVIEW_PATH
    _log_path = log_path if log_path is not None else LOG_PATH

    try:
        review_text = _review_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        review_text = ""

    try:
        log_text = _log_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        log_text = ""

    deferred = count_deferred(review_text)
    summary = latest_run_summary(log_text)
    line = build_line(summary, deferred)

    if line:
        print(line)

    # Weekly book-review nudge: at most once per BOOK_REMINDER_INTERVAL_DAYS, and only when
    # books actually await a tick. Stamped on show so it stays roughly weekly across sessions.
    try:
        book_text = (book_review_path if book_review_path is not None
                     else BOOK_REVIEW_PATH).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        book_text = ""
    unticked = count_unticked_books(book_text)
    stamp = stamp_path if stamp_path is not None else BOOK_REMINDER_STAMP
    try:
        stamp_text = stamp.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        stamp_text = ""
    today = today if today is not None else datetime.date.today()
    if unticked > 0 and reminder_due(stamp_text, today):
        print(f"📚 Corpus: {unticked} book(s) await your review — skim raw/_book_review.md "
              f"and tick [x] the good ones (they auto-download next run).")
        try:
            stamp.write_text(today.isoformat() + "\n", encoding="utf-8")
        except OSError:
            pass

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception:  # noqa: BLE001 — never let SessionStart hook crash
        raise SystemExit(0)

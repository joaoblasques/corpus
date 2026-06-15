#!/usr/bin/env python3
"""pending_review.py — surface pending-review state at SessionStart.

Reads raw/_inbox/_REVIEW.md (count lines beginning with "- DEFER ") and the
latest "## [...] config | scheduled run" block in corpus/_log.md, then prints
a single human-readable status line — or nothing when the corpus is clean.

Never raises: all file-reads are defensive; exit 0 always.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REVIEW_PATH = ROOT / "raw" / "_inbox" / "_REVIEW.md"
LOG_PATH = ROOT / "corpus" / "_log.md"


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
    recent '## [...] config | scheduled run' block in log_text, or None when
    no such block exists or parsing fails.

    Expected block shape (produced by scheduled_run.write_run_report):
        ## [2026-06-15 08:00] config | scheduled run
        - collectors:
          - gmail: 3 collected · status=ok
          - obsidian: 1 collected · status=ok
        - ingest:
          - ingest: 2 ingested · 0 deferred · status=ok
    """
    # Find all block header positions (we want the LAST one)
    header_re = re.compile(
        r"^## \[([^\]]+)\] config \| scheduled run$", re.MULTILINE
    )
    matches = list(header_re.finditer(log_text))
    if not matches:
        return None

    last_match = matches[-1]
    date_str = last_match.group(1)  # e.g. "2026-06-15 08:00" or "2026-06-15T08:00"
    # Keep only the date part for display — split on T or space (ISO 8601 variants)
    date_display = re.split(r"[T ]", date_str)[0] if date_str else date_str

    # Slice the block text from the header to the next "## " or end-of-string
    block_start = last_match.start()
    next_header = re.search(r"\n## ", log_text[last_match.end():])
    if next_header:
        block_text = log_text[block_start: last_match.end() + next_header.start()]
    else:
        block_text = log_text[block_start:]

    # Sum all "N collected" mentions in the block (one per channel)
    collected_total = sum(
        int(m.group(1)) for m in re.finditer(r"(\d+) collected", block_text)
    )

    # Extract "N ingested" from the ingest line
    ingested_match = re.search(r"(\d+) ingested", block_text)
    ingested_total = int(ingested_match.group(1)) if ingested_match else 0

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

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception:  # noqa: BLE001 — never let SessionStart hook crash
        raise SystemExit(0)

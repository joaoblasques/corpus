"""Characterization tests for bin/lint (BROKEN_LINK + ORPHAN rules).

Runner: pytest  (pip install pytest)
Run:    pytest tests/

Stream contract (confirmed against bin/lint source):
  - "BROKEN_LINK", "ORPHAN", "Clean.", and the summary line → stdout.
  - "not a directory" / argparse / internal errors → stderr.

Fixture note: frontmatter in fixtures follows the v0.5/v0.6 schema for
forward-compatibility, but bin/lint does not parse frontmatter beyond
alias extraction. Fields like type/domain/status are inert to the linter.
"""

import subprocess
import sys
from pathlib import Path

FIXTURES = Path(__file__).parent / "fixtures"
LINT     = Path(__file__).parent.parent / "bin" / "lint"


def run_lint(fixture: str):
    return subprocess.run(
        [sys.executable, str(LINT), str(FIXTURES / fixture)],
        capture_output=True,
        text=True,
    )


# --- BROKEN_LINK ----------------------------------------------------------

def test_broken_link_error_and_exit_2():
    r = run_lint("broken-link")
    assert r.returncode == 2
    assert "BROKEN_LINK" in r.stdout
    assert "missing-page" in r.stdout
    assert "ORPHAN" not in r.stdout  # README exempt; no other pages present

def test_clean_corpus_no_broken_link():
    r = run_lint("clean")
    assert "BROKEN_LINK" not in r.stdout


# --- ORPHAN ---------------------------------------------------------------

def test_orphan_warning_and_exit_1():
    r = run_lint("orphan")
    assert r.returncode == 1
    assert "ORPHAN" in r.stdout

def test_clean_corpus_no_orphan():
    r = run_lint("clean")
    assert "ORPHAN" not in r.stdout


# --- Exit-code precedence -------------------------------------------------

def test_clean_exit_0():
    r = run_lint("clean")
    assert r.returncode == 0
    assert "Clean." in r.stdout

def test_mixed_error_wins_exit_2():
    r = run_lint("mixed")
    assert r.returncode == 2
    assert "BROKEN_LINK" in r.stdout
    assert "ORPHAN" in r.stdout

def test_missing_path_exit_3(tmp_path):
    missing = tmp_path / "no-such-subdir"
    r = subprocess.run(
        [sys.executable, str(LINT), str(missing)],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 3
    assert "not a directory" in r.stderr

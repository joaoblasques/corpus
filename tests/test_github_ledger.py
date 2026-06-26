from __future__ import annotations
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import github_ledger  # noqa: E402


def test_unknown_repo_not_digested(tmp_path):
    led = tmp_path / "github_digested.txt"
    assert github_ledger.is_digested("owner/name", led) is False


def test_mark_then_is_digested(tmp_path):
    led = tmp_path / "github_digested.txt"
    github_ledger.mark_digested("owner/name", led)
    assert github_ledger.is_digested("owner/name", led) is True


def test_mark_is_idempotent(tmp_path):
    led = tmp_path / "github_digested.txt"
    github_ledger.mark_digested("owner/name", led)
    github_ledger.mark_digested("owner/name", led)
    lines = [l for l in led.read_text(encoding="utf-8").splitlines() if l.strip()]
    assert lines.count("owner/name") == 1


def test_creates_parent_dir(tmp_path):
    led = tmp_path / "state" / "github_digested.txt"
    github_ledger.mark_digested("a/b", led)
    assert led.exists()

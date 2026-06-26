"""Committed dedup ledger for the GitHub collector.

GitHub stars stay in place (a bookmark, not a queue), so the collector cannot
dedup via source state. In a stateless cloud run there is no persistent raw/ to
glob either. This tracked file (one `owner/name` per line) records repos already
digested, so both local and cloud runs skip them.
"""
from __future__ import annotations

from pathlib import Path

LEDGER_PATH = Path(__file__).resolve().parent.parent / "automation" / "state" / "github_digested.txt"


def _entries(ledger_path: Path) -> set[str]:
    if not ledger_path.exists():
        return set()
    return {
        line.strip()
        for line in ledger_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }


def is_digested(full_name: str, ledger_path: Path = LEDGER_PATH) -> bool:
    return full_name in _entries(ledger_path)


def mark_digested(full_name: str, ledger_path: Path = LEDGER_PATH) -> None:
    if is_digested(full_name, ledger_path):
        return
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with ledger_path.open("a", encoding="utf-8") as fh:
        fh.write(full_name + "\n")

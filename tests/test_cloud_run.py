from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import cloud_run  # noqa: E402

BIN = Path(__file__).resolve().parent.parent / "bin"


def test_plan_steps_ordered_and_complete():
    steps = [s["step"] for s in cloud_run.plan_steps()]
    # the single-cloud-writer nightly shape (spec §4.1)
    assert steps == [
        "clone_repos",
        "collect_sources",
        "drain_youtube_queue",
        "ingest",
        "reap_and_ledger",
        "commit_and_push",
    ]


def test_dry_run_cli_emits_json_and_no_side_effects():
    proc = subprocess.run(
        [sys.executable, str(BIN / "cloud_run.py"), "--dry-run"],
        capture_output=True, text=True, timeout=30,
    )
    assert proc.returncode == 0
    data = json.loads(proc.stdout)
    assert data["dry_run"] is True
    assert len(data["steps"]) == 6


def test_live_run_not_implemented_returns_nonzero():
    proc = subprocess.run(
        [sys.executable, str(BIN / "cloud_run.py")],
        capture_output=True, text=True, timeout=30,
    )
    assert proc.returncode == 1

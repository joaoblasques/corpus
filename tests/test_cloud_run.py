from __future__ import annotations
import json
import subprocess
import sys
import types
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import cloud_run  # noqa: E402

BIN = Path(__file__).resolve().parent.parent / "bin"


def _fake_proc(returncode=0, stdout=""):
    return types.SimpleNamespace(returncode=returncode, stdout=stdout)


def _git_runner(branch="main", staged_files="corpus/x.md", commit_rc=0, push_rc=0,
                origin="https://github.com/joaoblasques/corpus.git"):
    """Fake subprocess.run scripting the git calls commit_push makes, in order:
    rev-parse (branch) -> add -> diff --cached --name-only (staged) -> commit ->
    [cloud: remote get-url] -> push."""
    calls = []

    def run(cmd, *a, **k):
        calls.append(cmd)
        if "rev-parse" in cmd:
            return _fake_proc(0, branch + "\n")
        if "remote" in cmd and "get-url" in cmd:
            return _fake_proc(0, origin + "\n")
        if "diff" in cmd and "--name-only" in cmd:
            return _fake_proc(0, staged_files)
        if "commit" in cmd:
            return _fake_proc(commit_rc, "")
        if "push" in cmd:
            return _fake_proc(push_rc, "")
        return _fake_proc(0, "")

    run.calls = calls
    return run


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


# --- Task 1: collect subcommand ---

def test_run_collectors_runs_github_and_parses_json_report():
    calls = []

    def fake_run(cmd, *a, **k):
        calls.append(cmd)
        return _fake_proc(0, '{"found": 3, "written": 2, "duplicate": 1}')

    report = cloud_run.run_collectors(only=["github"], _run=fake_run)
    assert len(calls) == 1
    assert calls[0][1].endswith("github_client.py") and calls[0][2] == "run"
    assert report["github"]["returncode"] == 0
    assert report["github"]["report"]["written"] == 2


def test_run_collectors_keeps_raw_stdout_when_not_json():
    report = cloud_run.run_collectors(
        only=["github"], _run=lambda *a, **k: _fake_proc(0, "not json")
    )
    assert report["github"]["report"] == "not json"


def test_collect_cli_returns_nonzero_when_a_collector_fails():
    rc = cloud_run.main(
        ["collect", "--only", "github"],
        _run=lambda *a, **k: _fake_proc(1, '{"error": "gh auth"}'),
    )
    assert rc == 1


def test_collect_cli_rejects_unknown_collector():
    # a typo'd --only must fail loudly (exit 1), never silently no-op to exit 0
    called = []
    rc = cloud_run.main(
        ["collect", "--only", "nope"],
        _run=lambda *a, **k: called.append(1) or _fake_proc(0, "{}"),
    )
    assert rc == 1
    assert called == []  # no collector subprocess was launched


def test_dry_run_takes_precedence_over_subcommand():
    # --dry-run must print the plan and never trigger a live collect
    called = []
    rc = cloud_run.main(
        ["--dry-run", "collect"],
        _run=lambda *a, **k: called.append(1) or _fake_proc(0, "{}"),
    )
    assert rc == 0
    assert called == []


# --- Task 2: commit-push subcommand ---

# local mode = no token: keep the strict main-guard + push origin main.
# token="" forces local mode deterministically regardless of the test env.

def test_commit_push_aborts_off_main():
    run = _git_runner(branch="feature/x")
    res = cloud_run.commit_push(cloud_run.ROOT, token="", _run=run)
    assert res["status"] == "aborted"
    assert not any("commit" in c for c in run.calls)
    assert not any("push" in c for c in run.calls)


def test_commit_push_noop_when_nothing_staged():
    run = _git_runner(staged_files="")
    res = cloud_run.commit_push(cloud_run.ROOT, token="", _run=run)
    assert res["status"] == "noop"
    assert not any("commit" in c for c in run.calls)


def test_commit_push_commits_and_pushes_when_changes_present():
    run = _git_runner(staged_files="corpus/a.md\ncorpus/b.md")
    res = cloud_run.commit_push(cloud_run.ROOT, token="", _run=run)
    assert res["status"] == "pushed"
    assert res["files"] == 2
    assert any("commit" in c for c in run.calls)
    # local mode pushes the literal origin/main refspec
    push = [c for c in run.calls if "push" in c][0]
    assert "origin" in push and "main" in push


def test_commit_push_reports_push_failure():
    run = _git_runner(staged_files="corpus/a.md", push_rc=1)
    res = cloud_run.commit_push(cloud_run.ROOT, token="", _run=run)
    assert res["status"] == "push-failed"


def test_commit_push_cli_nonzero_on_abort(monkeypatch):
    monkeypatch.delenv("GH_TOKEN", raising=False)
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    rc = cloud_run.main(["commit-push"], _run=_git_runner(branch="dev"))
    assert rc == 1


def test_commit_push_cli_nonzero_on_commit_failure():
    rc = cloud_run.main(["commit-push"], _run=_git_runner(commit_rc=1))
    assert rc == 1


# cloud mode = token present: push HEAD:main via the tokenized URL, no main-guard.

def test_commit_push_cloud_pushes_head_to_main_via_token():
    run = _git_runner(branch="claude/lucid-pascal", staged_files="corpus/a.md")
    res = cloud_run.commit_push(cloud_run.ROOT, token="ghpat_SECRET", _run=run)
    assert res["status"] == "pushed"          # NOT aborted despite non-main branch
    push = [c for c in run.calls if "push" in c][0]
    assert "HEAD:main" in push
    joined = " ".join(push)
    assert "x-access-token:ghpat_SECRET@github.com/joaoblasques/corpus.git" in joined


def test_commit_push_cloud_noop_when_clean():
    run = _git_runner(branch="claude/x", staged_files="")
    res = cloud_run.commit_push(cloud_run.ROOT, token="ghpat_X", _run=run)
    assert res["status"] == "noop"


def test_commit_push_report_never_contains_token():
    run = _git_runner(branch="claude/x", staged_files="corpus/a.md")
    res = cloud_run.commit_push(cloud_run.ROOT, token="ghpat_SECRET", _run=run)
    assert "ghpat_SECRET" not in json.dumps(res)


def test_tokenized_remote_https_ssh_and_no_suffix():
    t = "TKN"
    assert cloud_run._tokenized_remote("https://github.com/o/r.git", t) == \
        "https://x-access-token:TKN@github.com/o/r.git"
    assert cloud_run._tokenized_remote("git@github.com:o/r.git", t) == \
        "https://x-access-token:TKN@github.com/o/r.git"
    assert cloud_run._tokenized_remote("https://github.com/o/r", t) == \
        "https://x-access-token:TKN@github.com/o/r.git"


def test_doctor_reports_secrets_and_reachability(monkeypatch):
    monkeypatch.setenv("GH_TOKEN", "x")
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.setenv("SCHEDULED_RUN_INGEST_MODEL", "claude-sonnet-4-6")

    def fake_run(cmd, *a, **k):
        if "rev-parse" in cmd:
            return _fake_proc(0, "claude/abc\n")
        if cmd[:1] == ["gh"]:
            return _fake_proc(0, "{}")
        return _fake_proc(0, "")

    d = cloud_run.doctor(_run=fake_run)
    assert d["GH_TOKEN_set"] is True
    assert d["GITHUB_TOKEN_set"] is False
    assert d["SCHEDULED_RUN_INGEST_MODEL"] == "claude-sonnet-4-6"
    assert d["gh_auth_status_rc"] == 0 and d["gh_api_user_rc"] == 0
    assert d["branch"] == "claude/abc"

# Cloud Nightly — Phase 1: GitHub-only end-to-end cloud loop

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prove the full nightly cloud loop end-to-end with the one collector that is already cloud-safe — clone → collect GitHub stars (ledger-deduped) → agent ingests → commit + push `corpus/` and the ledger — running in an Anthropic cloud Routine, billed only against the Max plan.

**Architecture:** `bin/cloud_run.py` grows from a dry-run skeleton into a real orchestrator with two deterministic subcommands the routine agent calls around its own ingest step: `collect` (runs the GitHub collector, emits a JSON report) and `commit-push` (main-branch-guarded `git add corpus/ automation/state/` → commit → `push origin main`, a clean no-op when nothing changed). The agent does the *judgment* step (ingest) in-session; `cloud_run.py` owns only the mechanical steps. The existing top-level `--dry-run` (the current smoke-test entrypoint) is preserved unchanged.

**Tech Stack:** Python 3.12 stdlib (`argparse`, `json`, `subprocess`, `pathlib`), pytest. No new third-party deps. GitHub auth in the cloud is the `gh` CLI reading `GH_TOKEN` (no auth code change); git push uses the routine's GitHub connection.

**Spec:** `docs/superpowers/specs/2026-06-26-cloud-nightly-migration-design.md` (§3 hybrid single-writer, §4.2 the routine/cloud_run split, §4.3 GitHub ledger, §10 Phase 1).

**Why GitHub-only (re-slice from the spec's "gmail+github+x" Phase 1):** In the cloud the `raw/` inbox is ephemeral. GitHub dedups via the committed `automation/state/github_digested.txt` ledger and never mutates the source, so a crashed run simply re-derives cleanly next time. Gmail (`gmail_client.py run` archives starred mail *immediately* after the ephemeral-inbox write) and X (un-bookmark) reap at the source before the corpus is durably pushed — a crash between reap and push silently loses knowledge, which cannot happen locally where the inbox persists. Fixing that needs a "collect-only, reap strictly after push" change to those two collectors. That hardening rides with Phase 2; Phase 1 proves the entire loop without it.

## Global Constraints

- Python 3.12; stdlib only (no new dependencies).
- **Preserve `python3 bin/cloud_run.py --dry-run`** exactly — it prints `{"dry_run": true, "steps": [...6...]}` and exits 0. The user's live smoke-test routine already calls it; do not break it.
- Never write outside the repo. Only `corpus/` and `automation/state/` are committed by the run; `raw/` stays gitignored and is never committed.
- A scheduled/cloud run operates on **`main` only**. `commit-push` must abort (non-zero, no commit) on any other branch — same guard discipline as `bin/scheduled_run.py`.
- Failure must be loud: any step that errors returns a non-zero exit code so the Routine run-history records a failed run (no silent stalls — the exact problem this migration fixes). Email failure-alerts are a Phase 2 add, out of scope here.
- Tests live under `tests/`, run with `python3 -m pytest`, no network, no real `git push`. Use an injected subprocess seam (`_run=`) exactly like `tests/test_scheduled_run.py`.
- Commit after each task. Commit-message footer (every commit):
  ```
  Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
  Claude-Session: https://claude.ai/code/session_01GrGvMKSxgyetukaRpXyaf5
  ```

## File Structure

- Modify `bin/cloud_run.py` — add `collect` and `commit-push` subcommands + their helper functions; keep `plan_steps()` and `--dry-run`.
- Modify `tests/test_cloud_run.py` — add tests for the two new subcommands and the main-branch guard; keep the existing three tests green.
- Create `docs/cloud-nightly-runbook.md` — the operator runbook: the exact live routine prompt, the `GH_TOKEN` secret, the push-permission setting, and how to read a run.

---

## Global interfaces (defined here, used across tasks)

`bin/cloud_run.py` after this phase exposes:

- `plan_steps() -> list[dict]` — unchanged (Phase 0).
- `run_collectors(only: list[str] | None = None, *, _run=None) -> dict` — runs each enabled collector subprocess; returns `{name: {"returncode": int, "report": <parsed-json-or-raw-str>}}`. Phase 1 enables only `github`.
- `commit_push(repo: Path, *, message: str | None = None, _run=None) -> dict` — main-guarded stage/commit/push of `corpus/` + `automation/state/`; returns `{"status": "pushed"|"noop"|"aborted"|"push-failed", ...}`.
- `on_main(repo: Path, *, _run=None) -> bool` — true iff `git -C repo rev-parse --abbrev-ref HEAD` is `main`.
- CLI: `--dry-run` (unchanged); `collect [--only github]`; `commit-push [--repo PATH] [--message MSG]`.

The `_run` parameter defaults to `subprocess.run` and is the only seam tests inject. Each injected fake returns an object with `.returncode` (int) and `.stdout` (str).

---

### Task 1: `collect` subcommand (GitHub collector runner)

**Files:**
- Modify: `bin/cloud_run.py`
- Test: `tests/test_cloud_run.py`

**Interfaces:**
- Consumes: the existing `bin/github_client.py run` CLI (prints a JSON report; deduped by the Phase-0 ledger).
- Produces: `run_collectors(only=None, *, _run=None) -> dict` and a CLI `python3 bin/cloud_run.py collect [--only github]` that prints `{"collected": {...}}` and returns 0 when every collector exits 0, else 1.

- [ ] **Step 1: Write the failing tests**

Add to `tests/test_cloud_run.py`:

```python
import types  # add near the existing imports


def _fake_proc(returncode=0, stdout=""):
    return types.SimpleNamespace(returncode=returncode, stdout=stdout)


def test_run_collectors_runs_github_and_parses_json_report():
    calls = []

    def fake_run(cmd, *a, **k):
        calls.append(cmd)
        return _fake_proc(0, '{"found": 3, "written": 2, "duplicate": 1}')

    report = cloud_run.run_collectors(only=["github"], _run=fake_run)
    # github_client.py run was invoked exactly once
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
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m pytest tests/test_cloud_run.py -q`
Expected: FAIL — `AttributeError: module 'cloud_run' has no attribute 'run_collectors'` (and `main()` does not yet accept `_run`).

- [ ] **Step 3: Implement `run_collectors` + wire `collect` into `main`**

In `bin/cloud_run.py`, extend the imports and add the collector machinery. Replace the current import block and `main` with:

```python
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent
ROOT = BIN.parent
GIT_BIN = "git"
COLLECTOR_TIMEOUT = 1200  # s — cap a hung API call; mirrors scheduled_run.COLLECTOR_TIMEOUT

# name -> argv. Phase 1 enables only github (cloud-safe: ledger dedup, no reap).
COLLECTORS = {
    "github": [sys.executable, str(BIN / "github_client.py"), "run"],
}


def _maybe_json(text: str):
    try:
        return json.loads(text)
    except (ValueError, TypeError):
        return text


def run_collectors(only=None, *, _run=None) -> dict:
    _run = _run or subprocess.run
    report = {}
    for name, cmd in COLLECTORS.items():
        if only is not None and name not in only:
            continue
        proc = _run(cmd, capture_output=True, text=True, timeout=COLLECTOR_TIMEOUT)
        report[name] = {
            "returncode": proc.returncode,
            "report": _maybe_json(proc.stdout),
        }
    return report
```

Keep `plan_steps()` exactly as-is. Then rewrite `main` to accept the `_run` seam and dispatch subcommands while preserving `--dry-run`:

```python
def main(argv=None, *, _run=None) -> int:
    ap = argparse.ArgumentParser(description="Nightly cloud corpus run.")
    ap.add_argument("--dry-run", action="store_true", help="print the planned steps and exit")
    sub = ap.add_subparsers(dest="cmd")

    pc = sub.add_parser("collect", help="run cloud-safe collectors into raw/_inbox/")
    pc.add_argument("--only", action="append", default=None,
                    help="restrict to named collector(s); repeatable")

    args = ap.parse_args(argv)

    if args.cmd == "collect":
        report = run_collectors(only=args.only, _run=_run)
        print(json.dumps({"collected": report}, indent=2))
        return 0 if all(v["returncode"] == 0 for v in report.values()) else 1

    if args.dry_run:
        print(json.dumps({"dry_run": True, "steps": plan_steps()}))
        return 0

    print(json.dumps({"error": "no command: pass --dry-run or a subcommand"}))
    return 1
```

> Note: the existing Phase-0 test `test_live_run_not_implemented_returns_nonzero` invokes the bare CLI (no args) and asserts exit 1 — still true (the final branch). `test_dry_run_cli_emits_json_and_no_side_effects` still passes (the `--dry-run` branch is unchanged).

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python3 -m pytest tests/test_cloud_run.py -q`
Expected: PASS (all Phase-0 tests + the 3 new ones).

- [ ] **Step 5: Commit**

```bash
git add bin/cloud_run.py tests/test_cloud_run.py
git commit -m "feat(cloud_run): add collect subcommand (github collector runner, JSON report)"
```

---

### Task 2: `commit-push` subcommand (main-guarded publish)

**Files:**
- Modify: `bin/cloud_run.py`
- Test: `tests/test_cloud_run.py`

**Interfaces:**
- Produces:
  - `on_main(repo: Path, *, _run=None) -> bool`
  - `commit_push(repo: Path, *, message: str | None = None, _run=None) -> dict` — aborts unless on `main`; stages `corpus/` + `automation/state/`; a clean tree is a `noop`; otherwise commits and pushes `origin main`.
  - CLI `python3 bin/cloud_run.py commit-push [--repo PATH] [--message MSG]` printing the dict and returning 0 on `pushed`/`noop`, 1 on `aborted`/`push-failed`.

- [ ] **Step 1: Write the failing tests**

Add to `tests/test_cloud_run.py`:

```python
def _git_runner(branch="main", staged_files="corpus/x.md", push_rc=0):
    """Fake subprocess.run that scripts the git calls commit_push makes, in order:
    rev-parse (branch) -> add -> diff --cached --name-only (staged) -> commit -> push."""
    calls = []

    def run(cmd, *a, **k):
        calls.append(cmd)
        if "rev-parse" in cmd:
            return _fake_proc(0, branch + "\n")
        if "diff" in cmd and "--name-only" in cmd:
            return _fake_proc(0, staged_files)
        if "push" in cmd:
            return _fake_proc(push_rc, "")
        return _fake_proc(0, "")

    run.calls = calls
    return run


def test_commit_push_aborts_off_main():
    run = _git_runner(branch="feature/x")
    res = cloud_run.commit_push(cloud_run.ROOT, _run=run)
    assert res["status"] == "aborted"
    # never committed or pushed
    assert not any("commit" in c for c in run.calls)
    assert not any("push" in c for c in run.calls)


def test_commit_push_noop_when_nothing_staged():
    run = _git_runner(staged_files="")
    res = cloud_run.commit_push(cloud_run.ROOT, _run=run)
    assert res["status"] == "noop"
    assert not any("commit" in c for c in run.calls)


def test_commit_push_commits_and_pushes_when_changes_present():
    run = _git_runner(staged_files="corpus/a.md\ncorpus/b.md")
    res = cloud_run.commit_push(cloud_run.ROOT, _run=run)
    assert res["status"] == "pushed"
    assert res["files"] == 2
    assert any("commit" in c for c in run.calls)
    assert any("push" in c for c in run.calls)


def test_commit_push_reports_push_failure():
    run = _git_runner(staged_files="corpus/a.md", push_rc=1)
    res = cloud_run.commit_push(cloud_run.ROOT, _run=run)
    assert res["status"] == "push-failed"


def test_commit_push_cli_nonzero_on_abort():
    rc = cloud_run.main(["commit-push"], _run=_git_runner(branch="dev"))
    assert rc == 1
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m pytest tests/test_cloud_run.py -q`
Expected: FAIL — `AttributeError: module 'cloud_run' has no attribute 'commit_push'`.

- [ ] **Step 3: Implement `on_main` + `commit_push` and wire the CLI**

In `bin/cloud_run.py`, add after `run_collectors`:

```python
def _git(args, repo, _run):
    return _run([GIT_BIN, "-C", str(repo)] + args, capture_output=True, text=True)


def on_main(repo, *, _run=None) -> bool:
    _run = _run or subprocess.run
    proc = _git(["rev-parse", "--abbrev-ref", "HEAD"], repo, _run)
    return proc.returncode == 0 and proc.stdout.strip() == "main"


def commit_push(repo, *, message=None, _run=None) -> dict:
    _run = _run or subprocess.run
    repo = Path(repo)
    if not on_main(repo, _run=_run):
        return {"status": "aborted", "reason": "not on main"}
    _git(["add", "corpus", "automation/state"], repo, _run)
    staged = _git(["diff", "--cached", "--name-only"], repo, _run).stdout.strip()
    if not staged:
        return {"status": "noop"}
    n = len([s for s in staged.splitlines() if s.strip()])
    msg = message or f"chore(cloud-run): nightly corpus update — {n} file(s)"
    commit = _git(["commit", "-m", msg], repo, _run)
    if commit.returncode != 0:
        return {"status": "commit-failed", "files": n}
    push = _git(["push", "origin", "main"], repo, _run)
    return {"status": "pushed" if push.returncode == 0 else "push-failed", "files": n}
```

Then add the subparser and dispatch inside `main` (place the new parser next to `collect`, and the dispatch branch before the `--dry-run` branch):

```python
    pp = sub.add_parser("commit-push", help="main-guarded commit + push of corpus/ and ledgers")
    pp.add_argument("--repo", default=str(ROOT))
    pp.add_argument("--message", default=None)
```

```python
    if args.cmd == "commit-push":
        res = commit_push(Path(args.repo), message=args.message, _run=_run)
        print(json.dumps(res, indent=2))
        return 0 if res["status"] in ("pushed", "noop") else 1
```

> The footer's `Co-Authored-By`/`Claude-Session` trailers are for *this repo's plan/code commits*. The cloud run's automated corpus commits use the short `chore(cloud-run): …` message above (matching the existing `chore(auto-ingest): …` scheduled-run style) — no trailer.

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python3 -m pytest tests/test_cloud_run.py -q`
Expected: PASS (all prior + the 5 new ones).

- [ ] **Step 5: Sanity-check the preserved dry-run + a no-op publish on this repo**

Run: `python3 bin/cloud_run.py --dry-run | python3 -m json.tool`
Expected: still the 6 steps.

Run: `python3 bin/cloud_run.py commit-push --repo .`
Expected on a clean `main`: `{"status": "noop"}` and exit 0 — it stages nothing and makes no commit. (If the working tree happens to have staged corpus changes, it would commit+push; run only when clean, or expect that.)

- [ ] **Step 6: Commit**

```bash
git add bin/cloud_run.py tests/test_cloud_run.py
git commit -m "feat(cloud_run): add commit-push subcommand (main-guarded publish of corpus + ledgers)"
```

---

### Task 3: Operator runbook for the live routine

**Files:**
- Create: `docs/cloud-nightly-runbook.md`

This task has no test cycle (documentation). It captures the exact configuration the user pastes into the Routine so the live loop is reproducible and reviewable.

- [ ] **Step 1: Write the runbook**

Create `docs/cloud-nightly-runbook.md`:

````markdown
# Cloud Nightly Runbook (Phase 1 — GitHub loop)

The nightly corpus run executes as a Claude Code **Routine** in Anthropic's cloud,
billed against the Max plan (no metered API cost). Phase 1 runs the GitHub
collector end-to-end; Gmail/X/PDF/vault/YouTube arrive in later phases.

## Routine configuration (claude.ai/code/routines)

- **Name:** `corpus nightly`
- **Model:** Sonnet
- **Repository:** `corpus` (write access — needed for the nightly push to `main`)
- **Trigger:** Schedule → Daily → 02:00 (local tz). Minimum granularity is 1 hour.
- **Permissions:** enable **Allow unrestricted branch pushes** (the run commits to
  `main`, not a `claude/` branch).
- **Environment variables (secrets):**
  - `GH_TOKEN` — a fine-grained GitHub PAT with: read on starred repos' contents,
    and `contents: write` on the `corpus` repo (for the push). The `gh` CLI and
    `git push` both read it.
  - `SCHEDULED_RUN_INGEST_MODEL=claude-sonnet-4-6` — safety pin so any ingest
    defaults to Sonnet, never burning the weekly Opus cap.

## Routine prompt (paste verbatim)

> You are running the nightly corpus collection in this `corpus` repo, on `main`.
> Work autonomously per CLAUDE.md. Steps, in order:
> 1. Run `python3 bin/cloud_run.py collect --only github` and read its JSON report.
> 2. Ingest everything new in `raw/_inbox/` following CLAUDE.md §8.1 (route to
>    existing domains; do not invent new domains without the §9 bar; stamp sources;
>    update `corpus/_index.md` and append `corpus/_log.md`). Defer any gated
>    judgment to `raw/_inbox/_REVIEW.md` as usual.
> 3. Run `python3 bin/cloud_run.py commit-push --repo .` to publish `corpus/` and
>    the GitHub ledger to `main`.
> 4. Report a one-paragraph summary: repos collected, pages created/updated, and
>    the commit-push status. If any step exits non-zero, stop and report it as a
>    FAILED run — do not continue.

## Reading a run

- Success: `collect` reports `github` returncode 0; `commit-push` reports
  `pushed` (or `noop` if there were no new stars that night).
- The new corpus commit appears on `origin/main` as `chore(cloud-run): nightly …`.
- Confirm in account usage that the run drew on the **subscription**, not API spend.
- A failed step exits non-zero → the Routine run-history marks the run failed
  (Phase 1 has no email alert yet; that's Phase 2).

## Scope / not yet here

- Gmail, X (need collect-only + reap-strictly-after-push hardening — Phase 2).
- PDF via Drive API, Obsidian vault read-only clone + ledger — Phase 2.
- `raw/_pending/youtube/` hand-off + slim Mac feeder — Phase 3.
- Retiring the local `com.corpus.daily` job — Phase 4 (keep it running until the
  cloud loop is trusted; both are idempotent, so an overlap night is harmless —
  the ledger and source-state dedup prevent double-collection).
````

- [ ] **Step 2: Commit**

```bash
git add docs/cloud-nightly-runbook.md
git commit -m "docs(cloud-run): Phase 1 operator runbook (routine prompt, GH_TOKEN, reading a run)"
```

---

## Phase-1 exit check

- [ ] `python3 -m pytest tests/test_cloud_run.py -q` → all green (Phase-0 three + Task-1 three + Task-2 five).
- [ ] `python3 bin/cloud_run.py --dry-run | python3 -m json.tool` → unchanged 6-step plan (smoke-test routine still works).
- [ ] `python3 bin/cloud_run.py collect --only github` → prints `{"collected": {"github": …}}` (locally this actually runs the collector; that's fine — it dedups via the ledger).
- [ ] `python3 bin/cloud_run.py commit-push --repo .` on a clean `main` → `{"status": "noop"}`, exit 0.
- [ ] `docs/cloud-nightly-runbook.md` exists with the routine prompt + `GH_TOKEN`/`SCHEDULED_RUN_INGEST_MODEL` secrets.

## What Phase 1 deliberately does NOT do (later plans)

- Gmail + X collectors in the cloud, **with** the collect-only / reap-strictly-after-push
  hardening that the ephemeral inbox requires → **Phase 2 plan** (with Drive + vault).
- PDF via Drive API; Obsidian read-only vault clone + `obsidian_digested.txt` ledger → **Phase 2**.
- `raw/_pending/youtube/` queue + slim Mac feeder + cloud drain/clear → **Phase 3**.
- Email failure-alerts; decommissioning the local `com.corpus.daily` job → **Phase 4**.

## User one-time setup (already in progress)

The routine, the `GH_TOKEN` secret, "allow unrestricted branch pushes", and keeping the
repo pushed are the user's cloud-side steps (spec §9). The Phase-0 dry-run smoke test
validates billing + clone + Python before this phase's live `collect`/`commit-push` are
wired into the routine prompt.

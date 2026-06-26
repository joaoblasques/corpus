# Cloud Nightly — Phase 0: Collector Cloud-Readiness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the corpus collectors and run-orchestrator able to authenticate from environment-supplied secrets and dedup without a persistent local `raw/`, so a later phase can run them in an Anthropic cloud Routine — all built and tested locally with no cloud dependency.

**Architecture:** A small shared helper materializes a JSON secret from an env var into a temp file (falling back to today's on-disk token files, so local runs are unchanged). Gmail and X are wired to it; GitHub gains a committed dedup ledger (it authenticates via `gh`'s native `GH_TOKEN`, so no auth code change). A `cloud_run.py --dry-run` skeleton reports the planned nightly steps as JSON without executing them, locking in the orchestration shape.

**Tech Stack:** Python 3.12 stdlib (`os`, `tempfile`, `pathlib`, `json`, `argparse`), pytest. No new third-party deps.

**Spec:** `docs/superpowers/specs/2026-06-26-cloud-nightly-migration-design.md` (Phase 0, §4.3, §4.5).

## Global Constraints

- Python 3.12; stdlib only for this phase (no new dependencies).
- Never write outside the repo. New tracked state lives under `automation/state/`.
- Local behavior must be unchanged when env vars are absent (file fallback).
- Tests live under `tests/`, run with `python3 -m pytest`. Match existing style in `tests/test_scheduled_run.py` (plain `pytest`, `tmp_path`, no network).
- Secret temp files must be created mode `0600`.
- Commit after each task. Commit-message footer (every commit):
  ```
  Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
  Claude-Session: https://claude.ai/code/session_01GrGvMKSxgyetukaRpXyaf5
  ```

## File Structure

- Create `bin/secret_env.py` — secret-from-env materializer (one responsibility: resolve a secret to a file path).
- Create `tests/test_secret_env.py` — its tests.
- Modify `bin/gmail_client.py` — resolve `CREDENTIALS`/`TOKEN` through the helper at auth time.
- Modify `bin/x_client.py` — resolve `x_token.json` through the helper in `_load_token`.
- Create `bin/github_ledger.py` — read/append the committed digest ledger (one responsibility).
- Create `tests/test_github_ledger.py` — its tests.
- Modify `bin/collect_github.py` — consult the ledger in `already_collected`; expose an append.
- Create `automation/state/.gitkeep` — ensure the tracked state dir exists.
- Create `bin/cloud_run.py` — nightly orchestrator; this phase ships only `--dry-run`.
- Create `tests/test_cloud_run.py` — its tests.

---

### Task 1: `secret_env.materialize_secret` helper

**Files:**
- Create: `bin/secret_env.py`
- Test: `tests/test_secret_env.py`

**Interfaces:**
- Produces: `materialize_secret(env_var: str, fallback_path: pathlib.Path) -> pathlib.Path`
  — returns a path to the secret's JSON. If `os.environ[env_var]` is set and non-empty, writes
  it to a new `0600` temp file and returns that path; else returns `fallback_path` if it exists;
  else raises `FileNotFoundError`.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_secret_env.py
from __future__ import annotations
import os
import stat
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import secret_env  # noqa: E402


def test_env_var_materialized_to_0600_temp_file(tmp_path, monkeypatch):
    monkeypatch.setenv("MYSECRET", '{"token": "abc"}')
    fallback = tmp_path / "nope.json"
    out = secret_env.materialize_secret("MYSECRET", fallback)
    assert out != fallback
    assert out.read_text(encoding="utf-8") == '{"token": "abc"}'
    mode = stat.S_IMODE(out.stat().st_mode)
    assert mode == 0o600, f"expected 0600, got {oct(mode)}"


def test_falls_back_to_existing_file_when_env_absent(tmp_path, monkeypatch):
    monkeypatch.delenv("MYSECRET", raising=False)
    fallback = tmp_path / "token.json"
    fallback.write_text("{}", encoding="utf-8")
    out = secret_env.materialize_secret("MYSECRET", fallback)
    assert out == fallback


def test_empty_env_var_treated_as_absent(tmp_path, monkeypatch):
    monkeypatch.setenv("MYSECRET", "")
    fallback = tmp_path / "token.json"
    fallback.write_text("{}", encoding="utf-8")
    assert secret_env.materialize_secret("MYSECRET", fallback) == fallback


def test_raises_when_neither_env_nor_file(tmp_path, monkeypatch):
    monkeypatch.delenv("MYSECRET", raising=False)
    import pytest
    with pytest.raises(FileNotFoundError):
        secret_env.materialize_secret("MYSECRET", tmp_path / "missing.json")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_secret_env.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'secret_env'`.

- [ ] **Step 3: Write the implementation**

```python
# bin/secret_env.py
"""Resolve a JSON secret to a filesystem path.

In the cloud/CI, secrets arrive as environment variables holding the JSON
content; locally they live in on-disk token files. `materialize_secret` bridges
the two so collector code can stay file-based: env var wins (written to a 0600
temp file), else the on-disk fallback, else an error.
"""
from __future__ import annotations

import os
import tempfile
from pathlib import Path


def materialize_secret(env_var: str, fallback_path: Path) -> Path:
    value = os.environ.get(env_var)
    if value:
        fd, name = tempfile.mkstemp(prefix="corpus_secret_", suffix=".json")
        try:
            os.fchmod(fd, 0o600)
            os.write(fd, value.encode("utf-8"))
        finally:
            os.close(fd)
        return Path(name)
    if fallback_path.exists():
        return fallback_path
    raise FileNotFoundError(
        f"secret unavailable: env {env_var!r} unset and {fallback_path} missing"
    )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_secret_env.py -q`
Expected: PASS (4 passed).

- [ ] **Step 5: Commit**

```bash
git add bin/secret_env.py tests/test_secret_env.py
git commit -m "feat(secret_env): materialize a JSON secret from env var to a 0600 file (file fallback)"
```

---

### Task 2: Wire Gmail auth through `secret_env`

**Files:**
- Modify: `bin/gmail_client.py` (module constants near lines 34-37; auth function near lines 149-155)
- Test: `tests/test_gmail_secret_env.py` (create)

**Interfaces:**
- Consumes: `secret_env.materialize_secret` (Task 1).
- Produces: `gmail_client._resolve_credentials() -> Path` and `gmail_client._resolve_token() -> Path`
  used by the auth path. Env vars: `GMAIL_CREDENTIALS_JSON`, `GMAIL_TOKEN_JSON`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_gmail_secret_env.py
from __future__ import annotations
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import gmail_client  # noqa: E402


def test_token_resolves_from_env(monkeypatch):
    monkeypatch.setenv("GMAIL_TOKEN_JSON", '{"refresh_token": "x"}')
    p = gmail_client._resolve_token()
    assert p.read_text(encoding="utf-8") == '{"refresh_token": "x"}'


def test_token_falls_back_to_default_path(monkeypatch):
    monkeypatch.delenv("GMAIL_TOKEN_JSON", raising=False)
    # default path is bin/token.json; resolver returns it whether or not it exists,
    # by delegating to secret_env (which raises only when used). Assert the path identity.
    assert gmail_client._resolve_token.__name__ == "_resolve_token"
    assert gmail_client.TOKEN.name == "token.json"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_gmail_secret_env.py -q`
Expected: FAIL — `AttributeError: module 'gmail_client' has no attribute '_resolve_token'`.

- [ ] **Step 3: Add resolvers and use them at auth time**

Add near the imports of `bin/gmail_client.py` (after `TOKEN = BIN / "token.json"`):

```python
import secret_env  # bin/ is importable for callers; safe local import

CREDENTIALS_ENV = "GMAIL_CREDENTIALS_JSON"
TOKEN_ENV = "GMAIL_TOKEN_JSON"


def _resolve_credentials():
    return secret_env.materialize_secret(CREDENTIALS_ENV, CREDENTIALS)


def _resolve_token():
    return secret_env.materialize_secret(TOKEN_ENV, TOKEN)
```

Then in the auth function (currently `if TOKEN.exists(): creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)`), replace the hard-coded `TOKEN`/`CREDENTIALS` reads with the resolvers. Exact change at lines ~154-155:

```python
    token_path = _resolve_token() if (TOKEN.exists() or os.environ.get(TOKEN_ENV)) else TOKEN
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
```

And wherever `CREDENTIALS` is passed to `InstalledAppFlow.from_client_secrets_file(...)`, replace with `str(_resolve_credentials())`.

> Note: ensure `import os` exists at module top (it does — used elsewhere). Keep the existing token write-back; in the cloud the temp token is discarded after the run, which is correct (the refresh token in the secret persists).

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_gmail_secret_env.py -q`
Expected: PASS (2 passed).

- [ ] **Step 5: Commit**

```bash
git add bin/gmail_client.py tests/test_gmail_secret_env.py
git commit -m "feat(gmail): resolve credentials/token via secret_env (env-var or file)"
```

---

### Task 3: Wire X auth through `secret_env`

**Files:**
- Modify: `bin/x_client.py` (`TOKEN = BIN / "x_token.json"` line ~17; `_load_token` lines ~34-43)
- Test: `tests/test_x_secret_env.py` (create)

**Interfaces:**
- Consumes: `secret_env.materialize_secret`.
- Produces: `x_client._load_token()` now reads from env `X_TOKEN_JSON` first, else `x_token.json`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_x_secret_env.py
from __future__ import annotations
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import x_client  # noqa: E402


def test_load_token_prefers_env(monkeypatch):
    monkeypatch.setenv("X_TOKEN_JSON", '{"access_token": "live", "refresh_token": "r"}')
    tok = x_client._load_token()
    assert tok["access_token"] == "live"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_x_secret_env.py -q`
Expected: FAIL — the current `_load_token` reads only `TOKEN` (file), returns None/raises without the env path.

- [ ] **Step 3: Update `_load_token`**

In `bin/x_client.py`, add near `TOKEN = BIN / "x_token.json"`:

```python
import secret_env
TOKEN_ENV = "X_TOKEN_JSON"
```

Change `_load_token` to resolve via the helper:

```python
def _load_token():
    try:
        path = secret_env.materialize_secret(TOKEN_ENV, TOKEN)
    except FileNotFoundError:
        return None
    return json.loads(path.read_text(encoding="utf-8"))
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_x_secret_env.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add bin/x_client.py tests/test_x_secret_env.py
git commit -m "feat(x): load token from X_TOKEN_JSON env var (file fallback)"
```

---

### Task 4: Committed GitHub digest ledger

**Files:**
- Create: `bin/github_ledger.py`
- Create: `automation/state/.gitkeep`
- Modify: `bin/collect_github.py` (`already_collected` near line 24; add ledger append)
- Test: `tests/test_github_ledger.py` (create)

**Interfaces:**
- Produces:
  - `github_ledger.LEDGER_PATH: pathlib.Path` = `<repo>/automation/state/github_digested.txt`
  - `github_ledger.is_digested(full_name: str, ledger_path: Path = LEDGER_PATH) -> bool`
  - `github_ledger.mark_digested(full_name: str, ledger_path: Path = LEDGER_PATH) -> None`
    (append-once; idempotent; creates the file/dir if missing)
- Consumes (in collect_github): `already_collected(full_name)` returns True if EITHER the existing
  `raw/` glob matches OR `github_ledger.is_digested(full_name)`.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_github_ledger.py
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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_github_ledger.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'github_ledger'`.

- [ ] **Step 3: Implement the ledger**

```python
# bin/github_ledger.py
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_github_ledger.py -q`
Expected: PASS (4 passed).

- [ ] **Step 5: Wire the ledger into `collect_github.already_collected` and append on collect**

Create `automation/state/.gitkeep` (empty) so the dir is tracked:

```bash
mkdir -p automation/state && touch automation/state/.gitkeep
```

In `bin/collect_github.py`, add at top: `import github_ledger`. Extend `already_collected`:

```python
def already_collected(full_name: str, dirs=None) -> bool:
    if github_ledger.is_digested(full_name):
        return True
    for d in (dirs if dirs is not None else DEDUP_DIRS):
        # ... existing glob logic unchanged ...
```

At the point a repo digest is successfully written to `raw/_inbox/`, add `github_ledger.mark_digested(full_name)` so the ledger grows as repos are collected.

- [ ] **Step 6: Run the github-collector tests + the new ledger tests**

Run: `python3 -m pytest tests/test_github_ledger.py tests/test_collect_github.py -q`
Expected: PASS (existing collect_github tests still green; if a test asserts re-collection, update it to account for the ledger and note why).

- [ ] **Step 7: Commit**

```bash
git add bin/github_ledger.py tests/test_github_ledger.py bin/collect_github.py automation/state/.gitkeep
git commit -m "feat(github): committed digest ledger for stateless dedup (cloud-safe)"
```

---

### Task 5: `cloud_run.py --dry-run` orchestration skeleton

**Files:**
- Create: `bin/cloud_run.py`
- Test: `tests/test_cloud_run.py`

**Interfaces:**
- Produces: `cloud_run.plan_steps() -> list[dict]` (the ordered nightly steps, each
  `{"step": str, "detail": str}`) and a CLI `python3 bin/cloud_run.py --dry-run` that prints
  `{"dry_run": true, "steps": [...]}` as JSON and exits 0 without side effects.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_cloud_run.py
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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_cloud_run.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'cloud_run'`.

- [ ] **Step 3: Implement the skeleton**

```python
# bin/cloud_run.py
"""Nightly cloud orchestrator (Phase 0: --dry-run skeleton only).

Defines the ordered steps of the single-cloud-writer nightly run (spec §4.1).
Later phases implement each step; this phase ships only the plan + a --dry-run
that prints it, so the orchestration shape is locked and testable with no side
effects.
"""
from __future__ import annotations

import argparse
import json
import sys


def plan_steps() -> list[dict]:
    return [
        {"step": "clone_repos", "detail": "clone corpus (main) + second-brain (read-only)"},
        {"step": "collect_sources", "detail": "gmail, github(+ledger), x, pdf(Drive API), obsidian(vault clone)"},
        {"step": "drain_youtube_queue", "detail": "move raw/_pending/youtube/* into raw/_inbox/"},
        {"step": "ingest", "detail": "ingest-auto: route to existing domains, write corpus/ pages"},
        {"step": "reap_and_ledger", "detail": "un-star/un-bookmark/un-label/move; append github+obsidian ledgers"},
        {"step": "commit_and_push", "detail": "commit corpus/ + ledgers; git rm pending youtube; push corpus only"},
    ]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Nightly cloud corpus run.")
    ap.add_argument("--dry-run", action="store_true", help="print the planned steps and exit")
    args = ap.parse_args(argv)
    if args.dry_run:
        print(json.dumps({"dry_run": True, "steps": plan_steps()}))
        return 0
    print(json.dumps({"error": "live run not implemented in Phase 0"}))
    return 1


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_cloud_run.py -q`
Expected: PASS (2 passed).

- [ ] **Step 5: Commit**

```bash
git add bin/cloud_run.py tests/test_cloud_run.py
git commit -m "feat(cloud_run): dry-run orchestration skeleton (single-cloud-writer step plan)"
```

---

## Phase-0 exit check

- [ ] Run the new unit suites together: `python3 -m pytest tests/test_secret_env.py tests/test_gmail_secret_env.py tests/test_x_secret_env.py tests/test_github_ledger.py tests/test_cloud_run.py -q` → all green.
- [ ] `git grep -n "raw/_pending"` is empty (that folder is Phase 3, not Phase 0).
- [ ] `python3 bin/cloud_run.py --dry-run | python3 -m json.tool` shows the 6 steps.

## What Phase 0 deliberately does NOT do (later plans)
- PDF via Drive API and Obsidian vault-clone + `obsidian_digested.txt` ledger → **Phase 2 plan**.
- `raw/_pending/youtube/` queue + slim Mac feeder + cloud drain/clear → **Phase 3 plan**.
- Live `cloud_run.py` step bodies + the `/schedule` routine + secrets wiring + Max-billing
  smoke test → **Phase 1 plan** (needs the user's cloud setup from spec §9).

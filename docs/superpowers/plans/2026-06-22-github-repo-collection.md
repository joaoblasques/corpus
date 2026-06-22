# GitHub Repo Collection Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Collect the user's starred GitHub repos (README + markdown docs + a metadata overview) into the corpus as one "repo digest" per repo, deduped, leaving stars in place; wired into the 2 AM job.

**Architecture:** A new collector mirroring the others — `bin/collect_github.py` (pure logic: dedup, document build) + `bin/github_client.py` (CLI driver; all GitHub I/O via the `gh` CLI through an injectable subprocess seam) — drained by the normal nightly ingest. Spec: `docs/superpowers/specs/2026-06-22-github-repo-collection-design.md`.

**Tech Stack:** Python 3.12, pytest, stdlib + the `gh` CLI. Tests under `tests/` (prepend `bin/` to `sys.path`); all `gh`/subprocess effects injected (`_run`) — no network.

## Global Constraints

- Files: `bin/collect_github.py`, `bin/github_client.py`; tests `tests/test_collect_github.py`, `tests/test_github_client.py`.
- Channel = `github`; source files → `raw/_inbox`, dedup against `raw/_inbox` + `raw/github`.
- **Dedup key:** the frontmatter `repo: <owner/name>` line. Never re-collect an already-collected repo.
- **Leave stars in place** — the collector must NEVER call any star-mutating endpoint (no `PUT`/`DELETE user/starred`).
- Auth via `gh` (already authenticated); if `gh auth status` fails → report `not configured`, skip gracefully.
- Truncation caps: README ~40 KB, each doc ~15 KB, at most `--max-docs` (default 8) docs.
- `gh` is invoked as `["gh", ...]` through `_run` (default `subprocess.run`, `capture_output=True, text=True`).

---

### Task 1: `collect_github.py` — pure logic (dedup + document)

**Files:** Create `bin/collect_github.py`; Test `tests/test_collect_github.py`.

**Interfaces:**
- Produces: `slugify(full_name)->str`, `already_collected(full_name, dirs=None)->bool`, `build_document(repo: dict, *, collected_at)->str`, `write_collected(repo, *, collected_at, inbox=None, dedup_dirs=None)->dict`, `DEDUP_DIRS`. `repo` dict keys: `full_name, html_url, description, language, stars, topics(list), latest_release, readme, docs(list of {path,text})`.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_collect_github.py`:
```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import collect_github as cg  # noqa: E402

REPO = {"full_name": "anthropics/claude-code", "html_url": "https://github.com/anthropics/claude-code",
        "description": "Agentic coding: tasks & PRs", "language": "TypeScript", "stars": 1234,
        "topics": ["agents", "cli"], "latest_release": "v2.0.1",
        "readme": "# Claude Code\nDoes things.", "docs": [{"path": "docs/x.md", "text": "Doc body"}]}


def test_slugify():
    assert cg.slugify("anthropics/claude-code") == "github-anthropics-claude-code"
    assert cg.slugify("d4vinci/Scrapling") == "github-d4vinci-scrapling"


def test_build_document_has_frontmatter_and_sections():
    doc = cg.build_document(REPO, collected_at="2026-06-22")
    assert "channel: github" in doc and "repo: anthropics/claude-code" in doc
    assert "stars: 1234" in doc and "latest_release: v2.0.1" in doc
    assert "topics: [agents, cli]" in doc
    assert "## README" in doc and "Does things." in doc
    assert "## Docs" in doc and "### docs/x.md" in doc and "Doc body" in doc


def test_build_document_tolerates_missing_pieces():
    doc = cg.build_document({"full_name": "a/b"}, collected_at="2026-06-22")
    assert "repo: a/b" in doc and "## README" in doc and "stars: 0" in doc


def test_write_collected_writes_then_dedups(tmp_path):
    d = tmp_path / "_inbox"
    r1 = cg.write_collected(REPO, collected_at="2026-06-22", inbox=d, dedup_dirs=[d])
    assert r1["status"] == "written" and Path(r1["path"]).name == "github-anthropics-claude-code.md"
    r2 = cg.write_collected(REPO, collected_at="2026-06-22", inbox=d, dedup_dirs=[d])
    assert r2["status"] == "duplicate"   # dedup by repo: full-name


def test_already_collected_matches_frontmatter_repo_line(tmp_path):
    d = tmp_path / "_inbox"; d.mkdir()
    (d / "x.md").write_text("---\nchannel: github\nrepo: owner/name\n---\nbody", encoding="utf-8")
    assert cg.already_collected("owner/name", dirs=[d]) is True
    assert cg.already_collected("owner/other", dirs=[d]) is False
```

- [ ] **Step 2: Run to verify they fail**

Run: `python3 -m pytest tests/test_collect_github.py -q`
Expected: FAIL (`No module named collect_github`).

- [ ] **Step 3: Implement**

Create `bin/collect_github.py`:
```python
#!/usr/bin/env python3
"""collect_github.py — pure logic for the GitHub repo collector.

Builds one "repo digest" markdown source per starred repo (README + docs + a metadata
overview) and dedups by the frontmatter `repo:` full-name. Network I/O lives in
github_client.py. Spec: docs/superpowers/specs/2026-06-22-github-repo-collection-design.md
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "raw" / "_inbox"
DEDUP_DIRS = [ROOT / "raw" / "_inbox", ROOT / "raw" / "github"]
_REPO_RE = re.compile(r"^repo:\s*(\S+)\s*$", re.M)


def slugify(full_name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", full_name.lower()).strip("-")
    return f"github-{s}"


def already_collected(full_name: str, dirs=None) -> bool:
    for d in (dirs if dirs is not None else DEDUP_DIRS):
        p = Path(d)
        if not p.exists():
            continue
        for md in p.glob("*.md"):
            try:
                head = md.read_text(encoding="utf-8", errors="ignore")[:1500]
            except OSError:
                continue
            m = _REPO_RE.search(head)
            if m and m.group(1) == full_name:
                return True
    return False


def _scalar(s) -> str:
    s = (str(s) if s is not None else "").replace("\n", " ").strip()
    if s and (any(c in s for c in ":#") or s[0] in "\"'[{-@`"):
        return '"' + s.replace('"', '\\"') + '"'
    return s


def build_document(repo: dict, *, collected_at: str) -> str:
    fn = repo["full_name"]
    topics = repo.get("topics") or []
    rel = repo.get("latest_release") or ""
    stars = int(repo.get("stars") or 0)
    desc = repo.get("description") or ""
    lang = repo.get("language") or ""
    lines = [
        "---", "channel: github", "source: github",
        f"repo: {fn}",
        f"repo_url: {repo.get('html_url') or ('https://github.com/' + fn)}",
        f"description: {_scalar(desc)}",
        f"language: {lang}",
        f"stars: {stars}",
        f"topics: [{', '.join(topics)}]",
        f"latest_release: {rel}",
        f"collected_at: {collected_at}",
        "---", "",
        f"# {fn}",
        "> " + " · ".join(filter(None, [
            desc, lang, f"★{stars}",
            (f"latest {rel}" if rel else ""),
            (f"topics: {', '.join(topics)}" if topics else ""),
        ])),
        "", "## README", (repo.get("readme") or "").strip(),
    ]
    docs = repo.get("docs") or []
    if docs:
        lines.append("\n## Docs")
        for d in docs:
            lines += [f"### {d.get('path', '')}", (d.get("text") or "").strip(), ""]
    return "\n".join(lines) + "\n"


def write_collected(repo: dict, *, collected_at: str, inbox=None, dedup_dirs=None) -> dict:
    fn = repo["full_name"]
    if already_collected(fn, dedup_dirs):
        return {"status": "duplicate", "path": None}
    ib = Path(inbox) if inbox is not None else INBOX
    ib.mkdir(parents=True, exist_ok=True)
    path = ib / f"{slugify(fn)}.md"
    path.write_text(build_document(repo, collected_at=collected_at), encoding="utf-8")
    return {"status": "written", "path": str(path)}
```

- [ ] **Step 4: Run to verify pass** — `python3 -m pytest tests/test_collect_github.py -q` → PASS (5 tests).

- [ ] **Step 5: Commit**
```bash
git add bin/collect_github.py tests/test_collect_github.py
git commit -m "feat(collect-github): pure logic — dedup + repo-digest document"
```

---

### Task 2: `github_client.py` — gh helpers (list + fetch)

**Files:** Create `bin/github_client.py`; Test `tests/test_github_client.py`.

**Interfaces:**
- Produces: `gh_available(*, _run=None)->bool`, `list_starred(max_n=None, *, _run=None)->list[dict]`, `fetch_repo(repo_item: dict, *, max_docs=8, _run=None)->dict`. `_run` mocks `subprocess.run` (returns an object with `.returncode`, `.stdout`).

- [ ] **Step 1: Write the failing tests**

Create `tests/test_github_client.py`:
```python
import base64
import json
import sys
import types
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import github_client as gh  # noqa: E402


def _proc(rc=0, stdout=""):
    return types.SimpleNamespace(returncode=rc, stdout=stdout, stderr="")


def _b64(s):
    return base64.b64encode(s.encode()).decode()


def test_gh_available():
    assert gh.gh_available(_run=lambda *a, **k: _proc(0)) is True
    assert gh.gh_available(_run=lambda *a, **k: _proc(1)) is False


def test_list_starred_parses_and_caps():
    data = [{"full_name": "a/b", "html_url": "u", "description": "d", "language": "Py",
             "stargazers_count": 5, "topics": ["t"], "default_branch": "main"},
            {"full_name": "c/d", "stargazers_count": 1}]
    run = lambda cmd, **k: _proc(0, json.dumps(data))
    out = gh.list_starred(_run=run)
    assert [r["full_name"] for r in out] == ["a/b", "c/d"]
    assert out[0]["stars"] == 5 and out[0]["topics"] == ["t"]
    assert gh.list_starred(max_n=1, _run=run)[0]["full_name"] == "a/b" and len(gh.list_starred(max_n=1, _run=run)) == 1


def test_fetch_repo_assembles_readme_docs_release():
    item = {"full_name": "a/b", "stars": 5}
    def run(cmd, **k):
        ep = cmd[2]  # ["gh","api","<endpoint>",...]
        if ep == "repos/a/b/readme":
            return _proc(0, json.dumps({"content": _b64("# Title\nbody")}))
        if ep == "repos/a/b/releases/latest":
            return _proc(0, json.dumps({"tag_name": "v1.2"}))
        if ep == "repos/a/b/contents":
            return _proc(0, json.dumps([{"name": "README.md", "path": "README.md", "content": _b64("x")},
                                        {"name": "CONTRIBUTING.md", "path": "CONTRIBUTING.md", "content": _b64("contrib")}]))
        if ep == "repos/a/b/contents/docs":
            return _proc(1, "")   # no docs folder
        return _proc(1, "")
    repo = gh.fetch_repo(item, _run=run)
    assert repo["readme"].startswith("# Title") and repo["latest_release"] == "v1.2"
    assert [d["path"] for d in repo["docs"]] == ["CONTRIBUTING.md"]   # README excluded
    assert repo["stars"] == 5   # metadata carried through from the item


def test_fetch_repo_tolerates_missing_pieces():
    repo = gh.fetch_repo({"full_name": "a/b"}, _run=lambda *a, **k: _proc(1, ""))
    assert repo["readme"] == "" and repo["latest_release"] == "" and repo["docs"] == []
```

- [ ] **Step 2: Run to verify they fail** — `python3 -m pytest tests/test_github_client.py -q` → FAIL (`No module named github_client`).

- [ ] **Step 3: Implement**

Create `bin/github_client.py`:
```python
#!/usr/bin/env python3
"""github_client.py — GitHub transport for the repo collector (via the `gh` CLI).

Lists the user's starred repos and fetches README + markdown docs + a metadata overview.
Leaves stars in place. All `gh` calls go through an injectable subprocess seam.
"""
from __future__ import annotations

import base64
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import collect_github as cg  # noqa: E402

README_CAP = 40_000
DOC_CAP = 15_000


def _gh(api_args, *, _run=None):
    run = _run if _run is not None else subprocess.run
    return run(["gh"] + api_args, capture_output=True, text=True)


def gh_available(*, _run=None) -> bool:
    try:
        return getattr(_gh(["auth", "status"], _run=_run), "returncode", 1) == 0
    except Exception:  # noqa: BLE001
        return False


def list_starred(max_n=None, *, _run=None) -> list:
    p = _gh(["api", "user/starred", "--paginate"], _run=_run)
    if getattr(p, "returncode", 1) != 0:
        return []
    try:
        data = json.loads(p.stdout)
    except Exception:  # noqa: BLE001
        return []
    out = []
    for it in data if isinstance(data, list) else []:
        out.append({
            "full_name": it.get("full_name"), "html_url": it.get("html_url"),
            "description": it.get("description") or "", "language": it.get("language") or "",
            "stars": it.get("stargazers_count") or 0, "topics": it.get("topics") or [],
            "default_branch": it.get("default_branch") or "main",
        })
        if max_n and len(out) >= max_n:
            break
    return out


def _decode(content) -> str:
    try:
        return base64.b64decode(content or "").decode("utf-8", "replace")
    except Exception:  # noqa: BLE001
        return ""


def _readme(full_name, _run) -> str:
    p = _gh(["api", f"repos/{full_name}/readme"], _run=_run)
    if getattr(p, "returncode", 1) != 0:
        return ""
    try:
        return _decode(json.loads(p.stdout).get("content"))[:README_CAP]
    except Exception:  # noqa: BLE001
        return ""


def _latest_release(full_name, _run) -> str:
    p = _gh(["api", f"repos/{full_name}/releases/latest"], _run=_run)
    if getattr(p, "returncode", 1) != 0:
        return ""
    try:
        return json.loads(p.stdout).get("tag_name") or ""
    except Exception:  # noqa: BLE001
        return ""


def _docs(full_name, max_docs, _run) -> list:
    out = []
    for sub in ("", "docs"):
        ep = f"repos/{full_name}/contents" + (f"/{sub}" if sub else "")
        p = _gh(["api", ep], _run=_run)
        if getattr(p, "returncode", 1) != 0:
            continue
        try:
            items = json.loads(p.stdout)
        except Exception:  # noqa: BLE001
            continue
        if not isinstance(items, list):
            continue
        for it in items:
            name = (it.get("name") or "")
            if not name.lower().endswith(".md"):
                continue
            if sub == "" and name.lower() == "readme.md":
                continue
            text = _decode(it.get("content")) if it.get("content") else ""
            if not text and it.get("url"):
                fp = _gh(["api", it["url"]], _run=_run)
                if getattr(fp, "returncode", 1) == 0:
                    try:
                        text = _decode(json.loads(fp.stdout).get("content"))
                    except Exception:  # noqa: BLE001
                        text = ""
            if text:
                out.append({"path": it.get("path") or name, "text": text[:DOC_CAP]})
            if len(out) >= max_docs:
                return out
    return out


def fetch_repo(repo_item: dict, *, max_docs=8, _run=None) -> dict:
    fn = repo_item["full_name"]
    return {**repo_item,
            "latest_release": _latest_release(fn, _run),
            "readme": _readme(fn, _run),
            "docs": _docs(fn, max_docs, _run)}
```

- [ ] **Step 4: Run to verify pass** — `python3 -m pytest tests/test_github_client.py -q` → PASS (4 tests).

- [ ] **Step 5: Commit**
```bash
git add bin/github_client.py tests/test_github_client.py
git commit -m "feat(github): gh helpers — gh_available, list_starred, fetch_repo"
```

---

### Task 3: `github_client.py` — `cmd_run` + CLI

**Files:** Modify `bin/github_client.py`; Modify `tests/test_github_client.py`.

**Interfaces:**
- Consumes: `gh_available`, `list_starred`, `fetch_repo`, `cg.already_collected`, `cg.write_collected`.
- Produces: `cmd_run(args)->int`, `cmd_list(args)->int`, `cmd_auth(args)->int`, `_build_parser()`, `_args(argv)`, `main(argv=None)->int`. `run` subcommand args: `--max`, `--max-docs` (default 8), `--dry-run`, `--collected-at`.

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_github_client.py`:
```python
def test_cmd_run_skips_when_gh_unavailable(monkeypatch, capsys):
    monkeypatch.setattr(gh, "gh_available", lambda **k: False)
    rc = gh.cmd_run(gh._args(["run"]))
    assert rc == 0 and "not configured" in capsys.readouterr().out


def test_cmd_run_collects_new_repos_only_no_unstar(monkeypatch, capsys):
    monkeypatch.setattr(gh, "gh_available", lambda **k: True)
    monkeypatch.setattr(gh, "list_starred", lambda mx=None, **k: [{"full_name": "a/b"}, {"full_name": "c/d"}])
    monkeypatch.setattr(gh.cg, "already_collected", lambda fn, dirs=None: fn == "a/b")  # a/b already in corpus
    monkeypatch.setattr(gh, "fetch_repo", lambda item, **k: {**item, "readme": "r"})
    written = []
    monkeypatch.setattr(gh.cg, "write_collected",
                        lambda repo, **k: written.append(repo["full_name"]) or {"status": "written", "path": "/x.md"})
    gh_calls = []
    monkeypatch.setattr(gh, "_gh", lambda args, **k: gh_calls.append(args) or _proc(0))
    rc = gh.cmd_run(gh._args(["run"]))
    out = capsys.readouterr().out
    assert rc == 0 and '"written": 1' in out and written == ["c/d"]   # a/b skipped (dup)
    assert not any("DELETE" in str(a) or "PUT" in str(a) for a in gh_calls)   # never un-stars


def test_cmd_run_dry_run_writes_nothing(monkeypatch, capsys):
    monkeypatch.setattr(gh, "gh_available", lambda **k: True)
    monkeypatch.setattr(gh, "list_starred", lambda mx=None, **k: [{"full_name": "c/d"}])
    monkeypatch.setattr(gh.cg, "already_collected", lambda fn, dirs=None: False)
    wrote = []
    monkeypatch.setattr(gh.cg, "write_collected", lambda *a, **k: wrote.append(1))
    rc = gh.cmd_run(gh._args(["run", "--dry-run"]))
    assert rc == 0 and wrote == [] and '"dry_run": true' in capsys.readouterr().out
```

- [ ] **Step 2: Run to verify they fail** — `python3 -m pytest tests/test_github_client.py -k cmd_run -q` → FAIL (`cmd_run`/`_args` not defined).

- [ ] **Step 3: Implement** — append to `bin/github_client.py`:
```python
import argparse  # noqa: E402
import datetime  # noqa: E402


def cmd_auth(args) -> int:
    print(json.dumps({"gh_available": gh_available()}))
    return 0


def cmd_list(args) -> int:
    print(json.dumps([r["full_name"] for r in list_starred(args.max)], indent=2))
    return 0


def cmd_run(args) -> int:
    if not gh_available():
        print(json.dumps({"status": "not configured", "reason": "gh not authed"}))
        return 0
    at = args.collected_at or datetime.date.today().isoformat()
    repos = list_starred(args.max)
    found = written = dup = failed = candidates = 0
    paths = []
    for item in repos:
        found += 1
        fn = item.get("full_name")
        if not fn or cg.already_collected(fn):
            dup += 1
            continue
        candidates += 1
        if args.dry_run:
            continue
        try:
            res = cg.write_collected(fetch_repo(item, max_docs=args.max_docs), collected_at=at)
        except Exception:  # noqa: BLE001
            failed += 1
            continue
        if res.get("status") == "written":
            written += 1
            paths.append(res.get("path"))
        elif res.get("status") == "duplicate":
            dup += 1
        else:
            failed += 1
    print(json.dumps({"found": found, "written": written, "duplicate": dup, "failed": failed,
                      "candidates": candidates, "dry_run": bool(args.dry_run), "paths": paths}))
    return 0


def _build_parser():
    p = argparse.ArgumentParser(description="GitHub repo collector (starred repos via gh).")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("auth", help="Report gh auth status.").set_defaults(func=cmd_auth)
    pl = sub.add_parser("list-starred", help="Print starred repo full-names.")
    pl.add_argument("--max", type=int, default=None)
    pl.set_defaults(func=cmd_list)
    pr = sub.add_parser("run", help="Collect new starred repos (README + docs + overview).")
    pr.add_argument("--max", type=int, default=None, help="Cap repos this run.")
    pr.add_argument("--max-docs", type=int, default=8, help="Max doc files per repo.")
    pr.add_argument("--dry-run", action="store_true", help="List new candidates; write nothing.")
    pr.add_argument("--collected-at", default=None, help="Override YYYY-MM-DD stamp.")
    pr.set_defaults(func=cmd_run)
    return p


def _args(argv=None):
    return _build_parser().parse_args(argv)


def main(argv=None) -> int:
    args = _args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run to verify pass** — `python3 -m pytest tests/test_github_client.py -q` → PASS.

- [ ] **Step 5: Commit**
```bash
git add bin/github_client.py tests/test_github_client.py
git commit -m "feat(github): cmd_run + CLI (collect new stars, never un-star, --dry-run)"
```

---

### Task 4: Wire into the scheduled run

**Files:** Modify `bin/scheduled_run.py`; Modify `tests/test_scheduled_run.py`.

**Interfaces:**
- Consumes: `github_client.py run`.
- Produces: a `github` leg in `run_collectors` (`results["github"] = {"status","collected"}`); `_CHANNEL_DIR["github"] = "github"`.

- [ ] **Step 1: Write the failing test**

Append to `tests/test_scheduled_run.py`:
```python
class TestGithubCollector:
    def test_github_leg_invoked_and_channel_dir(self):
        assert scheduled_run._CHANNEL_DIR.get("github") == "github"
        called = []
        def fake_run(cmd, **kwargs):
            called.append(" ".join(cmd))
            import types
            return types.SimpleNamespace(returncode=0, stdout='{"written": 2}', stderr="")
        res = scheduled_run.run_collectors(_subprocess_run=fake_run)
        assert any("github_client.py" in s and "run" in s for s in called), called
        assert res["github"]["status"] == "ok" and res["github"]["collected"] == 2
```

- [ ] **Step 2: Run to verify it fails**

Run: `python3 -m pytest tests/test_scheduled_run.py -k github -v`
Expected: FAIL (no github leg; `_CHANNEL_DIR["github"]` unset). NOTE: confirm `run_collectors` accepts a `_subprocess_run` seam; if its existing legs use a different injection name, match it (read `run_collectors` first and mirror the gmail/pdf leg exactly).

- [ ] **Step 3: Implement**

In `bin/scheduled_run.py`:
1. Add `"github": "github"` to the `_CHANNEL_DIR` dict.
2. In `run_collectors`, after the pdf leg, add a github leg mirroring the pdf/gmail legs (same `_run`/isolation pattern the file uses):
```python
    # --- GitHub: collect new starred repos (README + docs + overview) ---
    try:
        proc = _run([sys.executable, str(BIN / "github_client.py"), "run"],
                    capture_output=True, text=True)
        n = 0
        try:
            n = int(json.loads(proc.stdout).get("written", 0))
        except (json.JSONDecodeError, AttributeError, TypeError, ValueError):
            n = 0
        results["github"] = ({"status": "ok", "collected": n} if proc.returncode == 0
                             else {"status": "failed", "collected": 0,
                                   "error": (proc.stderr or "").strip()[:200]})
    except Exception as exc:  # noqa: BLE001
        results["github"] = {"status": "failed", "collected": 0, "error": str(exc)}
```
(Use the file's actual `_run` seam variable name — match the surrounding gmail/pdf legs verbatim, including how `results` and `_run` are referenced.)

- [ ] **Step 4: Run to verify pass** — `python3 -m pytest tests/test_scheduled_run.py -k github -q` → PASS.

- [ ] **Step 5: Commit**
```bash
git add bin/scheduled_run.py tests/test_scheduled_run.py
git commit -m "feat(scheduled-run): github collector leg + raw/github channel dir"
```

---

### Task 5: Docs + full-suite gate

**Files:** Modify `corpus/_config.md`, `corpus/_log.md`.

- [ ] **Step 1: Document in `corpus/_config.md`** — add to the collectors/channels area:
```markdown
**GitHub repos (channel `github`):** the daily run collects the user's **starred** repos via
the `gh` CLI (`bin/github_client.py run`) — one "repo digest" per repo (README + markdown docs
+ a metadata overview: description, topics, language, stars, latest release). Deduped by the
frontmatter `repo: <owner/name>`; **stars are left in place** (a bookmark, not a queue).
Sources land in `raw/_inbox` (channel `github`), drain via the normal ingest, then move to
`raw/github`. No source code is collected. Auth: `gh` (skipped with `not configured` if unauthed).
```

- [ ] **Step 2: Append a `config` entry to `corpus/_log.md`**:
```markdown

## [2026-06-22 HH:MM] config | GitHub repo collection (starred repos)
- new collector: bin/collect_github.py + bin/github_client.py (gh CLI); wired into the 2am run
- collects starred repos as one repo-digest each (README + docs + overview), deduped by repo:,
  leaves stars in place; channel github -> raw/github. Spec: docs/superpowers/specs/2026-06-22-github-repo-collection-design.md
```
(Use the real current time for `HH:MM`.)

- [ ] **Step 3: Full-suite gate** — `python3 -m pytest tests/ -q` → all pass (github + the entire existing suite).

- [ ] **Step 4: Commit**
```bash
git add corpus/_config.md corpus/_log.md
git commit -m "docs(github): document starred-repo collection channel"
```

---

## Notes for the executor
- **Live check after merge (real `gh`):** `python3 bin/github_client.py list-starred --max 5` prints your starred repos; `python3 bin/github_client.py run --dry-run` lists which new ones it *would* collect (no writes). A real `run` writes repo digests to `raw/_inbox`.
- The collector NEVER mutates stars — confirm no `gh api ... -X PUT/DELETE user/starred` anywhere.
- Everything is injected (`_run`) — no test touches the network or real `gh`.

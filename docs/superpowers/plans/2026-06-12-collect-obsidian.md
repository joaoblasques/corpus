# Collect-Obsidian Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A `collect-obsidian` collector that copies reference-layer notes (and fetches URL-list links) from the user's Obsidian vault into `raw/_inbox/`, and — after they're ingested into the corpus — deletes the originals from the vault (git-recoverable, never auto-committed).

**Architecture:** A pure core (`bin/collect_obsidian.py`) holds path-policy filtering, URL-list parsing, source-frontmatter building, dedup, discovery, and the reaper selector. A thin I/O module (`bin/obsidian_client.py`) does the file copies, calls `fetch_link.fetch` for URLs, and reaps (vault `git rm` + list-file edits) — all behind `collect`/`reap` CLI subcommands with `--dry-run`. Removal is gated on the raw source being `corpus_ingested`.

**Tech Stack:** Python 3.12, PyYAML, httpx+trafilatura (via existing `fetch_link.py`), git, pytest. No new deps, no OAuth.

**Spec:** `docs/superpowers/specs/2026-06-12-obsidian-collector-design.md`

---

## File Structure

| File | Responsibility |
|---|---|
| `bin/collect_obsidian.py` *(new)* | Pure core: `is_included`, `classify`, `parse_url_list`, `read_note`, `build_note_source`, `build_url_source`, `note_filename`/`url_filename`, `fm_field`, `is_vault_note_ingested`, `already_collected_vault`, `url_already_collected`, `discover`, `reapable`. Reuses `slugify`/`yaml_scalar`/`URL_RE` from `collect_email`. |
| `bin/obsidian_client.py` *(new)* | I/O + CLI: `cmd_collect` (copy notes, fetch URL-list links via `fetch_link`), `cmd_reap` (vault `git rm`, strike+append list files), `_args`/`main`. |
| `.claude/skills/collect-obsidian/SKILL.md` *(new)* | Thin skill driving collect → ingest → reap. |
| `corpus/_config.md` *(modify)* | Add `vault_root` + include/exclude reference. |
| `CLAUDE.md` *(modify → v0.7)* | Vault-removal exception (§2 + §13 + §15 + log). |
| `tests/test_collect_obsidian.py` *(new)* | Pure-core tests (fixture vault under tmp_path). |
| `tests/test_obsidian_client.py` *(new)* | collect/reap tests (mock fetch_link + git). |

---

## Task 1: Path policy — `is_included` + `classify`

**Files:** Create `bin/collect_obsidian.py`; Test `tests/test_collect_obsidian.py`.

- [ ] **Step 1: Write failing tests**

Create `tests/test_collect_obsidian.py`:
```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import collect_obsidian as co  # noqa: E402


def test_is_included_resources():
    assert co.is_included("03_Resources/Articles/Clean Code.md") is True
    assert co.is_included("03_Resources/Study Notes/CAP.md") is True
    assert co.is_included("00_Inbox/Clippings/scrape/merkle-trees-scrape.md") is True


def test_is_included_excludes():
    assert co.is_included("03_Resources/llm-wiki-system/CLAUDE.md") is False  # corpus mirror
    assert co.is_included("01_Projects/foo.md") is False                      # not a knowledge dir
    assert co.is_included("00_Inbox/Clippings/articles_processed.md") is False # ledger
    assert co.is_included("03_Resources/Articles/README.md") is False         # readme
    assert co.is_included("03_Resources/Books/cheatsheet.pdf") is False        # binary


def test_classify():
    assert co.classify("00_Inbox/Clippings/articles to process.md") == "url-list"
    assert co.classify("00_Inbox/Clippings/TO SCRAPE.md") == "url-list"
    assert co.classify("03_Resources/Articles/Clean Code.md") == "note"
```

- [ ] **Step 2: Run to verify fail**

Run: `python3 -m pytest tests/test_collect_obsidian.py -q`
Expected: FAIL (`No module named 'collect_obsidian'`).

- [ ] **Step 3: Create `bin/collect_obsidian.py` header + policy**
```python
#!/usr/bin/env python3
"""collect_obsidian.py — deterministic core for the collect-obsidian collector.

Pure functions: path policy, URL-list parsing, source-frontmatter building, dedup,
discovery, and the reaper selector. All I/O (copies, fetch, git) lives in
obsidian_client.py. Reuses helpers from collect_email (DRY).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent
ROOT = BIN.parent
INBOX = ROOT / "raw" / "_inbox"
DEDUP_DIRS = [ROOT / "raw" / "_inbox", ROOT / "raw" / "notes", ROOT / "raw" / "web"]

VAULT_ROOT = Path("/Users/jonasblasques/Dev/second-brain")
INCLUDE_DIRS = [
    "03_Resources/Articles", "03_Resources/Books", "03_Resources/Study Notes",
    "03_Resources/Snippets", "03_Resources/Prompt Templates", "00_Inbox/Clippings",
]
EXCLUDE_DIRS = ["03_Resources/llm-wiki-system"]
EXCLUDE_FILE_RE = re.compile(r"(?i)(_processed\.md$|(^|/)README\.md$)")
URL_LIST_NAMES = {"articles to process.md", "TO SCRAPE.md"}

sys.path.insert(0, str(BIN))
from collect_email import slugify, yaml_scalar, URL_RE  # noqa: E402


def is_included(rel_path: str) -> bool:
    rel = rel_path.replace("\\", "/")
    if any(rel == e or rel.startswith(e + "/") for e in EXCLUDE_DIRS):
        return False
    if not rel.endswith(".md"):
        return False
    if EXCLUDE_FILE_RE.search(rel):
        return False
    return any(rel.startswith(i + "/") for i in INCLUDE_DIRS)


def classify(rel_path: str) -> str:
    return "url-list" if rel_path.rsplit("/", 1)[-1] in URL_LIST_NAMES else "note"
```

- [ ] **Step 4: Run to verify pass**

Run: `python3 -m pytest tests/test_collect_obsidian.py -q`
Expected: 3 passed.

- [ ] **Step 5: Commit**
```bash
git add bin/collect_obsidian.py tests/test_collect_obsidian.py
git commit -m "feat(collect-obsidian): path policy (is_included + classify)"
```

---

## Task 2: URL-list parsing + note reading

**Files:** Modify `bin/collect_obsidian.py`; `tests/test_collect_obsidian.py`.

- [ ] **Step 1: Write failing tests**
```python
def test_parse_url_list():
    text = "\nhttps://a.com/x\n\nsome prose\nhttps://b.com/y?z=1\nhttps://a.com/x\n"
    assert co.parse_url_list(text) == ["https://a.com/x", "https://b.com/y?z=1"]


def test_read_note_extracts_title_tags_body(tmp_path):
    f = tmp_path / "n.md"
    f.write_text("---\ntitle: \"Clean Code\"\ntags:\n  - python\n  - clean-code\n---\n\nBody line.\n",
                 encoding="utf-8")
    title, tags, body = co.read_note(str(f))
    assert title == "Clean Code"
    assert tags == ["python", "clean-code"]
    assert body.strip() == "Body line."


def test_read_note_no_frontmatter_uses_stem(tmp_path):
    f = tmp_path / "Just A Note.md"
    f.write_text("plain body", encoding="utf-8")
    title, tags, body = co.read_note(str(f))
    assert title == "Just A Note" and tags == [] and body.strip() == "plain body"
```

- [ ] **Step 2: Run to verify fail**

Run: `python3 -m pytest tests/test_collect_obsidian.py -k "parse_url_list or read_note" -q`
Expected: FAIL.

- [ ] **Step 3: Implement (append)**
```python
def parse_url_list(text: str) -> list:
    seen, out = set(), []
    for m in URL_RE.finditer(text or ""):
        u = m.group(0).rstrip(".,)")
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def read_note(abs_path: str):
    """Return (title, tags, body) — splits the note's own frontmatter off the body."""
    t = Path(abs_path).read_text(encoding="utf-8", errors="replace")
    title, tags, body = "", [], t
    if t.startswith("---"):
        end = t.find("\n---", 3)
        if end != -1:
            fm, body = t[3:end], t[end + 4:].lstrip("\n")
            tm = re.search(r"^title:\s*(.+)$", fm, re.M)
            if tm:
                title = tm.group(1).strip().strip('"')
            tg = re.search(r"^tags:\s*\n((?:\s*-\s*.+\n?)+)", fm, re.M)
            if tg:
                tags = [re.sub(r"^\s*-\s*", "", ln).strip() for ln in tg.group(1).splitlines() if ln.strip()]
    if not title:
        title = Path(abs_path).stem
    return title, tags, body
```

- [ ] **Step 4: Run to verify pass**

Run: `python3 -m pytest tests/test_collect_obsidian.py -k "parse_url_list or read_note" -q`
Expected: 3 passed.

- [ ] **Step 5: Commit**
```bash
git add bin/collect_obsidian.py tests/test_collect_obsidian.py
git commit -m "feat(collect-obsidian): URL-list parsing + note frontmatter split"
```

---

## Task 3: Source builders + filenames

**Files:** Modify `bin/collect_obsidian.py`; `tests/test_collect_obsidian.py`.

- [ ] **Step 1: Write failing tests**
```python
def test_note_filename(tmp_path):
    p = co.note_filename("03_Resources/Articles/Clean Code!.md", tmp_path)
    assert p.name == "notes-clean-code.md"


def test_build_note_source():
    doc = co.build_note_source(
        {"vault_origin": "03_Resources/Articles/Clean Code.md", "title": "Clean: Code",
         "tags": ["python"], "collected_at": "2026-06-12"}, "Body text.")
    assert "channel: notes" in doc
    assert "source: obsidian" in doc
    assert "vault_origin: 03_Resources/Articles/Clean Code.md" in doc
    assert 'title: "Clean: Code"' in doc
    assert "  - python" in doc
    assert doc.rstrip().endswith("Body text.")


def test_build_url_source():
    doc = co.build_url_source(
        {"source_url": "https://a.com/x", "via_vault_list": "00_Inbox/Clippings/articles to process.md",
         "title": "A", "collected_at": "2026-06-12"}, "Article body")
    assert "channel: web" in doc
    assert "source_url: https://a.com/x" in doc
    assert "via_vault_list: 00_Inbox/Clippings/articles to process.md" in doc
    assert doc.rstrip().endswith("Article body")
```

- [ ] **Step 2: Run to verify fail**

Run: `python3 -m pytest tests/test_collect_obsidian.py -k "filename or build_note_source or build_url_source" -q`
Expected: FAIL.

- [ ] **Step 3: Implement (append)**
```python
def note_filename(rel_path: str, base=None) -> Path:
    base = base if base is not None else INBOX
    stem = rel_path.rsplit("/", 1)[-1]
    if stem.endswith(".md"):
        stem = stem[:-3]
    return base / f"notes-{slugify(stem)}.md"


def url_filename(url: str, title: str, base=None) -> Path:
    base = base if base is not None else INBOX
    return base / f"web-{slugify(title or url)}.md"


def build_note_source(meta: dict, body: str) -> str:
    lines = [
        "---", "channel: notes", "source: obsidian",
        f"vault_origin: {meta['vault_origin']}",
        f"title: {yaml_scalar(meta.get('title', ''))}",
    ]
    tags = meta.get("tags") or []
    if tags:
        lines.append("tags:")
        lines += [f"  - {t}" for t in tags]
    lines += [f"collected_at: {meta['collected_at']}", "---", "", body.strip(), ""]
    return "\n".join(lines)


def build_url_source(meta: dict, body: str) -> str:
    lines = [
        "---", "channel: web", "source: obsidian-list",
        f"source_url: {meta['source_url']}",
        f"via_vault_list: {meta['via_vault_list']}",
        f"title: {yaml_scalar(meta.get('title', ''))}",
        f"collected_at: {meta['collected_at']}", "---", "", body.strip(), "",
    ]
    return "\n".join(lines)
```

- [ ] **Step 4: Run to verify pass**

Run: `python3 -m pytest tests/test_collect_obsidian.py -k "filename or build_note_source or build_url_source" -q`
Expected: 4 passed.

- [ ] **Step 5: Commit**
```bash
git add bin/collect_obsidian.py tests/test_collect_obsidian.py
git commit -m "feat(collect-obsidian): source-frontmatter builders + filenames"
```

---

## Task 4: Dedup + frontmatter helpers

**Files:** Modify `bin/collect_obsidian.py`; `tests/test_collect_obsidian.py`.

- [ ] **Step 1: Write failing tests**
```python
def test_fm_field():
    assert co.fm_field("---\nvault_origin: a/b.md\n---\n", "vault_origin") == "a/b.md"
    assert co.fm_field("no fm", "vault_origin") is None


def test_is_vault_note_ingested(tmp_path):
    a = tmp_path / "a.md"; a.write_text("---\ncorpus_ingested: true\n---\nx", encoding="utf-8")
    b = tmp_path / "b.md"; b.write_text("---\ntitle: x\n---\ny", encoding="utf-8")
    assert co.is_vault_note_ingested(str(a)) is True
    assert co.is_vault_note_ingested(str(b)) is False


def test_already_collected_vault(tmp_path):
    d = tmp_path / "inbox"; d.mkdir()
    (d / "notes-x.md").write_text("---\nvault_origin: 03_Resources/Articles/X.md\n---\n", encoding="utf-8")
    assert co.already_collected_vault("03_Resources/Articles/X.md", [d]) is True
    assert co.already_collected_vault("03_Resources/Articles/Y.md", [d]) is False


def test_url_already_collected(tmp_path):
    d = tmp_path / "web"; d.mkdir()
    (d / "web-x.md").write_text("---\nsource_url: https://a.com/x\n---\n", encoding="utf-8")
    assert co.url_already_collected("https://a.com/x", [d]) is True
    assert co.url_already_collected("https://a.com/z", [d]) is False
```

- [ ] **Step 2: Run to verify fail**

Run: `python3 -m pytest tests/test_collect_obsidian.py -k "fm_field or ingested or already_collected_vault or url_already" -q`
Expected: FAIL.

- [ ] **Step 3: Implement (append)**
```python
def fm_field(text: str, key: str):
    m = re.search(rf"^{re.escape(key)}:\s*(.+)$", text, re.M)
    return m.group(1).strip() if m else None


def is_vault_note_ingested(abs_path: str) -> bool:
    try:
        t = Path(abs_path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    return "corpus_ingested: true" in t


def _raw_sources(dirs=None):
    for d in (dirs if dirs is not None else DEDUP_DIRS):
        p = Path(d)
        if not p.exists():
            continue
        for md in p.glob("*.md"):
            try:
                yield md, md.read_text(encoding="utf-8", errors="replace")
            except (OSError, UnicodeDecodeError):
                continue


def already_collected_vault(rel_path: str, dirs=None) -> bool:
    needle = f"vault_origin: {rel_path}\n"
    return any(needle in t for _, t in _raw_sources(dirs))


def url_already_collected(url: str, dirs=None) -> bool:
    needle = f"source_url: {url}\n"
    return any(needle in t for _, t in _raw_sources(dirs))
```

- [ ] **Step 4: Run to verify pass**

Run: `python3 -m pytest tests/test_collect_obsidian.py -k "fm_field or ingested or already_collected_vault or url_already" -q`
Expected: 4 passed.

- [ ] **Step 5: Commit**
```bash
git add bin/collect_obsidian.py tests/test_collect_obsidian.py
git commit -m "feat(collect-obsidian): dedup + frontmatter helpers"
```

---

## Task 5: Discovery + reaper selector

**Files:** Modify `bin/collect_obsidian.py`; `tests/test_collect_obsidian.py`.

- [ ] **Step 1: Write failing tests** (fixture vault)
```python
def _vault(tmp_path):
    v = tmp_path / "vault"
    (v / "03_Resources/Articles").mkdir(parents=True)
    (v / "03_Resources/llm-wiki-system").mkdir(parents=True)
    (v / "00_Inbox/Clippings").mkdir(parents=True)
    (v / "01_Projects").mkdir(parents=True)
    (v / "03_Resources/Articles/New.md").write_text("---\ntitle: New\n---\nbody", encoding="utf-8")
    (v / "03_Resources/Articles/Done.md").write_text("---\ncorpus_ingested: true\n---\nx", encoding="utf-8")
    (v / "03_Resources/llm-wiki-system/CLAUDE.md").write_text("mirror", encoding="utf-8")
    (v / "01_Projects/task.md").write_text("task", encoding="utf-8")
    (v / "00_Inbox/Clippings/articles to process.md").write_text("https://a.com/x\n", encoding="utf-8")
    return v


def test_discover_filters(tmp_path):
    v = _vault(tmp_path)
    found = co.discover(v, dedup_dirs=[tmp_path / "none"])
    rels = {(d["rel_path"], d["kind"]) for d in found}
    assert ("03_Resources/Articles/New.md", "note") in rels
    assert ("00_Inbox/Clippings/articles to process.md", "url-list") in rels
    assert "03_Resources/Articles/Done.md" not in {r for r, _ in rels}        # already ingested
    assert "03_Resources/llm-wiki-system/CLAUDE.md" not in {r for r, _ in rels}  # excluded
    assert "01_Projects/task.md" not in {r for r, _ in rels}                   # not a knowledge dir


def test_discover_skips_already_collected(tmp_path):
    v = _vault(tmp_path)
    raw = tmp_path / "raw"; raw.mkdir()
    (raw / "notes-new.md").write_text("---\nvault_origin: 03_Resources/Articles/New.md\n---\n", encoding="utf-8")
    rels = {d["rel_path"] for d in co.discover(v, dedup_dirs=[raw])}
    assert "03_Resources/Articles/New.md" not in rels   # already collected → skipped


def test_reapable_selects_only_ingested(tmp_path):
    raw = tmp_path / "raw"; raw.mkdir()
    (raw / "notes-a.md").write_text("---\ncorpus_ingested: true\nvault_origin: 03_Resources/Articles/A.md\n---\n", encoding="utf-8")
    (raw / "notes-b.md").write_text("---\nvault_origin: 03_Resources/Articles/B.md\n---\n", encoding="utf-8")  # NOT ingested
    (raw / "web-u.md").write_text("---\ncorpus_ingested: true\nvia_vault_list: 00_Inbox/Clippings/articles to process.md\nsource_url: https://a.com/x\n---\n", encoding="utf-8")
    r = co.reapable([raw])
    assert r["vault_notes"] == ["03_Resources/Articles/A.md"]                 # B excluded (not ingested)
    assert r["url_strikes"] == [("00_Inbox/Clippings/articles to process.md", "https://a.com/x")]
```

- [ ] **Step 2: Run to verify fail**

Run: `python3 -m pytest tests/test_collect_obsidian.py -k "discover or reapable" -q`
Expected: FAIL.

- [ ] **Step 3: Implement (append)**
```python
def discover(vault_root=None, dedup_dirs=None) -> list:
    root = Path(vault_root) if vault_root else VAULT_ROOT
    out = []
    for inc in INCLUDE_DIRS:
        base = root / inc
        if not base.exists():
            continue
        for f in sorted(base.rglob("*.md")):
            rel = str(f.relative_to(root))
            if not is_included(rel):
                continue
            if is_vault_note_ingested(str(f)):
                continue
            if already_collected_vault(rel, dedup_dirs):
                continue
            out.append({"rel_path": rel, "abs_path": str(f), "kind": classify(rel)})
    return out


def reapable(dedup_dirs=None) -> dict:
    notes, url_strikes = [], []
    for _, t in _raw_sources(dedup_dirs):
        if "corpus_ingested: true" not in t:
            continue
        vo = fm_field(t, "vault_origin")
        if vo:
            notes.append(vo)
        vl, su = fm_field(t, "via_vault_list"), fm_field(t, "source_url")
        if vl and su:
            url_strikes.append((vl, su))
    return {"vault_notes": notes, "url_strikes": url_strikes}
```

- [ ] **Step 4: Run to verify pass + full suite**

Run: `python3 -m pytest tests/test_collect_obsidian.py -q && python3 -m pytest -q`
Expected: new file all pass; full suite green (85 + new).

- [ ] **Step 5: Commit**
```bash
git add bin/collect_obsidian.py tests/test_collect_obsidian.py
git commit -m "feat(collect-obsidian): discovery + reaper selector"
```

---

## Task 6: `collect` orchestration + CLI

**Files:** Create `bin/obsidian_client.py`; Test `tests/test_obsidian_client.py`.

- [ ] **Step 1: Write failing tests** (mock `fetch_link.fetch`)

Create `tests/test_obsidian_client.py`:
```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import obsidian_client as oc  # noqa: E402


def test_collect_copies_note_and_fetches_url(tmp_path, monkeypatch):
    vault = tmp_path / "vault"
    (vault / "03_Resources/Articles").mkdir(parents=True)
    (vault / "00_Inbox/Clippings").mkdir(parents=True)
    (vault / "03_Resources/Articles/New.md").write_text("---\ntitle: New\n---\nbody", encoding="utf-8")
    (vault / "00_Inbox/Clippings/articles to process.md").write_text("https://a.com/x\n", encoding="utf-8")
    inbox = tmp_path / "inbox"; inbox.mkdir()
    monkeypatch.setattr(oc.co, "INBOX", inbox)
    monkeypatch.setattr(oc.co, "DEDUP_DIRS", [inbox])
    monkeypatch.setattr(oc, "fetch_url", lambda url: {"title": "Art", "text": "fetched body", "channel": "web"})
    rc = oc.cmd_collect(oc._args(["collect", "--vault", str(vault)]))
    assert rc == 0
    files = {p.name for p in inbox.glob("*.md")}
    assert any(n.startswith("notes-new") for n in files)
    assert any(n.startswith("web-art") for n in files)


def test_collect_dry_run_writes_nothing(tmp_path, monkeypatch):
    vault = tmp_path / "vault"
    (vault / "03_Resources/Articles").mkdir(parents=True)
    (vault / "03_Resources/Articles/New.md").write_text("body", encoding="utf-8")
    inbox = tmp_path / "inbox"; inbox.mkdir()
    monkeypatch.setattr(oc.co, "INBOX", inbox)
    monkeypatch.setattr(oc.co, "DEDUP_DIRS", [inbox])
    oc.cmd_collect(oc._args(["collect", "--vault", str(vault), "--dry-run"]))
    assert list(inbox.glob("*.md")) == []
```

- [ ] **Step 2: Run to verify fail**

Run: `python3 -m pytest tests/test_obsidian_client.py -q`
Expected: FAIL (`No module named 'obsidian_client'`).

- [ ] **Step 3: Implement `bin/obsidian_client.py` (collect portion)**
```python
#!/usr/bin/env python3
"""obsidian_client.py — I/O + CLI for the collect-obsidian collector."""
from __future__ import annotations

import argparse
import datetime
import json
import subprocess
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent
sys.path.insert(0, str(BIN))
import collect_obsidian as co  # noqa: E402
import fetch_link as fl  # noqa: E402


def fetch_url(url: str) -> dict:
    """Seam over fetch_link.fetch so tests can stub it. Returns {} on failure."""
    try:
        return fl.fetch(url)
    except Exception:
        return {}


def cmd_collect(args) -> int:
    vault = Path(args.vault) if args.vault else co.VAULT_ROOT
    collected_at = datetime.date.today().isoformat()
    found = co.discover(vault)
    if args.path:
        found = [d for d in found if d["rel_path"].startswith(args.path)]
    t = {"notes": 0, "urls": 0, "url_failed": 0, "skipped": 0}
    processed = 0
    for d in found:
        if args.max and processed >= args.max:
            break
        processed += 1
        try:
            if d["kind"] == "note":
                title, tags, body = co.read_note(d["abs_path"])
                if not args.dry_run:
                    path = co.note_filename(d["rel_path"])
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(co.build_note_source(
                        {"vault_origin": d["rel_path"], "title": title, "tags": tags,
                         "collected_at": collected_at}, body), encoding="utf-8")
                t["notes"] += 1
            else:  # url-list
                urls = co.parse_url_list(Path(d["abs_path"]).read_text(encoding="utf-8", errors="replace"))
                for url in urls:
                    if co.url_already_collected(url):
                        t["skipped"] += 1
                        continue
                    content = fetch_url(url)
                    if not content or not content.get("text"):
                        t["url_failed"] += 1
                        continue
                    if not args.dry_run:
                        path = co.url_filename(url, content.get("title", ""))
                        path.parent.mkdir(parents=True, exist_ok=True)
                        path.write_text(co.build_url_source(
                            {"source_url": url, "via_vault_list": d["rel_path"],
                             "title": content.get("title", ""), "collected_at": collected_at},
                            content["text"]), encoding="utf-8")
                    t["urls"] += 1
        except Exception:
            t["skipped"] += 1
    print(json.dumps({**t, "dry_run": bool(args.dry_run), "discovered": len(found)}, indent=2))
    return 0


def _args(argv):
    p = argparse.ArgumentParser(description="Obsidian vault → corpus collector.")
    sub = p.add_subparsers(dest="cmd", required=True)
    pc = sub.add_parser("collect")
    pc.add_argument("--vault", default=None)
    pc.add_argument("--dry-run", action="store_true")
    pc.add_argument("--max", type=int, default=None)
    pc.add_argument("--path", default=None)
    pc.set_defaults(func=cmd_collect)
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = _args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
```
> Task 7 adds the `reap` subparser to `_args`; `main` stays as written here.

- [ ] **Step 4: Run to verify pass**

Run: `python3 -m pytest tests/test_obsidian_client.py -q`
Expected: 2 passed.

- [ ] **Step 5: Commit**
```bash
git add bin/obsidian_client.py tests/test_obsidian_client.py
git commit -m "feat(collect-obsidian): collect orchestration + CLI"
```

---

## Task 7: `reap` (vault git rm + list strike) + CLI

**Files:** Modify `bin/obsidian_client.py`; `tests/test_obsidian_client.py`.

- [ ] **Step 1: Write failing tests** (mock git via a recorder)
```python
def test_reap_removes_only_ingested(tmp_path, monkeypatch):
    vault = tmp_path / "vault"
    (vault / "03_Resources/Articles").mkdir(parents=True)
    note = vault / "03_Resources/Articles/A.md"; note.write_text("x", encoding="utf-8")
    listf = vault / "00_Inbox/Clippings"; listf.mkdir(parents=True)
    (listf / "articles to process.md").write_text("https://a.com/x\nhttps://b.com/y\n", encoding="utf-8")
    raw = tmp_path / "raw"; raw.mkdir()
    (raw / "notes-a.md").write_text("---\ncorpus_ingested: true\nvault_origin: 03_Resources/Articles/A.md\n---\n", encoding="utf-8")
    (raw / "web-x.md").write_text("---\ncorpus_ingested: true\nvia_vault_list: 00_Inbox/Clippings/articles to process.md\nsource_url: https://a.com/x\n---\n", encoding="utf-8")
    monkeypatch.setattr(oc.co, "DEDUP_DIRS", [raw])
    calls = []
    monkeypatch.setattr(oc, "git_rm", lambda vault_root, rel: calls.append(rel))
    rc = oc.cmd_reap(oc._args(["reap", "--vault", str(vault)]))
    assert rc == 0
    assert calls == ["03_Resources/Articles/A.md"]                       # note staged for deletion
    remaining = (listf / "articles to process.md").read_text()
    assert "https://a.com/x" not in remaining and "https://b.com/y" in remaining  # processed URL struck
    assert "https://a.com/x" in (listf / "articles_processed.md").read_text()      # appended to ledger


def test_reap_dry_run_changes_nothing(tmp_path, monkeypatch):
    vault = tmp_path / "vault"; (vault / "03_Resources/Articles").mkdir(parents=True)
    raw = tmp_path / "raw"; raw.mkdir()
    (raw / "notes-a.md").write_text("---\ncorpus_ingested: true\nvault_origin: 03_Resources/Articles/A.md\n---\n", encoding="utf-8")
    monkeypatch.setattr(oc.co, "DEDUP_DIRS", [raw])
    calls = []
    monkeypatch.setattr(oc, "git_rm", lambda vault_root, rel: calls.append(rel))
    oc.cmd_reap(oc._args(["reap", "--vault", str(vault), "--dry-run"]))
    assert calls == []
```

- [ ] **Step 2: Run to verify fail**

Run: `python3 -m pytest tests/test_obsidian_client.py -k reap -q`
Expected: FAIL.

- [ ] **Step 3: Implement (append to `bin/obsidian_client.py`)**
```python
def git_rm(vault_root: Path, rel_path: str) -> None:
    """Stage a deletion in the vault (recoverable; NOT committed)."""
    subprocess.run(["git", "-C", str(vault_root), "rm", "--quiet", rel_path],
                   capture_output=True, check=False)


def _strike_url(vault_root: Path, list_rel: str, url: str) -> None:
    listf = vault_root / list_rel
    if listf.exists():
        lines = [ln for ln in listf.read_text(encoding="utf-8").splitlines() if ln.strip() != url]
        listf.write_text("\n".join(lines) + "\n", encoding="utf-8")
    ledger = listf.parent / "articles_processed.md"
    prev = ledger.read_text(encoding="utf-8") if ledger.exists() else ""
    ledger.write_text(prev + url + "\n", encoding="utf-8")


def cmd_reap(args) -> int:
    vault = Path(args.vault) if args.vault else co.VAULT_ROOT
    r = co.reapable()
    t = {"notes_removed": 0, "urls_struck": 0}
    for rel in r["vault_notes"]:
        if (vault / rel).exists() and not args.dry_run:
            git_rm(vault, rel)
            t["notes_removed"] += 1
        elif args.dry_run and (vault / rel).exists():
            t["notes_removed"] += 1
    for list_rel, url in r["url_strikes"]:
        if not args.dry_run:
            _strike_url(vault, list_rel, url)
        t["urls_struck"] += 1
    print(json.dumps({**t, "dry_run": bool(args.dry_run),
                      "note": "vault deletions are staged, not committed — review and commit in the vault"},
                     indent=2))
    return 0
```

Add the `reap` subparser inside `_args` (before `return p.parse_args(argv)`):
```python
    pr = sub.add_parser("reap")
    pr.add_argument("--vault", default=None)
    pr.add_argument("--dry-run", action="store_true")
    pr.set_defaults(func=cmd_reap)
```

And ensure `main` is exactly:
```python
def main(argv=None) -> int:
    args = _args(argv)
    return args.func(args)
```

- [ ] **Step 4: Run to verify pass + smoke + full suite**

Run:
```bash
python3 -m pytest tests/test_obsidian_client.py -q
python3 bin/obsidian_client.py collect --help
python3 bin/obsidian_client.py reap --help
python3 -m pytest -q
```
Expected: reap tests pass; both helps show `--dry-run`; full suite green.

- [ ] **Step 5: Commit**
```bash
git add bin/obsidian_client.py tests/test_obsidian_client.py
git commit -m "feat(collect-obsidian): reap (git rm + list strike) + CLI"
```

---

## Task 8: Skill + config + CLAUDE.md v0.7

**Files:** Create `.claude/skills/collect-obsidian/SKILL.md`; Modify `corpus/_config.md`, `CLAUDE.md`, `corpus/_log.md`.

- [ ] **Step 1: Write the skill**

Create `.claude/skills/collect-obsidian/SKILL.md`:
```markdown
---
name: collect-obsidian
description: Collect reference-layer notes (and URL-list links) from the user's Obsidian vault into raw/_inbox/, then after they're ingested, remove the originals from the vault. Use when the user wants to pull vault notes into the corpus.
---

# Collect Obsidian

Capture reference-layer notes from the Obsidian vault (`vault_root` in corpus/_config.md)
into `raw/_inbox/` (channel `notes`; URL-list links → channel `web` via fetch_link), then —
after the corpus has ingested them — delete the originals from the vault. Collection only;
never ingest into `corpus/` here.

## Safety rules (non-negotiable)
- `reap` deletes a vault note (or strikes a list URL) ONLY when its raw source is
  `corpus_ingested: true`. Never delete un-ingested content.
- Never touch notes already `corpus_ingested` in the vault (the 21 PARA-native ones) — they
  stay in place with their existing citations.
- `--dry-run` deletes/writes nothing. The reaper STAGES vault deletions (git rm) but does
  NOT commit — the user reviews and commits in the vault.

## Procedure
1. `python3 bin/obsidian_client.py collect --dry-run` — preview discovered notes/URLs. Then
   `collect` (optionally `--max N`, `--path 03_Resources/Articles`).
2. Run the normal corpus Branch-A ingest on `raw/_inbox/` (the v0.6 pipeline) → corpus pages,
   which stamps each raw source `corpus_ingested`.
3. `python3 bin/obsidian_client.py reap --dry-run` — preview removals. Then `reap`.
4. Tell the user to review and commit the vault deletions (`git -C <vault> status`).

## Notes
- Auth-walled URLs (LinkedIn/x.com) in `articles to process.md` fail extraction → recorded,
  URL left in the list.
- llm-wiki-system, 01_Projects, 04_Archive are out of scope (excluded).
- Large first run: collect discovers all ~489 resource notes; ingest + reap drain over waves.
```

- [ ] **Step 2: Update `corpus/_config.md`**

In the PARA-native section, append a note (exact text):
```markdown

## Obsidian vault collection (collect-obsidian)

- `vault_root`: `/Users/jonasblasques/Dev/second-brain`
- **Include:** `03_Resources/{Articles, Books, Study Notes, Snippets, Prompt Templates}`, `00_Inbox/Clippings/`.
- **Exclude:** `03_Resources/llm-wiki-system` (corpus mirror), `01_Projects`, `02_Areas`, `04_Archive`, rest of `00_Inbox`, `*_processed.md`, `README.md`, binaries.
- The `/collect-obsidian` skill copies these into `raw/_inbox/` (channel `notes`; URL-list links → `web`), and — after `corpus_ingested` — removes the vault original (git-recoverable, not auto-committed). The authoritative include/exclude policy lives in `bin/collect_obsidian.py`.
```

- [ ] **Step 3: Add the CLAUDE.md v0.7 vault-removal exception**

In CLAUDE.md §2, after the inbox-move exception, add:
```markdown
> **Vault-removal exception (v0.7).** After a vault source note's content has been collected into `raw/` and that raw source is confirmed `corpus_ingested`, the `collect-obsidian` reaper may delete the original vault note (or strike a processed URL from a vault list file). This is the only deletion of a source file permitted; it applies only to the configured `vault_root` paths, is gated on `corpus_ingested`, and is recoverable from the vault's own git history. The reaper stages (`git rm`) but never commits the vault.
```
Change the title line `# CLAUDE.md — LLM Corpus Schema (v0.6)` → `(v0.7)`. In §13, add a bullet: `- **Deleting a vault note before its raw source is `corpus_ingested`** → stop; re-read the §2 vault-removal exception.` In §15, add: `- v0.7 — §2 vault-removal exception for the collect-obsidian reaper (gated on corpus_ingested; vault git-recoverable; never auto-commits). Rationale: let the vault be decluttered as its knowledge lands in the corpus.`

- [ ] **Step 4: Log it + commit**
```bash
# append to corpus/_log.md:
#   ## [2026-06-12] schema | v0.6 → v0.7 — collect-obsidian vault-removal exception
#   - §2 vault-removal exception; §13 + §15 updated. Enables the Obsidian vault collector.
git add .claude/skills/collect-obsidian/SKILL.md corpus/_config.md CLAUDE.md corpus/_log.md
git commit -m "docs(collect-obsidian): skill + config + CLAUDE.md v0.7 vault-removal exception"
```

- [ ] **Step 5: Final full suite**

Run: `python3 -m pytest -q`
Expected: all green (85 existing + new collect_obsidian/obsidian_client tests).

---

## Definition of Done

- [ ] `python3 -m pytest -q` green (85 existing + new).
- [ ] `collect --dry-run` discovers reference-layer notes + URL-list links, writes nothing; `collect` writes `raw/_inbox/notes-*` and `web-*` with `vault_origin`/`via_vault_list`.
- [ ] Excluded paths (llm-wiki-system, Projects, Archive, ledgers, README, binaries) never discovered; already-`corpus_ingested` vault notes never discovered.
- [ ] `reap` removes a vault note / strikes a URL ONLY when its raw source is `corpus_ingested`; `--dry-run` changes nothing; reaper stages but never commits the vault.
- [ ] CLAUDE.md is v0.7 with the vault-removal exception; `_config.md` documents vault_root + scope.

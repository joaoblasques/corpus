# PDF Collector Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Collect PDFs dropped in a Google Drive folder, extract their text to channel-`pdf` markdown in `raw/_inbox/`, and after ingest move the original PDF to a `_processed/` subfolder.

**Architecture:** Two files mirroring the obsidian collector — `bin/collect_pdf.py` (pure logic: discover, extract, dedup, source-building, move-selector) and `bin/pdf_client.py` (CLI driver: `collect` + `file` subcommands). Wired into the daily `scheduled_run.py`. Reuses `collect_email.slugify`/`yaml_scalar`.

**Tech Stack:** Python 3.12, pytest, `pymupdf4llm` (+ `pymupdf`/`fitz`) for PDF→markdown. Tests under `tests/`, run with `python3 -m pytest`.

## Global Constraints

- Watch dir (default, in `collect_pdf.py`): `/Users/jonasblasques/Library/CloudStorage/GoogleDrive-tilakapash@gmail.com/My Drive/CorpusInbox/PDFs`
- Processed subfolder: `_processed` (created on first move).
- New channel `pdf` → raw path `raw/pdf/`. Collector writes extracted markdown to `raw/_inbox/` (channel `pdf`); the normal ingest moves it to `raw/pdf/`.
- `MIN_TEXT_WORDS = 50` — below this, a PDF is treated as a scan/non-text and is NOT written (low-text guard); it is left in the watch folder and reported.
- Extraction library: `pymupdf4llm` (AGPL-3.0 via PyMuPDF — acceptable for personal non-distributed tooling).
- After ingest: **move** (not delete) the original PDF to `_processed/`, gated on `corpus_ingested` of the raw copy.
- Dedup by `content_sha` (sha256 of the PDF bytes).
- Collector writes only into `raw/_inbox/`; the `file` step only touches the watch dir. Never writes to `corpus/`.
- Reuse `collect_email.slugify` and `collect_email.yaml_scalar` (DRY).
- `DEDUP_DIRS = [raw/_inbox, raw/pdf]`.
- Tests run with `python3 -m pytest`; test files prepend `bin/` to `sys.path` (see existing `tests/test_obsidian_client.py`).

---

### Task 1: `collect_pdf.py` foundation (discover, dedup, source-building)

**Files:**
- Create: `bin/collect_pdf.py`
- Test: `tests/test_collect_pdf.py`

**Interfaces:**
- Consumes: `collect_email.slugify(text) -> str`, `collect_email.yaml_scalar(value) -> str`.
- Produces:
  - constants `PDF_WATCH_DIR: Path`, `PROCESSED_SUBDIR = "_processed"`, `MIN_TEXT_WORDS = 50`, `INBOX: Path`, `DEDUP_DIRS: list[Path]`
  - `discover(watch_dir=None) -> list[dict]` — each `{"abs_path": str, "filename": str}` for top-level `*.pdf`
  - `content_sha(abs_path) -> str` (sha256 hex)
  - `pdf_filename(filename, base=None) -> Path` → `INBOX/f"pdf-{slugify(stem)}.md"`
  - `build_pdf_source(meta: dict, body: str) -> str`
  - `already_collected(sha: str, dirs=None) -> bool`
  - `fm_field(text, key) -> str|None`, `_raw_sources(dirs=None)` (helpers)

- [ ] **Step 1: Write the failing tests**

Create `tests/test_collect_pdf.py`:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import collect_pdf as cp  # noqa: E402


def test_discover_finds_top_level_pdfs_only(tmp_path):
    (tmp_path / "a.pdf").write_bytes(b"%PDF-1.4 a")
    (tmp_path / "b.PDF").write_bytes(b"%PDF-1.4 b")
    (tmp_path / "notes.md").write_text("x")
    (tmp_path / ".hidden.pdf").write_bytes(b"%PDF x")
    (tmp_path / "~$tmp.pdf").write_bytes(b"%PDF x")
    proc = tmp_path / "_processed"; proc.mkdir()
    (proc / "old.pdf").write_bytes(b"%PDF x")
    names = sorted(d["filename"] for d in cp.discover(tmp_path))
    assert names == ["a.pdf", "b.PDF"]


def test_content_sha_stable(tmp_path):
    f = tmp_path / "x.pdf"; f.write_bytes(b"hello pdf bytes")
    assert cp.content_sha(str(f)) == cp.content_sha(str(f))
    assert len(cp.content_sha(str(f))) == 64


def test_pdf_filename(tmp_path):
    p = cp.pdf_filename("Deep Learning Book!.pdf", tmp_path)
    assert p.name == "pdf-deep-learning-book.md"


def test_build_pdf_source_has_frontmatter():
    doc = cp.build_pdf_source(
        {"pdf_origin": "paper.pdf", "source_path": "/d/paper.pdf", "title": "A Paper",
         "author": "Jo", "pages": 12, "content_sha": "abc123", "collected_at": "2026-06-18"},
        "body text here")
    assert "channel: pdf" in doc
    assert "pdf_origin: paper.pdf" in doc
    assert "content_sha: abc123" in doc
    assert "pages: 12" in doc
    assert doc.rstrip().endswith("body text here")


def test_already_collected_detects_prior_sha(tmp_path):
    raw = tmp_path / "raw"; raw.mkdir()
    (raw / "pdf-x.md").write_text("---\nchannel: pdf\ncontent_sha: deadbeef\n---\nbody", encoding="utf-8")
    assert cp.already_collected("deadbeef", dirs=[raw]) is True
    assert cp.already_collected("0000", dirs=[raw]) is False
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_collect_pdf.py -v`
Expected: FAIL (`ModuleNotFoundError: No module named 'collect_pdf'`).

- [ ] **Step 3: Implement `bin/collect_pdf.py`**

```python
#!/usr/bin/env python3
"""collect_pdf.py — deterministic core for the PDF collector.

Pure functions: discovery, sha dedup, source-frontmatter building, and the
move-selector. All heavy I/O (extraction, file moves) is driven from pdf_client.py.
Reuses helpers from collect_email (DRY).
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent
ROOT = BIN.parent
INBOX = ROOT / "raw" / "_inbox"
DEDUP_DIRS = [ROOT / "raw" / "_inbox", ROOT / "raw" / "pdf"]

PDF_WATCH_DIR = Path(
    "/Users/jonasblasques/Library/CloudStorage/GoogleDrive-tilakapash@gmail.com/"
    "My Drive/CorpusInbox/PDFs"
)
PROCESSED_SUBDIR = "_processed"
MIN_TEXT_WORDS = 50

sys.path.insert(0, str(BIN))
from collect_email import slugify, yaml_scalar  # noqa: E402

_SKIP_RE = re.compile(r"^(\.|~\$)")  # hidden / office temp files


def discover(watch_dir=None) -> list:
    root = Path(watch_dir) if watch_dir is not None else PDF_WATCH_DIR
    if not root.exists():
        return []
    out = []
    for p in sorted(root.iterdir()):
        if not p.is_file():
            continue
        if p.suffix.lower() != ".pdf":
            continue
        if _SKIP_RE.match(p.name):
            continue
        out.append({"abs_path": str(p), "filename": p.name})
    return out


def content_sha(abs_path: str) -> str:
    h = hashlib.sha256()
    with open(abs_path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def pdf_filename(filename: str, base=None) -> Path:
    base = base if base is not None else INBOX
    stem = filename[:-4] if filename.lower().endswith(".pdf") else filename
    return base / f"pdf-{slugify(stem)}.md"


def build_pdf_source(meta: dict, body: str) -> str:
    lines = [
        "---", "channel: pdf", "source: pdf",
        f"pdf_origin: {meta['pdf_origin']}",
        f"source_path: {meta['source_path']}",
        f"title: {yaml_scalar(meta.get('title', ''))}",
        f"author: {yaml_scalar(meta.get('author', ''))}",
        f"pages: {meta.get('pages', 0)}",
        f"content_sha: {meta['content_sha']}",
        f"collected_at: {meta['collected_at']}", "---", "", body.strip(), "",
    ]
    return "\n".join(lines)


def _frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    return text[3:end] if end != -1 else ""


def fm_field(text: str, key: str):
    m = re.search(rf"^{re.escape(key)}:\s*(.+)$", _frontmatter(text), re.M)
    return m.group(1).strip() if m else None


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


def already_collected(sha: str, dirs=None) -> bool:
    for _, text in _raw_sources(dirs):
        if fm_field(text, "content_sha") == sha:
            return True
    return False
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_collect_pdf.py -v`
Expected: PASS (5 tests).

- [ ] **Step 5: Commit**

```bash
git add bin/collect_pdf.py tests/test_collect_pdf.py
git commit -m "feat(collect-pdf): logic core — discover, content_sha, build_pdf_source, dedup"
```

---

### Task 2: PDF text extraction (`extract`)

**Files:**
- Modify: `bin/collect_pdf.py` (add `extract`)
- Test: `tests/test_collect_pdf.py` (add extraction test)

**Interfaces:**
- Consumes: `pymupdf4llm.to_markdown(path) -> str`, `fitz` (PyMuPDF) for metadata.
- Produces: `extract(abs_path) -> dict` with keys `markdown: str`, `title: str`, `author: str`, `pages: int`, `words: int`. Title falls back to the filename stem when PDF metadata has no title.

- [ ] **Step 1: Install the dependency**

Run: `python3 -m pip install pymupdf4llm`
Expected: installs `pymupdf4llm` and `pymupdf`. Verify: `python3 -c "import pymupdf4llm, fitz; print('ok')"` → `ok`.

- [ ] **Step 2: Write the failing test**

Add to `tests/test_collect_pdf.py` (generates a real text PDF with fitz, then extracts it):

```python
def _make_pdf(path, text, title="", author=""):
    import fitz
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), text)
    if title or author:
        doc.set_metadata({"title": title, "author": author})
    doc.save(str(path)); doc.close()


def test_extract_reads_text_and_metadata(tmp_path):
    pdf = tmp_path / "doc.pdf"
    _make_pdf(pdf, "Hello world this is a real test pdf body. " * 10,
              title="My Test PDF", author="Tester")
    r = cp.extract(str(pdf))
    assert "Hello world" in r["markdown"]
    assert r["title"] == "My Test PDF"
    assert r["author"] == "Tester"
    assert r["pages"] == 1
    assert r["words"] >= 50


def test_extract_title_falls_back_to_stem(tmp_path):
    pdf = tmp_path / "Untitled Paper.pdf"
    _make_pdf(pdf, "some text " * 30)
    r = cp.extract(str(pdf))
    assert r["title"] == "Untitled Paper"
```

- [ ] **Step 3: Run test to verify it fails**

Run: `python3 -m pytest tests/test_collect_pdf.py -k extract -v`
Expected: FAIL (`AttributeError: module 'collect_pdf' has no attribute 'extract'`).

- [ ] **Step 4: Implement `extract`**

Add to `bin/collect_pdf.py`:

```python
def extract(abs_path: str) -> dict:
    """Extract a PDF to markdown + metadata. Seam over pymupdf4llm/fitz (stubbable)."""
    import pymupdf4llm
    import fitz
    markdown = pymupdf4llm.to_markdown(abs_path) or ""
    doc = fitz.open(abs_path)
    meta = doc.metadata or {}
    pages = doc.page_count
    doc.close()
    title = (meta.get("title") or "").strip() or Path(abs_path).stem
    author = (meta.get("author") or "").strip()
    return {"markdown": markdown, "title": title, "author": author,
            "pages": pages, "words": len(markdown.split())}
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_collect_pdf.py -v`
Expected: PASS (7 tests).

- [ ] **Step 6: Commit**

```bash
git add bin/collect_pdf.py tests/test_collect_pdf.py
git commit -m "feat(collect-pdf): extract PDF text+metadata to markdown via pymupdf4llm"
```

---

### Task 3: `pdf_client.py` — `collect` driver

**Files:**
- Create: `bin/pdf_client.py`
- Test: `tests/test_pdf_client.py`

**Interfaces:**
- Consumes: `collect_pdf` (`PDF_WATCH_DIR`, `MIN_TEXT_WORDS`, `discover`, `content_sha`, `already_collected`, `pdf_filename`, `build_pdf_source`, `extract`). Driver invoked via `pc.cmd_collect(pc._args([...]))`. Tests stub `pc.extract` and set `pc.cp.INBOX`/`pc.cp.DEDUP_DIRS`.
- Produces: `extract(abs_path)` seam, `cmd_collect(args) -> int`, `_args(argv)`, `main(argv=None)`. JSON summary keys: `collected, skipped, low_text, low_text_files, dry_run, discovered`.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_pdf_client.py`:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import pdf_client as pc  # noqa: E402


def test_collect_writes_pdf_source(tmp_path, monkeypatch):
    watch = tmp_path / "PDFs"; watch.mkdir()
    (watch / "a.pdf").write_bytes(b"%PDF-1.4 hello")
    inbox = tmp_path / "inbox"; inbox.mkdir()
    monkeypatch.setattr(pc.cp, "INBOX", inbox)
    monkeypatch.setattr(pc.cp, "DEDUP_DIRS", [inbox])
    monkeypatch.setattr(pc, "extract", lambda p: {
        "markdown": "real body " * 40, "title": "A", "author": "Jo", "pages": 3, "words": 80})
    rc = pc.cmd_collect(pc._args(["collect", "--dir", str(watch)]))
    assert rc == 0
    files = list(inbox.glob("pdf-*.md"))
    assert len(files) == 1
    text = files[0].read_text()
    assert "channel: pdf" in text and "pdf_origin: a.pdf" in text


def test_collect_low_text_guard_skips(tmp_path, monkeypatch):
    watch = tmp_path / "PDFs"; watch.mkdir()
    (watch / "scan.pdf").write_bytes(b"%PDF-1.4 img")
    inbox = tmp_path / "inbox"; inbox.mkdir()
    monkeypatch.setattr(pc.cp, "INBOX", inbox)
    monkeypatch.setattr(pc.cp, "DEDUP_DIRS", [inbox])
    monkeypatch.setattr(pc, "extract", lambda p: {
        "markdown": "two words", "title": "scan", "author": "", "pages": 5, "words": 2})
    pc.cmd_collect(pc._args(["collect", "--dir", str(watch)]))
    assert list(inbox.glob("pdf-*.md")) == []          # nothing written
    assert (watch / "scan.pdf").exists()                # left in place


def test_collect_dedup_skips_already_collected(tmp_path, monkeypatch):
    watch = tmp_path / "PDFs"; watch.mkdir()
    (watch / "a.pdf").write_bytes(b"%PDF-1.4 hello")
    inbox = tmp_path / "inbox"; inbox.mkdir()
    sha = pc.cp.content_sha(str(watch / "a.pdf"))
    (inbox / "pdf-a.md").write_text(f"---\nchannel: pdf\ncontent_sha: {sha}\n---\nx", encoding="utf-8")
    monkeypatch.setattr(pc.cp, "INBOX", inbox)
    monkeypatch.setattr(pc.cp, "DEDUP_DIRS", [inbox])
    calls = []
    monkeypatch.setattr(pc, "extract", lambda p: calls.append(p) or {
        "markdown": "x " * 60, "title": "A", "author": "", "pages": 1, "words": 60})
    pc.cmd_collect(pc._args(["collect", "--dir", str(watch)]))
    assert calls == []                                  # extract never called (deduped)


def test_collect_dry_run_writes_nothing(tmp_path, monkeypatch):
    watch = tmp_path / "PDFs"; watch.mkdir()
    (watch / "a.pdf").write_bytes(b"%PDF-1.4 hello")
    inbox = tmp_path / "inbox"; inbox.mkdir()
    monkeypatch.setattr(pc.cp, "INBOX", inbox)
    monkeypatch.setattr(pc.cp, "DEDUP_DIRS", [inbox])
    monkeypatch.setattr(pc, "extract", lambda p: {
        "markdown": "x " * 60, "title": "A", "author": "", "pages": 1, "words": 60})
    pc.cmd_collect(pc._args(["collect", "--dir", str(watch), "--dry-run"]))
    assert list(inbox.glob("pdf-*.md")) == []
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_pdf_client.py -v`
Expected: FAIL (`ModuleNotFoundError: No module named 'pdf_client'`).

- [ ] **Step 3: Implement `bin/pdf_client.py` (collect only)**

```python
#!/usr/bin/env python3
"""pdf_client.py — driver for the PDF collector (collect + file).

collect: extract new PDFs from the watch dir into raw/_inbox (channel pdf).
file:    after ingest, move ingested PDFs into the watch dir's _processed/ subfolder.
Pure logic lives in collect_pdf.py.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import shutil
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent
sys.path.insert(0, str(BIN))
import collect_pdf as cp  # noqa: E402


def extract(abs_path: str) -> dict:
    """Seam over collect_pdf.extract so tests can stub the heavy PDF library."""
    return cp.extract(abs_path)


def cmd_collect(args) -> int:
    watch = Path(args.dir) if args.dir else cp.PDF_WATCH_DIR
    collected_at = datetime.date.today().isoformat()
    found = cp.discover(watch)
    t = {"collected": 0, "skipped": 0, "low_text": 0, "low_text_files": []}
    processed = 0
    for d in found:
        if args.max and processed >= args.max:
            break
        processed += 1
        try:
            sha = cp.content_sha(d["abs_path"])
            if cp.already_collected(sha):
                t["skipped"] += 1
                continue
            meta = extract(d["abs_path"])
            if meta["words"] < cp.MIN_TEXT_WORDS:
                t["low_text"] += 1
                t["low_text_files"].append(d["filename"])
                continue
            if args.dry_run:
                t["collected"] += 1
                continue
            path = cp.pdf_filename(d["filename"])
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(cp.build_pdf_source(
                {"pdf_origin": d["filename"], "source_path": d["abs_path"],
                 "title": meta["title"], "author": meta["author"], "pages": meta["pages"],
                 "content_sha": sha, "collected_at": collected_at},
                meta["markdown"]), encoding="utf-8")
            t["collected"] += 1
        except Exception:  # noqa: BLE001 — a bad/locked file must not abort the batch
            t["skipped"] += 1
    print(json.dumps({**t, "dry_run": bool(args.dry_run), "discovered": len(found)}, indent=2))
    return 0


def _args(argv):
    p = argparse.ArgumentParser(description="PDF folder → corpus collector.")
    sub = p.add_subparsers(dest="cmd", required=True)
    pcol = sub.add_parser("collect")
    pcol.add_argument("--dir", default=None)
    pcol.add_argument("--max", type=int, default=None)
    pcol.add_argument("--dry-run", action="store_true")
    pcol.set_defaults(func=cmd_collect)
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = _args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_pdf_client.py -v`
Expected: PASS (4 tests).

- [ ] **Step 5: Commit**

```bash
git add bin/pdf_client.py tests/test_pdf_client.py
git commit -m "feat(pdf-client): collect — extract PDFs to raw/_inbox with low-text guard + dedup"
```

---

### Task 4: `file` step — move ingested PDFs to `_processed/`

**Files:**
- Modify: `bin/collect_pdf.py` (add `processable`)
- Modify: `bin/pdf_client.py` (add `_under_watch`, `cmd_file`, register subparser)
- Test: `tests/test_collect_pdf.py` (processable), `tests/test_pdf_client.py` (move)

**Interfaces:**
- Consumes: `cp.processable(dirs=None) -> list[str]` (pdf_origin filenames whose raw copy is `corpus_ingested: true`), `cp.PROCESSED_SUBDIR`.
- Produces: `pc._under_watch(watch: Path, rel: str) -> bool`, `pc.cmd_file(args) -> int`. JSON summary keys: `moved, dry_run`.

- [ ] **Step 1: Write the failing tests**

Add to `tests/test_collect_pdf.py`:

```python
def test_processable_selects_only_ingested(tmp_path):
    raw = tmp_path / "raw"; raw.mkdir()
    (raw / "pdf-a.md").write_text(
        "---\nchannel: pdf\npdf_origin: a.pdf\ncorpus_ingested: true\n---\nx", encoding="utf-8")
    (raw / "pdf-b.md").write_text(
        "---\nchannel: pdf\npdf_origin: b.pdf\n---\nx", encoding="utf-8")  # not ingested
    assert cp.processable(dirs=[raw]) == ["a.pdf"]
```

Add to `tests/test_pdf_client.py`:

```python
def test_file_moves_only_ingested_pdf(tmp_path, monkeypatch):
    watch = tmp_path / "PDFs"; watch.mkdir()
    (watch / "a.pdf").write_bytes(b"%PDF a")
    (watch / "b.pdf").write_bytes(b"%PDF b")
    raw = tmp_path / "raw"; raw.mkdir()
    (raw / "pdf-a.md").write_text(
        "---\nchannel: pdf\npdf_origin: a.pdf\ncorpus_ingested: true\n---\nx", encoding="utf-8")
    (raw / "pdf-b.md").write_text(
        "---\nchannel: pdf\npdf_origin: b.pdf\n---\nx", encoding="utf-8")
    monkeypatch.setattr(pc.cp, "DEDUP_DIRS", [raw])
    rc = pc.cmd_file(pc._args(["file", "--dir", str(watch)]))
    assert rc == 0
    assert not (watch / "a.pdf").exists()                       # moved
    assert (watch / "_processed" / "a.pdf").exists()
    assert (watch / "b.pdf").exists()                            # not ingested -> stays


def test_file_rejects_path_traversal(tmp_path, monkeypatch):
    watch = tmp_path / "PDFs"; watch.mkdir()
    outside = tmp_path / "etc"; outside.mkdir()
    (outside / "x.pdf").write_bytes(b"secret")
    raw = tmp_path / "raw"; raw.mkdir()
    (raw / "pdf-evil.md").write_text(
        "---\nchannel: pdf\npdf_origin: ../etc/x.pdf\ncorpus_ingested: true\n---\nx", encoding="utf-8")
    monkeypatch.setattr(pc.cp, "DEDUP_DIRS", [raw])
    pc.cmd_file(pc._args(["file", "--dir", str(watch)]))
    assert (outside / "x.pdf").exists()                          # never touched
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_collect_pdf.py -k processable tests/test_pdf_client.py -k file -v`
Expected: FAIL (`AttributeError`: `processable` / `cmd_file` not defined).

- [ ] **Step 3: Implement `processable` in `bin/collect_pdf.py`**

```python
def processable(dirs=None) -> list:
    """pdf_origin filenames whose raw copy is corpus_ingested (ready to move)."""
    out = []
    for _, text in _raw_sources(dirs):
        if "corpus_ingested: true" not in text:
            continue
        origin = fm_field(text, "pdf_origin")
        if origin:
            out.append(origin)
    return out
```

- [ ] **Step 4: Implement `_under_watch` + `cmd_file` in `bin/pdf_client.py` and register the subparser**

Add the functions:

```python
def _under_watch(watch: Path, rel: str) -> bool:
    """Reject traversal / absolute paths escaping the watch dir."""
    if os.path.isabs(rel) or ".." in os.path.normpath(rel).split(os.sep):
        return False
    try:
        return (watch / rel).resolve().is_relative_to(watch.resolve())
    except (OSError, ValueError):
        return False


def cmd_file(args) -> int:
    watch = Path(args.dir) if args.dir else cp.PDF_WATCH_DIR
    proc_dir = watch / cp.PROCESSED_SUBDIR
    t = {"moved": 0}
    for origin in cp.processable():
        if not _under_watch(watch, origin):
            continue
        src = watch / origin
        if not src.exists():
            continue
        if args.dry_run:
            t["moved"] += 1
            continue
        proc_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(proc_dir / Path(origin).name))
        t["moved"] += 1
    print(json.dumps({**t, "dry_run": bool(args.dry_run)}, indent=2))
    return 0
```

Register the `file` subparser inside `_args` (before `return p.parse_args(argv)`):

```python
    pfile = sub.add_parser("file")
    pfile.add_argument("--dir", default=None)
    pfile.add_argument("--dry-run", action="store_true")
    pfile.set_defaults(func=cmd_file)
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_collect_pdf.py tests/test_pdf_client.py -v`
Expected: PASS (all collect_pdf + pdf_client tests).

- [ ] **Step 6: Commit**

```bash
git add bin/collect_pdf.py bin/pdf_client.py tests/test_collect_pdf.py tests/test_pdf_client.py
git commit -m "feat(pdf-client): file — move ingested PDFs to _processed/ (gated, traversal-safe)"
```

---

### Task 5: Wire the PDF collector into the scheduled run

**Files:**
- Modify: `bin/scheduled_run.py` (`run_collectors` — add a PDF leg)
- Test: `tests/test_scheduled_run.py` (assert pdf_client invoked)

**Interfaces:**
- Consumes: `pdf_client.py collect` via subprocess (same pattern as obsidian).
- Produces: `results["pdf"] = {"status": ..., "collected": <int>}` in the `run_collectors` return dict, using the `collected` key from the pdf JSON summary.

- [ ] **Step 1: Write the failing test**

Look at `tests/test_scheduled_run.py::test_gmail_and_obsidian_invoked` for the pattern, then add:

```python
    def test_pdf_collector_invoked(self, tmp_path):
        """run_collectors calls pdf_client collect via subprocess."""
        called_scripts = []

        def fake_run(cmd, **kwargs):
            called_scripts.append(" ".join(cmd))
            import types
            return types.SimpleNamespace(returncode=0, stdout='{"collected": 0}', stderr="")

        scheduled_run.run_collectors(
            youtube_token_path=tmp_path / "nope.json", _subprocess_run=fake_run)
        assert any("pdf_client.py" in s and "collect" in s for s in called_scripts), (
            f"pdf_client.py collect not found in calls: {called_scripts}")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_scheduled_run.py -k pdf_collector -v`
Expected: FAIL (no pdf_client.py call in the recorded subprocess commands).

- [ ] **Step 3: Add the PDF leg to `run_collectors`**

In `bin/scheduled_run.py`, immediately AFTER the `# --- Obsidian ---` try/except block and BEFORE `# --- YouTube ---`, insert:

```python
    # --- PDF ---
    try:
        proc = _run(
            [sys.executable, str(BIN / "pdf_client.py"), "collect"],
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            results["pdf"] = {
                "status": "failed",
                "collected": 0,
                "error": proc.stderr.strip() or f"exit {proc.returncode}",
            }
        else:
            try:
                data = json.loads(proc.stdout)
                collected = data.get("collected", 0)
            except (json.JSONDecodeError, AttributeError):
                collected = 0
            results["pdf"] = {"status": "ok", "collected": collected}
    except Exception as exc:  # noqa: BLE001
        results["pdf"] = {"status": "failed", "collected": 0, "error": str(exc)}
```

> Note: the `file` (move-processed) step is intentionally NOT added to `run_collectors` here — it must run AFTER ingest. If the scheduled pipeline has a post-ingest hook, wire `pdf_client.py file` there; otherwise it is run manually / on the next day's run. Keeping it out of `run_collectors` avoids moving a PDF before its content is ingested. (Document this in Task 6.)

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_scheduled_run.py -v`
Expected: PASS (new pdf test + existing collector tests).

- [ ] **Step 5: Commit**

```bash
git add bin/scheduled_run.py tests/test_scheduled_run.py
git commit -m "feat(scheduled-run): run the PDF collector in the daily collection phase"
```

---

### Task 6: Config, gitignore, docs + full-suite gate

**Files:**
- Modify: `corpus/_config.md` (PDF section + channel row)
- Modify: `corpus/_log.md` (append a `config` entry)
- Modify: `.gitignore` (add `raw/pdf/*`)

**Interfaces:** none (config/docs).

- [ ] **Step 1: Add `raw/pdf/*` to `.gitignore`**

In `.gitignore`, in the block of `raw/<channel>/*` lines (next to `raw/web/*`), add:

```
raw/pdf/*
```

- [ ] **Step 2: Add the PDF section + channel row to `corpus/_config.md`**

Add a new section (after the `## Obsidian vault collection (collect-obsidian)` section):

```markdown
## PDF collection (collect-pdf)

- `pdf_watch_dir`: `~/Library/CloudStorage/GoogleDrive-tilakapash@gmail.com/My Drive/CorpusInbox/PDFs`
  (Google Drive for Desktop sync path; drop PDFs here from any device).
- `pdf_processed_subdir`: `_processed` (ingested originals are moved here; created on first move).
- Channel `pdf` → `raw/pdf/`. The `/collect-pdf` driver (`bin/pdf_client.py collect`) extracts
  each PDF's text to markdown via `pymupdf4llm` and writes it to `raw/_inbox/` (channel `pdf`);
  the normal Branch-A ingest then routes + moves it to `raw/pdf/`.
- Text-only: a PDF yielding < 50 words is treated as a scan and left in place (reported, not
  ingested). After ingest, `bin/pdf_client.py file` moves the original PDF to `_processed/`,
  gated on `corpus_ingested`. Dedup is by `content_sha`.
- The authoritative watch-dir/policy defaults live in `bin/collect_pdf.py`.
```

And add a row to the channel-labels table:

```markdown
| `pdf` | `raw/pdf/` (collected via `/collect-pdf` from a Drive folder) | — |
```

- [ ] **Step 3: Append a `config` entry to `corpus/_log.md`**

```markdown

## [2026-06-18 HH:MM] config | add PDF collector (collect-pdf)
- new channel `pdf` → raw/pdf/; watch dir = Google Drive My Drive/CorpusInbox/PDFs (synced locally)
- bin/collect_pdf.py + bin/pdf_client.py (collect + file); pymupdf4llm extraction; text-only
  (low-text guard at 50 words), content_sha dedup, move-to-_processed gated on corpus_ingested
- wired into scheduled_run collection phase; .gitignore raw/pdf/*
- spec: docs/superpowers/specs/2026-06-18-pdf-collector-design.md
```

(Use the real current time for `HH:MM`.)

- [ ] **Step 4: Run the full test suite as the gate**

Run: `python3 -m pytest tests/ -q`
Expected: PASS (all tests, including the new collect_pdf / pdf_client / scheduled_run ones).

- [ ] **Step 5: Commit**

```bash
git add corpus/_config.md corpus/_log.md .gitignore
git commit -m "docs(collect-pdf): document the PDF channel, watch dir, and lifecycle; gitignore raw/pdf"
```

---

## Notes for the executor

- **Smoke test after merge (optional, real PDF):** drop a small text PDF into
  `~/Library/CloudStorage/GoogleDrive-tilakapash@gmail.com/My Drive/CorpusInbox/PDFs/`, run
  `python3 bin/pdf_client.py collect --dry-run`, and confirm it reports `collected: 1` (or
  `low_text` for a scan). This hits the real Drive path + real `pymupdf4llm`.
- **`file` runs after ingest, never before.** It is gated on `corpus_ingested` of the raw copy,
  so running it early is a no-op, but keep it out of the pre-ingest collection phase.
- **Dependency:** `pymupdf4llm` must be installed in whatever Python environment the launchd
  scheduled job uses (the system `python3` here). Task 2 installs it for the dev environment;
  confirm the scheduled job uses the same interpreter (`sys.executable`).
```

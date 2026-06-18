# PDF Collector — Design

> Date: 2026-06-18
> Status: approved (design); pending implementation plan
> Mirrors the `collect-obsidian` collector (`bin/collect_obsidian.py` + `bin/obsidian_client.py`)
> and its design (`2026-06-12-obsidian-collector-design.md`).

## Problem

The corpus has collectors for email, Obsidian notes, YouTube, and web links, but **no way to
ingest PDFs**. PDFs are currently `"unsupported"` in `bin/fetch_link.py` (`classify()` returns
`"unsupported"` for `.pdf`), and no PDF-extraction library is installed. The user wants to drop
PDFs (articles, papers, ebooks) into a folder and have their text extracted, collected as
channel-tagged markdown, and ingested into the corpus like any other source — then the original
PDF moved aside.

## Decisions (confirmed with user)

- **Drop location:** a Google Drive folder, read via its local Drive-for-Desktop sync path. The
  folder already exists: `My Drive/CorpusInbox/PDFs/`, synced to
  `~/Library/CloudStorage/GoogleDrive-tilakapash@gmail.com/My Drive/CorpusInbox/PDFs/`.
  Drop from any device; the collector reads it as a normal local directory — no Drive API/OAuth.
- **PDF types:** text-based only (no OCR). Scanned/image PDFs are detected and flagged, not
  ingested as garbage.
- **After ingest:** move the original PDF to a `_processed/` subfolder (keep it), gated on
  `corpus_ingested` — mirrors the obsidian reaper, but moves instead of deletes.

## Scope

In: `bin/collect_pdf.py`, `bin/pdf_client.py`, `corpus/_config.md` (+ `_log.md` config entry),
`bin/scheduled_run.py` (wire in the new collector), `.gitignore` (add `raw/pdf/*`), tests, one
new dependency (`pymupdf4llm`).
Out: OCR, per-chapter splitting of large PDFs (noted as a follow-up), the Drive API path,
changes to `fetch_link.py` (PDF-from-URL stays out of scope; this is local-file PDFs only).

## Design

### 1. Configuration — `corpus/_config.md`

New section + channel:

- `pdf_watch_dir`: `~/Library/CloudStorage/GoogleDrive-tilakapash@gmail.com/My Drive/CorpusInbox/PDFs`
- `pdf_processed_subdir`: `_processed` (created on first move)
- Channel table gains: `pdf` → `raw/pdf/`.

The watch dir is read from config so it is configurable without code changes. `collect_pdf.py`
holds the default, matching how `collect_obsidian.py` holds `VAULT_ROOT`.

### 2. Extraction — `pymupdf4llm`

`pymupdf4llm.to_markdown(path)` produces clean PDF→markdown (headings, lists, tables preserved
reasonably). PDF metadata via PyMuPDF: `fitz.open(path).metadata` → `title`, `author`;
`doc.page_count` → page count. New dependency `pymupdf4llm` (pulls `pymupdf`). **License note:**
PyMuPDF is AGPL-3.0 — acceptable for this personal, non-distributed tooling.

### 3. `bin/collect_pdf.py` (logic module)

Pure-ish functions, unit-testable, mirroring `collect_obsidian.py`:

- `PDF_WATCH_DIR`, `PROCESSED_SUBDIR`, `MIN_TEXT_WORDS = 50`, `INBOX = raw/_inbox`.
- `discover(watch_dir=None) -> list[dict]` — top-level `*.pdf` in the watch dir (exclude the
  `_processed/` subdir, hidden/temp files, and `.gdoc` etc.). Each: `{abs_path, filename}`.
- `extract(abs_path) -> dict` — returns `{markdown, title, author, pages, words}` via
  `pymupdf4llm` + PyMuPDF metadata. Title falls back to the filename stem when PDF metadata has
  no title. (Seam over the library so tests can stub it.)
- `content_sha(abs_path) -> str` — sha256 of the file bytes (dedup key).
- `pdf_filename(filename) -> Path` — `INBOX / f"pdf-{slugify(stem)}.md"` (reuse
  `collect_email.slugify`).
- `build_pdf_source(meta, body) -> str` — frontmatter + body:
  ```yaml
  channel: pdf
  source: pdf
  pdf_origin: <filename relative to watch dir>
  source_path: <absolute path at collect time>
  title: <title>
  author: <author>
  pages: <n>
  content_sha: <sha256>
  collected_at: YYYY-MM-DD
  ```
- `already_collected(sha, dirs=None) -> bool` — true if any raw source under
  `[raw/_inbox, raw/pdf]` already has this `content_sha` (idempotency; mirrors
  `url_already_collected`).
- `processable(watch_dir=None) -> dict` — for the move step: scan raw sources (`raw/_inbox`,
  `raw/pdf`) for `corpus_ingested: true` + `pdf_origin`; return the list of `pdf_origin`
  filenames whose original still sits in the watch dir.

### 4. `bin/pdf_client.py` (CLI driver)

Mirrors `obsidian_client.py`. Subcommands:

- `collect [--dir PATH] [--max N] [--dry-run]`:
  for each discovered PDF: skip if `already_collected(sha)` (→ `skipped`); else `extract`; if
  `words < MIN_TEXT_WORDS` → **low-text guard**: do not write, increment `low_text`, record the
  filename (leave the PDF in place); else write `pdf-<slug>.md` to `raw/_inbox` via
  `build_pdf_source`. Dry run extracts/counts but writes nothing. JSON summary:
  `{collected, skipped, low_text, low_text_files, dry_run, discovered}`.
- `file [--dir PATH] [--dry-run]` (the "move-processed" step):
  `processable()` → for each `pdf_origin`, if `_under_watch(watch, origin)` and the file exists,
  move it to `<watch>/_processed/` (create the dir; `shutil.move`). Gated on `corpus_ingested`
  of the raw copy — never moves an un-ingested PDF. JSON summary `{moved, dry_run}`. Path-safety
  check (`_under_watch`) rejects traversal, like obsidian's `_under_vault`.

### 5. Data flow

```
drop PDF → Drive/My Drive/CorpusInbox/PDFs/   (phone / web / laptop)
  → pdf_client collect → extract text→markdown → raw/_inbox/pdf-<slug>.md   (channel pdf)
  → /ingest-auto (Branch A) → corpus pages + stamp raw copy corpus_ingested
  → pdf_client file → move original PDF → CorpusInbox/PDFs/_processed/   (gated on corpus_ingested)
```

The extracted markdown is the ingestable source; the original PDF is preserved in `_processed/`
(and in Drive). `raw/pdf/` is gitignored like the other raw channels.

### 6. Scheduled integration — `bin/scheduled_run.py`

Add the pdf collector to the daily 08:00 run alongside gmail/obsidian/youtube: run
`pdf_client collect` in the collection phase, and `pdf_client file` after the ingest phase (safe
— it is gated on `corpus_ingested`). The run-summary log line gains a `pdf=<n>` field.

### 7. Edge cases / safety

- **Scanned/image PDFs** (no text layer): the `MIN_TEXT_WORDS` guard skips them — no garbage
  source written; the PDF stays in the watch folder and is reported in `low_text_files` so the
  user can handle it (manual extraction or future OCR). To avoid re-flagging every run, the
  controller surfaces these once per run via the JSON summary (no separate ledger in v1).
- **Idempotency:** `content_sha` dedup means re-running `collect` before ingest does not
  re-extract; after ingest the `file` step removes the PDF from the watch dir, so it is not
  rediscovered.
- **Large PDFs (books):** extracted as a single markdown; the existing batch-ingest pipeline
  chunks it into pages. Per-chapter splitting is a possible follow-up, not v1.
- **Drive sync latency:** the collector reads whatever is materialized locally; a partially
  synced/0-byte placeholder is skipped by the low-text guard or an open error (caught, counted,
  left in place). No special handling beyond try/except per file.
- **Non-PDF / Google-native files** in the folder (`.gdoc`, `.docx`) are ignored — only `*.pdf`.

## Testing

Mirror the obsidian collector tests:
- `discover` picks up top-level `*.pdf`, excludes `_processed/`, hidden, and non-pdf files.
- `build_pdf_source` emits the channel-`pdf` frontmatter with all fields; body round-trips.
- `content_sha` stable; `already_collected` detects a prior raw source with the same sha.
- `collect` (driver, `extract`/`fitz` stubbed): writes one `pdf-*.md`; the **low-text guard**
  writes nothing and reports `low_text` for a near-empty extraction; `--dry-run` writes nothing.
- `file`/move: a `corpus_ingested` raw pdf source moves its origin into `_processed/`; an
  un-ingested one does **not** move; path-traversal `pdf_origin` is rejected.

## Risks / mitigations

- **Bad extraction quality** on complex layouts → the low-text guard catches the worst case
  (scans); for merely-messy text the §7 citation gate at ingest limits damage (a low-signal page
  produces few claims). Library swap (`markitdown`) is possible if quality disappoints.
- **AGPL dependency** → personal non-distributed use; acceptable. Documented in `_config.md`.
- **Watch-dir path drift** (Drive account/email change) → path in `_config.md`, single edit.

## Setup note

One-time: the user already created `My Drive/CorpusInbox/PDFs/`. The collector creates
`_processed/` on first move. `pip install pymupdf4llm` into the corpus tooling environment.

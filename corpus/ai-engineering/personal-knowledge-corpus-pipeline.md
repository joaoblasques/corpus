---
type: concept
domain: ai-engineering
status: draft
sources: []
aliases:
  - corpus pipeline
  - LLM corpus pipeline
  - personal knowledge corpus
  - collect ingest pipeline
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-15
updated: 2026-07-15
---

# Personal Knowledge Corpus Pipeline

**TL;DR.** A personal knowledge corpus (Karpathy LLM-Wiki pattern) is built by a pipeline with five stages: collect → quick-ingest → deep-ingest → write pages → index. The key architectural insight is that these stages split across two execution environments: a **local nightly job** (Mac, launchd) owns all stages that require local credentials and filesystem access; a **cloud Claude Code session** owns monitoring, push notifications, and interactive work. The repo is the bridge — local commits, cloud reads.

---

## Pipeline stages and where each runs

```
COLLECT → QUICK-INGEST → DEEP-INGEST → CORPUS PAGES → INDEXES → COMMIT/PUSH
  Local       Local          Local           Local        Local      Local
                                                                       ↓
                                                                   GitHub
                                                                       ↓
                                                             Cloud session (reads)
```

### Stage 1 — Collect

**Environment:** local Mac, `bin/scheduled_run.py` via launchd (02:00 daily)

Each channel runs as a subprocess:

| Channel | Script | Why local |
|---|---|---|
| Gmail | `gmail_client.py` | OAuth token in `~/.config/` |
| Obsidian | `obsidian_client.py` | Vault is a local folder |
| YouTube | `youtube_client.py` | OAuth token, yt-dlp |
| arXiv | `arxiv_client.py` | Open HTTP, but run locally for simplicity |
| PDF | `pdf_client.py` | Watches a local Google Drive folder |
| Books (EPUB) | `book_client.py` | Local Drive folder |
| GitHub | `github_client.py` | PAT stored locally |
| X bookmarks | `x_client.py` | OAuth token |

Output: stub markdown files in `raw/_inbox/`. No Claude involved.

### Stage 2 — Quick-ingest

**Environment:** local Mac, pure Python subprocesses

Two separate drains run each night before the expensive Claude ingest:

- **`quick_ingest_youtube.py`**: transcript stubs → Groq Whisper (audio→text) → Groq LLM summary → one `source` page per video. Drains ~50–60 videos/night.
- **`quick_ingest_docs.py`**: web/notes stubs → OpenRouter free LLM (Groq fallback) → one `source` page per doc. Drains ~50 docs/night.

These are **free or near-free** (Groq free tier, OpenRouter free models). No Claude API call. HTTP timeout per request: 30s; subprocess wall-clock limit: 1 hour.

Key constraint: stubs with `<120 words` of body are skipped as thin — they need a fetch pass first.

### Stage 3 — Deep-ingest

**Environment:** local Mac; invokes Claude API via local CLI

`run_ingest()` in `scheduled_run.py` calls the local `~/.claude/local/claude` binary headlessly:

```python
CLAUDE_BIN = Path.home() / ".claude" / "local" / "claude"
subprocess.run([str(CLAUDE_BIN), "--print", prompt, "--permission-mode", "bypassPermissions", ...])
```

The **local Claude CLI process** authenticates via local OAuth and streams to the Claude API. The LLM reasoning happens in Anthropic's cloud, but orchestration and all file writes happen on the local machine. Bounded to 6 sources/night by default (cost control — this is the expensive step).

The `/ingest-auto` skill runs inside this subprocess: reads source fully → routes to domain → extracts 3–10 entities/concepts → updates or creates corpus pages → updates index.

### Stage 4 — Corpus pages

**Written by:** both quick-ingest scripts (Python writes) and the headless Claude CLI process (Read/Write/Edit tool calls)

Page types produced [unsourced — see CLAUDE.md §3 for schema]:
- `source` — quick-intake output, minimal stub
- `entity`, `concept`, `synthesis` — deep-ingest output, full treatment

All pages: YAML frontmatter with `type`, `domain`, `status`, `sources`, `created`, `updated`.

### Stage 5 — Indexes + log

**Written by:** local processes

- `corpus/index.md` — appended by quick-ingest scripts and headless Claude
- `corpus/log.md` — `write_run_report()` in `scheduled_run.py` appends a structured run summary after every stage completes

Log format (newest-first, OKF reserved file):
```
## YYYY-MM-DD
* **Collectors**: gmail=N, obsidian=N, ...
* **Ingest**: N ingested · N deferred · status=ok
* **YoutubeQuick**: N intake · N rescued · N skipped
* **DocsQuick**: N intake · N thin · N llm_fail · status=ok
* **Gardener**: N stubs deepened
```

### Commit + push

`commit_and_push()` stages only `corpus/` (never `raw/` or `.`), commits with a structured message, and pushes to GitHub. This is the handoff point: everything downstream of here is read-only from the cloud.

---

## Cloud session role

The cloud session (Claude Code on the web, scheduled routine) clones the committed repo fresh at each run. It does **not** participate in collect→ingest→pages at all. Its role:

| Task | Why cloud, not local |
|---|---|
| Morning status report | Mac may be asleep; cloud runs regardless |
| Push notifications to phone | Requires Claude Code web infrastructure |
| Code maintenance / bug fixes | Interactive agentic session with full tool access |
| Query answering (`/query` skill) | Interactive, user is at keyboard |
| Manual ingest of complex sources | Needs oversight and Opus-quality reasoning |

The session-start hook (`bin/pending_review.py`) runs on every cloud session start and prints the last nightly run's stats, providing immediate orientation.

---

## Why the split makes sense

Local-only constraints that anchor stages 1–5 to the Mac:
- OAuth tokens and API keys are stored locally and never transferred to cloud containers
- Obsidian vault and Drive watch folders are local filesystems
- The headless Claude CLI process needs local binary + local auth

Cloud-only capabilities that anchor monitoring to the cloud session:
- `PushNotification` tool only exists in Claude Code web
- Cloud containers are always-on regardless of Mac sleep state
- Interactive sessions need the web UI

**Corollary:** if you are happy with email instead of push notifications, the entire system — including the morning status report — can run locally. The cloud session becomes optional; `scheduled_run.py` can send a run-summary email via the Gmail API (it already holds Gmail OAuth) after `write_run_report()`.

---

## Gardener and gap-resolver (auxiliary loops)

Two extra local loops run after deep-ingest each night:

- **Gardener** (`bin/gardener.py`): picks the highest-value stub pages and expands them using a Sonnet writer + Sonnet critic. Quota: 2–4 stubs/night. Pinned to Sonnet (not Opus) to protect the scarce Opus budget for interactive sessions.
- **GapResolver** (`bin/gap_resolver.py`): dispatches one logged query-gap per night — WebSearches 3 written sources and queues them into `raw/_inbox/` for the next ingest cycle. Growth-driven rather than collection-driven.

---

## Source

This page describes the system implemented in `bin/scheduled_run.py`, `bin/quick_ingest_youtube.py`, `bin/quick_ingest_docs.py`, `bin/gardener.py`, and `bin/gap_resolver.py` in this repository. Claims reflect the code as of 2026-07-15.

<!-- RELATED:START (generated by bin/corpus_heal.py related — do not edit inside) -->

## Related across domains

- [Obsidian & Personal Knowledge Management](/productivity/obsidian-pkm.md) · _productivity_

<!-- RELATED:END -->

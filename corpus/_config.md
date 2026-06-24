---
type: config
created: 2026-05-20
updated: 2026-06-15
---

# Corpus Config

Operational configuration for the LLM corpus system. Schema-level rules live in `CLAUDE.md`; this file is the data that those rules operate on.

---

## PARA-native ingest paths

Sources found under these paths are ingested **in place** — stamped with wiki metadata but **never copied to `raw/`**. These are the user's canonical notes with a permanent vault home.

| Path | Channel label | Notes |
|---|---|---|
| `03_Resources/Articles/` | `notes` | Obsidian Web Clipper saves, Matter exports already filed in vault, curated article notes |
| `03_Resources/Study Notes/` | `notes` | First-party study notes, course summaries, lecture notes |

All other sources arrive via `raw/_inbox/` (then routed to `raw/<channel>/`) or are dropped directly into a `raw/<channel>/` subfolder. `raw/notes/` is reserved for first-party notes that have no canonical PARA home (edge case / legacy).

**To add a path**: edit this table and append a `config | <change>` log entry to `corpus/_log.md`.

---

## Source file stamp fields

When any source is ingested, exactly these three frontmatter fields are written to the source file. No other edits to source files are permitted.

```yaml
corpus_ingested: true
corpus_ingested_at: YYYY-MM-DD   # most recent ingest date — updated on every successful ingest
corpus_pages:                     # accumulates; append new pages, never remove
  - corpus/<domain>/<page>.md
```

Rules:
- `corpus_pages` accumulates over time — append, never remove.
- `corpus_ingested_at` updates on every successful ingest (first or re-ingest). Full history is in `corpus/_log.md`.
- These are the **only** frontmatter fields you may add to source files. No other edits to source files are permitted.

---

## Channel labels (reference)

| Label | Raw path | PARA path |
|---|---|---|
| `matter` | `raw/matter/` | — |
| `youtube` | `raw/youtube/` | — |
| `web` | `raw/web/` | — |
| `notes` | `raw/notes/` (no PARA home) | `03_Resources/Articles/`, `03_Resources/Study Notes/` |
| `inbox` | `raw/_inbox/` (transient) | — |
| `email` | `raw/email/` (collected via `/collect-email`) | — |
| `pdf` | `raw/pdf/` (collected via `/collect-pdf` from a Drive folder) | — |

**Email collection**: starred Gmail messages are captured by the `/collect-email` skill into `raw/_inbox/` (channel `email`), then routed to `raw/email/` by the normal Branch A ingest flow. The skill writes a `gmail_message_id` frontmatter field used for dedup; it is not part of the §2 source-stamp spec.

**Label collection (corpus labels):** alongside starred mail, the `/collect-email`
run also collects messages under these Gmail labels (exact names; edit the
`CORPUS_LABELS` list in `bin/gmail_client.py`):
`Data Engineering`, `Data Engineering/databricks`, `Data Engineering/dbt`,
`Data Engineering/spark`, `Ml`, `ML Engineering`, `MLOps`, `Productivity`, `Prompting`.
Labeled emails record a `gmail_corpus_labels` frontmatter field and are NOT archived on
collection. After they are ingested (`corpus_ingested: true`), `bin/gmail_client.py
reap-labels` removes the matched corpus label(s) + `INBOX` (archive) — run post-ingest by
the scheduled job. The starred flow is unchanged (de-star + archive on collection).

**Query intake (`via_query`)**: the `/query` operation (§8.2) tops up thin coverage by fetching web sources to answer a gap. Each fetched source is auto-queued into `raw/_inbox/` (channel `web`, or `youtube` for video URLs) carrying a `via_query` frontmatter field (the originating question) for provenance, deduped by `source_url`. These drain into the corpus on the next normal Branch-A ingest. `via_query` is collector provenance, not part of the §2 source-stamp spec.

---

## Obsidian vault collection (collect-obsidian)

- `vault_root`: `/Users/jonasblasques/Dev/second-brain`
- **Include (collect → reap):** `Clippings/` (top-level), `00_Inbox/Clippings/`,
  `03_Resources/Books`, `06_Metadata/Reference/`. (Snippets / Prompt Templates removed
  2026-06-22 — not present in the vault.)
- **PARA-native (ingested in place, never reaped):** `03_Resources/Articles/`,
  `03_Resources/Study Notes/` — these keep their in-vault citations.
- **Exclude:** `03_Resources/llm-wiki-system` (corpus mirror), `01_Projects`, `02_Areas`,
  `04_Archive`, `06_Metadata/{Templates, SETUP_COMPLETE.md, README.md}`, rest of `00_Inbox`,
  `*_processed.md`, `README.md`, binaries.
- Inline external links in note bodies are fetched (channel `web`, provenance
  `via_vault_note`, deduped, asset/auth-walled links skipped, capped at 10/note), in addition
  to dedicated URL-list files (`articles to process.md`, `TO SCRAPE.md`).
- The `/collect-obsidian` skill copies these into `raw/_inbox/` (channel `notes`; URL-list links → `web`), and — after `corpus_ingested` — removes the vault original (git-recoverable, not auto-committed). The authoritative include/exclude policy lives in `bin/collect_obsidian.py`.

---

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

---

## GitHub repos (channel `github`)

The daily run collects the user's **starred** repos via the `gh` CLI (`bin/github_client.py run`) — one "repo digest" per repo (README + markdown docs + a metadata overview: description, topics, language, stars, latest release). Deduped by the frontmatter `repo: <owner/name>`; **stars are left in place** (a bookmark, not a queue). Sources land in `raw/_inbox` (channel `github`), drain via the normal ingest, then move to `raw/github`. No source code is collected. Auth: `gh` (skipped with `not configured` if unauthed).

---

## X (Twitter) bookmarks (channel `x`)

The daily run collects the user's **bookmarks** from X via the X API v2 (OAuth2 user-context) using `bin/x_client.py run`. One source document per bookmarked post, plus any linked article extracted from the post's URLs. Deduped by frontmatter `tweet_id`; **bookmarks are un-bookmarked only after the source is ingested** (`corpus_ingested: true`), via a separate reap step (`bin/x_client.py reap`). Sources land in `raw/_inbox` (channel `x`), drain via the normal ingest, then move to `raw/x`.

**Setup (one-time):** Create `bin/x_app.json` with the X app's OAuth2 credentials:
```json
{
  "client_id": "<your X app client ID>",
  "redirect_uri": "http://127.0.0.1:8723/callback"
}
```
Then run `python3 bin/x_client.py auth` to open a browser, authorize, and cache the token in `bin/x_token.json` (gitignored).

Auth: skipped with `not configured` if no `bin/x_app.json` or if auth fails (the run continues). `bin/x_token.json` and `bin/x_app.json` are never committed (listed in `.gitignore`).

---

## Scheduled automation (two macOS LaunchAgents)

The corpus runs two unattended jobs. Both use the Claude Code **subscription** (the
headless calls strip `ANTHROPIC_API_KEY`, so they bill the Max plan, NOT metered API).
Installed plists live on the local Mac only (`~/Library/LaunchAgents/`, NOT committed);
the repo ships only the templates + `automation/install_schedule.sh`. Run logs
(`raw/.scheduled_run.log`, `raw/.weekly_synthesis.log`) are gitignored.

### 1. `com.corpus.daily` — collect + ingest (nightly 02:00)

1. **Collection** — gmail (starred + 9 corpus labels), obsidian, pdf, youtube collectors run.
2. **Ingest** — headless Claude `/ingest-auto` processes up to `--max` inbox candidates
   (deterministically pre-filtered + **labeled-prioritized**, see `bin/ingest_candidates.py`).
3. **Reap** — `gmail_client.py reap-labels` un-labels + archives ingested labeled mail.
4. **Commit/push** — `corpus/` changes staged, committed, pushed (R10: never `raw/`).

- **Entrypoint:** `python3 bin/scheduled_run.py run` — installed args **`--max 50 --timeout 5400`**.
- **Schedule:** daily at **02:00** (chosen so it doesn't compete with daytime work).
  Asleep at 02:00 → launchd replays once on next wake (no flood).
- **Ingest model:** **Sonnet** (`SCHEDULED_RUN_INGEST_MODEL=claude-sonnet-4-6` in the plist
  `EnvironmentVariables`) — draws from a separate/larger weekly pool, preserving the scarce
  Opus weekly budget for interactive daytime work. Unset the env to revert to Opus.

### 2. `com.corpus.weekly-synthesis` — leftover-Opus synthesis (weekly Tue 13:00)

`bin/weekly_synthesis.py` — once a week, ~3h before the Opus weekly quota resets (user's reset:
Tue 15:59), spend leftover Opus on a bounded **Medium** synthesis+lint pass over the week's
newest ≤`--max-pages` (default 30) pages. **Probe-guarded**: fires a tiny Opus call first and
**skips** if Opus is rate-limited (remaining-credits isn't queryable, so it fails closed).
Runs on **Opus** (`claude-opus-4-8`); main-only TOCTOU-guarded commit.

- **Schedule:** Tuesday 13:00 (`StartCalendarInterval` Weekday=2). Manual preview:
  `python3 bin/weekly_synthesis.py --dry-run` (probe + page count, no pass/commit).

### Managing either job

`<job>` = `com.corpus.daily` or `com.corpus.weekly-synthesis`.

| Action | Command |
|---|---|
| Install / re-install daily | `bash automation/install_schedule.sh` |
| Install / re-install weekly | `CORPUS_JOB=weekly-synthesis bash automation/install_schedule.sh` |
| Uninstall | `[CORPUS_JOB=weekly-synthesis] bash automation/install_schedule.sh uninstall` |
| Verify registered | `launchctl print gui/$(id -u)/<job>` |
| Force a manual run | `launchctl kickstart -k gui/$(id -u)/<job>` |
| Disable (keep plist) | `launchctl disable gui/$(id -u)/<job>` |
| Tail run logs | `tail -f raw/.scheduled_run.log raw/.weekly_synthesis.log` |

**Tuning levers:** nightly throughput = `--max` in `com.corpus.daily.plist.template`'s
`ProgramArguments` (single-call ceiling — past ~50/call, prefer a batch loop); ingest model =
the `SCHEDULED_RUN_INGEST_MODEL` env block; synthesis timing/scope = the weekly template's
`Hour`/`Minute` and `weekly_synthesis.py --max-pages`. Re-run the installer after any edit.

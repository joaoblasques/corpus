# Spec: `collect-email` — Gmail → corpus source collector

- **Date:** 2026-06-09
- **Status:** approved design (pre-implementation)
- **Sub-project:** B (collection layer), collector #1 of the corpus-direction roadmap A → B → C
- **Author:** brainstormed with user; this doc is the validated design

---

## Context

The corpus (a Karpathy-style LLM wiki at `/Users/jonasblasques/Dev/corpus`) ingests sources from `raw/` into a synthesized markdown knowledge base. Today, sources arrive manually. This sub-project automates **collection** of one source — starred Gmail — into `raw/_inbox/`, where the existing deliberate ingest flow (the human/quality gate) takes over unchanged.

The guiding principle from the project brainstorm: **automate collection, keep processing deliberate.** This collector never writes to `corpus/`; it only deposits raw material into `raw/_inbox/`.

## Goal

A Claude Code skill, `/collect-email`, that on each run:
1. finds all starred Gmail messages,
2. writes each as a normalized markdown file into `raw/_inbox/`,
3. then de-stars and archives that email — **only after** the file is durably written.

Run manually first; later run via `/loop <interval> /collect-email` inside an active Claude Code session.

## Success criteria

- Starring an email and running `/collect-email` produces a correct markdown file in `raw/_inbox/` and leaves the email de-starred + archived in Gmail.
- A run that is interrupted after writing a file but before archiving does **not** duplicate that email on the next run (idempotent via `gmail_message_id`).
- A single malformed email does not abort the run; it is skipped, left starred, and reported.
- No write ever occurs to `corpus/` or to the user's Obsidian vault.

## Non-goals (explicitly out of v1)

- **Link-following** (article readability extraction, YouTube transcript fetch) → v1.1. v1 detects and records a dominant URL but does not fetch it.
- **The Obsidian collector** → separate spec, next in the B program.
- **True headless/cron operation** with no Claude Code session open → an S4 (scheduling) decision; see Risks.
- **Attachments / PDFs.**
- **Multi-account Gmail.**

## Architecture

- **Form:** a project skill at `.claude/skills/collect-email/SKILL.md`, versioned in the corpus repo.
- **Gmail access:** the claude.ai Gmail MCP connector already configured in this environment. Tool mapping:
  | Action | Tool | Notes |
  |---|---|---|
  | find starred | `mcp__claude_ai_Gmail__search_threads` | query: `is:starred` |
  | read content | `mcp__claude_ai_Gmail__get_thread` | subject, sender, date, body, message-id, URLs |
  | de-star | `mcp__claude_ai_Gmail__unlabel_message` | remove `STARRED` |
  | archive | `mcp__claude_ai_Gmail__unlabel_message` | remove `INBOX` |
  | resolve labels | `mcp__claude_ai_Gmail__list_labels` | if label IDs are needed |
- **Granularity:** search returns threads; star/label state is per-message. v1 processes each **starred message** within returned threads.
- **Invocation:** `/collect-email` (manual), then `/loop <interval> /collect-email` (cadence within a session).

## Behavior — one run

```
search Gmail `is:starred`
for each starred message:
   1. read full content (subject, from, date, body, gmail_message_id, URLs)
   2. dedup: if a raw file (in raw/_inbox/ or raw/email/) already has this
      gmail_message_id → skip to step 6 (retry archive only)
   3. write markdown → raw/_inbox/email-YYYY-MM-DD-<slug>.md
   4. verify the file exists on disk (read-back)
   5. (write confirmed)
   6. remove STARRED, then remove INBOX (archive) on the message
   7. record outcome in run tally
print summary: "<N> starred found · <M> collected · <K> skipped (dup) · <F> failed (left starred)"
list created files
```

If any step 1–4 fails for a message: skip it, leave it starred, record as failed, continue.
Step 6 is the only Gmail-mutating action and runs only after step 4 succeeds.

## Raw file format (`raw/_inbox/email-YYYY-MM-DD-<slug>.md`)

```yaml
---
channel: email
source: gmail
gmail_message_id: <id>        # dedup + traceability
from: <sender display + address>
subject: <subject>
date_received: YYYY-MM-DD
url: <dominant link if pointer, else omitted>
pointer: true | false         # body is essentially just a link?
collected_at: YYYY-MM-DD
---

<email body converted to markdown>
```

- **Filename:** `email-<date_received>-<slugified-subject>.md`, ASCII kebab-case slug, truncated to a sane length. On slug collision, append a short suffix from `gmail_message_id`.
- **Pointer detection (v1):** if the plain-text body is short and dominated by a single URL, set `pointer: true` and populate `url`. Body is still captured verbatim.

## Safety & idempotency

- **Ordering guarantee:** de-star/archive (step 6) happens strictly after the file is verified on disk (step 4). The raw `.md` is the durable artifact; Gmail *All Mail* retains the original regardless (archive ≠ delete) — two retained copies.
- **Idempotency key:** `gmail_message_id`. Partial-failure recovery: file written but archive failed → next run finds the email still starred *and* an existing raw file with that id → skips re-write, retries archive only.
- **Boundary:** the skill writes only to `raw/_inbox/`. It does not touch `corpus/` or the vault. It mutates Gmail state (label removal) only as specified.

## Error handling & reporting

- Per-message isolation: one failure never aborts the run.
- Failures leave the email starred (so it's retried next run) and are listed in the run summary with a short reason.
- Each run prints a one-line tally and the list of files created.

## Config change

Add an `email` channel to `corpus/_config.md`:
- Channel-labels table: `email` → `raw/email/`.
- Create `raw/email/` (with `.gitkeep`).
- Log a `config` entry in `corpus/_log.md`.

Collected files start in `raw/_inbox/`; the normal ingest flow (§8.1 Branch A) later moves them to `raw/email/`.

## Testing

1. Verify the Gmail connector + the four tools above are available (no inbox content accessed until this point, and only with user present).
2. User stars 2–3 real emails: one plain newsletter (body-is-content) and one that is essentially a single link (pointer).
3. Run `/collect-email` once, manually.
4. Verify: correct markdown in `raw/_inbox/`; `pointer`/`url` set correctly; emails de-starred + archived in Gmail; run summary accurate.
5. Re-run immediately: confirms 0 collected (all deduped), proving idempotency.

## Risks / open questions

- **Headless auth (deferred to S4):** the claude.ai Gmail connector is interactive; running `/collect-email` with no session open (true cron) may not have it. v1 runs via `/loop` inside a session, where it is available. If unattended operation is later required, graduate the Gmail fetch + mutation to a standalone script using the Gmail API (the brainstorm's Approach 2), keeping this skill for the judgment/extraction parts.
- **Thread vs message semantics:** if a thread has multiple starred messages, v1 processes each; confirm connector behavior during testing.
- **Body→markdown fidelity:** HTML-heavy marketing emails may convert messily; acceptable for v1 (body is captured; the human ingest step is the quality gate).
```

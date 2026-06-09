---
name: collect-email
description: Collect starred Gmail messages into the corpus raw/_inbox/ as markdown, then de-star and archive them. Run manually or via /loop. Use when the user wants to pull starred emails into the corpus pipeline.
---

# Collect Email

Capture every **starred** Gmail message into `raw/_inbox/` as a normalized markdown
file, then de-star and archive it. Collection only — never ingest into `corpus/`.

## Safety rules (non-negotiable)
- De-star/archive an email **only after** its markdown file is confirmed written.
- On any failure for one email: skip it, leave it starred, continue with the rest.
- Write only to `raw/_inbox/`. Never touch `corpus/` or the vault.

## Procedure

1. Find starred mail: call `mcp__claude_ai_Gmail__search_threads` with query `is:starred`.
   If none, report "0 starred" and stop.
2. For each thread, call `mcp__claude_ai_Gmail__get_thread` and identify the
   **starred message(s)** within it. Process each starred message:
   a. Extract: `message_id`, `from` (display + address), `subject`,
      `date_received` (YYYY-MM-DD), and the body as plain text/markdown.
   b. Write the body to a temp file, e.g. `/tmp/collect-email-body.md`.
   c. Run the deterministic writer (it handles dedup, pointer detection,
      frontmatter, filename, and the write):
      ```bash
      python3 bin/collect_email.py \
        --message-id "<message_id>" \
        --from "<from>" \
        --subject "<subject>" \
        --date "<date_received>" \
        --collected-at "$(date +%Y-%m-%d)" \
        --body-file /tmp/collect-email-body.md
      ```
   d. Parse the JSON it prints:
      - `{"status":"written", "path":...}` → confirm the file exists, then go to step 3.
      - `{"status":"duplicate"}` → already collected on a prior run; go straight to
        step 3 to finish archiving (idempotent retry).
      - anything else / error → record as failed, leave the email starred, skip step 3.
3. De-star and archive (only reached on written/duplicate):
   - `mcp__claude_ai_Gmail__unlabel_message` removing `STARRED`.
   - `mcp__claude_ai_Gmail__unlabel_message` removing `INBOX` (archive).
4. Report a one-line tally: `<N> starred found · <M> collected · <K> skipped (dup) · <F> failed (left starred)`, then list the created file paths.

## Notes
- This skill does NOT follow links inside emails (pointer emails are captured with
  their URL recorded in frontmatter; following is a future enhancement).
- Run via `/loop <interval> /collect-email` to probe on a cadence within an active
  Claude Code session (the Gmail connector is available there).
- After collection, run the normal corpus ingest on `raw/_inbox/` when you choose;
  ingest then routes files to `raw/email/`.

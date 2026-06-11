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

## Transport: owned Gmail credential (not the hosted connector)

Gmail access goes through `bin/gmail_client.py`, which uses the user's OWN Google
OAuth credential with `gmail.modify` scope. The hosted claude.ai Gmail connector is
**read-only** and cannot de-star/archive, so it is not used here. One-time setup
(`bin/credentials.json` + `python3 bin/gmail_client.py auth`) is documented in the
plan; if `bin/token.json` is missing, tell the user to run that auth step first.

`gmail_client.py run` performs the entire loop in code — search starred → write each
via `collect_email.py` → de-star/archive only after a confirmed write — so the safety
rules above are enforced by the program, not by following these steps by hand.

## Procedure

1. Preflight: confirm `bin/token.json` exists. If not, stop and tell the user to run
   `python3 bin/gmail_client.py auth` (one-time browser consent).
2. **Dry run first** (collects, does not touch Gmail):
   ```bash
   python3 bin/gmail_client.py run --dry-run
   ```
   Review the JSON tally and the written file paths in `raw/_inbox/`.
3. Real run (collects, then de-stars + archives each collected message):
   ```bash
   python3 bin/gmail_client.py run
   ```
   For a first cautious live run, cap it: `python3 bin/gmail_client.py run --max 1`.
4. Report the JSON tally it prints:
   `found · written · duplicate · failed · archived`, then list `paths`.
   - `written`/`duplicate` messages are archived (or, with `--dry-run`, left alone).
   - `failed` messages are left starred for a later retry (idempotent — dedup by
     `gmail_message_id` means re-running never double-writes).

## Notes
- Link-following is ON by default: useful links inside an email are ranked by
  learning-utility (Haiku, heuristic fallback), quality-floored, capped at 10, and
  captured into raw/web / raw/youtube with `via_email` provenance. Disable with
  `--no-links`; change the cap with `--max-links N`. Depth-1 only (links inside
  fetched pages are never followed).
- Run via `/loop <interval> /collect-email` to probe on a cadence. Because the
  transport is an owned credential (not the session connector), `run` also works
  headless — a future cron/CI path.
- After collection, run the normal corpus ingest on `raw/_inbox/` when you choose;
  ingest then routes files to `raw/email/`.

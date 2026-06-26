# Cloud Nightly Runbook (Phase 1 — GitHub loop)

The nightly corpus run executes as a Claude Code **Routine** in Anthropic's cloud,
billed against the Max plan (no metered API cost). Phase 1 runs the GitHub
collector end-to-end; Gmail/X/PDF/vault/YouTube arrive in later phases.

## Routine configuration (claude.ai/code/routines)

- **Name:** `corpus nightly`
- **Model:** Sonnet
- **Repository:** `corpus` (write access — needed for the nightly push to `main`)
- **Trigger:** Schedule → Daily → 02:00 (local tz). Minimum granularity is 1 hour.
- **Permissions:** enable **Allow unrestricted branch pushes** (the run commits to
  `main`, not a `claude/` branch).
- **Environment variables (secrets):**
  - `GH_TOKEN` — a fine-grained GitHub PAT with: read on starred repos' contents,
    and `contents: write` on the `corpus` repo (for the push). The `gh` CLI and
    `git push` both read it.
  - `SCHEDULED_RUN_INGEST_MODEL=claude-sonnet-4-6` — safety pin so any ingest
    defaults to Sonnet, never burning the weekly Opus cap.

## Routine prompt (paste verbatim)

> You are running the nightly corpus collection in this `corpus` repo, on `main`.
> Work autonomously per CLAUDE.md. Steps, in order:
> 1. Run `python3 bin/cloud_run.py collect --only github` and read its JSON report.
> 2. Ingest everything new in `raw/_inbox/` following CLAUDE.md §8.1 (route to
>    existing domains; do not invent new domains without the §9 bar; stamp sources;
>    update `corpus/_index.md` and append `corpus/_log.md`). Defer any gated
>    judgment to `raw/_inbox/_REVIEW.md` as usual.
> 3. Run `python3 bin/cloud_run.py commit-push --repo .` to publish `corpus/` and
>    the GitHub ledger to `main`.
> 4. Report a one-paragraph summary: repos collected, pages created/updated, and
>    the commit-push status. If any step exits non-zero, stop and report it as a
>    FAILED run — do not continue.

## Reading a run

- Success: `collect` reports `github` returncode 0; `commit-push` reports
  `pushed` (or `noop` if there were no new stars that night).
- The new corpus commit appears on `origin/main` as `chore(cloud-run): nightly …`.
- Confirm in account usage that the run drew on the **subscription**, not API spend.
- A failed step exits non-zero → the Routine run-history marks the run failed
  (Phase 1 has no email alert yet; that's Phase 2).

## Scope / not yet here

- Gmail, X (need collect-only + reap-strictly-after-push hardening — Phase 2).
- PDF via Drive API, Obsidian vault read-only clone + ledger — Phase 2.
- `raw/_pending/youtube/` hand-off + slim Mac feeder — Phase 3.
- Retiring the local `com.corpus.daily` job — Phase 4 (keep it running until the
  cloud loop is trusted; both are idempotent, so an overlap night is harmless —
  the ledger and source-state dedup prevent double-collection).

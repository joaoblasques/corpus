# Scheduled Collection & Ingestion — Requirements

> Date: 2026-06-12 · Track: Collection + Ingestion/synthesis (`STRATEGY.md`) · Status: ready for `ce-plan`

## Summary

A single **daily, local (MacBook/launchd) job** that keeps the corpus fed without manual triggering. It chains **collect → safe-subset auto-ingest → commit & push → report**. Collection (deterministic Python) is fully automated. Ingestion (agentic, with confirmation gates) auto-handles only *ungated* work and **defers anything needing human judgment to a review queue**. This operationalizes the `STRATEGY.md` **Backlog drain rate** metric: intake and synthesis run on a cadence instead of waiting for the user to sit down.

## Problem frame

The collection layer (3 collectors) and the v0.6 ingest pipeline are built and proven, but both run **manually, in an interactive session**. The corpus only advances when the user remembers to trigger collection and ingestion. The user is frequently away from the Mac (on their phone), so the backlog accumulates and the compounding bet under-delivers between sessions. Automating the chain closes that gap — the corpus drains its backlog on its own and only pulls the user in for the decisions that genuinely need a human.

## Key decisions

- **Ingestion is safe-subset auto-ingest, not fully unattended judgment.** The scheduled agent may do ungated work autonomously; it must defer gated decisions to a review queue. The user chose this over both "ingest on-demand" (too manual) and "fully unattended" (too much drift risk).
- **Execution is local-only.** Collectors need the user's local Gmail/YouTube OAuth tokens, the Obsidian vault, and `.env`; `raw/` is gitignored. Anthropic cloud routines (`/schedule`) can see none of these, so the entire chain runs on the MacBook via launchd. This is a forced constraint, not a preference.
- **Git posture is auto-commit + auto-push.** The user chose full hands-off over a local-only / human-checkpoint posture. **Consequence:** with no human review before the remote, the safe-subset gating boundary is the *sole* guardrail — so the job must **bias toward deferring to the review queue whenever coverage is uncertain**. Git history keeps every run revertable; the repo is private.
- **Reporting is repo-only.** No email/banner. A run summary lands in `corpus/_log.md` (committed/pushed); gated and failed items land in a gitignored review queue; the next interactive session surfaces the pending count.
- **One daily chained run**, not per-channel cadences — simplest, cheap, keeps backlog ≤ ~a day (longer only after the Mac has been asleep for a stretch).

## Requirements

### Scheduling & execution
- **R1** — A single job runs **once daily** on the MacBook via **launchd**, chaining the steps below in order. It needs no open Claude session.
- **R2** — The job is **single-flight**: a lock prevents a new run from starting while the previous run is still in progress (e.g., after the Mac wakes from a multi-day sleep into a large batch).
- **R3** — When the Mac is asleep at the scheduled time, the run executes **once on next wake** (launchd `StartCalendarInterval` semantics) — missed days coalesce into one catch-up run, not N stacked runs.

### Collection (deterministic)
- **R4** — The job runs the **email** and **obsidian** collectors automatically, writing new sources into `raw/_inbox/`. Per-channel failure is **isolated** — one collector failing does not abort the others or the ingest step (mirrors existing collector behavior).
- **R5** — The **youtube** collector is **wired into the job but is a no-op until its OAuth token exists**: when the token is absent it reports "not configured" and is skipped; it **auto-activates** once the user completes the pending YouTube OAuth setup — no schedule change required.

### Ingestion (safe-subset, agentic)
- **R6** — After collection, an agent runs the existing v0.6 Branch-A batch ingest over `raw/_inbox/` **non-interactively**, restricted to the **ungated subset**: route sources to **existing** domains, create/update entity & concept pages, dedup against the index, cross-link, and run lint.
- **R7** — The agent **must NOT** perform gated actions unattended. It **defers** (writes the source's disposition to the review queue, leaves the raw file unprocessed) when a source would require: a **new or provisional domain**, an **unusually large page cascade** (the §13 "20+ pages" pause), a **detected contradiction** needing a synthesis-page judgment, or a **PARA-native collision**. **When coverage/routing is uncertain, it defers rather than writes** (the auto-push guardrail principle).
- **R8** — The agent is **bounded**: a maximum batch size and a wall-clock timeout cap each run so an unattended agent cannot loop or run away. Work beyond the cap is left in `raw/_inbox/` for the next run (or the review queue).

### Git & persistence
- **R9** — Corpus changes from the ungated auto-ingest are **auto-committed and auto-pushed** each run with a clear, revertable `chore(auto-ingest)`-style message. The run summary in `corpus/_log.md` is committed/pushed with them.
- **R10** — Gated/failed items and the review queue stay **local and uncommitted** (they live under gitignored `raw/`), so only reviewed-by-gating corpus content reaches the remote.

### Reporting & review
- **R11** — Every run appends a summary to `corpus/_log.md` (a `config`/`ingest`-style entry): counts of collected · auto-ingested · deferred · failed, per channel.
- **R12** — Gated and failed items are written to a **gitignored review queue** (`raw/_inbox/_REVIEW.md` or similar) naming each deferred source and *why* it was deferred, so the user can act on it in a session.
- **R13** — A new interactive Claude session in the corpus **surfaces the pending state** ("N collected · M ingested · K awaiting decision") so the review queue is not silently forgotten.

## Key flows

1. **Nominal daily run** → acquire lock → run email + obsidian (+ youtube if configured) collectors → agent ingests the ungated subset of `raw/_inbox/` → auto-commit + push corpus changes + log summary → write any deferred/failed items to the review queue → release lock.
2. **Gated source encountered** → agent does not write the corpus change → records the source + reason in the review queue → leaves the raw file in `raw/_inbox/` for human-assisted ingest later → continues with the rest of the batch.
3. **Mac asleep for days** → launchd fires one catch-up run on wake → single large batch is ingested up to the R8 cap → remainder waits for the next run.
4. **Next interactive session** → corpus greets the user with the pending count → user reviews `_REVIEW.md`, makes the gated calls (new domains, collisions), and ingests the deferred sources with judgment.

## Acceptance examples

- **AE1 (clean daily run)** — New starred emails + new vault notes arrive; all route to existing domains → next morning they're collected, auto-ingested, committed, and pushed; `corpus/_log.md` shows the tally; review queue is empty.
- **AE2 (new-domain deferral)** — A cluster of sources fits no existing domain → auto-ingest writes nothing for them, lists them in `_REVIEW.md` as "needs new-domain decision," and still ingests the rest; user sees the pending item next session.
- **AE3 (collector failure isolated)** — The Gmail token is expired → the email leg reports failure in the run summary, obsidian still collects and ingests normally, the run completes.
- **AE4 (youtube auto-activation)** — Before OAuth: youtube leg logs "not configured" and is skipped. After the user completes OAuth: the *same* job starts collecting YouTube with no schedule edit.
- **AE5 (asleep catch-up)** — Mac asleep 3 days → one run on wake ingests the accumulated backlog up to the cap; overflow remains queued for the next run.

## Scope boundaries

**Deferred for later**
- The YouTube collector leg is active-but-deferred (no-op until OAuth completes) — wired now, no separate work.
- Email/macOS-banner notifications (repo-only reporting in v1; can add a channel later).
- Threshold/event-driven or multiple-times-daily cadence (start with once-daily; revisit if backlog regresses).

**Outside this feature's identity (for now)**
- Cloud/remote or multi-machine execution and sync — local single-Mac only.
- Scheduling the `/query` web-intake channel — `/query` stays interactive.
- Turning the *gated* decisions (new domains, collisions) into anything automated — those remain human, by design.

## Dependencies / assumptions

- **Reuses:** the three collectors (`bin/gmail_client.py`/`collect_email.py`, `collect_youtube.py`, `collect_obsidian.py`), the v0.6 Branch-A batch-ingest pipeline (CLAUDE.md §8.1), `corpus/_log.md`, `.env` (`ANTHROPIC_API_KEY`).
- **Assumption (planning to confirm):** the agentic ingestion runs via a **non-interactive Claude invocation** (headless `claude -p`, or equivalent) that loads CLAUDE.md and executes the batch pipeline under a **safe-subset instruction**; the deterministic collectors run as plain Python before it.
- **Assumption:** launchd (not cron) is the scheduler — it handles wake/catch-up and per-user agents cleanly on macOS.
- **Consequence:** auto-push means the gating boundary (R7) is the only pre-remote guardrail, so its definition must be conservative and "defer when uncertain" is a hard rule, not a preference.

## Success criteria

- The corpus advances **without any manual trigger**: a day's new email/vault content is collected, ungated-ingested, committed, and pushed unattended.
- **Zero unattended gated writes:** no new domain, collision resolution, or contradiction-synthesis ever lands on the remote without the user — they always route to the review queue.
- **No silent loss:** every deferred or failed source is recoverable from the review queue, and the next session surfaces the pending count.
- **Backlog drain rate** (the `STRATEGY.md` metric) becomes a moving daily number instead of a sit-down-dependent one.

## Outstanding questions

**Deferred to planning**
- The exact non-interactive Claude invocation and how the safe-subset instruction is delivered (skill vs prompt vs flag), including how it loads CLAUDE.md headlessly.
- The precise R8 bounds (max batch size, timeout) and how overflow is carried to the next run.
- launchd plist specifics (run time, lock mechanism, log file locations) and how the youtube no-op is detected (token presence check).
- Review-queue format/location (`raw/_inbox/_REVIEW.md` vs a dedicated path) and exactly how the next session surfaces the pending count.

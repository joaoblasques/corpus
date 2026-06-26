# Design: Migrate the nightly corpus run to Anthropic cloud (Max-billed)

- **Date:** 2026-06-26
- **Status:** Design — awaiting user review
- **Author:** Claude (Opus) + Jonas
- **Related:** `bin/scheduled_run.py`, `corpus/_config.md` (Scheduled automation), commit `d076808` (lock self-heal)

---

## 1. Motivation

The nightly pipeline (`com.corpus.daily`, 02:00) runs on a macOS LaunchAgent. It only
fires when the Mac is awake, and a stale single-flight lock silently blocked it for days
(fixed in `d076808`). The user wants the nightly run to happen **whether or not the Mac is
on**, using **only the Claude Max subscription** with **no metered API cost**.

**Primary goal (user-stated):** the Mac does not have to be on for the nightly run to happen.
**Hard constraint:** zero extra cost beyond the existing Max plan.

### Non-goals
- Not changing what the corpus *is* or how ingest routes/writes pages (§ CLAUDE.md unchanged).
- Not migrating the *weekly* Opus synthesis job (separate; can follow later).
- Not improving YouTube collection quality — only relocating what can move.

---

## 2. Key findings (researched 2026-06-26, official docs)

1. **Billing is favorable.** Claude Code **Routines** (scheduled cloud agents, managed via
   `/schedule`) run on Anthropic infrastructure and **draw down the Max subscription the same
   way interactive sessions do — no metered API charges.** Limit: 15 routine runs/day
   (we need 1/night). Source: code.claude.com/docs/en/routines.
2. **Cloud sandboxes cannot reach the local machine.** No local filesystem, no local browser
   cookies. Confirmed in docs. They *can* clone GitHub repos, run shell/Python, make outbound
   API calls, use per-environment **secrets (env vars)**, and push to GitHub.
3. **`raw/` is gitignored** — collected sources are never committed (only `corpus/` is). A
   stateless cloud sandbox therefore cannot see a local `raw/_inbox/`. The cloud run must
   **re-derive its inbox from live sources each night.**
4. **Collector → cloud feasibility:**

   | Collector | Cloud-feasible | Mechanism |
   |---|---|---|
   | Gmail | ✅ | Gmail API + OAuth token as secret |
   | GitHub | ✅ | GitHub API/token as secret (+ dedup ledger, see §4.3) |
   | X | ✅ | X API v2 OAuth token as secret |
   | PDF | ✅ (rework) | switch local Drive-sync folder → Google Drive API |
   | Obsidian vault | ✅ | clone `github.com/joaoblasques/second-brain` (vault is on GitHub) |
   | **YouTube** | ❌ | needs the Mac's **browser cookies** to beat YouTube's bot-gate |

---

## 3. Chosen approach — Hybrid (single cloud writer + Mac YouTube feeder)

The cloud is the **only** writer of `corpus/`. The Mac is demoted to a **YouTube feeder**: it
collects the one cookie-bound source and hands transcripts to the cloud through a tracked
queue. Everything else — collection, ingest, commit, push — happens in the cloud nightly,
independent of the Mac.

Rejected alternative (full-cloud): forcing YouTube into the cloud means dropping to API-only
captions and losing the just-recovered cookie/Whisper rescue path — it degrades the one
collector it touches. Rejected alternative (stay local + bulletproof): does not meet the
"Mac doesn't have to be on" goal.

---

## 4. Architecture

### 4.1 Components

```
┌─────────────────────────── Anthropic cloud (nightly Routine, Max-billed) ──────────────────────────┐
│  cloud_run agent session:                                                                           │
│   1. clone corpus repo + second-brain vault repo                                                    │
│   2. run 5 collectors (gmail, github, x, pdf→Drive API, obsidian→cloned vault) → raw/_inbox/        │
│   3. drain raw/_pending/youtube/ (committed by the Mac) into raw/_inbox/                             │
│   4. ingest-auto (agent performs routing/page-writing per CLAUDE.md)                                │
│   5. reap (un-star / un-bookmark / un-label / delete-vault-note) ; update github ledger             │
│   6. commit corpus/ + clear raw/_pending/youtube/ ; push corpus repo ; commit+push vault repo       │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘
        ▲ pending youtube transcripts (git)                         │ corpus pages, reaped vault notes (git)
        │                                                           ▼
┌─────────────────── Mac (only when on) ──────────────────┐   GitHub: corpus repo, second-brain repo
│  youtube feeder (slim launchd job, cookie-bound):       │
│   - collect playlist transcripts + whisper-rescue       │
│   - write NEW transcripts → raw/_pending/youtube/ (git) │
│   - commit + push that folder only                      │
└──────────────────────────────────────────────────────────┘
```

### 4.2 The cloud Routine
- Created by the user via `/schedule` (user-triggered, billed to Max). The routine prompt
  orchestrates the steps above. The **agent itself performs the ingest** in-session (no nested
  headless `claude` call — unlike today's `scheduled_run.py`).
- A new entrypoint **`bin/cloud_run.py`** runs the deterministic parts (clone, collectors,
  reap, commit, push) and emits a JSON report; the routine agent calls it, then performs the
  ingest step, then calls the commit/push step. (Split so the agent owns only the judgment
  step, matching today's local split.)
- Branch guard preserved: operate on `main` only.

### 4.3 Dedup without a local inbox
- **Source-state dedup (already cloud-safe):** Gmail (un-star/un-label), X (un-bookmark),
  Obsidian (reap vault note), PDF (move to `_processed` via Drive API). These mark "done" at
  the source, so a stateless re-fetch never re-collects.
- **GitHub needs a committed ledger** (stars stay in place). Add a tracked file
  **`automation/state/github_digested.txt`** (one `owner/name` per line). The collector reads
  it to skip already-digested repos and appends new ones. Tracked (not under `raw/`), tiny.

### 4.4 YouTube hand-off (the one tracked-`raw` exception)
- New tracked folder **`raw/_pending/youtube/`** (un-ignored in `.gitignore`; everything else
  under `raw/` stays ignored). Holds **only not-yet-ingested** transcripts.
- Mac feeder writes new transcripts here and pushes. Cloud run drains them into the working
  inbox, ingests, then **`git rm`s the folder's contents** and commits — the queue returns to
  empty. History and the ~962 blocked stubs remain local/gitignored as today.

### 4.5 Secrets / credential loading
Each cloud collector must read its token from an **environment variable** (a routine secret),
falling back to today's local file when the env var is absent (so local runs are unaffected):
- `GMAIL_TOKEN_JSON`, `GDRIVE_TOKEN_JSON`, `GITHUB_TOKEN`, `X_TOKEN_JSON` (+ any client creds).
- Small, uniform change per `bin/*_client.py`: "env var → temp file → existing code path."

---

## 5. Data flow (one nightly cloud run)
1. Clone `corpus` (main) + `second-brain` (default branch) into the sandbox.
2. Run collectors → write markdown into `raw/_inbox/` (sandbox-local, ephemeral).
3. `git -C second-brain` is the source for the obsidian collector; PDFs/emails/etc. come from APIs.
4. Move `raw/_pending/youtube/*` → `raw/_inbox/`.
5. Ingest-auto: agent routes to existing domains, writes/updates `corpus/` pages, defers gated
   judgment to `raw/_inbox/_REVIEW.md` (unchanged behavior).
6. Reap each source at its origin; append new repos to the github ledger.
7. `git add corpus/ automation/state/github_digested.txt`; `git rm raw/_pending/youtube/*`;
   commit; push corpus. Separately commit the vault deletions and push `second-brain`.

---

## 6. Error handling & reliability
- **Idempotency:** every step is idempotent. Collectors dedup at source; ingest is additive;
  a failed run leaves no half state (no commit on failure). Re-running re-derives cleanly.
- **Failure surfacing:** rely on Routine run-history + add an explicit failure notification
  (email to the user) when any step errors, so a silent stall (the very problem we're fixing)
  can't recur in the cloud.
- **Push races (cloud vs Mac feeder):** both push to GitHub. The Mac feeder only touches
  `raw/_pending/youtube/`; on push rejection it `pull --rebase` and retries. The cloud run is
  the sole `corpus/` writer, so corpus history stays linear.
- **Single-flight:** the daily-run cap (15/day) and one nightly schedule make concurrent cloud
  runs a non-issue; the dead-PID lock self-heal (`d076808`) protects any remaining local jobs.

---

## 7. Vault two-writer hazard (explicit risk)
Today the local reaper `git rm`s vault notes but **never commits** the vault (CLAUDE.md §2;
memory `never-commit-vault-from-code-session`). The cloud run has no human to commit, so it
**must commit + push** the vault deletions. Risk: the user's Obsidian Git-sync also writes the
vault → conflicts. **Mitigation:** cloud reaps + commits the vault on a `claude/reap` branch or
commits to default with `pull --rebase`; Obsidian sync pulls. This needs validation in Phase 2
and may warrant a CLAUDE.md §2 amendment (cloud reaper may commit the vault). **Open question
for the user:** is the vault safe for an automated committer, or should vault reaping stay
Mac-local (cloud just skips obsidian reap and re-collection is guarded by a ledger instead)?

---

## 8. Testing strategy
- **Unit:** env-var-token loading per collector (env present → used; absent → file fallback);
  github ledger read/skip/append; youtube hand-off drain+clear; `cloud_run.py` step reporting.
- **Integration (local dry-run):** run `cloud_run.py --dry-run` against the real repos with
  collectors mocked, asserting the JSON report and no writes outside allowed paths.
- **Live smoke:** Phase-1 routine on the 3 easy collectors, verified by one real nightly run
  committing to `corpus/` and confirmed **subscription-billed** (no API spend on the console).
- Keep the existing 400+ test suite green (note: some `scheduled_run` integration tests spawn
  real subprocesses and are slow — run the unit subset in CI-fast mode).

---

## 9. User one-time setup (cannot be automated — needs the user's accounts)
1. Create the nightly routine via `/schedule` (this is the billed, user-triggered step).
2. Add secrets to the routine environment: Gmail, Google Drive, GitHub, X tokens.
3. Grant the routine GitHub write to **both** `corpus` and `second-brain`.
4. Ensure the vault stays pushed to its GitHub remote (the "web counterpart").
5. Keep the Mac's slim YouTube launchd job installed (feeder only).

---

## 10. Phased rollout
- **Phase 0 (prereq):** collector env-var secret loading; github ledger; `bin/cloud_run.py`
  skeleton with `--dry-run`. Local, fully testable.
- **Phase 1 (prove billing + loop):** routine running gmail + github + x → ingest → commit/push.
  Confirm Max-billed, no API spend. Smallest end-to-end slice.
- **Phase 2 (Drive + vault):** PDF via Drive API; Obsidian via vault clone + reap (resolve the
  §7 two-writer question first).
- **Phase 3 (YouTube hand-off):** `raw/_pending/youtube/` queue; slim the Mac launchd job to
  feeder-only; cloud drains + clears the queue.
- **Phase 4 (decommission):** retire the local `com.corpus.daily` collect+ingest once the cloud
  run is trusted; keep only the YouTube feeder locally.

---

## 11. Open questions
1. **Vault committer (§7):** OK for the cloud to commit+push vault note deletions, or keep
   vault reaping Mac-local?
2. **Google auth:** reuse one Google OAuth client for both Gmail + Drive, or separate?
3. **GitHub identity for the cloud pushes:** the routine's built-in GitHub connection, or a
   dedicated bot PAT?
4. **Failure notification channel:** email is simplest — acceptable, or prefer another?

# Gardener (Stub-Expansion) — Design Spec

> Date: 2026-06-19
> Status: **design approved** (decisions locked); ready for implementation plan
> Parent: [Custodian vision](2026-06-19-custodian-vision-design.md) §7.2 · runs on the [harness](2026-06-19-custodian-harness-design.md).

## 1. Scope

The first Custodian mode: an **on-demand, manually-run** loop that expands the corpus's **stub
pages** into cited `draft` pages from their own sources. `bin/gardener.py` is thin — it supplies
`next_action` / `execute` / `constraints` + a custom verifier to `custodian.run_loop`, which carries
all the guarding/governance/commit/digest.

**In v1:** stub expansion only, inside a prioritized-worklist frame so `integrity-fix` / `orphan-link`
/ `dedup` slot in later as new worklist branches. Sonnet (subscription); main-only auto-commit.

**Out of scope (follow-ups):** integrity/orphan/dedup handlers; wiring into the 2 AM job (v1 is
manual so the first runs are watchable). The user chose manual-run + lint+content-critic governance.

## 2. What the Gardener supplies to `run_loop`

### 2.1 `next_action() -> stub | None` — the worklist
- Collect corpus pages with `status: stub` (skip catalog `_*` files).
- **Pre-filter to expandable stubs:** keep only those whose `sources:` list ≥1 file that exists on
  disk and is non-empty. Stubs with no usable source are NOT returned — they are collected and
  **queued once** at run start: `enqueue_review("stub-no-source", {pages:[…]})`.
- **Rank** expandable stubs by **inbound wikilink count desc, then `created` asc** (most-referenced
  thin pages first). Inbound count = occurrences of `[[<domain>/<slug>` across `corpus/`.
- Track **attempted** stubs in a run-local set; `next_action` returns the next un-attempted ranked
  stub (marking it attempted) and `None` when none remain → harness stops `converged_dry`.

### 2.2 `execute(stub, constraints) -> Result` — one expansion
- Read the stub page + the on-disk text of its cited sources.
- One headless **Sonnet** call (subscription; strips `ANTHROPIC_API_KEY`): "Expand this stub into a
  `draft` from ONLY its cited sources. §7-strict: every non-trivial claim cited, ≤25-word quotes (max
  one per source per page), NO fabrication, no claim absent from the sources. Keep CLAUDE.md §3/§4/§14
  form. Flip `status: stub`→`draft` and bump `updated`."
- Returns `Result(changed_paths=[stub_path], usage=<usage block>, errors=[…] on failure)`. On a
  model error / empty output it returns `changed_paths=[]` + an error note (the loop continues to the
  next stub — see §4 harness refinement).

### 2.3 `constraints` (re-injected each iteration)
"Edit only `corpus/`. Every non-trivial claim cites a source (§7). ≤25-word quotes. NEVER invent
claims not present in the cited sources. Follow CLAUDE.md."

### 2.4 `gardener_verify(changed_paths) -> Verdict` — lint + content-critic
Passed to `run_loop` as `_verify`. Two gates, BOTH must pass:
1. **lint** — `custodian.verify_gate(changed_paths)` (no broken citations/wikilinks on the page).
2. **content-critic** — one headless **Sonnet** call reading the expanded page + its cited sources'
   text: "Does EVERY new claim trace to a statement in a source actually cited on this page? List any
   claim that is unsupported, misattributed, or fabricated." `ok` only if the critic finds none.
`Verdict.ok = lint_ok AND critic_ok`; `notes` carries the critic's findings.
The harness then governs: pass → auto-commit; fail → revert the page + `enqueue_review` with the
critic's notes. (This realizes the user's "lint + content-critic, then auto-commit" choice.)

## 3. CLI & run

`python3 bin/gardener.py run [--max N] [--dry-run]`:
- main-only (reuse `sr._on_main`); acquires its own lock (`raw/.gardener.lock`).
- `--dry-run`: print the ranked worklist (expandable + no-source counts) and exit — no model calls,
  no writes.
- `run`: build `Budget` + `Caps` (default `max_pages_touched = min(stubs, 10)`, a Sonnet token
  budget, `wall_clock`), call `custodian.run_loop(next_action, execute, constraints, budget, caps,
  label="gardener", _verify=gardener_verify)`, print its summary JSON.
- Model: Sonnet for both expand and critic (`GARDENER_MODEL` env override; default `claude-sonnet-4-6`).

## 4. Harness refinement (revealed by this first worklist mode)

`run_loop`'s current no-progress rule is `if not result.changed_paths or fp == last_fp:` — it stops on
ANY single empty-change iteration. That's correct for one-shot modes but wrong for a **worklist**: one
stub that fails to expand would halt the whole run (and, being still a stub, re-rank first next run →
permanent stall). **Change the rule to repeat-fingerprint only:** `if fp == last_fp:`. Convergence then
comes from `next_action() → None`; a single failed iteration continues to the next stub; two
*consecutive identical* iterations (incl. two empties) still stop (runaway safety). Update the
affected `run_loop` test accordingly. (Small, well-scoped; keeps all other harness behavior.)

## 5. Caps, cost, safety

- **Sonnet only** (expand + critic) — protects the Opus weekly budget; subscription, not API.
- **Bounded:** `max_pages_touched` cap + token `Budget` + `wall_clock`; one stub per iteration.
- **Safety inherited from the harness:** main-only commits; revert-changed-path-only on verify fail;
  immutable `raw/`; digest of every action; the content-critic blocks fabrication before commit.
- **No L2 / no rule edits:** the Gardener only edits the stub pages it expands (auto-tier content).

## 6. Testing (drives the plan)

- **worklist:** `next_action` finds stubs, pre-filters unexpandable (no/empty source) → queued, ranks
  by inbound-count then created, marks attempted, returns `None` when exhausted (fake corpus dir).
- **execute:** builds the right prompt incl. source text; returns `Result` with the stub path; mock the
  headless call; failure path returns `changed_paths=[]` + error.
- **gardener_verify:** ok only when lint clean AND critic clean; critic-fail → `ok=False` with notes
  (inject fake lint + fake critic).
- **harness refinement:** `run_loop` no longer stops on a single empty-change iteration; still stops on
  repeat fingerprint and on `next_action→None` (update existing run_loop tests).
- **CLI:** `--dry-run` lists worklist, no model calls; `run` wires `run_loop` (mock it) and prints the
  summary; main-only guard.
- All seams injected — no network/git in tests.

## 7. Decisions locked
1. v1 = stub-expansion only, extensible worklist.
2. Verify = lint + content-critic; pass → auto-commit, fail → review queue.
3. Run = on-demand CLI (manual); nightly wiring is a follow-up.
4. Stub ranking = inbound-links desc, created asc; unexpandable stubs queued, not attempted.
5. Sonnet for expand + critic; main-only; harness no-progress refined to repeat-fingerprint.

## 8. Risks
| Risk | Mitigation |
|---|---|
| Fabricated/misattributed claim lands | content-critic gate before commit; §7 constraints; lint; digest + git revert |
| One bad stub halts the run | §4 harness refinement (single empty iteration no longer stops) |
| Expansion drifts off the sources | execute reads ONLY the page's cited sources; constraints re-injected each iteration |
| Cost runaway | Sonnet only; `max_pages_touched` + token Budget + wall-clock caps |
| Stub with no real source | pre-filtered out of the loop + queued for manual attention |

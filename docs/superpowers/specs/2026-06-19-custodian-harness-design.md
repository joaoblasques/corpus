# Custodian Harness — Design Spec

> Date: 2026-06-19
> Status: **design approved** (decisions locked); ready for implementation plan
> Parent: [the Custodian vision](2026-06-19-custodian-vision-design.md) — this is buildable unit #1 (§7.1).

## 1. Scope

Build the **shared toolkit** every Custodian mode plugs into: `bin/custodian.py`, a module of
well-tested helper functions + a `run_loop` orchestrator, in the style of `scheduled_run.py`'s
helpers (no class hierarchy). Plus a trivial **smoke mode** that drives the full loop end-to-end to
prove the wiring. **No real mode is built here** — Gardener / Adaptive Ingest / Dreamer are separate
specs; this is the engine they share.

**Out of scope (later specs):** Gardener's worklist & actions, real ingestion, the Dreamer,
L2 layout, the heuristics store. The harness only provides the loop, the guardrails, and governance.

## 2. The toolkit API (`bin/custodian.py`)

Reuses from `scheduled_run`: `acquire_lock`/`release_lock`, `current_branch`/`_on_main`
(main-only TOCTOU), and the subscription headless-Claude invocation pattern (strips
`ANTHROPIC_API_KEY`, `--output-format json` so `usage` is parseable). New surface:

```python
class Budget:
    """Token budget vs a cap. Unit = output_tokens (dominant cost driver)."""
    def __init__(self, max_output_tokens: int | None): ...
    def add(self, usage: dict) -> None      # usage = a headless result's "usage" block
    def spent(self) -> int
    def remaining(self) -> int              # math.inf when max is None
    def exhausted(self) -> bool             # spent >= max (always False when max is None)

@dataclass
class Caps:
    max_iterations: int = 25
    max_pages_touched: int = 40             # generalizes §13's "20+ pages" alarm
    wall_clock_s: int = 3600

@dataclass
class Verdict:
    ok: bool
    broken_citations: int
    broken_wikilinks: int
    notes: list[str]

@dataclass
class Result:                               # what a mode's execute() returns
    changed_paths: list[str]                # corpus/ files this iteration wrote
    usage: dict                             # headless "usage" block (for Budget)
    proposals: list[dict]                   # rule/heuristic/self-improvement proposals (never auto-applied)
    errors: list[str]

def fingerprint(changed_paths: list[str], errors: list[str]) -> str
def verify_gate(changed_paths: list[str], *, _lint=None) -> Verdict
def govern(verdict: Verdict, changed_paths: list[str], *, reversible: bool, _run=None) -> dict
def enqueue_review(kind: str, detail: dict, *, path=None) -> None        # → corpus/_review_queue.md
def write_digest(run_id: str, label: str, entries: list[dict], *, path=None) -> None  # → corpus/_digest.md
def run_loop(*, next_action, execute, constraints, budget, caps, label,
             _now=None, _run=None) -> dict
```

## 3. The `run_loop` contract

A mode supplies exactly three things; the harness does everything else:
- `next_action() -> action | None` — pick the highest-value worklist item. **`None` ⇒ dry ⇒ converged-stop.**
- `execute(action, constraints) -> Result` — perform ONE bounded batch (typically a headless Claude
  call, Sonnet by default). Returns the `Result` dataclass.
- `constraints: str` — the binding rules (§2 path isolation, §7 provenance) **re-injected into every
  iteration** (drift reinforcement).

**Algorithm (per iteration):**
```
for i in range(caps.max_iterations):
    if budget.exhausted():            stop("budget");        break
    if wall_clock_exceeded:           stop("wall_clock");    break
    action = next_action()
    if action is None:                stop("converged_dry"); break
    result = execute(action, constraints)
    budget.add(result.usage)
    if (touched += len(result.changed_paths)) > caps.max_pages_touched:
                                      stop("max_pages");     break
    fp = fingerprint(result.changed_paths, result.errors)
    if not result.changed_paths or fp == last_fp:
                                      stop("no_progress");   break   # nothing changed / looping
    last_fp = fp
    verdict = verify_gate(result.changed_paths)
    gov = govern(verdict, result.changed_paths, reversible=True)
    for p in result.proposals: enqueue_review("proposal", p)
    entries.append({action, verdict, gov})
write_digest(run_id, label, entries)
finalize_commit()   # commit the catalog files (_digest.md, _review_queue.md) on main so the
                    # digest + any queued notes ALWAYS persist — even if every iteration reverted
return {label, iterations, stop_reason, committed, queued, spent, entries-summary}
```

`finalize_commit` stages + commits only `corpus/_digest.md` and `corpus/_review_queue.md` (main-only
TOCTOU), separate from per-iteration content commits, so the control surface is never lost.

**Watchdog** is realized by composition (no separate process — YAGNI): the per-`execute` headless
timeout + the `wall_clock_s` cap + the `no_progress` fingerprint stop together guarantee termination.

## 4. Governance mechanic (locked)

- **corpus/ changes pass `verify_gate` (and reversible)** → `govern` stages the changed paths +
  commits (main-only). *Auto tier.*
- **corpus/ changes FAIL `verify_gate`** → `govern` runs `git checkout -- <changed_paths>` (revert)
  and `enqueue_review("verify-failed", …)` with what was attempted + why. **Nothing broken lands on main.**
- **`proposals`** (rule/heuristic/self-improvement) → never committed as rules → `enqueue_review("proposal", …)`.

`verify_gate` runs `corpus_lint.lint()` and **attributes** failures: the verdict is `ok=False` only if
a *changed* path is the SOURCE of a broken citation/wikilink (pre-existing breakage elsewhere doesn't
fail an unrelated iteration). `corpus/_review_queue.md` and `corpus/_digest.md` are catalog files
(underscore-prefixed, committed, append-only, newest-last like `_log.md`).

## 5. Smoke mode (validation)

A trivial mode in the same module (or `bin/custodian_smoke.py`) + a `python3 bin/custodian.py --smoke`
entrypoint: `next_action` yields one dummy action then `None`; `execute` returns a `Result` with no
`changed_paths`. Proves the loop runs end-to-end (lock → iterate → converged_dry stop → digest) on
`main` without touching corpus content. Used by an integration test and as a live wiring check.

## 6. Testing (unit, per helper — drives the TDD plan)

- **Budget:** `add` accumulates `output_tokens`; `remaining`/`exhausted` correct; `None` cap ⇒ infinite.
- **Caps:** dataclass defaults; `run_loop` honors `max_iterations`, `max_pages_touched`, `wall_clock_s`.
- **fingerprint:** identical (paths, errors) ⇒ identical hash; different ⇒ different; order-insensitive on paths.
- **verify_gate:** clean changed pages ⇒ `ok=True`; a changed page that sources a broken citation ⇒
  `ok=False` (inject a fake lint report); pre-existing breakage in an *unchanged* page ⇒ still `ok=True`.
- **govern:** pass+reversible ⇒ stages+commits (mock `_run`, assert `git commit`); fail ⇒ `git checkout --`
  on the changed paths + a review-queue entry, NO commit.
- **enqueue_review / write_digest:** append a structured entry to the catalog file (tmp path).
- **run_loop:** stops on `converged_dry` (next_action→None), on `budget`, on `no_progress` (repeat fp /
  empty changes), on `max_iterations`; routes `proposals` to the queue; reverts on verify-fail; returns
  a correct summary. All via injected `next_action`/`execute`/`budget`/`_run` (no network, no real git).
- **smoke integration:** `--smoke` exits 0, writes a digest, makes no commit.

## 7. Decisions locked

1. Toolkit of functions + `run_loop(next_action, execute, …)` callbacks (no Mode class).
2. Verify-fail ⇒ revert-and-queue (`main` always clean).
3. Scope = toolkit + smoke mode; Gardener is the next spec.
4. Budget unit = `output_tokens`; default Caps = 25 iters / 40 pages / 3600 s (conservative, overridable).
5. Control-surface files: `corpus/_review_queue.md` (review tier) + `corpus/_digest.md` (digest), both
   committed catalog files.

## 8. Risks

| Risk | Mitigation |
|---|---|
| `verify_gate` mis-attributes a failure to the wrong iteration | Attribute only to *changed* source paths; pre-existing breakage ignored |
| `git checkout --` reverts more than intended | Revert ONLY the iteration's `changed_paths` (never `.`); corpus/-only by construction |
| Budget metric (`output_tokens`) understates true cost | Acceptable proxy for v1; cap is conservative; revisit if needed |
| A mode's `execute` hangs | Per-call headless `--timeout` + `wall_clock_s` cap |
| Smoke/real mode accidentally commits off `main` | Reuse `scheduled_run._on_main` TOCTOU guard before every commit |

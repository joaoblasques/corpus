# The Custodian — Autonomous Corpus Runtime (Vision / Architecture)

> Date: 2026-06-19
> Status: **vision approved** (umbrella doc); decomposes into per-pillar specs (see §7)
> Type: overarching architecture. Implementation detail lives in the per-pillar specs, not here.

## 1. Problem & intent

The corpus today is a *compounding* knowledge base with strong discipline (immutable `raw/`,
§7 provenance, `corpus_ingested` idempotency, `corpus_lint.py`, scheduled collect→ingest→reap,
a weekly Opus synthesis pass). It is **driven** — it acts when scheduled or asked. The user wants
it to become **self-driving** along three axes:

1. **Continuous iteration** — managed agents that loop to keep the corpus tended and drained.
2. **Adaptive workflows** — ingestion/synthesis that changes its plan mid-run based on what it finds.
3. **Dream** — agents that learn and consolidate while idle, and improve their own heuristics over time.

This document defines the **single architecture** that delivers all three safely, and the order to build it.

**North star:** a personal Body of Knowledge that tends itself, ingests smarter over time, and
measurably gets better at its own job — while remaining auditable, provenance-clean, cost-bounded,
and never able to silently rewrite its own operating rules.

## 2. The four-layer data model

The research's non-negotiable foundation is an **immutable raw log + mutable derived layer**, and
**reading from raw, never from derived** (to prevent self-reinforcing error). The corpus already has
the bottom two layers; the Custodian adds the third plus an audit surface.

| Layer | Contents | Mutability | Role |
|---|---|---|---|
| **L0 `raw/`** | source documents | **immutable** (stamp-only per §2) | audit log + recovery surface |
| **L1 `corpus/`** | derived knowledge pages | mutable, provenance-cited (§7) | the Body of Knowledge |
| **L2 learned** | cross-page consolidations (MOC / meta-synthesis pages) **+** an agent-owned heuristics store | mutable, *derived from L0/L1* | what the system abstracts & learns — **never authoritative** |
| **Audit** | run digests, `corpus/_review_queue.md`, run logs | append-only | how the human stays in control |

**Invariants (enforced in code, not prompt):**
- Agents READ from L0/L1; they MUST NOT treat L2 as a source of truth (anti-self-reinforcement).
- `CLAUDE.md` is **human-owned**. Learned heuristics live in their own agent-owned store (L2) that
  ingest *consults*; a heuristic graduates into `CLAUDE.md` only on explicit human approval.
- L2 consolidation pages cite L1/L0 like any other page (§7 provenance applies to learned content too).

## 3. The Custodian harness (shared runtime)

One runtime (extending `bin/scheduled_run.py`'s proven patterns: lock, main-only TOCTOU commit,
subscription auth, run logging) that **all three modes plug into**. It carries every guardrail the
research flagged as mandatory. No mode re-implements these.

- **Hard caps in code** — `max_steps`, `max_pages_touched`, `max_tokens`, wall-clock. The canonical
  $47k-incident lesson: prompt-level limits are insufficient; caps are enforced by the harness.
- **Budget envelope** — per-run token budget; **Sonnet by default, Opus only on escalation/harvest**
  (the existing model split). A run switches to "thin mode" (no synthesis) as budget nears exhaustion.
- **Convergence + fingerprint stop** — halt when `hash(sources, pages_written, errors)` repeats
  across rounds (definitive no-progress) or a goal-distance metric < ε — not merely an iteration count.
- **Verifier gate** — `corpus_lint.py` (broken citations/wikilinks/orphans) + §7 provenance check.
  A write that fails the verifier is never auto-committed.
- **Reversibility check** — content edits under `corpus/` are reversible (git); edits to operating
  rules / the heuristics store's *promotion* / anything outside `corpus/` are treated as irreversible.
- **Tiered governance router** (see §4) — verifier + reversibility decide auto-commit vs review queue.
- **Drift reinforcement** — re-inject the binding constraints (§2 path isolation, §7 provenance) at
  the start of each loop iteration / cluster worker, not just at session start (counters measured drift).
- **Watchdog** — a no-progress timer escalates/kills a stalled run rather than waiting for self-detection.
- **Run digest** — every run appends a structured "what I did" entry to the audit surface.

## 4. Governance — tiered by reversibility + verifier

Every agent write flows through one decision:

```
write → verifier(lint + provenance) AND reversibility-check
  ├─ pass + reversible            → auto-commit (corpus/ only, main-only)   [AUTO TIER]
  └─ fail OR irreversible OR
     rule/self-modifying          → append to corpus/_review_queue.md       [REVIEW TIER]
```

- **Auto tier:** routine content work — ingest, lint-fix, dedup, stub expansion, L2 consolidation
  pages that pass provenance. Hands-off.
- **Review tier:** anything that fails verification, touches operating rules, or is a self-improvement
  proposal. The human clears the queue (the same motion already used for ingest deferrals).
- **Control surface:** a single **"while you were away" digest** (one log + optionally surfaced on
  return) — what each mode did, what's queued, what proposals await sign-off. One pane of glass.

## 5. The three modes

### 5.1 🌱 Gardener — continuous loop (Sonnet; nightly + on-demand)
Picks the highest-value action from a prioritized worklist and loops:
*drain ingest backlog → fix lint → expand stale stubs → merge duplicate entities → re-link orphans
→ refresh stale claims.* Each iteration = one bounded batch → verify → auto-commit if clean.
**Stops** on dry worklist, fingerprint no-progress, or budget. All actions are reversible +
lint-verified → auto tier.
- *Output:* steadily cleaner/fuller corpus + a digest line.
- *Subsumes* the previously-discussed "nightly drain-loop."

### 5.2 🔀 Adaptive Ingest — dynamic workflow (Sonnet w/ Opus escalation)
Makes the §8.1 batch pipeline self-sizing:
- **Dynamic fan-out** — after survey/cluster, spawn workers by cluster richness (dense → more; thin → defer).
- **Completeness-critic** — per cluster, loop-until-dry, capped at K rounds, critic must cite specific
  missed entities to continue.
- **Router** — extractor chosen by source type (youtube→timestamp-aware, pdf→citation-aware, digest→link-follow).
- **Escalation** — Sonnet handles routine extraction; escalate to **Opus only** for ambiguous
  entity-resolution, contradiction synthesis, or low-confidence pages.
- *Output:* better, cheaper, more thorough ingestion; fewer deferrals; convergence by budget construction.

### 5.3 🌙 Dreamer — learn while idle (tiered Opus; weekly harvest is v0)
Tiered cadence — daily-light (Sonnet) / weekly (Opus, exists) / monthly-meta (Opus, deeper). Two jobs:
- **(a) Consolidation → L2** *(auto tier)* — when a domain crosses an activity threshold
  (importance-weighted, per Generative Agents), cluster its recent pages and abstract recurring themes
  into MOC / meta-synthesis pages. Reads L0/L1, writes L2, pre-write contradiction check (§7.1).
- **(b) Self-improvement → heuristics store** *(review tier — always)* — reflect on `_log.md`,
  deferrals, and lint history to spot patterns ("keeps deferring dbt teasers → propose a routing rule";
  "ingest prompt missed X → propose a tweak"). Writes **proposals** to the agent-owned heuristics store
  that ingest consults; graduating one into `CLAUDE.md` is always the human's call.
- *Strict guardrails:* immutable raw, **read-from-raw-never-from-L2**, verifier-gated, probe-guarded
  Opus (existing pattern), self-improvement never auto-applied to rules, bounded consolidation depth.

## 6. Research grounding

Three parallel research passes (2026-06-19) informed this design; key load-bearing findings:

- **Loops:** ReAct / Reflexion / Plan-and-Execute are mature; the decisive lesson is *stopping* —
  code-level hard caps (the Nov-2025 **$47k** unbounded-loop incident), **fingerprint loop-detection**,
  convergence conditions, and **instruction reinforcement** against measured "agent drift" (~42% decay).
- **Adaptive:** plan-emit-**replan**, orchestrator + **dynamic fan-out** (LangGraph `Send`),
  **completeness-critic**, **escalation** (cheap→expensive). Anthropic's *Building Effective Agents*:
  add dynamism only where the task needs it (adaptive can 3–5× cost). Adaptive wins when output shape
  is unknown until data is read — exactly ingest.
- **Dream:** **Letta sleep-time compute** (background memory rewrite; ~2.5× cost reduction reported),
  **Generative Agents reflection** (importance-weighted abstraction), **Reflexion** (learn from own logs),
  tiered time-boundary consolidation. Mandatory rails: **immutable raw + mutable derived**,
  **read-from-raw-not-derived**, **pre-write contradiction checks**, **gate self-improvement behind a
  verifier** — never accept self-assessed quality alone.

Sources (selected): Anthropic *Building Effective Agents*; ReAct (arXiv 2210.03629); Reflexion
(arXiv 2303.11366); Plan-and-Solve (arXiv 2305.04091); Generative Agents (Park et al. 2023); Letta
sleep-time compute (letta.com/blog/sleep-time-compute); LangGraph `Send`/persistence docs. *(A few
very-recent papers surfaced by the research agents should be re-verified before being cited in a
buildable spec.)*

**The corpus is unusually well-positioned:** the research's "essential safety substrate" — immutable
source log, idempotency keys, pre-write contradiction handling, a verifier, change caps — is *already*
in CLAUDE.md. The Custodian formalizes and automates what the schema already implies.

## 7. Build decomposition (each → its own spec → plan → build)

1. **Custodian harness** *(foundation)* — caps, budget, fingerprint/convergence, verifier-gate,
   reversibility router, review queue, drift-reinforcement, watchdog, digest. Everything plugs in here.
2. **Gardener** — first application; lowest risk; subsumes the nightly drain-loop.
3. **Adaptive Ingest** — upgrade the §8.1 pipeline.
4. **Dreamer** — `4a` consolidation, then `4b` self-improvement (two sub-specs); built last on the
   proven harness.

Each sub-spec is brainstormed and written separately (this doc is the umbrella they share). No code
is written from this vision doc directly.

## 8. Risks & mitigations (carried into every sub-spec)

| Risk | Mitigation (harness-level unless noted) |
|---|---|
| Runaway loop / cost | Hard code caps; budget envelope; fingerprint stop; watchdog |
| Agent drift over long runs | Instruction reinforcement each iteration; state-validation checkpoints |
| Self-reinforcing error | Read L0/L1 never L2; consolidation cites raw; self-improvement is proposal-only |
| Semantic drift in consolidation | Immutable raw; pre-write contradiction check (§7.1); bounded depth |
| Silent rule rewrite | CLAUDE.md human-owned; heuristics store consulted-not-authoritative; promotion gated |
| Over-processing (invasive edits) | §13 "20+ pages" alarm as a hard cap; review tier for large diffs |
| Cost runaway from adaptive fan-out | Pre-flight budget estimate; max-workers cap; thin-mode fallback |
| Prompt injection via sources | Treat fetched content as data, not instructions; never inject raw bodies into the orchestrator |

## 9. Open questions (resolved per sub-spec, not here)

- Gardener worklist prioritization function (what's "highest value"?).
- Adaptive Ingest's confidence metric that triggers Opus escalation.
- L2 layout (where consolidation/MOC pages and the heuristics store physically live under `corpus/`).
- Digest delivery (passive log vs surfaced-on-return vs a scheduled summary).
- Cadence knobs for the Dreamer tiers.

---
*This vision is the shared frame. The first buildable unit is the Custodian harness (§7.1).*

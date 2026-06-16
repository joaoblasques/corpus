---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/web/long-running-agents.md
    channel: web
    ingested_at: 2026-06-16
aliases:
  - long-running agent
  - long-running agents
  - long-running execution
  - persistent agency
  - long-horizon reasoning
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-16
updated: 2026-06-16
---

# Long-Running Agents

**TL;DR.** A long-running agent "can keep making progress over hours, days, or weeks... across many context windows and sandboxes, recover from failure, leave structured artifacts behind, and resume where it left off." [^src1] It supersedes the chat-window-with-a-loop paradigm, which has a ceiling: the model forgets, declares tasks complete prematurely, and reintroduces fixed bugs [^src1]. The engineering centers on a state layer living *outside* the model's context window plus designed session-to-session handoffs [^src1]. Google, Anthropic, and Cursor have converged on the same shape: separate the model loop from the execution sandbox from the durable session log [^src1].

## Three meanings of "long-running"

The term blurs three distinct things [^src1]:

- **Long-horizon reasoning** — planning/executing over many dependent steps; mostly a model-quality story. METR's time-horizon metric (length of task a model completes at 50% reliability) has doubled roughly every seven months since 2019; on that curve frontier agents hit day-scale tasks by 2028 and year-scale by 2034 [^src1].
- **Long-running execution** — the process runs for hours or days, with the model invoked thousands of times; mostly a [[ai-engineering/agent-harness|harness]] story [^src1].
- **Persistent agency** — an identity that outlives any single task, accumulating memory and preferences; the "Memory Bank" flavor [^src1].

Production agents blend all three, but the engineering problems and the products that solve them differ [^src1].

## Why it matters

- **Economic phase change.** A ten-minute agent answers a question; a ten-hour agent can own a feature or a six-quarter-backlog migration [^src1]. Anthropic reported 30+ hours of autonomous coding in internal tests, including one run producing an 11,000-line Slack-style app [^src1].
- **Persistence changes what the agent is.** A stateless agent answers and disappears; a long-running one accumulates context across weeks [^src1]. Anthropic's Project Vend ran a Claude instance as an actual vending business for a month, surfacing the "weird coherence problems" of maintaining identity across weeks rather than turns [^src1].

## The three walls

Long-running designs are mostly answers to three recurring problems [^src1]:

1. **Finite context.** Even a 1M-token window fills, and [[ai-engineering/context-window-management|context rot]] degrades performance well before the hard limit; a 24-hour run will not fit any window on the roadmap [^src1].
2. **No persistent state.** A new session starts blank — "imagine a software project staffed by engineers working in shifts, where each new engineer arrives with no memory of what happened on the previous shift." [^src1]
3. **No self-verification.** Models skew positive grading their own work, so without a separate signal you get "the agent that ships at 30% complete with full confidence" [^src1].

## Architectural patterns

- **The [[ai-engineering/ralph-loop|Ralph loop]].** The simplest practitioner version — a Bash loop where `prd.json` is the plan and `progress.txt` is the lab notes, state on disk [^src1]. See its own page.
- **Anthropic — harness, then brain/hands/session.** An initializer agent sets up the environment and writes a `feature-list.json` + `init.sh`; a coding agent is woken repeatedly to make incremental progress, run tests, leave a `claude-progress.txt`, and commit, with a "test ratchet" forbidding editing/removing tests [^src1]. The "Decoupling the brain from the hands" architecture splits the **Brain** (model + harness loop), **Hands** (sandboxed ephemeral execution), and **Session** (append-only event log); a fresh container calls `wake(sessionId)` to reconstitute state, and decoupling dropped time-to-first-token ~60% at p50 and over 90% at p95 [^src1]. "Every component in a harness encodes an assumption about what the model can't do on its own." [^src1]
- **Cursor — planners, workers, judges.** After a flat lock-based model bottlenecked and an optimistic-concurrency version didn't fix coordination, Cursor's production design uses **planners** (explore the codebase, emit tasks, recursively spawn sub-planners), **workers** (focused executors that don't coordinate), and **judges** (decide when an iteration finishes/restarts) [^src1]. Notable findings: "a surprising amount of the system's behavior comes down to how we prompt the agents," and different models slot into different roles — a GPT model beat Opus for extended autonomous work because Opus "tended to stop early and take shortcuts" [^src1].
- **Google — Agent Platform.** Cloud Next '26 folded Vertex AI into the Gemini Enterprise Agent Platform, productizing long-running agents with SLAs: Agent Runtime (runs "for days at a time," sub-second cold starts), Agent Sessions (pinnable to custom session IDs), Agent Memory Bank (persistent curated long-term memory with a search API), Agent Sandbox, plus orchestration/registry/identity/gateway/observability services [^src1]. Architecturally "the same brain/hands/session split... just productized at platform scale." [^src1]

The session-as-event-log is the underappreciated part: it is what makes a run recoverable, debuggable, and auditable [^src1].

## Five production patterns

Osmani and Shubham Saboo distill five patterns separating working long-running agents from demos [^src1]:

1. **Checkpoint-and-resume** — write intermediate state to disk and checkpoint every N units; the common multi-day failure is context loss (error on document 201 of 200, restart from scratch) [^src1].
2. **Delegated approval (human-in-the-loop)** — let the agent pause in place with full execution state intact, consume zero compute while a human takes hours, then resume with sub-second latency [^src1].
3. **Memory-layered context** — long-term memory plus low-latency lookups; the production failure mode is *memory drift* (learning a shortcut from atypical interactions and over-applying it), so "govern memory like you govern microservices" [^src1].
4. **Ambient processing** — event-driven agents on a stream/table; don't hardcode policy into the agent, define it in a gateway so a fleet picks up changes without redeploys [^src1].
5. **Fleet orchestration** — a coordinator delegating to specialists, each with its own identity/policy/registry entry — the classic coordinator/worker shape, now handled declaratively [^src1].

## How to build one today

By use case [^src1]:

- **Coding on your own repo** — just use [[ai-engineering/claude-code|Claude Code]] (or Antigravity/Cursor/Codex); treat `AGENTS.md` "like a pilot's checklist," add typecheck/lint hooks, write a plan file, use the Ralph loop when you don't believe "done," and run in a worktree so a closed laptop doesn't kill the run [^src1].
- **Hosted agent product** — "Don't build the runtime. Pick a managed one" (Google Agent Platform, Claude Managed Agents, or self-host on ADK / Claude Agent SDK / Codex SDK) [^src1].
- **Autonomous/operational (monitoring, research, ops)** — Memory-Bank-style persistence (ADK + Memory Bank + Cloud Run + Cloud Scheduler) [^src1].

Cross-cutting moves: write the done-condition before the agent starts ("the single highest-leverage move"); separate the evaluator from the generator; invest in the session log, not just the prompt; and treat compaction and full context resets as first-class — Anthropic found summarization-as-compaction insufficient for very long jobs and used full context resets rebuilt from a structured handoff file [^src1].

## Limitations

Still genuinely unsolved [^src1]: **cost** (a 24-hour frontier run can "quietly burn through a week's API budget in an afternoon" without budgets/circuit breakers — see [[ai-engineering/agent-cost-management|Agent Cost Management]]); **security** (a larger attack surface; the brain/hands split keeps credentials unreachable from the sandbox); **alignment drift** (goals lose fidelity across re-summarization); **verification** (auditing 24 hours of activity is a human-time problem); and **the human role** — "the skill that's appreciating in value isn't writing code. It's writing specs that survive contact with an autonomous executor." [^src1]

[^src1]: [Long-running Agents](../../raw/web/long-running-agents.md)
</content>

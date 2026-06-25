---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/web/sleep-time-compute-beyond-inference-scaling-at-test-time.md
    channel: web
    ingested_at: 2026-06-25
  - path: raw/web/sleep-time-compute.md
    channel: web
    ingested_at: 2026-06-25
aliases:
  - sleep-time compute
  - offline compute
  - pre-compute inference
  - dreaming compute
  - MemGPT 2.0
  - Letta sleep-time agents
  - primary agent sleep-time agent
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-25
updated: 2026-06-25
---

# Sleep-Time Compute

**TL;DR**: Sleep-time compute lets LLMs "think" about a context **offline, before any query is posed**. By pre-computing useful quantities about a given context when the system is idle, test-time compute requirements can be reduced by ~5× for the same accuracy, or accuracy can be raised by 13–18% without adding latency [^src1]. The key insight: much of what models do at inference time (reasoning about a shared context) can be amortized ahead of time when query patterns are predictable.

## Motivation

Scaling test-time compute (chain-of-thought, best-of-N sampling, verifier loops) has become a primary lever for hard reasoning tasks, but it adds latency and cost at the moment of user interaction. Sleep-time compute moves a portion of that compute budget to an earlier, offline phase — analogous to a student studying the night before an exam rather than thinking from scratch during it [^src1].

## Core mechanism

1. **Offline phase** — given a context (e.g. a problem statement, a codebase, a document set), the model pre-computes: anticipated queries, intermediate reasoning steps, cached conclusions.
2. **Test-time phase** — when a real query arrives, the model can leverage the pre-computed state, reducing how much it needs to reason from scratch [^src1].

The method was evaluated on two modified reasoning benchmarks [^src1]:
- **Stateful GSM-Symbolic** — variant of grade-school math symbolic reasoning
- **Stateful AIME** — variant of competition mathematics

## Empirical results

| Metric | Result |
|---|---|
| Test-time compute reduction (same accuracy) | ~5× on Stateful GSM-Symbolic and Stateful AIME |
| Accuracy gain (same test-time compute) | +13% on Stateful GSM-Symbolic, +18% on Stateful AIME |
| Cost reduction via amortization (Multi-Query) | 2.5× decrease in average cost per query |

**Multi-Query GSM-Symbolic** is a new benchmark that extends GSM-Symbolic with *multiple related queries per context*. By amortizing sleep-time compute across related queries about the same context, cost per query drops 2.5× compared to independent test-time compute per query [^src1].

## When sleep-time compute is most effective

The key predictor is **query predictability**: how well the anticipated queries (computed during sleep time) match the actual queries at test time. When context structure makes queries predictable (e.g. a document with a fixed schema, a codebase with a stable API surface), sleep-time compute delivers its largest gains [^src1].

Inverse implication: for truly ad-hoc or adversarial queries, pre-computing useful intermediate state is harder, and gains shrink.

## Agentic SWE application

The paper includes a case study applying sleep-time compute to a realistic software engineering (SWE) task — the class of problem that tools like [[ai-engineering/claude-code|Claude Code]] tackle. The finding suggests that agents operating on codebases could pre-analyze repositories offline (anticipating likely tasks: type errors, refactoring patterns, API mismatches) and surface that pre-computed state at request time [^src1].

This connects to the [[ai-engineering/claude-managed-agents|Claude Managed Agents]] "dreaming" concept — agents consolidating memory and pre-computing context during idle periods rather than only on user demand.

## MemGPT 2.0 / Letta implementation

Letta (the team behind MemGPT) shipped sleep-time agents as part of Letta 0.7.0 [^src2]. Key design:

**Two-agent architecture** [^src2]: when you create a sleep-time-enabled agent, Letta creates two agents under the hood:
- **Primary agent** — handles user interactions; has tools for search and recall memory, but **no tools to edit its core in-context memory block**.
- **Sleep-time agent** — runs asynchronously during idle periods; has write access to the primary agent's core memory and its own in-context memory. It reorganizes, consolidates, and improves the learned context without blocking the primary agent.

The separation solves MemGPT 1.0's bundling problem: in MemGPT, memory management and conversation happened in a single agent, causing latency during interactions and messy incremental memories. Offloading memory management to the sleep-time agent makes memory formation clean and continuous [^src2].

**Configurable frequencies** [^src2]: sleep-time agents can be configured to run at different frequencies (higher = more tokens, better learned context). Because Letta is model-agnostic, primary and sleep-time agents can use different models — the recommendation is a fast model (e.g. gpt-4o-mini) for the primary agent and a stronger, slower model (e.g. gpt-4.1 or Sonnet 3.7) for the sleep-time agent, since the sleep-time agent is latency-unconstrained.

**Anytime memory writes** [^src2]: the sleep-time agent modifies primary agent memory in an "anytime" fashion — the primary agent can read from memory at any point without waiting for the sleep-time agent to finish its reasoning. This decouples the two timelines cleanly.

**Document analysis application** [^src2]: upload a large document; the sleep-time agent parses it in the background, writing key findings into the primary agent's memory. By the time the user asks a question, the document is already digested and retrievable at test time.

## Relationship to test-time scaling

Sleep-time compute is positioned as **complementary** to test-time scaling, not a replacement [^src1]. The paper is titled "Beyond Inference Scaling at Test-Time" — the argument is that the community has focused almost exclusively on what happens *during* a user query, and sleep-time compute opens a second axis of scaling: what the model does *between* queries.

Comparison:

| Dimension | Test-time compute | Sleep-time compute |
|---|---|---|
| Latency visible to user | Yes (slow) | No (offline) |
| Per-query cost | Scales with difficulty | Amortized across queries |
| Requires predictable queries? | No | Yes (for maximum gain) |
| Query-blind computation | No | Yes (anticipates future queries) |

## See also

- [[ai-engineering/llm|LLM]] — the model family this compute pattern applies to
- [[ai-engineering/agent-memory|Agent Memory]] — related: persistent memory as a form of pre-computation across sessions
- [[ai-engineering/claude-managed-agents|Claude Managed Agents]] — dreaming / gardener pattern: agents that operate offline to improve their own state
- [[ai-engineering/context-window-management|Context Window Management]] — adjacent concern: managing what state is in context at test time

---

[^src1]: [Sleep-time Compute: Beyond Inference Scaling at Test-time (arXiv:2504.13171)](../../raw/web/sleep-time-compute-beyond-inference-scaling-at-test-time.md)
[^src2]: [MemGPT 2.0: Sleep-time Agents in Letta](../../raw/web/sleep-time-compute.md) — Letta blog

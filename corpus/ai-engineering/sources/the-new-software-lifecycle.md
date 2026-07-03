---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-the-new-software-lifecycle-840140b4.md
    channel: web
    ingested_at: 2026-06-29
aliases:
  - new SDLC
  - new software lifecycle
  - vibe coding SDLC
  - Google SDLC whitepaper
tags:
  - corpus/ai-engineering
  - source
created: 2026-06-29
updated: 2026-06-29
---

# The New Software Lifecycle (Addy Osmani, June 2026)

**TL;DR.** Addy Osmani's summary of a Google whitepaper co-authored with Shubham Saboo and Sokratis Kartakis. Core thesis: **an agent = model + harness**, the split is roughly 10%/90%, and the most important knob inside that harness is context engineering [^src1].

## Agent = model + harness

> "The paper's rough split is 10% model, 90% harness. That sounds high until you've spent a week debugging one." [^src1]

The analogy: "The model is the engine. The harness is the car, the road, and the traffic laws." [^src1]

Two public benchmarks make the 90% claim concrete [^src1]:
- **Terminal Bench 2.0**: one team moved a coding agent from outside the top 30 to the top 5 by changing *only* the harness, same model underneath.
- **LangChain experiment**: added 13.7 points on the same benchmark by changing just the system prompt, tools, and middleware around a fixed model.

Most agent failures are harness failures — a missing tool, a loosely written rule, a forgotten guardrail, a context window full of junk. The model gets swapped out under the harness sooner or later anyway [^src1].

## Six context types

The paper sorts agent context into six types [^src1]:

| Type | Role |
|---|---|
| **Instructions** | System prompts, rule files (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`) — behavioral constraints |
| **Knowledge** | Domain facts, documentation, project-specific info |
| **Memory** | Persistent state across sessions; user preferences; accumulated decisions |
| **Examples** | Few-shot demonstrations, reference implementations |
| **Tools** | Callable functions, MCP servers, external APIs |
| **Guardrails** | Hard boundaries, safety constraints, escalation rules |

See [Context Engineering](/ai-engineering/context-engineering.md) for the discipline of filling and managing these.

## Static vs dynamic context (the bill)

The cost-deciding distinction is **static vs. dynamic context** [^src1]:

- **Static context** — loaded every turn: system instructions, rule files, global memory, core guardrails. *Reliable and expensive* — you pay for it on every call.
- **Dynamic context** — loaded on demand: skills that fire when a task matches, tool results, RAG documents. *Only pay for what a task touches.*

Getting this balance wrong in one direction burns tokens and buries the signal. Wrong in the other and the agent forgets safety rules. The boundary should be treated as a real architectural decision — reviewed in a PR, versioned like code [^src1].

**Progressive disclosure** scales dynamic context: the agent sees skill metadata at startup, loads full instructions when a task matches, and only pulls heavy reference material when it actually needs it. One agent can carry dozens of skills and only pay for the one it's using [^src1].

## Verification spectrum

The same agent can sit anywhere on a spectrum from vibe coding to agentic engineering. The differentiator is verification [^src1].

Two verification mechanisms [^src1]:
- **Tests** — cover deterministic parts: this input → that output.
- **Evals** — cover non-deterministic parts:
  - *Output evaluation*: is the final result correct?
  - *Trajectory evaluation*: was the path (tool calls, reasoning) sound?

Both matter. An answer that looks right but skipped its checks is more dangerous than one that's obviously broken [^src1]. Addy's one-liner for leaders: **"Set the bar at the eval, not the demo."** A demo shows the agent can work once. An eval suite shows it works reliably.

## Economic lens: context and routing are financial levers

The crossover point where vibe coding costs 3–10× more per feature than agentic engineering is illustrative, not a measured constant [^src1]. The key insight: context engineering and model routing are **financial levers**, not just technical ones.

- Route hard reasoning to a large model; route routine work (test generation, code review, CI checks) to a small, cheap one. Quality holds, cost drops.
- Passing a 100,000-token repo into every prompt doesn't scale — the model-routing plus context-scoping combination is what makes the economics work [^src1].

## Lifecycle asymmetry

AI compresses the software lifecycle unevenly [^src1]:
- **Implementation**: drops from weeks to hours — this is where the gains are.
- **Requirements, architecture, verification**: stay slow — they are judgment work.
- **Testing/QA**: inverts; your tests and evals become the main way you tell the agent what "correct" means.
- **Maintenance**: underrated upside — "code too risky to touch" can now be read, refactored, modernized by an agent.

METR study: experienced developers can go **19% slower** on some tasks once you count the time spent checking and fixing [^src1] — a reminder that implementation is now reviewing, not writing.

## Related

- [Agent Harness](/ai-engineering/agent-harness.md) — the 10/90 framing; what the harness includes
- [Context Engineering](/ai-engineering/context-engineering.md) — managing the six context types; static/dynamic tradeoffs
- [Agentic Coding](/ai-engineering/agentic-coding.md) — verification and eval practices; the review shift

---

[^src1]: [The New Software Lifecycle](../../../raw/web/web-the-new-software-lifecycle-840140b4.md) — Addy Osmani, June 16, 2026

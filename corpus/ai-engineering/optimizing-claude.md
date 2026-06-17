---
type: synthesis
domain: ai-engineering
status: draft
sources:
  - path: raw/notes/notes-clippings-the-advisor-strategy-give-sonnet-an-intelligence-boost-with.md
    channel: notes
    ingested_at: 2026-06-17
aliases:
  - optimizing Claude
  - Claude productivity
  - Claude setup optimization
  - getting more out of Claude
  - advisor strategy
  - advisor tool
tags:
  - corpus/ai-engineering
  - synthesis
created: 2026-06-09
updated: 2026-06-17
---

# Optimizing a Claude Setup for Efficiency and Productivity

**TL;DR**: Across the corpus's agent/context pages, a single principle organizes everything: **context is the scarce resource, and a lean window is both cheaper and higher-quality**. Every other productivity lever — skills over always-on instructions, sub-agents, concise specs, codified workflows — is downstream of protecting the window. This page synthesizes the corpus's guidance into one operational checklist.

> Provenance note: this synthesis builds on other corpus pages rather than directly on raw sources; each linked page carries the underlying citations. (This is the internal-provenance case the draft v0.6 `derived_from:` field is intended to formalize.)

## The organizing principle: context economy

Model output quality *degrades as the context window fills* — the practical target is to keep usage between the system-prompt baseline (~10%) and roughly 70%; performance falls off as it approaches 90–100% ([[ai-engineering/context-window-management|Context Window Management]]). The consequence reframes "efficiency": saving tokens is not only a cost play, it is a **quality** play. A flooded window degrades the agent regardless of model strength ([[ai-engineering/tool-calling-and-context-engineering|Tool Calling & Context Engineering]]).

## The levers (ordered by leverage)

### 1. Skills over an always-on `CLAUDE.md`
A skill loads only its name + description into context until it is invoked (progressive disclosure); a `CLAUDE.md`/`AGENTS.md` file is re-injected on *every* turn. Measured contrast: one skill cost 944 tokens always-on vs **53 tokens** as name + description ([[ai-engineering/agent-skills|Agent Skills]]). Reserve always-on instruction files for the minority of content that genuinely must be present every turn (proprietary information, a personal methodology).

> Calibration: the corpus flags this as an opinionated stance that tensions with sources treating `CLAUDE.md` as valuable long-term memory ([[ai-engineering/context-engineering|Context Engineering]]). The defensible synthesis: put *stable, must-be-every-turn* rules in `CLAUDE.md`; put *situational, reusable workflows* in skills.

### 2. Build skills by doing, then codify — and let them self-heal
Hand-writing a skill cold captures no experience of a successful run. Instead: walk the agent through the workflow once, secure a successful run in context, then have it write the skill; when it later fails, ask *why*, fix the cause, and instruct it to "update the skill so this doesn't happen again." Iteration converges (~5 loops for a robust multi-source workflow) ([[ai-engineering/agent-skills|Agent Skills]]).

### 3. Spend context on what is unique to you
"Code itself is context" — telling the agent which framework a codebase uses is redundant. Reserve instructions for your specific workflow, taste, and conventions; omit general knowledge the model already has ([[ai-engineering/context-engineering|Context Engineering]]).

### 4. Isolate work in sub-agents
Delegating to a sub-agent opens a *fresh* window; its file reads and large retrievals never enter the main window (observed savings 3.5k–9k tokens/task). Assign a cheaper model to simple sub-tasks ([[ai-engineering/context-window-management|Context Window Management]]).

### 5. Scale for productivity, not for looks
Start with one agent; add sub-agents only after a workflow is proven and the sub-agent carries real skills and context — not a speculative fleet of agents and skills up front ([[ai-engineering/multi-agent-systems|Multi-Agent Systems]]).

### 6. Be concise; manage the window actively
Verbose instructions hurt — extra tokens add confusion. Give clear specs and let the agent ask. Compact proactively with preservation notes (`/compact keep …`) before the window fills, and reset (`/clear`) between unrelated tasks ([[ai-engineering/context-window-management|Context Window Management]]). Treat the agent like a senior developer / new employee: specify intent, supply a worked example, correct iteratively ([[ai-engineering/ai-agent|AI Agent]]).

### 7. The advisor strategy: Sonnet executor + Opus advisor

The **advisor strategy** pairs a smaller, cheaper executor model (Sonnet or Haiku) with a larger advisor model (Opus) in the same agentic run [^src_adv]. The executor drives end-to-end — calling tools, reading results, iterating — and escalates to Opus only when it hits a decision it cannot reasonably resolve. Opus accesses the shared context, returns a short guidance response (typically 400–700 tokens), and the executor resumes.

This inverts the common orchestrator-subagent pattern where the large model decomposes work and the small model executes; here the small model drives and the large model advises on demand [^src_adv].

**Measured results** (Anthropic evals) [^src_adv]:
- Sonnet + Opus advisor: **+2.7 pp on SWE-bench Multilingual** vs Sonnet alone, while **reducing cost per task 11.9%**
- Haiku + Opus advisor on BrowseComp: **41.2%** vs Haiku solo at **19.7%** (more than double); costs 85% less than Sonnet solo
- The advisor only generates a short plan; the executor handles all full output at its lower rate — so the combined cost stays well below running Opus end-to-end

**API usage** (beta): declare `{"type": "advisor_20260301", "name": "advisor", "model": "claude-opus-4-6", "max_uses": 3}` in the tools list alongside your other tools. The handoff happens inside a single `/v1/messages` request — no extra round-trips or context management. Advisor tokens are reported separately in the usage block for cost tracking [^src_adv].

The key insight: "frontier-level reasoning applies only when the executor needs it, and the rest of the run stays at executor-level cost" [^src_adv]. This is the cost-intelligence lever that sits between "run Sonnet alone" and "run Opus end-to-end."

See [[ai-engineering/multi-agent-systems|Multi-Agent Systems]] for the broader generator-verifier and orchestrator-subagent patterns this fits into, and [[ai-engineering/claude-api|Claude API]] for the full platform context.

### 8. Don't install other people's skills
Two reasons: security (a downloaded skill is an attack vector) and missing context (it lacks *your* successful-run experience). Review others' skills to learn from them; don't adopt them wholesale ([[ai-engineering/agent-skills|Agent Skills]]).

[^src_adv]: [The advisor strategy: Give Sonnet an intelligence boost with Opus](../../raw/notes/notes-clippings-the-advisor-strategy-give-sonnet-an-intelligence-boost-with.md) — Anthropic

## What this synthesis does not yet cover

The corpus now covers Claude Code mechanics well (slash commands, hooks, skills, subagents, dynamic workflows via [[ai-engineering/claude-code|Claude Code]]), official Anthropic docs, and the advisor strategy (§7 above). Remaining gaps:

- **A specific personal setup** — the corpus has no record of an individual's actual configuration end-to-end.
- **Eval-driven optimization** — how to systematically measure before/after on a personal workflow.

## See also

- [[ai-engineering/agent-skills|Agent Skills]]
- [[ai-engineering/context-window-management|Context Window Management]]
- [[ai-engineering/context-engineering|Context Engineering]]
- [[ai-engineering/multi-agent-systems|Multi-Agent Systems]]
- [[ai-engineering/ai-agent|AI Agent]]
- [[ai-engineering/README|AI Engineering hub]]

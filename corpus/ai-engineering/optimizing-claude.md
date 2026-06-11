---
type: synthesis
domain: ai-engineering
status: draft
sources: []
aliases:
  - optimizing Claude
  - Claude productivity
  - Claude setup optimization
  - getting more out of Claude
tags:
  - corpus/ai-engineering
  - synthesis
created: 2026-06-09
updated: 2026-06-09
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

### 7. Don't install other people's skills
Two reasons: security (a downloaded skill is an attack vector) and missing context (it lacks *your* successful-run experience). Review others' skills to learn from them; don't adopt them wholesale ([[ai-engineering/agent-skills|Agent Skills]]).

## What this synthesis does not yet cover

The corpus answers the *principles* of Claude productivity well but is thin on:

- **Claude Code mechanics** — slash commands, hooks, `settings.json`, output styles, MCP configuration (only lightly touched via one source).
- **Primary documentation** — no official Anthropic / Claude Code docs are ingested; the cluster rests on one podcast plus course notes.
- **A specific personal setup** — the corpus has no record of an individual's actual configuration.

These are the highest-leverage sources to ingest next to deepen the `Claude` cluster.

## See also

- [[ai-engineering/agent-skills|Agent Skills]]
- [[ai-engineering/context-window-management|Context Window Management]]
- [[ai-engineering/context-engineering|Context Engineering]]
- [[ai-engineering/multi-agent-systems|Multi-Agent Systems]]
- [[ai-engineering/ai-agent|AI Agent]]
- [[ai-engineering/README|AI Engineering hub]]

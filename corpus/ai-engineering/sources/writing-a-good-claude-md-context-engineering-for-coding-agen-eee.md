---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/notes/notes-03-resources-articles-writing-good-claude-md-context-engineering.md
    channel: notes
    ingested_at: 2026-07-21
aliases: []
tags:
  - corpus/ai-engineering
  - source
  - context-engineering
  - coding-agents
  - claude-code
created: 2026-07-21
updated: 2026-08-14
provisional: false
url: https://www.humanlayer.dev/blog/writing-a-good-claude-md
origin: obsidian
---

# "Writing a Good CLAUDE.md: Context Engineering for Coding Agents"

**TL;DR:** CLAUDE.md is the only file that enters every coding-agent session. Because LLMs are stateless functions with a finite instruction budget, less is more — keep it under 300 lines, universally applicable, and offload task-specific detail via progressive disclosure.

## Core mental model: LLMs as stateless functions

Weights are frozen at inference time. The agent has no implicit memory of the codebase; CLAUDE.md is the sole default context injected into every session.[^1] Without it, the agent knows nothing about your project.

Claude Code injects CLAUDE.md via a `<system-reminder>` tag that also tells the model to ignore it when not relevant — meaning any instruction that is not universally applicable will be silently skipped.[^1]

## What to put in CLAUDE.md

The guide recommends covering three dimensions:[^1]

- **WHAT** — tech stack, project structure, monorepo map
- **WHY** — project purpose, what each part does
- **HOW** — commands to run, verify, and test changes

## Instruction-following degrades with volume

Empirically:[^1]

- Frontier thinking models reliably follow ~150–200 instructions; performance decays linearly after that threshold.
- Smaller models exhibit exponential decay and should be avoided for multi-step agentic tasks.
- Claude Code's built-in system prompt already consumes ~50 instructions before any user content is added.
- Crucially, as instruction count grows, *all* instructions are followed less — not just later ones. The degradation is uniform, not tail-heavy.

This means the effective user budget for reliable instruction-following is roughly 100–150 instructions in a frontier model.

## Less is more

The author's recommendation: keep the root CLAUDE.md under 300 lines. HumanLayer's own root file is under 60 lines.[^1]

> "Claude can only reliably follow ~150-200 instructions total, and Claude Code's system prompt already uses ~50 of them."[^1]

## Progressive disclosure

Task- or project-specific instructions should live in separate, self-descriptively named markdown files; CLAUDE.md references them rather than inlining everything.[^1] This keeps the always-loaded context lean while allowing deeper context to be pulled in on demand.

## Applicability

The same principles apply to `AGENTS.md` files used by OpenCode, Zed, Cursor, and Codex — not just Claude Code.[^1]

## Connections

- Related to [/ai-engineering/context-engineering.md](/ai-engineering/context-engineering.md) — CLAUDE.md is a concrete instance of context engineering for coding agents.
- Related to [/ai-engineering/claude-code.md](/ai-engineering/claude-code.md) — Claude Code is the primary runtime that reads CLAUDE.md.

[^1]: raw/notes/notes-03-resources-articles-writing-good-claude-md-context-engineering.md

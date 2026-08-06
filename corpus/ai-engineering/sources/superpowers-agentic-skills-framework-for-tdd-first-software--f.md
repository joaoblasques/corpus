---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/notes/notes-03-resources-articles-superpowers-agentic-skills-framework-tdd-workflow.md
    channel: notes
    ingested_at: 2026-07-20
aliases:
  - superpowers framework
  - superpowers agentic skills
tags:
  - corpus/ai-engineering
  - source
  - agentic-coding
  - tdd
  - claude-code
created: 2026-07-20
updated: 2026-08-06
provisional: false
url: https://github.com/obra/superpowers
origin: obsidian
consolidated_into: ai-engineering/gemini-cli.md
---

# Superpowers — Agentic Skills Framework for TDD-First Software Development

> **TL;DR**: Superpowers is a widely-adopted open-source skills framework that enforces a deliberate professional workflow on AI coding agents — specs before code, strict TDD, parallel subagent execution, and severity-gated code review. Available on Claude Code, Cursor, and Gemini CLI plugin marketplaces.

## Overview

Superpowers (81.5k stars, 6.3k forks, MIT license) is an agentic skills framework and software development methodology designed to guide AI coding agents through a structured professional workflow.[^1] Rather than jumping straight to code generation, the framework "steps back and asks what you're really trying to do" — enforcing specification and design before any implementation begins.[^1]

The framework is built primarily in Shell (54.8%) and JavaScript (32.1%) and is available on the Claude Code marketplace, Cursor plugin marketplace, and via `gemini extensions install`.[^1]

## Core Philosophy

Three guiding principles underpin the framework:[^1]

- **Complexity reduction as primary design goal** — YAGNI and DRY are enforced, not suggested.
- **Verification over claims** — agents must demonstrate correctness through tests, not assertions.
- **Systematic processes over ad-hoc** — every stage follows a defined protocol.

## Workflow Stages

The framework enforces a fixed sequence of seven stages:[^1]

1. **Brainstorming** — design refinement through clarifying questions before any code is touched.
2. **Git worktrees** — isolated development workspaces per feature to avoid branch contamination.
3. **Implementation planning** — work is broken into 2–5 minute bite-sized tasks.
4. **Subagent-driven development** — parallel task execution across multiple agents.
5. **Test-driven development** — strict RED-GREEN-REFACTOR cycle; tests are always written first.
6. **Code review** — severity-based issue blocking prevents merging defective work.
7. **Branch completion** — structured merge/PR decision workflow.

## Skills Library

Beyond the workflow stages, Superpowers ships a skills library that includes:[^1]

- **Systematic debugging** — 4-phase root cause analysis.
- **Collaborative planning** — structured specification sessions.
- **Parallel agent dispatching** — fan-out task orchestration.
- **Git worktree management** — lifecycle tooling for isolated workspaces.

## Enforced TDD

TDD is not optional in Superpowers. The RED-GREEN-REFACTOR cycle is enforced as a hard constraint: tests must be written before implementation, a failing test (RED) must exist before any production code is written, and refactoring happens only after GREEN is achieved.[^1]

## Connections

- [/ai-engineering/gemini-cli.md](/ai-engineering/gemini-cli.md) — this source is consolidated into the Gemini CLI page
- [/ai-engineering/information-retrieval.md](/ai-engineering/information-retrieval.md) — adjacent structured methodology in the ai-engineering domain

[^1]: `raw/notes/notes-03-resources-articles-superpowers-agentic-skills-framework-tdd-workflow.md` (obsidian, collected 2026-07-20)

---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/notes/notes-03-resources-articles-writing-good-specs-ai-agents-prd-structure.md
    channel: notes
    ingested_at: 2026-07-21
aliases: []
tags:
  - corpus/ai-engineering
  - source
  - doc-quick-intake
  - spec-writing
  - context-engineering
  - agentic-coding
created: 2026-07-21
updated: 2026-08-15
provisional: false
url: https://open.substack.com/pub/addyo/p/how-to-write-a-good-spec-for-ai-agents
origin: obsidian
---

# "How to Write a Good Spec for AI Agents: Five Principles"

**TL;DR:** Large specs overwhelm AI agents via context-window and attention-budget limits; small specs lose precision. Five principles resolve this tension: start with a high-level vision and let the agent draft details, structure the spec like a PRD with six concrete sections, break work into numbered tasks, pin exact stack versions, and iterate in Plan Mode before any code runs.[^1]

---

## Core problem

The fundamental spec-writing tension: large specs saturate the model's context window and diffuse its "attention budget," while small specs omit constraints the agent needs.[^1]

> "Feed the agent manageable tasks, not the whole codebase."[^1]

Large monolithic prompts produce the equivalent of "10 devs working without talking" — parallel, uncoordinated edits with no shared contract.[^1]

---

## The five principles

### Principle 1 — High-level vision first; agent drafts the details

Open with a concise goal statement, then prompt the agent to generate a detailed spec from it. This exploits the model's ability to extrapolate while keeping the human's initial input small.[^1]

**Plan Mode** (Shift+Tab in Claude Code): read-only mode where the agent plans but does not write code until the user approves. Use it to produce the draft spec, review it, then save as `SPEC.md` as the persistent per-project reference.[^1]

### Principle 2 — Structure like a PRD with six sections

Derived from analysis of 2,500+ agent config files, six sections consistently improve agent behavior:[^1]

| Section | What to include |
|---|---|
| **Commands** | Full executable commands with flags (`npm test`, `pytest -v`) — not just tool names |
| **Testing** | Framework, file locations, coverage expectations |
| **Project structure** | Explicit paths (`src/` for app code, `tests/` for unit tests) |
| **Code style** | One real code snippet beats three paragraphs of description |
| **Git workflow** | Branch naming, commit format, PR requirements |
| **Boundaries** | What the agent should NEVER touch |

The boundaries section is especially load-bearing: "Never commit secrets" was the #1 most helpful constraint surfaced by the GitHub study.[^1]

### Principle 3 — Break large specs into smaller tasks

Use a numbered task list; agents execute one step at a time. This keeps each prompt within a manageable context slice and prevents the parallel-uncoordinated-edit failure mode.[^1]

### Principle 4 — Be specific about stack

Vague: "React project." Precise: "React 18 with TypeScript, Vite, Tailwind CSS."[^1] Including versions and key dependencies prevents the agent from making incompatible choices that are invisible until runtime.

### Principle 5 — Iterate with the agent before coding

The spec is the first artifact built collaboratively. Refine it in Plan Mode (read-only, no code written) before switching the agent to execute mode.[^1] The spec is a living document, not a one-shot handoff.

---

## Connections

- See [/ai-engineering/context-engineering.md](/ai-engineering/context-engineering.md) for broader treatment of attention budget and context management.
- Relates to CLAUDE.md as a real-world instantiation of the "Boundaries" and "Commands" sections in principle 2.

---

[^1]: [notes-03-resources-articles-writing-good-specs-ai-agents-prd-structure.md](../../../raw/notes/notes-03-resources-articles-writing-good-specs-ai-agents-prd-structure.md) — original source: https://open.substack.com/pub/addyo/p/how-to-write-a-good-spec-for-ai-agents

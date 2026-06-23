---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-compound-engineering-how-every-codes-with-agents.md
    channel: web
    ingested_at: 2026-06-23
aliases:
  - compound engineering
  - compound knowledge
  - compound loop
  - plan-work-review-compound
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-23
updated: 2026-06-23
---

# Compound Engineering

**TL;DR**: Compound engineering is a software development methodology where each coding session's learnings are captured back into `AGENTS.md`, making the agent progressively more effective with the same team and codebase. The loop: **plan → work → review → compound** [^src1]. The result: a single developer can manage 5 software products — and over time, the AI becomes "not just a tool but a compounding investment" [^src1].

## The four-stage loop

1. **Plan** — spend time on a spec, task breakdown, and context-setting before touching the model. "High-quality planning is the only way to reliably go from 0 to 1 with an agent" [^src1].
2. **Work** — execute with the model; maintain review checkpoints. "Once you've got the model doing work, your job is quality control and course-correction" [^src1].
3. **Review** — read the code. Even in agentic workflows, the engineer must understand output to catch regressions and steer quality [^src1].
4. **Compound** — write learnings back. Patterns the model got wrong, conventions the team uses, edge cases that emerged — these go into `AGENTS.md` so the next session starts smarter [^src1].

"The fourth step is where leverage lives" — most teams skip it and end up in a permanent catch-up loop [^src1].

## What compounds into AGENTS.md

After each work session, write to `AGENTS.md` [^src1]:
- **Mistakes the model made** → rules preventing them (e.g. "never modify `auth.ts` without adding a test")
- **Patterns the model used well** → templates to standardize
- **Team preferences** → explicit style rules the model has to re-learn without them
- **Edge cases encountered** → explicit guardrails

The test: any time the model makes a mistake, you should be able to add exactly one rule to `AGENTS.md` that would have prevented it [^src1].

This is the same mechanism as the [[ai-engineering/agent-harness|ratchet principle]] — "every line in a good AGENTS.md should be traceable back to a specific thing that went wrong."

## Scale: 5 products, 1 person

Every.to applies compound engineering across their software business: 5 products each managed by a single developer, with the compound step keeping the model aligned to each codebase's conventions [^src1]. The claim: compound engineering makes a single developer as productive as a team of 5 [^src1].

"The gap between engineers who get 10x productivity from AI and those who get 2x isn't model choice or prompt quality — it's whether they compound" [^src1].

## Time allocation model

Every.to's reported split: **80% planning and review, 20% execution** [^src1]. More time spent NOT coding (spec work, review, `AGENTS.md` updates) produces more output because the model executes the implementation.

This mirrors [[ai-engineering/agentic-coding|spec-driven development]] — the engineer moves up the abstraction ladder.

## The compound engineering plugin

The workflow is packaged as a Claude Code plugin (`every.inc/compound-engineering`) that installs a shared knowledge base and ships a `compound-knowledge` agent that automatically proposes `AGENTS.md` updates after each session [^src1].

## See also

- [[ai-engineering/agentic-coding|Agentic Coding]] — the broader orchestration discipline; compound engineering is its learning-loop layer
- [[ai-engineering/agent-harness|Agent Harness]] — the ratchet principle (same mechanism)
- [[ai-engineering/claude-md-conventions|CLAUDE.md Conventions]] — where `AGENTS.md`/`CLAUDE.md` fit in the context stack
- [[ai-engineering/agent-skills|Agent Skills]] — skill files as an alternative to always-loaded AGENTS.md

---

[^src1]: [Compound Engineering: How Every.to Codes with Agents](../../raw/web/web-compound-engineering-how-every-codes-with-agents.md) — Every.to

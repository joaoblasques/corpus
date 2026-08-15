---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-introducing-visual-plan-scannable-claude-code-plans-0689d90a.md
    channel: web
    ingested_at: 2026-08-15
aliases:
  - visual-plan
  - visual-recap
  - constraint engineering
  - MDX plan contract
  - probabilistic compiler
  - agentic plan contract
tags:
  - corpus/ai-engineering
  - source
created: 2026-08-15
updated: 2026-08-15
url: https://www.builder.io/blog/claude-code-plan
origin: obsidian-list
---

# Introducing /visual-plan: Scannable Claude Code Plans

**TL;DR** — Builder.io's thesis: the LLM is a probabilistic compiler; the plan is source code; constraint engineering (not prompt engineering) is the new bottleneck. `/visual-plan` (MDX-based structured plans) and `/visual-recap` (structured post-execution recap) address the asymmetry between obsessively optimized machine context and ignored human context in agentic loops.[^src1]

## The probabilistic compiler problem

"C compilers are deterministic. Compile the same C twice, you get the same binary. But hand the same plan to an LLM twice, and you get two completely different codebases." Treating a plan as a contract that gates a deterministic binary doesn't hold — a plan gates a non-deterministic, probabilistic output.[^src1]

When developers skim a markdown plan and hit Approve, "you aren't blessing a plan. You're signing off on an uncompiled, unpredictable binary."[^src1]

## The context asymmetry

| Machine context (obsessively optimized) | Human context (an afterthought) |
|---|---|
| Structured tools and schemas | Three screens of raw markdown |
| Pruned, relevant token windows | Ephemeral terminal logs |
| An indexed, retrievable repo | Cognitive skimming |

"Your judgment is the most expensive resource in an autonomous loop. Starving your own context is a massive bottleneck."[^src1]

## How visual-plan works

Plans use **MDX** instead of standard markdown to enforce schema:
- `<DataModel>` blocks must declare keys and relations
- `<Endpoint>` blocks must explicitly define auth strategy
- The agent cannot hide a missing guard behind confident prose; it either fills out the schema or leaves it conspicuously blank — "type-safety for natural language"[^src1]

Plans check into Git history: versioned, collaborative contracts reviewers can comment on, redline, and edit directly.[^src1]

## How visual-recap works

Instead of a vague markdown summary or a 3,000-line diff, the recap lifts changes back into the components defined in the plan. Governance becomes: "do the plan and the recap align?" If they drift, the build is broken — even if the test suite passes.[^src1]

"Because they share a structured schema, we can run an agent to flag the drift automatically, letting you focus your attention on the only question that requires a human: was this drift a smart pivot or a hallucination?"[^src1]

## Constraint engineering framing

"You don't steer an autonomous agent by prompting it louder. You steer it by engineering the environment: schemas, types, AST-level linter rules, and visual contracts. Code generation is solved; constraint engineering is the new bottleneck."[^src1]

The shift: writing code → designing systems (constraint engineering).

## See also

- [Agentic Coding](/ai-engineering/agentic-coding.md)
- [Spec-Driven Development](/ai-engineering/spec-driven-development.md)
- [Agent Harness](/ai-engineering/agent-harness.md)
- [Claude Subagents](/ai-engineering/claude-subagents.md)

---

[^src1]: [Introducing /visual-plan: Scannable Claude Code plans](../../../raw/web/web-introducing-visual-plan-scannable-claude-code-plans-0689d90a.md) — Builder.io blog, 2026-06-29

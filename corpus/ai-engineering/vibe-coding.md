---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/email/email-2026-04-15-vibe-coding-isn-t-enough-here-s-a-better-approach.md
    channel: email
    ingested_at: 2026-06-15
  - path: raw/web/https-newsletter-towardsdatascience-com-e3t-ctc-l2-113-d5qls-3124b6d4.md
    channel: web
    ingested_at: 2026-06-15
  - path: raw/email/email-2026-06-07-being-good-at-ai-is-stupidly-simple.md
    channel: email
    ingested_at: 2026-06-15
  - path: raw/youtube/youtube-IiZ5HRaeX4s-stop-watching-tutorials-build-these-4-claude-projects-to-10x.md
    channel: youtube
    ingested_at: 2026-06-15
aliases:
  - vibe coding
  - vibe-coding
  - spec-driven development
  - SDD
  - spec-driven
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-15
updated: 2026-06-15
---

# Vibe Coding (and why Spec-Driven Development supersedes it)

**TL;DR**: *Vibe coding* is building software by describing intent in natural language and letting a coding agent produce it — fast and accessible, but it "often produces code that doesn't match what you asked for" [^src1]. **Spec-Driven Development (SDD)** is the maturity step: write a clear spec first, then implement from it, so humans and agents align on the non-negotiables before any code is written [^src1][^src2].

## What vibe coding is

The everyday on-ramp: open Claude, pick a strong model, turn on thinking, and the single most useful trick for non-technical users is **"ask me questions first"** — Claude's `AskUserQuestion` tool flips the interaction so the model interviews *you* (3–5 questions) instead of you prompting it badly [^src3]. From there you can "build a real website or app tonight, yourself, using English," turning on bypass-permissions and iterating by pasting errors back in [^src3]. The same "let Claude interview you, then build the MVP, then iterate" loop drives the "4 Claude projects" approach — plan before building anything complex, then add features as you need them [^src4].

## Why vibe coding isn't enough

Vibe coding is fast but loses intent across agent sessions and invites scope drift [^src1]. The failure mode generalizes the [[ai-engineering/agent-harness|harness]] lesson: without written constraints, the agent picks interpretations silently and runs with them.

## Spec-Driven Development (the better approach)

SDD introduces a **plan → implement → verify** workflow [^src1]:

- Write **project constitutions** and **feature specs** that preserve context across agent sessions [^src1].
- Apply plan-implement-verify to guide the agent step by step, reducing cognitive overhead and keeping output aligned with intent [^src1].
- Use the same workflow in new *and* existing codebases; package it into reusable [[ai-engineering/agent-skills|agent skills]] [^src1].

The deeper case: SDD "aligns both humans and agents around the project's main non-negotiables" and addresses the core issues of vibe coding [^src2]. This is the same discipline as the [[ai-engineering/ai-product-management|PRD-before-agents]] practice (clear Definition of Done + Non-Goals) and Karpathy's **Goal-Driven Execution** ("don't tell it what to do; give it success criteria and watch it go") in [[ai-engineering/claude-md-conventions|CLAUDE.md Conventions]].

## Relationship to other operating modes

| Mode | Specification effort | Best for |
|---|---|---|
| **Vibe coding** | Minimal — describe intent | Prototypes, personal tools, learning |
| **Spec-Driven Development** | Up-front spec + verify loop | Production, multi-session, existing codebases |
| **[[ai-engineering/agentic-workflow|Agentic workflow]]** | Structured workflow files (WAT) | Repeatable multi-step automations |

## See also

- [[ai-engineering/agentic-coding|Agentic Coding]] — the broader coding-agent practice
- [[ai-engineering/agent-harness|Agent Harness]] — written constraints are what vibe coding lacks
- [[ai-engineering/ai-product-management|AI Product Management]] — PRD / Definition of Done / Non-Goals
- [[ai-engineering/prompt-engineering|Prompt Engineering]] — the "ask me questions first" pattern
- [[ai-engineering/learning-ai-engineering|Learning AI Engineering]] — where vibe coding fits a beginner path
- [[ai-engineering/README|AI Engineering hub]]

---

[^src1]: [Vibe coding isn't enough. Here's a better approach (Spec-Driven Development)](../../raw/email/email-2026-04-15-vibe-coding-isn-t-enough-here-s-a-better-approach.md) — DeepLearning.AI / JetBrains course announcement
[^src2]: [From Vibe Coding to Spec-Driven Development](../../raw/web/https-newsletter-towardsdatascience-com-e3t-ctc-l2-113-d5qls-3124b6d4.md) — Mariya Mansurova, Towards Data Science
[^src3]: [Being good at AI is (stupidly) simple](../../raw/email/email-2026-06-07-being-good-at-ai-is-stupidly-simple.md) — Ruben Hassid
[^src4]: [Stop Watching Tutorials — Build These 4 Claude Projects](../../raw/youtube/youtube-IiZ5HRaeX4s-stop-watching-tutorials-build-these-4-claude-projects-to-10x.md) — Austin Marchese

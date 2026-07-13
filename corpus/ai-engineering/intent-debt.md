---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-the-intent-debt.md
    channel: web
    ingested_at: 2026-06-25
aliases:
  - intent debt
  - comprehension debt
  - cognitive debt
  - triple debt model
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-25
updated: 2026-06-25
---

# Intent Debt

**TL;DR**: A third type of software debt — alongside technical debt and cognitive debt — that lives in *artifacts*: the goals, constraints, and rationale that explain why a system is the way it is. Intent debt is "the only kind of debt your agents can't pay down for you" because agents can only fabricate plausible-sounding intent, never reconstruct actual intent [^src1].

## The triple debt model

Margaret-Anne Storey's Triple Debt Model [^src1]:

| Type | Lives in | AI can fix? | How it shows |
|---|---|---|---|
| **Technical debt** | Code | Yes — agents refactor tangled modules | Slow builds, fragile tests, one scary file |
| **Cognitive debt** | People | Partially — ask agent to explain code | Team's mental model lags behind system size |
| **Intent debt** | Artifacts | No — agents can only fabricate | System drifts from original goals; no one can say when or why |

The key insight: the three types are **independent**. Low technical debt + no written-down intent = enormous intent debt for everyone else. You can understand a system completely yourself and still carry zero written intent for every agent and future teammate [^src1].

## Why intent debt compounds differently in the agentic era

Before agents, intent debt cost you once in a while — onboarding, post-departure knowledge loss. Now it costs you **every session**, multiplied by every agent you run [^src1].

An agent starts most sessions cold. It has none of the tacit intent humans accumulate over years of shared context ("we don't do it that way because of an incident in 2023"). Whatever is not externalized into a file the agent can read simply doesn't exist for it. "Bringing agents onto a team doubles its size overnight with junior people who have no long-term memory" [^src1].

The "orchestration tax" in large-scale multi-agent work is partly an **intent-debt tax**: much of what makes managing many agents exhausting is re-supplying the intent that was never written down [^src1].

## Why intent can't be fabricated

An agent can infer *plausible* rationale from code the same way you can guess why a previous engineer did something. A guess about intent isn't the intent. The model doesn't know whether a 300ms debounce was a deliberate UX decision, a benchmark result, or a number someone typed once and never revisited. It will produce a "confident-sounding reason, which is worse than admitting it doesn't know" [^src1].

Technical debt and cognitive debt are recoverable: agents can refactor code and re-explain it from the artifact. Intent — the *why* behind the choices — "is the one input that has to come from you" [^src1].

## Relationship to comprehension debt

Intent debt is the complement to comprehension debt (the gap between existing code and human understanding):

> "Being unable to capture all intent is no license to capture none of it." [^src1]

A spec detailed enough to enumerate all implicit decisions is the program itself, so specs will always be incomplete. But the load-bearing decisions — the ones that would be expensive to get wrong — must be recorded, because nobody will reconstruct them later [^src1].

## Paying it down: externalize intent as first-class artifacts

Four documented practices [^src1]:

1. **Write the spec for the intent, not the implementation.** Capture goals, constraints, non-negotiables, and an explicit definition of done (fast, accessible, secure, beyond "functionally correct"). The spec carries the intent the code can't carry on its own.

2. **Treat AGENTS.md / CLAUDE.md as an intent ledger, not config.** An auto-generated file describes what the code *is*. An intent file describes what the team *means*: conventions, the "we don't do it this way because…", constraints invisible in any single file. "Stop using `/init`" for AGENTS.md setup.

3. **Capture decisions where they happen.** Lightweight ADRs (Architecture Decision Records) — recording *why* at the moment of deciding costs almost nothing. Reconstructing it 8 months later, after the person who knew has moved teams, costs a fortune. Agents have made logging cheaper than ever; the old excuse is gone.

4. **Self-improving agents that write intent back.** Agents that update a learnings file at the end of each session act as an intent-debt pump running in reverse: every mistake recorded, every "we tried X and it didn't work because Y" is intent that would otherwise have lived only in memory.

## What high intent debt looks like

- An agent "fixes" a bug by deleting a guard clause, and nobody can say whether the guard was load-bearing or leftover [^src1]
- A refactor changes behavior users depend on; the review passed because the diff looked clean and tests were green, but the tests only encoded prior behavior, never the intent [^src1]
- "You ask why two services talk over a queue instead of a direct call, and the honest answer is 'an agent suggested it and it seemed fine'" [^src1]

## Connection to agent design

Intent debt directly connects to [Spec-Driven Development](/ai-engineering/spec-driven-development.md) (the spec carries intent), [CLAUDE.md Conventions](/ai-engineering/claude-md-conventions.md) (CLAUDE.md as intent ledger), [Agent Harness](/ai-engineering/agent-harness.md) (harnesses encode intent in config), and [Compound Engineering](/ai-engineering/compound-engineering.md) (AGENTS.md as compound learning store).

The agentic era's "where the value moved": code is cheap, comprehension is recoverable, but "intent — the goals and constraints and reasons — is the one input that still has to originate with a human" [^src1].

---

[^src1]: [The Intent Debt — Addy Osmani's blog](../../raw/web/web-the-intent-debt.md) — Addy Osmani, June 2026

<!-- RELATED:START (generated by bin/corpus_heal.py related — do not edit inside) -->

## Related across domains

- [Cognitive Debt and Cognitive Surrender](/software-engineering/cognitive-debt.md) · _software-engineering_

<!-- RELATED:END -->

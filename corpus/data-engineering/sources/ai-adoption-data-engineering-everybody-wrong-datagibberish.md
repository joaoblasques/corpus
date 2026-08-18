---
type: source
domain: data-engineering
status: draft
aliases:
  - everybody wrong about AI in data
  - data gibberish AI adoption
  - AI adoption DE governance
  - Yordan Ivanov AI data
  - semantic layer governance AI
sources:
  - path: raw/_inbox/email-2026-06-29-everybody-talks-about-ai-and-they-are-all-wrong.md
    channel: email
    source_url: https://www.datagibberish.com/p/everybody-is-wrong-about-ai-in-data
    ingested_at: 2026-08-18
tags:
  - ai-adoption
  - governance
  - semantic-layer
  - data-engineering
  - opinion
created: 2026-08-18
updated: 2026-08-18
---

# "Everybody Talks About AI (And They Are All Wrong)" — Data Gibberish

**TL;DR:** Yordan Ivanov (Data Gibberish) argues that chaotic AI adoption in data teams is producing a governance debt backlog — and that semantic layers and real problem-solving are the antidote to hype-driven mediocrity.

## The Core Claim

AI adoption in data teams has no measurable success criterion: "Companies used to have one goal: make more money. This goal is tangible and measurable. You knew if you were winning. Now the goal is 'adopt AI'. And when you cannot define success, you cannot recognize failure either."[^1]

This produces cargo-cult behavior: people "shift roadmap, add a tool or two for evaluation, and somebody ships a workflow nobody asked for against a deadline nobody set."

## Two Problems AI Adoption Creates

**Democratized fragmentation:**
- Every platform enables agentic workflows → CEO, CFO, VP Product each pull "revenue" from different sources with different definitions
- "Call it democratization if you want. To me that's decision surface area with no shared truth underneath it."[^1]

**Stalling innovation:**
- AI reproduces patterns from existing code; it cannot invent genuinely new primitives
- "DuckDB, Polars and Arrow came from people doing non-consensus work. A model trained on yesterday's patterns would never be able to produce these."
- Outsourcing thinking to AI causes field convergence: "well-executed mediocrity, forever."[^1]

## The Governance Response

Ivanov's argument for semantic layers: when humans and agents pull "revenue" from three different sources, only a semantic layer guarantees a shared definition. "One source of truth that doesn't depend on who built the dashboard."

> "Semantic layers used to feel like a gimmick to me. A nice idea that never justified the overhead. I've changed my thinking on that."[^1]

## The Opportunity Framing

The mess of careless AI adoption *is* the backlog for skilled DE practitioners:
1. Find someone who isn't on the data team
2. Find the process making them want to throw their laptop
3. Ask what they're doing with AI — watch what happens

"The more people use AI carelessly, the more stupid shit piles up for someone like you to fix."[^1]

Cross-reference: [AI Impact on Data Engineering](/data-engineering/ai-impact-on-data-engineering.md); [Semantic Layer](/data-engineering/semantic-layer.md); [Data Observability](/data-engineering/data-observability.md).

[^1]: raw/_inbox/email-2026-06-29-everybody-talks-about-ai-and-they-are-all-wrong.md

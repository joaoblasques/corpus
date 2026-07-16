---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/notes/notes-03-resources-articles-reflective-ai-systems-that-learn-from-their-mistakes.md
    channel: notes
    ingested_at: 2026-07-14
aliases:
  - reflective AI
  - self-correcting AI
  - reflection loops
tags:
  - corpus/ai-engineering
  - source
  - doc-quick-intake
created: 2026-07-14
updated: 2026-07-16
provisional: false
url: https://www.linkedin.com/pulse/7-ai-terms-youll-hear-lot-this-year-alex-wang
origin: obsidian
consolidated_into: ai-engineering/openai.md
confidence: 0.8
last_confirmed: 2026-07-16
---

# Reflective AI — Systems That Learn From Their Mistakes

**TL;DR:** Reflective AI systems evaluate and revise their own outputs via a generate→critique→revise loop, improving accuracy without retraining. The pattern is considered foundational for autonomous agents and is active at DeepMind and OpenAI.[^1]

**Source:** Alex Wang, ["7 AI Terms You'll Hear a Lot This Year"](https://www.linkedin.com/pulse/7-ai-terms-youll-hear-lot-this-year-alex-wang) (LinkedIn Pulse).

---

## Definition

Reflective AI refers to systems that can "evaluate their own outputs and improve them, rather than producing a single response and stopping there."[^1] The core loop is: **generate → critique → revise**.

---

## Why It Matters

As AI systems become more autonomous, single-pass generation is insufficient.[^1] Three properties drive the pattern's value:

- Systems need mechanisms to **check their own reasoning**.
- They must be able to **identify mistakes and revise responses**.
- Reflection loops improve accuracy **without requiring additional training data**.[^1]

The source connects this to "nested learning" — models improving by reflecting on earlier steps.[^1]

---

## Where It Is Showing Up

| Actor | Activity |
|---|---|
| DeepMind | Research into systems that review and critique their own outputs.[^1] |
| OpenAI | Models that self-evaluate before producing a final answer.[^1] |
| Modern agent frameworks | Reflection used as a core loop (generate → critique → revise).[^1] |

---

## Key Takeaways

1. Self-correction is becoming an **essential capability** for advanced AI systems.[^1]
2. Reflection loops deliver accuracy gains without retraining.[^1]
3. The pattern is described as "foundational to the next generation of autonomous AI agents."[^1]

---

## Relation to Corpus Pages

- [AI Agent](/ai-engineering/ai-agent.md) — reflection loops are presented here as foundational to autonomous agents.
- [Agent Evaluation](/ai-engineering/agent-evaluation.md) — self-evaluation is the same judgement the eval layer applies externally.
- [Neurosymbolic AI](/ai-engineering/sources/neurosymbolic-ai-improving-ai-reasoning-ea.md) — sibling section of the same Alex Wang article; complementary approach to reasoning reliability (symbolic grounding there, self-correction here), not a competing claim.
- ["7 AI Terms You'll Hear a Lot This Year" (Alex Wang)](/ai-engineering/seven-ai-terms-2026-alex-wang.md) — shared-provenance synthesis: this page and four siblings all derive from that single article, so they do not corroborate each other.
- [AI Engineering hub](/ai-engineering/README.md)

---

[^1]: raw/notes/notes-03-resources-articles-reflective-ai-systems-that-learn-from-their-mistakes.md — Alex Wang, "7 AI Terms You'll Hear a Lot This Year."

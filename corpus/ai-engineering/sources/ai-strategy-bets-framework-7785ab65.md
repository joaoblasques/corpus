---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/web-your-ai-strategy-is-making-bets-do-you-know-which-ones-7785ab65.md
    channel: web
    ingested_at: 2026-08-24
aliases:
  - AI strategy bets framework
  - token economics bets
  - model self-sufficiency bet
  - platform lock-in bet
  - Dan Pupius framework
  - The General Partnership AI framework
  - fragile token abundance
tags:
  - corpus/ai-engineering
created: 2026-08-24
updated: 2026-08-24
---

# AI Strategy Is Making Bets. Do You Know Which Ones?

**TL;DR**: Dan Pupius (CTO, The General Partnership) argues that AI startup strategy is implicitly a set of bets across four axes — token economics, model self-sufficiency, platform lock-in, and regulatory environment. Most companies do not name these bets explicitly, which means they cannot act when the bet goes wrong [^src1].

> "Instead of asking 'What do we think will happen?', ask yourself two fundamental questions. First: What assumptions are irreversible? Second: What assumptions can we still revise?" [^src1]

## The four-axis bet framework

### Axis 1: Token economics — scarce ↔ abundant

Current state: "fragile token abundance" — tokens are cheap enough that products like Cursor can run AI continuously in the background and still be profitable [^src1].

The trap: if everyone can build the same thing for pennies, cost alone is not a moat [^src1].

| Bet | What it requires |
|---|---|
| Scarcity bet | Articulate why falling costs don't destroy your advantage (e.g., always-on agents at volume, latency-sensitive voice AI) |
| Abundance bet | Build advantage from: proprietary data, domain expertise, distribution, or cost-variance reduction (predictable billing vs. average price) |

Healthcare example: "Even as per-token prices fall, being able to tell a client 'Your bill won't exceed X' is valuable" — worst-case cost reduction is defensible even when average price races to zero [^src1].

### Axis 2: Model self-sufficiency — needs scaffolding ↔ handles natively

This axis determines the fate of "model wrapper" companies [^src1]. If the product augments what models can do (memory, retrieval, multi-step orchestration), that bet has an expiration date — the model may absorb those capabilities natively.

- **Harvey** (AI for law firms) and **Sierra** (customer service AI) are examples of companies betting that general models won't match their niche performance [^src1].

Diagnostic question: "Would my product still be needed if the model had unlimited capabilities?" [^src1]

The partially-disclosed axes (article behind paywall) also include:
- **Axis 3: Platform lock-in — reversible ↔ irreversible**: building on one model provider requires rewiring the product to leave; "you need to rewire the product to move away from that provider" [^src1].
- **Axis 4: Regulatory environment**: viral compliance trends may be more impactful than government regulation.

## How to use the framework

The goal is not to predict the future more precisely — it is to "recognize sooner when you're wrong and move before the market forces you to" [^src1].

Two structural questions per axis [^src1]:
1. What happens to this bet if the environment changes in the worst-case direction?
2. How hard is it to update the product if this bet is wrong?

Irreversible bets (deep platform integration, single-provider architecture) require a higher conviction threshold. Reversible bets (token cost assumptions, scaffolding approaches) can be held loosely and revised cheaply [^src1].

## Relationship to model wrapper debate

The framework reframes the "AI wrapper" criticism as vague [^src1]. The real question is not whether the product is a wrapper, but which bets the wrapper strategy embeds — and whether those bets are named and monitored. A company betting on model self-sufficiency remaining low (axis 2) is making a specific, trackable bet, not a generic "wrapper" play.

## See also

- [AI Agent](/ai-engineering/ai-agent.md) — agents are primary consumers in the token economics axis
- [Long-Running Agents](/ai-engineering/long-running-agents.md) — always-on agentic workloads are the scarce-token abundance exception case
- [Agent Harness](/ai-engineering/agent-harness.md) — harness vs. model as the axis-2 bet surface

---

[^src1]: [Your AI Strategy Is Making Bets. Do You Know Which Ones?](../../../raw/web/web-your-ai-strategy-is-making-bets-do-you-know-which-ones-7785ab65.md) — Dan Pupius (CTO, The General Partnership), Every, 2026-07-01; four-axis bet framework, fragile token abundance, Harvey/Sierra examples

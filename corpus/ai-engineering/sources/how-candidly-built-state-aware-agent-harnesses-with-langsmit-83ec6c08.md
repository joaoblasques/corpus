---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/web-how-candidly-built-state-aware-agent-harnesses-with-langsmit-83ec6c08.md
    channel: web
    ingested_at: 2026-08-21
aliases:
  - Candidly state-aware agent harness
  - IO-HMM agent evaluation
  - LangSmith conversation state
tags:
  - corpus/ai-engineering
  - source
created: 2026-08-21
updated: 2026-08-21
---

# How Candidly Built State-Aware Agent Harnesses with LangSmith

**TL;DR.** Candidly trained an Input-Output Hidden Markov Model (IO-HMM) on LangSmith conversation traces to infer turn-level engagement state; state-aware prompt policies injected into the harness halved the share of conversations in the "Disengaging" state. Evaluation becomes a *control signal* rather than a post-hoc grade. [^src1]

## Key concepts

**The standard evaluation problem.** Conversational agents are typically judged on conversation-level outcomes (resolved / abandoned), observed only at the end. But the agent acts turn by turn. To optimize during a conversation you need a turn-level model of where the interaction is. [^src1]

**Hybrid labeling pipeline.** Candidly used deterministic rules for clear outcomes (explicit frustration, no reply, product follow-through) + LLM-as-judge for ambiguous cases, calibrated against a human-labeled LangSmith dataset to 92.3% agreement. Labels attach to threads as LangSmith feedback. [^src1]

**Predictive features:**
- Q/A alignment: lexical overlap between Cait's response and the user prompt — highest predictor of resolution; low alignment → failing state signature
- Topic continuity: semantic similarity between consecutive agent responses — coherence predicts resolution
- Message length: longer user messages → resolution; short/one-word → exit
- Caps ratio: proportion of user text in caps — frustration signal [^src1]

**Result:** Gradient-boosted model on these features separated resolved from abandoned at **0.90 AUC**. [^src1]

**IO-HMM architecture.** Separates each turn:
- User-side signals → *emissions* (what we observe to infer latent state)
- Agent-side features → *transition inputs* (what the agent can control)

Fitted via expectation-maximization on thousands of conversations. Settled on **four engagement states** (five-state model didn't recover stable, interpretable regimes). [^src1]

**Four engagement states.** Resolution probability ranges from ~78% in the most engaged state to ~30% in the disengaging state. The same agent behavior helps in one state and hurts in another — pooled averages mask state-conditional effects entirely. [^src1]

**Wiring the policy into the harness:**
1. State inference runs on every turn inside the request path (milliseconds — lightweight deterministic compute)
2. Each inferred state maps to a versioned prompt-policy regime in LangSmith
3. Policies are verified offline on held-out LangSmith data before shipping
4. Randomized A/B assignment provides causal identification
5. Inferred state, prompt version, arm, outcome, and activation all live on the same trace [^src1]

**Result:** State-aware policy halved the share of turns in the Disengaging state (23% → 11%) and raised turns in Engaged state (53% → 64%). [^src1]

**Generalizable principle.** Any multi-turn agent with a goal has: (1) an outcome observed at the end, (2) turn-level signals computable from the trace, (3) behaviors the agent controls. The recipe applies beyond financial conversations — coding agents, orchestrators managing subagents. "State is the layer that connects those two views with more precision." [^src1]

## Related pages

- [Agent Harness](/ai-engineering/agent-harness.md)
- [LLM Evals](/ai-engineering/llm-evals.md)
- [AI Agent](/ai-engineering/ai-agent.md)

[^src1]: raw/_inbox/web-how-candidly-built-state-aware-agent-harnesses-with-langsmit-83ec6c08.md (LangChain blog / Candidly, channel: web, 2026-06-30)

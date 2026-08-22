---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/web-what-is-sakana-fugu-the-multi-model-orchestrator-that-routes-617e27b3.md
    channel: web
    ingested_at: 2026-08-22
aliases:
  - Sakana Fugu
  - Fugu
  - Fugu Ultra
  - Sakana AI orchestrator
  - LLM router Sakana
tags:
  - corpus/ai-engineering
  - entity
  - model-routing
  - multi-model
  - orchestration
confidence: 0.85
last_confirmed: 2026-08-22
created: 2026-08-22
updated: 2026-08-22
---

# Sakana Fugu

**TL;DR.** Sakana Fugu is a *trained orchestrator model* from Sakana AI (Tokyo, founded 2023) that classifies incoming prompts and routes them to the best-fit model in a pool — upfront, before generation, not an ensemble. Two tiers: Fugu (routine/high-volume) and Fugu Ultra (complex/unpredictable/high-stakes). [^fugu1]

## What it does

Fugu sits above a pool of AI models and makes a routing decision for each prompt:
1. **Prompt classification**: analyze structure, length, domain indicators, complexity signals
2. **Model pool matching**: map task classification to best-fit model (by capability profile, latency, cost/token)
3. **Cost-quality optimization**: cheap/fast for simple tasks; frontier for high-complexity
4. **Confidence + fallback**: when routing confidence is low, escalate to a stronger model

This is *not* an ensemble (calling multiple models and comparing). Fugu routes to one model upfront, before generation. [^fugu1]

## Fugu vs. Fugu Ultra

| Tier | Best for |
|---|---|
| Fugu | Predictable task types (customer support, content gen, summarization, Q&A); cost efficiency; high-volume; low-latency routing |
| Fugu Ultra | Complex/unpredictable agentic workflows; high-stakes outputs; specialized domains (legal, medical, technical); outputs where routing errors are costly |

## Sakana AI context

Founded 2023 in Tokyo; co-founders include Llion Jones (one of the original "Attention Is All You Need" authors). Research philosophy: collective intelligence from many smaller specialized components outperforms one massive model. Name means "fish" in Japanese; Fugu = pufferfish. [^fugu1]

## When multi-model routing makes sense

For high-volume pipelines with diverse task types, smart routing can achieve near-frontier quality at significantly lower cost. Not justified for single-purpose apps where all tasks are similar. Routing adds latency — problematic for real-time user interactions. [^fugu1]

## Limitations

- Router adds a generation step before the main generation (latency overhead)
- Router errors: ambiguous prompts may be misclassified → wrong model
- Reduced controllability: routing decision is opaque (learned, not rule-based)
- Pool dependency: effectiveness limited by the quality of models in the pool
- Benchmark drift: model capabilities shift; routing model trained on historical benchmarks may lag

## Landscape comparison

- **RouteLLM** (LMSYS, open-source): similar concept, model-agnostic
- **Martian**: commercial routing product focused on cost-quality tradeoffs
- **Fugu differentiator**: Sakana AI's research-first approach + integrated pool of specialized models

## Related

- [/ai-engineering/sources/model-routing-choosing-the-right-model-for-the-job-b.md](/ai-engineering/sources/model-routing-choosing-the-right-model-for-the-job-b.md)
- [/ai-engineering/sources/sakana-fugu-multi-model-orchestrator-617e27b3.md](/ai-engineering/sources/sakana-fugu-multi-model-orchestrator-617e27b3.md)

[^fugu1]: MindStudio Blog, "What Is Sakana Fugu? The Multi-Model Orchestrator That Routes Prompts Automatically," mindstudio.ai, 2026-06-30. `raw/_inbox/web-what-is-sakana-fugu-the-multi-model-orchestrator-that-routes-617e27b3.md`

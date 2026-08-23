---
type: source
domain: ai-engineering
status: complete
sources:
  - path: raw/_inbox/web-micro-agent-beat-frontier-models-with-collaboration-inside-m-22bd7e8d.md
    channel: web
    ingested_at: 2026-08-23
aliases:
  - vLLM Micro-Agent post
  - Micro-Agent looper patterns
tags:
  - corpus/ai-engineering
  - source
created: 2026-08-23
updated: 2026-08-23
---

# Micro-Agent: Beat Frontier Models with Collaboration Inside Model API (vLLM, 2026-06-29)

**Source**: vllm.ai blog — `raw/_inbox/web-micro-agent-beat-frontier-models-with-collaboration-inside-m-22bd7e8d.md`

## Summary

vLLM blog post introducing the Micro-Agent concept and documenting five looper patterns in vLLM Semantic Router, framing the router as a control plane that makes collaboration a first-class serving primitive. [^1]

## Core framing: router as control plane

Routers already own cost routing, safety policy, and cloud/edge coordination. The next job: **make the model better** by turning one API call into a bounded collaboration inside the serving layer — without requiring applications to build bespoke agent graphs. [^1]

The contrast: Sakana Fugu made a commercial product out of collaboration behind one endpoint; vLLM Semantic Router bets collaboration should be an **open serving primitive**, not locked inside one commercial endpoint. [^1]

## The Looper as execution runtime

The looper is the execution runtime for bounded micro-agents in vLLM Semantic Router. A request enters as an ordinary chat completion; the router may select a looper route instead of a single-model route. [^1]

## Five looper patterns

1. **Confidence** — sequential escalation. Try a cheaper model first, measure confidence (via log-probs, entailment verifier, etc.), escalate only when confidence is below threshold. Best for: cost-aware routing where most requests don't need frontier models. [^1]

2. **Ratings** — bounded fan-out. Run multiple candidates in parallel up to a `max_concurrent` cap; aggregate with rating-aware weights. Best for: A/B evaluation, ensemble strategies. [^1]

3. **ReMoM** (Repeated Mixture-of-Models) — breadth + synthesis. Fan out multiple reasoning attempts, wait for a quorum of successes, run a synthesis model to merge into the required output contract. Best for: high-variance reasoning tasks where output format must survive collaboration. [^1]

4. **Fusion** — disagreement as signal. Independent panel models generate answers; a judge analyzes agreement/contradiction/unique insight; a finalizer returns one answer. Best for: hard multiple-choice, long-form expert judgment, tasks where a single confident response is brittle. [^1]

5. **Workflows** — micro-agent workflow runtime. A planner (static or dynamic) assigns worker steps; bounded by max_steps, max_parallelism, timeouts, and output contract. Best for: SWE-style tasks needing planner + patcher + verifier + finalizer without a custom agent stack per application. [^1]

## Auto recipes: vllm-sr/auto

The public surface remains one model name (`vllm-sr/auto`); internally the router selects the right loop based on signals (difficulty, risk, latency, cost, contract pressure). [^1]

**Key lesson**: "The best loop is task-shaped." Different benchmarks need different recipes:
- GPQA-Diamond → ReMoM (strict multiple-choice preservation)
- LiveCodeBench → code-shaped loop (hidden-test robustness)
- Humanity's Last Exam → Fusion or deeper ReMoM (disagreement resolution) [^1]

## Benchmark scorecard (closed-model recipes)

| Benchmark | Score | vs. Reference frontier |
|---|---|---|
| LiveCodeBench (Jan–Apr 2025) | 92.6 | Fugu Ultra 92.0, GPT-5.5 90.7 |
| GPQA-Diamond | 96.0 | Fugu Ultra 95.5, Gemini 3.1 Pro 94.3 |
| Humanity's Last Exam (Closed) | 50.0 | Fugu Ultra 50.0, Fugu 48.5 |

## Distinction: serving runtime vs. app logic

"This is the difference between 'agent as app logic' and 'micro-agent as serving runtime.'" The router controls budget, policy, topology, trace, and failure mode. [^1]

## Related pages

- [/ai-engineering/vllm-semantic-router.md](/ai-engineering/vllm-semantic-router.md) — full vLLM Semantic Router page (updated with looper patterns)
- [/ai-engineering/vllm.md](/ai-engineering/vllm.md)
- [/ai-engineering/multi-agent-systems.md](/ai-engineering/multi-agent-systems.md)

[^1]: raw/_inbox/web-micro-agent-beat-frontier-models-with-collaboration-inside-m-22bd7e8d.md

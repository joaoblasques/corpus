---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/web-glm-5-2-built-for-long-horizon-tasks-64d6b4cb.md
    channel: web
    ingested_at: 2026-07-04
  - path: raw/web/web-glm-5-2-is-probably-the-most-powerful-text-only-open-weights-42e4b84f.md
    channel: web
    ingested_at: 2026-07-05
aliases:
  - GLM-5
  - GLM-5.2
  - GLM 5.2
  - ZhipuAI GLM
tags:
  - corpus/ai-engineering
  - entity
created: 2026-07-04
updated: 2026-07-05
---

# GLM-5

**TL;DR.** GLM-5.2 is ZhipuAI's open-source (MIT) frontier LLM optimized for long-horizon agentic coding tasks — 1M-token context that "stably sustains long-horizon work," three effort levels (balanced/max), and architecture improvements that reduce per-token FLOPs by 2.9× at 1M context via **IndexShare** [^src1]. On the FrontierSWE long-horizon coding benchmark, GLM-5.2 trails Opus 4.8 by only 1% while ranking first among open-source models [^src1].

## Key claims (vendor-reported)

| Benchmark | GLM-5.2 | Comparable |
|---|---|---|
| FrontierSWE (long-horizon) | 2nd open, -1% vs Opus 4.8 | Beats GPT-5.5 by +1%, Opus 4.7 by +11% |
| PostTrainBench (post-training on H100) | 2nd overall | Beats Opus 4.7 + GPT-5.5; trails Opus 4.8 |
| SWE-Marathon (ultra-long, build compilers etc.) | 2nd open | -13% vs Opus 4.8 |
| Terminal-Bench 2.1 | 81.0 (highest open) | Claude Opus 4.8: 85.0, Gemini 3.1 Pro: lower |
| SWE-bench Pro | 62.1 (vs 58.4 for GLM-5.1) | — |

These are ZhipuAI/Hugging Face self-reported figures [^src1].

## Architecture improvements (GLM-5.2 vs GLM-5.1)

### IndexShare (DSA — Distributed Sparse Attention)

To support 1M context at manageable compute cost, GLM-5.2 introduces **IndexShare**: every 4 transformer layers share a single lightweight indexer for sparse attention [^src1]. The indexer computes top-k indices once; the next 3 layers reuse them. This cuts the per-token FLOPs of indexer dot-product + top-k by 2.9× at 1M context length vs. GLM-5.1 [^src1].

### MTP with IndexShare and KVShare (speculative decoding)

The Multi-Token Prediction (MTP) draft head is also improved for speculative decoding acceptance rate [^src1]. IndexShare is applied to the MTP layer (multi-step MTP reuses one indexer across steps). KVShare enables the MTP head to attend to tokens the backbone can't, eliminating the training/inference discrepancy present in GLM-5.1's MTP [^src1].

### Effort-level control

GLM-5.2 introduces explicit **effort levels** for users to trade capability against speed/compute [^src1]. At comparable token budgets, GLM-5.2 sits between Claude Opus 4.7 and 4.8 on agentic coding; the Max effort level pushes performance further at higher compute cost.

## Deployment

- **License**: MIT — "no regional limits, technical access without borders" [^src1]
- **Context**: 1M tokens, with training specifically expanded for messy long-context coding-agent trajectories [^src1]
- **Available on**: Hugging Face Hub (weights)

## Community benchmarks (independent)

Simon Willison reported in June 2026 that GLM-5.2 was "probably the most powerful text-only open weights LLM" based on the Artificial Analysis Intelligence Index [^src2]:
- Score of **51** on the Artificial Analysis Intelligence Index — leading open-weights model at that date
- Ranked **#2 on Code Arena WebDev leaderboard** (behind Claude Fable 5)
- Available on **OpenRouter at $1.40 input / $4.40 output per million tokens** [^src2]
- Token-hungry: averages ~**43,000 output tokens per task** on the WebDev benchmark — notably higher than other models [^src2]

These are Artificial Analysis / Code Arena leaderboard figures as reported by Simon Willison, not ZhipuAI self-reported benchmarks.

Note: Z.ai (source of the Hugging Face blog) and ZhipuAI are the same entity — Z.ai is ZhipuAI's rebranded name.

## Related

- [vLLM](/ai-engineering/vllm.md) — high-throughput serving engine; GLM-5.x is vLLM-compatible
- [Quantization](/ai-engineering/quantization.md) — effort levels affect token budget (not quantization bits directly, but related to inference cost)
- [Simon Willison](/ai-engineering/simon-willison.md) — independent coverage of GLM-5.2 community benchmarks
- [AI Engineering hub](/ai-engineering/README.md)

---

[^src1]: [GLM-5.2: Built for Long-Horizon Tasks](../../raw/_inbox/web-glm-5-2-built-for-long-horizon-tasks-64d6b4cb.md) — Hugging Face blog, ZhipuAI, 2026-06
[^src2]: [GLM-5.2 is probably the most powerful text-only open weights LLM](../../raw/web/web-glm-5-2-is-probably-the-most-powerful-text-only-open-weights-42e4b84f.md) — Simon Willison, 2026-06-17

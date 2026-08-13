---
type: source
domain: ai-engineering
status: stub
sources:
  - path: raw/_inbox/web-qwen3-results-on-the-aider-polyglot-benchmark-06e6dd83.md
    channel: web
    ingested_at: 2026-08-13
aliases:
  - Qwen3 aider benchmark
  - Qwen3 polyglot benchmark
tags:
  - corpus/ai-engineering
  - source
  - open-source-models
  - benchmarks
  - coding-agents
  - qwen
created: 2026-08-13
updated: 2026-08-13
---

# Qwen3 Results on the Aider Polyglot Benchmark

TL;DR: Inference settings, quantization, and API provider significantly affect Qwen3 coding performance. Best result (65.3%) achieved with VLLM + bfloat16 + no-think mode; default thinking mode with mixed OpenRouter providers drops to 49.8%. Model choice matters less than serving configuration.

## Key Findings [^qwen3]

**Top results (Qwen3 235B-A22B)**:

| Configuration | Correct | Edit format |
|---|---|---|
| VLLM, bfloat16, no_think, whole | 65.3% | whole |
| Official Alibaba API, no think, whole | 61.8% | whole |
| VLLM, bfloat16, no_think, diff | 61.3% | diff |
| Official Alibaba API, no think, diff | 59.6% | diff |
| llama.cpp, Q5_K_M (unsloth), no_think, whole | 59.1% | whole |
| OpenRouter (TogetherAI only), no_think, diff | 54.7% | diff |
| OpenRouter (all providers), default/thinking, diff | 49.8% | diff |

**Qwen3 32B** (VLLM, bfloat16, no_think): 45.8% (whole) / 41.3% (diff).

**Key lessons**:
1. **Inference settings matter more than provider branding**: 15+ percentage points separate best from worst Qwen3 235B configurations.
2. **No-think mode outperforms thinking mode** for coding tasks on Qwen3 — "thinking" adds tokens without improving edit correctness.
3. **Provider heterogeneity degrades performance**: mixed OpenRouter providers use different quantizations and inference settings; single-provider (TogetherAI only) gains ~5 points over mixed.
4. **bfloat16 beats quantized**: Q5_K_M achieves 59.1% vs. 65.3% for bfloat16 — quantization costs ~6 points at the top.
5. **Correct edit format matters**: `whole` format achieves 100% correct edit format; `diff` achieves 91–95%, with the gap explaining some of the score difference.

**Recommended settings** for Qwen3 on OpenRouter:
```yaml
system_prompt_prefix: "/no_think"
use_temperature: 0.7
extra_params:
  max_tokens: 24000
  top_p: 0.8
  top_k: 20
  min_p: 0.0
  temperature: 0.7
```

Note: Gemini 2.5 Pro Preview 03-25 cost was found incorrectly reported (litellm was not including reasoning tokens in counts prior to v1.67.1 / April 21, 2025); true cost was significantly higher than the $6.32 figure that appeared on leaderboards.[^qwen3]

## Cross-links

- [/ai-engineering/README.md](/ai-engineering/README.md)

---

[^qwen3]: raw/_inbox/web-qwen3-results-on-the-aider-polyglot-benchmark-06e6dd83.md — aider.chat/blog/

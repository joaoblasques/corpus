---
type: entity
domain: ai-engineering
status: stub
sources:
  - path: raw/_inbox/web-qwen3-max-vs-gpt-5-1-benchmarks-pricing-context-window-reque-0f32c73c.md
    channel: web
    ingested_at: 2026-08-23
  - path: raw/_inbox/web-qwen3-7-plus-vs-gpt-5-1-benchmarks-pricing-context-window-re-02a1e8fa.md
    channel: web
    ingested_at: 2026-08-23
aliases: [Qwen3, Qwen3-Max, Qwen3.7-Plus, alibaba/qwen3-max, alibaba/qwen3.7-plus, Qwen 3]
tags: [alibaba, frontier-model, llm, value, agentic]
created: 2026-08-23
updated: 2026-08-23
---

# Qwen3

Alibaba Cloud's Qwen3 frontier model family. Two variants benchmarked here:

**Qwen3-Max**: $0.86/$3.44 per 1M input/output tokens, 262K context. Vision input, tool calling, prompt caching; no reasoning mode. Intelligence Index 31.7%, GPQA Diamond 86.1%, τ²-Bench 83.6%, SciCode 43.1%, HLE 26.2%. GPT-5.1 outperforms it on 5 of 6 shared benchmarks.[^1]

**Qwen3.7-Plus**: $0.32/$1.28 per 1M input/output tokens, 1.0M context. Outperforms GPT-5.1 on all 6 shared benchmarks: Intelligence Index 39.0%, GPQA Diamond 90.0%, τ²-Bench 93.0%, Coding Index 55.9%, SciCode 45.5%, HLE 33.4%.[^2]

See benchmark comparisons: [/ai-engineering/llm-benchmarks-2026.md](/ai-engineering/llm-benchmarks-2026.md)

[^1]: raw/_inbox/web-qwen3-max-vs-gpt-5-1-benchmarks-pricing-context-window-reque-0f32c73c.md
[^2]: raw/_inbox/web-qwen3-7-plus-vs-gpt-5-1-benchmarks-pricing-context-window-re-02a1e8fa.md

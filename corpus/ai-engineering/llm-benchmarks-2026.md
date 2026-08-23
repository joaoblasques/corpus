---
type: synthesis
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/web-gpt-4-1-vs-gpt-5-1-benchmarks-pricing-context-window-request-5e673749.md
    channel: web
    ingested_at: 2026-08-23
  - path: raw/_inbox/web-gemini-2-5-pro-vs-gpt-5-1-benchmarks-pricing-context-window-823eb2bb.md
    channel: web
    ingested_at: 2026-08-23
  - path: raw/_inbox/web-gemini-2-5-flash-vs-gpt-5-1-benchmarks-pricing-context-windo-76d93e4d.md
    channel: web
    ingested_at: 2026-08-23
  - path: raw/_inbox/web-gpt-5-1-vs-grok-4-benchmarks-pricing-context-window-requesty-49e62d64.md
    channel: web
    ingested_at: 2026-08-23
  - path: raw/_inbox/web-gpt-5-1-vs-grok-4-3-benchmarks-pricing-context-window-reques-e6f79ad6.md
    channel: web
    ingested_at: 2026-08-23
  - path: raw/_inbox/web-deepseek-v4-pro-vs-gpt-5-1-benchmarks-pricing-context-window-a71932e2.md
    channel: web
    ingested_at: 2026-08-23
  - path: raw/_inbox/web-deepseek-v4-flash-vs-gpt-5-1-benchmarks-pricing-context-wind-65af9fb3.md
    channel: web
    ingested_at: 2026-08-23
  - path: raw/_inbox/web-qwen3-max-vs-gpt-5-1-benchmarks-pricing-context-window-reque-0f32c73c.md
    channel: web
    ingested_at: 2026-08-23
  - path: raw/_inbox/web-qwen3-7-plus-vs-gpt-5-1-benchmarks-pricing-context-window-re-02a1e8fa.md
    channel: web
    ingested_at: 2026-08-23
  - path: raw/_inbox/web-gpt-5-1-vs-glm-5-1-benchmarks-pricing-context-window-request-5312780a.md
    channel: web
    ingested_at: 2026-08-23
  - path: raw/_inbox/web-minimax-m3-vs-gpt-5-1-benchmarks-pricing-context-window-requ-a13f5d83.md
    channel: web
    ingested_at: 2026-08-23
  - path: raw/_inbox/web-gpt-5-1-vs-kimi-k2-benchmarks-pricing-context-window-request-dd91d37f.md
    channel: web
    ingested_at: 2026-08-23
  - path: raw/_inbox/web-kimi-k2-7-code-vs-gpt-5-1-benchmarks-pricing-context-window-1483133c.md
    channel: web
    ingested_at: 2026-08-23
  - path: raw/_inbox/web-gpt-4-1-vs-gpt-5-benchmarks-pricing-context-window-requesty-dc2f7d1a.md
    channel: web
    ingested_at: 2026-08-23
aliases: [frontier model benchmarks, LLM comparison 2026, model pricing comparison]
tags: [benchmarks, pricing, frontier-models, gpt-5, deepseek, grok, qwen, kimi, gemini]
created: 2026-08-23
updated: 2026-08-23
---

# Frontier LLM Benchmarks & Pricing — 2026 Reference

TL;DR: As of mid-2026, GPT-5.1 leads most benchmark categories but costs the same as Gemini 2.5 Pro ($1.25/$10.00 per 1M tokens). DeepSeek V4 models offer striking value — competitive or superior benchmark scores at a fraction of the price. Multiple non-OpenAI models (DeepSeek V4 Flash, Qwen3.7-Plus, MiniMax M3, GLM-5.1, Grok-4.3, Kimi K2.7-code) outperform GPT-5.1 on at least some benchmarks while costing significantly less.

Data sourced from Requesty model comparison pages (collected 2026-06-30). Scores from official model cards, Artificial Analysis, and public leaderboards.

---

## Pricing & Specifications Summary

| Model | Provider | Input $/1M | Output $/1M | Context | Max Output | Reasoning |
|---|---|---|---|---|---|---|
| GPT-5.1 | OpenAI | $1.25 | $10.00 | 400K | 128K | Yes |
| GPT-5 | OpenAI | $1.25 | $10.00 | 400K | 128K | Yes |
| GPT-4.1 | OpenAI | $2.00 | $8.00 | 1.0M | 33K | No |
| Gemini 2.5 Pro | Google | $1.25 | $10.00 | 1.0M | 66K | Yes |
| Gemini 2.5 Flash | Google | $0.30 | $2.50 | 1.0M | 66K | Yes |
| Grok-4 | xAI | $3.00 | $15.00 | 256K | N/A | No |
| Grok-4.3 | xAI | $1.25 | $2.50 | 1M | N/A | Yes |
| DeepSeek V4 Pro | DeepSeek | $0.43 | $0.87 | 1M | 384K | No |
| DeepSeek V4 Flash | DeepSeek | $0.14 | $0.28 | 1M | 384K | No |
| Qwen3-Max | Alibaba | $0.86 | $3.44 | 262K | 66K | No |
| Qwen3.7-Plus | Alibaba | $0.32 | $1.28 | 1.0M | 66K | No |
| GLM-5.1 | Z.ai | $1.40 | $4.40 | 200K | 128K | Yes |
| MiniMax M3 | MiniMax | $0.30 | $1.20 | 1M | 128K | Yes |
| Kimi K2 | Moonshot AI | $0.60 | $2.50 | 262K | 262K | Yes |
| Kimi K2.7-code | Moonshot AI | $0.95 | $4.00 | 262K | 262K | Yes |

[^gpt51-gpt41]: raw/_inbox/web-gpt-4-1-vs-gpt-5-1-benchmarks-pricing-context-window-request-5e673749.md
[^gpt5-gpt41]: raw/_inbox/web-gpt-4-1-vs-gpt-5-benchmarks-pricing-context-window-requesty-dc2f7d1a.md
[^gemini-pro]: raw/_inbox/web-gemini-2-5-pro-vs-gpt-5-1-benchmarks-pricing-context-window-823eb2bb.md
[^gemini-flash]: raw/_inbox/web-gemini-2-5-flash-vs-gpt-5-1-benchmarks-pricing-context-windo-76d93e4d.md
[^grok4]: raw/_inbox/web-gpt-5-1-vs-grok-4-benchmarks-pricing-context-window-requesty-49e62d64.md
[^grok43]: raw/_inbox/web-gpt-5-1-vs-grok-4-3-benchmarks-pricing-context-window-reques-e6f79ad6.md
[^dsv4pro]: raw/_inbox/web-deepseek-v4-pro-vs-gpt-5-1-benchmarks-pricing-context-window-a71932e2.md
[^dsv4flash]: raw/_inbox/web-deepseek-v4-flash-vs-gpt-5-1-benchmarks-pricing-context-wind-65af9fb3.md
[^qwen3max]: raw/_inbox/web-qwen3-max-vs-gpt-5-1-benchmarks-pricing-context-window-reque-0f32c73c.md
[^qwen37plus]: raw/_inbox/web-qwen3-7-plus-vs-gpt-5-1-benchmarks-pricing-context-window-re-02a1e8fa.md
[^glm51]: raw/_inbox/web-gpt-5-1-vs-glm-5-1-benchmarks-pricing-context-window-request-5312780a.md
[^minimax]: raw/_inbox/web-minimax-m3-vs-gpt-5-1-benchmarks-pricing-context-window-requ-a13f5d83.md
[^kimik2]: raw/_inbox/web-gpt-5-1-vs-kimi-k2-benchmarks-pricing-context-window-request-dd91d37f.md
[^kimik27]: raw/_inbox/web-kimi-k2-7-code-vs-gpt-5-1-benchmarks-pricing-context-window-1483133c.md

---

## Benchmark Scores

Benchmarks vary by comparison page; N/A means score not reported for that model in these sources.

### Intelligence Index (reasoning composite)

| Model | Score |
|---|---|
| MiniMax M3 | 44.4% [^minimax] |
| DeepSeek V4 Pro | 44.3% [^dsv4pro] |
| Kimi K2.7-code | 41.9% [^kimik27] |
| GLM-5.1 | 40.2% [^glm51] |
| Qwen3.7-Plus | 39.0% [^qwen37plus] |
| **GPT-5.1** | **38.9%** [^gpt51-gpt41] |
| DeepSeek V4 Flash | 40.3% [^dsv4flash] |
| Grok-4 | 33.3% [^grok4] |
| Grok-4.3 | 37.6% [^grok43] |
| Kimi K2 | 32.7% [^kimik2] |
| Qwen3-Max | 31.7% [^qwen3max] |
| Gemini 2.5 Pro | 25.8% [^gemini-pro] |
| Gemini 2.5 Flash | 20.1% [^gemini-flash] |
| GPT-5 | 36.1% [^gpt5-gpt41] |
| GPT-4.1 | 19.4% [^gpt51-gpt41] |

### Math Index / AIME 2025

| Model | Math Index | AIME 2025 |
|---|---|---|
| **GPT-5.1** | **94.0%** | **94.0%** [^gpt51-gpt41] |
| GPT-5 | 94.3% | 94.3% [^gpt5-gpt41] |
| Kimi K2 | 94.7% | 94.7% [^kimik2] |
| Grok-4 | 92.7% | 92.7% [^grok4] |
| Gemini 2.5 Pro | 87.7% | 87.7% [^gemini-pro] |
| Gemini 2.5 Flash | 73.3% | 73.3% [^gemini-flash] |
| GPT-4.1 | 34.7% | 34.7% [^gpt51-gpt41] |

Note: DeepSeek V4, Qwen3, GLM-5.1, MiniMax M3, Kimi K2.7-code, Grok-4.3 had no Math Index / AIME score reported.

### GPQA Diamond (graduate-level science reasoning)

| Model | Score |
|---|---|
| MiniMax M3 | 92.9% [^minimax] |
| Qwen3.7-Plus | 90.0% [^qwen37plus] |
| Grok-4.3 | 90.1% [^grok43] |
| Kimi K2.7-code | 89.6% [^kimik27] |
| DeepSeek V4 Flash | 89.4% [^dsv4flash] |
| DeepSeek V4 Pro | 88.8% [^dsv4pro] |
| **GPT-5.1** | **87.3%** [^gpt51-gpt41] |
| GPT-5 | 85.4% [^gpt5-gpt41] |
| Gemini 2.5 Pro | 84.4% [^gemini-pro] |
| Kimi K2 | 83.8% [^kimik2] |
| Gemini 2.5 Flash | 79.0% [^gemini-flash] |
| Grok-4 | 87.7% [^grok4] |
| GLM-5.1 | 86.8% [^glm51] |
| Qwen3-Max | 86.1% [^qwen3max] |
| GPT-4.1 | 66.6% [^gpt51-gpt41] |

### LiveCodeBench (coding)

| Model | Score |
|---|---|
| **GPT-5.1** | **86.8%** [^gpt51-gpt41] |
| GPT-5 | 84.6% [^gpt5-gpt41] |
| Kimi K2 | 85.3% [^kimik2] |
| Gemini 2.5 Pro | 80.1% [^gemini-pro] |
| Grok-4 | 81.9% [^grok4] |
| Gemini 2.5 Flash | 69.5% [^gemini-flash] |
| GPT-4.1 | 45.7% [^gpt51-gpt41] |

Note: DeepSeek V4, Qwen3, GLM-5.1, MiniMax M3, Grok-4.3, Kimi K2.7-code had no LiveCodeBench score reported.

### Coding Index (where reported)

| Model | Score |
|---|---|
| Kimi K2.7-code | 60.8% [^kimik27] |
| DeepSeek V4 Pro | 59.4% [^dsv4pro] |
| MiniMax M3 | 58.6% [^minimax] |
| DeepSeek V4 Flash | 56.2% [^dsv4flash] |
| Qwen3.7-Plus | 55.9% [^qwen37plus] |
| GLM-5.1 | 55.8% [^glm51] |
| Grok-4.3 | 42.2% [^grok43] |
| Gemini 2.5 Pro | 33.3% [^gemini-pro] |

### τ²-Bench (agentic / tool use)

| Model | Score |
|---|---|
| Grok-4.3 | 97.7% [^grok43] |
| GLM-5.1 | 97.7% [^glm51] |
| DeepSeek V4 Pro | 96.2% [^dsv4pro] |
| DeepSeek V4 Flash | 95.0% [^dsv4flash] |
| Qwen3.7-Plus | 93.0% [^qwen37plus] |
| Kimi K2.7-code | 90.1% [^kimik27] |
| MiniMax M3 | 88.9% [^minimax] |
| Kimi K2 | 93.0% [^kimik2] |
| Qwen3-Max | 83.6% [^qwen3max] |
| GPT-5 | 84.8% [^gpt5-gpt41] |
| **GPT-5.1** | **81.9%** [^gpt51-gpt41] |
| Grok-4 | 74.9% [^grok4] |
| Gemini 2.5 Pro | 54.1% [^gemini-pro] |
| Gemini 2.5 Flash | 31.6% [^gemini-flash] |
| GPT-4.1 | 47.1% [^gpt51-gpt41] |

### Humanity's Last Exam (HLE — hardest reasoning)

| Model | Score |
|---|---|
| **GPT-5.1** | **26.5%** [^gpt51-gpt41] |
| GPT-5 | 26.5% [^gpt5-gpt41] |
| Grok-4.3 | 35.0% [^grok43] |
| MiniMax M3 | 37.1% [^minimax] |
| DeepSeek V4 Pro | 35.9% [^dsv4pro] |
| Kimi K2.7-code | 32.8% [^kimik27] |
| Qwen3.7-Plus | 33.4% [^qwen37plus] |
| DeepSeek V4 Flash | 32.1% [^dsv4flash] |
| Gemini 2.5 Pro | 21.1% [^gemini-pro] |
| Grok-4 | 23.9% [^grok4] |
| Kimi K2 | 22.3% [^kimik2] |
| GLM-5.1 | 28.0% [^glm51] |
| Qwen3-Max | 26.2% [^qwen3max] |
| Gemini 2.5 Flash | 11.1% [^gemini-flash] |
| GPT-4.1 | 4.6% [^gpt51-gpt41] |

---

## Key Observations

**Value leaders**: DeepSeek V4 Flash ($0.14/$0.28) and Gemini 2.5 Flash ($0.30/$2.50) and MiniMax M3 ($0.30/$1.20) offer very competitive scores at a fraction of GPT-5.1's cost. DeepSeek V4 Flash outperforms GPT-5.1 on 5 of 6 shared benchmarks while costing ~10× less on input.[^dsv4flash]

**Agentic outliers**: Multiple models dramatically exceed GPT-5.1 on τ²-Bench (tool use): Grok-4.3 (97.7%), GLM-5.1 (97.7%), DeepSeek V4 Pro (96.2%), DeepSeek V4 Flash (95.0%). GPT-5.1's 81.9% is solid but not leading.[^grok43][^glm51][^dsv4pro]

**Math / reasoning**: GPT-5.1 and GPT-5 lead on Math Index (94.0%/94.3%) and AIME 2025, with Kimi K2 slightly ahead on math (94.7%). Grok-4 is competitive (92.7%) but more expensive.[^kimik2][^grok4]

**Context window**: GPT-5.1's 400K context is mid-tier; Gemini 2.5 Pro/Flash and DeepSeek V4 offer 1M context. GPT-4.1 has 1M context but lower performance and max output of only 33K.[^gpt51-gpt41][^gemini-pro]

**GPT-5 vs GPT-5.1**: Scores are nearly identical (GPT-5.1 slightly higher on some reasoning benchmarks, GPT-5 slightly higher on math). Both share the same pricing ($1.25/$10.00).[^gpt5-gpt41][^gpt51-gpt41]

---

## Related Pages

- [/ai-engineering/gpt-5-1.md](/ai-engineering/gpt-5-1.md)
- [/ai-engineering/grok-4.md](/ai-engineering/grok-4.md)
- [/ai-engineering/deepseek-v4.md](/ai-engineering/deepseek-v4.md)
- [/ai-engineering/qwen3.md](/ai-engineering/qwen3.md)
- [/ai-engineering/kimi-k2.md](/ai-engineering/kimi-k2.md)
- [/ai-engineering/minimax-m3.md](/ai-engineering/minimax-m3.md)
- [/ai-engineering/glm-5.md](/ai-engineering/glm-5.md)

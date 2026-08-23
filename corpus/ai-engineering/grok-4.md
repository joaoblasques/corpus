---
type: entity
domain: ai-engineering
status: stub
sources:
  - path: raw/_inbox/web-gpt-5-1-vs-grok-4-benchmarks-pricing-context-window-requesty-49e62d64.md
    channel: web
    ingested_at: 2026-08-23
  - path: raw/_inbox/web-gpt-5-1-vs-grok-4-3-benchmarks-pricing-context-window-reques-e6f79ad6.md
    channel: web
    ingested_at: 2026-08-23
aliases: [Grok-4, xai/grok-4, Grok 4, Grok-4.3, xai/grok-4.3]
tags: [xai, frontier-model, llm, agentic]
created: 2026-08-23
updated: 2026-08-23
---

# Grok-4

xAI's frontier model family. Two variants compared here:

**Grok-4**: $3.00/$15.00 per 1M input/output tokens, 256K context. Supports computer use (unlike GPT-5.1). Competitive on GPQA Diamond (87.7%) and math (AIME 92.7%), but GPT-5.1 leads overall (8 of 10 benchmarks).[^1]

**Grok-4.3**: $1.25/$2.50 per 1M input/output tokens, 1M context. Much cheaper output than GPT-5.1. Outperforms GPT-5.1 on 4 of 6 benchmarks; notably: τ²-Bench 97.7% (vs GPT-5.1's 81.9%), GPQA Diamond 90.1%, HLE 35.0%. Math scores not reported.[^2]

See benchmark comparisons: [/ai-engineering/llm-benchmarks-2026.md](/ai-engineering/llm-benchmarks-2026.md)

[^1]: raw/_inbox/web-gpt-5-1-vs-grok-4-benchmarks-pricing-context-window-requesty-49e62d64.md
[^2]: raw/_inbox/web-gpt-5-1-vs-grok-4-3-benchmarks-pricing-context-window-reques-e6f79ad6.md

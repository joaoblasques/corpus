---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-claude-opus-4-8-vs-gpt-5-benchmarks-pricing-context-window-r-20f42447.md
    channel: web
    ingested_at: 2026-07-02
aliases: []
tags:
  - corpus/ai-engineering
  - source
  - doc-quick-intake
created: 2026-07-02
updated: 2026-08-23
provisional: false
url: https://www.requesty.ai/models/compare/anthropic--claude-opus-4-8/openai--gpt-5
origin: obsidian-list
---

# claude-opus-4-8 vs gpt-5: Benchmarks, Pricing & Context Window | Requesty

**TL;DR:** Side-by-side comparison of Claude Opus 4.8 and GPT-5 across benchmarks, pricing, and context window, published by Requesty — a unified API provider for 400+ models.[^src]

[^src]: raw/web/web-claude-opus-4-8-vs-gpt-5-benchmarks-pricing-context-window-r-20f42447.md

---

## Pricing & Specifications

| Spec | claude-opus-4-8 | gpt-5 |
|---|---|---|
| Input / 1M tokens | $5.00 | $1.25 |
| Output / 1M tokens | $25.00 | $10.00 |
| Context window | 1M tokens | 400K tokens |
| Max output | 128K tokens | 128K tokens |
| Vision input | Yes | Yes |
| Tool calling | Yes | Yes |
| Reasoning | Yes | Yes |
| Prompt caching | Yes | Yes |
| Computer use | Yes | N/A |
| Provider | Anthropic PBC | OpenAI Inc. |

GPT-5 is cheaper: at $1.25/$10.00 per 1M input/output tokens vs. Claude Opus 4.8's $5.00/$25.00.[^src] Claude Opus 4.8 offers a 1M-token context window vs. GPT-5's 400K.[^src]

---

## Benchmark Comparison

Source notes: "Scores sourced from official model cards, Artificial Analysis, and public leaderboards. Benchmarks measure specific skills and don't capture every aspect of model quality."[^src]

| Benchmark | Category | claude-opus-4-8 | gpt-5 |
|---|---|---|---|
| Intelligence Index | reasoning | 55.7% | 36.1% |
| Coding Index | coding | 74.3% | N/A |
| Math Index | math | N/A | 94.3% |
| GPQA Diamond | reasoning | 92.0% | 85.4% |
| AIME 2025 | math | N/A | 94.3% |
| LiveCodeBench | coding | N/A | 84.6% |
| Terminal-Bench Hard | agentic | 58.3% | 32.6% |
| τ²-Bench | agentic | 94.4% | 84.8% |
| SciCode | coding | 53.5% | 42.9% |
| MMLU Pro | knowledge | N/A | 87.1% |
| Humanity's Last Exam | reasoning | 45.7% | 26.5% |

"claude-opus-4-8 outperforms gpt-5 on 6 of 6 shared benchmarks."[^src] The source characterizes Claude Opus 4.8 as stronger on reasoning and agentic tasks, while GPT-5 leads on math benchmarks (AIME 2025: 94.3%, Math Index: 94.3%) where Claude Opus 4.8 scores are not available.[^src]

---

## Requesty Unified API

Requesty provides a single OpenAI-compatible API routing to both models. The source states: "Change just the 'model' parameter to switch between 'anthropic/claude-opus-4-8' and 'openai/gpt-5', no other code changes needed."[^src] Model IDs are `anthropic/claude-opus-4-8` and `openai/gpt-5`.

---

## Notes on Coverage

This source is a comparison page from a commercial API aggregator (Requesty). Benchmark data is aggregated from third-party sources and may lag model card updates. N/A entries indicate a benchmark was not reported for that model at the time of collection, not necessarily that the model performs poorly on it.

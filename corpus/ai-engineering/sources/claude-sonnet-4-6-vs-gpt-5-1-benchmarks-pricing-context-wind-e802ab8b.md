---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-claude-sonnet-4-6-vs-gpt-5-1-benchmarks-pricing-context-wind-e802ab8b.md
    channel: web
    ingested_at: 2026-07-02
aliases: []
tags:
  - corpus/ai-engineering
  - source
  - doc-quick-intake
created: 2026-07-02
updated: 2026-08-24
provisional: false
url: https://www.requesty.ai/models/compare/anthropic--claude-sonnet-4-6/openai--gpt-5.1
origin: obsidian-list
---

# claude-sonnet-4-6 vs gpt-5.1: Benchmarks, Pricing & Context Window

**Source:** Requesty model comparison page (2026-06-30). [open source](https://www.requesty.ai/models/compare/anthropic--claude-sonnet-4-6/openai--gpt-5.1)

**TL;DR:** claude-sonnet-4-6 outperforms gpt-5.1 on 5 of 6 shared benchmarks but costs more and carries a larger context window (1M vs 400K tokens). gpt-5.1 is cheaper and leads on math and coding-specific tasks where scores are available.[^src]

---

## Pricing & Specifications

| Attribute | claude-sonnet-4-6 | gpt-5.1 |
|---|---|---|
| Input / 1M tokens | $3.00 | $1.25 |
| Output / 1M tokens | $15.00 | $10.00 |
| Context window | 1M tokens | 400K tokens |
| Max output | 64K tokens | 128K tokens |
| Vision input | Yes | Yes |
| Tool calling | Yes | Yes |
| Reasoning | Yes | Yes |
| Prompt caching | Yes | Yes |
| Computer use | Yes | No |
| Provider | Anthropic PBC | OpenAI Inc. |

gpt-5.1 is cheaper: "claude-sonnet-4-6 costs $3.00/$15.00 per 1M input/output tokens, while gpt-5.1 costs $1.25/$10.00."[^src]

---

## Benchmark Comparison

Scores sourced from official model cards, Artificial Analysis, and public leaderboards (per source). Benchmarks measure specific skills and do not capture every aspect of model quality.[^src]

| Benchmark | Category | claude-sonnet-4-6 | gpt-5.1 |
|---|---|---|---|
| Intelligence Index | reasoning | 47.2% | 38.9% |
| Coding Index | coding | 63.0% | N/A |
| Math Index | math | N/A | 94.0% |
| GPQA Diamond | reasoning | 87.5% | 87.3% |
| AIME 2025 | math | N/A | 94.0% |
| LiveCodeBench | coding | N/A | 86.8% |
| Terminal-Bench Hard | agentic | 53.0% | 45.5% |
| τ²-Bench | agentic | 75.7% | 81.9% |
| SciCode | coding | 46.8% | 43.3% |
| MMLU Pro | knowledge | N/A | 87.0% |
| Humanity's Last Exam | reasoning | 30.0% | 26.5% |

**Pattern:** claude-sonnet-4-6 leads on reasoning (Intelligence Index, GPQA Diamond, Humanity's Last Exam) and agentic tasks (Terminal-Bench Hard). gpt-5.1 leads on math (AIME 2025, Math Index) and the agentic τ²-Bench. Many benchmark slots are N/A for one model, limiting direct comparison.[^src]

---

## Requesty Unified API

Both models are accessible through Requesty's single OpenAI-compatible API. "Change just the 'model' parameter to switch between 'anthropic/claude-sonnet-4-6' and 'openai/gpt-5.1', no other code changes needed."[^src] Model IDs: `anthropic/claude-sonnet-4-6` and `openai/gpt-5.1`.

---

## Context Window Note

claude-sonnet-4-6 supports up to 1M tokens of context; gpt-5.1 supports up to 400K tokens. The source notes: "quality often degrades past 128K for most models."[^src]

---

[^src]: Requesty model comparison page, collected 2026-06-30. [`raw/web/web-claude-sonnet-4-6-vs-gpt-5-1-benchmarks-pricing-context-wind-e802ab8b.md`](../../../raw/web/web-claude-sonnet-4-6-vs-gpt-5-1-benchmarks-pricing-context-wind-e802ab8b.md)

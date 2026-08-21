---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-claude-opus-4-6-vs-deepseek-r1-benchmarks-pricing-context-wi-37679b99.md
    channel: web
    ingested_at: 2026-07-02
aliases: []
tags:
  - corpus/ai-engineering
  - source
  - doc-quick-intake
created: 2026-07-02
updated: 2026-08-21
provisional: false
url: https://www.requesty.ai/models/compare/anthropic--claude-opus-4-6/novita--deepseek-deepseek-r1
origin: obsidian-list
---

# "claude-opus-4-6 vs deepseek-r1: Benchmarks, Pricing & Context Window | Requesty"

**TL;DR:** claude-opus-4-6 outperforms deepseek-r1 on every shared benchmark but costs significantly more for output tokens. deepseek-r1 is cheaper and stronger on pure math/coding tasks where claude-opus-4-6 has no published score.[^1]

[^1]: [raw/web/web-claude-opus-4-6-vs-deepseek-r1-benchmarks-pricing-context-wi-37679b99.md](../../../raw/web/web-claude-opus-4-6-vs-deepseek-r1-benchmarks-pricing-context-wi-37679b99.md)

---

## Pricing & specifications

| Attribute | claude-opus-4-6 | deepseek-r1 |
|---|---|---|
| Provider | Anthropic PBC | Novita AI |
| Input / 1M tokens | $5.00 | $4.00 |
| Output / 1M tokens | $25.00 | $4.00 |
| Context window | 1M tokens | 64K tokens |
| Max output | 128K tokens | N/A |
| Vision input | Yes | N/A |
| Tool calling | Yes | Yes |
| Reasoning | Yes | N/A |
| Prompt caching | Yes | N/A |
| Computer use | Yes | N/A |

Source: [^1]. Output pricing gap is stark: claude-opus-4-6 is 6.25× more expensive per output token. The context window gap is equally large: claude-opus-4-6 supports up to 1M tokens vs. deepseek-r1's 64K.[^1]

---

## Benchmark comparison

Scores sourced from official model cards, Artificial Analysis, and public leaderboards per [^1]. N/A indicates no published score for that model on that benchmark.

| Benchmark | Category | claude-opus-4-6 | deepseek-r1 |
|---|---|---|---|
| Intelligence Index | reasoning | 43.7% | 20.1% |
| GPQA Diamond | reasoning | 89.6% | 81.3% |
| Humanity's Last Exam | reasoning | 36.7% | 14.9% |
| Terminal-Bench Hard | agentic | 46.2% | 15.9% |
| τ²-Bench | agentic | 92.1% | 36.5% |
| SciCode | coding | 51.9% | 40.3% |
| Math Index | math | N/A | 76.0% |
| AIME 2025 | math | N/A | 76.0% |
| LiveCodeBench | coding | N/A | 77.0% |
| MMLU Pro | knowledge | N/A | 84.9% |

"claude-opus-4-6 outperforms deepseek-r1 on 6 of 6 shared benchmarks."[^1] On the 4 benchmarks where only deepseek-r1 has a published score (Math Index, AIME 2025, LiveCodeBench, MMLU Pro), no comparison can be drawn — these happen to be math and knowledge-heavy tasks.

### Strength profiles

- **claude-opus-4-6** leads decisively on agentic tasks (τ²-Bench: 92.1% vs 36.5%; Terminal-Bench Hard: 46.2% vs 15.9%) and reasoning benchmarks.[^1]
- **deepseek-r1** has stronger published math scores (AIME 2025: 76.0%, Math Index: 76.0%) and a broader knowledge benchmark (MMLU Pro: 84.9%), though claude-opus-4-6 has no published score on those tasks.[^1]

---

## API access via Requesty

Both models are accessible through Requesty's unified OpenAI-compatible API. "Change just the 'model' parameter to switch between 'anthropic/claude-opus-4-6' and 'novita/deepseek/deepseek-r1', no other code changes needed."[^1]

Model IDs on Requesty: `anthropic/claude-opus-4-6` and `novita/deepseek/deepseek-r1`.[^1]

---

## Tradeoffs summary

| Decision factor | Favors |
|---|---|
| Lowest output cost | deepseek-r1 ($4/M vs $25/M) |
| Longest context | claude-opus-4-6 (1M vs 64K) |
| Agentic / tool use tasks | claude-opus-4-6 |
| Reasoning benchmarks | claude-opus-4-6 |
| Math benchmarks (published) | deepseek-r1 |
| Vision, computer use, caching | claude-opus-4-6 only |

Source: [^1]. Note: benchmark gaps reflect published scores as of collection date (2026-07-01); missing scores mean no published result, not a zero.

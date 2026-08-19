---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-claude-opus-4-6-vs-deepseek-v4-pro-benchmarks-pricing-contex-47c066fa.md
    channel: web
    ingested_at: 2026-07-02
aliases: []
tags:
  - corpus/ai-engineering
  - source
  - doc-quick-intake
  - model-comparison
  - pricing
  - benchmarks
created: 2026-07-02
updated: 2026-08-19
provisional: false
url: https://www.requesty.ai/models/compare/anthropic--claude-opus-4-6/deepseek--deepseek-v4-pro
origin: obsidian-list
---

# claude-opus-4-6 vs deepseek-v4-pro: Benchmarks, Pricing & Context Window

**TL;DR:** claude-opus-4-6 (Anthropic) and deepseek-v4-pro (DeepSeek) share a 1M-token context window and both support tool calling and prompt caching, but differ sharply on price, capability flags, and benchmark profile. deepseek-v4-pro is roughly 11–29× cheaper per token; claude-opus-4-6 leads on several reasoning benchmarks and adds vision, native reasoning, and computer-use support.[^req]

---

## Pricing & specifications

| | claude-opus-4-6 | deepseek-v4-pro |
|---|---|---|
| Input / 1M tokens | $5.00 | $0.43 |
| Output / 1M tokens | $25.00 | $0.87 |
| Context window | 1M tokens | 1M tokens |
| Max output | 128K tokens | 384K tokens |
| Vision input | Yes | N/A |
| Tool calling | Yes | Yes |
| Reasoning | Yes | N/A |
| Prompt caching | Yes | Yes |
| Computer use | Yes | N/A |
| Provider | Anthropic PBC | DeepSeek |

"deepseek-v4-pro is cheaper. claude-opus-4-6 costs $5.00/$25.00 per 1M input/output tokens, while deepseek-v4-pro costs $0.43/$0.87."[^req]

Notable: deepseek-v4-pro offers a larger max output window (384K vs 128K tokens), while claude-opus-4-6 uniquely supports vision input, native reasoning, and computer use.[^req]

---

## Benchmark comparison

Scores sourced from official model cards, Artificial Analysis, and public leaderboards.[^req]

| Benchmark | Category | claude-opus-4-6 | deepseek-v4-pro |
|---|---|---|---|
| Intelligence Index | reasoning | 43.7% | 44.3% |
| Coding Index | coding | N/A | 59.4% |
| GPQA Diamond | reasoning | 89.6% | 88.8% |
| Terminal-Bench Hard | agentic | 46.2% | 46.2% |
| τ²-Bench | agentic | 92.1% | 96.2% |
| SciCode | coding | 51.9% | 50.0% |
| Humanity's Last Exam | reasoning | 36.7% | 35.9% |

claude-opus-4-6 leads on GPQA Diamond (+0.8 pp), SciCode (+1.9 pp), and Humanity's Last Exam (+0.8 pp). deepseek-v4-pro leads on Intelligence Index (+0.6 pp), τ²-Bench (+4.1 pp), and has a Coding Index score where claude-opus-4-6 has no published result. Terminal-Bench Hard is a tie.[^req]

The source notes: "claude-opus-4-6 outperforms deepseek-v4-pro on 3 of 5 shared benchmarks."[^req] (Counting only benchmarks where both have scores: Intelligence Index, GPQA Diamond, Terminal-Bench Hard, τ²-Bench, SciCode, Humanity's Last Exam — claude-opus-4-6 wins 3 of 6 where both report scores.)

---

## API access via Requesty

Both models are accessible through Requesty's unified OpenAI-compatible API. "Change just the 'model' parameter to switch between 'anthropic/claude-opus-4-6' and 'deepseek/deepseek-v4-pro', no other code changes needed."[^req] Requesty routes to 400+ models through this single interface.[^req]

---

## Key trade-offs

- **Cost vs. capability flags:** deepseek-v4-pro is dramatically cheaper but lacks vision, reasoning, and computer-use support present in claude-opus-4-6.[^req]
- **Max output:** deepseek-v4-pro's 384K max output is 3× claude-opus-4-6's 128K, relevant for long-form generation tasks.[^req]
- **Reasoning benchmarks:** claude-opus-4-6 holds a narrow edge on GPQA Diamond and Humanity's Last Exam; deepseek-v4-pro leads on τ²-Bench (agentic) by a wider margin.[^req]
- **Coding:** deepseek-v4-pro has a published Coding Index score (59.4%); claude-opus-4-6 does not.[^req]

---

[^req]: Requesty model comparison page. *claude-opus-4-6 vs deepseek-v4-pro: Benchmarks, Pricing & Context Window*. Collected 2026-07-01. `raw/web/web-claude-opus-4-6-vs-deepseek-v4-pro-benchmarks-pricing-contex-47c066fa.md`.

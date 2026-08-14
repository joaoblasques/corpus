---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-evaluating-performance-and-efficiency-of-the-github-copilot-bdecf2cf.md
    channel: web
    ingested_at: 2026-08-14
aliases: []
tags:
  - corpus/ai-engineering
  - source
created: 2026-08-14
updated: 2026-08-14
---

# Evaluating Performance and Efficiency of the GitHub Copilot Agentic Harness

**TL;DR.** GitHub Copilot's shared agentic harness achieves task-resolution parity with model-vendor harnesses (Claude Code, Codex CLI) across SWE-bench Verified, SWE-bench Pro, SkillsBench, TerminalBench, and Win-Hill benchmarks — while consuming fewer tokens across most configurations — and supports 20+ frontier models without vendor lock-in.[^src1]

## Benchmarks used

GitHub evaluated its harness across five benchmarks[^src1]:

| Benchmark | Purpose |
|---|---|
| SWE-bench Verified | 500 human-validated bug-fix tasks (Python OSS repos) |
| SWE-bench Pro | Multi-step engineering tasks requiring deeper reasoning |
| SkillsBench | Evaluates effective skill use and triggering |
| TerminalBench | Agent performance on terminal-based tasks |
| Win-Hill | Internal benchmark for Windows containers |

Comparison models: Claude Sonnet 4.6, Claude Opus 4.7, GPT-5.4, GPT-5.5.[^src1]

## Key findings

- **Token efficiency**: Copilot harness uses fewer tokens across most configurations vs. model-vendor harnesses at equivalent task completion.[^src1]
- **Task resolution parity**: Differences vs. Claude Code / Codex CLI are within run-to-run variance — "effective parity."[^src1]
- **TerminalBench variance**: Copilot never fell below a competitor on completion or to the right on cost; run-to-run spread shows GPT models deliver best value (low cost, strong resolution) while Claude Opus reaches highest resolution at a premium.[^src1]
- **Multi-model**: Single harness spans GPT, Claude, Gemini, MAI, plus BYOK for open-source/local models.[^src1]

## Architecture insight: Rubber Duck

Copilot's harness enables **cross-model-family critique** ("Rubber Duck"): one model reviews another's work to improve outcomes beyond what any single model produces alone.[^src1] This is a harness-level capability unavailable to single-vendor harnesses.

## Methodology

All runs: two-hour timeout, non-interactive single-turn, web-tools disabled, all tools allowed, context window normalized, reasoning effort medium.[^src1] Variance measured across five independent runs; best run reported for small benchmarks (<100 instances) to reduce variability effects.

[^src1]: [Evaluating performance and efficiency of the GitHub Copilot agentic harness across models and tasks](https://github.blog/ai-and-ml/github-copilot/evaluating-performance-and-efficiency-of-the-github-copilot-agentic-harness-across-models-and-tasks/) — GitHub Blog, 2026-06-29 (raw/web/web-evaluating-performance-and-efficiency-of-the-github-copilot-bdecf2cf.md)

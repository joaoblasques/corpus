---
type: concept
domain: trading
status: draft
sources:
  - path: raw/youtube/youtube-6njREUQAFdg-how-to-build-a-self-improving-ai-trading-agent-insanely-cool.md
    channel: youtube
    ingested_at: 2026-06-25
aliases:
  - self-learning trading agent
  - Hermes agent trading
  - iterative trading agent
tags:
  - corpus/trading
  - concept
created: 2026-06-25
updated: 2026-06-25
---

# Self-Improving Trading Agents

TL;DR: A self-improving trading agent wraps a trading strategy in a feedback loop modeled on the scientific method: execute → observe outcome → form hypothesis about cause → change one variable → repeat. Hermes agent (an autonomous self-learning framework) enables this loop with minimal manual prompting by managing the improvement cycle itself.

## The four criteria for a good trading agent

Before designing self-improvement, the foundational requirements [^src1]:

1. **Accurate** — input data must be clean; APIs must be reliable; the same article fed to multiple agents should produce consistent conclusions (requires explicit rules to enforce objectivity)
2. **Reliable** — operates 24/7 even when the local computer is off; uses cloud hosting (Railway or similar) to persist independently
3. **Well-defined goal** — explicitly define success AND failure in measurable terms (e.g. target Sharpe ratio, max drawdown %, monthly return target); the agent can only learn toward the goal if it can measure distance from it
4. **Self-improving** — learns from outcomes; updates strategy; iterates

## The scientific method feedback loop

The self-improvement pattern mirrors the scientific method deliberately [^src1]:

1. Execute strategy → observe outcome (toward goal or away from goal?)
2. Form hypothesis about why the result was what it was
3. Form second hypothesis: what to do differently
4. **Change only one variable** (critical — changing multiple variables at once makes it impossible to attribute a good/bad result to any specific change)
5. New baseline becomes the best-performing prior version
6. Iterate from the new baseline

"You only change one variable at a time and you run a series of tests. Every time you get one better, that is now the new baseline, and then you make iterations on that new baseline." [^src1]

## Hermes agent

Hermes is an autonomous self-learning agent framework designed to manage the iteration cycle above without requiring the user to manually direct each step [^src1]:

- Installs as a CLI tool (`hermes` command in terminal)
- Manages portfolio mechanics and score weights
- Runs on a weekly review cadence (with 3-day offset from strategy update cycles to allow data to accumulate)
- First cycle is read-only (review only); flips to live trading mode when ready
- "The brain is Hermes. It's going to be watching the live service on weekly cadence." [^src1]
- Works in conjunction with other specialized agents (e.g. Cornelius, which tunes learned parameters weekly)

## One-shot setup prompt

The Hermes setup is triggered by a single prompt pasted into Claude Code [^src1]:

Phase sequence:
1. **Environment check** — detect OS (Mac vs. Windows), installed tools
2. **Strategy definition** — define success metrics, failure thresholds, Sharpe ratio target; either use existing strategy or generate a basic one
3. **Scaffold** — create folder/file structure for Hermes to read and write
4. **Strategy deployment** — connect live trading APIs (skipped if strategy already live)
5. **Railway deployment** — host the strategy execution 24/7 on Railway (free tier for moderate usage)
6. **Handoff to Hermes** — convert historical trade data to Hermes-readable ledger; install Hermes; set mode to review-only

## Multi-agent architecture

The demonstrated setup uses at least two specialized agents with distinct roles [^src1]:

| Agent | Role | Cadence |
|---|---|---|
| Strategy agent | Executes trades on the defined strategy (e.g. every 30 min) | Continuous / scheduled |
| Cornelius | Tunes learned parameters JSON based on accumulated data | Weekly |
| Hermes | Reviews trades, modifies score weights, decides when to flip to live | Weekly (3-day offset from Cornelius) |

This separation of concerns — one agent trades, one tunes parameters, one governs strategy evolution — prevents feedback loops from destabilizing running positions.

## Setup infrastructure

- **Claude Code** — primary development environment for agent setup and prompting
- **Railway** — cloud hosting for 24/7 strategy execution; CLI-based deployment; free tier sufficient for moderate workloads
- **Hermes** — installed as CLI tool; manages the improvement loop
- **Strategy YAML** — machine-readable strategy definition that Hermes can read and modify

Related: [AI Trading Agents](/trading/ai-trading-agents.md)

[^src1]: [How To Build A Self-Improving AI Trading Agent (Insanely Cool)](../../raw/youtube/youtube-6njREUQAFdg-how-to-build-a-self-improving-ai-trading-agent-insanely-cool.md)

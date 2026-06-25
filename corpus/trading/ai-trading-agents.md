---
type: concept
domain: trading
status: draft
sources:
  - path: raw/youtube/youtube-6MC1XqZSltw-i-turned-claude-into-a-24-7-trader.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-45eaVU5NVi8-the-simple-4-step-process-to-build-your-own-ai-trading-assis.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-3r7u6q-egP8-how-claude-changes-crypto-trading-forever.md
    channel: youtube
    ingested_at: 2026-06-25
aliases:
  - agentic trading bot
  - autonomous trading agent
  - AI trader
tags:
  - corpus/trading
  - concept
created: 2026-06-25
updated: 2026-06-25
---

# AI Trading Agents

TL;DR: An AI trading agent is a Claude Code (or similar agentic LLM) session that wakes on a cron schedule, reads its memory files, does market research, places/manages trades via a broker API, updates its memory for the next run, and sends notifications — all without human intervention. The agent is stateless per session; persistent "memory" lives entirely in files.

## Core architecture pattern

Every agent run follows the same loop [^src1]:

1. **Wake** — routine or cron fires (Claude Code routines, local or remote)
2. **Read** — ingest context files (strategy, trade log, learned parameters)
3. **Research** — fetch market data, news, signals (Perplexity API, native web search, on-chain APIs)
4. **Decide** — apply strategy rules; place/modify/close positions via broker API
5. **Write** — update memory files: trade log, weekly review, learned parameters
6. **Notify** — send end-of-day summary to ClickUp, Telegram, or similar

"Files aren't just memory, but they're essentially the agent's full personality and discipline" [^src1].

## Statelessness and memory architecture

Claude Code routines wake up essentially stateless — no persistent in-session memory [^src1]. The solution: every file the agent reads or writes persists across runs.

Key memory files:
- **Strategy file** — trading rules, signal definitions, entry/exit conditions
- **Trade log** — all historical positions with outcomes
- **Research log** — market notes accumulated over time
- **Weekly review** — self-evaluation and lessons learned

When running remote routines, the project must live in a GitHub repo so the cloud environment can clone it, execute, and push updated memory files back to `main` before destroying the environment [^src1].

## Cron scheduling pattern (equities)

A typical schedule for US equity markets [^src1]:

| Trigger | Day(s) | Purpose |
|---|---|---|
| 6:00 AM | Mon–Fri | Pre-market research; draft trade ideas; no notification unless urgent |
| 8:30 AM | Mon–Fri | Execute planned trades; set trailing stops (e.g. 10%); notify only on trade placed |
| 12:00 PM | Mon–Fri | Cut losers (e.g. −7%); tighten stops on winners |
| 3:00 PM | Mon–Fri | End-of-day review; close/hold decisions |
| 4:00 PM | Friday only | Weekly review; self-grade; push to repo |

## Context budget management

"Treat tokens like money" — each routine fires with a fixed context budget [^src1]. Practical rules:
- Each routine gets ~200k tokens to work with (even with million-token models, "context rot" is a real concern)
- System instructions, strategy files, trade log, and research all compete for that budget
- Prefer selective file reads over loading everything

## Guardrails (non-optional)

Before deploying with real money, define explicit constraints [^src1]:
- Max position size (e.g. 5% of portfolio per trade)
- Daily loss cap (absolute or % drawdown)
- Position count limit (e.g. no more than 3 new positions per week)
- Instrument restrictions ("no options ever", "no crypto", etc.)
- Paper trading mode first — toggle to live only after satisfactory paper results

## Four-step build workflow

From SMB Capital's practitioner approach [^src2]:

1. **Plan mode** — brainstorm in Claude Code's plan mode (no edits accepted). Use "ask user questions" mode with multiple-choice batches to define spec interactively; produces a `.md` implementation plan.
2. **Build mode** — hand the `.md` plan to a new session in build mode (edits accepted). Claude builds the skeleton HTML/dashboard/scripts.
3. **Personalize** — iterative tweaks in build mode: add tabs, stats, playbook rules, coach layer.
4. **Routine** — schedule the daily ritual (e.g. 4:15 PM close-of-day prompt) to auto-populate the dashboard.

The coach layer is a performance-analysis module that reads all historical trade write-ups, detects recurring patterns and mistakes (e.g. "no man's land sizing"), and surfaces them in a daily coach's note [^src2].

## Tech stack (common combinations)

| Component | Examples |
|---|---|
| AI agent | Claude Code (Opus 4.7), Hermes agent |
| Broker API | [[trading/alpaca-api\|Alpaca]] (equities), exchange APIs (crypto) |
| Research | Perplexity API, native web fetch/search |
| Charting | [[trading/tradingview-pine-script\|TradingView]] + Pine Script |
| Notifications | ClickUp, Telegram, Slack |
| Hosting | Claude Code remote routines, Railway |
| Version control | GitHub (required for remote routines) |

## Crypto-specific capabilities

When applied to crypto, agents can additionally [^src3]:
- Scan thousands of on-chain wallets on [[trading/hyperliquid\|Hyperliquid]] (public data; no API key required)
- Identify top 20 most profitable vs. most losing wallets; cross-reference positions to find divergence signals
- Scan all perpetuals pairs for funding rate opportunities (collect funding by positioning on the paying side; some annualized rates exceed 50–100%)
- Execute trades from natural-language commands via Telegram

Related: [[trading/self-improving-agents|Self-Improving Trading Agents]], [[trading/alpaca-api|Alpaca API]], [[trading/tradingview-pine-script|TradingView & Pine Script]]

[^src1]: [I Turned Claude Into a 24/7 Trader](../../raw/youtube/youtube-6MC1XqZSltw-i-turned-claude-into-a-24-7-trader.md)
[^src2]: [The Simple 4-Step Process To Build Your Own AI Trading Assistant With Claude](../../raw/youtube/youtube-45eaVU5NVi8-the-simple-4-step-process-to-build-your-own-ai-trading-assis.md)
[^src3]: [How Claude Changes Crypto Trading Forever](../../raw/youtube/youtube-3r7u6q-egP8-how-claude-changes-crypto-trading-forever.md)

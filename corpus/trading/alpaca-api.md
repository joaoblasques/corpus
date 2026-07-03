---
type: entity
domain: trading
status: draft
sources:
  - path: raw/youtube/youtube-6MC1XqZSltw-i-turned-claude-into-a-24-7-trader.md
    channel: youtube
    ingested_at: 2026-06-25
aliases:
  - Alpaca Markets
  - alpaca.markets
tags:
  - corpus/trading
  - entity
created: 2026-06-25
updated: 2026-06-25
---

# Alpaca API

TL;DR: Alpaca (alpaca.markets) is a commission-free brokerage with a REST API designed for algorithmic and AI-driven trading of US equities. It provides paper-trading accounts out of the box, making it the dominant choice for agent-based trading experiments before committing real money.

## What it is

Alpaca is a FINRA-registered broker-dealer that exposes its trading functionality via REST API endpoints. Unlike retail brokers designed for human use, Alpaca is built API-first: no human trading interface is required [^src1].

Key properties:
- **Commission-free** equities trading
- **Paper trading account** — $100,000 simulated balance provided by default; same API endpoints as live
- **Live account** — requires identity verification (may take a few days to approve)
- **Credentials** — API key + secret key pair; generated in dashboard under "Trading API"; secret only shown once at creation

## Setup for agent trading

1. Create account at alpaca.markets
2. Access the "Trading API" section of the dashboard
3. Generate key + secret (save the secret immediately — only shown once)
4. Store credentials as **environment variables**, never in `.env` files committed to GitHub [^src1]

When using Claude Code remote routines, store `ALPACA_API_KEY` and `ALPACA_SECRET_KEY` as environment variables in the Claude Cloud environment configuration (not in `.env`). All routine prompts must explicitly reference these env var names — a mismatch (e.g. `ALPACA_API_SECRET` vs `ALPACA_SECRET_KEY`) causes silent failures [^src1].

## Common API operations (agent use)

| Operation | Notes |
|---|---|
| Get account balance | Validates connectivity; use as first check in each routine |
| List open positions | Pre-trade state check |
| Place market/limit order | Main trade execution |
| Set stop-loss / take-profit | Post-entry position management |
| Get order history | Trade log population |

## Paper vs. live trading

The paper and live accounts use identical API credentials format and identical endpoints — only the base URL differs. Recommended approach: build and test entirely on paper until confident in the agent's behavior, then swap credentials [^src1].

"Start with paper trading first if you're not comfortable. This is not financial advice." [^src1]

Related: [AI Trading Agents](/trading/ai-trading-agents.md), [TradingView & Pine Script](/trading/tradingview-pine-script.md)

[^src1]: [I Turned Claude Into a 24/7 Trader](../../raw/youtube/youtube-6MC1XqZSltw-i-turned-claude-into-a-24-7-trader.md)

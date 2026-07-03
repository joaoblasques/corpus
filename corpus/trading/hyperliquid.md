---
type: entity
domain: trading
status: draft
sources:
  - path: raw/youtube/youtube-3r7u6q-egP8-how-claude-changes-crypto-trading-forever.md
    channel: youtube
    ingested_at: 2026-06-25
aliases:
  - Hyperliquid DEX
  - Hyperliquid perps
tags:
  - corpus/trading
  - entity
created: 2026-06-25
updated: 2026-06-25
---

# Hyperliquid

TL;DR: Hyperliquid is a decentralized perpetual futures exchange running on its own blockchain. All trades, positions, and wallet data are fully public on-chain — making it uniquely suited for AI-powered whale tracking and smart-money signal extraction without any API keys or KYC.

## What it is

Hyperliquid is a DeFi (decentralized finance) platform specifically for perpetual futures (perpetuals/perps) — derivatives contracts with no expiry date that track underlying asset prices. Key properties [^src1]:

- **No KYC** — no identity verification required
- **No middleman** — fully non-custodial, on-chain settlement
- **Fully transparent** — every trade, position, wallet, entry price, leverage, and unrealized P&L is public on-chain
- **Own blockchain** — not built on Ethereum or another L1; runs its own chain

## Why public data matters for AI agents

Because every position is on-chain and publicly readable, an AI agent can [^src1]:
- Scan 33,000+ wallet addresses in a single session
- Rank wallets by profitability (total P&L across all historical trades)
- Extract every open position for the top 20 most profitable wallets in real time
- Compare top-performing vs. worst-performing wallets to find divergence signals

Example output from such a scan: "Smart money is net long on Bitcoin and net short on almost everything else, especially Ethereum. Smart money is heavily long on XMR, TRX, Pendle, and Farcoin while losing traders are short on those coins." [^src1]

This type of analysis — historically requiring hours of manual research — takes under a minute with a Claude agent hitting Hyperliquid's public endpoints.

## Funding rate farming

Hyperliquid, like other perpetuals exchanges, pays funding every 8 hours [^src1]:
- **Positive funding** → longs pay shorts
- **Negative funding** → shorts pay longs
- Some annualized rates exceed 50–100%
- Strategy: scan all perpetuals pairs, identify highest funding rates, position on the receiving side

This is a market-neutral strategy (no directional bet on price) — profit comes purely from the funding payment.

## AI whale tracking workflow

Workflow demonstrated live [^src1]:
1. Agent hits Hyperliquid public endpoints
2. Pulls open position data across 33,000 addresses
3. Ranks wallets by profitability; builds ranked report
4. Compares profitable vs. losing wallets; cross-references positions token by token
5. Identifies tokens where smart money and losing traders are on **opposite sides** — that divergence is the signal

Related: [AI Trading Agents](/trading/ai-trading-agents.md), [TradingView & Pine Script](/trading/tradingview-pine-script.md)

[^src1]: [How Claude Changes Crypto Trading Forever](../../raw/youtube/youtube-3r7u6q-egP8-how-claude-changes-crypto-trading-forever.md)

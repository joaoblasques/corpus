---
type: entity
domain: trading
status: draft
sources:
  - path: raw/youtube/youtube-BiqG3it0gY0-a-polymarket-bot-made-438-000-in-30-days-your-industry-is-ne.md
    channel: youtube
    ingested_at: 2026-06-25
aliases:
  - Polymarket prediction market
tags:
  - corpus/trading
  - entity
created: 2026-06-25
updated: 2026-06-25
---

# Polymarket

TL;DR: Polymarket is an on-chain prediction market where users bet on the probability of real-world events. Its fully public on-chain data has made it a laboratory for AI arbitrage bots — demonstrated most vividly by a bot that turned $313 into $414,000 in one month (98% win rate, 6,600+ trades) by exploiting price update latency between Polymarket and spot crypto exchanges.

## What it is

Polymarket is a decentralized prediction market built on blockchain. Users trade binary contracts representing the probability of outcomes (e.g. "Will Bitcoin exceed $70k by end of month?"). Contracts settle to $0 or $1 based on real-world outcomes.

Key properties:
- All trades are on-chain and public
- Short-duration crypto contracts (e.g. 15-minute price direction contracts)
- Prices theoretically reflect consensus probability

## The landmark bot case

In late 2025, a single bot turned $313 into $414,000 in one month [^src1]:
- **Strategy**: exploit price update latency — Polymarket's short-duration crypto contracts updated prices much slower than the spot exchanges (Binance) tracking the same underlying assets
- **Mechanism**: when Bitcoin moved sharply on Binance, making a 15-minute contract outcome nearly certain, Polymarket still showed ~50/50 odds; the bot bought the mispriced side repeatedly
- **Win rate**: 98% across 6,600+ trades
- **No prediction required**: the bot did not forecast anything — it simply identified and exploited a structural pricing lag

A developer claimed to have reverse-engineered and rebuilt a working version in Rust using Claude in 40 minutes — covering real-time price monitoring, probability calculation, position sizing, and automated risk controls [^src1].

Additional documented results on Polymarket [^src1]:
- Separate Claude-powered system: $2.2M in 2 months using ensemble probability models trained on news and social data
- Sports contracts swarm model: $1.49M trading NBA contracts trained on 3 years of historical data
- Bots using identical strategies to human traders captured ~2x the profit — not better strategy, but flawless execution (no fatigue, no emotional overrides, no missed trades)

## Arbitrage window compression

Polymarket data makes the compression of arbitrage windows measurable in a way most markets cannot [^src1]:
- Average arbitrage window: 12.3 seconds in 2024 → 2.7 seconds in early 2026
- The mechanism: AI identifies the gap, builds the system to exploit it, compresses the window until only the most sophisticated players survive
- 94–95% of Polymarket wallets lose money, feeding the few sophisticated bots

See also: [[trading/prediction-markets|Prediction Markets]], [[trading/arbitrage-compression|Arbitrage Compression]]

[^src1]: [A Polymarket Bot Made $438,000 In 30 Days](../../raw/youtube/youtube-BiqG3it0gY0-a-polymarket-bot-made-438-000-in-30-days-your-industry-is-ne.md)

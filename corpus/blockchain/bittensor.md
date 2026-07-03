---
type: entity
domain: blockchain
status: draft
sources:
  - path: raw/youtube/youtube-99JCA0JScoA-top-3-bittensor-tao-subnets-explained.md
    channel: youtube
    ingested_at: 2026-06-25
aliases:
  - TAO
  - Bittensor network
  - BitTensor
tags:
  - corpus/blockchain
  - entity
created: 2026-06-25
updated: 2026-06-25
---

# Bittensor (TAO)

TL;DR: Bittensor is a decentralized AI network where specialized AI services (subnets) compete for token rewards based on performance. TAO is its native token. The network is analogized to Alphabet/Google — Bittensor is the parent, and individual subnets are its subsidiaries (like YouTube or Waymo within Google). Three highlighted subnets: Score Vision (subnet 44, computer vision analytics), Hippias (subnet 75, decentralized AI-native storage), and Quasar (subnet 24, extended-context LLM memory).

## What Bittensor is

Bittensor is a blockchain-based protocol that creates a marketplace for AI computation. Key properties [^src1]:

- **Subnet architecture** — specialized AI services run as subnets; each subnet competes for network-emitted TAO token rewards based on measured performance
- **Decentralized incentive** — miners provide AI compute/services; validators measure quality; rewards flow to best performers
- **Token**: TAO (native) + subnet-specific tokens

The Alphabet analogy [^src1]: "Bittensor is the Alphabet Inc. Within the Bittensor ecosystem, there are massive companies — subnets — that are currently brewing."

As of this source: 128 subnets exist.

## Subnet 44: Score Vision

**What it does**: AI that analyzes live camera feeds and converts them into structured real-time data [^src1].

Origin: Started in sports analytics (soccer/football), with partnerships from Bundesliga, Serie A, and Premier League. Expanded to general industrial and commercial computer vision.

**Sire bot**: Score's prediction-market bot that watches live soccer matches, tracks player stamina, formation data, and scoring probabilities in real time, then identifies betting market inefficiencies and places bets automatically.

**Monaco** (launched Q1 2026): No-code computer vision platform built on Bittensor. "Allows anyone to create advanced vision AI models through conversation. Just as AI coding assistants have simplified software development." [^src1]

Use cases cited by Score:
- **Tooday** (agricultural company) — converts factory camera feeds into structured quality/workflow data; reduces waste
- **Via** (European fuel retailer) — forecourt and in-store cameras → real-time operational intelligence, anomaly detection
- **Sports venues** — audience sentiment tracking during ads (facial expressions, body language); delivers actionable advertiser analytics

**Investment disclosure**: Source creator holds both Score subnet stake and SIRE token.

## Subnet 75: Hippias

**What it does**: Decentralized, AI-native cloud storage — described as "AWS S3 on distributed decentralized infrastructure" [^src1].

Key differentiators from Filecoin and Arweave:
- **AI-native** — built inside Bittensor; every Bittensor subnet inherently needs storage → built-in demand flywheel
- **Hybrid model** — supports both IPFS-style fully decentralized storage (permanent/public data) and S3-style user-pays per-GB model (familiar for businesses)
- **No single point of failure** — data distributed across multiple nodes; eliminates centralized outage risk
- **Dual incentive** — providers earn both storage fees and Bittensor subnet emissions (vs. Filecoin/Arweave's single revenue stream)
- **Filecoin comparison**: Filecoin reached $11B market cap in 2021; Hippias targets the same addressable market with AI-native positioning

Reliability motivation: AWS, Azure, and Google Cloud together experienced 100+ service outages in the 12 months between August 2024 and August 2025 [^src1].

## Subnet 24: Quasar

**What it does**: Extended context for LLMs — a mechanism to give AI models effectively unlimited memory and context length [^src1].

Technical claims:
- **5 million token context window** support (vs. ~200k practical limit of standard attention mechanisms)
- **Linear scaling** — computational cost scales linearly with context length, not quadratically (unlike standard attention)
- **Cost reduction**: claimed 99.5% cost reduction vs. traditional extended-context approaches
- Backed by Const, an OG Bittensor contributor/founder

Technical mechanism: "Quasar attention takes a different approach. It uses a continuous time formulation implemented as a fully matrix-based system" [^src1] — contrasted with gated delta attention (Qwen 3.5) and Kimi delta attention, which introduce instability at extreme lengths.

Use cases enabled by effective unlimited context:
- LLMs that read entire research libraries, complete legal document archives, or full codebases
- AI agents with persistent memory across weeks/months of conversations
- Enterprise analysis of multi-year company data without forgetting

"AI without memory can only go so far, but once it's remembering everything... that's when it becomes truly powerful." [^src1]

## TAO token and staking

The economic model [^src1]:
- TAO is the native token; subnet staking allows token holders to allocate stake to specific subnets
- Subnet tokens (e.g. SIRE for Score) represent subnet-specific economic participation
- Validators and miners within subnets earn emissions proportional to performance

Related: [Bitcoin](/blockchain/bitcoin.md), [Proof-of-Work](/blockchain/proof-of-work.md)

[^src1]: [Top 3 Bittensor TAO Subnets (Explained)](../../raw/youtube/youtube-99JCA0JScoA-top-3-bittensor-tao-subnets-explained.md)

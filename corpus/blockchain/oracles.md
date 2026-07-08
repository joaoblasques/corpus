---
type: concept
domain: blockchain
status: draft
sources:
  - path: raw/_inbox/book-mastering-ethereum-03-chapter-11-oracles.md
    channel: book
    ingested_at: 2026-07-08
aliases:
  - blockchain oracle
  - Chainlink
  - oracle problem
  - decentralized oracle
  - price feed
  - VRF
tags:
  - corpus/blockchain
  - concept
created: 2026-07-08
updated: 2026-07-08
---

# Oracles

TL;DR: Oracles bridge the gap between the deterministic, closed Ethereum execution environment and real-world data. The EVM cannot fetch external data natively; oracles inject it as transaction data. The trust problem — if the oracle is corrupted, the smart contract is corrupted — drives demand for decentralized oracle networks like Chainlink.

## Why Oracles Are Needed

The EVM must be completely deterministic; every node must arrive at the same state given the same inputs. Two consequences follow [^src1]:

1. **No intrinsic randomness** — a random function would cause nodes to diverge on state.
2. **No external data fetch** — extrinsic information (prices, weather, event results) can only enter as transaction data.

"All nodes can agree on the contents of signed transactions, so extrinsic information, including sources of randomness, price information, weather forecasts, and so on, can be introduced as the data part of transactions sent to the network. However, such data simply cannot be trusted because it comes from unverifiable sources" [^src1].

Oracles attempt to solve this by providing trustworthy (or near-trustworthy) external data feeds.

## Oracle Use Cases

Oracles provide [^src1]:
- **Price feeds** — ETH/USD, BTC/USD, token prices for DeFi lending, DEX pricing.
- **Randomness** — verifiable random numbers for lotteries, NFT minting, games (Chainlink VRF).
- **Event outcomes** — sports results, election results for prediction markets.
- **Real-world triggers** — weather data for parametric insurance; earthquake measurements for catastrophe bonds.
- **Cross-chain data** — token prices and state from other blockchains.
- **Attestations** — government IDs, academic credentials, KYC verification.
- **Time and intervals** — precise timing triggers for financial derivatives.
- **Interest rates** — benchmark rates (LIBOR equivalent) for on-chain derivatives.

## Oracle Designs

### Immediate-Read Oracles

Provide data only for immediate queries, not stored on chain. Example: a contract that directly queries an oracle address for the current ETH price at contract call time [^src1].

### Publish-Subscribe Oracles

Push data onto the chain proactively at regular intervals or on change. Price feeds from Chainlink operate this way — the oracle network writes the latest price to a smart contract every heartbeat or when deviation exceeds a threshold [^src1].

### Request-Response Oracles

The most flexible and complex pattern:
1. Smart contract emits an event requesting data.
2. An off-chain oracle node detects the event.
3. The node fetches the data, signs it, and submits it in a transaction back to the contract [^src1].

This requires the requesting contract to handle asynchronous responses (store a state variable while waiting).

## Centralized vs. Decentralized Oracles

**Centralized oracles** — a single entity controls the data feed. Simple and cheap but introduces a single point of failure and trust. "If the inheritance amount controlled by such a contract is high enough, the incentive to hack the oracle and trigger distribution of assets before the owner dies is very high" [^src1].

**Decentralized oracle networks (DONs)** — multiple independent nodes each fetch and sign data; an aggregation mechanism (median, weighted average) produces a final result. Chainlink is the dominant DON. Manipulation requires corrupting a supermajority of nodes simultaneously [^src1].

## Chainlink Architecture

Chainlink uses an on-chain aggregator contract plus a network of node operators:
- Each node operator fetches data independently.
- Nodes submit their answers on-chain.
- The aggregator computes a weighted median and stores it.
- Smart contracts read directly from the aggregator address.

Node operators are incentivized with LINK token payments and penalized (slashed) for submitting outlier data [^src1].

## Chainlink VRF (Verifiable Random Function)

Chainlink VRF provides cryptographically provable randomness. The oracle node generates a random number and a proof that it was generated from a specific seed and the node's private key. The proof is verifiable on-chain; no one — including the oracle node itself — can predict or manipulate the output [^src1].

## The Oracle Problem (Trust Minimization)

Even decentralized oracles require trust assumptions:
- Node operators may collude.
- Majority stake can be concentrated.
- API data sources themselves may be manipulated before the oracle reads them.

Fully trustless oracles remain an open research problem. The oracle problem is sometimes framed as "you cannot bring real-world data on-chain without trusting someone" [^src1].

## Oracle Manipulation Attacks

Price oracle manipulation is a major DeFi attack vector:
- Flash loans can briefly move spot prices on DEXes used as oracles.
- Contracts relying on a single DEX spot price as a price feed are vulnerable.
- Time-weighted average prices (TWAPs) over multiple blocks resist flash-loan manipulation [^src1].

## Cross-links

- [Smart Contracts](/blockchain/smart-contracts.md) — oracle data is consumed by smart contracts.
- [DeFi](/blockchain/defi.md) — price feeds, interest rates, and liquidation triggers rely on oracles.
- [Smart Contract Security](/blockchain/smart-contract-security.md) — oracle manipulation is a major vulnerability class.
- [Ethereum Transactions](/blockchain/ethereum-transactions.md) — oracle data enters the chain as transaction data.
- [Zero-Knowledge Proofs](/blockchain/zero-knowledge-proofs.md) — ZK attestations may reduce oracle trust requirements.

[^src1]: [Mastering Ethereum — Chapter 11. Oracles](../../raw/_inbox/book-mastering-ethereum-03-chapter-11-oracles.md)

---
type: concept
domain: blockchain
status: draft
sources:
  - path: raw/_inbox/book-mastering-ethereum-11-chapter-3-ethereum-nodes.md
    channel: book
    ingested_at: 2026-07-08
aliases:
  - Ethereum client
  - execution client
  - consensus client
  - Geth
  - full node
tags:
  - corpus/blockchain
  - concept
created: 2026-07-08
updated: 2026-07-08
---

# Ethereum Nodes

TL;DR: Post-Merge, an Ethereum node runs *two* pieces of software: an execution client (runs the EVM, verifies transactions) and a consensus client (implements Gasper PoS). Client diversity across five execution and five consensus implementations is a security property of the network.

## Dual-Client Architecture

Before The Merge (September 15, 2022) a single client implemented all Ethereum requirements. The Merge separated concerns into two layers [^src1]:

**Execution client** — receives blocks and transactions, executes them in the EVM, and verifies their correctness. Handles the "what happened" part of state transitions.

**Consensus client** — runs the Gasper PoS consensus protocol, allowing all nodes to agree on a single chain history. Handles the "which chain is canonical" part.

Both clients must run simultaneously and communicate over an Engine API (local RPC). Neither is sufficient alone.

## Execution Clients (as of June 2025)

| Client | Language | Notes |
|---|---|---|
| Geth | Go | Oldest; most widely used; maintained by Ethereum Foundation |
| Nethermind | C# | Second most widely used |
| Besu | Java | Enterprise-grade; Hyperledger project |
| Erigon | Go | Optimized for archive storage; ~2 TB for archive vs ~21 TB for standard |
| Reth | Rust | Newer; created by Paradigm after Parity/OpenEthereum was discontinued |

[^src1]

## Consensus Clients (as of June 2025)

| Client | Language | Notes |
|---|---|---|
| Lighthouse | Rust | Most-used consensus client; maintained by Sigma Prime |
| Prysm | Go | First consensus client; now maintained by Offchain Labs |
| Teku | Java | Enterprise; Consensys project |
| Nimbus | Nim | Lightweight; designed for low-resource environments |
| Lodestar | TypeScript | JavaScript ecosystem; useful for browser/tooling integration |

[^src1]

## Node Types

**Full node** — downloads the current blockchain, discards historical state and receipts (the default). As of June 2025, requires ≥2 TB storage [^src1].

**Archive node** — keeps all historical state and receipts indefinitely. Required for queries against old state (e.g., "what was account X's balance at block N?"). Erigon and Reth archive nodes need ~2 TB; standard archive nodes can exceed 21 TB [^src1].

**Light client / remote client** — does not store or validate locally; relies on a full node for state. MetaMask and similar wallet extensions are remote clients. Sufficient for normal users and developers; insufficient for running validators or indexers.

## Client Diversity as Security

Ethereum has a greater diversity of implementations running on the network than any other blockchain, which is generally regarded as a security property [^src1]. If a bug exists in one client's implementation, other clients keep the network running; exploitation of a particular client simply hassles those developers while they patch, while other clients are unaffected.

The Ethereum community tracks client distribution and actively discourages any single client from exceeding ~33% of validators (at which point a client bug could cause finality failure).

## Formal Specification

Unlike Bitcoin, which is specified by its reference implementation (Bitcoin Core), Ethereum is defined by a formal mathematical specification — the **Yellow Paper** — originally written by Gavin Wood [^src1]. Reference implementations in Python exist for both execution and consensus layers. All production clients are built against this spec plus Ethereum Improvement Proposals (EIPs).

## Running a Node

Running a full node requires [^src1]:
- ≥2 TB fast SSD (NVMe recommended).
- Reliable broadband (the node downloads and propagates blocks continuously).
- Choosing an execution client + consensus client pair (e.g., Geth + Lighthouse, Reth + Lighthouse).
- Syncing can take days to weeks on first startup.

For development, alternatives exist: testnets, local devnets (Anvil, Hardhat), or hosted node APIs (Infura, Alchemy).

## Cross-links

- [Ethereum](/blockchain/ethereum.md) — the platform these nodes implement.
- [Ethereum Consensus](/blockchain/ethereum-consensus.md) — Gasper; what the consensus client implements.
- [Ethereum Virtual Machine](/blockchain/ethereum-virtual-machine.md) — what the execution client runs.
- [P2P Networking](/blockchain/p2p-networking.md) — underlying gossip network nodes communicate over.

[^src1]: [Mastering Ethereum — Chapter 3. Ethereum Nodes](../../raw/_inbox/book-mastering-ethereum-11-chapter-3-ethereum-nodes.md)

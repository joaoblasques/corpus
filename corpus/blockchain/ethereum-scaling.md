---
type: concept
domain: blockchain
status: draft
sources:
  - path: raw/_inbox/book-mastering-ethereum-08-chapter-16-scaling-ethereum.md
    channel: book
    ingested_at: 2026-07-08
aliases:
  - L2 rollups
  - Layer 2
  - optimistic rollup
  - ZK rollup
  - zkEVM
  - EIP-4844
  - proto-danksharding
  - danksharding
  - Ethereum scalability
  - scalability trilemma
tags:
  - corpus/blockchain
  - concept
created: 2026-07-08
updated: 2026-07-08
---

# Ethereum Scaling

TL;DR: Ethereum's L1 handles ~15 transactions/second; L2 rollups push computation off-chain and post proofs or data summaries to L1, inheriting L1 security while achieving 10-100x throughput gains. EIP-4844 (Cancun, March 2024) introduced blob transactions that cut L2 data costs ~10x. The long-term roadmap is danksharding — massive parallel blob capacity.

## The Scalability Trilemma

Vitalik Buterin's scalability trilemma states that a blockchain can optimize at most two of three properties simultaneously [^src1]:

**Decentralization** — anyone can run a node and validate.

**Security** — resistant to attacks; transactions irreversible; smart contracts immutable.

**Scalability** — high throughput (TPS) suitable for global adoption.

Ethereum prioritizes decentralization and security; scalability is addressed through L2s rather than L1 expansion [^src1]. (Solana takes the opposite tradeoff: high throughput at the cost of higher validator hardware requirements and reduced decentralization.)

## L1 Bottlenecks

Ethereum's L1 constraints [^src1]:
- ~15M gas target per block (~15 TPS for simple transfers, fewer for complex DeFi operations).
- 30M gas hard cap per block.
- Block time: 12 seconds.
- State growth: full node requires ≥2 TB storage (2025).
- MEV: block proposers can reorder transactions for profit, degrading UX.

## Layer 2 Architecture

L2 rollups move execution off-chain while posting transaction data (or proofs) to L1 [^src1]:

1. Users submit transactions to an L2 sequencer.
2. The sequencer batches many transactions together.
3. The batch (data + proof/assertions) is posted to Ethereum L1.
4. L1 provides data availability and security guarantees for the batch.

"Ethereum essentially becomes a settlement layer, meaning its main role shifts toward verifying proofs, ensuring data availability, and providing ultimate security guarantees for L2 transactions" [^src1].

## Optimistic Rollups

**Assume valid, challenge if wrong.** Transaction results are posted to L1 as valid by default. A dispute period (7 days) allows anyone to submit a fraud proof if they detect invalid state transitions [^src1].

| Project | Notes |
|---|---|
| Optimism (OP Stack) | First major optimistic rollup; powers Base, Zora, and many L2s |
| Arbitrum (Nitro) | Largest optimistic rollup by TVL; uses interactive fraud proofs |
| Base | Coinbase's L2, built on OP Stack |

**Withdrawal latency**: 7-day challenge window before L1 withdrawals finalize (bridging services provide liquidity to skip the wait) [^src1].

**Advantage**: EVM-equivalent; easy to port existing Solidity contracts.

## ZK Rollups (Zero-Knowledge Rollups)

**Prove correctness with cryptography.** The sequencer generates a validity proof (SNARK or STARK) that the state transition was computed correctly. L1 verifies the proof on-chain; no challenge period needed [^src1].

| Project | Proof System | EVM Compatibility |
|---|---|---|
| zkSync Era | PLONK-based (Boojum) | zkEVM (type 2) |
| StarkNet | STARK (Cairo VM) | Custom VM (EVM via transpilation) |
| Scroll | SNARK-based zkEVM | zkEVM (type 2) |
| Linea | SNARK-based | zkEVM |
| Polygon zkEVM | SNARK-based | zkEVM (type 2) |

**Withdrawal latency**: near-instant after proof verification (~hours to verify, not 7 days) [^src1].

**Disadvantage**: proof generation is computationally expensive; ZK-EVM development is complex.

## zkEVM: Proving EVM Execution

A zkEVM generates a validity proof that an EVM execution trace is correct. Different zkEVM types [^src1]:

| Type | Description | Speed |
|---|---|---|
| Type 1 | Fully EVM-equivalent (byte-for-byte identical) | Slowest proving |
| Type 2 | EVM-equivalent at Solidity level; may differ in internal opcode behavior | Slower |
| Type 3 | Mostly EVM-compatible; some opcodes emulated | Medium |
| Type 4 | High-level language transpiled (e.g., Solidity → Zinc) | Fastest |

## EIP-4844 (Proto-Danksharding, Cancun 2024)

EIP-4844 was the most impactful near-term scaling upgrade [^src1]:

- Introduced **blob transactions** (type 0x03) carrying up to 6 large data blobs (~128 KB each).
- Blobs are stored by consensus nodes for ~18 days (not by execution nodes or L1 state).
- Only the KZG commitment hash is permanently stored on L1.
- Blob fee market is separate from normal gas (avoids competing with regular transactions).
- Result: L2 data publication costs dropped ~10x immediately on Cancun activation.

## Danksharding (Future)

Full danksharding is Ethereum's long-term data availability solution [^src1]:
- Target: 64–256 blobs per block (vs. 6 today).
- Uses **Data Availability Sampling (DAS)** — each node only downloads a random sample of each blob, using erasure coding to verify availability without downloading everything.
- Enables light nodes to verify data availability without full downloads.
- Requires: EIP-4844 (DONE), PeerDAS (in progress), Full Danksharding (future roadmap).

With full danksharding, L2 data availability cost approaches zero, potentially enabling thousands of TPS across the rollup ecosystem.

## State Growth and Statelessness

Ethereum's state (all account balances, contract storage) grows indefinitely [^src1]. A full node must store all state (~2 TB in 2025). Long-term solutions:

**Verkle trees** — replace Merkle Patricia Tries with more compact proofs, enabling stateless clients to verify blocks without storing full state.

**EIP-4444** — prune historical block data from full nodes; require archive nodes or external services for old data.

**Stateless clients** — a client that can validate blocks using only the block itself and a *witness* (proof of the relevant state) without storing state at all.

## State Channels (Niche)

State channels allow two parties to conduct many off-chain interactions, settling only the final state on-chain [^src1]. Used primarily in the Lightning Network (Bitcoin) and the Ethereum equivalent Raiden. Limited to bilateral or known-party interactions; not general-purpose like rollups.

## Cross-links

- [Ethereum](/blockchain/ethereum.md) — L1 platform being scaled.
- [Ethereum Virtual Machine](/blockchain/ethereum-virtual-machine.md) — zkEVMs prove EVM execution.
- [Zero-Knowledge Proofs](/blockchain/zero-knowledge-proofs.md) — SNARKs/STARKs power ZK rollup validity proofs.
- [Ethereum Transactions](/blockchain/ethereum-transactions.md) — EIP-4844 blob transactions.
- [Ethereum Consensus](/blockchain/ethereum-consensus.md) — PoS finality speeds up L2 settlement.
- [DeFi](/blockchain/defi.md) — primary beneficiary of L2 scaling (lower fees).

[^src1]: [Mastering Ethereum — Chapter 16. Scaling Ethereum](../../raw/_inbox/book-mastering-ethereum-08-chapter-16-scaling-ethereum.md)

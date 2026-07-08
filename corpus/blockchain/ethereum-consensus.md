---
type: concept
domain: blockchain
status: draft
sources:
  - path: raw/_inbox/book-mastering-ethereum-07-chapter-15-consensus.md
    channel: book
    ingested_at: 2026-07-08
aliases:
  - Gasper
  - Casper FFG
  - LMD-GHOST
  - proof of stake Ethereum
  - PoS Ethereum
  - The Merge
  - Ethereum validator
  - finality Ethereum
tags:
  - corpus/blockchain
  - concept
created: 2026-07-08
updated: 2026-07-08
---

# Ethereum Consensus (Gasper / PoS)

TL;DR: Ethereum's consensus protocol is **Gasper**, a combination of LMD-GHOST (fork choice) and Casper FFG (finality). It replaced proof-of-work via The Merge on September 15, 2022. Validators stake 32 ETH; randomly selected proposers create blocks; committees of attestors vote on the canonical chain. Finality is achieved in ~12 minutes (two epochs); slashing punishes equivocation.

## Background: The Merge

On September 15, 2022, Ethereum completed "The Merge" hard fork, transitioning from proof-of-work (Ethash) to proof-of-stake (Gasper) [^src1]. Energy consumption dropped ~99.95%. The Merge was a technical milestone of replacing the consensus layer of a live network with hundreds of billions of dollars of value at stake.

## Consensus Fundamentals

Three key properties of a consensus mechanism [^src1]:

**Safety** — the network consistently agrees on the same blockchain state; no double-spends or conflicting transaction histories. Every node has an identical view of chain history.

**Liveness** — the network continues to process transactions and add new blocks. Valid transactions submitted to honest nodes will eventually be included in a block.

**Finality** — the point at which a block is considered irreversible. Ethereum favors liveness over safety under network partition: the chain continues producing blocks even if finality stalls. Finalized blocks are cryptographically irreversible [^src1].

"Designing a consensus protocol that is both safe and live under all circumstances is not possible — you have to favor one of the two" [^src1]. Ethereum's Gasper prioritizes liveness.

## Proof of Stake Mechanics

**Validators** — participants who lock up (stake) exactly 32 ETH as collateral to participate in consensus. As of 2025, Ethereum has over 1 million active validators [^src1].

**Staking** — locking ETH in the deposit contract to become a validator. Staked ETH is illiquid (locked) until the validator exits and the unstake process completes.

**Slots and Epochs**:
- A **slot** is 12 seconds; each slot has one potential block proposer.
- An **epoch** consists of 32 slots (6.4 minutes).
- Committees are reshuffled every epoch [^src1].

## Gasper: LMD-GHOST + Casper FFG

Gasper is composed of two complementary protocols [^src1]:

### LMD-GHOST (Fork Choice)

Latest Message Driven GHOST (Greediest Heaviest Observed SubTree). When there are multiple candidate chain heads (forks), each validator's most recent vote (attestation) is counted once. The chain head is the block with the most accumulated validator weight — not the longest chain (unlike Bitcoin's longest-chain rule).

GHOST is resistant to short-range selfish mining attacks that were possible with the longest-chain rule [^src1].

### Casper FFG (Finality)

Casper the Friendly Finality Gadget provides finality on top of LMD-GHOST. A block achieves finality in two phases [^src1]:

1. **Justification** — a checkpoint (the first block of an epoch) is justified when 2/3 of staked ETH attests to it.
2. **Finalization** — when two consecutive checkpoints are justified, the earlier one is finalized and can never be reverted without burning at least 1/3 of staked ETH.

Finality takes approximately 2 epochs (~12.8 minutes) under normal conditions [^src1].

## Block Proposal and Attestation

**Proposer selection** — a pseudorandom algorithm (RANDAO + VDF) selects one validator per slot to propose a block. The proposer collects transactions from the mempool, executes them (via the execution client), and broadcasts the block [^src1].

**Attestation** — validators not proposing a block are assigned to committees and attest (vote) on:
1. The head of the chain (LMD-GHOST vote).
2. A checkpoint pair (Casper FFG vote).

Attestations are aggregated and included in blocks [^src1].

## Slashing

Slashing is the economic penalty for validator misbehavior [^src1]:

| Violation | Description | Penalty |
|---|---|---|
| Double voting (equivocation) | Signing two different blocks for the same slot | Partial ETH burn + ejection |
| Surround voting | Voting for contradictory checkpoint pairs | Partial ETH burn + ejection |

The slashing penalty scales with the number of simultaneously slashed validators — if many validators get slashed together (coordinated attack), the penalty approaches 100% of stake.

Slashed validators are immediately ejected from the validator set. Whistleblowers who report slashable evidence receive a reward [^src1].

## Inactivity Leak

If the network fails to finalize for ~4 epochs (33 minutes), an *inactivity leak* activates: inactive validators' stakes decay until the active set has enough stake to finalize again. This mechanism restores liveness even if up to 1/3 of validators go offline [^src1].

## MEV (Maximal Extractable Value)

Validators (block proposers) can reorder, insert, or censor transactions within their proposed block to extract value — MEV [^src1]. The MEV-boost ecosystem (Flashbots) separates block building from proposing via Proposer-Builder Separation (PBS), partially decentralizing MEV extraction.

## Validator Economics

Validators earn rewards for [^src1]:
- Proposing blocks (occasional but larger reward).
- Attesting correctly and on time (frequent, smaller rewards).
- Sync committee participation (rare committee elected every 256 epochs).

Penalty for being offline: approximately equal in magnitude to the attestation reward (symmetric — you earn nothing for being offline, but you lose the reward you would have earned).

## Liquid Staking

Most users cannot run a validator independently (32 ETH minimum, ~$80K+; 24/7 uptime; technical complexity). Liquid staking protocols (Lido, Rocket Pool) pool ETH and issue a liquid derivative token (stETH, rETH) representing staked ETH + accrued rewards [^src1].

Lido controls ~30% of staked ETH (as of 2025), creating centralization risk. The Ethereum community debates this concentration [^src1].

## Cross-links

- [Ethereum](/blockchain/ethereum.md) — The Merge context and Ethereum overview.
- [Ethereum Nodes](/blockchain/ethereum-nodes.md) — consensus clients implement Gasper.
- [Proof of Work](/blockchain/proof-of-work.md) — Ethereum's previous consensus mechanism (Ethash).
- [Ethereum Scaling](/blockchain/ethereum-scaling.md) — PoS enables faster finality important for rollup settlements.
- [Smart Contract Security](/blockchain/smart-contract-security.md) — MEV is an economic attack vector.

[^src1]: [Mastering Ethereum — Chapter 15. Consensus](../../raw/_inbox/book-mastering-ethereum-07-chapter-15-consensus.md)

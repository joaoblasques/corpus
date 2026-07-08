---
type: concept
domain: blockchain
status: draft
sources:
  - path: raw/notes/notes-cambrian-explosion-of-crypto-proofs-scrape.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/_inbox/book-mastering-ethereum-09-chapter-17-zero-knowledge-proofs.md
    channel: book
    ingested_at: 2026-07-08
aliases:
  - ZKP
  - zero knowledge proof
  - SNARKs
  - STARKs
  - STARK
  - SNARK
  - Groth16
  - PLONK
  - cryptographic proof systems
  - computational integrity
tags:
  - corpus/blockchain
  - concept
created: 2026-06-17
updated: 2026-07-08
---

# Zero-Knowledge Proofs & Proof Systems

TL;DR: Cryptographic proof systems let a prover convince a verifier that a computation was done correctly, without revealing the inputs. The field exploded from 1–3 new systems per year to multiple per week (2019). All share two fundamentals: arithmetization and low-degree compliance. The key tradeoff: asymmetric (SNARK) gives short proofs; symmetric (STARK) gives post-quantum security and no trusted setup. Author recommendation: Groth16/PLONK for short proofs, STARKs for everything else.

## What cryptographic proof systems are

A **computational integrity (CI) system** lets a prover demonstrate that a computation over public or private inputs produced a specific output — without the verifier re-running the computation. When inputs are private, this is a zero-knowledge proof [^src1].

Applications in blockchain: Zcash privacy, zkRollups (Ethereum scaling), StarkWare's STARK-based validity proofs, and more.

## The Cambrian Explosion

The field went from 1–3 new proof systems per year to multiple per month/week starting around 2019. Notable 2019 systems: Libra, Sonic, PLONK, Halo, Marlin, Fractal, Spartan [^src1].

Source: Eli Ben-Sasson, co-founder of StarkWare.

## Two universal building blocks

All CI systems share exactly two fundamental components [^src1]:

### 1. Arithmetization

Convert the computation into bounded-degree polynomial constraints. Common representations:
- **R1CS** (Rank-1 Constraint System): most common — used by Groth16, PLONK
- **AIR** (Algebraic Intermediate Representation): used by STARKs

### 2. Low-degree compliance (LDC)

Cryptographically enforce that the prover's polynomials are actually low-degree — i.e., that the prover isn't cheating by using a high-degree polynomial that passes spot-checks.

Two approaches:

| Approach | Mechanism | Properties |
|---|---|---|
| **Hiding queries** | Homomorphic encryption: queries are hidden from prover | Short proofs (Groth16 <200 bytes); requires trusted setup; asymmetric assumptions |
| **Commitment schemes** | Prover commits to polynomials upfront (Merkle tree-based) | Larger proofs (dozens of KB); no trusted setup; symmetric assumptions; post-quantum |

## Cryptographic assumption tradeoffs

| | Symmetric primitives | Asymmetric primitives |
|---|---|---|
| Examples | SHA-2, Keccak, Blake | Discrete log, RSA, elliptic curves |
| Field arithmetic | Smaller | Larger |
| Post-quantum security | Plausible (Lindy Effect) | Broken by Shor's algorithm |
| Proof size | Large (dozens of KB) | Small (Groth16: <200 bytes) |

The "Lindy Effect" here: symmetric primitives have been battle-tested much longer than ECC/discrete-log-based systems [^src1].

## SNARKs vs. STARKs

| | SNARK | STARK |
|---|---|---|
| Stands for | Succinct Non-interactive ARgument of Knowledge | Scalable Transparent ARgument of Knowledge |
| Trusted setup | Required (for most variants) | None (transparent) |
| Proof size | Very small | Larger |
| Prover time | Varies | Quasi-linear |
| Verifier time | Constant | Poly-logarithmic |
| Post-quantum | No (asymmetric assumptions) | Yes (symmetric assumptions) |
| Examples | Groth16, PLONK, Halo | FRI-based STARKs (StarkWare) |

"Transparent" means the setup parameters are publicly generated with no secret randomness — no trusted party required [^src1].

## Practical recommendation (Ben-Sasson, StarkWare)

- **Groth16 / PLONK SNARKs**: use when proof size is the constraint (e.g., on-chain verification costs)
- **Symmetric STARKs**: use for scalability, post-quantum security, and transparency (no trusted setup) [^src1]

## ZK Proofs in Ethereum

This section covers ZK proof applications specific to Ethereum, sourced from Chapter 17 of Mastering Ethereum [^src2].

### Why Ethereum Needs ZK Proofs

The EVM is a state transition function: every new block applies transactions to produce a new state. Today, every full node re-executes all transactions in every block to trustlessly verify the new state. This approach creates a hardware/decentralization tradeoff: higher throughput requires stronger hardware, which pushes toward centralization [^src2].

ZK proofs break this tradeoff: a small set of powerful provers can execute transactions and generate a proof; all other nodes verify the proof (much cheaper) and update state trustlessly [^src2].

### ZK Rollups

ZK rollups post aggregated proofs to Ethereum L1 once per batch (roughly hourly). The L1 verifies the ZK proof before accepting the new state root. This means [^src2]:
- L2 transactions are final when the proof is verified on L1.
- Time to finality = posting interval (avg ~30 min for current rollups).
- L1 does not need to re-execute L2 transactions — just verify the proof.

**zkSync Era** and **Starknet** are the leading ZK rollups:
- zkSync Era uses Groth16 and PLONK proofs; is EVM-compatible.
- Starknet uses zk-STARKs (Cairo VM); requires transpiling or rewriting contracts in Cairo.

### zkEVM

A zkEVM is a circuit proving EVM execution. It produces a validity proof that a specific EVM state transition (given the transactions and prior state) was computed correctly, without re-executing [^src2].

Challenges: EVM was not designed with ZK proving in mind; some opcodes are expensive to circuit-encode. As of 2025, zkEVMs are live but proof generation time is a known bottleneck.

### ZK Proof Systems Used in Ethereum

| System | Used By | Properties |
|---|---|---|
| Groth16 | zkSync, Tornado Cash | Shortest proofs (<200 bytes); trusted setup; fast verify |
| PLONK | Many L2s | Universal trusted setup; flexible; efficient |
| zk-STARKs | Starknet | No trusted setup; post-quantum; larger proofs |

**Trusted setup** — for Groth16 and early PLONK, a multi-party ceremony generates public parameters. If any participant in the ceremony is honest (destroys their secret), the system is secure. PLONK (2019) introduced *universal and updatable* trusted setups [^src2].

**Post-quantum security** — STARKs rely only on collision-resistant hash functions (symmetric cryptography), which quantum computers cannot efficiently attack. SNARKs rely on elliptic curve discrete logarithm, which Shor's algorithm breaks [^src1].

### Groth16 Timeline

Introduced in 2016, Groth16 "significantly improved the efficiency of zk-SNARKs by reducing proof size and verification time. Because of its exceptional succinctness, Groth16 remains widely used today, despite the availability of newer systems" [^src2].

### zk-SNARK vs. zk-STARK in Ethereum Context

| Dimension | zk-SNARK (Groth16/PLONK) | zk-STARK |
|---|---|---|
| Proof size | Very small (200 bytes – few KB) | Large (100s of KB) |
| On-chain verification cost | Low | Higher (larger calldata) |
| Trusted setup | Required (Groth16) / Universal (PLONK) | None (transparent) |
| Post-quantum | No | Yes |
| L2 examples | zkSync Era | Starknet |

## Related Pages

- [Hash Functions](/blockchain/hash-functions.md) — symmetric primitives (SHA-2) underpin STARKs and commitment schemes
- [Merkle Trees](/blockchain/merkle-trees.md) — Merkle-tree-based commitment schemes are the primary LDC method for STARKs
- [Public-Key Cryptography](/blockchain/public-key-cryptography.md) — asymmetric assumptions (ECC, discrete log) underpin SNARKs
- [Ethereum Scaling](/blockchain/ethereum-scaling.md) — ZK rollups are the primary scaling path
- [Ethereum Virtual Machine](/blockchain/ethereum-virtual-machine.md) — the zkEVM proves EVM execution

[^src1]: [A Cambrian Explosion of Crypto Proofs](../../raw/notes/notes-cambrian-explosion-of-crypto-proofs-scrape.md)
[^src2]: [Mastering Ethereum — Chapter 17. Zero-Knowledge Proofs](../../raw/_inbox/book-mastering-ethereum-09-chapter-17-zero-knowledge-proofs.md)

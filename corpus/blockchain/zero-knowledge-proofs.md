---
type: concept
domain: blockchain
status: draft
sources:
  - path: raw/notes/notes-cambrian-explosion-of-crypto-proofs-scrape.md
    channel: notes
    ingested_at: 2026-06-17
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
updated: 2026-06-17
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

## Related pages

- [[blockchain/hash-functions|Hash Functions]] — symmetric primitives (SHA-2) underpin STARKs and commitment schemes
- [[blockchain/merkle-trees|Merkle Trees]] — Merkle-tree-based commitment schemes are the primary LDC method for STARKs
- [[blockchain/public-key-cryptography|Public-Key Cryptography]] — asymmetric assumptions (ECC, discrete log) underpin SNARKs

[^src1]: [A Cambrian Explosion of Crypto Proofs](../../raw/notes/notes-cambrian-explosion-of-crypto-proofs-scrape.md)

---
type: concept
domain: blockchain
status: draft
sources:
  - path: raw/notes/notes-hash-functions-scrape.md
    channel: notes
    ingested_at: 2026-06-17
aliases:
  - SHA-256
  - cryptographic hash
  - SHA-2
  - hash function
tags:
  - corpus/blockchain
  - concept
created: 2026-06-17
updated: 2026-06-17
---

# Hash Functions

TL;DR: A cryptographic hash function deterministically maps arbitrary-size inputs to a fixed-size output. Called "a fingerprinting machine" — any input produces a unique fingerprint, any change to the input produces a completely different fingerprint. SHA-256 is the hash function powering Bitcoin; MD5 and SHA-1 are broken.

## What a hash function is

A hash function takes any input (a byte, a file, a novel) and produces a fixed-size output digest — always the same size regardless of input length [^src1].

Properties of a basic hash function:
- **Deterministic**: same input always produces same output
- **Fixed output size**: SHA-256 always produces 256-bit digests
- **Uniform distribution**: outputs are evenly spread across the output space

## Cryptographic requirements (beyond basic)

To be useful in security contexts, a hash function must also be:

| Property | Definition |
|---|---|
| **One-way** (preimage resistance) | Infeasible to reverse: given digest `d`, cannot find input `x` such that `H(x) = d` |
| **Avalanche effect** | A single bit change in input causes ~half the output bits to flip |
| **Collision-resistance** | Infeasible to find two different inputs that produce the same output |

The avalanche effect is what makes Merkle trees work: any change to a leaf propagates all the way up the tree [^src1].

## Output space and security

SHA-256 produces 2^256 possible outputs. The practical security threshold is 128 bits — requiring roughly 2^128 operations to break by brute force [^src1]. This is computationally infeasible with any foreseeable classical computing.

## Birthday attack

A collision attack exploits the birthday paradox: in a group of 23 people, there's a >50% chance two share a birthday, despite 365 possibilities. Applied to hash functions:

- Brute-force collision search: O(n) where n = output space
- Birthday attack: finds collisions in O(√n) time — much faster

For SHA-256 (2^256 outputs), birthday attack requires ~2^128 operations — still infeasible. For MD5 (128-bit output), it required ~2^64 operations — feasible, and exploited [^src1].

## Status of common algorithms

| Algorithm | Status | Notes |
|---|---|---|
| MD5 | **Broken** | Collisions found; do not use for security |
| SHA-1 | **Broken** | Collision demonstrated via SHAttered attack |
| SHA-2 (SHA-256) | Secure | Powers Bitcoin; 128-bit effective security |
| SHA-3 | Secure | Different internal design; NIST-standardized alternative |

## Bitcoin usage

Bitcoin uses SHA-256 in multiple contexts:
- Mining (proof-of-work): find nonce such that `SHA-256(SHA-256(block_header))` meets difficulty target
- Address derivation: `RIPEMD160(SHA-256(pub_key))`
- Transaction hashing: txids are SHA-256 double-hashes

## Related pages

- [Merkle Trees](/blockchain/merkle-trees.md) — built from pairwise hash operations; relies on avalanche effect
- [Proof-of-Work](/blockchain/proof-of-work.md) — PoW mining is a hash-finding exercise
- [Public-Key Cryptography](/blockchain/public-key-cryptography.md) — address derivation combines SHA-256 and RIPEMD160

[^src1]: [Hash Functions](../../raw/notes/notes-hash-functions-scrape.md)

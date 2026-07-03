---
type: concept
domain: blockchain
status: draft
sources:
  - path: raw/notes/notes-merkle-trees-scrape.md
    channel: notes
    ingested_at: 2026-06-17
aliases:
  - Merkle tree
  - Merkle root
  - Merkle proof
  - inclusion proof
  - SPV
  - simplified payment verification
tags:
  - corpus/blockchain
  - concept
created: 2026-06-17
updated: 2026-06-17
---

# Merkle Trees

TL;DR: A cryptographic data structure that compresses arbitrary amounts of data into a single hash (the Merkle root). Enables O(log n) inclusion proofs — proving a piece of data belongs to a set without transmitting the full set. Bitcoin uses Merkle trees in block headers to enable lightweight clients (SPV nodes) to verify transactions without downloading full blocks.

## Construction

1. Hash each data block individually: `H(block_i)`
2. Pair adjacent hashes and hash the pair: `H(H(block_1) || H(block_2))`
3. Repeat up the tree until a single **Merkle root** remains

Any single bit change in any data block propagates to the root via the hash avalanche effect [^src1]. This makes the Merkle root a compact cryptographic commitment to the entire dataset.

```
               [Merkle Root]
              /             \
        [Hash AB]         [Hash CD]
        /      \           /      \
   [Hash A]  [Hash B]  [Hash C]  [Hash D]
      |          |         |         |
   Block A    Block B   Block C   Block D
```

## The problem Merkle trees solve

For a 2GB dataset you could either:
- Store a **single hash** of the whole thing — can verify integrity but can't identify which block changed
- Store **N hashes** (one per block) — can identify the bad block, but must transmit all N hashes

Merkle trees give you a third option: one root hash, but O(log n) sibling hashes per block to prove any individual block's membership [^src1].

## Merkle proofs (inclusion proofs)

To prove that block `X` is in the dataset, you need only:
- The block itself
- O(log n) "sibling" hashes along the path from the block to the root

The verifier recomputes the root from block + siblings and checks it matches the trusted root. No other blocks need to be transmitted [^src1].

Example: in a tree of 1 million blocks, proving inclusion requires ~20 sibling hashes (log₂(1,000,000) ≈ 20).

## Bitcoin application: SPV light clients

Bitcoin block headers include only the **Merkle root** of all transactions — not the transactions themselves. This enables:

- **Full nodes**: download and verify all transactions
- **SPV (Simplified Payment Verification) nodes**: download only block headers + request Merkle proofs for specific transactions

Mobile Bitcoin wallets are SPV clients. They can verify a transaction was included in a block using only O(log n) hashes, without downloading the entire blockchain [^src1].

## Related pages

- [Hash Functions](/blockchain/hash-functions.md) — the avalanche effect that makes Merkle trees work
- [Bitcoin](/blockchain/bitcoin.md) — block headers contain the Merkle root of transactions
- [Public-Key Cryptography](/blockchain/public-key-cryptography.md) — RIPEMD160(SHA-256(pub_key)) is another hash-based commitment scheme

[^src1]: [Merkle Trees](../../raw/notes/notes-merkle-trees-scrape.md)

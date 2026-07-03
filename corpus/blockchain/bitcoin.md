---
type: entity
domain: blockchain
status: draft
sources:
  - path: raw/notes/notes-introduction-to-cryptocurrency-scrape.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-a-brief-history-of-money-scrape.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-satoshi-nakamoto-scrape.md
    channel: notes
    ingested_at: 2026-06-17
aliases:
  - BTC
  - Bitcoin network
  - cryptocurrency
tags:
  - corpus/blockchain
  - entity
created: 2026-06-17
updated: 2026-06-17
---

# Bitcoin

TL;DR: A decentralized, trustless digital currency launched by Satoshi Nakamoto in January 2009. Bitcoin synthesizes cryptographic proof-of-work, a P2P gossip network, public-key identity, and Merkle tree data structures to solve the problem of digital double-spend without a central authority.

## What Bitcoin is

Bitcoin is the first successful decentralized digital currency. It addresses the fundamental challenge of digital money — preventing double-spend — without relying on any trusted third party. Instead of a bank, it relies on cryptographic proof and economic incentives [^src1].

Since its 2009 launch, Bitcoin has spawned "a multi-hundred-billion-dollar industry" and spurred innovation across distributed systems, cryptography, and economics [^src1].

## Technical stack

Bitcoin combines five key technical layers:

| Layer | Mechanism | Corpus page |
|---|---|---|
| Identity | Public/private key pairs (secp256k1 ECC) | [Public-Key Cryptography](/blockchain/public-key-cryptography.md) |
| Data integrity | Merkle trees in block headers | [Merkle Trees](/blockchain/merkle-trees.md) |
| Consensus | Proof-of-work (Nakamoto Consensus) | [Proof-of-Work](/blockchain/proof-of-work.md) |
| Network | Gossip protocol over P2P overlay | [P2P Networking](/blockchain/p2p-networking.md) |
| Hash function | SHA-256 (double-hashed in many contexts) | [Hash Functions](/blockchain/hash-functions.md) |

## Key facts

- Genesis Block (January 2009): embedded 2009 Times headline about banking bailouts [^src2]
- First recorded price: $0.003/coin (2010) [^src2]
- First commercial transaction: 10,000 BTC for two pizzas (May 2010) [^src2]
- Satoshi's addresses: ~600,000–700,000 BTC, unmoved [^src3]
- Address format: `RIPEMD160(SHA2(pub_key))`

## Learning resources

The nakamoto.ghost.io course by Haseeb Qureshi (managing partner at Dragonfly Capital) provides a nine-module developer curriculum covering: History of Bitcoin, Cryptography 101, P2P Networking, Consensus, Cryptoeconomics, Decentralized Computation, Smart Contracts, Security, Scaling [^src1].

## Related pages

- [Satoshi Nakamoto](/blockchain/satoshi-nakamoto.md) — creator
- [History of Money](/blockchain/history-of-money.md) — what Bitcoin responds to
- [The Cypherpunks](/blockchain/the-cypherpunks.md) — ideological lineage
- [Proof-of-Work](/blockchain/proof-of-work.md) — consensus mechanism
- [P2P Networking](/blockchain/p2p-networking.md) — network layer

[^src1]: [Introduction to Cryptocurrency](../../raw/notes/notes-introduction-to-cryptocurrency-scrape.md)
[^src2]: [A Brief History of Money](../../raw/notes/notes-a-brief-history-of-money-scrape.md)
[^src3]: [Satoshi Nakamoto](../../raw/notes/notes-satoshi-nakamoto-scrape.md)

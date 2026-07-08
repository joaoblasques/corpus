---
type: source
domain: blockchain
status: mature
sources:
  - path: raw/_inbox/book-mastering-ethereum-01-chapter-1-what-is-ethereum.md
    channel: book
    ingested_at: 2026-07-08
  - path: raw/_inbox/book-mastering-ethereum-10-chapter-2-ethereum-basics.md
    channel: book
    ingested_at: 2026-07-08
  - path: raw/_inbox/book-mastering-ethereum-11-chapter-3-ethereum-nodes.md
    channel: book
    ingested_at: 2026-07-08
  - path: raw/_inbox/book-mastering-ethereum-12-chapter-4-cryptography.md
    channel: book
    ingested_at: 2026-07-08
  - path: raw/_inbox/book-mastering-ethereum-13-chapter-5-wallets.md
    channel: book
    ingested_at: 2026-07-08
  - path: raw/_inbox/book-mastering-ethereum-14-chapter-6-transactions.md
    channel: book
    ingested_at: 2026-07-08
  - path: raw/_inbox/book-mastering-ethereum-15-chapter-7-smart-contracts-and-solidity.md
    channel: book
    ingested_at: 2026-07-08
  - path: raw/_inbox/book-mastering-ethereum-16-chapter-8-smart-contracts-and-vyper.md
    channel: book
    ingested_at: 2026-07-08
  - path: raw/_inbox/book-mastering-ethereum-17-chapter-9-smart-contract-security.md
    channel: book
    ingested_at: 2026-07-08
  - path: raw/_inbox/book-mastering-ethereum-02-chapter-10-tokens.md
    channel: book
    ingested_at: 2026-07-08
  - path: raw/_inbox/book-mastering-ethereum-03-chapter-11-oracles.md
    channel: book
    ingested_at: 2026-07-08
  - path: raw/_inbox/book-mastering-ethereum-04-chapter-12-decentralized-applications.md
    channel: book
    ingested_at: 2026-07-08
  - path: raw/_inbox/book-mastering-ethereum-05-chapter-13-decentralized-finance.md
    channel: book
    ingested_at: 2026-07-08
  - path: raw/_inbox/book-mastering-ethereum-06-chapter-14-the-ethereum-virtual-machine.md
    channel: book
    ingested_at: 2026-07-08
  - path: raw/_inbox/book-mastering-ethereum-07-chapter-15-consensus.md
    channel: book
    ingested_at: 2026-07-08
  - path: raw/_inbox/book-mastering-ethereum-08-chapter-16-scaling-ethereum.md
    channel: book
    ingested_at: 2026-07-08
  - path: raw/_inbox/book-mastering-ethereum-09-chapter-17-zero-knowledge-proofs.md
    channel: book
    ingested_at: 2026-07-08
aliases:
  - Mastering Ethereum
  - Antonopoulos Ethereum book
  - ethereumbook
tags:
  - corpus/blockchain
  - source
created: 2026-07-08
updated: 2026-07-08
---

# Mastering Ethereum (Antonopoulos & Wood)

TL;DR: The definitive open-source reference for Ethereum, covering the full stack from cryptographic primitives to DeFi and ZK scaling. Published under CC BY-SA 4.0; actively maintained on GitHub. All 17 chapters ingested into the blockchain domain corpus on 2026-07-08.

## Bibliographic Details

**Title**: Mastering Ethereum: Building Smart Contracts and DApps  
**Authors**: Andreas M. Antonopoulos, Gavin Wood  
**License**: CC BY-SA 4.0  
**Repository**: https://github.com/ethereumbook/ethereumbook  
**Chapter count**: 17 chapters (all ingested)

## Chapter Inventory

| Chapter | Title | Corpus pages |
|---|---|---|
| 1 | What Is Ethereum? | [Ethereum](/blockchain/ethereum.md) |
| 2 | Ethereum Basics | [Ethereum](/blockchain/ethereum.md) |
| 3 | Ethereum Nodes | [Ethereum Nodes](/blockchain/ethereum-nodes.md) |
| 4 | Cryptography | [Public-Key Cryptography](/blockchain/public-key-cryptography.md) (Ethereum section) |
| 5 | Wallets | [Ethereum](/blockchain/ethereum.md) (wallet section) |
| 6 | Transactions | [Ethereum Transactions](/blockchain/ethereum-transactions.md) |
| 7 | Smart Contracts and Solidity | [Smart Contracts](/blockchain/smart-contracts.md) |
| 8 | Smart Contracts and Vyper | [Smart Contracts](/blockchain/smart-contracts.md) |
| 9 | Smart Contract Security | [Smart Contract Security](/blockchain/smart-contract-security.md) |
| 10 | Tokens | [Ethereum Tokens](/blockchain/ethereum-tokens.md) |
| 11 | Oracles | [Oracles](/blockchain/oracles.md) |
| 12 | Decentralized Applications | [Decentralized Applications](/blockchain/decentralized-applications.md) |
| 13 | Decentralized Finance | [DeFi](/blockchain/defi.md) |
| 14 | The Ethereum Virtual Machine | [Ethereum Virtual Machine](/blockchain/ethereum-virtual-machine.md) |
| 15 | Consensus | [Ethereum Consensus](/blockchain/ethereum-consensus.md) |
| 16 | Scaling Ethereum | [Ethereum Scaling](/blockchain/ethereum-scaling.md) |
| 17 | Zero-Knowledge Proofs | [Zero-Knowledge Proofs](/blockchain/zero-knowledge-proofs.md) |

## Coverage Notes

- Ch4 (Cryptography) covers the same ground as the existing [Public-Key Cryptography](/blockchain/public-key-cryptography.md) page (Bitcoin-focused). Ethereum-specific additions (secp256k1 key derivation to Ethereum addresses, Keccak-256 vs SHA-256, KZG commitments, validator BLS keys) should be cross-referenced there rather than creating a duplicate concept page.
- Ch5 (Wallets) material — HD wallets, BIP-32/39/44, mnemonic seed phrases — is summarized in the Ethereum entity page under the "Wallets" section.

---
type: source
domain: blockchain
status: draft
sources:
  - path: raw/pdf/book-mastering-bitcoin-3rd-edition-01-introduction.md
    channel: book
    ingested_at: 2026-07-07
  - path: raw/pdf/book-mastering-bitcoin-3rd-edition-02-how-bitcoin-works.md
    channel: book
    ingested_at: 2026-07-07
  - path: raw/pdf/book-mastering-bitcoin-3rd-edition-03-bitcoin-core-the-reference-implementatio.md
    channel: book
    ingested_at: 2026-07-07
  - path: raw/pdf/book-mastering-bitcoin-3rd-edition-04-keys-and-addresses.md
    channel: book
    ingested_at: 2026-07-07
  - path: raw/pdf/book-mastering-bitcoin-3rd-edition-05-wallet-recovery.md
    channel: book
    ingested_at: 2026-07-07
  - path: raw/pdf/book-mastering-bitcoin-3rd-edition-06-transactions.md
    channel: book
    ingested_at: 2026-07-07
  - path: raw/pdf/book-mastering-bitcoin-3rd-edition-07-authorization-and-authentication.md
    channel: book
    ingested_at: 2026-07-07
  - path: raw/pdf/book-mastering-bitcoin-3rd-edition-08-digital-signatures.md
    channel: book
    ingested_at: 2026-07-07
  - path: raw/pdf/book-mastering-bitcoin-3rd-edition-09-transaction-fees.md
    channel: book
    ingested_at: 2026-07-07
  - path: raw/pdf/book-mastering-bitcoin-3rd-edition-10-the-bitcoin-network.md
    channel: book
    ingested_at: 2026-07-07
  - path: raw/pdf/book-mastering-bitcoin-3rd-edition-11-the-blockchain.md
    channel: book
    ingested_at: 2026-07-07
  - path: raw/pdf/book-mastering-bitcoin-3rd-edition-12-mining-and-consensus.md
    channel: book
    ingested_at: 2026-07-07
  - path: raw/pdf/book-mastering-bitcoin-3rd-edition-13-bitcoin-security.md
    channel: book
    ingested_at: 2026-07-07
aliases:
  - Mastering Bitcoin
  - Mastering Bitcoin 3rd Edition
  - Antonopoulos Bitcoin book
tags:
  - corpus/blockchain
  - source
created: 2026-07-07
updated: 2026-07-07
---

# Mastering Bitcoin (3rd Edition) — Antonopoulos & Harding

TL;DR: The definitive technical reference for Bitcoin. Covers the full stack from cryptographic primitives (elliptic curves, hash functions, digital signatures) through transaction structure and Script, the P2P network protocol, blockchain data structure, mining consensus, and operational security. Open-source (CC BY-SA 4.0) on GitHub.

## Overview

Authors: Andreas M. Antonopoulos (Bitcoin educator and author) and David A. Harding (Bitcoin contributor, BIP co-author). Published 2023 (3rd edition). Source repository: https://github.com/bitcoinbook/bitcoinbook

The 3rd edition adds coverage of Taproot (Schnorr signatures, Tapscript, MAST), SegWit v1, and hardware signing device workflows (PSBT/BIP 174).

## Structure

| Chapter | Topic |
|---|---|
| 1 | Introduction: Bitcoin as distributed, peer-to-peer digital cash |
| 2 | How Bitcoin Works: transaction lifecycle, blockchain explorers |
| 3 | Bitcoin Core: reference implementation, full node, JSON-RPC API |
| 4 | Keys and Addresses: private keys, public keys, ECC, address formats |
| 5 | Wallet Recovery: HD wallets, BIP-32/39/44, seed phrases |
| 6 | Transactions: UTXO model, inputs/outputs, serialization, PSBT |
| 7 | Authorization & Authentication: Bitcoin Script, P2PKH, P2WPKH, Taproot |
| 8 | Digital Signatures: ECDSA, Schnorr, signature malleability |
| 9 | Transaction Fees: fee market, RBF, CPFP, mempool dynamics |
| 10 | The Bitcoin Network: P2P protocol, full nodes, SPV, Stratum |
| 11 | The Blockchain: block structure, headers, Merkle paths, forks |
| 12 | Mining and Consensus: PoW, difficulty adjustment, halvings, mempool |
| 13 | Bitcoin Security: key management, cold storage, hardware wallets |

## Key concepts introduced

- [Bitcoin Transactions](/blockchain/bitcoin-transactions.md) — UTXO model; inputs spend previous outputs; no intrinsic "accounts"
- [Bitcoin Script](/blockchain/bitcoin-script.md) — Forth-like stack language for authorization/authentication
- [Bitcoin Security](/blockchain/bitcoin-security.md) — decentralized security model; key custody as bearer asset

## Source provenance

All 13 chapters collected from the public GitHub repository (CC BY-SA 4.0). Each chapter is a separate source file in the inbox, collected 2026-07-06.

[^src1]: Mastering Bitcoin, 3rd Edition, Antonopoulos & Harding, CC BY-SA 4.0, https://github.com/bitcoinbook/bitcoinbook

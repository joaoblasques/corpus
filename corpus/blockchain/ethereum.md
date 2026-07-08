---
type: entity
domain: blockchain
status: draft
sources:
  - path: raw/_inbox/book-mastering-ethereum-01-chapter-1-what-is-ethereum.md
    channel: book
    ingested_at: 2026-07-08
  - path: raw/_inbox/book-mastering-ethereum-10-chapter-2-ethereum-basics.md
    channel: book
    ingested_at: 2026-07-08
  - path: raw/_inbox/book-mastering-ethereum-13-chapter-5-wallets.md
    channel: book
    ingested_at: 2026-07-08
aliases:
  - ETH
  - world computer
  - Ethereum platform
tags:
  - corpus/blockchain
  - entity
created: 2026-07-08
updated: 2026-07-08
---

# Ethereum

TL;DR: Ethereum is a globally decentralized, programmable blockchain — a "world computer" — that executes arbitrary code via smart contracts, uses ether (ETH) as its native utility currency, and transitioned from proof-of-work to proof-of-stake in September 2022 (The Merge).

## Definition

From a computer-science perspective, Ethereum is "a deterministic but practically unbounded state machine, consisting of a globally accessible singleton state and a virtual machine that applies changes to that state" [^src1]. In practical terms it is an open-source, globally decentralized computing infrastructure that executes programs called *smart contracts*, using a blockchain to synchronize state and *ether* to meter execution costs [^src1].

## Ethereum vs. Bitcoin

Bitcoin's Script language is intentionally constrained to simple true/false evaluation of spending conditions; Ethereum's language is *Turing complete*, meaning Ethereum can function as a general-purpose computer [^src1]. Where Bitcoin is primarily a digital-currency payment network, ether is intended as a *utility currency* to pay for use of the Ethereum world computer — not as a primary store of value [^src1].

Both share P2P networking, Byzantine fault-tolerant consensus, cryptographic primitives, and a native digital currency. Key differences:

| Dimension | Bitcoin | Ethereum |
|---|---|---|
| Language | Script (limited) | Turing-complete EVM |
| Purpose | Digital cash | Programmable world computer |
| Consensus (2026) | Proof of work | Proof of stake (post-Merge) |
| Accounts | UTXO model | Account/balance model |
| Smart contracts | Very limited | First-class |

See [Bitcoin](/blockchain/bitcoin.md) for the Bitcoin-specific page.

## History

Vitalik Buterin first described Ethereum in a whitepaper circulated in December 2013, proposing a Turing-complete, general-purpose blockchain [^src1]. Gavin Wood co-designed the protocol, wrote the Yellow Paper (the formal specification), and shifted the vision from "programmable money" to a general-purpose computing platform [^src1].

The first Ethereum block was mined on **July 30, 2015** [^src1].

Development stages:
- **Frontier** (2015) — genesis, minimal network for miners and developers.
- **Homestead** (March 2016) — stability improvements.
- **Metropolis** (October 2017) — developer tooling and privacy features.
- **Serenity / The Merge** (September 15, 2022) — transition from PoW (Ethash) to PoS (Gasper). Energy use dropped ~99.95%.

## Ether (ETH)

Ether is denominated in **wei** (1 ETH = 10^18 wei) [^src2]. Common sub-units:

| Name | Wei exponent |
|---|---|
| Wei | 1 |
| Shannon (Gwei) | 10^9 |
| Ether | 10^18 |

Ether is always represented internally as an unsigned integer in wei [^src2].

## Account Model

Ethereum has two types of accounts [^src1][^src2]:

**Externally Owned Accounts (EOAs)** — controlled by a private key; have no associated code; send transactions.

**Contract accounts** — controlled by their smart-contract code; have both code and persistent storage; triggered by transactions from EOAs.

Both types are identified by a 20-byte Ethereum address. EOA addresses are derived from the public-key portion of the keypair (secp256k1 elliptic curve, Keccak-256 hash of the public key, last 20 bytes). Contract addresses are derived from the deployer address and nonce at deployment time.

## Wallets

An Ethereum wallet is a software application that manages private keys, constructs transactions, and presents an account interface [^src2][^src3]. Critically, wallets hold *keys*, not ether — the ether balances live on the blockchain.

Two wallet architectures:

**Nondeterministic (JBOK)** — each key independently generated; each needs its own backup. Considered legacy.

**Hierarchical Deterministic (HD, BIP-32/BIP-44)** — all keys derived from a single root seed in a tree structure; one mnemonic backup recovers the entire wallet [^src3]. This is the industry standard.

Mnemonic seed phrases (BIP-39) encode the seed as 12–24 English words for human backup. Loss of seed = permanent loss of all derived keys and funds.

## Permissionless and Permissioned Blockchains

Ethereum is a *permissionless* blockchain — anyone can join, participate in consensus, and read/write data [^src1]. This contrasts with *permissioned* blockchains that restrict access to authorized participants.

## Cross-links

- [Smart Contracts](/blockchain/smart-contracts.md) — programs deployed on Ethereum.
- [Ethereum Transactions](/blockchain/ethereum-transactions.md) — the mechanism that triggers state changes.
- [Ethereum Virtual Machine](/blockchain/ethereum-virtual-machine.md) — the execution engine.
- [Ethereum Consensus](/blockchain/ethereum-consensus.md) — Gasper PoS protocol.
- [Ethereum Tokens](/blockchain/ethereum-tokens.md) — ERC-20, ERC-721 and other token standards.
- [Public-Key Cryptography](/blockchain/public-key-cryptography.md) — underlies EOA key pairs.
- [Bitcoin](/blockchain/bitcoin.md) — predecessor; Ethereum was designed to transcend Bitcoin's limitations.
- [Proof of Work](/blockchain/proof-of-work.md) — Ethereum's original consensus (Ethash), replaced by PoS.

[^src1]: [Mastering Ethereum — Chapter 1. What Is Ethereum?](../../raw/_inbox/book-mastering-ethereum-01-chapter-1-what-is-ethereum.md)
[^src2]: [Mastering Ethereum — Chapter 2. Ethereum Basics](../../raw/_inbox/book-mastering-ethereum-10-chapter-2-ethereum-basics.md)
[^src3]: [Mastering Ethereum — Chapter 5: Wallets](../../raw/_inbox/book-mastering-ethereum-13-chapter-5-wallets.md)

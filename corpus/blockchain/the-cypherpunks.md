---
type: concept
domain: blockchain
status: draft
sources:
  - path: raw/notes/notes-the-cypherpunks-scrape.md
    channel: notes
    ingested_at: 2026-06-17
aliases:
  - Cypherpunks
  - cypherpunk movement
  - crypto-libertarians
tags:
  - corpus/blockchain
  - concept
created: 2026-06-17
updated: 2026-06-23
---

# The Cypherpunks

TL;DR: A Bay Area computer science mailing list founded in 1992 that believed cryptography was the primary tool for preserving individual freedom online. They built the intellectual and technical foundation for Bitcoin through a series of failed digital cash experiments — each failure teaching the next what was missing.

## Origin

In 1992, three Bay Area computer scientists established a mailing list to discuss cryptography, mathematics, politics, and philosophy. Members became known as **cypherpunks** — a portmanteau of "cyberpunk" and "ciphers" [^src1].

Core thesis: the internet would become central to human freedom; governments would inevitably attempt to monitor and censor it; cryptography was the only viable defense [^src1].

## The crypto wars

Before the 1970s, strong encryption was classified as a munition and export-controlled — limited to military and intelligence agencies. The cypherpunks championed Diffie-Hellman, RSA, and PGP against these restrictions [^src1]. Adam Back embedded the RSA algorithm in his email signature as civil disobedience against export controls.

## The missing ingredient: digital money

Encryption alone proved insufficient for digital freedom. The cypherpunks recognized that a truly free digital economy required **digitally native money** independent of central bank control [^src1].

They built several attempts:

| System | Year | Creator | Mechanism | Failure mode |
|---|---|---|---|---|
| Chaumian eCash (DigiCash) | 1990 | David Chaum | Blind signatures; bank tracked serial numbers to prevent double-spend | Company went bankrupt 1998 — single point of failure |
| e-gold | 1996 | Various | Gold-backed digital currency | US government froze accounts 2008 on money laundering charges |
| b-money | 1998 | Wei Dai | Decentralized PoW-based currency | Vulnerable to sybil attacks |
| BitGold | 2005 | Nick Szabo | Decentralized PoW-based currency | Vulnerable to sybil attacks |

The pattern: centralized systems fail from shutdown; decentralized proposals fail from sybil attacks. The missing ingredient was a trustless decentralized **consensus mechanism** — which Bitcoin delivered in 2009.

## Cultural legacy

The cypherpunk motto "Cypherpunks write code" directly influenced Satoshi Nakamoto's approach — ship working code, not manifestos [^src1]. Satoshi cited b-money (Wei Dai) and BitGold (Nick Szabo) in the Bitcoin whitepaper.

## Related pages

- [Satoshi Nakamoto](/blockchain/satoshi-nakamoto.md) — **predecessor-of**: the cypherpunk movement (b-money, BitGold, Hashcash) that Satoshi synthesized into Bitcoin
- [Proof-of-Work](/blockchain/proof-of-work.md) — the consensus mechanism that finally solved the sybil attacks that defeated b-money and BitGold
- [History of Money](/blockchain/history-of-money.md) — broader context of money's evolution
- [Public-Key Cryptography](/blockchain/public-key-cryptography.md) — **uses**: the cryptographic tools (Diffie-Hellman, RSA, PGP) cypherpunks championed against export controls

[^src1]: [The Cypherpunks](../../raw/notes/notes-the-cypherpunks-scrape.md)

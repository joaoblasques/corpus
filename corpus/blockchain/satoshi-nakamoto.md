---
type: entity
domain: blockchain
status: draft
sources:
  - path: raw/notes/notes-satoshi-nakamoto-scrape.md
    channel: notes
    ingested_at: 2026-06-17
aliases:
  - Satoshi
  - Bitcoin creator
  - Nakamoto
tags:
  - corpus/blockchain
  - entity
created: 2026-06-17
updated: 2026-06-17
---

# Satoshi Nakamoto

TL;DR: The pseudonymous creator of Bitcoin. Identity unknown — possibly one person, possibly a group. Coded Bitcoin in C++ from 2007, published the whitepaper in 2008, launched the network in January 2009, and vanished in April 2011. Holds ~600,000–700,000 BTC, unmoved to this day.

## Identity

We don't know who Satoshi Nakamoto was [^src1]. A male profile was posted on the P2P Foundation, but this establishes nothing. Satoshi's pseudonymity was likely deliberate — founders of e-gold and Liberty Reserve were indicted for money-related activities, making anonymity a rational choice for someone building an alternative monetary system.

## Development timeline

| Date | Event |
|---|---|
| May 2007 | Began coding Bitcoin in C++ |
| Late 2008 | Privately contacted Hal Finney and Wei Dai for whitepaper feedback |
| Late 2008 | Whitepaper published to public cryptography mailing list — muted initial response |
| January 2009 | Bitcoin network launched |
| May 2010 | First commercial purchase: 10,000 BTC for two Papa John's pizzas |
| 2010 | Refused WikiLeaks Bitcoin donations: "Bitcoin is a small beta community in its infancy" |
| April 2011 | Handed control to Gavin Andresen and disappeared |

Satoshi's known addresses hold ~600,000–700,000 BTC, never moved [^src1].

## Principal innovation: Nakamoto Consensus

Bitcoin was not invented from scratch. Satoshi synthesized existing cypherpunk research [^src1]:

- **Ralph Merkle** → Merkle trees (data integrity)
- **Haber & Stornetta** → cryptographic timestamping
- **Adam Back** → Hashcash (proof-of-work)
- **Wei Dai** → b-money (decentralized PoW currency concept)

The principal innovation was **Nakamoto Consensus**: using proof-of-work as the mechanism for decentralized agreement — solving the sybil attack problem that defeated b-money and BitGold.

## Ideology

Satoshi was libertarian and distrustful of central banks and fiat currency. The Genesis Block embeds a 2009 Times headline about banking bailouts as an ideological statement. Core belief: "The root problem with conventional currency is all the trust that's required to make it work" [^src1].

## Related pages

- [Bitcoin](/blockchain/bitcoin.md) — the system Satoshi created
- [Proof-of-Work](/blockchain/proof-of-work.md) — Satoshi's core innovation
- [The Cypherpunks](/blockchain/the-cypherpunks.md) — the movement that preceded Bitcoin
- [History of Money](/blockchain/history-of-money.md) — the context that motivated Bitcoin

[^src1]: [Satoshi Nakamoto](../../raw/notes/notes-satoshi-nakamoto-scrape.md)

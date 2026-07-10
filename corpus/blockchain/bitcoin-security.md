---
type: concept
domain: blockchain
status: draft
sources:
  - path: raw/pdf/book-mastering-bitcoin-3rd-edition-13-bitcoin-security.md
    channel: book
    ingested_at: 2026-07-07
  - path: raw/pdf/book-mastering-bitcoin-3rd-edition-05-wallet-recovery.md
    channel: book
    ingested_at: 2026-07-07
aliases:
  - bitcoin security
  - key custody
  - cold storage
  - hardware wallet
  - HD wallet
  - BIP-32
  - BIP-39
tags:
  - corpus/blockchain
  - concept
created: 2026-07-07
updated: 2026-07-07
---

# Bitcoin Security

TL;DR: Bitcoin security is radically different from traditional financial security: possession of the private key IS possession of the funds. There is no fraud reversal, no customer service, and no recourse within the protocol. Security therefore focuses entirely on key custody — generating, storing, and recovering private keys.

## The bearer asset model

Traditional payment security: the payment network needs end-to-end encryption to protect the user's private identifier (card number) from being reused by attackers.

Bitcoin payment security: a transaction only authorizes a specific value to a specific recipient. No private information is transmitted; an eavesdropper cannot reuse a transaction. Bitcoin traffic needs no encryption — but the private key that signs transactions must be protected absolutely [^src1].

"Possession is ten-tenths of the law" in Bitcoin: whoever holds the key controls the funds. Lost key = lost funds, permanently, with no recovery path inside the protocol [^src1].

## Key custody tiers

| Tier | Storage | Use case | Risk |
|---|---|---|---|
| Hot wallet | Software on internet-connected device | Daily spending | Malware, theft |
| Cold storage | Keys generated/stored offline | Long-term savings | Physical loss/destruction |
| Hardware wallet | Dedicated signing device (Ledger, Trezor) | Balance of security/convenience | Firmware bugs, supply chain |
| Paper wallet | Private key printed on paper | Deep cold storage | Physical damage, loss |
| Multisig | m-of-n keys required | Institutional custody, inheritance | Coordination complexity |

## HD Wallets (BIP-32/39/44)

Hierarchical Deterministic (HD) wallets derive all keys from a single root seed:
- **BIP-39**: 12 or 24 mnemonic words encode the root entropy; human-memorizable backup
- **BIP-32**: defines the derivation tree (master private key → child keys)
- **BIP-44**: defines derivation paths by coin type and account (m/44'/0'/0'/...)

A single 12-word seed phrase recovers the entire wallet including all derived addresses. Seed phrase = root key = full access. Store offline; never digitize [^src2].

## Developer security principles

- Never trust the network (nodes can be compromised; verify with SPV or own full node)
- Decentralize key storage; avoid single points of failure
- Treat keys like bearer cash; assume any digital copy is compromised
- For Bitcoin applications: never request unnecessary permissions; use the most restrictive script type; watch for signature malleability (historical issue, mitigated by SegWit) [^src1]

[^src1]: [Mastering Bitcoin, ch. 13](../../raw/_inbox/book-mastering-bitcoin-3rd-edition-13-bitcoin-security.md), Antonopoulos & Harding, CC BY-SA 4.0
[^src2]: [Mastering Bitcoin, ch. 5](../../raw/_inbox/book-mastering-bitcoin-3rd-edition-05-wallet-recovery.md), Antonopoulos & Harding, CC BY-SA 4.0

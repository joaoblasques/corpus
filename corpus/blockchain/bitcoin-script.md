---
type: concept
domain: blockchain
status: draft
sources:
  - path: raw/pdf/book-mastering-bitcoin-3rd-edition-07-authorization-and-authentication.md
    channel: book
    ingested_at: 2026-07-07
aliases:
  - Bitcoin Script
  - Script
  - scriptPubKey
  - scriptSig
  - P2PKH
  - P2WPKH
  - Taproot
  - Tapscript
tags:
  - corpus/blockchain
  - concept
created: 2026-07-07
updated: 2026-07-07
---

# Bitcoin Script

TL;DR: Bitcoin Script is a Forth-like, stack-based, non-Turing-complete language embedded in every Bitcoin transaction. The output script (scriptPubKey) specifies spending conditions; the input script (scriptSig/witness) provides proof of authorization. Full nodes execute both scripts together to validate a spend.

## Design philosophy

Script is intentionally minimal and non-Turing-complete (no loops). This ensures:
- Validation time is bounded (no infinite loops)
- Scripts can be verified by all 10,000+ full nodes cheaply
- The language is auditable and predictable

Authorization (who may spend) and authentication (proving you are that person) are both expressed in Script [^src1].

## Standard script types

| Type | When introduced | Description |
|---|---|---|
| P2PK (Pay-to-Public-Key) | Original Bitcoin | Output locks to a raw public key; input provides signature |
| P2PKH (Pay-to-Public-Key-Hash) | Early Bitcoin | Output locks to hash of public key; input provides PubKey + Sig |
| P2MS (Multisig) | BIP 11 | m-of-n multisignature; up to 3 keys |
| P2SH (Pay-to-Script-Hash) | BIP 16 | Output commits to hash of redeem script; input reveals + satisfies script |
| P2WPKH (SegWit v0) | BIP 141 | Like P2PKH but witness data in separate "witness" field |
| P2WSH (SegWit v0 script) | BIP 141 | Like P2SH but witness-based |
| P2TR (Taproot / SegWit v1) | BIP 341 | Key-path spend via Schnorr; or script-path via MAST |

## How execution works

A spend is valid when the concatenated script (`scriptSig || scriptPubKey` for legacy; witness + scriptPubKey for SegWit) executes with a non-empty, non-zero top stack value.

Example P2PKH execution:
1. scriptSig pushes: [Signature, PublicKey]
2. scriptPubKey runs: OP_DUP, OP_HASH160, [PubKeyHash], OP_EQUALVERIFY, OP_CHECKSIG
3. Stack after: [1] (true) → spend is valid [^src1]

## Taproot (BIP 340/341/342)

Taproot (activated November 2021) adds two spend paths to any output:
- **Key path**: single Schnorr signature from the aggregate key (looks like a simple P2PK; maximum privacy)
- **Script path**: reveals a specific leaf of a Merkle tree of scripts (MAST — Merkelized Alternative Script Trees); only the executed leaf is revealed

Benefits:
- Cooperative spends (multisig, Lightning channel close) look identical to single-sig → improved privacy
- Complex smart contract conditions remain hidden unless exercised
- Schnorr signatures are linear (enable MuSig, adaptor signatures, cross-input aggregation)

[^src1]: [Mastering Bitcoin, ch. 7](../../raw/pdf/book-mastering-bitcoin-3rd-edition-07-authorization-and-authentication.md), Antonopoulos & Harding, CC BY-SA 4.0

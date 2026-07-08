---
type: concept
domain: blockchain
status: draft
sources:
  - path: raw/_inbox/book-mastering-ethereum-14-chapter-6-transactions.md
    channel: book
    ingested_at: 2026-07-08
aliases:
  - Ethereum transaction
  - EIP-1559
  - gas price
  - priority fee
  - base fee
  - nonce Ethereum
tags:
  - corpus/blockchain
  - concept
created: 2026-07-08
updated: 2026-07-08
---

# Ethereum Transactions

TL;DR: An Ethereum transaction is a signed message from an EOA that triggers a state change. Post-EIP-1559, fees have a burned base fee plus a validator priority fee (tip). The nonce prevents replay and orders transactions from a single account.

## What Is a Transaction?

"Transactions are signed messages originated by an externally owned account, transmitted by the Ethereum network, and recorded on the Ethereum blockchain" [^src1]. Transactions are the *only* things that can trigger a state change or cause a contract to execute. Contracts never run on their own; everything starts with a transaction.

## Transaction Type System (EIP-2718)

Since EIP-2718, every transaction starts with a type byte: `transaction = tx_type || tx_payload`. As of June 2025, five types exist [^src1]:

| Type | Name | Introduced |
|---|---|---|
| `0x00` | Legacy | Ethereum genesis |
| `0x01` | EIP-2930 (access list) | Berlin hard fork |
| `0x02` | EIP-1559 (fee market) | London hard fork (Aug 2021) |
| `0x03` | EIP-4844 (blob-carrying) | Cancun hard fork (Mar 2024) |
| `0x04` | EIP-7702 | Recent |

## Core Transaction Fields (Legacy / Type 0)

All transactions share these fundamental fields [^src1]:

**Chain ID** — prevents replay attacks across different networks (added by EIP-155).

**Nonce** — a sequence number issued by the originating EOA. Each new transaction from the same account increments the nonce by 1. Prevents message replay; also determines transaction ordering from a single account.

**Gas limit** — maximum gas units the sender is willing to buy. The sender pays only for actual gas used, not the full limit.

**Recipient** — destination Ethereum address. Empty (`to` field absent) for contract-creation transactions.

**Value** — amount of ether (in wei) to transfer.

**Data** — variable-length binary payload. For contract calls, contains the ABI-encoded function selector and arguments.

**v, r, s** — three components of the ECDSA digital signature by the originating EOA's private key. The `from` address is not transmitted; it is recovered from the signature.

Serialization uses **Recursive-Length Prefix (RLP)** encoding. All numbers are big-endian integers [^src1].

## EIP-1559 Fee Market (Type 2) — the Standard

Introduced in the London hard fork (August 5, 2021), EIP-1559 replaced the simple gas-price auction with a two-part fee [^src1]:

**Base fee** — the minimum fee required to include a transaction, denominated in wei/gas. Set by the protocol based on block utilization:
- Block gas target = 15 million gas (half the 30M limit).
- If a block uses more than 15M gas → base fee increases next block.
- If a block uses less → base fee decreases.
- Base fee is **burned** (destroyed), reducing ETH supply.

**Priority fee (tip)** — optional payment to validators to incentivize inclusion. Goes to the block proposer, not burned.

Two EIP-1559 fields replace legacy `gasPrice`:
- `maxFeePerGas` — absolute maximum the sender will pay (base fee + tip).
- `maxPriorityFeePerGas` — maximum tip the sender will pay to the validator.

Effective tip = `min(maxPriorityFeePerGas, maxFeePerGas - baseFee)`.

## EIP-4844 Blob Transactions (Type 3)

Introduced in the Cancun hard fork (March 13, 2024) to support L2 rollups [^src1]:

- Carries a **blob** sidecar — ~131,000 bytes of data not accessible by the EVM but whose KZG commitment is accessible.
- Blobs use a separate **blob gas** market (independent from normal gas), also following an EIP-1559-style targeting rule.
- Additional fields: `maxFeePerBlobGas`, `blobVersionedHashes` (KZG commitment hashes).
- Blobs are pruned after ~18 days; only the commitment remains permanently on chain.

## Special Transaction: Contract Creation

A contract-creation transaction has an **empty `to` field**. The `data` field contains the contract's compiled bytecode (plus constructor arguments). The resulting contract address is deterministically derived from `keccak256(rlp([sender, nonce]))` [^src1].

## Nonce Mechanics

The nonce is critical for two reasons [^src1]:
1. **Replay protection** — a signed transaction with nonce N can only be included once.
2. **Ordering** — transactions from the same EOA are processed in strict nonce order. A gap (e.g., nonce 5 never submitted) blocks all higher-nonce transactions.

## Gas and Computation Cost

Gas is the unit measuring computational effort. Complex smart-contract calls cost more gas than simple ETH transfers (which cost 21,000 gas). Gas metering is enforced inside the EVM opcode-by-opcode; if gas runs out mid-execution, the transaction reverts (but gas spent is not refunded).

## Cross-links

- [Ethereum](/blockchain/ethereum.md) — Ethereum's account model and EOA types.
- [Ethereum Virtual Machine](/blockchain/ethereum-virtual-machine.md) — executes the transaction's data payload.
- [Smart Contracts](/blockchain/smart-contracts.md) — what the data payload calls.
- [Ethereum Scaling](/blockchain/ethereum-scaling.md) — EIP-4844 blobs and rollup data.
- [Public-Key Cryptography](/blockchain/public-key-cryptography.md) — ECDSA signatures that authenticate transactions.
- [Bitcoin Transactions](/blockchain/bitcoin-transactions.md) — UTXO model comparison.

[^src1]: [Mastering Ethereum — Chapter 6. Transactions](../../raw/_inbox/book-mastering-ethereum-14-chapter-6-transactions.md)

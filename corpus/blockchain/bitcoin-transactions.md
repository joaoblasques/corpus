---
type: concept
domain: blockchain
status: draft
sources:
  - path: raw/pdf/book-mastering-bitcoin-3rd-edition-06-transactions.md
    channel: book
    ingested_at: 2026-07-07
  - path: raw/pdf/book-mastering-bitcoin-3rd-edition-09-transaction-fees.md
    channel: book
    ingested_at: 2026-07-07
aliases:
  - UTXO
  - unspent transaction output
  - bitcoin transaction
  - coinbase transaction
  - transaction inputs
  - transaction outputs
tags:
  - corpus/blockchain
  - concept
created: 2026-07-07
updated: 2026-07-07
---

# Bitcoin Transactions

TL;DR: A Bitcoin transaction is a signed message that convinces full nodes to update their database: removing value from one set of keys and assigning it to another. Bitcoins don't exist as discrete objects — they exist only as unspent transaction outputs (UTXOs). A transaction consumes UTXOs as inputs and creates new UTXOs as outputs.

## The UTXO model

Bitcoin has no accounts or balances. Instead, the system tracks **Unspent Transaction Outputs (UTXOs)**: records of the form "X satoshis, controlled by script Y."

To transfer value, Alice creates a transaction that:
1. **Inputs**: references one or more UTXOs she controls (spending them)
2. **Outputs**: creates new UTXOs assigning value to recipients

"Alice sends Bob 1 BTC" means: the UTXO formerly controlled by Alice's key is destroyed; two new UTXOs are created — one controlled by Bob's key, one controlled by Alice's key (change) [^src1].

The land-title analogy: Alice doesn't "hand" Bob bitcoins; she convinces a public record-keeper (full nodes) to update who controls the land parcel [^src1].

## Transaction structure

| Field | Description |
|---|---|
| Version | Transaction format version |
| Inputs | List of UTXOs being spent; each includes: txid of previous tx, output index, scriptSig/witness |
| Outputs | List of new UTXOs; each includes: value in satoshis, scriptPubKey |
| Locktime | Earliest block/time this tx can be included |

The standard serialization format (Bitcoin Core's binary format) is used for P2P relay and commitments. PSBT (BIP 174/370) is an alternative format for partially-signed transactions in hardware wallet workflows [^src1].

## Transaction fees

Miners choose which transactions to include in blocks. Fee = sum(input values) − sum(output values). There is no explicit "fee output" — unallocated value is implicitly collected by the miner via the coinbase transaction [^src2].

**Fee market mechanics**:
- Blocks have a maximum size (weight); miners maximize fee revenue given the constraint
- Transactions signal willingness to pay via fee rate (sat/vbyte)
- **RBF (Replace-By-Fee)**: a transaction in mempool can be replaced by a higher-fee version spending the same inputs
- **CPFP (Child-Pays-For-Parent)**: if a low-fee parent is stuck in mempool, a child transaction spending its output with a high fee incentivizes miners to include both

**Conflicting transactions**: a UTXO can only be spent once. If Alice signs two transactions spending the same UTXO (double-spend attempt), only one will be confirmed — the blockchain's topological ordering enforces this [^src2].

## Coinbase transaction

The first transaction in every block. It:
- Has no inputs (creates new bitcoins out of "thin air")
- Awards the block subsidy (currently 3.125 BTC after the 2024 halving) + all transaction fees in the block
- Is the mechanism through which new bitcoin enters circulation

[^src1]: [Mastering Bitcoin, ch. 6](../../raw/pdf/book-mastering-bitcoin-3rd-edition-06-transactions.md), Antonopoulos & Harding, CC BY-SA 4.0
[^src2]: [Mastering Bitcoin, ch. 9](../../raw/pdf/book-mastering-bitcoin-3rd-edition-09-transaction-fees.md), Antonopoulos & Harding, CC BY-SA 4.0

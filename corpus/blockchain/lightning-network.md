---
type: concept
domain: blockchain
status: draft
sources:
  - path: raw/_inbox/book-mastering-bitcoin-3rd-edition-14-second-layer-applications.md
    channel: book
    ingested_at: 2026-07-08
aliases:
  - Lightning Network
  - LN
  - Lightning
  - routed payment channels
tags:
  - corpus/blockchain
  - concept
created: 2026-07-08
updated: 2026-07-08
---

# Lightning Network

TL;DR: The Lightning Network (LN) is a second-layer protocol that routes Bitcoin payments across a mesh of bidirectional payment channels, using Hash Time Lock Contracts (HTLCs) to enable trustless multi-hop payments. It achieves millisecond settlement, sub-cent fees, and strong payment privacy via onion routing — all without touching the base-layer blockchain for each payment.

## What Is the Lightning Network

"The Lightning Network (LN) is a proposed routed network of bidirectional payment channels connected end-to-end. A network like this can allow any participant to route a payment from channel to channel without trusting any of the intermediaries." [^src1]

First described by Joseph Poon and Thadeus Dryja in February 2015, building on earlier payment channel concepts [^src1]. As of the 3rd edition of *Mastering Bitcoin*, at least five independent open-source implementations exist, coordinated by the *Basics of Lightning Technology (BOLT)* interoperability specification [^src1].

## How Routing Works

### Channel Graph

Each LN node maintains one or more payment channels (see [Payment Channels](/blockchain/payment-channels.md)). Together, channels form a graph. A sender finds a path through this graph to reach a recipient without a direct channel [^src1].

Nodes advertise routing information — open channels, capacity, and fees — via a P2P flooding model similar to how Bitcoin propagates transactions [^src1].

### HTLC Chain

Payments traverse a path using Hash Time Lock Contracts (HTLCs) [^src1]:

1. The recipient generates a secret `R` and publishes its hash `H` to the sender (as an invoice).
2. The sender constructs an HTLC on the first channel: "pay hash `H` or refund after N blocks."
3. Each intermediate node forwards an HTLC on the next channel, decrementing the timeout and collecting a small fee.
4. The final recipient reveals `R`, claiming the last HTLC.
5. `R` propagates backwards; each intermediate node uses it to claim the upstream HTLC.

"Alice has paid Eric 1 bitcoin without opening a channel to Eric. None of the intermediate parties in the payment route had to trust each other." [^src1]

### Example: Alice → Bob → Carol → Diana → Eric

In a five-node example [^src1]:
- Alice has a channel with Bob (4 BTC capacity); Bob with Carol; Carol with Diana; Diana with Eric.
- Alice sends 1.003 BTC in an HTLC to Bob (timeout: 10 blocks). The extra 0.003 pays routing fees.
- Bob forwards 1.002 BTC to Carol (9 blocks); Carol 1.001 BTC to Diana (8 blocks); Diana 1 BTC to Eric (7 blocks).
- Eric claims 1 BTC by revealing `R` to Diana. Diana claims from Carol. The secret propagates all the way back to Bob claiming from Alice.
- Net result: Alice paid 1 BTC to Eric; each intermediate node earned ~0.001 BTC fee; all channel balances updated off-chain.

## Onion Routing (Sphinx)

"The LN implements an onion-routed protocol based on a scheme called Sphinx." [^src1]

Properties [^src1]:
- Intermediate nodes can decrypt only their layer — they learn the previous and next hop but not the full path.
- They cannot determine path length or their position in it.
- Each packet is fixed-length and padded with random data to prevent length-based inference.
- Unlike Tor, there are no exit nodes; payments never need to be transmitted to the Bitcoin blockchain.

The sender wraps the route in nested encryption, outermost to innermost, "starting with the end and working backward." Each hop unwraps one layer and forwards the remainder [^src1].

## Benefits

"LN is layered on top of the Bitcoin network, giving Bitcoin a significant increase in capacity, privacy, granularity, and speed, without sacrificing the principles of trustless operation without intermediaries." [^src1]

| Benefit | Detail |
|---|---|
| **Privacy** | Payments not public; intermediaries see only adjacent hops, not sender/recipient [^src1] |
| **Fungibility** | Harder to apply blockchain surveillance and blacklists [^src1] |
| **Speed** | Settled in milliseconds; HTLCs cleared without mining a block [^src1] |
| **Granularity** | Enables payments as small as Bitcoin's dust limit or smaller [^src1] |
| **Capacity** | Increases Bitcoin system capacity by orders of magnitude; bounded only by node speed and capacity [^src1] |
| **Trustless** | Uses Bitcoin transactions between peers; no trusted intermediary required [^src1] |

## Requirements from Base Layer

LN can be applied to any blockchain that supports [^src1]:
- Multisignature transactions
- Timelocks (absolute and relative)
- Basic smart contracts (script)

On Bitcoin, it specifically uses 2-of-2 multisig funding outputs, `CHECKLOCKTIMEVERIFY` (CLTV), `CHECKSEQUENCEVERIFY` (CSV), and HTLC scripts (see [Bitcoin Script](/blockchain/bitcoin-script.md)).

## Colored Coins on Lightning (RGB and Taproot Assets)

Both RGB and Taproot Assets protocols are designed to forward non-bitcoin assets over LN [^src1]. Two forwarding strategies exist [^src1]:

- **Native forwarding** — every hop must hold the asset. Requires a separate LN-like network per asset.
- **Translated forwarding** — only the edge hops need the asset; intermediate hops use BTC. Used by Taproot Assets; may be vulnerable to the *free American call option* problem (receivers selectively accept/reject based on exchange rate).

## BOLT Specification

The multi-implementation LN ecosystem is coordinated by BOLT (Basics of Lightning Technology), a set of interoperability standards. LN commitment state uses a 48-bit index, supporting more than 281 trillion (2.8 × 10¹⁴) state transitions per channel [^src1].

## Related Pages

- [Payment Channels](/blockchain/payment-channels.md) — the fundamental building block; funding, commitment, and settlement transactions
- [Bitcoin Script](/blockchain/bitcoin-script.md) — Script opcodes enabling HTLCs and timelocks
- [Bitcoin Transactions](/blockchain/bitcoin-transactions.md) — UTXO model that anchors channel state

[^src1]: [Mastering Bitcoin, 3rd Edition — Chapter 14: Second-Layer Applications](../../raw/_inbox/book-mastering-bitcoin-3rd-edition-14-second-layer-applications.md)

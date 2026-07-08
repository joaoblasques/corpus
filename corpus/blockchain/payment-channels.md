---
type: concept
domain: blockchain
status: draft
sources:
  - path: raw/_inbox/book-mastering-bitcoin-3rd-edition-14-second-layer-applications.md
    channel: book
    ingested_at: 2026-07-08
aliases:
  - payment channel
  - state channel
  - bidirectional payment channel
  - unidirectional payment channel
tags:
  - corpus/blockchain
  - concept
created: 2026-07-08
updated: 2026-07-08
---

# Payment Channels

TL;DR: Payment channels are trustless, off-chain mechanisms for exchanging Bitcoin transactions between two parties. Only two on-chain transactions are needed (funding + settlement); an unlimited number of off-chain commitment transactions update the balance in between, enabling high-throughput, low-latency, and low-fee micropayments.

## What Is a Payment Channel

"Payment channels are a trustless mechanism for exchanging Bitcoin transactions between two parties outside of the Bitcoin blockchain. These transactions, which would be valid if settled on the Bitcoin blockchain, are held offchain instead, waiting for eventual batch settlement." [^src1]

The term "channel" is a metaphor. State channels are virtual constructs represented by the exchange of state between two parties outside of the blockchain [^src1]. A payment channel is a state channel where the state being altered is the balance of a virtual currency [^src1].

## Lifecycle of a Channel

Three transaction types define a channel's lifetime [^src1]:

1. **Funding transaction** — locks a shared balance on-chain in a 2-of-2 multisig output, establishing channel capacity.
2. **Commitment transactions** — signed off-chain messages that alter the balance. Either party could broadcast them, but both prefer to hold them.
3. **Settlement transaction** — the final on-chain close, either cooperative (no timelock, immediate) or unilateral (broadcasting the latest commitment).

"In the entire lifetime of the channel, only two transactions need to be submitted for mining on the blockchain: the funding and settlement transactions. In between these two states, the two parties can exchange any number of commitment transactions that are never seen by anyone else or submitted to the blockchain." [^src1]

## Simple (Unidirectional) Channel

In the classic example, Emma pays Fabian per second of streaming video [^src1]:

- Emma funds a 2-of-2 multisig with 36 millibits (1 hour budget).
- Each second, Emma signs a new commitment transaction crediting Fabian one more second of payment and returning the remainder to herself.
- Fabian counter-signs and releases 1 second of video.
- At the end, Fabian broadcasts the final commitment (or they cooperatively sign a settlement).

Only the funding and one settlement transaction ever appear on-chain, regardless of how many seconds of video were consumed [^src1].

## Making Channels Trustless: Timelocks

Two problems arise in the naive design [^src1]:
- If Fabian disappears after the funding transaction, Emma's funds are locked forever.
- Emma could broadcast an early commitment (e.g., commit #1) to avoid paying for video already consumed.

**Solution — timelocks:**
- Emma constructs a refund transaction (the first commitment) with a long absolute timelock *before* broadcasting the funding transaction. This guarantees she can reclaim funds if Fabian disappears.
- Each subsequent commitment gets a slightly shorter timelock. The most recent commitment can therefore always be broadcast before any earlier one [^src1].

For the single-direction case, an alternative is the **Spillman-style channel** (2013): only Fabian holds both signatures on each commitment, so he always prefers to broadcast the latest, highest-paying state. Requires SegWit (safe only since 2017) [^src1].

## Bidirectional Channels: Asymmetric Revocable Commitments

Timelocks limit channel lifetime and cap the number of state transitions. Bidirectional channels use **revocation keys** instead [^src1].

### Design

Each party holds a *different* commitment transaction [^src1]:
- Hitesh's version: pays Irene immediately; pays Hitesh after 1,000-block timelock.
- Irene's version: pays Hitesh immediately; pays Irene after 1,000-block timelock.

This asymmetry disincentivises unilateral broadcasts (the broadcaster must wait while the counterparty can spend immediately).

### Revocation Key Mechanics

Each commitment's delayed output has two redemption paths [^src1]:
1. After 1,000 blocks — the holder claims their funds normally.
2. Immediately with the **revocation key** — the counterparty can claim *all* funds as a penalty.

The revocation key is constructed from two half-secrets, one per party. When a new commitment is agreed upon, each party reveals their half-secret for the *prior* commitment. "If Hitesh cheats, Irene gets BOTH outputs." [^src1]

"Asymmetric revocable commitments with relative time locks (CSV) are a much better way to implement payment channels and a very significant innovation in this technology. With this construct, the channel can remain open indefinitely and can have billions of intermediate commitment transactions." [^src1]

In Lightning Network implementations, the commitment state uses a 48-bit index, allowing more than 281 trillion state transitions per channel [^src1].

## Hash Time Lock Contracts (HTLC)

HTLCs extend payment channels to support multi-hop routed payments (see [Lightning Network](/blockchain/lightning-network.md)).

An HTLC commits funds to a redeemable secret with an expiration [^src1]:

```
IF
    # Payment if you have the secret R
    HASH160 <H> EQUALVERIFY
    <Receiver Public Key> CHECKSIG
ELSE
    # Refund after timeout.
    <lock time> CHECKLOCKTIMEVERIFY DROP
    <Payer Public Key> CHECKSIG
ENDIF
```

- The recipient creates a secret `R`, publishes its hash `H`.
- The payer locks funds to `H`; only the holder of `R` can claim them.
- If unclaimed after the timeout, the payer gets a refund [^src1].

HTLCs chain across hops in the Lightning Network, propagating the same `H` and decrementing the timelock at each hop.

## UTXO Primitives Used

Payment channels are built on the following Bitcoin primitives [^src1]:

| Primitive | Role |
|---|---|
| 2-of-2 multisig (Quorum of Control) | Locks the funding output; both parties must sign |
| Timelock / CSV / CLTV | Sequences commitments; enables refunds; enforces HTLC expiry |
| No Double-Spend guarantee | Ensures spending the funding output with the latest commitment invalidates all earlier ones |
| Nonexpiration | Commitment transactions remain valid until broadcast |
| Authorization (digital signatures) | Each party's signature required to advance state |

## Related Pages

- [Lightning Network](/blockchain/lightning-network.md) — routed network of payment channels
- [Bitcoin Script](/blockchain/bitcoin-script.md) — Script opcodes (CHECKLOCKTIMEVERIFY, CHECKSEQUENCEVERIFY) that implement timelocks
- [Bitcoin Transactions](/blockchain/bitcoin-transactions.md) — UTXO model underlying payment channels

[^src1]: [Mastering Bitcoin, 3rd Edition — Chapter 14: Second-Layer Applications](../../raw/_inbox/book-mastering-bitcoin-3rd-edition-14-second-layer-applications.md)

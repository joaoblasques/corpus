---
type: concept
domain: software-engineering
status: draft
sources:
  - path: raw/email/email-2026-06-02-i-spent-8-hours-learning-the-cap-theorem-heres-what-i-found.md
    channel: email
    ingested_at: 2026-06-12
aliases:
  - CAP theorem
  - CAP
  - Brewer's theorem
  - consistency availability partition tolerance
  - CP
  - AP
tags:
  - corpus/software-engineering
  - concept
created: 2026-06-12
updated: 2026-06-12
---

# CAP Theorem

**TL;DR**: Eric Brewer's theorem states that any distributed data store can provide at most two of Consistency, Availability, and Partition tolerance [^src1]. Because partitions are unavoidable in real networks, the practical choice in a partitioned system is binary: **CP** (refuse to answer to stay consistent) or **AP** (answer with possibly-stale data to stay available) [^src1].

## The three properties

- **Consistency (C)** — all nodes see the same data at the same time; the moment a write is acknowledged, every node reflects it (linearizability across nodes) [^src1].
- **Availability (A)** — every request gets a response; if a node is up, it answers [^src1].
- **Partition tolerance (P)** — the system keeps operating even when the network between nodes breaks and messages are lost [^src1].

## CAP consistency ≠ ACID consistency

A critical disambiguation: the C in CAP is **not** the C in ACID [^src1].

- **ACID consistency** — transactions don't violate constraints (referential integrity, unique keys).
- **CAP consistency** — linearizability across nodes.

> "Two different things that somehow share a name and confuse us." [^src1]

## Why you only really pick CP or AP

Partition tolerance "isn't a knob you can tune" — you cannot predict network failures, cables get unplugged, availability zones lose connectivity, and even a heavy garbage-collection pause can look exactly like a partition to a node's neighbors [^src1]. Since partitions will happen, P is mandatory; the real decision is what to sacrifice during one [^src1].

In a two-node setup where Node A and Node B cannot talk:

- **Choose consistency (CP)**: Node A refuses the write/read until it can confirm with Node B. The system becomes partially unavailable during the partition [^src1].
- **Choose availability (AP)**: both nodes keep answering and accepting writes, but they drift out of sync — B is unaware of A's write and vice versa [^src1].

Attempting both fails by construction: if a client writes `x = 1` to Node A and another reads `x` from Node B during a partition, B must either return a stale value (violating C) or refuse to respond (violating A). "There is no world where Node B answers correctly and immediately." [^src1]

## Relationship to distributed systems

CAP is the formal statement behind several [distributed systems fallacies](/software-engineering/distributed-systems-fallacies.md) — chiefly "the network is reliable" and "the network is secure." The eventual-consistency design used in [microservices](/software-engineering/microservices.md) is an AP-side tradeoff: temporary inconsistency is accepted to keep the system answering [^src1].

## See also

- [Distributed Systems Fallacies](/software-engineering/distributed-systems-fallacies.md) — partition tolerance is the formalization of "the network is reliable" being false
- [Microservices](/software-engineering/microservices.md) — eventual consistency as an AP tradeoff
- [Software Engineering hub](/software-engineering/README.md)

---

[^src1]: [I spent 8 hours learning the CAP theorem](../../raw/email/email-2026-06-02-i-spent-8-hours-learning-the-cap-theorem-heres-what-i-found.md)

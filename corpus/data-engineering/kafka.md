---
type: entity
domain: data-engineering
status: draft
sources:
  - path: 03_Resources/Study Notes/Kafka Tutorial for Beginners - Core Concepts.md
    channel: notes
    ingested_at: 2026-05-21
aliases:
  - Apache Kafka
  - Kafka
  - kafka
tags:
  - corpus/data-engineering
  - entity
created: 2026-05-21
updated: 2026-05-21
---

# Apache Kafka

**TL;DR**: An event streaming platform that decouples services through asynchronous "fire and forget" communication — producers publish events to topics; consumers read independently; data is retained on disk [^src1].

## The problem it solves

Synchronous API calls between microservices create tight coupling: performance bottlenecks, single points of failure, the "domino effect" where one slow service degrades the whole system [^src1]. Kafka inserts a durable buffer so services no longer need to know about each other.

## Core model

```
Producer → Topic (Partitions) → Consumer Group → Downstream Processing
```

### Events (Records / Messages)

The fundamental unit: a business fact with a key, value, and timestamp. Immutable once written [^src1].

### Topics

Named categories where events are published. Producers write to a topic; consumers subscribe to it. A topic is divided into **partitions** [^src1].

### Partitions

Ordered, immutable sequences within a topic. Enable:
- **Horizontal scalability** — different partitions processed by different consumer instances
- **Parallel processing** — multiple partitions read simultaneously
- **Ordering guarantee** — within a single partition only (not across partitions) [^src1]

### Consumer Groups

Multiple consumer instances sharing partition processing. Each partition is assigned to exactly one consumer in the group, enabling scalable consumption without duplicate processing [^src1].

### Brokers

Servers that store topic partitions. Partitions are replicated across multiple brokers; one is the leader (handles reads/writes), others are followers (failover) [^src1].

## Kafka vs traditional message queues

| Kafka | Traditional MQ |
|---|---|
| Message retained on disk (configurable retention) | Message deleted after consumption |
| Multiple independent consumers can replay | Single consumer ownership typical |
| Designed for high-throughput streaming | Designed for reliable point-to-point delivery |

[^src1]

## Kafka Streams API

Library for real-time transformations, aggregations, joins, and filtering on data in-flight — no separate processing framework required [^src1].

## ZooKeeper → KRaFt

Kafka historically used Apache ZooKeeper for cluster coordination. Kafka 3.0+ uses **KRaFt** — a native Raft-based consensus protocol that removes the ZooKeeper dependency, simplifying deployment [^src1].

## See also

- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [[03_Resources/Study Notes/Kafka Tutorial for Beginners - Core Concepts|Kafka Tutorial for Beginners - Core Concepts]]

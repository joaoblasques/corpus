---
type: entity
domain: data-engineering
status: draft
sources:
  - path: 03_Resources/Study Notes/Kafka Tutorial for Beginners - Core Concepts.md
    channel: notes
    ingested_at: 2026-05-21
  - path: raw/web/kafka-share-groups-and-parallelizing-consumption-part-1-tuni.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/can-kafka-queues-make-consumers-faster-part-2-head-of-line-b.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/introducing-dimster-a-performance-benchmarking-tool-for-apac.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-05-14-duckdb-goes-remote-when-lakehouses-guess-netflix-tames-data.md
    channel: email
    ingested_at: 2026-06-15
  - path: raw/email/email-2026-05-28-slashing-snowflake-costs-open-source-agent-tradeoffs-kafkas.md
    channel: email
    ingested_at: 2026-06-15
  - path: raw/email/email-2025-05-15-if-you-re-learning-kafka-this-article-is-for-you.md
    channel: email
    ingested_at: 2026-06-19
aliases:
  - Apache Kafka
  - Kafka
  - kafka
  - share groups
  - Kafka Queues
  - head-of-line blocking
  - zero-copy
  - sendfile
  - consumer offset
  - rebalancing
  - acks
  - diskless Kafka
tags:
  - corpus/data-engineering
  - entity
created: 2026-05-21
updated: 2026-06-19
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

## Internals: why Kafka is fast

LinkedIn built Kafka ~2011 to handle log processing — combining traditional log aggregators with publish/subscribe messaging for high throughput and scalability [^src7]. Several design choices explain the performance [^src7]:

- **Offsets, not message IDs.** A message (with an optional **key**) is just bytes; it has no explicit ID, only a **logical offset**. A consumer computes the next offset by adding the current message's length — avoiding the overhead of an ID→location index [^src7].
- **Segment files.** Each partition is a logical log implemented as a set of **segment files** (~1 GB); the broker **appends** each new message to the active segment [^src7].
- **Rely on the OS page cache.** Kafka lets the OS filesystem + **kernel page cache** handle storage rather than a proprietary cache — sidestepping the JVM's high object-memory overhead and GC slowdowns; the kernel reclaims page-cache memory when applications need it [^src7].
- **Sequential access.** Disk beats RAM slightly for *sequential* access; Kafka makes both writes (append to last segment) and reads (consume a partition in order, via offset→file and timestamp→offset index files) sequential [^src7].
- **Zero-copy (`sendfile()`).** Normally serving a file over the network copies data four times with four user/kernel context switches; the `sendfile()` syscall copies directly **page cache → socket buffer**, cutting it to **two context switches** and skipping the copy into the Kafka application [^src7].
- **Batching + compression.** The protocol's **message set** abstraction groups messages, cutting network round-trips and enabling larger sequential disk writes; batches can be compressed when bandwidth is the bottleneck [^src7].

## The producer protocol

When you call the producer API [^src7]: a **ProducerRecord** (value + topic, optionally key/partition/timestamp/headers) is **serialized** to byte arrays; if no partition is given, a **partitioner** chooses one from the key; the record is added to a **batch** for its topic+partition; a separate thread sends batches to the right broker, which returns metadata (topic, partition, offset) on success or an error (the producer may retry) [^src7].

- **Send modes:** *fire-and-forget* (no confirmation, may lose data), *synchronous* (wait for response — rare in production, hurts performance), *asynchronous* (send without waiting, with a callback for errors) [^src7].
- **Delivery acknowledgement — the `acks` parameter** controls how many replicas must receive a record before the write is considered successful [^src7]:
  - `acks=0` — don't wait; highest throughput, high risk of data loss.
  - `acks=1` — leader acknowledges receipt.
  - `acks=all` — all replicas acknowledge; safest (survives a broker crash) but adds latency.
- **Partitioning by key:** null key → **Round-Robin** (≤ v2.3) or **Sticky Partitioner** (≥ v2.4, fills one partition per batch then switches); non-null key → hashed and mapped to a partition, so same-key messages land on the same partition [^src7].

## The consumer protocol

Kafka chose a **pull** model (vs push systems like Scribe/Flume) so consumers read at their own pace — catching up if behind, batching when ready, never flooded [^src7]. The Consumer API is an infinite **poll loop** issuing async pull requests carrying the start offset; the broker seeks and returns data; the consumer computes the next offset [^src7].

- **Offset commit.** Uniquely, the consumer does *not* track its own position — it tells the broker it has processed up to an offset (**offset commit**), and the broker records this in an internal topic; everything before that offset is assumed processed [^src7].
- **Consumer groups** are coordinated by a **Group Coordinator** (one broker, chosen by group ID): the first consumer to join becomes **leader**, gets the active-consumer list, and assigns partition subsets; members maintain ownership via **heartbeats** [^src7].
- **Partition assignment strategies:** **Range** (default; consecutive partitions per topic, uneven splits burden the first consumers), **Round Robin** (across all subscribed topics, maximizes consumer use but needs much movement on rebalance), **Sticky** (round-robin-like first assignment, but preserves as many existing assignments as possible on reassignment) [^src7].
- **Rebalancing** (membership changes): **eager** (all consumers stop, drop ownership, rejoin — brief full unavailability) vs **cooperative** (move only a subset of partitions, others keep processing) [^src7].

## The object-storage trend (decoupling compute and storage)

Kafka's page-cache design tightly couples compute and storage — you can't scale them independently, and replication across availability zones incurs high transfer costs in the cloud [^src7]. Efforts to fix this [^src7]:

- **Tiered storage** (originally Uber's proposal): recent data on local broker disk, historical data in remote object storage (HDFS/S3/GCS) — but brokers aren't fully stateless (replication still happens, data moves on membership changes) [^src7].
- **Object-storage-native Kafka** — **WarpStream, AutoMQ, Bufstream, Redpanda** operate Kafka **directly on object storage**: cheaper, compute/storage separated, and **replication eliminated** because object storage already ensures durability [^src7].
- **KIP-1150 "Diskless Topics"** (Aiven, 2025): a new topic class that **delegates replication to object storage**, aiming to cut Kafka infrastructure costs by up to 80% [^src7].

## Share Groups (Kafka Queues) and parallelism beyond partitions

With classic **consumer groups**, partition count is the parallelism ceiling: a topic with 4 partitions can be processed by at most 4 instances in the same group, because only one instance processes a partition at a time [^src2]. Kafka 4.x adds **share groups** (a.k.a. "Kafka Queues"), a new primitive where a share group can have **more active instances than partitions** [^src2].

### Head-of-line blocking

The core motivation is **head-of-line blocking**: because one instance owns a partition, *any* delay in processing stalls the entire partition [^src2]. Example: a pipeline that calls an external enrichment API for ~half its records — if that API is briefly unavailable, the consumer can't process any messages, even ones that don't need enrichment [^src2]. Benchmarks show share groups provide little advantage when processing has no delay, but once you add realistic per-message processing time (modelling IO), share groups scale **linearly** as instances are added — at least 8x throughput observed going from 4 to 32 instances, with no per-instance overhead [^src2]. The decisive **downside is losing ordering guarantees**: several instances consume from the same partition, so order is no longer preserved — a deal-breaker for many systems [^src2].

### The `max.poll.records` trap (the new bottleneck)

With share groups the parallelism bottleneck shifts from partition count to the **inflight record budget** and the **size of fetch requests** [^src3]. Two configs dominate [^src3]:

- `group.share.partition.max.record.locks` (broker-side) — how many records can be locked/inflight per partition (default 2000, max 10000).
- `max.poll.records` (consumer) — records returned per poll (default 500).

With the default 500, a single consumer can grab 25% of a 2000-record budget; at 5 ms/record that batch takes 2.5 s, during which other consumers sit idle [^src3]. This produces a **greedy-capture regime**: a few consumers hog large batches while the rest starve, collapsing 300 consumers across 6 partitions to ~24 effective consumers (~4800 msg/s vs a 60K theoretical max) [^src3]. At low load the system can instead drift into **accidental fair-sharing** (small batches spread evenly), which *looks* healthy but is fragile and can suddenly degrade — "consumption may look fine for a long time, but suddenly degrade" [^src3].

**Rule of thumb** [^src3]: set `max.poll.records ≈ group.share.partition.max.record.locks / consumers-per-partition`, then go somewhat lower to absorb timing variance, fetch skew, and backlog. For very long processing (>1 s) drop it to 1; or raise `max.record.locks` for a more forgiving budget. The default of 500 is "arguably the wrong value for share groups" — there is no broker-side fair-sharing enforcement yet [^src3].

### Dimster (benchmarking)

These findings were produced with **Dimster** (DIMensional teSTER), an open-source Kafka-centric performance benchmarking tool [^src4]. Its design idea is **dimensional testing**: treat each config/workload aspect (batch size, acks, consumer count, partition count, produce rate) as a dimension in N-dimensional space and run identical benchmarks sweeping one or two dimensions at a time [^src4]. It ships four test modes — **run** (fixed throughput + live interaction to mutate a running workload), **explore** (find peak sustainable throughput under a latency target), **drain-backlog**, and **correctness** (detect loss, corruption, out-of-order, duplicates) — and emits self-contained, reproducible result bundles (JSON/CSV, source configs, broker logs, charts, Grafana-as-HTML) [^src4]. It uses Kubernetes as a standardized runtime (minikube/k3d locally up to EKS/GKE) [^src4]. In an explore test, a 300-member share group hit 95% of theoretical max on only 10 partitions, where a consumer group needed 300 partitions [^src4].

## See also

- [[data-engineering/idempotent-pipelines|Idempotent Pipelines]] — append-only stream ingestion with at-most-once settings
- [[data-engineering/stream-processing|Stream Processing]] — Kafka as the transport layer in real-time pipelines
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [[03_Resources/Study Notes/Kafka Tutorial for Beginners - Core Concepts|Kafka Tutorial for Beginners - Core Concepts]]
[^src2]: [Can Kafka Queues Make Consumers Faster? Part 2: Head-Of-Line Blocking](../../raw/web/can-kafka-queues-make-consumers-faster-part-2-head-of-line-b.md)
[^src3]: [Kafka Share Groups and Parallelizing Consumption — Part 1: Tuning max.poll.records](../../raw/web/kafka-share-groups-and-parallelizing-consumption-part-1-tuni.md)
[^src4]: [Introducing Dimster, a performance benchmarking tool for Apache Kafka](../../raw/web/introducing-dimster-a-performance-benchmarking-tool-for-apac.md)
[^src5]: [TLDR Data — Kafka Queues / Head-of-Line Blocking (newsletter origin)](../../raw/email/email-2026-05-14-duckdb-goes-remote-when-lakehouses-guess-netflix-tames-data.md)
[^src6]: [TLDR Data — Kafka's New Bottleneck / Share Groups (newsletter origin)](../../raw/email/email-2026-05-28-slashing-snowflake-costs-open-source-agent-tradeoffs-kafkas.md)
[^src7]: [If you're learning Kafka, this article is for you (Vu Trinh)](../../raw/email/email-2025-05-15-if-you-re-learning-kafka-this-article-is-for-you.md)

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
  - path: raw/web/web-the-trinity-of-modern-data-architecture-process-intelligence-b19b93a7.md
    channel: web
    ingested_at: 2026-07-03
  - path: raw/_inbox/pdf-designing-event-driven-systems-concepts-and-patter-part-01.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/web-when-not-to-use-queues-for-kafka-9296826b.md
    channel: web
    ingested_at: 2026-08-10
  - path: raw/_inbox/web-diskless-kafka-at-fintech-robinhood-for-cost-efficient-log-a-0ec9eb53.md
    channel: web
    ingested_at: 2026-08-10
  - path: raw/_inbox/web-mcp-vs-rest-http-api-vs-kafka-the-architect-s-guide-to-agent-e36f1d1c.md
    channel: web
    ingested_at: 2026-08-10
  - path: raw/_inbox/web-my-confluent-chapter-from-apache-kafka-startup-to-11-billion-9dcd0637.md
    channel: web
    ingested_at: 2026-08-10
  - path: raw/_inbox/web-why-databricks-and-snowflake-speak-the-kafka-protocol-ingest-b83e18be.md
    channel: web
    ingested_at: 2026-08-10
  - path: raw/_inbox/web-when-to-use-amqp-jms-kafka-or-mqtt-trade-offs-not-a-winner-7db4e92a.md
    channel: web
    ingested_at: 2026-08-10
aliases:
  - Apache Kafka
  - Kafka
  - kafka
  - share groups
  - Kafka Queues
  - Queues for Kafka
  - QfK
  - WarpStream
  - diskless Kafka
  - AutoMQ
  - KIP-1150
  - Kafka protocol
  - Kafka API
  - Kafka-compatible
  - Databricks Zerobus
  - Snowflake Datastream
  - AMQP
  - JMS
  - MQTT
  - messaging protocol comparison
  - head-of-line blocking
  - zero-copy
  - sendfile
  - consumer offset
  - rebalancing
  - acks
tags:
  - corpus/data-engineering
  - entity
created: 2026-05-21
updated: 2026-08-10
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

## Queues for Kafka (QfK) — native message queuing in Kafka 4.2

Kafka was designed for pub/sub streaming, not for point-to-point message queuing: once a consumer group processes a partition, that message is not delivered to other consumers in the same group. Traditional message queues (IBM MQ, RabbitMQ, Amazon SQS) consume messages destructively — one consumer, one message. Kafka's retention-based model was incompatible with that pattern [^qfk1].

**Queues for Kafka (QfK)**, GA in Apache Kafka 4.2, adds Share Groups: a new group type where each message is delivered to exactly one consumer, independent of partition ownership. A topic becomes a task queue while retaining Kafka's durability, scalability, and ecosystem — multiple consumer groups and share groups can coexist on the same topic [^qfk1].

### When to use QfK

- **Task queues / worker pool processing** — backend jobs distributed across many workers; one message, one consumer
- **Parallel processing with dynamic scaling** — add/remove consumers without rebalancing partitions; multiple consumers can process the same partition in parallel (impossible with traditional consumer groups)
- **Lightweight point-to-point delivery** — when fan-out or replay aren't needed but Kafka durability and ecosystem are valuable [^qfk1]

**Critical constraint:** QfK requires that messages can be consumed independently — ordering guarantees are not preserved. This is a deal-breaker for many systems (see head-of-line blocking tradeoff above) [^qfk1].

### When NOT to use QfK (Kafka 4.2)

| Scenario | Why QfK fails | Better option |
|---|---|---|
| Strict message ordering required | QfK doesn't preserve ordering | Kafka Consumer Groups |
| Exactly-once semantics (EOS) | QfK lacks transaction API support | Kafka transaction APIs or IBM MQ (XA) |
| Request/reply communication | Kafka requires design effort for this | REST APIs or dedicated MQ |
| Legacy protocols (JMS, AMQP, MQTT) | QfK doesn't support these | Kafka Connect bridges or native brokers |
| Analytical workloads (windowing, enrichment) | QfK is for operational, not analytical | Kafka Streams, Apache Flink, Spark |

[^qfk1]

These limitations reflect the initial GA release; QfK's roadmap targets many of them in future releases [^qfk1].

### Enterprise QfK (Confluent)

Confluent Cloud offers QfK as a fully managed, consumption-based service with enterprise extensions: RBAC, data lineage, audit logging, Share Group metrics, and integration with Stream Catalog + Control Center [^qfk1].

## Diskless Kafka: object-storage-native event streaming

Classic Kafka couples compute and storage: every broker stores partition replicas on local disk. This creates two pain points in the cloud: (1) you can't scale compute and storage independently, and (2) inter-AZ replication traffic is expensive during traffic spikes [^disk1].

**Diskless Kafka** removes brokers entirely and stores all data directly in cloud object storage (S3), using the Kafka protocol as the compatibility layer. Stateless compute nodes serve the Kafka API; durability is delegated to S3, which already provides multi-AZ redundancy — replication is eliminated [^disk1].

### Robinhood case study: WarpStream for log analytics

Robinhood processes >10 TB/day across microservices, trading systems, and 250+ Flink apps. Its logging workloads followed predictable market-hours traffic patterns: peak at trading time, near-zero at night/weekends. Provisioning for peak meant idle capacity most of the time [^disk1].

Migration from open-source Kafka to **WarpStream** (diskless Kafka, BYOC model) for log analytics produced:

- **45% total cost reduction**
- **99% inter-AZ networking savings** (no broker-to-broker replication)
- **36% lower compute costs**
- **13% lower storage costs** [^disk1]

The elasticity of stateless compute — scaling up for market hours, down overnight — was the primary driver. Robinhood's mission-critical trading flows still run on Confluent's managed Kafka; WarpStream handles log analytics and observability, where latency tolerance is higher [^disk1].

### Diskless Kafka tradeoffs

Object storage introduces higher read/write latency than local disk — diskless Kafka suits **asynchronous or analytical workloads** (log analytics, observability, long-term retention, batch reads). Ultra-low-latency transactional workloads may still require broker-local storage. WarpStream's integration with Amazon S3 Express One Zone narrows this gap for many real-time use cases [^disk1].

**Vendors and proposals:**
- WarpStream (Confluent-acquired): in production, BYOC model, object storage native
- AutoMQ, Aiven, Slack: active KIPs (KIP-1183, KIP-1150, KIP-1176) — different approaches to modernizing storage
- Confluent Freight Clusters: production-stage, separate cluster type from main Confluent platform [^disk1]

## MCP, REST, and Kafka: architectural decision framework

MCP, REST/HTTP APIs, and Apache Kafka are not alternatives — they solve different problems at different layers [^mcp1]:

| Technology | Layer | Designed for |
|---|---|---|
| Apache Kafka | Data backbone | High-volume event streaming, pub/sub, decoupling, consistency at scale |
| REST/HTTP API | Synchronous integration | Direct, moderate-volume, latency-sensitive API calls |
| MCP | Agent tool access | Standardized, discoverable tool interface for AI agents |

The key test for MCP: **does it matter if the data is a few seconds or minutes old?** If yes, MCP should not own that responsibility. If no, MCP is the right interface [^mcp1].

### When Kafka is the right choice

- Data is high-volume or high-velocity
- Multiple consumers need the same events independently
- Ordering and exactly-once delivery matter
- Same events must feed operational apps, analytics, data lakes, and AI agents simultaneously
- Governance, lineage, and auditability are non-negotiable [^mcp1]

### The real-time context engine pattern

The most powerful pattern combining Kafka and MCP: Kafka + Flink govern and process operational data, producing current materialized views; those views are exposed to AI agents through MCP. The consistency guarantee comes from the streaming layer, not from MCP [^mcp1].

> "An agent routing shipments from yesterday's inventory, approving transactions against a risk score from three hours ago, or reading an account balance that has not propagated: none of these is reliable." [^mcp1]

See [Shift Left Architecture](/data-engineering/shift-left-architecture.md) for the broader three-interface pattern. See [MCP](/ai-engineering/mcp.md) for the agent protocol details.

## Kafka as the enterprise event-driven integration backbone

Beyond a single pipeline's transport layer, Kafka has become "the de facto standard for event-driven integration at enterprise scale" — the architectural commitment to events (not scheduler cadence) as the primary integration primitive, ensuring decoupling, scalability, and data consistency across real-time and batch systems [^src8]. Process-orchestration engines have followed the same shift: Camunda's **Zeebe** is itself an event-driven engine, letting organizations implement event-driven workflows without Kafka as a prerequisite; for broader enterprise integration, Kafka complements the orchestration layer, connecting the full landscape of operational systems, SaaS platforms, and data infrastructure into one event-driven backbone [^src8]. Core SaaS platforms have added eventing/CDC interfaces alongside their traditional request-response APIs — SAP S/4HANA, Salesforce CRM, and ServiceNow are named examples — signaling that even systems designed around synchronous HTTP are moving toward event-driven models [^src8]. See [Process Intelligence](/data-engineering/process-intelligence.md) for how this event layer pairs with process orchestration and agentic AI guardrails.

## Kafka as a Streaming Platform — the canonical framing (Stopford 2018)

*Designing Event-Driven Systems* (Ben Stopford, O'Reilly 2018) is the canonical reference for what Kafka really is and is not [^eds-p01]:

- **Not REST-async**: Kafka's home ground is persistent, replayable event streams shared across many services — not point-to-point request-response [^eds-p01].
- **Not an ESB**: unlike traditional enterprise service buses that encourage central orchestration and schema management, Kafka's mantra is the opposite: "Centralize an immutable stream of facts. Decentralize the freedom to act, adapt, and change." [^eds-p01]
- **Not a database (but database-like)**: Kafka provides storage, a SQL interface (KSQL), and transactions, but it is optimized for continuous computation and data movement — "a database inside out." The database's components (commit log, query engine, indexes, caches) are unbundled and distributed: Kafka is the commit log; Kafka Streams/KSQL creates the indexes and views wherever they are needed [^eds-p01].

The book argues that Kafka enables a shift from shared databases (tight coupling) to a shared event log (loose coupling + a central source of truth). Services derive their own private read models from the log, keeping data local while staying synchronized with the organization's facts. See [Designing Event-Driven Systems (source)](/data-engineering/sources/designing-event-driven-systems.md) for the full treatment including Event Sourcing, CQRS, exactly-once semantics, and schema evolution.

## Confluent: from startup to IBM acquisition

Confluent was founded in 2014 by Jay Kreps, Neha Narkhede, and Jun Rao — the original creators of Apache Kafka at LinkedIn. When Kai Waehner joined in 2017, Confluent had ~100 employees and Kafka was still widely misunderstood as "just a fast message broker" [^conf1].

By the IBM acquisition in early 2026 (announced December 2025, enterprise value $11 billion), Confluent had crossed $1.12B in annual revenue, with Confluent Cloud alone at $624M and ~1,500 customers spending >$100K/year [^conf1]. Apache Kafka went from 2017 niche to 150,000+ organizations — the de facto standard for data streaming [^conf1].

Confluent's technology arc [^conf1]:
- **Kafka** itself evolved from a log used for ingestion to a complete infrastructure layer: Connect (hundreds of connectors), Streams, exactly-once semantics, tiered storage, diskless (WarpStream), Queues for Kafka (QfK)
- **Apache Flink** became the platform's stream processing layer for stateful computation at scale
- **Apache Iceberg** added an open table format layer connecting streaming with lakehouse + AI data pipelines
- **WarpStream** (Confluent-acquired) delivers BYOC object-storage-native Kafka

Confluent deployed everywhere: fully serverless cloud, BYOC (WarpStream), self-managed on-prem, and edge (factory floors, retail stores) [^conf1]. Forrester's 2023 Streaming Data Platforms Wave named Confluent a leader alongside Microsoft and Google — establishing data streaming as its own recognized software category, not a subset of message queues or iPaaS [^conf1].

**IBM acquisition logic**: IBM brings global enterprise reach and large-deal expertise; Confluent fills a gap in IBM's portfolio. Integration with IBM's broader product stack is the next challenge [^conf1].

## Kafka protocol vs Kafka framework

The explosion of "Kafka-compatible" services (Databricks Zerobus Ingest, Snowflake Datastream, Redpanda, WarpStream) reflects a fundamental split [^dbs1]:

- **Kafka API / Kafka protocol** — the open wire protocol (Apache 2.0 license). Defines how clients talk to brokers: requests, binary format, rules. Anyone can implement against it.
- **Kafka framework** — the actual open-source software: brokers, Kafka Connect, Kafka Streams. One implementation of the protocol.

When Databricks or Snowflake say "Kafka-compatible," they mean existing Kafka producers can stream into their platform with a config change — no code changes. This is the ingestion use case. It is **not** the same as running Kafka as an enterprise event-driven backbone [^dbs1].

**Ingestion vs architecture** [^dbs1]: The most common production pattern is both:
1. Kafka as the **operational backbone** — event-driven architecture, CDC from operational systems, real-time pipelines
2. A lakehouse connector as the **analytics sink** — Kafka Connect pipes events into Databricks/Snowflake for analytics and ML training

Kafka-compatible ingestion in analytics platforms does NOT replace Kafka as an architecture; it adds a clean consumption path from it [^dbs1].

**Kafka as four things** [^dbs1]: messaging (pub-sub) + storage (durable replayable commit log — events persist, not deleted on consumption) + Kafka Connect (integration framework) + Kafka Streams (stream processing). The persistent log is what makes Kafka a system of record for events, not just a pipe.

## AMQP, JMS, Kafka, MQTT: trade-offs (not a winner)

The protocols address different operational models [^msg1]:

| Protocol | What it is | Model | Best for |
|---|---|---|---|
| **MQTT** | Wire protocol (OASIS) | Pub-sub, persistent sessions, QoS 0/1/2 | Device/IoT edge, constrained hardware, metered links |
| **AMQP** (1.0) | Wire protocol (ISO/IEC 19464) | Reliable message routing with exchanges/queues | Enterprise B2B, financial messaging (JPMorgan origin) |
| **JMS** (Jakarta) | Java API (not wire protocol) | Provider-agnostic Java messaging abstraction | Java/EE environments; swaps providers in theory |
| **Kafka** | Distributed platform | Append-only log, consumer-offset replay, platform (4 capabilities) | Event streaming backbone, high-throughput, replay, fan-out |

Key distinctions [^msg1]:
- **AMQP 0.9.1 ≠ AMQP 1.0** — wire-incompatible protocols. RabbitMQ ≥4.0 supports 1.0 natively; Azure Service Bus and IBM MQ use 1.0.
- **JMS is an API, not a protocol** — the wire underneath is vendor-specific; swapping providers is a migration, not a drop-in.
- **Kafka + Queues for Kafka (QfK)** — Kafka now supports queue-style consumption (Share Groups), so the "Kafka is only pub-sub" objection is increasingly moot.
- **A single platform often speaks several**: Confluent runs Kafka and MQTT for edge ingestion; IBM MQ runs JMS + AMQP for enterprise messaging.

The tools are borrowing each other's features (RabbitMQ added a log; AMQP standards committee reconvened for agentic AI workloads) but **their underlying storage models and delivery guarantees have not merged** — that is still what drives the choice [^msg1].

## See also

- [Idempotent Pipelines](/data-engineering/idempotent-pipelines.md) — append-only stream ingestion with at-most-once settings
- [Stream Processing](/data-engineering/stream-processing.md) — Kafka as the transport layer in real-time pipelines
- [Storage Fundamentals](/data-engineering/storage-fundamentals.md) — the object-storage trend (tiered/diskless Kafka) builds on the object-storage layer covered there
- [Process Intelligence](/data-engineering/process-intelligence.md) — event-driven integration as one of three converged architecture layers
- [Shift Left Architecture](/data-engineering/shift-left-architecture.md) — three-interface pattern using Kafka as the streaming backbone
- [MCP](/ai-engineering/mcp.md) — the agent tool-access interface that pairs with Kafka's streaming layer
- [Data Engineering hub](/data-engineering/README.md)

---

[^src1]: [Kafka Tutorial for Beginners - Core Concepts](/03_Resources/Study Notes/Kafka Tutorial for Beginners - Core Concepts.md)
[^src2]: [Can Kafka Queues Make Consumers Faster? Part 2: Head-Of-Line Blocking](../../raw/web/can-kafka-queues-make-consumers-faster-part-2-head-of-line-b.md)
[^src3]: [Kafka Share Groups and Parallelizing Consumption — Part 1: Tuning max.poll.records](../../raw/web/kafka-share-groups-and-parallelizing-consumption-part-1-tuni.md)
[^src4]: [Introducing Dimster, a performance benchmarking tool for Apache Kafka](../../raw/web/introducing-dimster-a-performance-benchmarking-tool-for-apac.md)
[^src5]: [TLDR Data — Kafka Queues / Head-of-Line Blocking (newsletter origin)](../../raw/email/email-2026-05-14-duckdb-goes-remote-when-lakehouses-guess-netflix-tames-data.md)
[^src6]: [TLDR Data — Kafka's New Bottleneck / Share Groups (newsletter origin)](../../raw/email/email-2026-05-28-slashing-snowflake-costs-open-source-agent-tradeoffs-kafkas.md)
[^src7]: [If you're learning Kafka, this article is for you (Vu Trinh)](../../raw/email/email-2025-05-15-if-you-re-learning-kafka-this-article-is-for-you.md)
[^src8]: [The Trinity of Modern Data Architecture: Process Intelligence, Event-Driven Integration, and Trusted Agentic AI](../../raw/web/web-the-trinity-of-modern-data-architecture-process-intelligence-b19b93a7.md)
[^eds-p01]: [Designing Event-Driven Systems (part 1/6)](../../raw/pdf/pdf-designing-event-driven-systems-concepts-and-patter-part-01.md)
[^qfk1]: [When (Not) to Use Queues for Kafka?](../../raw/web/web-when-not-to-use-queues-for-kafka-9296826b.md) — Kai Waehner, kai-waehner.de, 2026-01-28
[^disk1]: [Diskless Kafka at FinTech Robinhood for Cost-Efficient Log Analytics and Observability](../../raw/web/web-diskless-kafka-at-fintech-robinhood-for-cost-efficient-log-a-0ec9eb53.md) — Kai Waehner, kai-waehner.de, 2026-01-22
[^mcp1]: [MCP vs. REST/HTTP API vs. Kafka: The Architect's Guide to Agentic AI Integration](../../raw/web/web-mcp-vs-rest-http-api-vs-kafka-the-architect-s-guide-to-agent-e36f1d1c.md) — Kai Waehner, kai-waehner.de, 2026-04-10
[^conf1]: [My Confluent Chapter: From Apache Kafka Startup to $11 Billion IBM Acquisition (Kai Waehner)](../../raw/web/web-my-confluent-chapter-from-apache-kafka-startup-to-11-billion-9dcd0637.md)
[^dbs1]: [Why Databricks and Snowflake Speak the Kafka Protocol: Ingestion vs. Architecture (Kai Waehner)](../../raw/web/web-why-databricks-and-snowflake-speak-the-kafka-protocol-ingest-b83e18be.md)
[^msg1]: [When to Use AMQP, JMS, Kafka, or MQTT: Trade-offs, Not a Winner (Kai Waehner)](../../raw/web/web-when-to-use-amqp-jms-kafka-or-mqtt-trade-offs-not-a-winner-7db4e92a.md)

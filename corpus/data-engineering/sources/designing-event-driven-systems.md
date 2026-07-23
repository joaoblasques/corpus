---
type: source
domain: data-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-designing-event-driven-systems-concepts-and-patter-part-01.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-designing-event-driven-systems-concepts-and-patter-part-02.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-designing-event-driven-systems-concepts-and-patter-part-03.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-designing-event-driven-systems-concepts-and-patter-part-04.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-designing-event-driven-systems-concepts-and-patter-part-05.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-designing-event-driven-systems-concepts-and-patter-part-06.md
    channel: pdf
    ingested_at: 2026-07-23
aliases:
  - Designing Event-Driven Systems
  - Ben Stopford
  - event-driven systems book
  - EDS
tags:
  - corpus/data-engineering
  - source
created: 2026-07-23
updated: 2026-07-23
---

# Designing Event-Driven Systems (Stopford, O'Reilly 2018)

**TL;DR**: The canonical O'Reilly reference on building event-driven and streaming services with Apache Kafka. Argues that Kafka is not merely a message broker but a "streaming platform" — a replayable log that acts as a shared source of truth, enabling Event Sourcing, CQRS, and the "database inside out" pattern at company scale. The core mantra: "Centralize an immutable stream of facts. Decentralize the freedom to act, adapt, and change." [^eds-p01]

## Book Structure

The book is organized into five parts [^eds-p01]:

- **Part I — Setting the Stage**: Introduces Kafka and stream processing; corrects common misconceptions (not REST, not ESB, not a database).
- **Part II — Designing Event-Driven Systems**: Event collaboration, stateful functions, Event Sourcing, CQRS, and materialized views.
- **Part III — Rethinking Architecture at Company Scales**: Shared data across organizations, the data dichotomy, event streams as a shared source of truth, lean data.
- **Part IV — Consistency, Concurrency, and Evolution**: Eventual consistency, the single writer principle, Kafka transactions (exactly-once semantics), schema evolution.
- **Part V — Implementing Streaming Services with Kafka**: Kafka Streams API, KSQL, and a worked order-validation ecosystem example with code.

## Core Concepts

### Commands, Events, and Queries

Three distinct ways programs interact over a network [^eds-p02]:

| Type | Behavior | Response |
|---|---|---|
| **Command** | Requests a state change | Maybe |
| **Event** | Records what happened | Never |
| **Query** | Looks something up | Always |

Events "wear two hats": a **notification hat** (triggers services into action) and a **replication hat** (copies data from one service to another). Events lead to less coupling than commands and queries — they express facts, not instructions [^eds-p02].

### Event Collaboration

A choreography pattern where a set of services collaborate around a single business workflow, each doing its part by listening to events and creating new ones. No single service owns the whole process; each owns a small part — some subset of state transitions [^eds-p02]. The resulting event log forms "a shared narrative describing exactly how your business evolved over time." [^eds-p02]

Choreography (no central control) suits larger multi-team systems. Orchestration (one controller) is easier to reason about but creates coupling to the controller [^eds-p02].

### Event Sourcing and Command Sourcing

**Event Sourcing**: every state change is stored immutably in a log, in the order it occurred. The current state can always be rederived by replaying the log. Analogous to version control for data — "Accountants don't use erasers." [^eds-p03]

**Command Sourcing**: the original *input* (not just the resulting state change) is also stored, enabling full rewind-and-replay from the raw commands [^eds-p03].

Key benefit: when a bug introduces data corruption, fix the bug, rewind the log to before the corruption, and replay — the database is automatically overwritten with correct values and corrected events are published downstream [^eds-p03].

### CQRS (Command Query Responsibility Segregation)

Separates the **write path** (events journaled to Kafka) from the **read path** (event-sourced views derived from the log), linked by an asynchronous channel [^eds-p03]. Writes are fast (append to log). Read models are updated asynchronously, so they can be optimized independently.

Trade-off: because the read model updates asynchronously, a user may not immediately "read their own writes." A blocking read (long polling) can collapse this asynchrony where needed [^eds-p06].

### Materialized Views

A close analogue to materialized views in relational databases: a precomputed query stored and kept up to date as the underlying event stream changes [^eds-p03]. With CQRS and Kafka, you can have many materialized views, each optimized for a different use case, all derived from the same event stream [^eds-p03].

### Polyglot Views

Because a replayable log allows bootstrapping any view from the same source of truth, different services can maintain their own read models in the most appropriate database technology — key/value store, search engine, columnar store — without coupling to a shared schema [^eds-p03].

### Lean Data

Rather than collecting and curating large datasets, services maintain small, targeted views containing only the data they need. If the messaging layer remembers (via the log), downstream databases don't have to store everything reliably — they can be dropped and rederived from the log [^eds-p04].

The pattern is analogous to immutable infrastructure in DevOps: deterministic, rebuild-from-source, no snowflake databases drifting over time [^eds-p04].

### The Data Dichotomy

Services want to hide data (to stay loosely coupled); databases want to expose data (to be useful). This tension drives a cyclical pattern: teams centralize data → teams extract copies and go independent → data quality degrades → teams recentralize [^eds-p04].

The solution: treat **data on the outside** (data services share) as a first-class citizen, held in a replayable log, not a shared database. "Messaging turns highly coupled, shared datasets into data a service can own and control. Replayable logs go a step further by adding a central reference." [^eds-p04]

### The Database Inside Out

Coined by Martin Kleppmann, extended by Jay Kreps [^eds-p04]. A traditional database bundles: commit log + query engine + indexes + caching. Stream processing unbundles these:

- Kafka = the commit log
- Kafka Streams/KSQL = indexes/views
- Views live inside or close to the application = continuously updated cache

The result: one shared event stream can feed many specialized views across the organization, each tuned to a team's use case. "If you squint a bit, you can see the whole of your organization's systems and data flows as a single distributed database." (Jay Kreps, 2013) [^eds-p04]

### Exactly-Once Semantics

Kafka's transactions provide exactly-once processing for service-to-service communication through Kafka [^eds-p05]:

- **Idempotence** in the broker: each producer+message gets a unique sequence number; duplicates in the log are discarded at write time.
- **Atomic commit**: sending to multiple topics and committing offsets is wrapped in a single transaction — either all succeed or none do.
- **State store atomicity**: in Kafka Streams, writes to state stores and writes to output topics are wrapped in the same transaction — ties storage and messaging atomically without XA.

Transactions do not cover calls to external services (HTTP, external databases). For cross-service transactions, use sagas [^eds-p05].

### Schema Evolution

Schemas are the APIs of event-driven services [^eds-p05]. Best practices:

- Use Avro with the Confluent Schema Registry for backward-compatible evolution.
- Additive changes (new fields) are backward-compatible; removing/moving fields is not.
- **Dual Schema Upgrade Window**: for breaking changes, maintain two topics (v1, v2) simultaneously, giving services time to migrate. A Kafka Streams job can down-convert or up-convert between schemas automatically [^eds-p05].
- Use GitHub pull requests for schema change collaboration: version-controlled, reviewable, auditable [^eds-p05].

### Kafka Streams and KSQL

Kafka Streams is a JVM library for stateful stream processing [^eds-p06]:

- **Streams** (KStreams): infinite sequence of events, processed one record at a time.
- **Tables** (KTables / Global KTables): a whole dataset materialized locally in a state store; behaves like a database table. KTables are partitioned (scale-out); Global KTables are broadcast (full copy on every node, enables foreign-key joins).
- **State stores**: disk-resident hash tables backed by Kafka topics — durable local storage that participates in Kafka transactions.

The core streaming pattern is **Join → Filter → Process**: join streams/tables, filter what isn't needed, execute business logic, push output to a new stream [^eds-p06].

KSQL provides a SQL-like interface to Kafka Streams, runnable as a sidecar for non-JVM services [^eds-p06].

### The Single Writer Principle

To avoid collisions in eventually consistent systems, assign a single service as the sole writer for each type of data (topic). This isolates consistency logic, simplifies schema upgrades, and enables clean ownership [^eds-p05]. Variants: command topic (separate topic for initiating commands vs. state-change events) and single writer per transition (each service owns specific state transitions within a shared topic) [^eds-p05].

## Key Claims

- "Kafka is a streaming platform … its home ground is event-based communication, where events are business facts that have value to more than one service." [^eds-p01]
- "The core mantra of event-driven services: Centralize an immutable stream of facts. Decentralize the freedom to act, adapt, and change." [^eds-p01]
- Event Sourcing "ensures every state change in a system is recorded, much like a version control system." [^eds-p03]
- "If an event stream is the source of truth, you can have as many different views in as many different shapes, sizes, or technologies as you may need." [^eds-p03]
- Lean data: "If messaging remembers, derived views can be refined to contain only the data that is absolutely necessary. You can always go back for more." [^eds-p04]
- On exactly-once: Kafka transactions "free you from the worries of failure and retries in a distributed world — worries that really should be a concern of the infrastructure, not of your code." [^eds-p05]
- "Stateful stream processors, like Kafka's Streams API, are proudly stateful. They make data available wherever it is required." [^eds-p03]

## Related Corpus Pages

- [Apache Kafka](/data-engineering/kafka.md) — entity page covering Kafka internals, producer/consumer protocols, share groups, and the enterprise event-driven backbone
- [Stream Processing](/data-engineering/stream-processing.md) — concept page covering batch vs stream, delivery guarantees, engines (Flink/Kafka Streams/Spark SS), and scaling

---

[^eds-p01]: [Designing Event-Driven Systems (part 1/6)](../../../raw/pdf/pdf-designing-event-driven-systems-concepts-and-patter-part-01.md)
[^eds-p02]: [Designing Event-Driven Systems (part 2/6)](../../../raw/pdf/pdf-designing-event-driven-systems-concepts-and-patter-part-02.md)
[^eds-p03]: [Designing Event-Driven Systems (part 3/6)](../../../raw/pdf/pdf-designing-event-driven-systems-concepts-and-patter-part-03.md)
[^eds-p04]: [Designing Event-Driven Systems (part 4/6)](../../../raw/pdf/pdf-designing-event-driven-systems-concepts-and-patter-part-04.md)
[^eds-p05]: [Designing Event-Driven Systems (part 5/6)](../../../raw/pdf/pdf-designing-event-driven-systems-concepts-and-patter-part-05.md)
[^eds-p06]: [Designing Event-Driven Systems (part 6/6)](../../../raw/pdf/pdf-designing-event-driven-systems-concepts-and-patter-part-06.md)

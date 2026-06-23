---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/email/email-2025-05-25-week-23-34-real-time-processing-for-data-engineering-intervi.md
    channel: email
    ingested_at: 2026-06-19
  - path: raw/email/email-2025-05-22-how-to-choose-between-batch-and-stream-processing.md
    channel: email
    ingested_at: 2026-06-19
aliases:
  - stream processing
  - real-time processing
  - streaming
  - batch vs stream
  - batch processing
  - micro-batch
  - microbatch
  - event time
  - watermark
  - delivery guarantees
  - exactly-once
  - Lambda architecture
tags:
  - corpus/data-engineering
  - concept
created: 2026-06-19
updated: 2026-06-23
---

# Stream Processing (and Batch vs Stream)

**TL;DR.** **Batch processing** collects data over a period and processes it all at once on a schedule (completeness over speed, easy to test); **stream processing** handles data as it arrives, within ms–s (real-time insight, harder to operate) [^src2]. The decisive question is *not* which is trendier but **whether the use case actually needs low latency** — "just because something *can* be done in real time doesn't mean it *should* be" [^src1]. Most real-world pipelines, especially at small/mid-size companies, are **batch or micro-batch**; true streaming is reserved for fraud detection, live recommendations, ad-tech/clickstream, and IoT [^src1][^src2].

## Batch vs stream

| | Batch | Stream |
|---|---|---|
| **Unit** | Large volume at once | One record / small window at a time |
| **Cadence** | Scheduled or triggered (hourly/daily) | Continuous, minimal delay |
| **Priority** | Completeness & consistency | Timeliness & reaction |
| **Ops** | Easier to test/debug | Must handle out-of-order / late data |
| **Use cases** | Daily dashboards, backfills, lake→warehouse transfers | Alerts, event-driven microservices, personalization, IoT |

[^src1][^src2]

**Micro-batch** is the practical middle ground: a job every few minutes (e.g. Spark Structured Streaming, or Airflow on a short schedule) often meets the SLA without full streaming complexity [^src2]. The **Lambda architecture** is the classic hybrid — streaming for real-time, batch for periodic reprocessing/accuracy — though it is seen less in practice today [^src2].

## When you actually need real-time

Most general-purpose analytics and DE use cases are served fine by batch/micro-batch — simpler, cheaper, easier to maintain [^src2]. Real-time is typically reserved for [^src1][^src2]:

- Financial institutions — fraud detection within seconds.
- E-commerce — real-time product recommendations.
- Ad-tech / marketing — clickstream tracking in near real-time.
- IoT — monitoring/reacting to sensor data instantly.

Teams that jump into real-time without a clear need struggle with debugging, cost overruns, and unclear business value [^src1].

## Core concepts

Terms that recur in streaming systems (and interviews) [^src1]:

- **Latency** — time from event source to final output; keep it low.
- **Throughput** — events handled per second/minute.
- **Backpressure** — the system can't keep up with incoming data; shows as lagging consumers / growing queues.
- **State** — running totals / last-N-events the system must remember; correct state management is key to consistency and fault tolerance in distributed systems.
- **Event time vs processing time** — when the event *happened* vs when the system *processes* it. Delay between the two (network issues) must be handled, especially in aggregations and windowed calculations.

**Real-time ≠ distributed stream processing** [^src1]: real-time on a single system works for small scale/prototypes; real systems at scale use **distributed stream processing** across many machines (partitioning, replication, node coordination) for scalability and fault tolerance.

## Tooling

Streaming splits into a **messaging/transport** layer, a **processing engine**, and a **sink** [^src2]:

- **Messaging & transport** — **[[data-engineering/kafka|Apache Kafka]]** (industry standard, high-throughput, durable, replayable; the most-asked tool in real-time DE interviews), **AWS Kinesis**, **GCP Pub/Sub**, **Azure Event Hubs** [^src1][^src2].
- **Processing engines** — **Apache Flink** (stateful, event-time, windowing, watermarks), **Kafka Streams** (lightweight JVM library over Kafka topics), **Spark Structured Streaming** (familiar Spark APIs, micro-batch or continuous), **Apache Storm** (older spouts/bolts topology, legacy) [^src1][^src2].
- **Batch tools (for contrast)** — warehouse SQL engines ([[data-engineering/snowflake|Snowflake]]/[[data-engineering/bigquery|BigQuery]]/[[data-engineering/redshift|Redshift]]/Databricks SQL), **[[data-engineering/dbt|dbt]]** (transformation), **[[data-engineering/apache-spark|Apache Spark]]** (large-scale batch), Pandas/Polars (small-scale); orchestrated by **[[data-engineering/data-orchestration|Airflow, Dagster, or Prefect]]** [^src2].

## Delivery guarantees

A core interview topic — pick by the business cost of duplicates vs loss [^src1]:

- **At-most-once** — each event processed ≤ once; may lose data on failure. Only when occasional loss is acceptable.
- **At-least-once** — every event processed, but retries may produce **duplicates** → need downstream deduplication.
- **Exactly-once** — processed once and only once even under failure; needs checkpointing + transactional writes → more complex, more overhead.

For financial transactions, lean **exactly-once** (or solid at-least-once with idempotent/dedup sinks) — the risk of double-processing or missing a transaction is too high [^src1]. This is the streaming analogue of [[data-engineering/idempotent-pipelines|idempotent pipelines]] in batch.

## Choosing the right method

Best practices: *start simple, optimize only when necessary, let the use case drive the architecture* [^src2]:

1. **Start from the business requirement** — how fresh must the data be? What's the cost of a 10-min / 1-hour delay? Clarifies whether real-time is needed or just "nice to have" [^src2].
2. **Consider team maturity** — streaming needs deeper engineering (monitoring, alerting); early teams should start batch and evolve [^src2].
3. **Choose hybrid where it helps** — stream for recent insight, batch to validate/backfill/reprocess (e.g. serve ML features from streaming, retrain nightly from batch) [^src2].
4. **Don't optimize prematurely** — building real-time too early adds unnecessary complexity and cost [^src2].

## Worked example: a real-time pipeline on AWS

A minimal IoT pipeline from the source [^src1]: a Python script simulates temperature sensors emitting readings every second → **Amazon Kinesis Data Stream** (ingestion buffer) → **AWS Lambda** (real-time processing engine, triggered per record) → **Amazon DynamoDB** (NoSQL store of the latest reading per device); optionally an **SNS** alert on threshold breach [^src1]. Resources are provisioned with **[[mlops/terraform|Terraform]]** (`providers.tf`, `kinesis.tf`, `dynamodb.tf`, `iam.tf`, `lambda.tf`, `outputs.tf`) [^src1].

## Interview questions (real-time)

- **Late-arriving events on a Kafka topic** → process by **event time** with a framework supporting **watermarks** (e.g. Flink); define a lateness bound (e.g. 10 min), include late events in the right window, and route too-late events to a side output for backfill/audit [^src1].
- **Real-time dashboard missing updates** → check **consumer lag** first, then throughput/backpressure, then a heavy transform or slow sink; keep metrics/alerts on processing latency, throughput, and failures [^src1].
- **Fraud detection with a 3-second SLA** → Kafka for ingest + Flink for stateful low-latency processing; avoid external DB lookups in the hot path (load reference data into memory/Flink state); decouple alerting to a separate topic [^src1].

## Related

- [[data-engineering/kafka|Apache Kafka]] — the dominant transport layer; producer/consumer internals
- [[data-engineering/etl-pipeline|ETL Pipeline]] — batch vs real-time extraction; ETL vs ELT
- [[data-engineering/data-ingestion-patterns|Data Ingestion Patterns]] — stream-via-event-log vs batch-extract
- [[data-engineering/data-orchestration|Data Orchestration]] — scheduling batch/micro-batch jobs
- [[data-engineering/idempotent-pipelines|Idempotent Pipelines]] — the batch analogue of exactly-once
- [[data-engineering/apache-spark|Apache Spark]] — Spark Structured Streaming is one of the named processing engines
- [[data-engineering/databricks|Databricks]] — runs Spark Structured Streaming / Lakeflow for streaming + micro-batch
- [[data-engineering/data-engineering-interview|Data Engineering Interview]] — event streaming is a tested skill
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [Week 23/34: Real-Time Processing for Data Engineering Interviews (Pipeline to Insights)](../../raw/email/email-2025-05-25-week-23-34-real-time-processing-for-data-engineering-intervi.md)
[^src2]: [How to Choose Between Batch and Stream Processing? (Pipeline to Insights)](../../raw/email/email-2025-05-22-how-to-choose-between-batch-and-stream-processing.md)

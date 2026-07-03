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
  - path: raw/pdf/pdf-chapter3-intro-to-real-time-streaming.md
    channel: pdf
    ingested_at: 2026-06-25
  - path: raw/pdf/pdf-chapter4-popular-streaming-systems.md
    channel: pdf
    ingested_at: 2026-06-25
  - path: raw/pdf/pdf-chapter1-intro-to-batch-processing.md
    channel: pdf
    ingested_at: 2026-06-25
  - path: raw/pdf/pdf-chapter2-intro-to-event-based-computing.md
    channel: pdf
    ingested_at: 2026-06-25
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
  - event-based computing
  - event-driven
  - queuing
  - vertical scaling
  - horizontal scaling
  - embarrassingly parallel
tags:
  - corpus/data-engineering
  - concept
created: 2026-06-19
updated: 2026-06-25
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

- **Messaging & transport** — **[Apache Kafka](/data-engineering/kafka.md)** (industry standard, high-throughput, durable, replayable; the most-asked tool in real-time DE interviews), **AWS Kinesis**, **GCP Pub/Sub**, **Azure Event Hubs** [^src1][^src2].
- **Processing engines** — **Apache Flink** (stateful, event-time, windowing, watermarks), **Kafka Streams** (lightweight JVM library over Kafka topics), **Spark Structured Streaming** (familiar Spark APIs, micro-batch or continuous), **Apache Storm** (older spouts/bolts topology, legacy) [^src1][^src2].
- **Batch tools (for contrast)** — warehouse SQL engines ([Snowflake](/data-engineering/snowflake.md)/[BigQuery](/data-engineering/bigquery.md)/[Redshift](/data-engineering/redshift.md)/Databricks SQL), **[dbt](/data-engineering/dbt.md)** (transformation), **[Apache Spark](/data-engineering/apache-spark.md)** (large-scale batch), Pandas/Polars (small-scale); orchestrated by **[Airflow, Dagster, or Prefect](/data-engineering/data-orchestration.md)** [^src2].

## Delivery guarantees

A core interview topic — pick by the business cost of duplicates vs loss [^src1]:

- **At-most-once** — each event processed ≤ once; may lose data on failure. Only when occasional loss is acceptable.
- **At-least-once** — every event processed, but retries may produce **duplicates** → need downstream deduplication.
- **Exactly-once** — processed once and only once even under failure; needs checkpointing + transactional writes → more complex, more overhead.

For financial transactions, lean **exactly-once** (or solid at-least-once with idempotent/dedup sinks) — the risk of double-processing or missing a transaction is too high [^src1]. This is the streaming analogue of [idempotent pipelines](/data-engineering/idempotent-pipelines.md) in batch.

## Choosing the right method

Best practices: *start simple, optimize only when necessary, let the use case drive the architecture* [^src2]:

1. **Start from the business requirement** — how fresh must the data be? What's the cost of a 10-min / 1-hour delay? Clarifies whether real-time is needed or just "nice to have" [^src2].
2. **Consider team maturity** — streaming needs deeper engineering (monitoring, alerting); early teams should start batch and evolve [^src2].
3. **Choose hybrid where it helps** — stream for recent insight, batch to validate/backfill/reprocess (e.g. serve ML features from streaming, retrain nightly from batch) [^src2].
4. **Don't optimize prematurely** — building real-time too early adds unnecessary complexity and cost [^src2].

## Worked example: a real-time pipeline on AWS

A minimal IoT pipeline from the source [^src1]: a Python script simulates temperature sensors emitting readings every second → **Amazon Kinesis Data Stream** (ingestion buffer) → **AWS Lambda** (real-time processing engine, triggered per record) → **Amazon DynamoDB** (NoSQL store of the latest reading per device); optionally an **SNS** alert on threshold breach [^src1]. Resources are provisioned with **[Terraform](/mlops/terraform.md)** (`providers.tf`, `kinesis.tf`, `dynamodb.tf`, `iam.tf`, `lambda.tf`, `outputs.tf`) [^src1].

## Interview questions (real-time)

- **Late-arriving events on a Kafka topic** → process by **event time** with a framework supporting **watermarks** (e.g. Flink); define a lateness bound (e.g. 10 min), include late events in the right window, and route too-late events to a side output for backfill/audit [^src1].
- **Real-time dashboard missing updates** → check **consumer lag** first, then throughput/backpressure, then a heavy transform or slow sink; keep metrics/alerts on processing latency, throughput, and failures [^src1].
- **Fraud detection with a 3-second SLA** → Kafka for ingest + Flink for stateful low-latency processing; avoid external DB lookups in the hot path (load reference data into memory/Flink state); decouple alerting to a separate topic [^src1].

## Scaling streaming systems

Streaming performance is constrained by available resources; "real-time" is defined by a **response timeframe guarantee** that must match the speed/cost constraints of those resources [^src3]. Two scaling axes [^src3]:

**Vertical scaling** — upgrade components on a single node (faster CPU, more RAM, more I/O bandwidth). GPU processing accelerates ML/image-intensive streaming. Effect: limited by total single-system capacity; each component contributes differently depending on the workload — **benchmark/test** to identify the bottleneck [^src3].

**Horizontal scaling** — add more nodes. Streaming pipelines have **minimal inter-task delays**, which makes transferring data between workers tricky. Best practice: process a **full event's lifecycle within a single pipeline copy**; scale by running multiple identical pipeline copies. Events enter one pipeline and all tasks for that event complete within it. A **load balancer** (or "card dealer") routes incoming events to the least-busy pipeline [^src3]. Eventually a new bottleneck emerges (e.g. disk write performance at the sink) — consider shortening the pipeline or buffering writes [^src3].

## Messaging failure modes

Distributed streaming systems must handle four types of communication problems [^src3]:

| Problem | Characteristics | Mitigation |
|---|---|---|
| **Missing messages** | Events that never arrive; difficult to detect without a sequence identifier | Sequence IDs; requesting missing messages delays the pipeline |
| **Delayed messages** | Arrive late; often caused by resource contention | Watermark-based event-time processing |
| **Out-of-order messages** | A combination of missing + delayed; older event arrives after a newer one | Sequence/state tracking; handle depends on processing type |
| **Repeat messages** | Same event arrives multiple times (retries, system failure) | Sequence/idempotency handling; sometimes safe to ignore (e.g. temperature readings) |

## Popular streaming tools: Celery, Kafka, Spark Streaming

Three commonly used open-source systems [^src4]:

**Celery** — a distributed **task queue** (FIFO or priority-ordered). Used primarily for **asynchronous task queues**: password reset emails, digital order fulfillment, image resizing. Supports real-time processing of large message volumes, with built-in management and both vertical and horizontal scaling [^src4].

**Apache Kafka** — a distributed **event streaming** platform designed for high-throughput event passing between producers and consumers. Producers publish to **topics**; consumers subscribe and handle events independently (logging, transformation, relay, etc.). Also handles **event storage** with configurable retention. Best used for: single source of truth, change data capture, data backups, system migrations. Extremely powerful but complex to set up [^src4].

**Spark Streaming** — part of **Apache Spark**; designed to process streaming data using the same Spark APIs (Python, Scala, SQL). Strengths: large-scale processing, ML pipelines. Can transition batch→stream fairly easily. Does **not** store or log events — designed for processing/transforming data, not as a durable message bus [^src4].

Choosing between them [^src4]: Celery for background task queues; Kafka as a durable, high-throughput event log/bus between systems; Spark Streaming when you want Spark's processing ecosystem applied to a stream.

## Batch processing fundamentals

Batch processing handles data in **groups** ("batches"), running from start to finish with no data added during the run. Typically triggered by an interval (time-based) or a threshold (size-based) [^src5]. An instance of a batch run is called a **job**.

**Why batch?** Simplicity and consistency are the primary advantages — the data set is bounded and well-defined at run time [^src5]. Multiple strategies can improve performance:

- **Vertical scaling** — upgrade a single node (faster CPU, faster I/O, more memory). Easiest change, lowest complexity, rarely requires algorithm changes. **Cons:** inherently limited by hardware ceiling; can be expensive; improvements are not guaranteed to continue [^src5].
- **Horizontal scaling** — split the task across multiple machines (or CPUs). Best for **"embarrassingly parallel"** tasks — work that can be easily divided among workers with minimal inter-task coordination. A processing framework like Apache Spark or Dask is required. Can yield **near-linear performance improvements** for certain workloads. **Cons:** complexity, networking requirements, ongoing management; non-parallelizable tasks still bottleneck [^src5].

### Batch delay sources

A real-world batch pipeline accumulates at least four types of delay [^src5]:

1. **Waiting on source data** — is all data available? (e.g. machines send logs during low utilization; high utilization suppresses logs)
2. **Waiting on the process** — if processing 100 GB takes 23 hrs and data grows 5%/month, within two months the job takes longer than a day to process one day's data.
3. **Waiting on the data to be available downstream** — collect (1 day) + process (7 hrs) + update systems (5 hrs) + generate report (2 min) = **~1.5 days** total latency even for a "daily" report.

These cumulative delays are the primary motivation for switching to streaming when SLAs require sub-hour freshness.

## Event-based computing

**Event-based processing** doesn't run on a schedule — tasks fire when **an event occurs** (user clicks, file upload, message arrival). This decouples producers from consumers and is the conceptual foundation of streaming systems [^src6].

**Queues** (a.k.a. buffers) sit between event producers and consumers. Properties [^src6]:
- **FIFO** — first in, first out; processing order is preserved.
- **Decoupled** — producers and consumers don't need to run simultaneously.
- **Scalable** — vertically (faster hardware per node) or horizontally (more consumer workers).
- **Failure modes**: bad data / processing errors; data-size variance (burst traffic); difficult to know queue depth; scaling limits.

### Batch vs stream: a quick reference

| Characteristic | Batch | Queue (size=1) | Stream |
|---|---|---|---|
| **Unit of processing** | Groups (N records) | One at a time | Continuous, unbounded |
| **End** | Defined by batch size | N/A | No defined end event |
| **Order** | Not necessarily preserved | FIFO | Maintained |
| **Latency** | High (batch frequency) | Medium | Low |

"**Queues are batches with a batch size of one**" [^src6]. Streams handle data without pausing and are **defined by the flow of data, not the content**.

**Choosing the approach** [^src6]:
- Can tolerate processing in groups + simplicity matters → **batch**
- Need order but can pause → **queue**
- Continuous data / unknown volume / can't stop → **stream**

## Related

- [Apache Kafka](/data-engineering/kafka.md) — the dominant transport layer; producer/consumer internals
- [ETL Pipeline](/data-engineering/etl-pipeline.md) — batch vs real-time extraction; ETL vs ELT
- [Data Ingestion Patterns](/data-engineering/data-ingestion-patterns.md) — stream-via-event-log vs batch-extract
- [Data Orchestration](/data-engineering/data-orchestration.md) — scheduling batch/micro-batch jobs
- [Idempotent Pipelines](/data-engineering/idempotent-pipelines.md) — the batch analogue of exactly-once
- [Apache Spark](/data-engineering/apache-spark.md) — Spark Structured Streaming is one of the named processing engines
- [Databricks](/data-engineering/databricks.md) — runs Spark Structured Streaming / Lakeflow for streaming + micro-batch
- [Data Engineering Interview](/data-engineering/data-engineering-interview.md) — event streaming is a tested skill
- [Data Engineering hub](/data-engineering/README.md)

---

[^src1]: [Week 23/34: Real-Time Processing for Data Engineering Interviews (Pipeline to Insights)](../../raw/email/email-2025-05-25-week-23-34-real-time-processing-for-data-engineering-intervi.md)
[^src2]: [How to Choose Between Batch and Stream Processing? (Pipeline to Insights)](../../raw/email/email-2025-05-22-how-to-choose-between-batch-and-stream-processing.md)
[^src3]: [Intro to Real-Time Streaming — DataCamp Streaming Concepts](../../raw/pdf/pdf-chapter3-intro-to-real-time-streaming.md)
[^src4]: [Popular Streaming Systems — DataCamp Streaming Concepts](../../raw/pdf/pdf-chapter4-popular-streaming-systems.md)
[^src5]: [Intro to Batch Processing — DataCamp Streaming Concepts ch.1](../../raw/pdf/pdf-chapter1-intro-to-batch-processing.md)
[^src6]: [Intro to Event-Based Computing — DataCamp Streaming Concepts ch.2](../../raw/pdf/pdf-chapter2-intro-to-event-based-computing.md)

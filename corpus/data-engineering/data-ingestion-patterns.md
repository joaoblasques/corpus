---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/email/email-2026-05-06-how-companies-ingest-data-2-key-patterns.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/web/data-pipeline-design-patterns-1-data-flow-patterns-start-dat.md
    channel: web
    ingested_at: 2026-06-19
  - path: raw/email/email-2025-08-05-fix-your-data-pipeline-from-the-start.md
    channel: email
    ingested_at: 2026-06-19
aliases:
  - data ingestion patterns
  - data loading patterns
  - stream ingestion
  - batch ingestion
  - data ingestion
  - landing zone
  - raw zone
tags:
  - corpus/data-engineering
  - concept
created: 2026-06-12
updated: 2026-06-19
---

# Data Ingestion Patterns

**TL;DR.** Most companies ingest data in one of **two ways**: (1) **stream** data into a cloud store via an event log like Kafka, or (2) **extract** data from source systems in **batch** [^src1]. The two differ in latency, ordering, and operational shape; the choice is driven by how fresh the data must be and how the source exposes change.

## The two patterns

| Pattern | Mechanism | Typical use |
|---|---|---|
| **Stream into a cloud store via an event log** | Events are produced to an append log (e.g. [Kafka](/data-engineering/kafka.md)); consumers land them in a cloud store / lakehouse continuously | High-velocity, low-latency data where freshness matters [^src1] |
| **Batch extract from source systems** | Periodically pull rows from operational databases / APIs / files on a schedule | Periodic loads from OLTP systems, SaaS APIs, third-party dumps [^src1] |

These two patterns are the entry point of the pipeline — the **bronze/raw** stage of the [medallion architecture](/data-engineering/medallion-architecture.md) — and feed everything downstream (cleansing, modeling, serving).

## The landing zone (where raw data first lands)

Whichever entry pattern is used, the data first arrives in a **landing zone** — "where all raw source data first lands in your database (or wherever you store your raw data)" [^src3]. It's easy to brush past it in favor of the more interesting modeling/automation work, but neglecting it sets you up for bigger long-term issues; deliberately designing the landing zone benefits the *entire* architecture [^src3]. This is the same stage as the **Raw DB / Bronze / Landing** row of the [pipeline layers](/data-engineering/pipeline-layers.md) mapping — append-only, schema-drift-tolerated, never modified after ingestion — which is exactly what makes downstream transformations safely re-runnable from raw. (Treat as a routing-and-design pointer; the source is a short video teaser, so the specific example designs are not captured here.)

## Relation to other pages

- **Streaming** ingestion is the [Kafka](/data-engineering/kafka.md) / event-log path; its load mechanics (append-only, at-most-once settings for de-duplicated downstream data) are covered under stream load strategies in [Incremental Pipeline Design](/data-engineering/incremental-pipeline-design.md).
- **Batch** ingestion is the extract path; *how* to extract incrementally (timestamp columns, primary-key / hash diffing) and *how* to load (overwrite-partition, row-based update, append) is the subject of [Incremental Pipeline Design](/data-engineering/incremental-pipeline-design.md).
- The distinction also tracks the [CDC](/data-engineering/change-data-capture.md) vs full-load vs incremental axis: CDC is one way a streaming source exposes change.

Which entry pattern is even *viable* is governed by **source/sink properties** — a source's **replayability** ("what did the data look like *n* periods ago?") and a sink's **overwritability** — which is also the prerequisite framing for the downstream [data-flow patterns](/data-engineering/data-flow-patterns.md) (extraction / behavioral / structural) that build on top of ingestion [^src2].

## REST API ingestion with dlt

For REST API sources, **dlt** (data load tool) provides a declarative alternative to writing pagination loops by hand: describe the API shape in a `RESTAPIConfig` object and dlt handles authentication, pagination (cursor/offset/link patterns), and nested JSON normalization automatically. See [dlt](/data-engineering/dlt.md) for details.

## See also

- [Incremental Pipeline Design](/data-engineering/incremental-pipeline-design.md) — extract/load/backfill design for batch pipelines
- [Apache Kafka](/data-engineering/kafka.md) — the streaming-ingestion event log
- [Change Data Capture](/data-engineering/change-data-capture.md) — capturing change from operational sources
- [Medallion Architecture](/data-engineering/medallion-architecture.md) — where ingestion sits in the pipeline
- [Data Flow Patterns](/data-engineering/data-flow-patterns.md) — extraction/behavioral/structural patterns layered on the entry choice
- [Data Engineering hub](/data-engineering/README.md)

---

[^src1]: [How Companies Ingest Data: 2 Key Patterns](../../raw/email/email-2026-05-06-how-companies-ingest-data-2-key-patterns.md)
[^src2]: [Data Pipeline Design Patterns - #1 Data Flow Patterns](../../raw/web/data-pipeline-design-patterns-1-data-flow-patterns-start-dat.md)
[^src3]: [Fix Your Data Pipeline...From The Start — the "Landing Zone" (Kahan Data Solutions)](../../raw/email/email-2025-08-05-fix-your-data-pipeline-from-the-start.md)

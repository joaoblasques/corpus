---
type: source
domain: data-engineering
status: draft
sources:
  - path: raw/notes/notes-03-resources-articles-data-crash-course-tinybird-chapter-two.md
    channel: notes
    ingested_at: 2026-07-17
aliases: []
tags:
  - corpus/data-engineering
  - source
  - doc-quick-intake
  - olap
  - real-time-processing
  - columnar-storage
  - materialized-views
created: 2026-07-17
updated: 2026-08-11
provisional: false
url: https://www.tinybird.co/data-crash-course/chapter-two
origin: obsidian
---

# Data Crash Course · Tinybird — Chapter Two

**TL;DR:** Foundational reference for real-time analytical data engineering: OLAP vs row-based storage, data ingestion practices, schema and query optimization, and materialized views for pre-aggregation.

Source: Tinybird Data Crash Course, Chapter Two[^1]

---

## Real-time Data Processing

Real-time data processing is defined as "immediate processing and analysis of data as it is created or received."[^1] It is critical for applications that need instantaneous insights — real-time dashboards and automated decision-making systems are the primary examples cited.[^1]

---

## Database Selection

The source distinguishes two key dimensions for database choice in analytical workloads:[^1]

- **OLAP databases** are optimized for complex queries and analytical workloads, as opposed to OLTP systems designed for transactional row-level operations.
- **Columnar storage** offers superior compression and processing speed compared to row-based storage — the recommended default for analytical use cases.[^1]

---

## Data Ingestion

Two practices are highlighted for efficient ingestion:[^1]

- **Structured data** is faster to process and query than unstructured formats.
- **Batching and open formats** enhance ingestion efficiency and interoperability between systems.[^1]

---

## Storage Optimization

Schema design is the primary lever for storage efficiency:[^1]

- **Tight schemas** improve data compression and access speed.
- **Access-pattern-aware sorting** — ordering data based on how it will be queried — accelerates retrieval.[^1]

The source flags poor schema design as the leading pitfall: it causes "increased latency and higher storage costs."[^1]

---

## Query Optimization

Two core techniques are identified:[^1]

- **Indexing and filtering** minimize the volume of data scanned per query.
- **Parallelization** reduces wall-clock query time by splitting work across processing units.[^1]

---

## Materialized Views

Materialized views pre-aggregate data so that query-time computation is reduced.[^1] The source notes incremental updates as a complementary mechanism enabling "fast real-time data updates" without full recomputation.[^1]

---

## Practical Example: Real-time Dashboard

The source walks through a concrete scenario — displaying real-time user statistics:[^1]

1. Use a columnar OLAP database for efficient query execution.
2. Apply materialized views to pre-aggregate user data.
3. Ingest structured data to maintain low latency.

Claimed outcome: sub-second latency with reduced computational overhead from pre-aggregated data.[^1]

---

## Related corpus pages

- [/data-engineering/README.md](/data-engineering/README.md)

---

[^1]: raw/notes/notes-03-resources-articles-data-crash-course-tinybird-chapter-two.md — Tinybird Data Crash Course Chapter Two (collected 2026-07-17, origin obsidian, source URL: https://www.tinybird.co/data-crash-course/chapter-two)

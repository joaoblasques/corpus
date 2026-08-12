---
type: source
domain: data-engineering
status: draft
sources:
  - path: raw/notes/notes-03-resources-articles-data-crash-course-tinybird-chapter-three.md
    channel: notes
    ingested_at: 2026-07-17
aliases: []
tags:
  - corpus/data-engineering
  - source
  - doc-quick-intake
  - clickhouse
  - olap
  - real-time-processing
  - data-ingestion
  - columnar-storage
created: 2026-07-17
updated: 2026-08-12
provisional: false
url: https://www.tinybird.co/data-crash-course/chapter-three
origin: obsidian
---

# Data Crash Course · Tinybird — Chapter Three

**TL;DR:** Tinybird's chapter three covers real-time OLAP fundamentals: why columnar storage enables millisecond queries at scale, how to balance latency vs. throughput given modern hardware constraints, and how schema design and batched ingestion determine end-to-end performance.

**Source:** [tinybird.co/data-crash-course/chapter-three](https://www.tinybird.co/data-crash-course/chapter-three)[^1]

---

## Real-time data analytics

Real-time analytics is defined as "the ability to process and analyze data as it is created or received."[^1] The motivating benchmark is companies like Vercel and Canva querying billions of rows in milliseconds.[^1]

Immediate insights enable businesses to react promptly to changes and make data-driven decisions, which is the core business case for investing in real-time infrastructure.[^1]

---

## Modern hardware considerations

The source frames two competing axes for data infrastructure choices:[^1]

- **Latency vs. throughput** — speed of individual data processing vs. volume of data processed per unit time.
- **CPU vs. memory speed** — faster sequential memory access improves overall performance.

These hardware realities directly motivate the preference for columnar databases and batch ingestion patterns described below.[^1]

---

## OLAP databases and columnar storage

For large-scale analytical workloads, the source recommends databases optimized for analytical queries with **columnar storage** for better compression and vectorization.[^1] ClickHouse is cited as a specific example of a columnar database with "superior compression and vectorization capabilities."[^1]

Columnar layout improves query performance by allowing the engine to read only the columns needed and apply SIMD vectorized operations across tightly packed values.[^1]

---

## Data ingestion strategies

Two ingestion patterns are recommended:[^1]

- **Structured data** — enforces faster processing and easier manipulation downstream.
- **Batching and open formats** — batch processing optimizes throughput; open formats (e.g., Parquet, Arrow) enhance flexibility and interoperability.

---

## Schema and query optimization

The source identifies poor schema design as a common pitfall: it leads to inefficient storage and slow queries, with consequences for both storage cost and query latency.[^1]

Best practices cited:[^1]

- Design a "tight schema with necessary attributes" aligned to access patterns.
- Use appropriate data types to maximize compression.
- Apply indexes and filters to query less data.
- Leverage parallel processing where possible.
- Materialized views can pre-aggregate data, saving processing power and cost.

---

## Scaling

For scaling data infrastructure, the source recommends strategic planning with sharding (horizontal partitioning) and replication (redundancy and read throughput).[^1]

---

## Related corpus pages

- [/data-engineering/databricks.md](/data-engineering/databricks.md)
- [/data-engineering/semantic-layer.md](/data-engineering/semantic-layer.md)

[^1]: raw/notes/notes-03-resources-articles-data-crash-course-tinybird-chapter-three.md

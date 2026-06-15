---
type: entity
domain: data-engineering
status: draft
sources:
  - path: raw/email/email-2026-05-25-when-and-when-not-to-use-databricks.md
    channel: email
    ingested_at: 2026-06-11
  - path: raw/web/debunking-8-data-layout-myths-why-liquid-clustering-outperfo.md
    channel: web
    ingested_at: 2026-06-11
  - path: raw/web/unity-catalog.md
    channel: web
    ingested_at: 2026-06-11
  - path: raw/web/databricks-pricing-flexible-plans-for-data-and-ai-solutions.md
    channel: web
    ingested_at: 2026-06-11
  - path: raw/web/lakeflow-spark-declarative-pipelines-databricks-on-aws.md
    channel: web
    ingested_at: 2026-06-11
aliases:
  - Databricks
  - Unity Catalog
  - Unity Catalogue
  - Liquid Clustering
  - Lakeflow
  - Lakeflow Spark Declarative Pipelines
tags:
  - corpus/data-engineering
  - entity
created: 2026-06-11
updated: 2026-06-11
---

# Databricks

**TL;DR.** Databricks is a **lakehouse platform** that puts warehouse-style SQL, BI, ML, and streaming on top of low-cost object storage (S3, ADLS, GCS) using open table formats such as Delta or Iceberg [^src1]. It earns its keep when the alternative is stitching a warehouse, Spark cluster, streaming engine, notebook environment, feature store, governance layer, and permission model from multiple vendors [^src1]. It is "a powerful platform... also a heavy one" — the adoption question is fit, not quality [^src1]. Key primitives: **Unity Catalog** (governance), **Liquid Clustering** (data layout), **Lakeflow Spark Declarative Pipelines** (orchestration), and **Photon** (vectorised query engine) [^src1].

## When Databricks makes sense

Five strong-fit situations [^src1]:

1. **Multi-TB data with mixed workloads** — BI, ad-hoc SQL, batch, streaming, and ≥1 ML use case on the same data with one permission story.
2. **Ten or more engineers across disciplines** — shared platform + shared catalogue makes lineage and governance reusable.
3. **Multi-source ingestion with governance requirements** — a dozen sources plus real legal obligations (finance, healthcare, regulated public sector); Unity Catalog, row/column-level security, unified audit logs.
4. **Replatforming off Hadoop or legacy Spark** — biggest immediate win; Spark knowledge transfers, short learning curve.
5. **Streaming, ML, and BI on the same data** — lakehouse is the path of least resistance.

## When Databricks is overkill

The section "that does not get written often enough" [^src1]:

- **Sub-500GB BI-only workloads** — Postgres + dbt + a managed BI tool quietly out-delivers on cost, simplicity, hiring, time-to-dashboard. See [[data-engineering/postgres|Postgres]], [[data-engineering/dbt|dbt]].
- **Small teams (1–3 engineers) who have never run Spark** — months lost to cluster configs, shuffle partitions, broadcast joins.
- **Single-cloud, single-source SQL workloads** — one cloud warehouse (BigQuery, Snowflake, Redshift, Synapse) is enough.
- **Pure batch, daily refresh** — managed Airflow + warehouse + dbt is "boring... boring is hireable" [^src1].
- **Early-stage startups still figuring out the data layer** — a lakehouse is a premature commitment to heavy architecture.

## Decision framework

Four questions to run every time the adoption question comes up [^src1]:

1. **Data scale and growth?** Multi-TB and growing → lakehouse. Sub-500GB and linear → Postgres + dbt.
2. **Team size and skill mix?** Small SQL-first team → wrong tool. Larger mixed-discipline team → compounding leverage.
3. **Workload mix?** BI + ML + streaming on same data → lakehouse. BI-only or batch-SQL-only → single warehouse.
4. **Realistic total cost of ownership?** Build a TCO model (compute, storage, egress, governance, engineering time) for both Databricks and the simpler stack, over one and three years [^src1].

## Common adoption mistakes

Seven recurring patterns [^src1]:

1. Picking Databricks "for the logo" — cultural pressure dressed as a decision.
2. Running all-purpose (interactive) clusters 24/7 — they bill for idle; move scheduled jobs to job clusters or serverless, auto-terminate aggressively.
3. Rolling out Unity Catalog before there is anything to govern — UC is genuine setup work; deploy when governance pain is real.
4. Treating Databricks as "just managed Spark" — never adopting Lakeflow, serverless SQL, or Photon. The platform does one thing instead of five.
5. No cost guardrails on day one — budgets, alerts, cluster policies, tags in week one.
6. Underestimating egress and storage — DBU bill is on the Databricks invoice; egress, object storage, snapshot retention, and UC metadata live on the cloud provider's invoice. Monitor both.
7. Picking Databricks without picking who owns it — name an owner before adoption.

## Cost model

Databricks has **several prices, by workload type**, not one [^src1]:

- **All-purpose compute** — most expensive; interactive notebook work. Do not run scheduled jobs here.
- **Jobs compute** — cheaper than all-purpose for the same spec; scheduled work belongs here.
- **SQL warehouses (serverless/classic)** — built for BI; serverless is meaningfully cheaper for bursty workloads.
- **Declarative pipelines (Lakeflow)** — own SKU; value is orchestration, dependency management, incremental processing.

The **DBU** (Databricks Unit) is a normalised measure of processing capacity; matching the workload to the right SKU drops the bill with no code change [^src1]. Most waste lives in cluster lifecycle: auto-terminate interactive clusters, use spot instances for fault-tolerant work, right-size drivers, enforce cluster policies [^src1]. Databricks pricing is pay-as-you-go at per-second granularity with no up-front cost, plus Committed Use Contracts for volume discounts [^src4].

## Unity Catalog

Databricks' governance layer for tables, files, models, and access policies [^src1]. A unified catalog for structured data, unstructured data, business metrics, and AI models across open formats like Delta Lake, Apache Iceberg, Hudi, and Parquet [^src3]. Provides row- and column-level security, unified audit logs, auto-detection/tagging of sensitive data, and a single pane of glass for policy enforcement [^src1][^src3]. Setup is non-trivial: Metastore, catalogues, external locations, storage credentials, and permissions inheritance [^src1].

## Liquid Clustering vs partitioning

Liquid Clustering is Databricks' modern data-layout standard, GA since 2024, positioned to replace Hive-style partitioning [^src2]. Hive-style partitioning forces a commit at table-creation time to a physical file organization; wrong-cardinality columns produce billions of tiny files or slower queries — and in Databricks' analysis it leads to over-partitioning and small-file problems in **more than 75% of cases** [^src2]. Liquid instead treats clustering keys as engine *input*: keys can change at any time (or be auto-selected via Automatic Liquid Clustering), cardinality is not a constraint, and layout evolves without unnecessary rewrites [^src2].

Key points [^src2]:

- **Directory-pruning is a myth on modern OTFs.** Delta uses a transaction log with per-column stats; pruning happens against statistics at file granularity, not directory structure. Liquid uses the same mechanism.
- **Row-level concurrency** vs partitioning's file-level concurrency — two writers on different rows in the same file no longer conflict, removing a main reason teams partitioned (write boundaries).
- **Metadata-only operations** (DELETE, COUNT, DISTINCT, GROUP BY) are supported; metadata-only DELETEs ran ~90% faster than full-rewrite DELETEs in benchmarks.
- **It is a write-side optimization** producing standard Parquet with min/max stats; any compatible reader (open-source Spark, [[data-engineering/duckdb|DuckDB]], etc.) benefits — not Databricks-only.
- Production: Arctic Wolf runs a 3.8+ PB telemetry table ingesting 1+ trillion events/day on Liquid Clustering [^src2].

> Source caveat: the Liquid Clustering myth-busting is a Databricks blog promoting its own feature over partitioning; benchmark figures are vendor-reported.

See [[data-engineering/merge-into|MERGE INTO]] and [[data-engineering/parquet|Parquet]] for related layout mechanics.

## Lakeflow Spark Declarative Pipelines

A framework for batch and streaming pipelines in SQL and Python, formerly known as DLT — you describe tables and the platform handles orchestration and incremental processing [^src1][^src5]. Lakeflow SDP extends and is interoperable with Apache Spark Declarative Pipelines while running on the performance-optimized Databricks Runtime [^src5]. Core concepts: pipelines, flows, streaming tables, and materialized views; common use cases are ingestion from cloud storage (S3, ADLS Gen2, GCS) and message buses (Kafka, Kinesis, Pub/Sub, EventHub, Pulsar) plus incremental transformations [^src5]. See [[data-engineering/kafka|Kafka]].

## Related

- [[data-engineering/open-table-formats|Open table formats]] — Delta/Iceberg underpin the lakehouse
- [[data-engineering/data-lake|Data lake]] · [[data-engineering/apache-iceberg|Apache Iceberg]] · [[data-engineering/parquet|Parquet]]
- [[data-engineering/dbt|dbt]] · [[data-engineering/postgres|Postgres]] — the "simpler stack" alternatives
- [[data-engineering/duckdb|DuckDB]] — reads Liquid-Clustered output

[^src1]: [When (and when not) to use Databricks](../../raw/email/email-2026-05-25-when-and-when-not-to-use-databricks.md)
[^src2]: [Debunking 8 data layout myths: why Liquid Clustering outperforms partitioning](../../raw/web/debunking-8-data-layout-myths-why-liquid-clustering-outperfo.md)
[^src3]: [Unity Catalog (Databricks)](../../raw/web/unity-catalog.md)
[^src4]: [Databricks pricing](../../raw/web/databricks-pricing-flexible-plans-for-data-and-ai-solutions.md)
[^src5]: [Lakeflow Spark Declarative Pipelines (Databricks on AWS)](../../raw/web/lakeflow-spark-declarative-pipelines-databricks-on-aws.md)

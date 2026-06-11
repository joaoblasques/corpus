---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/email/email-2026-05-26-5-insights-to-help-you-learn-any-open-table-format-faster.md
    channel: email
    ingested_at: 2026-06-11
  - path: raw/web/what-is-open-data-infrastructure-blog-fivetran.md
    channel: web
    ingested_at: 2026-06-11
aliases:
  - OTF
  - open table format
  - table format
  - Delta Lake
  - Hudi
tags:
  - corpus/data-engineering
  - concept
created: 2026-06-11
updated: 2026-06-11
---

# Open Table Formats

**TL;DR.** An open table format (OTF) is a **separate, database-independent metadata layer** that lets a query engine "see" a directory of Parquet objects in object storage as a single transactional table. The big three are Apache Iceberg, Delta Lake, and Apache Hudi; newer entrants include Apache Paimon and DuckLake [^src1]. Because the metadata layer is open (not owned by any one database), the same data can be read and written by many engines — the foundation of **Open Data Infrastructure (ODI)**, which separates storage, compute, and tooling into independently-evolving layers to avoid vendor lock-in [^src2]. See [[data-engineering/apache-iceberg|Apache Iceberg]] for the reference implementation.

## The core idea: metadata as source of truth

When data is stored as Parquet files on S3, "those are just objects" [^src1]. Users want to work with a friendlier abstraction — a table — so every query engine (Snowflake, BigQuery, Redshift, Databricks, even PostgreSQL) needs a "translator" to see files as a table [^src1]. That translator is a **metadata layer**, and it is "the main idea behind any table format out there, from Iceberg to Delta Lake" [^src1].

The defining property of an *open* table format: the metadata layer is **separate and has no database dependence** — that is why they earned the "open" prefix [^src1]. This is the single most transferable concept across formats: learn the metadata layer of one and you can pick up any other quickly [^src1].

## Open Data Infrastructure (the architectural pattern)

ODI is the architecture OTFs enable: store data **once** in open formats and use it **anywhere** — across tools, compute engines, and AI systems — without single-vendor lock-in [^src2]. It is a shift away from tightly-coupled proprietary "walled gardens" that bundle storage, compute, and tooling into one ecosystem [^src2].

Three architectural principles [^src2]:

1. **Open, standards-based movement and transformation** — pipelines are portable, not locked into proprietary APIs/runtimes.
2. **A unified, open data lake foundation** — data landed once in open formats on object storage (S3, ADLS, GCS); compute engines plug in on top. See [[data-engineering/data-lake|data lake]].
3. **Activation, semantics, and AI consumption** — business entities and metrics defined once and reused everywhere, so dashboards, workflows, and AI agents act on the same trusted logic.

Four claimed benefits: no vendor lock-in; lower cost at scale (store once, apply compute where needed, no duplicate pipelines); faster innovation (adopt new tools without large migrations); and a foundation built for AI/real-time workloads [^src2].

> Note: ODI framing comes from Fivetran, an ingestion vendor; treat the benefit claims as vendor advocacy, not neutral benchmark.

## Gotchas / things to watch

- **Format is not the whole story.** A separate metadata layer (transaction log + per-file statistics) replaces directory structure as the planning mechanism — e.g. on Delta and Iceberg, directory-pruning does not exist; the engine prunes against statistics in the log, not the directory tree (see [[data-engineering/databricks|Databricks]] Liquid Clustering) [^src3].
- **Separate storage from compute from day one** is the practical ODI starting move; adopt open formats early to preserve portability [^src2].
- **More than three players now.** Beyond Iceberg/Delta/Hudi, Paimon and DuckLake have entered the market [^src1]; see [[data-engineering/duckdb|DuckDB]] for DuckLake.

## Related

- [[data-engineering/apache-iceberg|Apache Iceberg]] — reference open table format
- [[data-engineering/data-lake|Data lake]] — the storage substrate
- [[data-engineering/parquet|Parquet]] — the underlying file format
- [[data-engineering/databricks|Databricks]] — lakehouse platform built on Delta/Iceberg
- [[data-engineering/query-engine-routing|Query-engine routing]] — multi-engine access enabled by OTFs

[^src1]: [5 insights to help you learn any open table format faster](../../raw/email/email-2026-05-26-5-insights-to-help-you-learn-any-open-table-format-faster.md)
[^src2]: [What is Open Data Infrastructure? (Fivetran)](../../raw/web/what-is-open-data-infrastructure-blog-fivetran.md)
[^src3]: [Debunking 8 data layout myths (Databricks)](../../raw/web/debunking-8-data-layout-myths-why-liquid-clustering-outperfo.md)

---
type: concept
domain: data-engineering
status: draft
sources:
  - path: 03_Resources/Study Notes/dbt Data Architecture - Simple Stack Design.md
    channel: notes
    ingested_at: 2026-05-21
  - path: raw/email/email-2025-09-08-medallion-architecture-is-not-a-data-model.md
    channel: email
    ingested_at: 2026-06-11
  - path: raw/email/email-2025-07-08-what-is-an-analytics-database.md
    channel: email
    ingested_at: 2026-06-19
aliases:
  - pipeline layers
  - data pipeline layers
  - staging warehouse marts
  - ELT layers
  - simple stack
  - bronze silver gold
  - medallion layers
tags:
  - corpus/data-engineering
  - concept
created: 2026-05-21
updated: 2026-06-19
---

# Pipeline Layers (Staging → Warehouse → Marts)

**TL;DR**: The standard ELT separation pattern — raw ingested data moves through progressive transformation layers (staging, warehouse, marts) before reaching BI tools, with each layer having a distinct purpose and materialization strategy [^src1].

## The Simple Stack

```
External Sources → [Extract & Load] → Raw DB → Staging → Warehouse → Marts → Reporting
```

Two distinct databases on the same server [^src1]:

| Database | Schemas | Contents |
|---|---|---|
| **Raw DB** | One per source (e.g., `stripe`, `google_analytics`) | Untransformed, as-ingested data |
| **Analytics DB** | `staging`, `warehouse`, `marts` | Progressive transformations |

## Layer definitions

| Layer | Materialization | Purpose |
|---|---|---|
| **Staging** | View | Lightly clean and standardize raw data; 1:1 with source tables; no business logic |
| **Warehouse** | Table | Joins, enrichment, applied business logic; the integration layer |
| **Marts** | Table | Consumption-ready tables shaped for specific BI use cases or consumer teams |

Using **views** for staging keeps them cheap and always reflecting current raw data. **Tables** for warehouse and marts reflect the compute cost of joins and aggregations paid once at build time [^src1].

## Mapping to bronze/silver/gold (medallion)

The staging→warehouse→marts split is one naming of the same progressive-refinement idea captured by the [[data-engineering/medallion-architecture|medallion architecture]] (bronze→silver→gold). These are interchangeable vocabularies for *lifecycle stages*, not data models [^src2]:

| This page (Simple Stack) | Medallion | Other names [^src2] | Intent |
|---|---|---|---|
| Raw DB | Bronze | Landing | Raw ingestion; append-only; schema drift tolerated |
| Staging | Silver | Curated | Cleansed, conformed, de-duped, typed, business keys resolved |
| Warehouse + Marts | Gold | Serving / Data Mart | Business-ready, modeled for consumption |

Each stage progressively removes complexity for an increasingly broader, less technical audience: bronze (technical) → silver (less technical) → gold (business) [^src2].

**Key boundary**: these layers are *model-agnostic*. > "Stop treating Bronze/Silver/Gold as data models. They're lifecycle stages." [^src2] The pipeline layer (how data is transformed and moved) is orthogonal to the data model (entities, grain, keys — star schema, OBT, Data Vault, etc.). Gold is *not* automatically a star schema; it is simply business-ready data, modeled however the consumer needs [^src2]. See [[data-engineering/dimensional-modeling|dimensional modeling]] for the modeling axis.

## Application DB vs Analytics DB (a prior question)

Before the Raw→Analytics split *inside* the analytics database, there's an upstream question many teams get wrong. For a lot of companies the primary data source is a single in-house application, so the data team ends up working with that application's **back-end database** — and the tempting shortcut is to *"just use that same database server to build your data warehouse"* [^src3]. That conflates two different systems with different trade-offs: an **application (transactional) database** is optimized for many small reads/writes serving the live app, whereas an **analytics database** is optimized for large scans and aggregations serving reporting [^src3]. Running analytics on the application DB risks contending with production traffic and fighting a storage/engine layout tuned for the wrong workload — which is *why* the pipeline pulls data **out** of the app DB into a separate analytics DB (the Raw → Analytics flow below). For the engine-level reason (row vs columnar storage, OLTP vs OLAP), see [[data-engineering/storage-fundamentals|Storage Fundamentals]] and the OLAP engines [[data-engineering/duckdb|DuckDB]] / [[data-engineering/clickhouse|ClickHouse]] / [[data-engineering/snowflake|Snowflake]].

## Why separate Raw from Analytics

- Raw data is append-only and never modified after ingestion
- Raw database gives a stable, auditable foundation — transformations can always be re-run from raw
- Separation enforces the discipline that sources point to raw data only; models point to other models [^src1]

## Tools that implement this pattern

- [[data-engineering/dbt|dbt]] — the canonical tool for implementing this layered transformation model; project directory structure mirrors the schema structure

## See also

- [[data-engineering/dbt|dbt]] — tool that codifies this architecture
- [[data-engineering/medallion-architecture|Medallion Architecture]] — bronze/silver/gold naming of the same staged-refinement idea
- [[data-engineering/dimensional-modeling|Dimensional Modeling]] — the orthogonal modeling axis (gold ≠ star schema by default)
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [[03_Resources/Study Notes/dbt Data Architecture - Simple Stack Design|dbt Data Architecture - Simple Stack Design]]
[^src2]: [Medallion Architecture is NOT a Data Model](../../raw/email/email-2025-09-08-medallion-architecture-is-not-a-data-model.md)
[^src3]: [What is an "Analytics" Database? (Kahan Data Solutions)](../../raw/email/email-2025-07-08-what-is-an-analytics-database.md)

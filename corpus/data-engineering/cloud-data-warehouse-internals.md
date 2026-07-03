---
type: synthesis
domain: data-engineering
status: draft
sources:
  - path: raw/email/email-2025-04-17-the-internal-of-bigquery-snowflake-databricks-and-redshift.md
    channel: email
    ingested_at: 2026-06-19
aliases:
  - cloud data warehouse internals
  - cloud warehouse architecture
  - BigQuery vs Snowflake vs Databricks vs Redshift
  - shared-disk OLAP
  - disaggregated storage and compute
  - vectorization vs code specialization
tags:
  - corpus/data-engineering
  - synthesis
created: 2026-06-19
updated: 2026-06-19
---

# Cloud Data Warehouse Internals

**TL;DR.** From a 10,000-foot view the four leading cloud warehouses — **[BigQuery](/data-engineering/bigquery.md), [Snowflake](/data-engineering/snowflake.md), [Databricks](/data-engineering/databricks.md), and [Redshift](/data-engineering/redshift.md)** — are the *same machine*: they **separate storage from compute**, run query execution on virtual machines that exploit **vectorization or code specialization**, and keep data in **object storage** using a **hybrid or columnar** file format [^src1]. What differs is *how each one optimizes* that shared blueprint. This page is the cross-warehouse comparison; each system has its own entity page for depth.

## The shared blueprint (2010s shift)

The 2010s saw the **cloud-native shared-disk OLAP** system emerge, pioneered by Google BigQuery (2010) and Snowflake (2012) [^src1]. Unlike traditional share-nothing data systems, these store data **separately in object storage** (the exception being Redshift's original design), let the vendor manage the storage layer, and give users advanced distributed query power **without managing infrastructure** [^src1]. The paradigm shift was **share-nothing → shared-disk** [^src1].

Two file-format terms recur [^src1]:

- **Column format** — columns stored completely separately (used by Redshift).
- **Hybrid format** — like [Parquet](/data-engineering/parquet.md): data grouped into **row groups** (a horizontal partition of rows); within each, a column's data is a **column chunk** (vertical partition). Used by BigQuery (Capacitor), Snowflake, and Databricks (Parquet/Delta).

## Per-warehouse optimizations

| Warehouse | Compute engine | Storage layer & format | Distinctive optimization |
|---|---|---|---|
| **BigQuery** | Dremel (on Borg) | Colossus; **Capacitor** (hybrid) | Worker-node + **separate shuffle layer**; runtime plan adaptation [^src1] |
| **Snowflake** | Proprietary C++ (VectorWise lineage) | S3/GCS/Azure; proprietary (hybrid) | Local **caching** + **file stealing** for skew [^src1] |
| **Databricks** | **Photon** (C++) on Spark/DBR | Cloud object store; **Delta Lake** (Parquet + WAL) | In-place Spark improvement; vectorized, runtime-adaptive Photon [^src1] |
| **Redshift** | PostgreSQL-derived, MPP | RMS (S3-backed, RA3/serverless); **column** | **Code specialization** (compiled C++ per query) + compilation service [^src1] |

### BigQuery — shuffle separation

Dremel evolved from share-nothing to shared-disk (GFS → Colossus), then **separated the shuffle layer** into distributed storage so compute and shuffle can scale independently; it adapts the query plan at runtime because it often processes unseen data with poor statistics [^src1]. See [BigQuery](/data-engineering/bigquery.md).

### Snowflake — caching and file stealing

Because Snowflake is not the cloud vendor, each S3 read costs real money, so it **caches aggressively** on worker nodes and uses **file stealing** to handle skew (an idle worker requests files from a busy peer, reading them from S3 rather than burdening the peer) [^src1]. It avoids shuffle-based execution: workers exchange data directly [^src1]. See [Snowflake](/data-engineering/snowflake.md).

### Databricks — Photon, improving Spark in place

Databricks could not replace Spark without disrupting customers, so it **enhanced it**: the **Photon** engine is a C++ library of physical operators inside the Databricks Runtime, built on a **vectorized model** (vs Spark's code-generation) with **runtime adaptivity**, falling back to Spark SQL for unsupported operations [^src1]. Photon uses **columnar in-memory representation**, eliminating the column-to-row pivot that row-oriented Spark SQL needed when scanning Parquet [^src1]. Storage is **Delta Lake** — an ACID layer that records which Parquet objects belong to a table via a **write-ahead log in cloud object storage**; a file unreferenced by the log is unreadable [^src1]. See [Databricks](/data-engineering/databricks.md).

### Redshift — code specialization

Redshift is the special case: **share-nothing originally**, later adding **RMS** (S3-backed) for storage/compute separation in RA3/serverless [^src1]. Rather than vectorization it uses **code specialization** — compiling query-specific C++, caching the binaries locally, and (since 2020) in an external **compilation service** shared across clusters [^src1]. See [Redshift](/data-engineering/redshift.md).

## Why this matters

The practical payoff (Vu Trinh's framing): in a world where "you might work with Databricks today and learn Snowflake tomorrow," knowing the shared blueprint gives you a **starting point for any new cloud warehouse** — they differ in optimization details, not in fundamentals [^src1].

## Related

- [BigQuery](/data-engineering/bigquery.md) · [Snowflake](/data-engineering/snowflake.md) · [Databricks](/data-engineering/databricks.md) · [Redshift](/data-engineering/redshift.md)
- [Compute–Storage Decoupling](/data-engineering/compute-storage-decoupling.md) — this comparison generalized: the same separate-compute-from-object-storage move across warehouses, lakehouse, and streaming
- [Storage Fundamentals](/data-engineering/storage-fundamentals.md) — row vs columnar vs hybrid; vectorization vs code specialization
- [Apache Parquet](/data-engineering/parquet.md) — the canonical hybrid format
- [Apache Spark](/data-engineering/apache-spark.md) — the engine Photon accelerates
- [Open Table Formats](/data-engineering/open-table-formats.md) — Delta/Iceberg metadata layers
- [Data Engineering hub](/data-engineering/README.md)

---

[^src1]: [The internal of BigQuery, Snowflake, Databricks and Redshift (Vu Trinh)](../../raw/email/email-2025-04-17-the-internal-of-bigquery-snowflake-databricks-and-redshift.md)

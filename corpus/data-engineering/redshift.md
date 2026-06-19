---
type: entity
domain: data-engineering
status: draft
sources:
  - path: raw/email/email-2025-04-17-the-internal-of-bigquery-snowflake-databricks-and-redshift.md
    channel: email
    ingested_at: 2026-06-19
aliases:
  - Redshift
  - Amazon Redshift
  - redshift
  - RMS
  - Redshift Managed Storage
  - ParAccel
tags:
  - corpus/data-engineering
  - entity
created: 2026-06-19
updated: 2026-06-19
---

# Amazon Redshift

**TL;DR.** Amazon Redshift is a **column-oriented, massively parallel processing (MPP)** cloud data warehouse, built on technology from **ParAccel** and based on an older **PostgreSQL 8.0.2** [^src1]. Preview launched November 2012; general availability February 2013 [^src1]. It is the architectural **special case** among the big four: it was designed **share-nothing** first and only later bolted on storage/compute separation via **Redshift Managed Storage (RMS)** [^src1]. Its distinctive performance lever is **code specialization** (per-query compiled C++) rather than the vectorization the others rely on [^src1].

## From share-nothing to RMS

Redshift initially used a **share-nothing** architecture (data lived on the compute nodes) [^src1]. Later it introduced **Redshift Managed Storage (RMS)**, which uses Amazon S3 behind the scenes — offloading data from the compute node so customers can **scale compute and storage independently** [^src1]. RMS is only available in the **RA3** cluster and the **serverless** Redshift service [^src1].

A Redshift cluster has a single **coordinator (leader) node** plus multiple **worker nodes**; with RMS the data is offloaded to S3, making compute nodes stateless [^src1]. To know which worker owns which subset, Redshift **partitions the table's data into buckets** distributed across workers, by an engine-chosen scheme or a user-declared one (round-robin or hash) [^src1].

Like [[data-engineering/snowflake|Snowflake]], Redshift **caches data on each worker's local SSD** to speed queries, via a **two-level tiered cache**: a low level for cold blocks (reference count incremented on each access) and a high level for hot blocks promoted after repeated access; eviction decrements counts until a block drops to the low level or is evicted [^src1].

## Compute: code specialization, not vectorization

The OLAP world has two main ways to speed up query execution, and they are **not mutually exclusive** [^src1]:

- **Vectorization** — process a batch (vector) of values instead of one record at a time (used by BigQuery, Snowflake, and Databricks' Photon).
- **Code specialization** — generate code per query to cut CPU instructions; without it, every operator runs a `switch` to check the data type and pick a function. The generated code avoids this because all operators for a query are produced at execution time.

**Redshift uses code specialization** [^src1]: it generates **C++ code specific to the query plan and schema**, compiles it, and ships the binary to compute nodes [^src1]. Compiled objects are **cached** in the local cluster cache and reused for identical/similar queries — faster because Redshift skips re-compilation; on a cache miss it must generate the code [^src1]. In **2020** Redshift added a **compilation service** that uses separate (non-cluster) resources and caches compiled objects in an **external cache**, so they can be served across multiple clusters [^src1].

## Storage format

Unlike BigQuery, Snowflake, and Databricks (which use a **hybrid** format), Redshift stores data in pure **column format** — letting it pack data and apply compression to minimize disk I/O; a row is stitched together using the offset of a specific value [^src1].

## Related

- [[data-engineering/cloud-data-warehouse-internals|Cloud Data Warehouse Internals]] — the cross-warehouse comparison this page feeds
- [[data-engineering/snowflake|Snowflake]] · [[data-engineering/bigquery|BigQuery]] · [[data-engineering/databricks|Databricks]] — the other three cloud warehouses
- [[data-engineering/postgres|PostgreSQL]] — Redshift forked from PostgreSQL 8.0.2
- [[data-engineering/storage-fundamentals|Storage Fundamentals]] — column vs hybrid format; vectorization vs code specialization
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [The internal of BigQuery, Snowflake, Databricks and Redshift (Vu Trinh)](../../raw/email/email-2025-04-17-the-internal-of-bigquery-snowflake-databricks-and-redshift.md)

---
type: entity
domain: data-engineering
status: draft
sources:
  - path: raw/email/email-2025-04-17-the-internal-of-bigquery-snowflake-databricks-and-redshift.md
    channel: email
    ingested_at: 2026-06-19
aliases:
  - BigQuery
  - Google BigQuery
  - bigquery
  - Dremel
  - Colossus
  - Capacitor
tags:
  - corpus/data-engineering
  - entity
created: 2026-06-19
updated: 2026-06-19
---

# Google BigQuery

**TL;DR.** BigQuery is Google's **serverless cloud data warehouse** (publicly launched 2010), one of the two pioneers — with [Snowflake](/data-engineering/snowflake.md) — of the **cloud-native shared-disk OLAP** architecture that separates compute from storage [^src1]. It combines three internal Google technologies: **Dremel** (query engine), **Colossus** (storage), and **Borg** (compute/cluster management, "think Kubernetes") [^src1]. Users get advanced distributed query processing without managing any infrastructure [^src1].

## The three pillars

BigQuery is an assembly of long-running Google systems [^src1]:

- **Dremel** — the query-processing engine, introduced 2010; inspired by the MapReduce shuffle implementation [^src1].
- **Colossus** — the storage layer; successor to the Google File System (GFS). "You can think of it as S3 or GCS object storage" [^src1].
- **Borg** — compute/cluster management (the system Kubernetes descended from) [^src1].

## Compute: Dremel's evolution to shared-disk + separate shuffle

Dremel began on a few hundred **shared-nothing** servers, each keeping a subset of data on local disk — which forced data movement on cluster-membership changes and prevented compute and storage from scaling independently [^src1]. Google gradually shifted Dremel to a **shared-disk architecture** on GFS and then Colossus, letting compute and storage scale separately — at the cost of network latency talking to the storage layer, which they invested heavily to reduce [^src1].

A second bottleneck was **shuffling**. In MapReduce's first phase each worker maps its assigned data and writes output to temporary local storage (RAM/disk); in the reduce phase each worker pulls the keys it owns (the shuffle) [^src1]. Because mapper/reducer scaling is unpredictable and shuffle storage was colocated with compute, the two could not scale independently — so Google **separated the shuffle layer** into a distributed storage system of its own [^src1].

Because storage/compute separation means Dremel often processes **unseen data** with no good statistics, optimal up-front planning is hard; Google's answer is to let Dremel **dynamically change the query execution plan at runtime** based on statistics collected during execution [^src1]. (This runtime-adaptivity theme recurs across all four warehouses — see [Cloud Data Warehouse Internals](/data-engineering/cloud-data-warehouse-internals.md).)

## Storage: the Capacitor format

BigQuery stores data in Colossus using an internal columnar format called **Capacitor** [^src1]. From a high level Capacitor organizes data in a **hybrid format** like [Parquet](/data-engineering/parquet.md) (row groups containing per-column chunks) — and in fact **Capacitor inspired the design of Parquet**, especially in how it handles nested and repeated fields [^src1]. Capacitor carries metadata to help engines **prune unnecessary data** (e.g. per-column min/max values) and applies **Run-Length Encoding (RLE)** and **dictionary encoding** to optimize storage space [^src1].

## Related

- [Cloud Data Warehouse Internals](/data-engineering/cloud-data-warehouse-internals.md) — the cross-warehouse comparison this page feeds
- [Snowflake](/data-engineering/snowflake.md) · [Databricks](/data-engineering/databricks.md) · [Redshift](/data-engineering/redshift.md) — the other three cloud warehouses
- [Apache Parquet](/data-engineering/parquet.md) — the open format Capacitor inspired; the hybrid row-group/column-chunk layout
- [Dataform](/data-engineering/dataform.md) — BigQuery-native transformation orchestration
- [Storage Fundamentals](/data-engineering/storage-fundamentals.md) — column vs hybrid format
- [Data Engineering hub](/data-engineering/README.md)

---

[^src1]: [The internal of BigQuery, Snowflake, Databricks and Redshift (Vu Trinh)](../../raw/email/email-2025-04-17-the-internal-of-bigquery-snowflake-databricks-and-redshift.md)

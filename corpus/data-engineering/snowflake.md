---
type: entity
domain: data-engineering
status: draft
sources:
  - path: raw/youtube/youtube-nhwp1btg0cw.md
    channel: youtube
    ingested_at: 2026-06-17
  - path: raw/email/email-2025-04-17-the-internal-of-bigquery-snowflake-databricks-and-redshift.md
    channel: email
    ingested_at: 2026-06-19
aliases:
  - Snowflake
  - snowflake
  - virtual warehouse
  - micro-partition
  - micro-partitions
  - Snowpipe
  - Unistore
  - hybrid tables
tags:
  - corpus/data-engineering
  - entity
created: 2026-06-17
updated: 2026-06-19
---

# Snowflake

**TL;DR.** Snowflake is a **managed, cloud-only OLAP database written from scratch in C++** that pioneered the commercial **disaggregated (shared-disk) architecture**: object storage (S3/GCS/Azure) for data, elastic **virtual warehouses** for compute, and a separate **cloud-services layer** for the catalog/optimizer/coordinator [^src1]. It came on the scene ~2013 (founded by two ex-Oracle engineers plus Marcin Żukowski of Vectorwise/VWise, funded by VC firm Sutter Hill), beat Redshift's design philosophy by being cloud-native from day one, and is analyzed here from CMU's Advanced Database Systems lecture (Andy Pavlo) as a still-state-of-the-art reference system [^src1]. Its competitive moat is no longer the engine (commoditized by DataFusion/Velox) but the surrounding experience — Snowpipe, Snowpark, runtime adaptivity [^src1].

## Architecture: three layers

Snowflake separates **table data from metadata** and splits the system into three tiers [^src1]:

1. **Data storage** — an object store (originally S3-only; now S3/GCS/Azure, chosen by the customer at signup but still Snowflake-managed). They deliberately chose **not** to build their own storage layer — letting Amazon handle replication/durability and spending their engineering on the execution engine and caching instead [^src1].
2. **Virtual warehouse (compute)** — the customer requests compute capacity (not an explicit node count); gets an endpoint to run queries. A running warehouse bills whether or not queries run; **serverless deployments** (added 2022) spin down when idle at a premium [^src1].
3. **Cloud-services layer** — the front-end catch-all: coordinator, scheduler, catalog, query optimizer. The **catalog runs on FoundationDB** (a transactional key-value store, also Sutter-Hill-backed) for transactional metadata updates [^src1].

A worker node is (originally) a raw EC2 instance maintaining a **local cache on attached SSD**; a query spawns a fresh worker **process** that dies when the query ends, giving compute isolation between customers [^src1].

## Compute-side caching + consistent hashing

Because Snowflake is *not* the cloud vendor, every S3 read costs them real money and latency — so they **aggressively cache on the worker nodes** [^src1]. The local cache holds both intermediate results and persistent files pulled from S3; **intermediate results are prioritized** for retention (LRU eviction), since they're ephemeral and must be fast [^src1]. It's a **multi-layer buffer pool** — memory → local disk → S3 — not the classic two-layer design [^src1].

**Consistent hashing** assigns which worker node "owns" (caches) each micro-partition file. This is the clever part: adding/removing compute nodes only moves files from a predecessor on the ring rather than reshuffling everything (as a shared-nothing system would), so customers can scale up/down cheaply without re-fetching all data from S3 [^src1].

## Execution: push-based vectorized, no shuffle

- **Push-based vectorized execution** using pre-compiled, templated C++ primitives per data type (Marcin's Vectorwise X100 lineage) [^src1].
- **Codegen only for serialize/deserialize** of data moving between workers (this predates Apache Arrow; they used LLVM for a protobuf-like wire format) [^src1].
- **No explicit shuffle phase** — worker processes push data directly to the next node, or keep processing locally up the pipeline [^src1]. Trade-off: there's no fault-tolerant shuffle abstraction, so if a worker dies and loses intermediate results, **Snowflake kills the whole query and restarts it from scratch** (and the customer pays for the restart) — failures are rare enough at their scale/speed that adding partial-retry infrastructure wasn't worth the complexity [^src1].
- **Hash join** is the default (sort-merge supported but rarely chosen); they explicitly expose the join-filter (Bloom filter passed build→probe side) as a separate operator [^src1].

## Work stealing + flexible compute

- **Work stealing** — idle worker processes look for work, querying peers at the same query stage to steal input files. A stealing worker reads stolen files **from S3, not from the slow peer**, to avoid burdening an already-behind node [^src1].
- **Flexible compute** — when a query plan has a portion that would run slowly on the customer's provisioned warehouse, Snowflake farms that sub-plan out to **idle nodes of *other* customers** (combined back via `UNION ALL`). Win-win: query runs faster, Snowflake spends no extra money (the borrowed nodes are already paid for), and the lending customer is unaware [^src1]. Borrowed nodes can't write intermediate results locally (the owner could reclaim them any moment), so results are written back to S3 as if a table — which doubles as a **query-result cache** (catalog records the materialized fragment for reuse) [^src1]. This is the database version of 1980s "cycle scavenging" (Condor), made practical by the cloud's single giant compute pool [^src1].

## Storage format & micro-partitions

By default, data inserted into Snowflake lands in their **proprietary columnar (PAX) format** — predates Parquet/ORC but is "basically equivalent": columnar, dictionary + run-length encoding [^src1]. Incoming data is broken into **micro-partitions** (roughly a Parquet row group): raw ranges of 50–500 MB compressed (via block compression like Snappy/Zstd) down to ~16 MB each [^src1]. Background jobs periodically **re-cluster/resort** micro-partitions based on observed join/access keys — extra work possible only because the format is proprietary and they control ingestion (unlike Dremel/Spark reading random files on S3) [^src1].

**Semi-structured types** unique to Snowflake: `VARIANT` (arbitrary JSON/XML hierarchy), `ARRAY`, and `OBJECT` (single-level variant) [^src1]. Data types for semi-structured fields are inferred **at ingestion** (vs Dremel inferring at runtime), but the original unparsed strings are always kept as a fallback in case the inference is wrong [^src1].

## Optimizer: prune first, adapt at runtime

The optimizer (called the "compiler," Oracle-vernacular) is **Cascades-style top-down** [^src1]. Because external/inserted-table statistics are assumed to be garbage/stale, it operates **without relying on high-quality stats** — only basic **zone maps (min/max ranges per column)**, no histograms or sketches [^src1]. The optimizer's primary early goal is **micro-partition pruning** — throwing away files that can't satisfy the predicate before execution starts [^src1]. To prune against complex expressions (`col1+col2 > N`, `EXTRACT(YEAR ...) = 2024`) it **reuses the runtime expression-evaluation engine** inside the optimizer (reasoning over possible values, not real data) — hard because of null semantics, but avoids the MySQL-style hack of running sub-queries mid-optimization [^src1]. One showcased adaptive optimization: **aggregation push-down below joins**, injected disabled-by-default and triggered at runtime when data volumes exceed the cost-model estimate [^src1].

## Beyond proprietary storage: external & hybrid tables

Snowflake's storage story expanded over time [^src1]:
- **Snowpipe** — a Kafka-style endpoint ingesting Arrow-format data (written into the proprietary format).
- **External tables** (2021) — read data not in the proprietary format (Hive metastore catalogs, Parquet).
- **Apache Iceberg** support (2022) — Parquet + Iceberg metadata; simple insert/update/delete. See [[data-engineering/apache-iceberg|Apache Iceberg]], [[data-engineering/open-table-formats|Open Table Formats]].
- **Hybrid tables / Unistore** (2022) — a full transactional **row store** inside Snowflake; rows land log-structured, then background compaction converts to columnar (a fracture-mirrors / HTAP approach merging row + column data at query time) [^src1]. Compare [[data-engineering/mondaydb|mondayDB]], also a DuckDB-powered HTAP design.

## The Databricks vs Snowflake benchmark war (2021)

Databricks published audited TPC-DS results (Nov 2021) claiming the fastest implementation ever, with a graph beating Snowflake; the two French founders rebutted that Databricks ran Snowflake wrong [^src1]. The crux: Snowflake's published numbers run on data **already ingested into the proprietary format with micro-partition re-clustering done** — preparation that official TPC rules require counting in the measured time — whereas the Databricks/Barcelona run threw raw TPC-DS files at it without preparation [^src1]. Net: a win for Databricks' positioning as a high-performance warehouse (see [[data-engineering/databricks|Databricks]]). Caveat: vendor benchmarks carry well-known TPC-specific optimization tricks ("Volkswagen-style" test detection) [^src1].

## Cross-warehouse view

A second source (Vu Trinh's cloud-warehouse internals survey) corroborates and frames Snowflake against its peers [^src2]: founded **July 2012** by two ex-Oracle engineers plus VectorWise co-founder Marcin Żukowski, built in **C++**, separating compute (proprietary shared-nothing engine on cloud VMs) from storage (S3/GCS) with local-disk caching [^src2]. Distinctively, Snowflake **avoids shuffle-based execution** — workers exchange data directly with one another — unlike BigQuery's Dremel or Databricks' Photon [^src2]. Its **Virtual Warehouses** are abstract "T-shirt sizes" (X-Small→XX-Large); each query runs on exactly one VW with non-shared nodes for performance isolation [^src2]. The worker cache stores **file headers + specific columns** (not whole files), under LRU, and uses **consistent hashing** so queries hitting the same data land on the same node; **file stealing** (reading stolen files from S3, not the busy peer) handles skew [^src2]. Storage uses large immutable files with **min-max-based pruning** [^src2]. See [[data-engineering/cloud-data-warehouse-internals|Cloud Data Warehouse Internals]] for the four-way comparison and [[data-engineering/bigquery|BigQuery]]/[[data-engineering/redshift|Redshift]] for the peers.

## Related

- [[data-engineering/cloud-data-warehouse-internals|Cloud Data Warehouse Internals]] — BigQuery/Snowflake/Databricks/Redshift compared
- [[data-engineering/bigquery|BigQuery]] · [[data-engineering/redshift|Redshift]] — the other shared-disk pioneers
- [[data-engineering/databricks|Databricks]] — the competing lakehouse platform; benchmark rivalry
- [[data-engineering/apache-iceberg|Apache Iceberg]] · [[data-engineering/open-table-formats|Open Table Formats]] — external/Iceberg table support
- [[data-engineering/parquet|Parquet]] — the open analogue of Snowflake's proprietary PAX format
- [[data-engineering/duckdb|DuckDB]] — embedded OLAP engine covered in the same lecture series
- [[data-engineering/apache-spark|Apache Spark]] — Spark SQL / Photon, the contrasting "random files on S3" model
- [[data-engineering/query-engine-routing|Query-Engine Routing]] — multi-engine access over open formats
- [[data-engineering/mondaydb|mondayDB]] — another HTAP serving-layer design
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [CMU Advanced Database Systems — Snowflake (Andy Pavlo)](../../raw/youtube/youtube-nhwp1btg0cw.md)
[^src2]: [The internal of BigQuery, Snowflake, Databricks and Redshift (Vu Trinh)](../../raw/email/email-2025-04-17-the-internal-of-bigquery-snowflake-databricks-and-redshift.md)

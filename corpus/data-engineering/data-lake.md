---
type: concept
domain: data-engineering
status: draft
sources:
  - path: 03_Resources/Study Notes/Data Lake Fundamentals - Apache Iceberg and Parquet.md
    channel: notes
    ingested_at: 2026-05-21
  - path: raw/web/what-is-open-data-infrastructure-blog-fivetran.md
    channel: web
    ingested_at: 2026-06-11
aliases:
  - data lake
  - lakehouse
  - data lakehouse
  - open lake foundation
tags:
  - corpus/data-engineering
  - concept
created: 2026-05-21
updated: 2026-06-11
---

# Data Lake / Lakehouse

**TL;DR**: A data lake is files in cloud object storage (S3, ADLS, GCS) — cheap, flexible, but schema-free and prone to becoming a "data swamp." A lakehouse adds a metadata wrapper (Iceberg, Delta Lake, Hudi) to get data-warehouse reliability on top of lake flexibility [^src1].

## Data lake

Raw files in cloud object storage. No inherent schema enforcement, no transactions, no versioning. Risk: without governance, a data lake becomes a data swamp — files accumulate with no clear lineage or queryability [^src1].

**Strengths:** Storage is cheap. Any format. Unlimited scale.

**Weaknesses:** No ACID, no schema enforcement, no efficient random access.

## Lakehouse

The lakehouse pattern adds an **open table format** (Iceberg, Delta Lake, or Hudi) as a metadata wrapper on top of lake files. This gives:

| Capability | How |
|---|---|
| ACID transactions | Table format tracks write operations atomically |
| Schema enforcement / evolution | Table format owns the schema; files don't need to change |
| Time travel | Snapshots tracked in metadata; query any prior state |
| Efficient querying | Manifest files avoid full-bucket `list_files`; partition pruning skips irrelevant files |

The underlying files remain [Parquet](/data-engineering/parquet.md) — the table format just manages them [^src1].

### The lake as a unified, open foundation

A complementary framing positions the open data lake as the **single universal storage layer** where enterprise data is landed once in open formats, with compute engines and tools evolving on top of a pluggable foundation [^src2]. > "the lake becomes the universal source of truth" [^src2]. The defining moves are storing data once in open table formats (Iceberg, Delta Lake) and separating storage from compute, which avoids vendor-controlled access paths, minimizes data duplication, and preserves cost control [^src2]. This is the lakehouse definition viewed from the open-data-infrastructure angle: the lake plus open table formats is what lets analytics, ML, vector retrieval, and AI agents operate against the same data without copying it between systems [^src2].

> The broader open-data-infrastructure pattern (separating storage/compute/transformation/consumption into pluggable layers) and the medallion/open-table-format machinery are owned elsewhere; this page cites only the lakehouse-as-open-foundation definition.

## Cost hierarchy

```
Storage (cheap) < Compute < Ingress/Egress (expensive)
```

The most important cost optimization is minimizing data read — achieved through columnar formats (Parquet) + partitioning [^src1].

## Partitioning anti-patterns

**Do:** partition on date/time for time-series data — one folder per day is usually optimal.

**Never:** partition on high-cardinality columns (`user_id`, `email`) — creates millions of tiny files; S3 `list_files` becomes the query bottleneck. Iceberg's **hidden partitioning** solves this for transforms while keeping the schema clean [^src1].

## See also

- [Parquet](/data-engineering/parquet.md) — the file format layer
- [Apache Iceberg](/data-engineering/apache-iceberg.md) — the primary open table format covered here
- [Open Table Formats](/data-engineering/open-table-formats.md) — the format layer that promotes a lake to a lakehouse
- [Data Engineering hub](/data-engineering/README.md)

---

[^src1]: [Data Lake Fundamentals - Apache Iceberg and Parquet](/03_Resources/Study Notes/Data Lake Fundamentals - Apache Iceberg and Parquet.md)
[^src2]: [What is Open Data Infrastructure?](../../raw/web/what-is-open-data-infrastructure-blog-fivetran.md)

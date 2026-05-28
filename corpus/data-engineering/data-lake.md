---
type: concept
domain: data-engineering
status: draft
sources:
  - path: 03_Resources/Study Notes/Data Lake Fundamentals - Apache Iceberg and Parquet.md
    channel: notes
    ingested_at: 2026-05-21
aliases:
  - data lake
  - lakehouse
  - data lakehouse
tags:
  - corpus/data-engineering
  - concept
created: 2026-05-21
updated: 2026-05-21
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

The underlying files remain [[data-engineering/parquet|Parquet]] — the table format just manages them [^src1].

## Cost hierarchy

```
Storage (cheap) < Compute < Ingress/Egress (expensive)
```

The most important cost optimization is minimizing data read — achieved through columnar formats (Parquet) + partitioning [^src1].

## Partitioning anti-patterns

**Do:** partition on date/time for time-series data — one folder per day is usually optimal.

**Never:** partition on high-cardinality columns (`user_id`, `email`) — creates millions of tiny files; S3 `list_files` becomes the query bottleneck. Iceberg's **hidden partitioning** solves this for transforms while keeping the schema clean [^src1].

## See also

- [[data-engineering/parquet|Parquet]] — the file format layer
- [[data-engineering/apache-iceberg|Apache Iceberg]] — the primary open table format covered here
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [[03_Resources/Study Notes/Data Lake Fundamentals - Apache Iceberg and Parquet|Data Lake Fundamentals - Apache Iceberg and Parquet]]

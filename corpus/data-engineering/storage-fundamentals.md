---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/email/email-2025-09-28-storage-fundamentals-for-data-engineers.md
    channel: email
    ingested_at: 2026-06-15
  - path: raw/web/data-serialisation-choosing-the-best-format-for-performance.md
    channel: web
    ingested_at: 2026-06-15
  - path: raw/web/file-storage-vs-object-storage-vs-block-storage.md
    channel: web
    ingested_at: 2026-06-15
aliases:
  - storage hierarchy
  - storage fundamentals
  - file storage
  - block storage
  - object storage
  - row-based vs columnar
  - data serialisation
  - serialization
tags:
  - corpus/data-engineering
  - concept
created: 2026-06-15
updated: 2026-06-15
---

# Storage Fundamentals

**TL;DR.** Storage sits at the heart of the data-engineering lifecycle — every stage (ingestion, transformation, serving) stores data multiple times, and storage choices drive cost, performance, and end-user experience [^src1]. Understanding the **storage hierarchy** (raw hardware → storage systems → storage abstractions), the **three cloud storage types** (file / block / object), and **serialisation formats** (row-based vs columnar) lets you avoid bottlenecks and overspend [^src1]. A recurring theme: *start small and practical* — resist jumping to a full lakehouse before the problem demands it [^src1].

## The storage hierarchy

Three layers, bottom-up [^src1]:

**1. Raw hardware ingredients.** Choose by performance, durability, and cost [^src1]:
- **SSD** — flash memory cells (charged = 1); no moving parts, so faster/quieter/more reliable than HDD but pricier per GB [^src1].
- **HDD (magnetic disk)** — spinning platters + read/write head; slower and wear-prone, but cheaper for bulk storage [^src1].
- **RAM** — high-speed volatile memory; data must be moved from disk into RAM (near the CPU) for the CPU to process it efficiently; lost on power-off, more expensive than SSD [^src1].
- **CPU cache** — on-chip memory even faster than RAM (up to ~1 TB/s, few-ns latency) for frequently-used data [^src1].

Supporting processes: **networking** (distributing reads/writes across servers), **serialisation** (memory ↔ disk/network byte conversion), and **compression** (pattern/redundancy encoding to save space and speed reads) [^src1].

**2. Storage systems** — what you actually interact with, built from the raw ingredients [^src1]:
- **Databases** — organised collections managed by a DBMS (query execution, consistency, access control); relational (tables/schemas) or NoSQL (documents, key-value, graphs) [^src1].
- **Object storage** — large-scale unstructured data (files, images, backups), typically cloud (AWS S3) [^src1].

**3. Storage abstractions** — higher-level combinations [^src1]:
- **Data warehouse** — structured, consistent store for analytics (OLAP), combining current + historical data; distinct from OLTP production DBs [^src1].
- **Data lake** — central repository for structured/semi/unstructured data at any scale; **schema-on-read** (store raw, decide schema later); usually on low-cost object storage [^src1].
- **Lakehouse** — lake's raw-data flexibility + warehouse's fast analytics in one system, eliminating constant data movement [^src1].

See [[data-engineering/data-lake|Data Lake / Lakehouse]] for the lake/lakehouse architecture in depth.

## Three cloud storage types

| Type | Structure | Access | Best for |
|---|---|---|---|
| **File** | Hierarchical folders + files with metadata (name, perms, timestamps) | NFS (Unix/Linux) / SMB (Windows) [^src3] | Shared access, simplicity, centralisation over raw performance [^src1] |
| **Block** | Fixed-size blocks with unique IDs; no files/folders/metadata | Attach to server, format with a filesystem (ext4/NTFS/XFS), manage at OS level [^src1] | High-performance/low-latency: transactional DBs, VM disks (e.g. Amazon EBS) [^src1] |
| **Object** | Immutable objects in a flat namespace, each with a unique key, in a container (S3 bucket) | Key-based; objects rewritten whole, not updated in place [^src1] | Petabyte-scale unstructured data; horizontal scaling, durability via replication, parallel reads — backbone of data lakes [^src1] |

Object storage's immutability removes synchronisation overhead and enables high scalability and fault tolerance; examples are AWS S3, Google Cloud Storage, Azure Blob Storage [^src1].

## Serialisation: row-based vs columnar

Serialisation converts in-memory data into a byte sequence for disk/network; the **layout** determines query performance [^src2]:

- **Row-based** — stores each row as a unit, all columns together. Optimal for transactional (OLTP) operations that read/modify whole records. Used by MySQL, SQLite, SQL Server, PostgreSQL [^src2]. Weakness: analytical queries reading a few columns must scan whole rows; adding a column rewrites all rows [^src2]. Formats: **CSV** (human-readable, no types), **XML** (legacy, slow), **JSON / JSONL** (hierarchical / line-delimited; repeated column names cost space), **Avro** (compact binary, schema in JSON, schema-evolution, splittable) [^src2].
- **Columnar** — stores each column's values together. Ideal for warehousing/analytics that aggregate specific columns; highly compressible, self-indexing, faster `AVG/MIN/MAX`. Used by Redshift, BigQuery, [[data-engineering/duckdb|DuckDB]] [^src2]. Canonical format: **[[data-engineering/parquet|Apache Parquet]]**.

The row/columnar split is the same physical distinction underlying OLTP databases vs analytical [[data-engineering/parquet|Parquet]]/[[data-engineering/apache-iceberg|Iceberg]] tables.

## Choosing a storage solution

No one-size-fits-all; weigh: performance (read/write speed), scalability, accessibility (SLAs), metadata management, query support, schema flexibility, data quality & governance/lineage, and compliance (data residency) [^src1].

**Maturity-dependent responsibilities** [^src1]:
- *Early-stage org* — the DE often owns the whole storage setup end-to-end (request a prod-DB replica, spin up a DB, pick cloud storage). Key discipline: **start small** — "resist the temptation to jump straight to advanced platforms like Databricks or a full lakehouse"; ask *do we need this right now, and what problem would it solve that we actually face today?* [^src1].
- *Mature org* — more specialised; work within an existing platform alongside dedicated ingestion/transformation/governance teams [^src1].

This mirrors the broader [[data-engineering/data-engineer-role|data-engineer-role]] principle of working backward from requirements rather than from tools.

## Related

- [[data-engineering/data-lake|Data Lake / Lakehouse]] — the lake/lakehouse abstraction
- [[data-engineering/parquet|Apache Parquet]] — the canonical columnar format
- [[data-engineering/data-engineering-best-practices|Data Engineering Best Practices]] — storage layering in pipeline design
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [Storage Fundamentals for Data Engineers](../../raw/email/email-2025-09-28-storage-fundamentals-for-data-engineers.md)
[^src2]: [Data Serialisation: Choosing the Best Format for Performance](../../raw/web/data-serialisation-choosing-the-best-format-for-performance.md)
[^src3]: [File Storage vs Object Storage vs Block Storage](../../raw/web/file-storage-vs-object-storage-vs-block-storage.md)

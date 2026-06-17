---
type: entity
domain: data-engineering
status: draft
sources:
  - path: 03_Resources/Articles/scd2-table-creation-merge-into-spark-iceberg.md
    channel: notes
    ingested_at: 2026-05-07
  - path: 03_Resources/Study Notes/Data Lake Fundamentals - Apache Iceberg and Parquet.md
    channel: notes
    ingested_at: 2026-05-21
  - path: raw/_inbox/email-2025-09-24-understanding-open-table-formats-with-apache-iceberg.md
    channel: email
    ingested_at: 2026-06-11
  - path: raw/youtube/youtube-4bg64wnkfge.md
    channel: youtube
    ingested_at: 2026-06-17
aliases:
  - Apache Iceberg
  - Iceberg
  - iceberg
tags:
  - corpus/data-engineering
  - entity
created: 2026-05-07
updated: 2026-06-11
---

# Apache Iceberg

**TL;DR**: Open table format that adds a transactional metadata layer on top of [[data-engineering/parquet|Parquet]] files in object storage — giving data lakes ACID transactions, schema evolution, time travel, and partition pruning without a traditional database engine [^src1][^src2].

Iceberg is the **table format layer**. Parquet is the **file format layer** underneath it.

## Open table format positioning

Iceberg is one of three major **open table formats (OTFs)** — alongside Apache Hudi and Delta Lake — distinct from **file formats** (Parquet, ORC) [^src3]. The distinction is the recurring source of confusion: an OTF is not merely "a pointer to some metadata files"; it is a specification layer that turns a directory of files into a table with transactional semantics [^src3]. See [[data-engineering/open-table-formats|open table formats]] for the cross-format comparison; this page covers the Iceberg-specific implementation.

The "open" in OTF means the format is a published standard, not tied to one vendor's engine — multiple query engines (Trino, Spark, DuckDB, etc.) can read and write the same table, which underpins the open-data-infrastructure / lakehouse story [^src3].

## Key features

| Feature | What It Does |
|---|---|
| **Schema Evolution** | Add, drop, or rename columns without a full table rewrite [^src2] |
| **Time Travel** | Query the table as it existed at any past snapshot [^src2] |
| **ACID Transactions** | Safe concurrent reads and writes; no dirty reads [^src2] |
| **Hidden Partitioning** | Partition on `day(event_timestamp)` without adding a column to the schema [^src2] |
| **Partition Pruning** | Automatically skip partitions that don't match the `WHERE` clause [^src2] |
| **Manifest Files** | Iceberg tracks all underlying Parquet files internally — avoids expensive S3 `list_files` calls [^src2] |
| **MERGE INTO** | Enables atomic multi-action DML in Spark SQL [^src1] |

## Role in the data stack

Without Iceberg (or Delta Lake / Hudi), Spark SQL cannot perform atomic multi-action DML (`MERGE INTO`) against a table. Iceberg is a prerequisite for SCD2 pipelines in Spark [^src1].

In a lakehouse architecture, Iceberg is the metadata wrapper that promotes a data lake (files in S3/GCS/ADLS) to a data warehouse experience — adding reliability and queryability without moving data [^src2].

## Format evolution: V1 → V2 → V3 → V4

Russell Spitzer (Iceberg PMC) frames the format's history as a sequence of capability additions, each driven by use cases brought to the community [^src4]:

- **V1** — only three atomic operations: **add, remove, or replace data files** [^src4]. Enough to build a fully transactional system (appends, deletes, insert-override) on files in storage, but row-level changes were "really, really expensive": changing a few rows in a large file meant rewriting the whole file. GDPR / right-to-be-forgotten made this untenable at scale [^src4].
- **V2** — added **delete files** enabling **row-level deletes/updates without rewriting unchanged data** ("merge on read": read the delete file + its data file together to reconstruct the current table) [^src4]. Crucially, the table changes *only by adding files*, so the metadata layer grows monotonically [^src4].
- **V3** — position delete replacement, new **`variant` and `geo` types**, and **encryption support** [^src4].
- **V4** — work began less than a week after V3 was ratified (May 29, 2025), targeting **streaming and AI** use cases [^src4].

Iceberg has also grown **beyond the table-format spec** into an interoperability stack: catalog protocol, interoperable **views**, **Puffin** blob/index files, and a recently-added UDF-portability spec — with Java, Python, Rust, Go, and C++ implementations [^src4].

## V4 roadmap: streaming + AI

**Streaming** problems V4 targets [^src4]:
- Adding one small commit currently forces writing a data file **and** a single-row manifest **and** rewriting the manifest list — metadata grows by a file per commit, and reading recent data needs a multi-hop read (manifest list → manifest → data). Teams work around it with aggressive metadata compaction [^src4].
- **Root manifest** — a top-level manifest file that can hold *either* manifests or data files directly, collapsing the hierarchy. Writers append straight to the root with no intercessor manifest; **column statistics** (not just partition stats) propagate up for pruning [^src4].
- **Adaptive metadata tree** — the root acts as a buffer, spinning off a leaf manifest only once enough files accumulate, **at write time** — no separate rewrite-manifest compaction action. Small/streaming tables can live entirely at the root level: one IO between query and data [^src4].

**AI** problems V4 targets — three issues with feature-store / LLM-training workloads [^src4]:
- **Wide tables** — feature stores reach thousands–tens of thousands of columns; Iceberg's model requires one file holding *every* column, so wider tables force shorter (fewer-row) files [^src4].
- **Column updates** — AI tables grow "to the right" (adding/replacing whole feature columns) rather than down (adding rows); V1–V3 only had add/remove *files* or *rows* as first-class ops [^src4].
- **Multimodal data** — a single column may hold a large JPEG/video blob, dominating file size [^src4].

The V4 answer mirrors the V2 move: allow a column to live in a **separate column file** from the base file, giving **add/remove/change at the column level** [^src4]. A V4 table will support add/remove/change for **files, rows, *and* columns** [^src4]. These same row/column-delete capabilities are also being applied to the **metadata layer** — e.g. removing a data file via a row-delete on a manifest instead of rewriting the manifest, making the metadata layer far more cacheable [^src4].

> Governance note: Spitzer stresses Iceberg's "open" rests on three legs — open standard, open code, and most importantly **open governance** — invoking Conway's Law: an interoperating format needs an interoperating community [^src4]. Project scale: 13,000+ commits and 1,500+ unique contributors across all implementations [^src4].

## SQL examples (Trino)

**Create an Iceberg table with partitioning and sorting:**
```sql
CREATE TABLE schema.nba_game_details (
    player_name VARCHAR,
    season      INTEGER,
    game_date   DATE
)
WITH (
    format       = 'PARQUET',
    partitioning = ARRAY['season'],
    sorted_by    = ARRAY['player_name', 'game_date']
);
```

**Hidden partitioning on a timestamp:**
```sql
CREATE TABLE schema.events (
    event_id        BIGINT,
    event_timestamp TIMESTAMP
)
WITH (
    format       = 'PARQUET',
    partitioning = ARRAY['day(event_timestamp)']
);
```

**Inspect underlying files:**
```sql
SELECT file_path, record_count, file_size_in_bytes, partition
FROM "schema.nba_game_details$files";
```

**Validate partition pruning:**
```sql
SHOW STATS FOR (
    SELECT * FROM schema.nba_game_details WHERE season = 2022
);
```
[^src2]

## See also

- [[data-engineering/parquet|Parquet]] — the file format Iceberg manages
- [[data-engineering/merge-into|MERGE INTO]] — Spark SQL operation enabled by Iceberg
- [[data-engineering/scd2|SCD2]] — primary use case combining Iceberg + MERGE INTO
- [[data-engineering/data-lake|Data Lake / Lakehouse]] — architecture context for Iceberg
- [[data-engineering/open-table-formats|Open Table Formats]] — Iceberg vs. Hudi vs. Delta Lake comparison
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [[03_Resources/Articles/scd2-table-creation-merge-into-spark-iceberg|SCD2 Table Creation with MERGE INTO in Spark and Iceberg]]
[^src2]: [[03_Resources/Study Notes/Data Lake Fundamentals - Apache Iceberg and Parquet|Data Lake Fundamentals - Apache Iceberg and Parquet]]
[^src3]: [Understanding Open Table Formats with Apache Iceberg](../../raw/email/email-2025-09-24-understanding-open-table-formats-with-apache-iceberg.md)
[^src4]: [Apache Iceberg Summit Keynote — the future of Iceberg (Russell Spitzer)](../../raw/youtube/youtube-4bg64wnkfge.md)

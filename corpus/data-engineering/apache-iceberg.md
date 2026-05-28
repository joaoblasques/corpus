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
aliases:
  - Apache Iceberg
  - Iceberg
  - iceberg
tags:
  - corpus/data-engineering
  - entity
created: 2026-05-07
updated: 2026-05-21
---

# Apache Iceberg

**TL;DR**: Open table format that adds a transactional metadata layer on top of [[data-engineering/parquet|Parquet]] files in object storage — giving data lakes ACID transactions, schema evolution, time travel, and partition pruning without a traditional database engine [^src1][^src2].

Iceberg is the **table format layer**. Parquet is the **file format layer** underneath it.

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
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [[03_Resources/Articles/scd2-table-creation-merge-into-spark-iceberg|SCD2 Table Creation with MERGE INTO in Spark and Iceberg]]
[^src2]: [[03_Resources/Study Notes/Data Lake Fundamentals - Apache Iceberg and Parquet|Data Lake Fundamentals - Apache Iceberg and Parquet]]

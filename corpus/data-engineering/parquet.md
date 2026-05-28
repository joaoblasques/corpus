---
type: entity
domain: data-engineering
status: draft
sources:
  - path: 03_Resources/Study Notes/Data Lake Fundamentals - Apache Iceberg and Parquet.md
    channel: notes
    ingested_at: 2026-05-21
aliases:
  - Parquet
  - Apache Parquet
  - parquet
  - columnar file format
tags:
  - corpus/data-engineering
  - entity
created: 2026-05-21
updated: 2026-05-21
---

# Apache Parquet

**TL;DR**: A binary, column-oriented file format for analytical data. Replaces CSV for any serious data work by enabling column pruning, lossless compression, and dramatic I/O reduction for analytical queries [^src1].

Parquet is the **file format layer**. [[data-engineering/apache-iceberg|Apache Iceberg]] is the **table format layer** that sits on top of Parquet files to add transactional metadata.

## Columnar storage

Data is stored column-by-column, not row-by-row. Analytical queries typically touch only a few columns across many rows — columnar storage means only the needed columns are read from disk.

> "Queries only read the columns they need → less I/O → lower egress cost." [^src1]

Egress cost (data moved out of cloud storage) is typically the most expensive data-engineering cost. Columnar format directly reduces it.

## Compression

Only lossless compression is acceptable for data engineering. Two core mechanisms [^src1]:

### Run Length Encoding (RLE)

Stores consecutive repeated values as `(value, count)` instead of repeating the value. Maximally effective when similar values are adjacent.

### Sort order for maximum compression

**Sort columns low cardinality → high cardinality** to maximize RLE effectiveness [^src1]:

```
Example: listing_id, date, availability_status
Sort order: listing_id first (each listing has 365 rows with similar values)
→ 400 identical values compressed to 1 entry
→ 10 GB → 0.3 GB (97% reduction)
```

This sort-order strategy is one of the highest-leverage performance optimizations in data lake engineering.

## Partitioning

Organize Parquet files into subdirectories by column value to enable **partition pruning** — queries skip entire partitions that don't match the `WHERE` clause [^src1].

**Best practices:**
- Time-based is most common (`date`, `year/month`); one folder per day is usually right
- Partition on low-cardinality columns only

**Anti-pattern:** Never partition on high-cardinality columns (`user_id`, `email`) — creates millions of tiny files, making S3 `list_files` the bottleneck [^src1].

## Iceberg adds the table format layer

Parquet alone is just files. [[data-engineering/apache-iceberg|Apache Iceberg]] wraps Parquet with:
- Manifest files that track all Parquet files (avoids expensive S3 `list_files`)
- ACID transactions, schema evolution, time travel
- Hidden partitioning (partition on `day(event_timestamp)` without adding a column)

## SQL example (Trino / Iceberg table backed by Parquet)

```sql
CREATE TABLE schema.nba_game_details (
    player_name VARCHAR,
    season      INTEGER,
    game_date   DATE
)
WITH (
    format     = 'PARQUET',
    partitioning = ARRAY['season'],
    sorted_by  = ARRAY['player_name', 'game_date']
);
```
[^src1]

## See also

- [[data-engineering/apache-iceberg|Apache Iceberg]] — table format layer on top of Parquet
- [[data-engineering/data-lake|Data Lake / Lakehouse]] — storage architecture that uses Parquet as the file format
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [[03_Resources/Study Notes/Data Lake Fundamentals - Apache Iceberg and Parquet|Data Lake Fundamentals - Apache Iceberg and Parquet]]

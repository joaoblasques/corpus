---
type: entity
domain: data-engineering
status: draft
sources:
  - path: 03_Resources/Study Notes/Data Lake Fundamentals - Apache Iceberg and Parquet.md
    channel: notes
    ingested_at: 2026-05-21
  - path: raw/web/apache-parquet-for-data-engineers-optimized-data-storage.md
    channel: web
    ingested_at: 2026-06-16
  - path: raw/email/email-2025-05-08-back-to-the-basics-what-is-columnar-storage.md
    channel: email
    ingested_at: 2026-06-19
aliases:
  - Parquet
  - Apache Parquet
  - parquet
  - columnar file format
  - ORC
  - Apache ORC
  - columnar storage
  - vectorized execution
tags:
  - corpus/data-engineering
  - entity
created: 2026-05-21
updated: 2026-06-23
---

# Apache Parquet

**TL;DR**: A binary, column-oriented file format for analytical data. Replaces CSV for any serious data work by enabling column pruning, lossless compression, and dramatic I/O reduction for analytical queries [^src1].

Parquet is the **file format layer**. [Apache Iceberg](/data-engineering/apache-iceberg.md) is the **table format layer** that sits on top of Parquet files to add transactional metadata.

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

## Physical layout: row groups → column chunks → pages

A Parquet file is a hierarchical structure with three nested units [^src2]:

- **Row group** — a large chunk holding the column data for a *subset of rows*; contains one column chunk per column. By default Parquet splits data into ~1 GB files (configurable), producing multiple `.parquet` files [^src2].
- **Column chunk** — stores the data for a *single column* within a row group; divided into pages.
- **Page** — the smallest storage unit. Page types include **data pages** (the actual column data), **dictionary pages** (unique values for dictionary encoding), and **index pages** (index info for faster retrieval) [^src2].

> "Pages are the smallest unit of data storage in Parquet." [^src2]

## Predicate pushdown via min/max statistics

Each column in a row group carries **min/max statistics** in its metadata. Query engines use these to skip entire row groups that can't satisfy a filter — this is **predicate pushdown**, applied at row-group selection time during reads [^src2].

This is a distinct mechanism from partition pruning (above): pruning skips whole files/directories before the file is opened, while min/max statistics skip row groups *inside* a file. They compose. See [Query Engine Routing](/data-engineering/query-engine-routing.md) for how engines exploit these read-time optimizations.

## Footer metadata (self-describing files)

Parquet files are self-describing: schema and statistics live in the file itself, so query engines don't need to infer or be told the schema when reading [^src2]. Metadata appears at multiple levels [^src2]:

- **File header / footer** — a magic number plus file-level properties (schema, compression algorithms). The **footer** holds the authoritative metadata read first on open: schema, row-group details, and column metadata.
- **Row-group metadata** — number of rows, per-column statistics (min/max), and encoding used.
- **Page metadata** — size, compression type, and decoding specifics per page.

Parquet files are **immutable** once written [^src2].

## Encoding schemes

Beyond the Run Length Encoding covered above, Parquet applies **dictionary encoding** to compress columns with many repeated values: a dictionary page stores the unique values, and data pages store references (indices) into that dictionary rather than the raw values [^src2].

## Compression codecs

Parquet supports multiple pluggable compression codecs — **Snappy, Gzip, and LZO** among them — applied per column chunk [^src2]. (Snappy is the common default in practice; the source's write example specifies `compression='SNAPPY'`.) These operate *in addition to* the encoding schemes above.

## Nested data: the Dremel model

Parquet's columnar layout for nested/repeated structures derives from Google's **Dremel paper** (the same lineage as BigQuery) [^src2]. A record's schema-tree is flattened depth-first into one leaf column per primitive field (e.g. `Name.Language.Code`), and two compact per-value markers reconstruct structure on read [^src2]:

- **Repetition level (R)** — depth of nesting for repeated fields; increments when traversing repeated fields.
- **Definition level (D)** — whether a value is defined vs. null; increments when traversing optional fields.

This lets Parquet store `struct`, `array`, optional, and repeated fields efficiently without reading data that a query doesn't touch [^src2].

## Supported data types

Parquet keeps a minimal set of **primitive types** — `BOOLEAN`, `INT32`, `INT64`, `INT96`, `FLOAT`, `DOUBLE`, `BYTE_ARRAY`, `FIXED_LEN_BYTE_ARRAY` — and layers **logical types** on top via annotations to interpret them; e.g. a string is a `BYTE_ARRAY` with a `UTF8` annotation [^src2].

## Limitations

Parquet is optimized for read-heavy analytics, not transactional workloads. The source notes it is **not ideal for small, transactional datasets** (row-group/page overhead), writes can be slower than other formats, and being binary it is **not human-readable** [^src2].

## Why columnar wins for analytics

Parquet is the canonical columnar format; the deeper question is *why* columnar storage suits analytics at all [^src3]. Four reasons [^src3]:

- **Performance (less I/O)** — analytical queries touch a few of many columns; a columnar engine reads **only the relevant columns**, scanning less data, whereas row-based systems must read whole rows even for one field [^src3].
- **Compression** — storing values of the same type together compresses far better [^src3]. Beyond RLE and dictionary encoding (above), the article names **bit-packing** (use only the minimum bits needed for small numeric values) and **delta encoding** (store the difference between consecutive values) [^src3].
- **Vectorized processing** — columnar layout unlocks **vectorized execution**: operations applied to batches of column values at once, letting engines (DuckDB, Presto, Spark) use **SIMD** (Single Instruction, Multiple Data) CPU instructions to evaluate e.g. `price > 100` across a whole column segment in one shot [^src3].
- **Parallelism** — each column stored separately can be read in parallel across CPU cores/nodes [^src3].

Caveat: **not every OLAP warehouse is a column store** — DDIA notes traditional row-oriented and other architectures are also used; columnar is a strong default for analytics, not a law [^src3].

## ORC: the other columnar format

**Apache ORC** (Optimized Row Columnar) is a Hadoop-native columnar format focused on deep compression, efficient storage, and built-in indexing; it grew popular with Hive and often outperforms older formats like RCFile [^src3]. Its internal units parallel Parquet's [^src3]:

- **Stripes** — the largest unit; each holds rows and is independently compressed and indexed (analogous to Parquet row groups).
- **Row Index** — lets the reader skip data blocks that don't match query criteria.
- **Stripe Footer** — column-level metadata and statistics (min/max, count, nulls).
- **File Footer** — global metadata: schema, column encodings, file-level stats.
- **Postscript** — compression-algorithm and versioning info.

## Real-world columnar at scale

Two petabyte-scale cases (note: lessons apply at PB scale, not to a 100 GB warehouse — "don't let FOMO push you into rearchitecting") [^src3]:

- **Uber** — manages hundreds of PB with Parquet as the primary format; switching compression from SNAPPY/Gzip to **Zstandard (ZSTD)** yielded up to **39% smaller files** and improved query performance (lower vCore usage). They also built high-throughput **column deletion / reordering** tools — pruning unused columns saved PB-level space on a single table; many improvements (ZSTD, column pruning) were contributed back to open-source Parquet [^src3].
- **Criteo** — ~30 billion events/day; migrated nearly a petabyte from **RCFile to Parquet** for better engine support (Cascading/Pig/Spark/Impala) and compression; Gzip-compressed Parquet matched or beat RCFile with added storage efficiency [^src3].

## Iceberg adds the table format layer

Parquet alone is just files. [Apache Iceberg](/data-engineering/apache-iceberg.md) wraps Parquet with:
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

- [Apache Iceberg](/data-engineering/apache-iceberg.md) — table format layer on top of Parquet
- [Apache Spark](/data-engineering/apache-spark.md) — pairs Parquet with Catalyst column pruning + predicate pushdown (min/max stats)
- [Cloud Data Warehouse Internals](/data-engineering/cloud-data-warehouse-internals.md) — the hybrid row-group/column-chunk layout Parquet shares with BigQuery/Snowflake/Databricks
- [Data Lake / Lakehouse](/data-engineering/data-lake.md) — storage architecture that uses Parquet as the file format
- [Dimensional Modeling](/data-engineering/dimensional-modeling.md) — how joins/shuffles destroy RLE compression (temporal cardinality explosion)
- [Data Engineering hub](/data-engineering/README.md)

---

[^src1]: [Data Lake Fundamentals - Apache Iceberg and Parquet](/03_Resources/Study Notes/Data Lake Fundamentals - Apache Iceberg and Parquet.md)
[^src2]: [Apache Parquet for Data Engineers](../../raw/web/apache-parquet-for-data-engineers-optimized-data-storage.md)
[^src3]: [Back To The Basics: What Is Columnar Storage (SeattleDataGuy)](../../raw/email/email-2025-05-08-back-to-the-basics-what-is-columnar-storage.md)

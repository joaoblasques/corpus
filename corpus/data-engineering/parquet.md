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
aliases:
  - Parquet
  - Apache Parquet
  - parquet
  - columnar file format
tags:
  - corpus/data-engineering
  - entity
created: 2026-05-21
updated: 2026-06-16
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

## Physical layout: row groups → column chunks → pages

A Parquet file is a hierarchical structure with three nested units [^src2]:

- **Row group** — a large chunk holding the column data for a *subset of rows*; contains one column chunk per column. By default Parquet splits data into ~1 GB files (configurable), producing multiple `.parquet` files [^src2].
- **Column chunk** — stores the data for a *single column* within a row group; divided into pages.
- **Page** — the smallest storage unit. Page types include **data pages** (the actual column data), **dictionary pages** (unique values for dictionary encoding), and **index pages** (index info for faster retrieval) [^src2].

> "Pages are the smallest unit of data storage in Parquet." [^src2]

## Predicate pushdown via min/max statistics

Each column in a row group carries **min/max statistics** in its metadata. Query engines use these to skip entire row groups that can't satisfy a filter — this is **predicate pushdown**, applied at row-group selection time during reads [^src2].

This is a distinct mechanism from partition pruning (above): pruning skips whole files/directories before the file is opened, while min/max statistics skip row groups *inside* a file. They compose. See [[data-engineering/query-engine-routing|Query Engine Routing]] for how engines exploit these read-time optimizations.

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
[^src2]: [Apache Parquet for Data Engineers](../../raw/web/apache-parquet-for-data-engineers-optimized-data-storage.md)

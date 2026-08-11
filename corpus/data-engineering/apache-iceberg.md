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
  - path: raw/email/email-2025-09-24-understanding-open-table-formats-with-apache-iceberg.md
    channel: email
    ingested_at: 2026-06-11
  - path: raw/youtube/youtube-4bg64wnkfge.md
    channel: youtube
    ingested_at: 2026-06-17
  - path: raw/_inbox/web-the-iceberg-ecosystem-today-anders-swanson-3afb0089.md
    channel: web
    ingested_at: 2026-08-11
  - path: raw/_inbox/web-inside-snowflakes-ai-roadmap-w-chris-child-fe3830a6.md
    channel: web
    ingested_at: 2026-08-11
  - path: raw/_inbox/web-under-the-hood-of-apache-iceberg-w-christian-thiel-2573cee1.md
    channel: web
    ingested_at: 2026-08-11
  - path: raw/_inbox/web-the-future-of-the-lakehouse-delta-lake-rust-and-data-platfor-8d2f4c75.md
    channel: web
    ingested_at: 2026-08-11
  - path: raw/_inbox/web-how-amazon-s3-works-w-andy-warfield-b9737b60.md
    channel: web
    ingested_at: 2026-08-11
aliases:
  - Apache Iceberg
  - Iceberg
  - iceberg
  - Lakekeeper
  - Iceberg REST catalog
  - vended credentials
  - external catalog
  - four-part namespace
  - S3 table buckets
tags:
  - corpus/data-engineering
  - entity
created: 2026-05-07
updated: 2026-08-11
---

# Apache Iceberg

**TL;DR**: Open table format that adds a transactional metadata layer on top of [Parquet](/data-engineering/parquet.md) files in object storage — giving data lakes ACID transactions, schema evolution, time travel, and partition pruning without a traditional database engine [^src1][^src2].

Iceberg is the **table format layer**. Parquet is the **file format layer** underneath it.

## Open table format positioning

Iceberg is one of three major **open table formats (OTFs)** — alongside Apache Hudi and Delta Lake — distinct from **file formats** (Parquet, ORC) [^src3]. The distinction is the recurring source of confusion: an OTF is not merely "a pointer to some metadata files"; it is a specification layer that turns a directory of files into a table with transactional semantics [^src3]. See [open table formats](/data-engineering/open-table-formats.md) for the cross-format comparison; this page covers the Iceberg-specific implementation.

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

## Iceberg ecosystem in production (2026)

From Anders Swanson (dbt Labs developer experience advocate) [^src5]:

**Three phases of Iceberg integration:**
1. **Naive** — point engine at Parquet/JSON in object storage; reading works, but no version tracking
2. **REST catalog** — engines connect to an Iceberg REST catalog to get the current table version; eliminates path management
3. **Schema-scale** — discovery of new tables, schema synchronization, multi-table transactions; "producer-led sharing" where the upstream team writes to a shared catalog and downstream engines see it automatically

**Catalog model:** Internal catalogs (Snowflake, SQL Server) vs. external catalogs (e.g., Lakekeeper, AWS Glue). The trend is a **four-part namespace** — `catalog.database.schema.identifier` — following Spark, Databricks Unity Catalog, and Snowflake catalog-link approaches [^src5].

**Vended credentials** solve the "two keys" problem: authenticate once to the catalog; the catalog vends short-lived object-store credentials so you don't manage separate S3 keys [^src5]. Vended credentials do NOT solve cross-platform identity/grants — that remains the hardest unsolved problem [^src5].

**Metadata performance** is the practical pain point: if listing tables in a federated world takes 5 seconds, users blame the query engine even if the external catalog is slow. Snowflake catalog-link databases mirror/cache metadata for native performance; DuckDB deliberately excludes external catalog tables from information_schema listing today [^src5].

> "The making of a treaty is the treaty... The goodwill is the standard." — Anders Swanson, on why unprecedented vendor collaboration on Iceberg matters more than any specific feature [^src5]

**Lakekeeper** (Christian Thiel, co-lead architect) is one of the most widely-used Iceberg catalogs as of 2026 [^src6].

## Delta Lake and open Iceberg ecosystem (Ethan, delta-rs maintainer)

Podcast conversation with Ethan (delta-rs maintainer, pharmaceutical industry) on open table formats and enterprise lakehouse architecture [^src7]:

- **delta-rs** — the Rust implementation of the Delta Lake protocol; enables Delta table reads/writes outside Spark (Python, Rust, DuckDB, other engines). Ethan is a project maintainer and works on multi-engine lakehouse infrastructure in regulated environments (pharma).
- **Delta Lake and Iceberg converging** — both formats are "becoming one" at the governance/catalog layer (Unity Catalog bridging Delta ↔ Iceberg via UniForm); the distinction between the two is narrowing for most practical use cases.
- **Open catalogs** — Iceberg REST catalog and Databricks Unity Catalog are converging as the de facto open lakehouse catalog protocols; catalog-first architecture is now the primary way multi-engine access is managed safely.
- **Rust in the data ecosystem** — Rust's performance and safety profile make it a natural fit for data infrastructure (DataFusion, DuckDB's Rust-written extensions, delta-rs), especially where latency and correctness matter.
- **Enterprise data platform in pharma** — data governance and auditability requirements in regulated industries are not optional; Iceberg's time travel and metadata immutability are directly valuable there.
- **Agentic analytics** — Ethan discusses the future of AI-enabled data systems: agents need stable, versioned, schema-aware table formats; open table formats and open catalogs are the infrastructure enabler for agentic pipelines (same direction as [dbt Roundup's agentic analytics thesis](/data-engineering/dbt.md)).

## Amazon S3 and Iceberg (S3 table buckets)

AWS VP Andy Warfield: S3 evolved from storage into a compute-adjacent layer; **S3 table buckets** are AWS's managed Iceberg offering — Iceberg tables stored and served natively from S3 without a separate catalog service [^src8]. This blurs the storage/catalog line and extends S3's role from object store to managed table layer.

## See also

- [Parquet](/data-engineering/parquet.md) — the file format Iceberg manages
- [MERGE INTO](/data-engineering/merge-into.md) — Spark SQL operation enabled by Iceberg
- [SCD2](/data-engineering/scd2.md) — primary use case combining Iceberg + MERGE INTO
- [Data Lake / Lakehouse](/data-engineering/data-lake.md) — architecture context for Iceberg
- [Open Table Formats](/data-engineering/open-table-formats.md) — Iceberg vs. Hudi vs. Delta Lake comparison
- [Snowflake](/data-engineering/snowflake.md) — Iceberg integration and catalog-link
- [Databricks](/data-engineering/databricks.md) — Unity Catalog and Delta Lake / Iceberg convergence
- [Data Engineering hub](/data-engineering/README.md)

---

[^src1]: [SCD2 Table Creation with MERGE INTO in Spark and Iceberg](/03_Resources/Articles/scd2-table-creation-merge-into-spark-iceberg.md)
[^src2]: [Data Lake Fundamentals - Apache Iceberg and Parquet](/03_Resources/Study Notes/Data Lake Fundamentals - Apache Iceberg and Parquet.md)
[^src3]: [Understanding Open Table Formats with Apache Iceberg](../../raw/email/email-2025-09-24-understanding-open-table-formats-with-apache-iceberg.md)
[^src4]: [Apache Iceberg Summit Keynote — the future of Iceberg (Russell Spitzer)](../../raw/youtube/youtube-4bg64wnkfge.md)
[^src5]: raw/_inbox/web-the-iceberg-ecosystem-today-anders-swanson-3afb0089.md
[^src6]: raw/_inbox/web-under-the-hood-of-apache-iceberg-w-christian-thiel-2573cee1.md
[^src7]: raw/_inbox/web-the-future-of-the-lakehouse-delta-lake-rust-and-data-platfor-8d2f4c75.md
[^src8]: raw/_inbox/web-how-amazon-s3-works-w-andy-warfield-b9737b60.md

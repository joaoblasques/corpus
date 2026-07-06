---
type: synthesis
domain: data-engineering
status: draft
sources:
  - path: raw/email/email-2025-04-17-the-internal-of-bigquery-snowflake-databricks-and-redshift.md
    channel: email
    ingested_at: 2026-06-19
  - path: raw/email/email-2025-09-28-storage-fundamentals-for-data-engineers.md
    channel: email
    ingested_at: 2026-06-15
  - path: raw/email/email-2025-05-15-if-you-re-learning-kafka-this-article-is-for-you.md
    channel: email
    ingested_at: 2026-06-19
  - path: raw/web/web-what-to-look-for-in-a-serverless-database-for-ai-application-8e1ddee7.md
    channel: web
    ingested_at: 2026-07-06
  - path: raw/web/web-what-is-serverless-postgresql-3e7858c3.md
    channel: web
    ingested_at: 2026-07-06
aliases:
  - compute-storage decoupling
  - compute storage separation
  - disaggregated storage and compute
  - storage compute disaggregation
  - object storage as the substrate
tags:
  - corpus/data-engineering
  - synthesis
created: 2026-06-23
updated: 2026-07-06
confidence: 0.8
last_confirmed: 2026-07-06
---

# Compute–Storage Decoupling

**TL;DR.** The dominant architectural move of the 2010s–2020s data stack is the **separation of compute from storage**, with durable state pushed down to **cloud object storage** (S3 / GCS / Azure Blob) and stateless(-ish) compute scaled independently on top. This page is the cross-paradigm synthesis: the *same* decoupling shows up in **cloud data warehouses**, in the **lakehouse**, and — most recently — in **event streaming**. Three corpus clusters that were ingested separately turn out to describe one convergent pattern.

## The pattern

Object storage is the load-bearing primitive. It is an immutable, flat-namespace, key-addressed store that scales horizontally, achieves durability through replication, and supports massively parallel reads — which is exactly why it became "the backbone of data lakes" [^src2]. Once durable state lives in object storage, **compute becomes an elastic, swappable layer**: you can add/remove query workers, restart them, or run several engines against the same bytes without moving data. The trade-off is latency — object storage is rewritten-whole, not updated-in-place, and each read can cost real money and network round-trips [^src2].

## Three paradigms, one move

### Cloud data warehouses — share-nothing → shared-disk

The 2010s saw the **cloud-native shared-disk OLAP** system emerge (BigQuery 2010, Snowflake 2012): data stored **separately in object storage**, the vendor managing the storage layer, users getting distributed query power without managing infrastructure [^src1]. This *is* compute–storage decoupling, and it reshapes each engine's optimizations — Snowflake **caches aggressively** and uses **file stealing** precisely *because* every S3 read costs money; BigQuery went further and **separated the shuffle layer** into distributed storage so compute and shuffle scale independently [^src1]. Even Redshift, the share-nothing holdout, later bolted on **RMS** (S3-backed) to get storage/compute separation in RA3/serverless [^src1]. The full four-way comparison lives in [Cloud Data Warehouse Internals](/data-engineering/cloud-data-warehouse-internals.md).

### The lakehouse — a metadata log over object storage

The **lakehouse** combines a lake's raw-data flexibility with a warehouse's fast analytics in one system, eliminating constant data movement [^src2]. Its enabling trick is also decoupling: an open table format records *which* object-storage files belong to a table via a metadata layer. Databricks' **Delta Lake** is an ACID layer that tracks the Parquet objects belonging to a table through a **write-ahead log in cloud object storage** — a file unreferenced by the log is simply unreadable [^src1]. Compute (Photon/Spark) and the bytes (Parquet in S3) are independent; see [Storage Fundamentals](/data-engineering/storage-fundamentals.md) for the file/block/object hierarchy this rests on, and [Open Table Formats](/data-engineering/open-table-formats.md) for the metadata layer.

### Event streaming — the newest convergence

Streaming is the latest paradigm to make the move, and it is instructive *because Kafka historically did the opposite*. Kafka's page-cache design **tightly couples compute and storage** — you cannot scale them independently, and cross-AZ replication is expensive in the cloud [^src3]. The fixes all reach for object storage: **tiered storage** (recent data on broker disk, historical data in S3/GCS/HDFS), **object-storage-native Kafka** (WarpStream, AutoMQ, Bufstream, Redpanda) that runs **directly on object storage** and *eliminates replication* because object storage already guarantees durability, and Aiven's **KIP-1150 "Diskless Topics"** that delegate replication to object storage, targeting up to 80% infrastructure-cost cuts [^src3]. This is the warehouse story replayed a decade later for streams — see [Apache Kafka](/data-engineering/kafka.md) and [Stream Processing](/data-engineering/stream-processing.md).

### OLTP databases — the newest convergence

The most recent front of compute–storage decoupling is **transactional (OLTP) databases**. Traditional provisioned databases size around expected demand, but AI workloads are unpredictable: agents fan out queries without warning, pipelines sit idle during model development, then traffic surges. Modern serverless databases address this by fully decoupling compute from storage [^src4]:

- **True scale-to-zero**: compute can drop to zero during idle periods; storage persists independently (data, replicas, backups, point-in-time recovery remain available whether compute is running or not) [^src4].
- **Independent scaling**: compute scales vertically (more vCores), horizontally (more nodes), or both; storage grows separately [^src4].
- **Cost model alignment**: a 2025 study found enterprises using serverless databases reported average cost reductions of **38% vs traditional provisioned databases** and potential savings of 40–65% for intermittent inference workloads; 65% reduction in infrastructure management tasks [^src4].

The key architectural distinction: *not every product labeled "serverless" is architecturally serverless*. Some are autoscaling clusters with usage-based billing layered on top of a traditionally coupled system — limiting how far they can scale down, how independently each layer can grow, and how cost-efficient they can be at idle and peak extremes [^src4].

**Serverless PostgreSQL** extends the pattern to the most widely adopted open relational database [^src5]. Compute provisions on demand, scales to zero when idle, and billing is usage-based rather than fixed-capacity. **Lakebase architecture** (Databricks Lakebase) goes further: it unifies transactional and analytical workloads on a shared data foundation, so operational data and analytics share the same storage layer — eliminating ETL pipelines between OLTP and analytical systems [^src5]. Neon and Databricks Lakebase are the leading implementations "built for the demands of AI-forward applications and agent-based systems" [^src5].

The cold start trade-off is the same across streaming and databases: compute paused to zero requires reactivation latency (milliseconds to several seconds depending on provider) when a query arrives; latency-sensitive workloads maintain a non-zero compute floor [^src4][^src5].

See [Serverless Databases](/data-engineering/serverless-databases.md) for the full concept (criteria, AI workload patterns, connection models, database branching).

## Why it matters

- **Cost follows the same logic everywhere.** Once durable state is in object storage, the optimization problem becomes *minimizing reads of it* — caching (Snowflake), eliminating replication (diskless Kafka), pruning via partitions/row-groups (Parquet/Capacitor). Recognizing the shared pattern means a cost lever learned on one system **transfers** to the next [^src1].
- **Engines become interchangeable over shared bytes.** Decoupling is what makes [open table formats](/data-engineering/open-table-formats.md) and multi-engine querying possible at all — the same Iceberg/Delta table read by several compute engines.
- **It is a convergence, not a coincidence.** The trade-off (cheap, durable, parallel, but high-latency and pay-per-read) is identical across warehouses, lakehouse, and streaming, which is why all three independently landed on object storage as the substrate.

## Related

- [Cloud Data Warehouse Internals](/data-engineering/cloud-data-warehouse-internals.md) — the warehouse-side deep comparison (this synthesis generalizes it across paradigms)
- [Storage Fundamentals](/data-engineering/storage-fundamentals.md) — file/block/object storage; why object storage scales
- [Apache Kafka](/data-engineering/kafka.md) — tiered/diskless storage; streaming's late convergence
- [Stream Processing](/data-engineering/stream-processing.md) — the streaming paradigm context
- [Apache Parquet](/data-engineering/parquet.md) · [Open Table Formats](/data-engineering/open-table-formats.md) — the file + metadata layers that live in object storage
- [Data Lake / Lakehouse](/data-engineering/data-lake.md) — the lake/lakehouse abstraction
- [Serverless Databases](/data-engineering/serverless-databases.md) — concept page: serverless OLTP decoupling, AI workload patterns, Lakebase
- [Data Engineering hub](/data-engineering/README.md)

---

[^src1]: [The internal of BigQuery, Snowflake, Databricks and Redshift (Vu Trinh)](../../raw/email/email-2025-04-17-the-internal-of-bigquery-snowflake-databricks-and-redshift.md)
[^src2]: [Storage Fundamentals for Data Engineers](../../raw/email/email-2025-09-28-storage-fundamentals-for-data-engineers.md)
[^src3]: [If you're learning Kafka, this article is for you (Vu Trinh)](../../raw/email/email-2025-05-15-if-you-re-learning-kafka-this-article-is-for-you.md)
[^src4]: [What To Look For in a Serverless Database for AI Applications](../../raw/web/web-what-to-look-for-in-a-serverless-database-for-ai-application-8e1ddee7.md)
[^src5]: [What Is Serverless PostgreSQL?](../../raw/web/web-what-is-serverless-postgresql-3e7858c3.md)
</content>

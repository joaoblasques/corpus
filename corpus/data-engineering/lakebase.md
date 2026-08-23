---
type: concept
domain: data-engineering
status: draft
aliases:
  - Lakebase
  - serverless Postgres on Databricks
  - LTAP
  - Lake Transactional Analytical Processing
  - HTAP alternative
tags:
  - corpus/data-engineering
  - database
  - oltp
  - postgres
  - cloud-storage
  - databricks
  - neon
  - open-table-formats
sources:
  - path: raw/_inbox/web-from-monolith-to-lakebase-to-ltap-rethinking-the-database-fr-229b688f.md
    channel: web
    title: "From monolith to Lakebase to LTAP: rethinking the database from storage up"
    author: Reynold Xin (Databricks cofounder)
confidence: 0.9
last_confirmed: 2026-08-23
created: 2026-08-23
updated: 2026-08-23
---

# Lakebase and LTAP

**TL;DR**: Lakebase is Databricks's serverless Postgres built on Neon's architecture. It externalizes the WAL to a distributed quorum service (SafeKeeper) and data files to an object-storage-backed cache (PageServer), making compute fully stateless. LTAP (Lake Transactional/Analytical Processing) extends this by transcoding Postgres rows to Parquet columnar format as data lands in the lake — creating a single governed copy in Delta/Iceberg that both Postgres and Lakehouse engines read, without ETL pipelines.[^xin]

## The monolithic OLTP problem

Traditional Postgres (and MySQL, Oracle) store two things on one machine:[^xin]

- **WAL (Write-Ahead Log)**: sequential append log; a commit is durable the moment this is flushed to local disk.
- **Data files**: random-access page files; updated asynchronously from the WAL.

Both living on the same disk creates compounding problems:[^xin]

| Problem | Root cause |
|---|---|
| Data loss from misconfiguration | Durability tied to a local disk flush that the OS may lie about |
| Data loss from node failure | WAL + data files on one machine; disk dies, data dies |
| Read replicas are full physical clones | Replica = copy entire DB + stream WAL continuously |
| HA requires a second full clone | Two physical copies, expensive to provision, PITR risk at failover |
| Analytics contends with transactions | Same CPU/memory; one heavy analytical query degrades OLTP latency |

All five problems trace to the same root: **colocating WAL and data files on a single machine.**[^xin]

## Lakebase architecture

The core move: make Postgres compute **stateless** by externalizing both storage pieces to independent, scalable services.[^xin]

### SafeKeeper (WAL layer)

Replaces local disk flush with **Paxos-based distributed replication**. A commit is durable when a quorum of SafeKeeper nodes acknowledges it — no individual disk can lose it. This is exactly what a serious monolithic deployment would need for synchronous replication anyway, so write latency is **unchanged** vs a properly-configured HA Postgres.[^xin]

Performance result: "5× higher write throughput and 2× lower read latency" vs classic Postgres HA.[^xin]

### PageServer (data files layer)

Acts as a **write-through cache** for cloud object storage (the lake). The WAL streams from SafeKeeper into PageServer; PageServer asynchronously applies changes and materializes pages into cheap object storage. When Postgres needs a page:[^xin]

1. Check local buffer pool (in-memory on Postgres node)
2. Check local disk cache
3. Only on cache miss: fetch from PageServer

Because the local cache can be sized identically to a monolith's cache, **cache hit rates and read latency are unchanged for the vast majority of operations.**[^xin]

### Capabilities that follow mechanically

Once WAL lives in SafeKeeper and data files in PageServer:[^xin]

- **Unlimited storage**: data in object storage, not provisioned disk
- **Serverless elastic compute**: stateless Postgres can scale to zero; pay only for actual use
- **Durable writes**: commit durable via Paxos quorum, not a single disk flush
- **Simple HA**: failover = spin up a new Postgres compute node pointing at the same storage; no physical clone
- **Instant branching/cloning/PITR**: branching is a metadata operation (pointer to a version), not a physical copy — same model as Git branching for code

> "For a monolithic database, cloning means physically copying the whole dataset, which is slow, expensive, and risky to the production system. When the data lives in an externalized, versioned storage layer, a branch or a clone is a metadata operation rather than a physical copy."[^xin]

## LTAP: Lake Transactional/Analytical Processing

### The core insight

The PageServer already streams the WAL and materializes pages into object storage. LTAP adds one step: **transcode Postgres row-format to Parquet columnar as data lands in the lake.**[^xin]

Result: a single durable copy of the data in open columnar formats (Delta + Iceberg, stored as Parquet) that both Postgres and Lakehouse engines (Databricks, Spark, etc.) read. No ETL pipeline, no CDC, no second copy to keep in sync.[^xin]

### How freshness works

The key challenge: how does an analytical query see data committed moments ago that hasn't been materialized yet?

1. Analytical query asks Postgres for the current **LSN** (Log Sequence Number — a cheap metadata lookup; Postgres serves no analytical data itself).
2. Query reads the vast majority of data from object storage (already materialized).
3. For very recent uncommitted changes not yet materialized: fetches only those from PageServer and merges on top.[^xin]

> "Postgres itself serves none of the analytical read traffic other than returning a single number (LSN). Your transactional workload does not slow down because someone kicked off a large analytical query."[^xin]

### Type system and multi-versioning

**Type system**: Most Postgres types map natively to Parquet. Edge cases (NaN, ±Infinity, NUMERIC beyond range, extension types) are not dropped — they are carried in a structured overflow field in the same Parquet table, preserving the canonical Postgres text representation.[^xin]

**Multi-versioning**: Postgres retains every row version for MVCC and PITR. LTAP preserves this by carrying the physical heap address (block + offset) in each materialized row, so heap pages remain reconstructable. Intermediate row versions visible inside Postgres MVCC are not exposed to Iceberg/Delta readers and are eventually garbage-collected.[^xin]

### LTAP vs CDC / "zero-ETL"

| Dimension | CDC / "mirroring" / zero-ETL | LTAP |
|---|---|---|
| Opt-in required | Yes — must select which tables to replicate | No — every table is automatically in the lake |
| Second copy | Yes | No — one durable copy |
| Replication lag | Yes, typically present | LSN-based; analytic reads are current to the last commit |
| Divergence risk | Yes — two copies can drift | No — no data movement |
| Governance | Two sets of permissions to maintain | Single governed copy |

[^xin]

### LTAP vs HTAP

HTAP (Hybrid Transactional/Analytical Processing) tries to build one engine that handles both workloads. LTAP unifies at the **storage layer** instead of the **engine layer**:[^xin]

| HTAP failure mode | LTAP approach |
|---|---|
| Incomplete feature set (new engine can't match mature Postgres or Spark) | Retain full Postgres + full Lakehouse ecosystems |
| No ecosystem (drivers, extensions, tools) | Postgres ecosystem unchanged |
| No performance isolation (transactions and analytics share hardware) | Full isolation: Postgres compute serves transactions; Lakehouse engines serve analytics |

## Columnar storage side effect

Columnar Parquet compresses data 10× better than row-format. This makes the storage path between PageServer and object store substantially cheaper and dramatically reduces network I/O — a free benefit of the format chosen for analytical performance.[^xin]

## See also

- [/data-engineering/open-table-formats.md](/data-engineering/open-table-formats.md) — Delta + Iceberg formats used by LTAP
- [/data-engineering/change-data-capture.md](/data-engineering/change-data-capture.md) — CDC is what LTAP replaces
- [/data-engineering/databricks.md](/data-engineering/databricks.md) — Lakebase is built into Databricks
- [/data-engineering/cloud-data-warehouse-internals.md](/data-engineering/cloud-data-warehouse-internals.md) — storage/compute separation patterns

---

[^xin]: raw/_inbox/web-from-monolith-to-lakebase-to-ltap-rethinking-the-database-fr-229b688f.md — Reynold Xin, Databricks cofounder, Databricks Blog

---
type: entity
domain: data-engineering
status: draft
sources:
  - path: raw/web/mondaydb-3-solving-htap-for-a-trillion-table-system-monday-e.md
    channel: web
    ingested_at: 2026-06-16
aliases:
  - mondayDB
  - mondayDB 3
  - MDB3
  - monday.com database
tags:
  - corpus/data-engineering
  - entity
created: 2026-06-16
updated: 2026-06-16
---

# mondayDB

**TL;DR** — mondayDB 3 (MDB3) is monday.com's purpose-built columnar serving layer that replaced its MySQL, Cassandra, and Redis fleet with a single system powered by an embedded **DuckDB** columnar engine [^src1]. It solves HTAP (hybrid transactional/analytical) for a "trillion-table" system — millions of user-defined boards, each its own evolving schema — via per-tenant file isolation, smart routing, and always-fresh reads [^src1]. Reported gains: board loads 5x faster (large boards 20x, aggregations ~50x), infra costs down 40–60%, migrating 1M+ organizations with zero downtime and zero data loss [^src1].

## The problem

A monday.com "board" is a dynamic user-defined table where columns can be added, renamed, retyped, or deleted on the fly [^src1]. The original design stored each item as a MySQL row with column values in a JSON blob — schema-flexible (no `ALTER TABLE`) but mismatched to the access pattern [^src1]. Opening a board reads ~500 rows but *all* columns: a wide analytical read run on a row store that had to deserialize the full JSON blob per row and could not index/filter/sort within it [^src1]. Over 1M organizations sharing the same multi-tenant tables produced billion-row B-tree indexes and wasted I/O on unrelated tenants' pages [^src1].

## Architecture — CQRS with a soft-stateful serving layer

MDB3 fully separates write and read paths, sharing no compute, processes, or local storage (only the WAL backend is shared) [^src1].

- **Batch layer** — DuckDB files in object storage (S3) are the durable source of truth for cold data; a flush pipeline consolidates WAL entries into them [^src1].
- **Speed layer** — an external WAL captures real-time mutations (flowing through Kafka and a writer), available for read-time merging within milliseconds [^src1].
- **Serving layer** — a fleet of thin Go processes on Kubernetes nodes with local NVMe SSDs, each a soft-stateful read-through cache holding an LRU of 200,000+ DuckDB files; any node can serve any board because truth is S3 + WAL [^src1].

This is a Lambda-style architecture; failure is isolated — write-path failures (Kafka lag) don't block reads, and read-path failures don't block writes [^src1].

## Read path — sync-then-query

The core algorithm: before every query, sync the local DuckDB file with the latest WAL entries, then execute — typically under 10 ms across seven steps (route → check cache → load/rebuild → determine WAL position → sync → execute → return) [^src1]. Sync uses an idempotent **deletion-first** pattern (delete matching rows by primary key, then bulk-insert via DuckDB's Table Appender API), guaranteeing correctness across retries and rebuilds [^src1]. This delivers read-after-write consistency within a board partition; cross-board reads are eventually consistent, typically converging within 500 ms [^src1].

## Smart routing (Ranja)

Routing becomes part of the database: a request must consistently hit the node holding the warm file. MDB3 uses **Weighted Rendezvous Hashing** (Highest Random Weight), not consistent hashing — each node computes `score = hash(node_id, tenant_id) * weight` with no central coordinator [^src1]. It adds capacity-aware weights, hedged requests (a secondary fires if the primary is silent past 500 ms), and a capacity-aware SIEVE eviction policy achieving "a 3-6x improvement in hit rate over standard LRU" [^src1]. The routing layer was formally verified with TLA+ and makes 65M routing decisions/second on commodity hardware [^src1].

## Why DuckDB, and turning its constraint into an asset

The workload is analytical, not transactional — "textbook columnar territory" — so DuckDB won for in-process execution (no network round-trips), runtime per-tenant attach/detach mapping one file per board, and vectorized execution over 2,048-value batches [^src1]. DuckDB's single-writer-per-file limitation became the key architectural decision: by never writing to DuckDB from the write path and managing writes in an external distributed WAL instead, they got full read/write separation, independent scaling, and failure isolation [^src1]. See [DuckDB](/data-engineering/duckdb.md).

## Zero-downtime migration

An 18-month, feature-flag-controlled, reversible migration: months of **dual-read validation** (every query run against both MySQL and MDB3, results compared) caught NULL-handling, Unicode-normalization, floating-point, sort-tie, and time-zone bugs before cutover [^src1]. Because dual-writing kept the new system current, the cutover itself was a flag flip with no data transfer; dual-write mode was held 30 days as a rollback target [^src1].

## Key lesson

"The best database for a given workload is often not a database at all; it is a carefully engineered system that aligns storage format, execution model, and caching strategy with the application's actual access patterns" [^src1]. The architecture is being extended into an AI contextual layer (text/semantic search, RAG) at the same latency, since per-board file isolation and sync-then-query freshness map directly onto context retrieval [^src1].

## Related corpus pages

Built on [DuckDB](/data-engineering/duckdb.md); uses [Apache Kafka](/data-engineering/kafka.md) in the write path and [Redis](/data-engineering/redis.md) as a high-frequency write-cache WAL backend. Compare with [Change Data Capture](/data-engineering/change-data-capture.md) and [Materialized Views](/data-engineering/materialized-views.md).

[^src1]: [mondayDB 3 – Solving HTAP for a Trillion-Table System](../../raw/web/mondaydb-3-solving-htap-for-a-trillion-table-system-monday-e.md)

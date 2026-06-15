---
type: entity
domain: data-engineering
status: draft
sources:
  - path: raw/web/duckdb-1-5-3-not-an-ordinary-patch-release.md
    channel: web
    ingested_at: 2026-06-11
  - path: raw/web/quack-the-duckdb-client-server-protocol.md
    channel: web
    ingested_at: 2026-06-11
  - path: raw/web/your-obsidian-vault-can-now-run-sql-and-your-agent-can-read.md
    channel: web
    ingested_at: 2026-06-11
aliases:
  - DuckDB
  - MotherDuck
  - Quack
  - DuckLake
tags:
  - corpus/data-engineering
  - entity
created: 2026-06-11
updated: 2026-06-11
---

# DuckDB

**TL;DR.** DuckDB is an **embedded, in-process OLAP engine** (first released 2019) — like SQLite but column-oriented for analytics, with no client-server, no protocol, just low-level API calls [^src2]. It excels at single-node, in-process analytics with zero infrastructure [^src2]. As of 2026 it is "moving further out of its initial niche... into a core building block of modern data architecture" via the **Quack** client-server protocol, **DuckLake**, and managed cloud (**MotherDuck**) [^src2].

## Why it matters

DuckDB made noise about its **in-process architecture**: an analyst interacts with data in a Python notebook where the data lives in a DuckDB instance in the *same process* — or DuckDB is "glued" to an existing application to add SQL over that application's data [^src2]. The trade-off: in-process works "less well" when multiple processes try to modify the same database file simultaneously, because DuckDB keeps state in main memory and would have to synchronize it across processes [^src2]. Quack is the answer to that limitation.

## Quack: the client-server protocol

Introduced May 2026, Quack turns DuckDB into a **client-server database with multiple concurrent writers** — DuckDB acts as both client and server, two instances talking to each other [^src2]. Design choices [^src2]:

- **HTTP-based** — built on HTTP/TCP; works with existing load balancing, auth, firewalls. Lets DuckDB-Wasm in a browser connect directly to a DuckDB instance on an EC2 server.
- **Request-response, single round-trip** — a query is handled in one round trip once connected (vs Arrow Flight SQL's minimum two), critical for latency-sensitive small writes.
- **Custom serialization** — new `application/duckdb` MIME type reusing DuckDB's internal serialization primitives (same as WAL files); deliberately *not* Arrow, to avoid being restricted by externally-controlled formats.
- **Security** — random auth token at startup, binds to localhost by default; no SSL for localhost (recommend nginx + Let's Encrypt to expose externally). Default port **9494** (94 = year Netscape Navigator shipped).
- **Pluggable auth/authz** — default token compare and "yes to everything" authorization, both overridable via user-supplied callbacks (even SQL macros).

**Benchmarks** (vs PostgreSQL and Arrow Flight SQL) [^src2]:
- *Bulk transfer:* 60M rows in **4.94 s** (Arrow Flight 17.40 s, PostgreSQL 158.37 s) — "the fastest way to shove tables through a socket."
- *Small writes:* up to ~5,500 tx/s at 8 parallel threads, outperforming PostgreSQL up to that point; beyond 8 threads DuckDB hits a current concurrent-insert limit and PostgreSQL scales better.

Quack is still **beta**; production release planned with **DuckDB v2.0 in fall 2026** [^src1][^src2]. MotherDuck (Boaz Leskes) and GizmoSQL (Philip Moore) are credited for prior client-server DuckDB work [^src2].

## DuckDB 1.5.3 — extensions over core

The v1.5.3 patch release (May 2026) is "not an ordinary patch": DuckDB core changes are limited bugfixes, but the **upgraded extensions** bring the real features [^src1]:

- **Quack as a core extension** — transparently autoinstalled/autoloaded on first use [^src1].
- **DuckLake + Quack** — DuckLake now supports a DuckDB-with-Quack instance as its **catalog database**, so a remote DuckDB server can be a remotely-accessible catalog [^src1][^src2].
- **Iceberg** — `MERGE INTO` now supported for Iceberg tables; `INSERT`/`UPDATE` on partitioned Iceberg tables (truncate/bucket transforms); CTAS via ADBC; `ALTER TABLE`; `GEOMETRY` type [^src1]. See [[data-engineering/apache-iceberg|Apache Iceberg]] and [[data-engineering/merge-into|MERGE INTO]].
- **AWS / HTTPS** — IRSA web_identity chain, IAM auth for RDS/Aurora PostgreSQL, `HTTP_PROXY` support [^src1].
- **Internals** — jemalloc now statically linked into core (was an extension) so other extensions can load dynamically [^src1].

## DuckLake

A lakehouse format/catalog approach (referenced alongside Iceberg as a newer OTF entrant in [[data-engineering/open-table-formats|open table formats]]). Quack makes multi-process modification "far simpler" than DuckLake alone and at higher performance; DuckLake can use a remote DuckDB-via-Quack server as its catalog, unlocking capabilities like data inlining [^src1][^src2].

## Obsidian / MotherDuck integration

The "DuckDB and MotherDuck" Obsidian community plugin lets a vault run SQL inline [^src3]:

- A ```` ```duckdb ```` fenced code block renders as a SQL panel (Run / Freeze / Clear freeze) in reading mode; **DuckDB WASM range-reads Parquet over HTTP, no token needed**, and works with anything DuckDB reads — Parquet, CSV, JSON, Excel, Iceberg, Delta, geospatial [^src3].
- **Freeze** drops the result in as a markdown table bracketed by sentinel comments (`<!-- md:cache ... -->`) carrying query hash, connection, timestamp, and row count — so it diffs cleanly in git and renders everywhere, including mobile [^src3].
- Swap the fence to ```` ```motherduck ```` for cloud data (every MotherDuck account has a shared `sample_data` database). Local DuckDB and MotherDuck connections coexist in the same note: local for files on disk, cloud to push heavy SQL off the laptop [^src3].

This is the "your agent can read" angle: agents can read the frozen markdown results directly without re-running queries [^src3].

## Where DuckDB fits in multi-engine routing

In multi-engine Iceberg deployments DuckDB is the **selective-lookup / sub-second tier** — "a point lookup that costs $0.01 on DuckDB costs $0.08 on Snowflake" — but cannot distribute across nodes, so heavy distributed joins go elsewhere. Table compaction expands the set of queries DuckDB can serve. See [[data-engineering/query-engine-routing|Query-engine routing]].

## Related

- [[data-engineering/query-engine-routing|Query-engine routing]] — DuckDB as the cheap fast tier
- [[data-engineering/apache-iceberg|Apache Iceberg]] · [[data-engineering/open-table-formats|Open table formats]] · [[data-engineering/parquet|Parquet]]
- [[data-engineering/merge-into|MERGE INTO]]

[^src1]: [DuckDB 1.5.3: Not an Ordinary Patch Release](../../raw/web/duckdb-1-5-3-not-an-ordinary-patch-release.md)
[^src2]: [Quack: The DuckDB Client-Server Protocol](../../raw/web/quack-the-duckdb-client-server-protocol.md)
[^src3]: [Your Obsidian vault can now run SQL (and your agent can read it)](../../raw/web/your-obsidian-vault-can-now-run-sql-and-your-agent-can-read.md)

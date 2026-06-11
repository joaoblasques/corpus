---
type: synthesis
domain: data-engineering
status: draft
sources:
  - path: raw/web/routing-multiple-query-engines-with-iceberg-lakeops-blog.md
    channel: web
    ingested_at: 2026-06-11
  - path: raw/web/greybeam-drop-in-query-engines-for-snowflake.md
    channel: web
    ingested_at: 2026-06-11
aliases:
  - query routing
  - multi-engine
  - drop-in query engine
  - query-engine routing
tags:
  - corpus/data-engineering
  - synthesis
created: 2026-06-11
updated: 2026-06-11
---

# Query-Engine Routing

**TL;DR.** One promise of [[data-engineering/apache-iceberg|Apache Iceberg]] is **multi-engine access**: Spark writes, Trino queries, Flink streams, DuckDB explores, Athena scans — all on the same tables in the same object storage [^src1]. But "nothing in the stack decides which engine should run which query" [^src1]. **Query routing** is a proxy layer that sits between clients and engines, evaluates each query, picks the cheapest/fastest engine for its shape, translates the SQL dialect if needed, and returns results — so to the client "it looks like a regular database" [^src1]. Two examples synthesized here: **QueryFlux/LakeOps** (open-source Iceberg routing) and **Greybeam** (a drop-in Snowflake proxy).

## The problem routing solves

Without a routing layer, every team picks the engine they know regardless of cost/latency. "A point lookup that costs $0.01 on DuckDB costs $0.08 on Snowflake" — across thousands of queries/day the wrong decisions add up to significant overspend [^src1]. Greybeam frames the same insight from the warehouse side: "99% of BI queries are small, only scanning less than 100GB" — yet they all hit the warehouse anyway [^src2].

Four compounding problems without routing [^src1]:

1. **Every query hits the same engine regardless of shape** — CPU-heavy joins pay scan-pricing; selective lookups wait behind batch jobs.
2. **N×M driver configs fragment the platform** — each engine needs its own connection strings, credentials, client libraries.
3. **No cost awareness in dispatch** — compute-priced engines (Trino, StarRocks) charge for CPU-seconds; scan-priced engines (Athena, BigQuery) charge for bytes read.
4. **SLA violations** when batch and interactive workloads compete on a shared cluster.

## Why multiple engines at all

Each engine has a distinct operational sweet spot [^src1]:

| Engine | Sweet spot |
|---|---|
| Spark | Batch ETL, heavy transforms, streaming ingest, all Iceberg maintenance (compaction, snapshot expiry) |
| Trino | Interactive SQL, low-latency analytics, ad-hoc exploration |
| Flink | Continuous streaming writes, exactly-once |
| [[data-engineering/duckdb|DuckDB]] | Single-node sub-second selective queries; zero infra; cannot distribute |
| Athena | Serverless, scan-priced; infrequent/unpredictable volumes |
| Snowflake | Managed warehouse, BI integrations; reads Iceberg via external/REST catalogs |
| StarRocks | High-concurrency, low-latency MPP for BI dashboards |

"No single engine handles everything well" — Trino is poor at large ETL writes, Spark slow at point lookups, DuckDB cannot distribute, Athena expensive for compute-heavy joins [^src1].

## Architecture of a routing layer

A SQL routing proxy accepts client connections over whatever protocol they already use (Trino HTTP, PostgreSQL/MySQL wire, Arrow Flight SQL), evaluates routing rules, selects a backend, optionally translates the dialect, dispatches, and returns results [^src1]. The decision happens in two stages [^src1]:

1. **Group selection** — rules evaluate the query (protocol, SQL text, client tags, headers) and pick a named **cluster group** (a pool of engines for one workload type).
2. **Member selection** — within the group a strategy (round-robin, least-loaded, failover, weighted) picks a healthy instance under its concurrency limit.

If no member is available, the query queues at the proxy (controlled backpressure) or spills to a fallback group [^src1].

## SQL-dialect translation

Multi-engine routing requires SQL compatibility across dialects — a PostgreSQL-wire client sending Trino SQL to a DuckDB backend fails without translation [^src1]. QueryFlux uses **sqlglot** for automatic conversion across 30+ dialects: detect source dialect from the frontend protocol, detect target from the engine type, skip translation if compatible (e.g. MySQL ↔ StarRocks), otherwise parse → transform AST → re-serialize [^src1]. Common cases: catalog-qualified names (Trino's three-part `catalog.schema.table` vs Athena's `schema.table`), function mapping (`date_diff` vs `datediff` vs `TIMESTAMPDIFF`), type casts, window syntax [^src1]. Edge cases use post-translation Python transform scripts [^src1].

## Routing strategies

Assigned **per routing group**, not globally [^src1]:

- **Cost routing** — cheapest engine that meets latency. Compute-heavy joins → compute-priced backends; scan-heavy reads → scan-priced backends. Good for batch ETL, scheduled reports. In the queryflux-bench suite, workload-aware routing **reduced total query cost by up to 56%**, individual queries sometimes by 90% vs a single default engine [^src1].
- **Latency routing** — fastest engine for the query shape, using historical P50 latency. For dashboards, BI tools, AI-agent queries [^src1].
- **Throughput (balanced) routing** — spread queries to maximize overall throughput and avoid bottlenecks; for mixed workloads [^src1].

## Table optimization unlocks better routing

Routing decides *where* a query runs, but the set of *eligible* engines depends on physical table layout [^src1]. A table with 50,000 small files and fragmented manifests forces even simple queries onto heavy distributed engines; the same table compacted into a few hundred sorted files with current Puffin statistics can be served by DuckDB sub-second [^src1]. "Compaction does not just speed up one engine — it expands the set of engines that are viable for each query shape" [^src1]. This is a compounding effect between table maintenance and routing: optimizing Iceberg tables is a prerequisite for full multi-engine value [^src1].

## Self-improving routing for agentic workloads

AI-agent query shapes are both repetitive (80% parameterized templates) and unpredictable (20% novel) [^src1]. QueryFlux's design uses a fall-through stack [^src1]:

- **Adaptive router** — pure statistics over query history; routes to lowest-P50 engine for shapes with 20+ observations. ~0ms (in-memory). Handles the 80%.
- **LLM router** — for never-seen shapes, an LLM reasons over live table stats, engine capabilities, and cluster load; cached by parameterized hash (~300ms first call, 0ms thereafter).
- **Semantic router** — local embedding similarity to known shapes when LLM confidence is low (~1ms).
- **Default group** — fallback.

Guardrails (ReadOnlyGuard, RowLimitGuard, CostEstimateGuard, PIIMaskGuard, HumanApprovalGuard) sit between routing and dispatch; an MCP-server frontend gives any MCP-compatible agent routing/translation/guardrails with zero custom code [^src1].

## Two implementations compared

**QueryFlux + LakeOps** [^src1] — open-source, Rust-based SQL proxy (~0.35ms p50 overhead) for self-hosted multi-engine Iceberg. QueryFlux is the proxy (protocols, rule-based routing, sqlglot translation, capacity management, Prometheus/Grafana). LakeOps layers an intelligent control plane on top: table-health-aware routing (reads Iceberg metadata — file counts, delete-file ratios, partition skew — and steers queries on degraded tables to Trino/Spark over DuckDB), query-pattern learning, optimization-driven engine expansion, a unified cost model, and policy-driven automation across routing *and* table maintenance.

**Greybeam** [^src2] — a managed, drop-in **Snowflake proxy**. You "simply swap your connection string"; dashboards/reports keep working while Greybeam translates and routes SQL to the optimal engine. It caches Snowflake data as Apache Iceberg tables in a bucket you own (via CDC streams, or reads existing Iceberg directly), routes most queries to DuckDB, and **transparently falls back to Snowflake** if anything fails (<100ms penalty, mostly SQL parsing). Claimed **75–98% reductions in Snowflake compute** for read workloads. Routing today is heuristic (table size, join complexity, query patterns) with a learned model "actively building." Auth: every request is authenticated against Snowflake first, so it cannot bypass Snowflake permissions. Pricing: compute from $0.75/hr (8 vCPU) plus a $100/month platform fee.

**Synthesis.** Both implement the same thesis — *most analytical queries are small and do not need a warehouse, so route them to a cheaper engine over open Iceberg storage* — but at different layers. QueryFlux/LakeOps is an open, self-hosted control plane for a full multi-engine lakehouse; Greybeam is a closed, zero-config wedge specifically in front of Snowflake. Both rely on Iceberg as the portability substrate, both use SQL translation + automatic routing + warehouse fallback, and both are moving from heuristic toward learned routing. Note both sources are vendor materials promoting their own products; cost-savings percentages are vendor-reported.

## Related

- [[data-engineering/apache-iceberg|Apache Iceberg]] — the multi-engine substrate
- [[data-engineering/duckdb|DuckDB]] — the cheap, fast selective-query tier
- [[data-engineering/open-table-formats|Open table formats]] · [[data-engineering/data-lake|Data lake]]
- [[data-engineering/databricks|Databricks]] — alternative single-platform lakehouse model

[^src1]: [Routing multiple query engines with Iceberg (LakeOps)](../../raw/web/routing-multiple-query-engines-with-iceberg-lakeops-blog.md)
[^src2]: [Greybeam: drop-in query engines for Snowflake](../../raw/web/greybeam-drop-in-query-engines-for-snowflake.md)

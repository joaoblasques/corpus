---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/web/incremental-materialized-view-clickhouse-docs.md
    channel: web
    ingested_at: 2026-06-11
  - path: raw/web/introduction-to-materialized-views-bigquery-google-cloud-doc.md
    channel: web
    ingested_at: 2026-06-11
  - path: raw/web/incremental-refresh-for-materialized-views-databricks-on-aws.md
    channel: web
    ingested_at: 2026-06-11
  - path: raw/web/working-with-materialized-views.md
    channel: web
    ingested_at: 2026-06-11
  - path: raw/web/everything-you-need-to-know-about-incremental-view-maintenan.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-05-21-quick-insights-on-materialized-views.md
    channel: email
    ingested_at: 2026-06-15
aliases:
  - materialized view
  - incremental materialized view
  - incremental refresh
  - MV
  - IVM
  - incremental view maintenance
  - differential dataflow
  - DBSP
tags:
  - corpus/data-engineering
  - concept
created: 2026-06-11
updated: 2026-06-15
---

# Materialized Views

**TL;DR.** A materialized view (MV) is a **pre-computed dataset derived from a query and stored for reuse**, so querying it is faster than re-running the query against the base table [^src4]. The central trade-off across all platforms: MVs **shift computation from query time to insert/refresh time**, trading storage and maintenance cost for faster, cheaper reads [^src1][^src2]. Platforms split into two design philosophies — **insert-time incremental** (ClickHouse incremental MVs, a trigger on inserts) vs **refresh-based** (BigQuery, Databricks, Snowflake background maintenance) — and each imposes a **restricted SQL surface** for the incremental path [^src1][^src2][^src3][^src4].

## The core idea: move compute off the read path

ClickHouse states the motivation plainly: incremental MVs *"allow you to shift the cost of computation from query time to insert time, resulting in faster SELECT queries."* The stored result is often a smaller representation (a partial sketch for aggregations), so reads are both faster and cheaper [^src1]. BigQuery frames the same benefit as reducing total processing time by reducing bytes scanned [^src2]. Snowflake: pre-computed results speed up expensive aggregation, projection, and selection — especially for frequent or complex queries — but *"materializing intermediate results incurs additional costs"* [^src4].

This is the recurring tension: faster/cheaper reads vs added **storage** + **maintenance/refresh** cost. Snowflake's decision rule captures it well — create an MV when results change rarely, are used often, and the query is resource-intensive; otherwise use a regular view [^src4].

## Insert-time vs refresh-based: two architectures

| Platform | Model | Update mechanism |
|---|---|---|
| ClickHouse (incremental MV) | Insert-time trigger | Runs the query on each inserted block; writes to a target table; merges asynchronously [^src1] |
| ClickHouse (refreshable MV) | Refresh-based | Periodic full re-execution; static snapshot until refresh [^src1] |
| BigQuery | Refresh / background | Auto-precomputes in background when base tables change; "always fresh" via runtime merge [^src2] |
| Databricks | Refresh (incremental or full) | Cost-model picks the cheaper of incremental refresh vs full recompute [^src3] |
| Snowflake | Background maintenance | Background service refreshes on base-table DML; always-current reads [^src4] |

### ClickHouse: the MV is "just a trigger"

Unlike transactional databases, *"a ClickHouse materialized view is just a trigger that runs a query on blocks of data as they're inserted into a table,"* with results inserted into a second target table [^src1]. New inserts produce new partial results that merge with existing ones — the merged result equals running the query over all original data [^src1]. ClickHouse MVs update in real time, functioning *"more like continually updating indexes,"* in contrast to databases where MVs are static snapshots needing refresh (which is what ClickHouse's separate *refreshable* MVs do) [^src1].

To merge incremental state you need engines that collapse rows by ordering key: `SummingMergeTree` (sums numeric columns) for simple sums, or `AggregatingMergeTree` with `AggregateFunction` columns and `-State`/`-Merge` function suffixes for arbitrary aggregations [^src1]. Critical correctness rule: **partial aggregation states are required** — averaging the averages of sub-ranges produces wrong results [^src1]. Because merges are asynchronous, queries must reconcile outstanding rows with `FINAL` or by aggregating on the ordering key at read time [^src1]. The docs report a 25x+ speedup (0.133s → 0.004s) and reducing 238M rows to 5000 by storing daily aggregates [^src1].

A key alignment gotcha: the MV's `GROUP BY` columns should match the target table's `ORDER BY` for `SummingMergeTree`/`AggregatingMergeTree`; misalignment causes inefficient merges, suboptimal performance, or **data discrepancies** [^src1].

### Refresh-based platforms: incremental vs full refresh

**Databricks** is the clearest exposition of incremental-vs-full. A *refresh* attempts incremental (process only new/changed data since last refresh, append results); a *full refresh* clears the table and checkpoints and reprocesses all source data [^src3]. Outputs are identical; Databricks runs a **cost analysis** to pick the cheaper of incremental vs full recompute [^src3]. Incremental refresh is only available on **serverless** compute — non-serverless MVs are always fully recomputed [^src3]. A `REFRESH POLICY` lets you control this: `AUTO` (default, cost-based), `INCREMENTAL` (prefer incremental, fall back to full), `INCREMENTAL STRICT` (fail rather than fall back to full), `FULL` (always full) [^src3]. Use `INCREMENTAL STRICT` when unexpected full refreshes would blow cost/SLA budgets and you'd rather the job fail so you can debug [^src3].

**BigQuery** distinguishes **incremental** MVs (limited SQL surface, eligible for *smart tuning* — the optimizer auto-reroutes base-table queries to the MV) from **non-incremental** MVs (most SQL, but every refresh runs the full query, no smart tuning, no always-fresh guarantee) [^src2]. By default BigQuery only creates incremental MVs; `allow_non_incremental_definition = true` opts into non-incremental [^src2]. "Zero maintenance, always fresh": if base-table changes would invalidate the MV, BigQuery reads directly from base tables; otherwise it reads the MV plus only the changed rows [^src2].

## Insert-time vs query-time compute, restated

The unifying frame across sources: every MV is a bet that **you will read the result more often than the base data changes**, so paying compute once at write/refresh time beats paying it on every read [^src1][^src4]. ClickHouse pays it literally at insert time (per block) [^src1]; refresh-based platforms pay it on a background schedule or cost-driven refresh [^src2][^src3][^src4]. The wrong bet — frequently changing base data, rarely read results — makes maintenance cost dominate and an MV the wrong tool [^src4].

## Platform limitations (the restricted SQL surface)

Incremental/materialized paths are deliberately constrained.

**Snowflake** (most restrictive) [^src4]:
- A MV can query **only a single table** — **no joins**, including self-joins.
- Cannot query another MV, a regular view, a hybrid table, a dynamic table, or a UDTF.
- No UDFs, window functions, `HAVING`, `ORDER BY`, `LIMIT`, `GROUP BY GROUPING SETS/ROLLUP/CUBE`, nested subqueries, or `MINUS`/`EXCEPT`/`INTERSECT`.
- Only a fixed list of aggregate functions allowed (`SUM`, `COUNT`, `AVG`, `MIN`, `MAX`, `APPROX_COUNT_DISTINCT`/HLL, stddev/variance family, bit-agg family); aggregates cannot be nested or combined with `DISTINCT`; functions must be **deterministic** (no `CURRENT_TIME`/`CURRENT_TIMESTAMP`) [^src4].
- No standard DML on the MV (`INSERT`/`UPDATE`/`DELETE`/`MERGE`/`COPY`/truncate); cannot directly clone; no Time Travel querying [^src4].
- `SELECT *` is discouraged — columns are fixed at creation and new base columns are **not** propagated automatically [^src4].

**BigQuery** [^src2]: only incremental MVs get smart tuning; restricted SQL syntax and limited aggregations; you **can't update the MV query after creation**; can't nest MVs; can't query external/wildcard tables, logical views, or snapshots; `max_staleness` must be 30 min – 3 days; GoogleSQL only; no direct DML. MVs over CDC-active tables can't do runtime merge — set `max_staleness` to at least 2x the base table's, and you can't reference both the MV and its CDC base table in one query, nor use smart tuning [^src2].

**Databricks** [^src3]: incremental refresh supported only on serverless; only certain sources support it (Delta tables, MVs, streaming tables, Unity Catalog managed Iceberg v2/v3 — v3 recommended; foreign Iceberg unsupported); some operations require **row-tracking** enabled; sources with **row filters or column masks do not support incremental refresh**; recursive CTEs fall back to full recompute; UDF behavior changes may silently require a manual full refresh. For sources where records should be processed exactly once (Kafka, Auto Loader ingest, archived/deleted-after-processing tables), use **streaming tables** instead of MVs [^src3].

**ClickHouse** [^src1]: incremental MVs trigger **only on inserts to the left-most (source) table** in the query — right-side JOIN tables are read in full but **don't trigger updates**, so JOINs behave like a snapshot join against static dimension data (use refreshable MVs for complex JOINs if reduced freshness is acceptable). `UNION ALL` isn't directly supported (create one MV per branch writing to a shared target). The source table is **replaced by the inserted block** inside the MV query, which can yield surprising JOIN/filter results. CTEs are inlined (not materialized) and re-evaluated per insert. Multiple MVs on one table run sequentially by default; `parallel_view_processing=1` improves insert throughput at the cost of higher CPU/memory pressure and weaker failure/ordering semantics [^src1].

## When to use (and not)

Snowflake's guidance generalizes: create an MV when view results change infrequently, are used often (more often than they change), and the query is resource-intensive; create a **regular view** when results change often, are rarely used, or the query is cheap to re-run [^src4]. Good MV designs **filter** (rows and/or columns) and/or **pre-compute resource-intensive operations** so they don't repeat [^src4]. BigQuery's headline use cases: pre-processing aggregates/joins, dashboard acceleration (e.g. Looker daily-active-users), real-time analytics on high-velocity streams, and cost management on repetitive expensive queries [^src2].

## Cost

MVs cost on three axes — **querying, maintenance/refresh, and storage** [^src2][^src4]. Snowflake's automatic background maintenance **consumes credits**, billed per second; cost scales with the number of MVs per base table, the volume of changed data, and especially **clustering** (a differently-clustered MV may rewrite far more micro-partitions than the base-table change) [^src4]. Batching base-table DML (deletes, inserts/updates/merges) reduces maintenance cost [^src4]. Both Snowflake and Databricks let you suspend an MV, but suspending typically **defers** cost rather than reducing it [^src3][^src4]. BigQuery stores `AVG`/`ARRAY_AGG`/`APPROX_COUNT_DISTINCT` results as an internal intermediate **sketch** (`BYTES`), affecting size calculation [^src2].

## Gotchas

- **Always-fresh ≠ free**: refresh-based platforms guarantee correct reads by falling back to base tables for un-refreshed partitions, which can make reads slower when maintenance lags [^src2][^src4].
- **Base-table schema changes can suspend or invalidate** the MV (Snowflake: altering/dropping any column suspends all MVs on the table, even unused columns — you must recreate) [^src4].
- **Cross-platform JOIN behavior differs sharply**: forbidden in Snowflake, snapshot-only on the right side in ClickHouse incremental MVs, supported but incrementality-sensitive in Databricks [^src1][^src3][^src4].
- **CDC base tables** (BigQuery) need `max_staleness` tuning and disable smart tuning [^src2].

## Incremental view maintenance (IVM): the delta principle

The platform sections above are the productized face of a deeper idea: **incremental view maintenance** [^src5]. A plain MV trades freshness for read latency — refreshing the whole dataset periodically — so a single changed row forces reprocessing all source data (`SELECT COUNT(*)` recounts every row to learn one row was inserted) [^src5]. IVM instead reprocesses **only the view data affected by the change (the delta)**, which the DBSP paper frames as a speedup of `O(|DB|/|ΔDB|)` — for `|DB|≈10⁹` and `|ΔDB|≈10²` that is ~10 million times faster [^src5]. Cheap deltas let MVs refresh on every change, keeping the view fresh while reads still hit pre-computed data [^src5]. Two design questions define an IVM engine: **when** to update (schedule, ad-hoc, or — most commonly — a trigger/sensor watching for changed data, the same role Airflow triggers play in a warehouse) and **how to know what to update** [^src5].

### Why hand-written deltas and bag algebra fall short

Hand-coded triggers (e.g. a Postgres `AFTER INSERT` trigger that upserts into `customer_order_totals`) work for simple cases but break down for joins, window functions, and recursion [^src5]. The systematic alternative is **bag (relational) algebra**: translate the view's SQL into select/project/join/union/difference operators, then mathematically derive how inserts/deletes (deltas) propagate to the view [^src5]. This preserves SQL ergonomics but is **no longer cheap** for complex, recursive, or nested queries — expressiveness traded for cost [^src5].

### The modern dataflow stack: timely → differential → DBSP

Three influential papers underpin most recent IVM products, forming a flexibility-vs-simplicity ladder [^src5]:

- **Timely dataflow** (Naiad) — the lowest, most flexible layer. Models time as a vector of `(epoch, loop counter)` so deeply nested loops (graph algorithms) are easy, and uses **out-of-band watermark broadcasts** (data and control planes separated) so tasks get a global view of progress and compute concurrently rather than cascading punctuations sequentially [^src5]. API is four methods (`SendBy`, `NotifyAt`, `OnRecv`, `OnNotify`) — "a powerful but low-level framework," like Hadoop Map/Reduce [^src5].
- **Differential dataflow** — built on timely. Introduces **differential computation**: state varies over a *partially ordered* set of versions (not a linear sequence) and updates are retained in an indexed structure rather than consolidated into a "current" state, letting the engine selectively reuse prior computation [^src5]. Standard SQL-like operators (joins, aggregations, recursion) are built on top, so developers express views in SQL/Datalog [^src5].
- **DBSP** — built on digital-signal-processing intuition. Just as any logic circuit reduces to NAND gates, DBSP shows four operators (lift, delay `z⁻¹`, plus two for recursion) are functionally complete for relational algebra, so **arbitrary batch SQL can be mechanically converted into an incremental DBSP circuit** [^src5]. It constrains time/state management for a simpler model, giving up some of differential dataflow's concurrency in exchange [^src5].

### Who uses what, and the gap

**Materialize** is built directly on differential dataflow; newer entrants like **Feldera** are built on DBSP [^src5]. The broader IVM landscape includes Postgres's (semi-working) `pg_ivm`, Epsio, Bytewax, ClickHouse IVMs, dbt incremental models (still batch-based), and frontend sync engines (Zero, ElectricSQL) that increasingly resemble IVM engines [^src5]. The honest caveat: IVM in stream processors is still a work in progress, many databases have incomplete implementations, and a real **Postgres** IVM "would be a very big deal" — differential dataflow's complexity has kept it niche, and SQL-frontend products are what make it accessible [^src5].

## Related

- [[data-engineering/change-data-capture|Change data capture]] — MVs over CDC-active base tables carry extra limitations.
- [[data-engineering/apache-iceberg|Apache Iceberg]] — Databricks incremental refresh supports Unity Catalog managed Iceberg (v3 recommended) [^src3].
- [[data-engineering/dbt|dbt]] — incremental models solve a similar problem in the transformation layer.
- [[data-engineering/sql-intermediate-results|Storing Intermediate Results in SQL]] — MV vs CTE vs temp table decision framework; refresh-blocking & `CONCURRENTLY`.

[^src1]: [Incremental materialized view (ClickHouse docs)](../../raw/web/incremental-materialized-view-clickhouse-docs.md)
[^src2]: [Introduction to materialized views (BigQuery / Google Cloud)](../../raw/web/introduction-to-materialized-views-bigquery-google-cloud-doc.md)
[^src3]: [Incremental refresh for materialized views (Databricks on AWS)](../../raw/web/incremental-refresh-for-materialized-views-databricks-on-aws.md)
[^src4]: [Working with Materialized Views (Snowflake docs)](../../raw/web/working-with-materialized-views.md)
[^src5]: [Everything You Need to Know About Incremental View Maintenance](../../raw/web/everything-you-need-to-know-about-incremental-view-maintenan.md)
[^src6]: [Quick insights on materialized views (Vu Trinh, newsletter origin)](../../raw/email/email-2026-05-21-quick-insights-on-materialized-views.md)

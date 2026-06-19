---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/youtube/youtube-vstjydo88ka.md
    channel: youtube
    ingested_at: 2026-06-17
  - path: raw/email/email-2025-08-01-sql-vs-dbt-models-the-value-of-ctes.md
    channel: email
    ingested_at: 2026-06-19
aliases:
  - CTE
  - common table expression
  - common table expressions
  - temporary table
  - temp table
  - staging table
  - subquery
  - subqueries
  - CTE vs temp table
  - storing transformations in SQL
  - intermediate results
tags:
  - corpus/data-engineering
  - concept
created: 2026-06-17
updated: 2026-06-19
---

# Storing Intermediate Results in SQL (CTEs, Subqueries, Views, Temp Tables, Materialized Views)

**TL;DR.** There are five ways to store a transformation in SQL, split by whether they **materialize** (store) the result [^src1]:

| Mechanism | Materializes? | Lifetime / scope |
|---|---|---|
| **Subquery** | No | Single query |
| **CTE** (`WITH`) | No | Single query |
| **View** | No | Persists by name; reusable across queries |
| **Temporary table** | Yes | One session/pipeline, then auto-dropped |
| **Materialized view** | Yes | Persists; must be refreshed |

The non-materialized three store *transformation logic only* — the query re-executes every time they're called, producing no stored data [^src1]. The materialized two store *results*, avoiding recomputation at the cost of storage and staleness management [^src1]. The opinionated default: **use CTEs by default; promote to a view only when the logic must be shared; reach for a temp table when one transformation feeds several downstream steps** [^src1].

This page is the decision framework. For the rewrite-rule mechanics of views see [[data-engineering/postgresql-views|PostgreSQL Views]]; for MV refresh internals and incremental view maintenance see [[data-engineering/materialized-views|Materialized Views]].

## The non-materialized three: CTE vs subquery vs view

All three "do not store the results — every time they're called the query is executed again" [^src1]. They share **identical performance characteristics** on modern engines; choose on readability and sharing, not speed [^src1].

- **CTE (`WITH`)** — a named subquery that exists only within a single (usually complex) query. The recommended default: same performance as a subquery but far more readable, since each step gets a clean name [^src1].
- **Subquery** — "generally terrible": slower than or equal to a CTE. The one exception is **older engines (MySQL, older PostgreSQL) that don't optimize CTEs well** — or any engine where the `WITH` clause breaks index optimizations — where a subquery is preferred [^src1]. On modern analytical/warehouse/lake engines, `WITH` and subqueries are identical in performance, so pick the more readable `WITH` [^src1].
- **View** — a *named query* that persists and can be referenced from other queries, sharing transformation logic across pipelines [^src1]. Use a view **only when the logic is genuinely shared** across multiple pipelines or handed to analysts as a curated interface that abstracts complex logic [^src1].

> Verbatim opinion: "subqueries are pretty terrible... generally speaking you want to mostly use CTE" [^src1].

**CTEs in dbt — a tell.** In a [[data-engineering/dbt|dbt]] context, whether (and how) a team uses CTEs is treated as "a key indicator of how a team thinks about and uses dbt" — and of how well they understand the way cloud databases operate [^src2]. The framing matches this page: CTEs are valued *not* for performance (they don't drastically change it) but for letting you structure a model into named steps that improve cleanliness, simplify debugging, and provide functionality analogous to breaking a Python program into functions [^src2].

**View gotcha — dependency locking.** Because views depend on their base tables, dropping or altering a table that a view references is blocked ("it yells at you"), making views harder to move and manage your data around [^src1]. This is the same rigidity covered structurally in [[data-engineering/postgresql-views|PostgreSQL Views]] (columns pinned by attribute number; `DROP`/restructure refused or cascaded).

## The materialized two: temporary table vs materialized view

Both **store data** so it can be reused without re-running the heavy transformation — valuable when one transformation feeds three more, where a CTE would force re-executing that transformation three times [^src1].

- **Temporary table** — `CREATE TEMPORARY TABLE ... AS`. Exists only within one query session/pipeline, then is **automatically deleted** on session close [^src1]. Demonstrated win: a 13-second self-join query, once materialized into a temp table, was queried by two downstream analyses in ~1 second each [^src1]. Upside: no cleanup needed. Downside: gone on session close, so you can't troubleshoot the intermediate step afterward without re-running [^src1].
- **Staging table** — the pragmatic middle ground: a **normal table with very short retention** (e.g. ~5 days) used only as a helper to speed up ETL. Unlike a temp table it **survives session close** (so the intermediate is inspectable), at the cost of explicit retention management [^src1].
- **Materialized view** — turns a query into a stored table so the heavy transformation isn't re-executed [^src1]. Unlike temp tables, MVs **live on**. Costs: they must be **refreshed** (`REFRESH MATERIALIZED VIEW`), and a plain refresh is **blocking** — concurrent readers are locked out unless you create a **unique index** and `REFRESH ... CONCURRENTLY`, which lets readers see old data from the index while the refresh runs (slower refresh, but non-blocking) [^src1]. A unique index also adds a uniqueness data-quality guarantee [^src1].

## When materialized views are the wrong choice

The big drawback of MVs: they **recompute the entire dataset on every refresh — no incremental gains** [^src1]. This is where temp tables (and, more broadly, hand-built incremental tables via the plain table API) win: you can update only the new window instead of recomputing everything [^src1]. The expressed bias is against MVs precisely because "they marry you to the idea of having to compute the entire window all the time" [^src1].

> This is the productized version of the incremental-vs-full tension covered in [[data-engineering/materialized-views|Materialized Views]] — where engines like Databricks add cost-based incremental refresh and the DBSP/IVM line of work makes deltas cheap. The opinion here ("build the incremental table yourself") is one resolution; incremental MV maintenance is the other.

## Decision rules (summary)

1. **Default to a CTE** — readable, no materialization, single-query scope [^src1].
2. **View only when shared** across pipelines, or as a clean analyst interface [^src1].
3. **Subquery only** for old engines or where `WITH` breaks index optimizations [^src1].
4. **Temp table** when one transformation feeds several downstream steps in a session; **staging table** when you also need the intermediate to survive for troubleshooting [^src1].
5. **Materialized view** when the result changes rarely, is read often, and recomputing the whole window is acceptable — otherwise build an incremental table yourself [^src1].

## See also

- [[data-engineering/postgresql-views|PostgreSQL Views]] — view = rewrite rule (macro); schema-evolution rigidity
- [[data-engineering/materialized-views|Materialized Views]] — refresh models, incremental view maintenance, restricted SQL surface
- [[data-engineering/pipeline-layers|Pipeline Layers]] — staging tables in the ELT layering pattern
- [[data-engineering/sql-window-functions|SQL Window Functions]] — common content inside these transformations
- [[data-engineering/etl-pipeline|ETL Pipeline]] — where intermediate-result choices live
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [SQL Views vs Temporary Tables vs CTEs vs Subqueries](../../raw/youtube/youtube-vstjydo88ka.md)
[^src2]: [SQL vs dbt Models (& the value of CTEs) (Kahan Data Solutions)](../../raw/email/email-2025-08-01-sql-vs-dbt-models-the-value-of-ctes.md)

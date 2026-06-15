---
type: concept
domain: data-engineering
status: draft
sources:
  - path: 03_Resources/Articles/scd2-table-creation-merge-into-spark-iceberg.md
    channel: notes
    ingested_at: 2026-05-07
  - path: 03_Resources/Study Notes/Dimensional Data Modeling - Idempotent Pipelines and SCD Patterns.md
    channel: notes
    ingested_at: 2026-05-21
  - path: raw/web/stop-using-slowly-changing-dimensions-part-1.md
    channel: web
    ingested_at: 2026-06-11
  - path: raw/email/email-2025-11-04-scd-2-considered-harmful-part-2.md
    channel: email
    ingested_at: 2026-06-12
aliases:
  - SCD2
  - Slowly Changing Dimension Type 2
  - slowly changing dimension
  - date stamping
  - date-stamping
  - snapshots
tags:
  - corpus/data-engineering
  - concept
created: 2026-05-07
updated: 2026-06-12
---

# SCD2 (Slowly Changing Dimension Type 2)

**TL;DR**: A data modeling pattern that preserves full history of dimension changes by closing old rows (setting `valid_to`, `is_current = false`) and inserting new current rows, rather than overwriting [^src1].

## Required columns

| Column | Purpose |
|---|---|
| `customer_id` | Natural key — identifies the real-world entity |
| `datetime_updated` | Change tracking — when the source record changed |
| `valid_from` | Start of this row's validity window |
| `valid_to` | End of this row's validity window (NULL if current) |
| `is_current` | Boolean flag — true for the active row per entity |
| `is_active` | Boolean flag — false for soft-deleted entities |

## Three conditions → three actions

When updating an SCD2 table via MERGE INTO [^src1]:

| Condition | Action |
|---|---|
| Row exists in both, `is_current = true`, and source has newer data | Mark old row inactive: set `valid_to`, `is_current = false` |
| Row exists in source only (new or updated) | INSERT as new current row |
| Row exists in target only (deleted from source) | Mark inactive: `is_active = false` |

## The dual-source trick

To handle updates atomically — closing the old row and inserting a new one in a single MERGE — the source query uses `UNION ALL` with a `NULL` join key [^src1]:

```sql
SELECT customer_id AS join_key, * FROM prod.db.customer
UNION ALL
SELECT NULL AS join_key, * FROM customers_with_updates
```

The `NULL join_key` row never satisfies the `ON` match condition, so it always triggers `WHEN NOT MATCHED → INSERT`, producing the new current row even when the entity already exists in the target [^src1].

## Atomicity guarantee

Because the entire MERGE INTO is a single atomic operation, a pipeline failure cannot produce partially-updated SCD2 history — no risk of an old row being closed without the new row being inserted [^src1].

## Performance caveat

MERGE INTO performs a full outer join internally. Use only on dimension tables of manageable size — never on fact tables [^src1].

## `end_date` sentinel

Prefer `9999-12-31` over `NULL` for the current row's `end_date` — enables `BETWEEN` joins without null handling [^src2].

## When to skip SCD entirely

- Scale < 10–15M users → daily snapshots are simpler and cheap
- Rapidly changing dimensions (hourly) → SCD adds rows without benefit
- SCD only pays off at large scale where storage savings matter [^src2]

SCDs must be **tables** — never views or stored procedures [^src2].

## Critique: date-stamping as a simpler alternative

A counterpoint argues SCD2 is an outdated solution and that **date-stamping** every table is simpler and more powerful [^src3]. The premise: > "STORAGE IS CHEAP! (And your data team's time is expensive)" [^src3]. Rather than maintaining `valid_from`/`valid_to`/`is_current` columns and MERGE logic, take a dated snapshot of each source daily (Meta did this from MySQL into Hive: a daily snapshot with a date stamp) [^src3].

Claimed benefits over SCD2 [^src3]:

- **Resilient pipelines** — each day's partition is independent and re-runnable
- **History for free** — every snapshot is preserved, giving a "time machine" without closing/opening rows
- **Fewer bugs** — no risk of a half-applied SCD2 update; ~90% fewer bugs claimed
- **Tool-agnostic** — works with Hive metastore, [[data-engineering/apache-iceberg|Iceberg]], Delta, or Hudi

This is the *functional data engineering* lineage (Maxime Beauchemin), repackaged as date-stamping as the organizing principle, not an afterthought [^src3]. The trade-off is storage volume: daily full snapshots duplicate unchanged rows, which is precisely the cost SCD2 was designed to avoid at very large scale — see the "When to skip SCD entirely" thresholds above [^src2]. The two views agree on the boundary: SCD2 only pays off where storage savings outweigh complexity.

### Part 2: why SCD2 makes querying and backfilling painful

A follow-up sharpens the critique with concrete mechanics [^src4]. The motivating problem is **point-in-time state across multiple tables** ("for users who now have 1000+ followers but had under 200 three months ago, what device were they using then?") — a join over user, device, and relationship *state as of a past date* [^src4]. Under SCD2 every such join needs `valid_from <= D AND (valid_to > D OR valid_to IS NULL)` logic on each table; miss one and results are *silently wrong*, or you join snapshots from different points in time [^src4].

The append/datestamp alternative reduces every historical query to a flat `WHERE ds = '{date}'` filter per table — complexity stays in the business logic, not in date-range gymnastics [^src4]. **`ds`** (datestamp) marks when each row was valid/ingested; it is named `ds` rather than `date` to avoid confusion with the event date [^src4]. "Date partitions" are how warehouses physically implement datestamps — `WHERE ds='...'` scans one partition instead of the whole table, making it faster and cheaper [^src4].

The decisive pain is **backfilling**. SCD2's `valid_to`/`is_current` close-out logic chains each day to the previous day's state (`depends_on_past=True` in Airflow), forcing **sequential** reruns — backfilling November means 30 days run one-at-a-time, and the daily SQL doesn't even work for backfills (you maintain a *second* codebase that reconstructs `valid_from`/`valid_to` for historical dates) [^src4]. With datestamps each day reads/writes only its own `ds` partition with **no inter-day dependency**, so an Airflow `dags backfill` runs all 30 days **in parallel** with the *same* SQL — "a button you push" [^src4]. The one pattern to avoid is a table whose day depends on its own previous day's partition (cumulative metrics); for most dimensions, recompute from raw and keep `depends_on_past=False` [^src4]. See [[data-engineering/idempotent-pipelines|Idempotent Pipelines]] for the functional-pipeline framing this rests on.

## Not-yet-ingested related sources

- `scd2-joining-fact-dimension-tables` — querying SCD2 tables (companion article)

## See also

- [[data-engineering/merge-into|MERGE INTO]] — the Spark SQL operation used to implement this pattern
- [[data-engineering/apache-iceberg|Apache Iceberg]] — table format required for MERGE INTO in Spark SQL
- [[data-engineering/dimensional-modeling|Dimensional Modeling]] — the broader modeling context; streak_identifier pattern for building SCD2
- [[data-engineering/idempotent-pipelines|Idempotent Pipelines]] — SCD2 is idempotent; SCD1 and SCD3 are not
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [[03_Resources/Articles/scd2-table-creation-merge-into-spark-iceberg|SCD2 Table Creation with MERGE INTO in Spark and Iceberg]]
[^src2]: [[03_Resources/Study Notes/Dimensional Data Modeling - Idempotent Pipelines and SCD Patterns|Dimensional Data Modeling - Idempotent Pipelines and SCD Patterns]]
[^src3]: [Stop Using Slowly Changing Dimensions (Part 1)](../../raw/web/stop-using-slowly-changing-dimensions-part-1.md)
[^src4]: [SCD-2 considered harmful! Part 2](../../raw/email/email-2025-11-04-scd-2-considered-harmful-part-2.md)

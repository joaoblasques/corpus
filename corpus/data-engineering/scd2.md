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
  - path: raw/web/web-sql-to-dbt-guide-slowly-changing-dimensions-with-dbt-snapsho.md
    channel: web
    ingested_at: 2026-06-17
  - path: raw/web/web-how-to-join-a-fact-and-a-type-2-dimension-scd2-table-start-d.md
    channel: web
    ingested_at: 2026-06-25
  - path: raw/web/web-stop-using-slowly-changing-dimensions-part-1-c49c7e0e.md
    channel: web
    ingested_at: 2026-07-01
  - path: raw/web/web-scd-2-considered-harmful-part-2-d71941a6.md
    channel: web
    ingested_at: 2026-07-01
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
updated: 2026-06-25
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
- **Tool-agnostic** — works with Hive metastore, [Iceberg](/data-engineering/apache-iceberg.md), Delta, or Hudi

This is the *functional data engineering* lineage (Maxime Beauchemin), repackaged as date-stamping as the organizing principle, not an afterthought [^src3]. The trade-off is storage volume: daily full snapshots duplicate unchanged rows, which is precisely the cost SCD2 was designed to avoid at very large scale — see the "When to skip SCD entirely" thresholds above [^src2]. The two views agree on the boundary: SCD2 only pays off where storage savings outweigh complexity.

### Part 2: why SCD2 makes querying and backfilling painful

A follow-up sharpens the critique with concrete mechanics [^src4]. The motivating problem is **point-in-time state across multiple tables** ("for users who now have 1000+ followers but had under 200 three months ago, what device were they using then?") — a join over user, device, and relationship *state as of a past date* [^src4]. Under SCD2 every such join needs `valid_from <= D AND (valid_to > D OR valid_to IS NULL)` logic on each table; miss one and results are *silently wrong*, or you join snapshots from different points in time [^src4].

The append/datestamp alternative reduces every historical query to a flat `WHERE ds = '{date}'` filter per table — complexity stays in the business logic, not in date-range gymnastics [^src4]. **`ds`** (datestamp) marks when each row was valid/ingested; it is named `ds` rather than `date` to avoid confusion with the event date [^src4]. "Date partitions" are how warehouses physically implement datestamps — `WHERE ds='...'` scans one partition instead of the whole table, making it faster and cheaper [^src4].

The decisive pain is **backfilling**. SCD2's `valid_to`/`is_current` close-out logic chains each day to the previous day's state (`depends_on_past=True` in Airflow), forcing **sequential** reruns — backfilling November means 30 days run one-at-a-time, and the daily SQL doesn't even work for backfills (you maintain a *second* codebase that reconstructs `valid_from`/`valid_to` for historical dates) [^src4]. With datestamps each day reads/writes only its own `ds` partition with **no inter-day dependency**, so an Airflow `dags backfill` runs all 30 days **in parallel** with the *same* SQL — "a button you push" [^src4]. The one pattern to avoid is a table whose day depends on its own previous day's partition (cumulative metrics); for most dimensions, recompute from raw and keep `depends_on_past=False` [^src4]. See [Idempotent Pipelines](/data-engineering/idempotent-pipelines.md) for the functional-pipeline framing this rests on.

## dbt Snapshot strategies for SCD2

dbt snapshots implement SCD2 declaratively. Two strategies based on what triggers historical tracking [^src5]:

**Timestamp strategy** (`snap_campaign_performance`): captures a new historical record every time the source data updates, using a reliable `updated_at` column. Right fit when: metrics change frequently and every change matters (e.g., daily ROAS/conversion rate/budget utilization changes) [^src5].

**Check strategy** (`snap_visitor_segments`): creates a new record only when specific columns actually change, ignoring other updates. Right fit when: tracking categorical transitions (prospect → VIP buyer), not every data refresh [^src5].

> *"The strategy-to-use-case mapping is the core lesson: timestamp for metrics that change frequently, check for categorical shifts."* [^src5]

**Three query patterns** against snapshots (using the special dbt columns `dbt_valid_from`, `dbt_valid_to`, `dbt_updated_at`):

- **Current state**: `WHERE dbt_valid_to IS NULL`
- **Point-in-time**: `WHERE '2024-01-15' >= dbt_valid_from AND ('2024-01-15' < dbt_valid_to OR dbt_valid_to IS NULL)`
- **Trend analysis**: window function with `LAG(roas) OVER (PARTITION BY campaign_id ORDER BY dbt_valid_from)`

**dbt SCD2 costs** [^src5]: storage (a daily-changing campaign creates 365 records/year × thousands of campaigns); query complexity (date filters + window functions not every analyst is comfortable with); processing time (every `dbt snapshot` run compares current data against all historical records); and schema maintenance (snapshot schemas need monitoring; treat snapshot documentation like any other model).

Use `invalidate_hard_deletes=true` to handle deleted source records. Create mart models that pre-calculate common historical analyses to hide complexity from consumers.

## Joining a fact table to an SCD2 dimension

The canonical pattern uses an `AND ... BETWEEN` range join rather than a simple equality on `user_id` [^src6]. The key insight: each SCD2 row has `row_effective_datetime` and `row_expiration_datetime` defining the window during which it represents the entity state. A fact table record's timestamp is the probe; a join that also checks `purchased_datetime BETWEEN row_effective_datetime AND row_expiration_datetime` returns the correct historical state [^src6].

Example schema pair [^src6]:

```sql
-- fact table
CREATE TABLE items_purchased (
    item_purchased_id VARCHAR(40),
    order_id         VARCHAR(40),
    user_id          VARCHAR(40),
    item_cost        DECIMAL(10, 2),
    purchased_datetime TIMESTAMP
);

-- SCD2 dimension
CREATE TABLE user_dim (
    user_key                BIGINT,
    user_id                 VARCHAR(40),
    zipcode                 VARCHAR(10),
    row_effective_datetime  TIMESTAMP,
    row_expiration_datetime TIMESTAMP,
    current_row_indicator   VARCHAR(10)
);
```

Join pattern (example using a CTE) [^src6]:

```sql
WITH user_items AS (
    SELECT ip.user_id, ip.item_cost, ud.zipcode, ip.purchased_datetime
    FROM items_purchased ip
    JOIN user_dim ud
        ON  ip.user_id = ud.user_id
        AND ip.purchased_datetime BETWEEN ud.row_effective_datetime
                                      AND ud.row_expiration_datetime
)
SELECT EXTRACT(YEAR FROM purchased_datetime)  yr,
       EXTRACT(MONTH FROM purchased_datetime) mnth,
       zipcode,
       COUNT(DISTINCT user_id)                num_high_spenders
FROM user_items
GROUP BY yr, mnth, zipcode;
```

The `BETWEEN` join ensures each purchase maps to the user's address *as of that purchase date*, preserving historical accuracy [^src6]. Prefer the `9999-12-31` sentinel for the open-ended current row (see "end_date sentinel" section) so `BETWEEN` works without null-handling [^src2].

**Educating consumers**: end users must understand the join pattern before querying SCD2 tables directly. A common mitigation is wrapping the SCD2 table in a view or function that exposes a simpler interface [^src6].

## See also

- [MERGE INTO](/data-engineering/merge-into.md) — the Spark SQL operation used to implement this pattern
- [Apache Iceberg](/data-engineering/apache-iceberg.md) — table format required for MERGE INTO in Spark SQL
- [Dimensional Modeling](/data-engineering/dimensional-modeling.md) — the broader modeling context; streak_identifier pattern for building SCD2
- [Idempotent Pipelines](/data-engineering/idempotent-pipelines.md) — SCD2 is idempotent; SCD1 and SCD3 are not
- [Data Engineering hub](/data-engineering/README.md)

---

[^src1]: [SCD2 Table Creation with MERGE INTO in Spark and Iceberg](/03_Resources/Articles/scd2-table-creation-merge-into-spark-iceberg.md)
[^src2]: [Dimensional Data Modeling - Idempotent Pipelines and SCD Patterns](/03_Resources/Study Notes/Dimensional Data Modeling - Idempotent Pipelines and SCD Patterns.md)
[^src3]: [Stop Using Slowly Changing Dimensions (Part 1)](../../raw/web/stop-using-slowly-changing-dimensions-part-1.md)
[^src4]: [SCD-2 considered harmful! Part 2](../../raw/email/email-2025-11-04-scd-2-considered-harmful-part-2.md)
[^src5]: [SQL to dbt guide: Slowly Changing Dimensions with dbt Snapshots](../../raw/web/web-sql-to-dbt-guide-slowly-changing-dimensions-with-dbt-snapsho.md)
[^src6]: [How to Join a Fact and a Type 2 Dimension (SCD2) Table – Start Data Engineering](../../raw/web/web-how-to-join-a-fact-and-a-type-2-dimension-scd2-table-start-d.md)

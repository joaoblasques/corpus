---
type: concept
domain: data-engineering
status: draft
sources:
  - path: 03_Resources/Study Notes/Dimensional Data Modeling - Idempotent Pipelines and SCD Patterns.md
    channel: notes
    ingested_at: 2026-05-21
  - path: raw/_inbox/email-2025-09-09-learn-the-kimball-dimensional-modeling-with-a-dbt-project.md
    channel: email
    ingested_at: 2026-06-11
  - path: raw/web/data-identity-politics-and-the-kimball-vs-inmon-war.md
    channel: web
    ingested_at: 2026-06-11
  - path: raw/youtube/youtube-7jbcvxmj1bs.md
    channel: youtube
    ingested_at: 2026-06-17
aliases:
  - dimensional modeling
  - dimensional data modeling
  - fact and dimension tables
  - Kimball
  - Kimball method
  - star schema
  - grain
  - cumulative table design
  - temporal cardinality explosion
  - compactness vs usability
  - OLTP vs OLAP
  - master data
  - fixed dimension
tags:
  - corpus/data-engineering
  - concept
created: 2026-05-21
updated: 2026-06-17
---

# Dimensional Modeling

**TL;DR**: A data modeling approach structuring analytical data as facts (measurable events) and dimensions (context/attributes), optimized for analytical query patterns. SCD Type 2 is the canonical dimension pattern for tracking history [^src1]. Introduced by Ralph Kimball in the 1996 *Data Warehouse Toolkit*; popular because it aligns with how business users think — in measurable metrics observed across contexts (product, region, time) [^src2].

## Star schema

The dimensional model is implemented as a **star schema**: a central fact table surrounded by multiple dimension tables, named for its star-like shape [^src2].

- **Fact table** — central; stores performance measurements from business-process events. Each row is a measurement event holding *foreign keys* (links to dimensions) and *measures* (numeric values: revenue, quantity, profit). Kimball recommends storing the lowest-level measurements for flexibility [^src2].
- **Dimension table** — provides context (the "who, what, where, when, how, why"). Each focuses on one business dimension (product, country, date) and has a single primary key, distributed to fact tables as a foreign key. Without dimensions, a metric like revenue gives no insight [^src2].

## Grain

The **grain** is the level of detail represented by a single fact-table row [^src2]. > "all rows must be at the same grain level" [^src2]. Declaring the grain (transaction vs. daily summary vs. monthly aggregate) early ensures consistency and scalability. See also Joe Reis's extended treatment below.

### Grain: wrong grains in practice (Joe Reis, *Mixed Model Arts*)

Grain is one of the most critical decisions in any dataset. "Get it right, and your data makes sense and is useful. Get it wrong, and things break in often mysterious and painful ways." [^src5]

**Incompatible grains**: combining datasets without a common granularity directly creates no meaningful join. Dataset A at daily-product grain + Dataset B at transaction grain cannot be combined without rolling up. The "mixed-grain trap" — storing both in one table (some rows individual transactions, others daily totals) — is worse: a `SUM()` will double-count revenue silently [^src5].

**Fan-out**: the most common source of incorrect analytics. When joining tables with mismatched grains, rows multiply unintentionally [^src5]. Example: a `Customers` table (1 row per customer) joined to an `Orders` table (1 row per order) on `CustomerID` results in Alice (2 orders) appearing twice. The result grain is now "1 row per order" — `COUNT(customers)` returns 3 instead of 2; `SUM(signup_bonus)` double-counts Alice's value.

> "The danger isn't the join itself, but forgetting that the result's grain has changed." [^src5]

The fan-out join is *correct* for order-level analysis — the error is applying customer-level aggregations to the post-join result without accounting for the new grain. This is why declaring grain explicitly at every layer of the pipeline is not pedantry: it prevents silent double-counting.

## The Kimball four-step design process

A bottom-up sequence where each step builds on the last [^src2]:

1. **Select the business process** — identify the activity to analyze (sales, customer interactions).
2. **Declare the grain** — define the level of detail of a fact row.
3. **Identify the dimensions** — descriptive attributes (product, time, customer demographics).
4. **Identify the facts** — the quantitative measures tied to the process (revenue, profit).

## Kimball vs. Inmon (the resolved war)

The 1990s "Kimball vs. Inmon war" over data-warehouse methodology is largely settled: > "the industry didn't choose Kimball or Inmon. It chose both" [^src3]. Modern lakehouse architectures commonly use Inmon-style governance for raw/bronze layers and Kimball-style dimensional models (star schemas) for gold/serving layers [^src3]. See [[data-engineering/medallion-architecture|medallion architecture]] — the gold layer is where star schemas typically live, though medallion does not mandate any particular model.

## Dimensions, fixed vs slowly-changing (practitioner framing)

Zach Wilson (ex-Facebook/Netflix/Airbnb) defines a **dimension as an attribute of an entity** [^src4]. Two kinds [^src4]:
- **Fixed dimension** — a single immutable value (birthday, signup date, signup ID). Easy: just a table with columns, no modeling needed [^src4].
- **Slowly-changing dimension** — a value that shifts over time (favorite food), "nasty" to model — see [[data-engineering/scd2|SCD2]].

Data modeling is framed as an **empathetic exercise**: the goal is data your *consumers* actually use to make decisions, not the smallest/fastest data — "if your data is really fast and really compact and no one uses it... you failed" [^src4]. **Knowing your consumer** is the central discipline; the five consumer types are data analysts, other data engineers, ML models (often via a feature store), customers, and executives (treated like customers — give them the most distilled chart) [^src4].

## OLTP vs Master Data vs OLAP (the modeling continuum)

Three ways to model data, each matched to a consumer [^src4]:

| Model | Optimized for | Consumer | Anti-pattern cost |
|---|---|---|---|
| **OLTP** | single-record access/update (`WHERE user_id = 7`) | production apps (Postgres/MySQL/Mongo) | terrible for analytics — needs many joins |
| **Master data** | completeness of entity definitions, deduped | the trust/consistency layer | sits between OLTP and OLAP |
| **OLAP** | large-volume group-by, minimized joins | analytics/dimensional modeling | slow single-record access |

Mismatching model to consumer means "you're going to have a bad time" [^src4]. The **production-pipeline continuum**: production DB snapshots → **master data** (join/dedup/conform daily snapshots into the consistent "truth" layer) → OLAP cubes (group-bys/aggregates) → metrics (a single number per day) [^src4]. Rule of thumb: analytics consumers should **never query production database snapshots directly** — five analysts writing five pipelines on raw snapshots produce five subtly-different metrics; master data is where trust lives [^src4]. See [[data-engineering/medallion-architecture|Medallion Architecture]] for the bronze/silver/gold analogue.

## Cumulative table design

A pattern for tracking dimensions **over time inside one partition** so historical questions don't require querying 30 partitions [^src4]. Mechanism: **full-outer-join yesterday's cumulative table with today's snapshot**, coalesce IDs and unchanging dimensions, then **append today's value to an array** (e.g. a daily `is_active` boolean) [^src4]. The full outer join captures new, churned, resurrected, and deleted entities (present yesterday, absent today, or vice versa) [^src4].

- **Why it wins** — the latest partition holds all history in arrays of small booleans instead of repeating large string keys per day; answering "weekly active?" reads **one partition** and scans an array instead of querying 7 daily partitions (monthly active: ~97% less data read) [^src4]. Facebook's `dim_all_users` uses this — the table with the most downstream dependencies Wilson knew of (~15,000 pipelines) [^src4]. Historical and transition analysis (churn / resurrection / new / deleted) run **without shuffle** (just scan the array), so it's effectively infinitely scalable on engines like Trino/Presto [^src4].
- **Drawbacks** [^src4]: (1) **backfills must run sequentially** — each day depends on the prior, so you can't backfill 365 days in parallel (an 8-year backfill once took three weeks); (2) **PII / retention pain** — the design pulls all historical data forward, so deleted/inactive users persist in today's partition unless explicitly filtered (a real privacy hazard, cited around the Cambridge Analytica era). Also cap the array length (e.g. Facebook keeps 30 values for monthly-active) — unbounded arrays become hard to render and query [^src4].

## Compactness vs usability tradeoff

A spectrum of how to physically encode a dimension, traded against who must consume it [^src4]:

| Encoding | When to use | Consumer | Notes |
|---|---|---|---|
| **Most compact** (byte blob / custom codec) | minimize IO & latency (e.g. Airbnb calendar shipped to every client) | software engineers | not queryable without custom decoder |
| **Middle ground** (array/map/struct) | staging & **master data** layers | other data engineers / technical DS | "where I found a massive amount of impact" |
| **Most usable** (string/int/decimal/boolean only) | analyst-facing | non-technical analysts | no array/map/struct |

The governing rule: **usability beats compactness** unless you're at extreme scale, because employee time spent decoding a hard format eats the cloud savings ("30 minutes of employee time... you just ate all of your savings") [^src4]. The complex types `struct` (a "table within a table" — Trino's `ROW`), `array` (ordered, single-type), and `map` (typed keys/values) are the middle-ground tools [^src4].

## Temporal cardinality explosion

When adding a **temporal aspect** to a dimension increases its cardinality by **≥1 order of magnitude** [^src4]. Canonical example: Airbnb's ~10M listings × 365 nights = billions of rows [^src4]. The design choice: model at the **listing level with an array of nights** (~10M rows) vs the **listing-night level** (billions of rows) [^src4]. With the right sort order, parquet compression makes the two *about the same size on disk* — **but the array version survives joins** [^src4]:

- A join on the exploded listing-night table makes Spark (or any distributed engine) **shuffle the rows, destroying the run-length-encoding compression** — the downstream dataset balloons (e.g. from ~80% compression to ~15%) [^src4].
- Keeping nights together in an array means a join keeps the array intact (no shuffle), and consumers can explode *after* the join with all values still grouped [^src4]. So if your downstream consumers also produce datasets, prefer the array form. This ties dimensional modeling directly to physical [[data-engineering/parquet|Parquet]] RLE behavior.

## SCD type comparison

| Type | Strategy | Idempotent? | Use |
|---|---|---|---|
| **0** | Fixed attribute — never changes | ✅ | Birthdays, immutable facts |
| **1** | Overwrite old value | ❌ | **Never for analytics** — loses history |
| **2** | New row per change (start/end dates) | ✅ | Gold standard for analytics |
| **3** | Store original + current value | ❌ | Loses intermediate changes |

[^src1]

## SCD Type 2 structure

```sql
entity_id       -- the thing being tracked
dimension_value -- the attribute changing over time
start_date
end_date        -- prefer 9999-12-31 over NULL (better BETWEEN compatibility)
is_current      -- boolean
```

**Joining facts to SCD2 dimensions:**
```sql
SELECT f.*, d.dimension_value
FROM facts f
JOIN dimension_scd d
  ON f.entity_id = d.entity_id
 AND f.event_date BETWEEN d.start_date AND d.end_date
```
[^src1]

## Building SCD Type 2 — the streak_identifier pattern

For building SCD2 from a history of changes (e.g., NBA player active status), the standard approach uses four steps [^src1]:

**Step 1: Generate complete time series (fill gaps)**
```sql
CROSS JOIN GENERATE_SERIES(min_season, 2021) AS gs(season)
```

**Step 2: Identify change points with LAG**
```sql
CASE WHEN is_active != LAG(is_active, 1, FALSE) OVER (PARTITION BY player_name ORDER BY season)
     THEN 1 ELSE 0 END AS did_change
```

**Step 3: Assign streak IDs via cumulative sum of changes**
```sql
SUM(did_change) OVER (PARTITION BY player_name ORDER BY season) AS streak_id
```
Each time a change occurs, `streak_id` increments — all consecutive rows with the same attribute value share the same `streak_id`.

**Step 4: Collapse to SCD2 rows**
```sql
SELECT player_name, is_active,
       MIN(season) AS start_season,
       MAX(season) AS end_season,
       (MAX(season) = 2021) AS is_current
FROM identified
GROUP BY player_name, is_active, streak_id
```
[^src1]

## Deriving other SCD types from Type 2

Type 2 is the richest; other types can be derived [^src1]:

```sql
-- Type 1 (latest only) — loses history:
SELECT player_name, is_active FROM scd WHERE is_current = TRUE

-- Type 3 (original + current) — loses intermediate changes:
SELECT player_name,
       MAX(CASE WHEN rn = 1 THEN is_active END) AS original_active,
       MAX(CASE WHEN is_current THEN is_active END) AS current_active
FROM (SELECT *, ROW_NUMBER() OVER (PARTITION BY player_name ORDER BY start_season) rn FROM scd)
GROUP BY player_name
```

## When to skip SCD (use daily snapshots instead)

- Scale < 10–15M users — daily snapshots are simpler and cheap
- Rapidly changing dimensions (hourly) — SCD adds rows without storage benefit
- Rule of thumb: SCD only pays off at scale where storage savings matter [^src1]

SCDs must be **tables**, never views or stored procedures [^src1].

## See also

- [[data-engineering/scd2|SCD2]] — detailed implementation of Type 2
- [[data-engineering/idempotent-pipelines|Idempotent Pipelines]] — SCD2 requires idempotent pipeline design
- [[data-engineering/merge-into|MERGE INTO]] — the Spark SQL mechanism for applying SCD2 updates atomically
- [[data-engineering/sql-window-functions|SQL Window Functions]] — LAG and cumulative SUM reference; the functions that power the streak_identifier pattern
- [[data-engineering/medallion-architecture|Medallion Architecture]] — gold layer is a common home for star schemas; orthogonal to modeling choice
- [[data-engineering/dbt|dbt]] — common tool for implementing Kimball models in SQL
- [[data-engineering/parquet|Parquet]] — run-length encoding behind the compactness/cardinality tradeoffs
- [[data-engineering/data-modeling-meaning|Meaning in Data Modeling]] — semantics/master-data layer
- [[data-engineering/README|Data Engineering hub]]

## See also (updated)

- [[data-engineering/sql-intermediate-results|Storing Intermediate Results in SQL]] — grain-aware staging table decisions

---

[^src1]: [[03_Resources/Study Notes/Dimensional Data Modeling - Idempotent Pipelines and SCD Patterns|Dimensional Data Modeling - Idempotent Pipelines and SCD Patterns]]
[^src2]: [Learn the Kimball dimensional modeling with a dbt project](../../raw/email/email-2025-09-09-learn-the-kimball-dimensional-modeling-with-a-dbt-project.md)
[^src3]: [Data Identity Politics and The Kimball vs. Inmon War](../../raw/web/data-identity-politics-and-the-kimball-vs-inmon-war.md)
[^src4]: [Dimensional Data Modeling Day 1 (Zach Wilson / DataExpert)](../../raw/youtube/youtube-7jbcvxmj1bs.md)
[^src5]: [Ch. 8 — Grain: Getting the Level Right (Joe Reis, Mixed Model Arts)](../../raw/web/web-ch-8-grain-getting-the-level-right.md)

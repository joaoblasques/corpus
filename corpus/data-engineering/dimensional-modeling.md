---
type: concept
domain: data-engineering
status: draft
sources:
  - path: 03_Resources/Study Notes/Dimensional Data Modeling - Idempotent Pipelines and SCD Patterns.md
    channel: notes
    ingested_at: 2026-05-21
aliases:
  - dimensional modeling
  - dimensional data modeling
  - fact and dimension tables
tags:
  - corpus/data-engineering
  - concept
created: 2026-05-21
updated: 2026-05-21
---

# Dimensional Modeling

**TL;DR**: A data modeling approach structuring analytical data as facts (measurable events) and dimensions (context/attributes), optimized for analytical query patterns. SCD Type 2 is the canonical dimension pattern for tracking history [^src1].

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
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [[03_Resources/Study Notes/Dimensional Data Modeling - Idempotent Pipelines and SCD Patterns|Dimensional Data Modeling - Idempotent Pipelines and SCD Patterns]]

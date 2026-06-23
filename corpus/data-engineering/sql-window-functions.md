---
type: concept
domain: data-engineering
status: draft
sources:
  - path: 03_Resources/Study Notes/SQL - Window Functions Reference.md
    channel: notes
    ingested_at: 2026-05-21
  - path: raw/email/email-2025-07-20-de101-2-sql-is-crucial-for-data-engineers.md
    channel: email
    ingested_at: 2026-06-19
aliases:
  - window functions
  - SQL window functions
  - OVER clause
  - ROW_NUMBER
  - RANK
  - DENSE_RANK
  - LAG
  - LEAD
tags:
  - corpus/data-engineering
  - concept
created: 2026-05-21
updated: 2026-06-23
last_confirmed: 2026-06-19
---

# SQL Window Functions

**TL;DR**: Compute values across a set of rows related to the current row without collapsing rows like `GROUP BY` does — you keep individual row detail AND get group/ordered context [^src1].

## Syntax template

```sql
FUNCTION_NAME(col) OVER (
  PARTITION BY col(s)   -- divide into groups
  ORDER BY col(s)       -- order within groups
  frame_clause          -- which rows to include
)
```

## The seven functions

### Ranking

| Function | Ties | Skips ranks? | Use when |
|---|---|---|---|
| `ROW_NUMBER()` | Unique always | No | Need stable unique position |
| `RANK()` | Same rank | Yes — jumps after ties | Olympic-style ranking |
| `DENSE_RANK()` | Same rank | No — consecutive | Ranking without gaps |

```sql
SELECT sale_id, sale_date, sale_amount,
  ROW_NUMBER()  OVER (ORDER BY sale_date) AS row_num,
  RANK()        OVER (ORDER BY sale_date) AS rnk,
  DENSE_RANK()  OVER (ORDER BY sale_date) AS dense_rnk
FROM sales;
-- Ties on same date:  ROW_NUMBER: 1,2,3 | RANK: 1,1,3 | DENSE_RANK: 1,1,2
```

### Running aggregates

```sql
-- Running total overall
SUM(sale_amount) OVER (ORDER BY sale_date) AS running_total

-- Running total per group (resets per partition)
SUM(sale_amount) OVER (PARTITION BY employee_id ORDER BY sale_date) AS running_total_per_emp
```

### LAG / LEAD

```sql
LAG(col, offset, default)  OVER (PARTITION BY ... ORDER BY ...)
LEAD(col, offset, default) OVER (PARTITION BY ... ORDER BY ...)
```

- **LAG**: period-over-period comparison (MoM, DoD), previous-state capture
- **LEAD**: look-ahead comparisons, forecasting context
- Always supply the `default` (3rd arg) — returns NULL at partition edges otherwise [^src1]

## Frame clauses

```sql
ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW       -- running total (default when ORDER BY present)
ROWS BETWEEN 6 PRECEDING AND CURRENT ROW               -- 7-day rolling average
ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING  -- full partition aggregate
```

Default frame when `ORDER BY` present: `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` (includes ties in ordering column). Use `ROWS` explicitly to avoid unexpected tie-inclusion behavior [^src1].

## Interview cheat sheet

| Business problem | Function |
|---|---|
| Unique row number | `ROW_NUMBER()` |
| Rank with gaps on ties | `RANK()` |
| Rank without gaps | `DENSE_RANK()` |
| Running total / cumulative sum | `SUM() OVER (ORDER BY ...)` |
| Month-over-month comparison | `LAG()` |
| Day-ahead preview | `LEAD()` |
| Top N per group | `ROW_NUMBER()` + `WHERE row_num <= N` |

## Usage in data engineering

Window functions appear throughout the DE stack [^src1]:
- **dbt models**: enrichment and ranking in `warehouse` and `marts` layers — see [[data-engineering/dbt|dbt]]
- **Spark SQL**: same syntax; used in pipeline transformations
- **SCD2 construction**: `LAG()` identifies change points; cumulative `SUM()` builds streak IDs — see [[data-engineering/dimensional-modeling|Dimensional Modeling]] (streak_identifier pattern)

## See also

- [[data-engineering/dimensional-modeling|Dimensional Modeling]] — streak_identifier pattern uses LAG + cumulative SUM as core building blocks
- [[data-engineering/dbt|dbt]] — window functions used in mart-layer enrichment
- [[data-engineering/data-transformation|Data Transformation]] — the transform layer where these functions are applied (categorization, enrichment, pre-aggregation)
- [[data-engineering/sql-intermediate-results|Storing Intermediate Results in SQL]] — CTEs/temp tables that hold the window-function logic
- [[data-engineering/data-engineering-interview|Data Engineering Interview]] — window functions are a recurring SQL-round topic
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [[03_Resources/Study Notes/SQL - Window Functions Reference|SQL - Window Functions Reference]]

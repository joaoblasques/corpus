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
aliases:
  - SCD2
  - Slowly Changing Dimension Type 2
  - slowly changing dimension
tags:
  - corpus/data-engineering
  - concept
created: 2026-05-07
updated: 2026-05-21
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

## Not-yet-ingested related sources

- `Modern Data Warehousing - Stop Using SCD Part 1` — counterpoint on SCD usage
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

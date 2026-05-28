---
type: concept
domain: data-engineering
status: draft
sources:
  - path: 03_Resources/Articles/scd2-table-creation-merge-into-spark-iceberg.md
    channel: notes
    ingested_at: 2026-05-07
aliases:
  - MERGE INTO
  - merge into
  - Spark MERGE INTO
tags:
  - corpus/data-engineering
  - concept
created: 2026-05-07
updated: 2026-05-07
---

# MERGE INTO

**TL;DR**: A Spark SQL statement that atomically combines insert, update, and delete actions against a target table in a single operation, replacing multi-query workflows [^src1].

## Three clauses

| Clause | Trigger | Allowed actions |
|---|---|---|
| `WHEN MATCHED` | Row exists in both source and target | UPDATE, DELETE |
| `WHEN NOT MATCHED` | Row exists in source only | INSERT |
| `WHEN NOT MATCHED BY SOURCE` | Row exists in target only | UPDATE, DELETE |

## Key mechanic: the NULL join_key

For patterns that need to both update an existing row AND insert a new row for the same entity (e.g., SCD2 history), a `UNION ALL` source with a `NULL` join key is used [^src1]:

```sql
SELECT customer_id AS join_key, * FROM prod.db.customer
UNION ALL
SELECT NULL AS join_key, * FROM customers_with_updates
```

`NULL` never matches the `ON` join condition, so it always routes to `WHEN NOT MATCHED → INSERT`. This lets a single MERGE close an old row (via MATCHED) and open a new one (via NOT MATCHED with NULL key) atomically [^src1].

## Atomicity

The entire statement executes as one atomic operation. A failure mid-execution leaves the target in its pre-merge state — no partial writes [^src1].

## Performance constraint

Internally executes as a full outer join. Suitable only for dimension tables of manageable size. Using MERGE INTO on large fact tables will cause performance problems [^src1].

## See also

- [[data-engineering/scd2|SCD2]] — primary use case for this pattern in data modeling
- [[data-engineering/apache-iceberg|Apache Iceberg]] — table format that supports MERGE INTO in Spark SQL
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [[03_Resources/Articles/scd2-table-creation-merge-into-spark-iceberg|SCD2 Table Creation with MERGE INTO in Spark and Iceberg]]

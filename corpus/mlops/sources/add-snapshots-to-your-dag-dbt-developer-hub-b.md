---
type: source
domain: mlops
status: draft
sources:
  - path: raw/web/web-add-snapshots-to-your-dag-dbt-developer-hub.md
    channel: web
    ingested_at: 2026-07-21
aliases: []
tags:
  - corpus/mlops
  - source
  - doc-quick-intake
created: 2026-07-21
updated: 2026-08-16
provisional: false
url: https://docs.getdbt.com/docs/building-a-dbt-project/snapshots/
origin: obsidian-list
---

# Add snapshots to your DAG | dbt Developer Hub

> [dbt Developer Hub](https://docs.getdbt.com/docs/building-a-dbt-project/snapshots/)

## TL;DR

dbt snapshots implement type-2 Slowly Changing Dimensions (SCDs) over mutable source tables by recording row-level changes over time. Two built-in strategies — `timestamp` and `check` — determine how dbt detects changes. The `timestamp` strategy is preferred for its robustness to schema evolution.[^1]

---

## What snapshots solve

Source tables are often mutable: a record is overwritten when its state changes, destroying historical information. For example, an `orders` row moves from `pending` to `shipped` and the prior state is lost. dbt snapshots preserve every version of each row by appending new records with validity windows (`dbt_valid_from` / `dbt_valid_to`).[^1]

Example snapshot output:

| id | status | updated_at | dbt_valid_from | dbt_valid_to |
|----|--------|------------|----------------|--------------|
| 1  | pending | 2024-01-01 | 2024-01-01 | 2024-01-02 |
| 1  | shipped | 2024-01-02 | 2024-01-02 | null |

Current records have `dbt_valid_to = null` by default; dbt Core v1.9+ allows setting `dbt_valid_to_current` to a sentinel date (e.g. `9999-12-31`) for cleaner date-range filtering.[^1]

---

## Snapshot strategies

### Timestamp (recommended)

Uses a single `updated_at` column to detect changes. If the column value is more recent than the last snapshot run, dbt invalidates the old record and inserts the new one; unchanged timestamps are skipped.[^1]

Required config: `updated_at` — the column representing when the source row was last updated (supports ISO date strings and unix epoch integers, depending on platform).[^1]

> "Automatically handles new or removed columns in the source table" — less prone to errors as schema evolves.[^1]

Preferred because it requires tracking only one column and is robust to column additions/removals, unlike `check` which requires updating `check_cols` when the schema changes.[^1]

### Check

Compares a configured list of columns between current and historical values. Useful for tables without a reliable `updated_at` column. If any of the listed columns change, dbt invalidates the old record and records the new one.[^1]

Required config: `check_cols` — a list of columns (e.g. `["name", "email"]`) or `'all'` to check every column. Explicitly enumerating columns is preferred over `'all'`; a surrogate key can condense many columns into one.[^1]

---

## How `dbt snapshot` runs

- **First run**: creates the snapshot table from the `select` statement, adding `dbt_valid_from` and `dbt_valid_to` columns. All records get `dbt_valid_to = null` (or `dbt_valid_to_current` if configured).[^1]
- **Subsequent runs**: compares source rows against the snapshot table using the unique key. Changed or new records are inserted; `dbt_valid_to` on stale records is updated to close the validity window.[^1]

The command must be run on a schedule (e.g. via a cron job or orchestrator) — dbt does not auto-execute it.[^1]

---

## Key configuration notes

- **Unique key**: must be genuinely unique; dbt uses it to match rows across runs. A uniqueness test on the source is recommended.[^1]
- **Downstream references**: snapshot tables are referenced in downstream models using the standard `ref()` function, the same as any dbt model.[^1]
- **`dbt_valid_to_current`** (dbt Core v1.9+): sets a non-null sentinel on current records instead of `null`, enabling straightforward date-range filtering without null checks.[^1]

---

[^1]: [raw/web/web-add-snapshots-to-your-dag-dbt-developer-hub.md](../../../raw/web/web-add-snapshots-to-your-dag-dbt-developer-hub.md) — dbt Developer Hub, collected 2026-07-20.

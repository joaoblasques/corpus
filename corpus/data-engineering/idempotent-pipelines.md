---
type: concept
domain: data-engineering
status: draft
sources:
  - path: 03_Resources/Study Notes/Dimensional Data Modeling - Idempotent Pipelines and SCD Patterns.md
    channel: notes
    ingested_at: 2026-05-21
aliases:
  - idempotent pipeline
  - idempotency
  - pipeline idempotency
tags:
  - corpus/data-engineering
  - concept
created: 2026-05-21
updated: 2026-05-21
---

# Idempotent Pipelines

**TL;DR**: A pipeline is idempotent when it produces the same result regardless of when, how many times, or at what hour it runs. Mathematically: `f(x) = y` — same input always yields same output. Non-idempotency causes silent data quality bugs, backfill inconsistencies, and tests that pass while production fails [^src1].

## Why it matters

Non-idempotent pipelines create a class of bugs that are exceptionally hard to detect: "tests that pass but prod fails." These bugs typically surface during backfills — when a pipeline runs over historical data — and produce results inconsistent with the original production run [^src1].

**Backfill reliability is the real test of idempotency.**

## Common pitfalls and fixes

| Pitfall | Problem | Fix |
|---|---|---|
| `INSERT INTO` without prior `TRUNCATE` | Re-runs append duplicates | `TRUNCATE TABLE` then `INSERT INTO` |
| Open-ended date filter (`date > X`) | Different data returned on backfill vs prod | Use fixed windows: `date BETWEEN X AND Y` |
| Incomplete partition sensors | Processes partial upstream data | Wait for all upstream partitions to land |
| Missing `depends_on_past` on cumulative jobs | Out-of-order execution breaks accumulation | Always set in Airflow for cumulative pipelines |
| Relying on `_LATEST_` partition | Backfill picks up current data, not historical | Use specific dated partitions [^src1] |

**Exception:** a properly built SCD Type 2 table can be used as a `_LATEST_`-equivalent because it encodes point-in-time history correctly [^src1].

## Loading strategies and idempotency trade-offs

| Strategy | Idempotent? | Cost | When to use |
|---|---|---|---|
| **Full Reload** | ✅ | High at scale | Simple pipelines; early-stage; correctness over efficiency |
| **Incremental** | ✅ (if designed correctly) | Low at scale | Large tables; requires careful `depends_on_past` and fixed-window filters |

Full reload is easier to make idempotent. Incremental pipelines require explicit windowing and careful state management [^src1].

## SCDs and idempotency

| SCD Type | Idempotent? | Notes |
|---|---|---|
| Type 0 | ✅ | Immutable — never changes by design |
| Type 1 | ❌ | Overwrites history — different result on re-run |
| Type 2 | ✅ | New row per change; history preserved; safe to backfill |
| Type 3 | ❌ | Loses intermediate changes |

SCD Type 2 is the only acceptable type for analytics history tracking that maintains idempotency [^src1]. See [[data-engineering/scd2|SCD2]].

## See also

- [[data-engineering/scd2|SCD2]] — idempotent history-preserving dimension pattern
- [[data-engineering/dimensional-modeling|Dimensional Modeling]] — the data modeling context in which idempotency matters most
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [[03_Resources/Study Notes/Dimensional Data Modeling - Idempotent Pipelines and SCD Patterns|Dimensional Data Modeling - Idempotent Pipelines and SCD Patterns]]

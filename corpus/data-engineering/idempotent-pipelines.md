---
type: concept
domain: data-engineering
status: draft
sources:
  - path: 03_Resources/Study Notes/Dimensional Data Modeling - Idempotent Pipelines and SCD Patterns.md
    channel: notes
    ingested_at: 2026-05-21
  - path: raw/email/email-2025-11-04-scd-2-considered-harmful-part-2.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/web/data-pipeline-design-patterns-1-data-flow-patterns-start-dat.md
    channel: web
    ingested_at: 2026-06-19
aliases:
  - idempotent pipeline
  - idempotency
  - pipeline idempotency
  - functional data engineering
  - datestamps
  - ds column
tags:
  - corpus/data-engineering
  - concept
created: 2026-05-21
updated: 2026-06-19
---

# Idempotent Pipelines

**TL;DR**: A pipeline is idempotent when it produces the same result regardless of when, how many times, or at what hour it runs. Mathematically: `f(x) = y` — same input always yields same output. Non-idempotency causes silent data quality bugs, backfill inconsistencies, and tests that pass while production fails [^src1].

## Why it matters

Non-idempotent pipelines create a class of bugs that are exceptionally hard to detect: "tests that pass but prod fails." These bugs typically surface during backfills — when a pipeline runs over historical data — and produce results inconsistent with the original production run [^src1].

**Backfill reliability is the real test of idempotency.**

### Prerequisite: a replayable source and an overwritable sink

Idempotency is not free — it is only *achievable* when two data-flow properties hold: the **source is replayable** (it can answer "what did the data look like *n* periods ago?" — e.g. an event stream, logs, or a CDC/WAL dump, but not a constantly-mutated OLTP table) and the **sink is overwritable** (rows are addressable by a unique key, or storage is namespaced by a unique run id) [^src3]. Lacking either, you cannot rerun cleanly; the pragmatic fallback is a **self-healing pipeline**, where the *next* run catches up failed/unprocessed data instead of guaranteeing identical reruns — simpler to build, but bugs can hide for several runs [^src3]. See [Data Flow Patterns](/data-engineering/data-flow-patterns.md) for the full extraction/behavioral/structural taxonomy this sits in.

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

SCD Type 2 is the only acceptable type for analytics history tracking that maintains idempotency [^src1]. See [SCD2](/data-engineering/scd2.md).

## Functional data engineering and datestamps

"Idempotent" is the operational face of **functional data engineering** (Maxime Beauchemin): pipelines that, like pure functions, give the same output for the same input and rely on **no hidden/secret state** [^src2]. The practical implementation is **datestamps** — append a `ds` column recording the date the data was valid/ingested, never overwrite [^src2]:

- The rawest upstream data is never deleted — keep appending with datestamps [^src2].
- A pipeline runs identically in daily and backfill mode (same SQL, different `ds` parameter — `WHERE ds='{{ ds }}'` injected by the orchestrator) [^src2].
- Bugs are fixed by correcting the pipeline and re-running the affected `ds` range; the corrected partition overwrites the bad one [^src2].
- Time travel is built in: filter to any `ds` [^src2].

### Parallel backfills as the payoff

The clearest proof of idempotency is the backfill. When each day reads and writes only its own `ds` partition with **no dependency on the previous day**, an orchestrator can launch the whole range **in parallel** — the entire month finishes in roughly the time of one day's run, using the exact same SQL as the daily job [^src2]. The anti-pattern to avoid: a task that depends on the **previous day's partition of its own table**, which forces sequential, un-parallelizable backfills (the `depends_on_past=True` chain) [^src2]. This is sometimes unavoidable for cumulative metrics, but most dimension tables should recompute from raw each day and keep `depends_on_past=False` [^src2]. See [SCD2](/data-engineering/scd2.md) for how this critique applies to slowly-changing dimensions specifically.

## See also

- [SCD2](/data-engineering/scd2.md) — idempotent history-preserving dimension pattern; datestamps vs valid_from/valid_to
- [Dimensional Modeling](/data-engineering/dimensional-modeling.md) — the data modeling context in which idempotency matters most
- [Incremental Pipeline Design](/data-engineering/incremental-pipeline-design.md) — extraction, load, and backfill design decisions
- [Data Flow Patterns](/data-engineering/data-flow-patterns.md) — idempotent vs self-healing as behavioral choices; the replayability/overwritability prerequisites
- [Data Engineering hub](/data-engineering/README.md)

---

[^src1]: [Dimensional Data Modeling - Idempotent Pipelines and SCD Patterns](/03_Resources/Study Notes/Dimensional Data Modeling - Idempotent Pipelines and SCD Patterns.md)
[^src2]: [SCD-2 considered harmful! Part 2](../../raw/email/email-2025-11-04-scd-2-considered-harmful-part-2.md)
[^src3]: [Data Pipeline Design Patterns - #1 Data Flow Patterns](../../raw/web/data-pipeline-design-patterns-1-data-flow-patterns-start-dat.md)

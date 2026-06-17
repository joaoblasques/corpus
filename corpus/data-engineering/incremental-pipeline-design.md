---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/web/3-design-decisions-for-maintainable-incremental-data-pipelin.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-06-10-3-design-decisions-for-maintainable-incremental-pipelines.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/web/web-full-refresh-vs-incremental-pipelines.md
    channel: web
    ingested_at: 2026-06-17
aliases:
  - incremental pipeline design
  - incremental load strategy
  - incremental load
  - backfilling
  - bootstrap
  - extraction logic
  - full refresh
  - WAP pattern
  - write-audit-publish
tags:
  - corpus/data-engineering
  - concept
created: 2026-06-12
updated: 2026-06-17
---

# Incremental Pipeline Design

**TL;DR.** Maintainable incremental pipelines come down to three decisions: (1) **extraction logic is dictated by the source's timestamp columns**, (2) **load strategy is dictated by the destination data model**, and (3) **pipelines must be designed for easy backfilling** [^src1]. Get these right and large-scale pipelines "just chug along"; get them wrong and they require painful manual intervention [^src1][^src2].

## Decision 1 — the source's timestamp column dictates extraction

Three source-column situations determine how to pull incremental changes for a window `start_ts → end_ts` [^src1]:

| Source has | Extraction logic |
|---|---|
| **`updated_at`** | `WHERE updated_at >= start_ts AND updated_at < end_ts`. Preferred. Ensure `updated_at` is set to `inserted_at` on initial creation [^src1] |
| **`inserted_at` only** (append-only, e.g. facts) | `WHERE inserted_at >= start_ts AND inserted_at < end_ts`, or `WHERE inserted_at > (SELECT max(inserted_at) FROM destination)` [^src1] |
| **Neither** | Compare source vs destination by **primary key** (left join, keep `d.pk IS NULL`); if no PK, **construct one** (e.g. md5 hash of the row / composite key) and diff on the hash [^src1] |

The same patterns apply to API pulls [^src1]. Third-party data dumped to S3/SFTP/FTP may need a **full load first**, after which the above incremental patterns apply [^src1].

## Decision 2 — the destination data model dictates load strategy

Three load strategies, matched to output type [^src1]:

| Strategy | How | Re-runnability | Common models |
|---|---|---|---|
| **Overwrite partitions** | Replace whole partitions per run; destination partitioned by event time (`created_at`/`updated_at`); e.g. `overwritePartitions` | **Gold standard** — re-runnable with no manual intervention | Facts, snapshot dimensions [^src1] |
| **Row-based update/insert/delete** | Modify rows by id; `MERGE INTO`, `INSERT ON CONFLICT`, `DELETE & INSERT` | Inefficient; needs a clean-up step before re-run | [[data-engineering/scd2|SCD2]], updating destination tables [^src1] |
| **Append** | Append all rows | Fine where duplication is OK or de-duped downstream | High-velocity stream ingest; Kafka at-most-once settings [^src1] |

Overwrite-partition is favored precisely because it is **idempotent** without manual cleanup — re-running a window reproduces the same partition. Row-based loads (the [[data-engineering/merge-into|MERGE INTO]] family) require destination cleanup before a backfill. See [[data-engineering/idempotent-pipelines|Idempotent Pipelines]].

## Decision 3 — design for easy backfilling

Backfills are inevitable; make them run without manual intervention [^src1]. **Running a backfill = running the pipeline for a past time range** [^src1]. If a load step uses **Update or Delete** (or the pipeline depends on the destination in any way), the destination must be **cleaned up before** the backfill [^src1].

Three backfill scaling strategies, easiest → hardest [^src1]:

1. **Single process** — one run over the full range; needs enough resources to process everything at once.
2. **Serial pipeline runs** — most orchestrators support this, but a pipeline can stay "perpetually catching up" (backfilling a 12 h daily run over 2 years takes ~1 year to catch up).
3. **Parallel pipeline runs** — only possible when runs are **independent**: the destination is not read during load and there are no look-back calculations.

These combine (1+2 or 1+3) depending on resources, data size, and deadline [^src1]. **Bootstrap** — running once over all history, then switching to incremental — is a special case of backfilling and is almost always recommended for the first run [^src1].

## Schema changes

**Additive** schema changes are usually fine — widening a type (`int → long`) or adding columns — and can be handled automatically if you have schema evolution [^src1]. **Column-meaning changes require manual intervention** [^src1].

## Decision chart (summary)

> Incremental loading strategy depends on the **nature of the source** (which timestamp columns exist) and the **model of your destination tables** (fact/dimension/SCD) [^src1].

## Full refresh vs incremental: the five tradeoff dimensions

The choice between full refresh and incremental loading has implications across five dimensions [^src3]:

| Dimension | Full Refresh | Incremental |
|---|---|---|
| **Compute cost** | Expensive for large tables — rebuilds everything each run | Processes only changed data |
| **Implementation ease** | Very simple (`CREATE OR REPLACE`) | Requires understanding the data's update behavior |
| **Backfilling** | Click rerun — done; painful for large/slow tables | Depends on load strategy: overwrite-partition is easy; row-based needs cleanup |
| **Updates/deletes** | Naturally handles them (row simply disappears or changes in next snapshot) | Must handle explicitly (MERGE, soft deletes) |
| **Tooling constraints** | Always available | Some platforms historically lacked MERGE (early Redshift); always check platform support |

**Full refresh works well when** [^src3]:
- Dataset is relatively small.
- Rebuilding is inexpensive.
- Underlying data has no reliable change tracking.
- Simplicity matters more than efficiency.

Full refresh breaks down when: table is large (copying hourly is slow/expensive), business needs fresher data than the batch window allows, or deletes must be tracked accurately [^src3].

## WAP Pattern (Write-Audit-Publish) for full refreshes

A safety wrapper pairing naturally with full refresh [^src3]:

1. **Write** — create a staged version of the dataset (full transformation from source).
2. **Audit** — run data quality checks on staged data: row count comparisons vs. previous version, null checks on required columns, duplicate key detection, metric range validation. If any check fails, stop before touching the production table.
3. **Publish** — if all checks pass, promote staged data to production.

Pairing WAP with full refresh provides a quality gate without modifying production data directly. The same write-audit-publish approach applies to incremental patterns. See [[data-engineering/data-quality|Data Quality]] for the full DQ framework.

## See also

- [[data-engineering/idempotent-pipelines|Idempotent Pipelines]] — why overwrite-partition + fixed windows make backfills safe and parallel
- [[data-engineering/data-ingestion-patterns|Data Ingestion Patterns]] — stream vs batch entry point
- [[data-engineering/scd2|SCD2]] — the row-based-update load case; datestamp alternative
- [[data-engineering/merge-into|MERGE INTO]] — the row-based update/insert/delete mechanism
- [[data-engineering/change-data-capture|Change Data Capture]] — full load vs incremental vs CDC
- [[data-engineering/data-orchestration|Data Orchestration]] — orchestrator backfill semantics
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [3 Design Decisions for Maintainable Incremental Data Pipelines](../../raw/web/3-design-decisions-for-maintainable-incremental-data-pipelin.md)
[^src2]: [3 Design Decisions for Maintainable Incremental Pipelines (email)](../../raw/email/email-2026-06-10-3-design-decisions-for-maintainable-incremental-pipelines.md)
[^src3]: [Full Refresh vs Incremental Pipelines](../../raw/web/web-full-refresh-vs-incremental-pipelines.md)

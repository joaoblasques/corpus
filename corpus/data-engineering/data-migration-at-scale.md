---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/web/migrating-data-ingestion-systems-at-meta-scale.md
    channel: web
    ingested_at: 2026-06-15
  - path: raw/email/email-2026-05-14-duckdb-goes-remote-when-lakehouses-guess-netflix-tames-data.md
    channel: email
    ingested_at: 2026-06-15
aliases:
  - data migration
  - shadow migration
  - reverse shadow
  - large-scale migration
  - data ingestion migration
tags:
  - corpus/data-engineering
  - concept
created: 2026-06-15
updated: 2026-06-15
---

# Data Migration at Scale

**TL;DR.** Migrating a live data system without losing data or trust requires a **phased shadow lifecycle** — run old and new systems side-by-side, compare outputs continuously, and promote/roll back per job automatically. Meta migrated 100% of its petabyte-scale data-ingestion system (one of the world's largest MySQL deployments) using a **Shadow → Reverse Shadow → Cleanup** lifecycle with row-count + checksum verification, automated promotion tooling, and fast rollback [^src1]. The same pattern (continuous comparison + automated promotion) underlies safe large-scale cutovers generally [^src2].

## The migration lifecycle

Each job must pass success criteria before advancing a stage [^src1]:
- **No data-quality issues** — identical row count *and* checksum between old and new systems.
- **No landing-latency regression** — new system matches or beats old.
- **No resource (compute/storage) regression**.
- Extra agreed criteria for critical tables, negotiated with dependent teams.

### Phase 1 — Shadow

Set up **shadow jobs** in pre-production consuming the same source as production but writing to a separate **shadow table** — a production-realistic test in an isolated place [^src1]. Continuously monitor row-count/checksum mismatches; on mismatch, find root cause, deploy a fix to pre-prod, verify resolution [^src1]. Also measure compute/storage quotas to confirm capacity before proceeding [^src1].

### Phase 2 — Reverse Shadow

Once both run reliably in production, **swap roles**: the shadow job now writes to the **production** table (becoming the new production job), and the original production job writes to the **shadow** table (becoming the shadow) [^src1]. Two benefits [^src1]:
1. Ongoing data-quality signals — keep comparing outputs after rollout.
2. **Fast rollback** — if discrepancies appear, revert without recreating/reconfiguring the old system.

### Phase 3 — Cleanup

Keep comparing; if no discrepancies, remove the shadow job (now the *old* system) — the new system fully owns the production job, completing the migration [^src1].

## CDC makes rollback essential

Both systems used **[change data capture](/data-engineering/change-data-capture.md)** to incrementally ingest. A property of CDC: *generated data feeds the next generation*, so problematic data **propagates** — any bad landed data passes to new landed data [^src1]. Two mitigations [^src1]:
- **Early signals after rollout** — during reverse shadow, trigger backfill on both jobs; if results still match, success; if not, roll back immediately so consumers are never impacted.
- **Stop the bleeding on rollback** — mark a partition's metadata as bad-quality; a bad *delta* partition halts new landing + alerts; a bad *target* partition makes the system pick an older partition and merge more deltas. On rollback, query metadata for all bad partitions and fix with backfill.

## Executing at scale (tens of thousands of jobs)

- **Automated promotion** — jobs continuously emit lifecycle + criteria signals (to Scuba); external tooling auto-promotes/demotes jobs between stages based on whether they meet criteria, with system- and job-level dashboards [^src1].
- **Custom DQ analysis tooling** — for each landed shadow partition, read the matching prod partition, compare row count + checksum, log mismatches; hourly, query example mismatching rows and log debug info — enabling fast root-cause and dedup of known issues. (Still used post-migration for release validation.) [^src1]
- **Batch planning with limited capacity** — can't shadow everything at once; migrate in **batches** selected by throughput/priority/special-case, excluding jobs with known unresolved issues to reduce noise; notify dependent teams ahead [^src1].
- **Avoid wasteful full dumps** — a new job's first snapshot lands via a slow/expensive **full dump**; creating shadow jobs while bugs exist triggers redundant full dumps (at creation and again during remediation). Avoiding those, and reusing old-system snapshot partitions as the initial snapshot, improved efficiency [^src1].

## Pattern summary

The transferable pattern: **run both systems → compare continuously (row count + checksum) → promote per-job automatically on objective criteria → keep the old system live as a shadow for fast rollback → clean up only when proven**. This complements [CI/CD](/data-engineering/cicd-for-data-infrastructure.md)'s plan-then-gate discipline and the idempotency required for safe backfills.

## Related

- [Change Data Capture](/data-engineering/change-data-capture.md) — why bad data propagates in CDC
- [Idempotent Pipelines](/data-engineering/idempotent-pipelines.md) — backfill correctness
- [CI/CD for Data Infrastructure](/data-engineering/cicd-for-data-infrastructure.md) — staged rollout with gates
- [Data Quality](/data-engineering/data-quality.md) — checksum/row-count verification
- [Data Engineering hub](/data-engineering/README.md)

---

[^src1]: [Migrating Data Ingestion Systems at Meta Scale](../../raw/web/migrating-data-ingestion-systems-at-meta-scale.md)
[^src2]: [TLDR Data — DuckDB Goes Remote / Netflix Tames Data Governance (newsletter)](../../raw/email/email-2026-05-14-duckdb-goes-remote-when-lakehouses-guess-netflix-tames-data.md)

---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/email/email-2026-05-16-change-data-capture-cdc-fundamentals-for-data-engineers.md
    channel: inbox
    ingested_at: 2026-06-11
aliases:
  - CDC
  - change data capture
tags:
  - corpus/data-engineering
  - concept
created: 2026-06-11
updated: 2026-06-11
---

# Change Data Capture (CDC)

**TL;DR.** CDC captures changes **as they happen** and streams them to downstream systems in near real time, without repeatedly querying the entire source database [^src1]. It is the most advanced of three approaches engineers use to move and sync data between systems — **full load**, **incremental loading**, and **CDC** — each with different trade-offs. Engineers usually escalate from simpler to more advanced approaches as systems grow and freshness requirements tighten [^src1]. The signals that you have outgrown incremental loading and should consider CDC are: **missing deletes, high latency, and difficult backfills** [^src1].

## The decision framework: three approaches

### Step 0 — Full load

Copy the entire table from source to destination on every run [^src1]. Full load is the right choice when [^src1]:

- The table is small (fewer than a few million rows) and quick to copy.
- Data changes rarely, or you have no way to detect what changed.
- You are doing a one-time historical migration.
- Freshness requirements are loose (once a day is fine).

> *"Full load is underrated. Many pipelines don't need anything fancier."* A 50,000-row table where the business only needs yesterday's data is fine on a nightly full load — don't over-engineer it [^src1].

Full load breaks down when the table has tens of millions of rows (copying hourly is slow and expensive), the business needs fresher data than the batch window allows, or **deletes need to be tracked accurately** [^src1].

### Step 1 — Incremental loading

Process only the rows changed since the last execution, most commonly via a timestamp column such as `updated_at` or `last_modified` [^src1]. Incremental loading breaks down in three ways [^src1]:

1. **You only see the latest state.** If a pipeline runs every 24h on a bank-account table and a customer makes five withdrawals during the day, the midnight run sees only the final balance — the four intermediate changes are invisible. The same problem hits **hard deletes**: if a row is physically deleted from the source, the incremental pipeline may never know it existed, leaving stale rows in the warehouse. A workaround is **soft deletes** (an `is_deleted` flag), but only if you control the source system [^src1].
2. **Latency.** Even well-designed incremental pipelines take time to run. If downstream needs updates within seconds, a 5-minute pipeline is already too slow [^src1].
3. **Backfills become large.** A pipeline running smoothly for two months that suddenly must reload history tries to process two months of data in one run — effectively a full load, creating major infrastructure pressure. Common fix: process in smaller time windows rather than all at once [^src1].

### Step 2 — CDC

CDC sidesteps the snapshot-comparison trap. Both full load and incremental loading try to detect changes **after the fact** by comparing snapshots, rather than **capturing the exact moment the change occurred** [^src1]. CDC captures changes as they happen and sends them downstream in near real time without repeatedly querying the full database [^src1].

## Motivating example

At an HVAC-services company, a PM needed to know **every time a technician was reassigned to a project, the moment it happened** — because some secure facilities required specially trained technicians, and the wrong assignment needed immediate remediation [^src1]. The SQL Server `assignments` table stored **only current state**: no history, no timestamps. An assignment change overwrote the row, with no record of the previous value or when it changed [^src1].

- **Full load on a schedule** could tell you *something* changed between two snapshots, but a daily run would surface a 9am reassignment only the next morning, and multiple reassignments between snapshots would collapse to the final state [^src1].
- **[[data-engineering/scd2|SCD Type 2]]** preserves history by inserting a new row on change and marking the old row inactive — better, but it still only captures changes **when the snapshot process runs**, so intermediate changes between snapshots are missed entirely [^src1].

Note on SCD types: **SCD Type 1** overwrites old values, keeping only the latest state; **SCD Type 2** preserves history by storing multiple versions of a row [^src1]. The use case needed Type 2 for historical tracking, but even Type 2 could not catch changes between snapshots — which is what pushed the author toward CDC [^src1].

## Capturing deletes

Deletes are a recurring weakness of the simpler approaches and a primary reason to adopt CDC [^src1]:

- **Full load** *can* track deletes (the row simply disappears from the next snapshot) but accurate delete tracking is one of the points where full load breaks down at scale [^src1].
- **Incremental loading** typically **misses hard deletes** entirely — a physically deleted source row may never be known to the pipeline, leaving it stranded in the warehouse. Soft deletes (`is_deleted`) only work when you control the source [^src1].
- **CDC** captures change events including deletes natively, since it observes the database's change stream rather than diffing snapshots [^src1].

## When to use CDC

The source frames CDC adoption as an escalation, not a default. Reach for CDC when you hit the incremental-loading wall — **missing deletes, high latency, or difficult backfills** [^src1]. Conversely, do not over-engineer: small, slow-changing tables with loose freshness needs are well served by full load [^src1].

The source also notes (without full elaboration in the captured excerpt) that the database in the example **already supported native CDC**, and that **database triggers** could have solved the problem too — two implementation paths that differ in mechanism [^src1]. It further distinguishes **CDC from database replication** as separate concerns [^src1].

> [unsourced — captured excerpt ends before the detailed CDC methods] The source promised coverage of three main CDC methods (with PostgreSQL examples), CDC vs database replication, and beginner caveats, but the body was truncated at "What Is Change Data Capture?" — those specifics are not available in the ingested text.

## Related

- [[data-engineering/scd2|SCD Type 2]] — history-tracking dimension pattern; complements but does not replace CDC.
- [[data-engineering/medallion-architecture|Medallion architecture]] — CDC streams are a canonical bronze-layer source.
- [[data-engineering/idempotent-pipelines|Idempotent pipelines]] — relevant when replaying or backfilling change streams.

[^src1]: [Change Data Capture (CDC) Fundamentals for Data Engineers](../../raw/email/email-2026-05-16-change-data-capture-cdc-fundamentals-for-data-engineers.md)

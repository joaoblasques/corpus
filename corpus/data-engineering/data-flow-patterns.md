---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/web/data-pipeline-design-patterns-1-data-flow-patterns-start-dat.md
    channel: web
    ingested_at: 2026-06-19
aliases:
  - data flow patterns
  - data pipeline design patterns
  - data flow design patterns
  - extraction patterns
  - source and sink
  - replayability
  - self-healing pipeline
tags:
  - corpus/data-engineering
  - concept
created: 2026-06-19
updated: 2026-06-19
---

# Data Flow Patterns

**TL;DR.** Data pipelines turn flakey when built without solid design foundations. Before choosing a pattern, characterize your **source** (replayable? ordered?) and **sink** (overwritable?); then combine three independent pattern axes — **extraction** (*how* you pull: time-ranged / full-snapshot / lookback / streaming), **behavioral** (*how* it reacts to failure: idempotent / self-healing), and **structural** (*how* tasks are arranged: multi-hop / conditional / disconnected) [^src1]. The recurring advice: pick the **simplest** pattern that meets the requirement; design patterns are overhead that only pays off once you have more than a few pipelines [^src1].

## Source & sink properties

Understand inputs/outputs *before* designing the pipeline [^src1].

- **Source replayability** — can the source answer *"what did the data look like n periods ago?"* A replayable source (event stream, web-server logs, a CDC/WAL dump) is critical for backfills; a non-replayable source (mutable application tables, current-state APIs) only shows the present [^src1]. You can manufacture replayability by dumping incoming data into a raw/loading area, which then acts as the replayable source — though if you dump only periodically, the *degree* of replayability drops to that period [^src1].
- **Source ordering** — the order in which records arrive. Some pipelines require it (a log-out must follow a log-in; attributing a checkout to a click). Handle out-of-order events with **exponential backoff, watermarking, or late-event handling** [^src1].
- **Sink overwritability** — can you update specific existing rows? Overwritable: DB tables with a unique key, cloud storage namespaced by a unique run id (`s3://bkt/yyyy-mm-dd/...`). Non-overwritable: a Kafka queue without log compaction, "create-only" sinks, tables without a unique key [^src1]. Overwritability is what prevents duplicates/partial records when a run fails [^src1].

> The two combine into the foundational rule of the page: **idempotency requires a replayable source *and* an overwritable sink** [^src1]. See [[data-engineering/idempotent-pipelines|Idempotent Pipelines]].

## Extraction patterns (how you pull)

| Pattern | What it pulls | Best for | Key cons |
|---|---|---|---|
| **Time-ranged** | only the data for a specific window (yesterday's data at 12:01 AM) | fast pulls; parallelizable backfills | incremental loads are hard (UPSERT/MERGE); non-replayable sources give different results on rerun [^src1] |
| **Full snapshot** | the entire dataset each run (add a `run_id`/folder for history) | simple; dimensional data; easy to see historical changes | slow; storage cost explodes; schema changes break old snapshots (table formats help); unfit for fact data [^src1] |
| **Lookback** | an aggregate over the past *n* periods (MAU, trailing-30-day KPI) | large source where only the current trailing metric matters; runs on fact tables | late-arriving events make metrics swing between runs [^src1] |
| **Streaming** | each record flows through, enriched/filtered as it goes (CC-fraud, stock monitoring) | lowest latency; essential for real-time | must be built for replayability; back-pressure, checkpointing, rate limits, no-downtime deploys all need thought [^src1] |

For time-ranged pulls into an [[data-engineering/scd2|SCD2]] table, **pause further pulls before rerunning a failed one** to avoid corrupting the table [^src1]. For full snapshots from a production table, **pull from a replica** [^src1].

## Behavioral patterns (how it handles failure)

- **Idempotent** — same inputs always produce the same output: reruns/backfills create no duplicates or schema changes. Requires a **replayable source and overwritable sink**. Pros: easy reruns/backfills, clean lineage, replayable debugging. Cons: longer dev time; hard to maintain idempotency when requirements change or a non-replayable enrichment source (an OLTP table) sneaks in [^src1]. This is the corpus's [[data-engineering/idempotent-pipelines|Idempotent Pipelines]] concept, here framed as one *behavioral* choice among others.
- **Self-healing** — instead of guaranteeing idempotency, the **next run catches up** the unprocessed/failed data. For time-ranged pipelines this can be as simple as auto-running the failed run(s) before the current one; full-snapshot and lookback pipelines can just skip the failed run [^src1]. Pros: simpler to build/maintain, less alert fatigue, ideal when upstream sources break intermittently. Cons: code bugs hide for several runs (everyone assumes it self-heals), you need de-dup logic for catch-up runs, run times become inconsistent, and you may lose historical change data without a replayable source [^src1].

The pragmatic stance: idempotency is the gold standard but can be impractical with changing requirements and non-replayable sources; self-healing is the simpler fallback (and a catch-up run can itself be made idempotent, giving the best of both) [^src1].

## Structural patterns (how tasks are arranged)

- **Multi-hop** — keep data at separate levels of "cleanliness" with DQ checks between layers (the [[data-engineering/medallion-architecture|medallion]] idea). Pros: rerun only failed transforms + dependents; intermediate tables pinpoint where a bug entered. Cons: storage + processing cost of copies; custom patterns have a steep learning curve — use well-established ones [^src1].
- **Conditional / dynamic** — flows that branch on run time or input. Pros: handles complex requirements in one pipeline/repo. Cons: hard to debug, slow to develop, hard to test (must simulate every input scenario). Pipelines grow into this; watch for exploding complexity [^src1].
- **Disconnected** — pipelines that depend on *other* pipelines' sinks without explicit cross-pipeline dependency (no task sensor). Pros: quick to build; teams work independently. Cons: convoluted lineage/SLA definition, hard to improve end-to-end latency, high cross-team communication overhead [^src1].

## How to choose

Patterns compose — a pipeline can be **self-healing (behavioral) + full-snapshot (extraction) + multi-hop (structural)** at once [^src1]. Walk the decision the article frames as a flow chart, and **default to the simplest design that satisfies the requirement**; consistency across your pipelines is itself a benefit (devs communicate and understand code more easily) [^src1].

## See also

- [[data-engineering/idempotent-pipelines|Idempotent Pipelines]] — the behavioral idempotent pattern in depth; replayable-source + overwritable-sink prerequisite
- [[data-engineering/data-ingestion-patterns|Data Ingestion Patterns]] — the stream-vs-batch entry choice that precedes these patterns
- [[data-engineering/incremental-pipeline-design|Incremental Pipeline Design]] — concrete extract/load/backfill mechanics for time-ranged pulls
- [[data-engineering/pipeline-coding-patterns|Pipeline Coding Patterns]] — the *coding* (vs data-flow) patterns; part 2 of the same series
- [[data-engineering/medallion-architecture|Medallion Architecture]] — the canonical multi-hop structure
- [[data-engineering/change-data-capture|Change Data Capture]] — a replayable streaming source
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [Data Pipeline Design Patterns - #1 Data Flow Patterns](../../raw/web/data-pipeline-design-patterns-1-data-flow-patterns-start-dat.md)

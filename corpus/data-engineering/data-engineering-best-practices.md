---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/email/email-2025-09-10-data-engineering-best-practices.md
    channel: email
    ingested_at: 2026-06-15
  - path: raw/web/data-engineering-best-practices-1-data-flow-code-start-data.md
    channel: web
    ingested_at: 2026-06-15
  - path: raw/web/github-josephmachado-data-engineering-best-practices-sample.md
    channel: web
    ingested_at: 2026-06-15
  - path: raw/web/web-data-engineering-system-design-9-data-serving-problems.md
    channel: web
    ingested_at: 2026-06-17
  - path: raw/email/email-2025-07-26-de-101-4-de-best-practices.md
    channel: email
    ingested_at: 2026-06-19
  - path: raw/email/email-2025-04-25-the-2025-ai-enabled-data-engineering-roadmap.md
    channel: email
    ingested_at: 2026-06-19
  - path: raw/email/email-2026-06-16-9-software-engineering-skills-a-de-should-have-and-how-to-le.md
    channel: email
    ingested_at: 2026-06-20
  - path: raw/email/email-2026-06-13-in-2026-the-data-fundamentals-matter-more-than-ever.md
    channel: email
    ingested_at: 2026-06-20
  - path: raw/web/6-data-engineering-skills-to-progress-in-the-age-of-ai-start.md
    channel: web
    ingested_at: 2026-06-26
aliases:
  - data engineering best practices
  - pipeline best practices
  - resilient data pipelines
  - data pipeline design
tags:
  - corpus/data-engineering
  - concept
created: 2026-06-15
updated: 2026-06-26
last_confirmed: 2026-06-26
---

# Data Engineering Best Practices

**TL;DR.** Six industry-standard practices that separate resilient, maintainable pipelines from fragile ones [^src1]. There is no perfect design, but following these concepts lets you ramp on any codebase fast and build pipelines on par with tech-forward companies [^src1]. The guiding meta-rule: *analyze your requirements, fix high-priority gaps first* — don't implement best practices for their own sake [^src1].

## The six practices

### 1. Use standard patterns that progressively transform data

Follow a **3-hop (layered) architecture** so common issues are already handled and references abound [^src1]:

- **Raw layer** — upstream data as-is (maybe type/column-name standardisation).
- **Transformed layer** — modeled per a principle (Kimball [[data-engineering/dimensional-modeling|dimensional modeling]], Data Vault, ER).
- **Consumption layer** — joined/aggregated datasets mapping to end-user use cases; **a metric is defined in exactly one place**.
- **Interface layer [optional]** — a view that presents warehouse tables in an easy-to-consume form.

Most tools ship their own 3-hop variant: Spark's [[data-engineering/medallion-architecture|Medallion (bronze/silver/gold)]], dbt's project structure (staging/warehouse/marts — see [[data-engineering/pipeline-layers|Pipeline Layers]]) [^src1]. Inputs to a step are *upstream*; consumers are *downstream*. At scale, different teams own different layers [^src1].

### 2. Validate data before exposing it (data-quality checks)

Define expectations for each dataset and check them *before* downstream consumers can use the data — bad data is disastrous and expensive to unwind (re-running every affected process) [^src1]. The reference project uses **Great Expectations**, storing expectations as JSON separate from code for cleaner code [^src1]. Caveat: *don't overdo it* — too many tests raise run time, cost (full-table scans), and redundancy; a common approach checks only **source data and final consumption data**, skipping intermediates [^src1]. See [[data-engineering/data-quality|Data Quality]].

### 3. Avoid duplicates with idempotent pipelines

Backfilling (re-running pipelines) is common; re-runs must not duplicate rows. The property of same-input → same-output is **idempotence** [^src1]. Two techniques [^src1]:
- **Run-id-based overwrites** — for append-only output; partition by a `run_id` (time range) and overwrite that partition on reprocess (requires tracking run-ids, e.g. Airflow backfill).
- **Natural-key UPSERTS** — for inserts+updates on a natural key (e.g. SCD2); re-runs update existing rows instead of inserting new ones.

See [[data-engineering/idempotent-pipelines|Idempotent Pipelines]] and [[data-engineering/scd2|SCD2]].

### 4. Write DRY code; keep I/O separate from transformation

Follow DRY on two axes: **code** (shared logic in one utility/base-class method) and **patterns** (a blueprint like a `StandardETL` base class inherited by pipelines) [^src1]. **Separate I/O (read/write) from transformation logic** — this enables easier testing, simpler debugging, and follows functional-design principles [^src1].

### 5. Track the when/how/what of runs (metadata) for debugging

For each step, track inputs/outputs, start/end times, and retries (which passed/failed) — orchestrators store most of this [^src1]. Critically, keep **dataset metadata in version control**: unique keys, physical storage location, table name, storage type (Delta/Iceberg), partition keys, and schema [^src1].

### 6. Use tests to check behavior, not break existing logic

Three test types for pipelines [^src1]:
- **Unit** — a single function (e.g. `test_get_bronze_datasets`).
- **Integration** — two+ systems working together (e.g. transformation + I/O).
- **End-to-end** — whole system; hard to set up for complex systems and often overkill.

The reference uses **pytest**, sharing one Spark session across test cases (created/torn-down via `conftest.py`) since session creation is slow [^src1]. As with DQ checks, don't overdo tests — it slows development velocity [^src1].

## Practical framing

Most companies (big and small) implement only *some* of these, by prioritization or lack of need [^src1]. The discipline is to **identify high-priority gaps and address them before** spending effort "implementing best practices to have best practices" [^src1]. The reference implementation is a runnable Spark/Postgres project (`josephmachado/data_engineering_best_practices`) using AdventureWorks data, Great Expectations, a `DeltaDataSet` metadata dataclass, and a `StandardETL` base class [^src3].

## The one-wide-table anti-pattern in the serving layer

A classic serving-layer failure: building one beautifully pre-joined wide table and letting every consumer — dashboards, data science, internal apps, downstream pipelines — query it [^src4]. "It felt clean at first. Then it wasn't." [^src4]

The fundamental lesson: **you will never have a single-serving approach that satisfies every use case** [^src4]. Different consumers need different serving designs:

- Dashboard → pre-aggregated data (full-table scan for every filter is slow)
- Data scientists → lower grain than the pre-aggregated layer
- Internal apps → sub-second lookups by primary key (columnar layout with large data scans without indexing is wrong)
- Refresh frequencies diverge: data scientists accept daily; dashboards may need hourly

The nine serving questions (full detail paywalled) are: (1) how data will be stored and served, (2) acceptable staleness, (3) what is the "raw" grain level, (4) usage pattern, (5) concurrent reader count, (6) handling of stale/incorrect data, (7) safe-write guarantees, (8) access/authorization levels, (9) AI model consumption [^src4].

> Note: the majority of this article is behind a paywall; only the intro mental-model section is captured above.

## The AI-era best-practices checklist (corroboration)

Zach Wilson's 2025 roadmap frames the *same* practices as the durable, "low-disruption-risk" core to know now that AI writes much of the SQL — grouped for prompting an AI coding tool [^src5]:

- **Data modeling** — proper table/column naming; clear separation of dimension, fact, and aggregation tables [^src5]. (See [[data-engineering/dimensional-modeling|Dimensional Modeling]].)
- **Partitioning** — "almost every dataset in your data lake should be partitioned"; minimize/anonymize PII [^src5].
- **Data-lake storage** — maximize **run-length-encoding** compression, store as **Parquet**, set sensible retention, avoid duplicating datasets that already exist [^src5]. (See [[data-engineering/parquet|Parquet]].)
- **DAG idempotency** — a task runs the same whether backfilled or in production and regardless of how many times it's run; solved with partition sensors / cumulative-DAG awareness and using `MERGE`/`INSERT OVERWRITE` rather than `INSERT INTO` [^src5]. (See [[data-engineering/idempotent-pipelines|Idempotent Pipelines]] and [[data-engineering/merge-into|MERGE INTO]].)
- **Serving / dashboarding** — serve from a low-latency store (Druid/Snowflake), pre-aggregate before loading, and don't put non-aggregated data into low-latency stores [^src5].

This independently confirms the idempotency, partitioning, and storage-layering practices above; the role-level framing is in [[data-engineering/ai-impact-on-data-engineering|AI's Impact on Data Engineering]] [^src5].

## Software engineering skills every data engineer should have

Alejandro Aboy's survey of 9 SE skills for DEs (2026) identifies the ones that differentiate "a senior DE from a junior DE that knows a lot of tools" [^src6]:

1. **Pick one lane and go deep.** Specialization (Spark, streaming, dbt, cloud) is more valuable than breadth across all tools. Depth signals expertise to employers and clients [^src6].
2. **Write understandable code.** "Code is read more than it's written." Clear variable names, short functions, self-documenting logic — code that a colleague can debug at 3am during an incident [^src6].
3. **Know at least one design pattern.** Repository pattern, Factory, Observer — patterns make code reusable and testable. A data pipeline with a clear design pattern is far easier to extend [^src6].
4. **Participate in code review.** Both sides: submit PRs and review others' code. The review habit builds taste and surfaces implicit best practices that never appear in tutorials [^src6].
5. **Contribute to open-source.** "The best portfolio a DE can have." OSS contributions signal initiative, collaboration, and real-world software craftsmanship that side projects alone don't demonstrate [^src6].

> "The difference between a senior DE and a junior DE that knows a lot of tools is often just these software engineering fundamentals" [^src6].

## Data fundamentals still matter in 2026

Counter-intuitive given the AI hype: *schema-on-read was tried and failed*. Around 2010, "data lakes" promised you could dump raw files and impose structure later — in practice, "people ended up with data swamps" because governance and quality were deferred, not solved [^src7].

What survived [^src7]:
- **Data centralization is still valuable** — organizations that keep data scattered across silos pay the cost in every analytics project. A centralized, governed data platform is not legacy; it's still the right foundation.
- **Glue skills matter** — the DE who connects data sources, handles schema drift, and makes downstream consumers succeed is still indispensable. "Glue skills" (building reliable pipelines between systems) are not automated away.
- **Data gets messier, not cleaner** — as more systems generate more data in more formats, the DE's job of cleaning, conforming, and governing has grown, not shrunk.
- **Build end-to-end** — understanding the full pipeline from source to serving, not just one layer (ingestion, or modeling, or visualization), is the differentiator. "AI tools will optimize each layer, but the engineer who understands how they connect still wins" [^src7].

## Corroboration: the same practices framed as AI-era durable skills

StartDataEngineering's "6 skills in the age of AI" independently reaches the same core: design patterns exist to keep pipelines maintainable, so the durable skill is knowing *when to apply a best practice and when to break it* [^src8]. Its six concepts map onto this page — the **3-stage progressive transform** (source → type conversions → Kimball model → summary tables) restates practice #1's layered architecture; **validating data before exposing it** + an orchestrator (Airflow) restates practice #2; and it points to four companion best-practice resources (Data Flow patterns, Code patterns, Implementation best practices, Metadata & Logging best practices) covering practices #1, #4, and #5 [^src8]. The role-level "fundamentals endure as codegen commoditises" framing is in [[data-engineering/ai-impact-on-data-engineering|AI's Impact on Data Engineering]] [^src8].

## Related

- [[data-engineering/idempotent-pipelines|Idempotent Pipelines]] · [[data-engineering/data-quality|Data Quality]]
- [[data-engineering/pipeline-layers|Pipeline Layers]] · [[data-engineering/medallion-architecture|Medallion Architecture]]
- [[data-engineering/de-portfolio-projects|DE Portfolio Projects]] — runnable projects applying these
- [[data-engineering/data-engineer-role|The Data Engineer Role]] — fundamentals over tools
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [Data Engineering Best Practices (1: Data flow & code)](../../raw/web/data-engineering-best-practices-1-data-flow-code-start-data.md)
[^src2]: [Data Engineering Best Practices! (newsletter)](../../raw/email/email-2025-09-10-data-engineering-best-practices.md)
[^src3]: [josephmachado/data_engineering_best_practices (sample)](../../raw/web/github-josephmachado-data-engineering-best-practices-sample.md)
[^src4]: [Data Engineering System Design: 9 Data Serving Problems (Vu Trinh)](../../raw/web/web-data-engineering-system-design-9-data-serving-problems.md)
[^src5]: [The 2025 AI-enabled Data Engineering roadmap (Zach Wilson, DataEngineer.io)](../../raw/email/email-2025-04-25-the-2025-ai-enabled-data-engineering-roadmap.md)
[^src6]: [9 Software Engineering Skills a DE Should Have (Alejandro Aboy)](../../raw/email/email-2026-06-16-9-software-engineering-skills-a-de-should-have-and-how-to-le.md)
[^src7]: [In 2026, The Data Fundamentals Matter More Than Ever (Pipeline to Insights)](../../raw/email/email-2026-06-13-in-2026-the-data-fundamentals-matter-more-than-ever.md)
[^src8]: [6 Data Engineering Skills To Progress in the Age of AI (Joseph Machado, StartDataEngineering)](../../raw/web/6-data-engineering-skills-to-progress-in-the-age-of-ai-start.md)

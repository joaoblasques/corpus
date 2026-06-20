---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/email/email-2025-09-17-how-to-avoid-messy-data-in-your-warehouse.md
    channel: inbox
    ingested_at: 2026-06-11
  - path: raw/web/6-steps-to-avoid-messy-data-in-your-warehouse-start-data-eng.md
    channel: web
    ingested_at: 2026-06-11
  - path: raw/web/dlthub-ai-workbench-data-quality-toolkit-schema-aware-checks.md
    channel: web
    ingested_at: 2026-06-11
  - path: raw/web/web-the-data-engineering-mindset-every-ai-builder-needs.md
    channel: web
    ingested_at: 2026-06-17
  - path: raw/email/email-2025-08-01-de-101-6-testing-and-data-quality.md
    channel: email
    ingested_at: 2026-06-19
  - path: raw/email/email-2025-04-16-understanding-the-t-in-etl-a-back-to-basics-guide-to-data-tr.md
    channel: email
    ingested_at: 2026-06-19
  - path: raw/web/web-sql-to-dbt-guide-hands-on-data-quality-integrity-worfklows.md
    channel: web
    ingested_at: 2026-06-20
aliases:
  - data quality
  - messy data
  - data contracts
  - data validation
  - DAMA-DMBOK
  - five pillars of trusted data
tags:
  - corpus/data-engineering
  - concept
created: 2026-06-11
updated: 2026-06-19
---

# Data Quality

**TL;DR.** Garbage in, garbage out: *"No matter how good your data model and pipelines are, if your input data is wrong, the data in your warehouse will be unusable."* [^src2] Data quality is enforced by (1) a structured framework for building a clean warehouse, (2) **data contracts** — formalized, validated expectations on input data agreed with upstream teams [^src2], and (3) **schema-aware validation** that bootstraps checks from what the loader already knows, then escalates from schema rules to business meaning [^src3]. Most data-quality failures are *"a symptom of an incorrect assumption or a small mistake"* — a wrong write disposition, a null in a key, a drifted enum value [^src3].

## The 6-step clean-warehouse framework

The StartDataEngineering framework lists six steps to build and maintain a warehouse that gives stakeholders what they need while avoiding messy data; following them in order is ideal but real projects reorder by situation [^src2]. Notably, several steps are **non-technical** — nailing them earns the team more time/money, which avoids the shortcuts that cause messy data [^src2].

1. **Understand the business.** Know how the company makes money before designing anything. This informs the data model, the metrics that matter, and which tables to prioritize. The outcome is a **conceptual data model (CDM)** of how business entities interact [^src2].
2. **Make data easy to use with the appropriate data model.** A bad model is painful to use and leads to messy data. The source teaches [[data-engineering/dimensional-modeling|Kimball dimensional modeling]] — `dim_noun` dimension tables, `fct_verb` fact tables at the lowest grain, bridge tables for many-to-many, and **data marts with OBTs (One Big Table)** so metric calculations stay in one place and are consistent across teams [^src2]. The flow uses bronze/silver/gold layers to transform data progressively (see [[data-engineering/medallion-architecture|medallion architecture]]) [^src2].
3. **Good input data is necessary for a good warehouse** (the data-contracts step — see below) [^src2].
4. **Define a Source of Truth (SOT) and trace its usage.** "The numbers look different" is a top data-team problem. Define the **SOT metric** in the data-mart layer (one place, used by all stakeholders), make the **SOT data** the mart layer, and track **SOT data lineage** — which teams consume the mart — so metric mismatches are resolvable (e.g. dbt lineage) [^src2].
5. **Keep stakeholders in the loop.** Establish need/pain before building, drive awareness (emails, demos), set expectations with a 20-40% time buffer and iterative delivery, and evangelize with before/after query speeds [^src2].
6. **Watch for org-level red flags.** No leadership buy-in, constant reorgs, no data team, misaligned teams with competing objectives — persistent versions are signals to change jobs [^src2].

> *"Data utopia does not exist... we, as data engineers, have the ability & responsibility to clean up the mess."* [^src2]

## Data contracts and the five input-data verticals

Validate input data against expectations **before** using it in pipelines; these formalized checks agreed with upstream are **data contracts** [^src2]. Define expectations across five verticals [^src2]:

- **Data Freshness** — is the data as recent as expected?
- **Data Types** — did a type change, or were columns added/modified without notifying the data team?
- **Data Constraints** — uniqueness, non-null, relationships, enum sets respected?
- **Data Size Variance** — is row volume consistent across loads/periods?
- **Data Metric Variance** — are critical metrics consistent across loads/periods?

When checks fail, work with upstream teams to fix the source. The discipline is non-negotiable: *"Never use bad data to build your data models, no matter the pushback from upstream teams, since you will be responsible for bad data!"* [^src2]

## Schema-aware validation (dlt AI Workbench)

The dltHub data-quality toolkit operationalizes the contract idea by **bootstrapping checks from the loader's existing schema** [^src3]. The failure mode it targets: an agent writes the pipeline (endpoints, pagination, incremental loading, schema normalization), but assumptions slip silently — *"nulls in primary keys, duplicates from the wrong write disposition, drifted enum values"* [^src3]. Application-side business logic isn't shipped downstream with the data, so engineers code against assumptions that may be wrong or that drift over time [^src3].

### Schema is the floor, business meaning is the ceiling

dlt's schema already tracks which columns are primary keys, non-nullable, or unique — the loader actually uses these. The toolkit reads them and **proposes checks before asking anything**, e.g. `is_unique("id")` because `id` is marked primary key, `is_not_null("customer_id")` because it's non-nullable [^src3]. *"The schema is the floor, not the ceiling."* The ceiling is the business rules never written down — status must be one of three values, `amount` after discount must be non-negative, an email must look like an email — stated in plain language and mapped to primitives [^src3].

Four primitives cover most cases — `is_unique`, `is_not_null`, `is_in`, `case` — plus column-level metrics (`null_rate`, `mean`, `row_count`) that record values over time so you can **spot drift** [^src3].

### Sampling before a rule ships

A distinctive step: the toolkit **samples the column before shipping a rule**. If you say `status` should be `active`/`inactive`, it samples and may report it also found `pending` and `cancelled`, asking whether to include them [^src3]. Every check is confirmed with the user before any code is written — explicit, visible, approved — guarding against typos or values you didn't know existed [^src3].

### What lands in the pipeline

Checks are written as **decorators** on dlt resources, running as part of `pipeline.run()` (per-load mode), with `dq.enable_data_quality(pipeline)` flipping the flag; results land in `_dlt_checks` and `_dlt_dq_metrics` tables in the destination, queryable/dashboardable/alertable [^src3]. For already-loaded data, a standalone audit uses `dq.run_checks(...)` [^src3].

### Detection + diagnosis + routing, not just a lab result

*"Most DQ tools are the lab result... This one is the medical system: detection, diagnosis, and fix in the same doctor visit."* [^src3] When a check fails, the toolkit routes the failure to the toolkit that owns the surface area [^src3]:

| Failure pattern | Routed to |
|---|---|
| Ingestion wrong (write disposition, schema) | rest-api-pipeline |
| Modeling wrong (joins, canonical fields) | transformations |
| Anomaly worth a look | data-exploration |
| Everything passes | dlthub-platform (schedule) |

Two real catches [^src3]:
- `is_not_null` on `customer_id` in orders — null 50% of the time; the pipeline loaded it because *"nothing told it not to."* The canonical model expected `customer_id` to join orders to customers; **half the joins would have been silently wrong**. Caught before the model was queried.
- `is_unique` on a meant-to-be primary key — duplicates everywhere because the **write disposition was `append` instead of `merge`**, re-inserting the same rows every load. The check flagged a column; the fix lived in ingestion code.

The author contrasts this with Great Expectations, where the same `customer_id` null would surface as an alert that then requires a human to chase down whether it's a source, ingestion, or modeling problem and file a ticket — *"agentic context replaces the human tribal knowledge and bottlenecks"* [^src3].

## DAMA-DMBOK quality dimensions for AI systems

For AI builders specifically, five DAMA-DMBOK dimensions matter most [^src4]:

| Dimension | AI impact |
|---|---|
| **Validity** | Free-text where structured value expected silently corrupts model inputs (e.g., product category accepting "elec." or "consumer tech" instead of "Electronics") |
| **Completeness** | Missing values create silent bias — segments with systematically missing data cause the model to perform worse for those users |
| **Timeliness** | A recommendation model trained on 30-day-old data in fast-moving contexts is already outdated before first user |
| **Uniqueness** | Duplicate records inflate patterns in training data — a transaction appearing twice teaches the model it happened twice |
| **Consistency (Semantic Validity)** | A column `distance_traveled` that silently switches from km to miles doesn't fail loudly — it slowly corrupts the model's understanding of the world |

> *"Consistency violations are extremely hard to catch without proper monitoring and documentation."* [^src4]

## The five pillars of trusted data (dlthub)

A memorable framework mapping across the DAMA dimensions [^src4]:

1. **Structural Integrity** — data matches expected schema, data types, and required fields so pipelines don't break.
2. **Semantic Validity** — values follow real-world rules and logic (valid ranges, correct formats, meaningful statuses).
3. **Uniqueness and Relationships** — no duplicates, maintained key relationships, accurate historical records.
4. **Privacy and Governance** — sensitive information protected, masked, or removed; usage aligns with legal requirements.
5. **Operational Health** — data arriving reliably and on time. Even accurate data is low quality if it is late, incomplete, or if pipelines fail silently.

## Common AI-system DQ failures

Three canonical failure patterns from production [^src4]:

- **Breaking schema changes**: column renamed or type changed → model depending on it fails silently. Example: `user_id` renamed to `customer_id`; the pipeline keeps running but is joining on nothing.
- **Missed data SLAs**: hourly data stops arriving → recommendation model serves stale data for hours without anyone noticing.
- **Data duplication**: same transaction loaded via batch AND streamed via CDC into the same table → training set has every transaction twice; model thinks popular items are twice as popular.

## Three monitoring layers for AI/data systems

A practical framing for what to instrument [^src4]:

- **Input distribution monitoring** — statistical distribution of key features, input volume, null rates, format violations, schema changes; catches data drift (when incoming data diverges from training distribution).
- **Output monitoring** — distribution of prediction classes/values, rate of low-confidence predictions, user feedback signals.
- **Pipeline health monitoring** — job completion status, pipeline latency, data freshness, volume anomalies.

For an early-stage system, three signals alone provide huge value: **data freshness** (when was last successful load?), **volume checks** (records per hour), and **schema validation** (does incoming data match expected structure?) [^src4]. See [[data-engineering/data-observability|Data Observability]] for the full observability pattern catalog.

## Code tests vs data-quality checks (different things, different timing)

A distinction worth keeping explicit: **code tests** and **data-quality checks** are not the same and run at different moments [^src5]. Code tests verify the *transformation logic is correct* and run **before code is deployed to production** (i.e. in CI, once per change — see [[data-engineering/cicd-for-data-infrastructure|CI/CD for Data Infrastructure]]); data-quality checks verify the *data is correct* and run **every time the pipeline runs** (per-load, on live data) [^src5]. Both matter because *"ensuring your data is correct before stakeholders can access it is critical — imagine your pipeline accidentally adding (or removing) a 0 to a revenue metric"* [^src5]. The five-vertical data contracts above are the per-run checks; pytest-style unit tests on the pipeline code are the pre-deploy checks. (Practically, the pre-deploy gate is implemented with **pytest** — see [[data-engineering/pipeline-coding-patterns|Pipeline Coding Patterns]] for the testing techniques.)

## Why the transform layer is a DQ surface

The transform step is itself a quality risk: "Each transform and SQL script is another opportunity to introduce errors," so **unit tests and data-quality checks "aren't just nice to have, they're essential for catching issues before they hit production"** [^src6]. This compounds with an **ownership** problem — transform tooling like [[data-engineering/dbt|dbt]] has broadened who can build platform layers (engineers, analytics engineers, analysts), which is great for speed but blurs the line of responsibility: where does ownership of the core warehouse end and use-case-specific layers begin? Without clear boundaries, things get messy fast [^src6]. See [[data-engineering/data-transformation|Data Transformation]] for the transform-layer challenges this DQ discipline guards against.

## dbt's three-layer testing strategy

The Alejandro Aboy "SQL to dbt" series provides a hands-on view of dbt's built-in quality gates, based on their synthetic marketing dataset [^src7]:

**Data integrity vs data quality (two distinct problems)** [^src7]:
- **Data integrity** — can you run your analysis without this data? Guards against system failures (missing joins, broken pipelines).
- **Data quality** — does wrong data lead to bad decisions? Guards against silent errors in business logic.
Start with integrity constraints to prevent failures, then add quality tests for business-critical calculations.

**Three testing layers** [^src7]:

| Layer | Tool | When it runs | What it catches |
|---|---|---|---|
| **Data contracts** | `dbt_project.yml` + model constraints | Compilation (before models build) | Schema violations: wrong types, missing columns, `budget < 0` |
| **Generic tests** | `schema.yml` `tests:` blocks | After each `dbt run` | Reusable checks: `unique`, `not_null`, `accepted_values`, custom SQL |
| **Singular tests** | `tests/<model>_test.sql` | After each `dbt run` | Business logic: "revenue minus discount must be non-negative" |

Data contracts are **proactive** — they fail fast at compilation so bad data never enters the pipeline. Generic and singular tests are **reactive** — models build, but failures are reported for investigation.

**dbt-expectations** [^src7]: an extension package adding statistical anomaly detection (`expect_column_mean_to_be_between`, `expect_table_row_count_to_equal_other_table`, etc.). Catches drift that static rules miss — e.g. "the average budget dropped 80% vs last week" is not a null-check failure.

**Multi-layer defense principle** [^src7]: contracts catch schema problems before they propagate downstream; generic tests catch business-rule violations per-run; singular tests encode domain knowledge that no tool can auto-detect. The three layers are complementary and each has a different fix path:
- Contract failure → fix the schema or update the contract definition.
- Generic test failure → investigate upstream source (the source system likely introduced the issue).
- Singular test failure → review with a domain expert (this often means business rules or requirements have changed).

## Synthesis: contracts vs schema-aware checks

The two technical sources are complementary, not competing. StartDataEngineering defines data contracts as **expectations agreed with upstream teams across five verticals**, validated before use [^src2]; the dlt toolkit is a **mechanism** that derives a baseline of those checks automatically from the loader's schema (the "floor"), then layers business rules (the "ceiling") and routes failures to a fix [^src3]. Both insist quality is enforced **at ingestion, before downstream consumption** — the contract is the policy, the schema-aware toolkit is one implementation.

## Related

- [[data-engineering/dimensional-modeling|Dimensional modeling]] — the modeling step in the 6-step framework.
- [[data-engineering/medallion-architecture|Medallion architecture]] — quality rules are enforced at the silver layer.
- [[data-engineering/change-data-capture|Change data capture]] — write disposition (`append` vs `merge`) is a recurring quality pitfall in change-driven loads.
- [[data-engineering/dbt|dbt]] — lineage and SOT tracking referenced as the Source-of-Truth tooling.
- [[data-engineering/data-observability|Data Observability]] — the instrumentation layer that detects when quality goals are not met; observability patterns (flow interruption, skew, lag, SLA misses).

[^src1]: [How to Avoid Messy Data in Your Warehouse!](../../raw/email/email-2025-09-17-how-to-avoid-messy-data-in-your-warehouse.md)
[^src2]: [6 Steps to Avoid Messy Data in Your Warehouse](../../raw/web/6-steps-to-avoid-messy-data-in-your-warehouse-start-data-eng.md)
[^src3]: [AI Workbench: Data quality toolkit preview (dltHub)](../../raw/web/dlthub-ai-workbench-data-quality-toolkit-schema-aware-checks.md)
[^src4]: [The Data Engineering Mindset Every AI Builder Needs](../../raw/web/web-the-data-engineering-mindset-every-ai-builder-needs.md)
[^src5]: [[DE 101] #6 - Testing and Data Quality (Start Data Engineering)](../../raw/email/email-2025-08-01-de-101-6-testing-and-data-quality.md)
[^src6]: [Understanding the "T" in ETL: A Back-to-Basics Guide to Data Transformations](../../raw/email/email-2025-04-16-understanding-the-t-in-etl-a-back-to-basics-guide-to-data-tr.md)
[^src7]: [SQL to dbt Guide — Hands-on Data Quality & Integrity Workflows](../../raw/web/web-sql-to-dbt-guide-hands-on-data-quality-integrity-worfklows.md) — Alejandro Aboy, Pipeline to Insights

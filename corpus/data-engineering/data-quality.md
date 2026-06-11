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
aliases:
  - data quality
  - messy data
  - data contracts
  - data validation
tags:
  - corpus/data-engineering
  - concept
created: 2026-06-11
updated: 2026-06-11
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

## Synthesis: contracts vs schema-aware checks

The two technical sources are complementary, not competing. StartDataEngineering defines data contracts as **expectations agreed with upstream teams across five verticals**, validated before use [^src2]; the dlt toolkit is a **mechanism** that derives a baseline of those checks automatically from the loader's schema (the "floor"), then layers business rules (the "ceiling") and routes failures to a fix [^src3]. Both insist quality is enforced **at ingestion, before downstream consumption** — the contract is the policy, the schema-aware toolkit is one implementation.

## Related

- [[data-engineering/dimensional-modeling|Dimensional modeling]] — the modeling step in the 6-step framework.
- [[data-engineering/medallion-architecture|Medallion architecture]] — quality rules are enforced at the silver layer.
- [[data-engineering/change-data-capture|Change data capture]] — write disposition (`append` vs `merge`) is a recurring quality pitfall in change-driven loads.
- [[data-engineering/dbt|dbt]] — lineage and SOT tracking referenced as the Source-of-Truth tooling.

[^src1]: [How to Avoid Messy Data in Your Warehouse!](../../raw/email/email-2025-09-17-how-to-avoid-messy-data-in-your-warehouse.md)
[^src2]: [6 Steps to Avoid Messy Data in Your Warehouse](../../raw/web/6-steps-to-avoid-messy-data-in-your-warehouse-start-data-eng.md)
[^src3]: [AI Workbench: Data quality toolkit preview (dltHub)](../../raw/web/dlthub-ai-workbench-data-quality-toolkit-schema-aware-checks.md)

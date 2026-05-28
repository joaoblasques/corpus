---
type: entity
domain: data-engineering
status: draft
sources:
  - path: 03_Resources/Study Notes/dbt Data Architecture - Simple Stack Design.md
    channel: notes
    ingested_at: 2026-05-21
aliases:
  - dbt
  - data build tool
tags:
  - corpus/data-engineering
  - entity
created: 2026-05-21
updated: 2026-05-21
---

# dbt (data build tool)

**TL;DR**: A SQL-first transformation framework that compiles `.sql` model files into warehouse-optimized queries, enforces layer separation via materialization strategies, and treats data transformations as software (version control, testing, lineage) [^src1].

## Role in the data stack

dbt operates on the "T" of ELT — it transforms data **already in the warehouse**. It does not extract or load.

```
Sources → [Extract & Load] → Raw DB → [dbt transforms] → Analytics DB → Reporting
```

## Sources vs Models

| Concept | What it is | How to reference |
|---|---|---|
| **Source** | Pointer to raw, untransformed data in the Raw DB | `{{ source('schema', 'table') }}` |
| **Model** | Transformed output deployed by dbt (`.sql` file) | `{{ ref('model_name') }}` |

Never point a `source` at a table that has already been transformed — sources must reference raw data only [^src1].

## Layer architecture (The Simple Stack)

dbt projects mirror the database schema structure [^src1]:

| dbt directory | DB schema | Materialization | Purpose |
|---|---|---|---|
| `models/staging/` | `staging` | `view` | Clean and standardize raw data; 1:1 with source tables |
| `models/warehouse/` | `warehouse` | `table` | Joined, enriched, business-logic models |
| `models/marts/` | `marts` | `table` | Consumption-ready tables for BI tools and end users |

See [[data-engineering/pipeline-layers|Pipeline Layers]] for the architecture pattern this implements.

## `dbt_project.yml` configuration

Materializations and schema targets are set centrally [^src1]:

```yaml
models:
  my_project:
    staging:
      +materialized: view
      +schema: staging
    warehouse:
      +materialized: table
      +schema: warehouse
    marts:
      +materialized: table
      +schema: marts
```

## Database design

Two separate databases on the same server [^src1]:
- **Raw DB** — one schema per external source (e.g., `stripe`, `google_analytics`)
- **Analytics DB** — `staging`, `warehouse`, `marts` schemas

## See also

- [[data-engineering/pipeline-layers|Pipeline Layers]] — the staging → warehouse → marts architecture pattern
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [[03_Resources/Study Notes/dbt Data Architecture - Simple Stack Design|dbt Data Architecture - Simple Stack Design]]

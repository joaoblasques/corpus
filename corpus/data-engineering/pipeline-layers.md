---
type: concept
domain: data-engineering
status: draft
sources:
  - path: 03_Resources/Study Notes/dbt Data Architecture - Simple Stack Design.md
    channel: notes
    ingested_at: 2026-05-21
aliases:
  - pipeline layers
  - data pipeline layers
  - staging warehouse marts
  - ELT layers
  - simple stack
tags:
  - corpus/data-engineering
  - concept
created: 2026-05-21
updated: 2026-05-21
---

# Pipeline Layers (Staging → Warehouse → Marts)

**TL;DR**: The standard ELT separation pattern — raw ingested data moves through progressive transformation layers (staging, warehouse, marts) before reaching BI tools, with each layer having a distinct purpose and materialization strategy [^src1].

## The Simple Stack

```
External Sources → [Extract & Load] → Raw DB → Staging → Warehouse → Marts → Reporting
```

Two distinct databases on the same server [^src1]:

| Database | Schemas | Contents |
|---|---|---|
| **Raw DB** | One per source (e.g., `stripe`, `google_analytics`) | Untransformed, as-ingested data |
| **Analytics DB** | `staging`, `warehouse`, `marts` | Progressive transformations |

## Layer definitions

| Layer | Materialization | Purpose |
|---|---|---|
| **Staging** | View | Lightly clean and standardize raw data; 1:1 with source tables; no business logic |
| **Warehouse** | Table | Joins, enrichment, applied business logic; the integration layer |
| **Marts** | Table | Consumption-ready tables shaped for specific BI use cases or consumer teams |

Using **views** for staging keeps them cheap and always reflecting current raw data. **Tables** for warehouse and marts reflect the compute cost of joins and aggregations paid once at build time [^src1].

## Why separate Raw from Analytics

- Raw data is append-only and never modified after ingestion
- Raw database gives a stable, auditable foundation — transformations can always be re-run from raw
- Separation enforces the discipline that sources point to raw data only; models point to other models [^src1]

## Tools that implement this pattern

- [[data-engineering/dbt|dbt]] — the canonical tool for implementing this layered transformation model; project directory structure mirrors the schema structure

## See also

- [[data-engineering/dbt|dbt]] — tool that codifies this architecture
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [[03_Resources/Study Notes/dbt Data Architecture - Simple Stack Design|dbt Data Architecture - Simple Stack Design]]

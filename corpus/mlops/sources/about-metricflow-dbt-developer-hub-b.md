---
type: source
domain: mlops
status: draft
sources:
  - path: raw/web/web-about-metricflow-dbt-developer-hub.md
    channel: web
    ingested_at: 2026-07-21
aliases: []
tags:
  - corpus/mlops
  - source
  - doc-quick-intake
created: 2026-07-21
updated: 2026-08-16
provisional: false
url: https://docs.getdbt.com/docs/build/about-metricflow
origin: obsidian-list
---

# About MetricFlow | dbt Developer Hub

**TL;DR:** MetricFlow is a SQL query generation tool that powers dbt's Semantic Layer. It lets teams define metrics once in YAML and query them consistently across dimensions, eliminating duplicated per-analyst SQL.

---

## What MetricFlow Is

MetricFlow is "a SQL query generation tool designed to streamline metric creation across different data dimensions for diverse business needs."[^1] It handles SQL query construction and defines the specification for dbt semantic models and metrics, allowing metric definitions in dbt projects queryable via MetricFlow commands.

MetricFlow is developed and maintained by dbt Labs, distributed under the Apache 2.0 license, and compatible with dbt version 1.6 and higher.[^1]

Starting in dbt Core v1.12, semantic models can also be defined using OSI (Open Semantic Interchange) documents as an alternative to dbt's native YAML configuration.[^1]

---

## Core Abstractions

MetricFlow operates through YAML files, where a **semantic graph** links language to data. The graph has two node types:[^1]

- **Semantic models** — data entry points corresponding to dbt models. Each carries metadata (table name, primary keys) and three sub-components:
  - *Entities*: join keys used to traverse between models (the graph's edges).
  - *Dimensions*: slicing/grouping axes for metrics.
  - *Measures*: (implicit in metric definitions).

- **Metrics** — functions over semantic models that produce quantitative indicators. MetricFlow supports multiple metric types (additive, ratio, derived, cumulative — listed but not fully expanded in the source).

The semantic graph is a subset of the dbt DAG. Unlike the DAG (which encodes task dependencies), the semantic graph encodes *information relationships* between tables — what data is available for consumption.[^1]

When generating a metric, MetricFlow's SQL engine determines "the best path between tables using the framework defined in YAML files for semantic models and metrics."[^1]

---

## Design Principles

MetricFlow abides by four explicit principles:[^1]

1. **Flexibility with completeness** — define metric logic using flexible abstractions on any data model.
2. **DRY (Don't Repeat Yourself)** — minimize redundancy by enabling metric definitions whenever possible.
3. **Simplicity with gradual complexity** — approach using familiar data modeling concepts.
4. **Performance and efficiency** — optimize performance while supporting centralized data engineering and distributed logic ownership.

---

## Motivation: The Multi-Query Problem

Without MetricFlow, the same metric (e.g. `order_total`) gets re-implemented independently by multiple analysts:

```sql
select sum(order_total) as order_total from orders
```

Each analyst adds their own dimensional slices (by day, by order type, etc.), producing divergent SQL. MetricFlow replaces this with a single YAML metric definition that any consumer queries consistently via MetricFlow commands.[^1]

---

## Compatibility and Limitations

- Requires dbt 1.6+.[^1]
- Does not currently support dbt built-in functions or packages; "support is planned for the future."[^1]
- Works with the Open Semantic Interchange (OSI) format (dbt Core v1.12+).[^1]

---

[^1]: [raw/web/web-about-metricflow-dbt-developer-hub.md](../../../raw/web/web-about-metricflow-dbt-developer-hub.md) — About MetricFlow | dbt Developer Hub (collected 2026-07-18).

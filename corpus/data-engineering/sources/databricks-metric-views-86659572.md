---
type: source
domain: data-engineering
status: draft
tags:
  - corpus/data-engineering
  - semantic-layer
  - databricks
  - metrics
sources:
  - path: raw/web/web-databricks-metric-views-and-the-reality-of-the-semantic-laye-86659572.md
    channel: web
    title: Databricks Metric Views and the Reality of the Semantic Layer
aliases: []
confidence: 0.85
last_confirmed: 2026-08-12
created: 2026-08-12
updated: 2026-08-12
---

# Databricks Metric Views and the Semantic Layer

**TL;DR**: Databricks Metric Views are first-class Unity Catalog objects that define business metrics and dimensions in a YAML-over-SQL structure. They address the classic semantic layer problem — scattered business logic across pipelines, dashboards, and notebooks. As AI/LLM-driven analytics emerge, having machine-readable metric definitions matters more.

## The semantic layer problem

Business logic drifts into pipelines, dashboards, notebooks, and random scripts. No single place answers "how is this metric calculated?" Two reports for the same metric show different numbers; tribal knowledge is required to explain the discrepancy. Data teams spend time in repo archaeology rather than analysis.[^src]

"Despite decades of industry experience, we still struggle with this. Data teams continue to fight their way through repos, documentation, and tribal knowledge just to understand how a number is calculated."[^src]

## What Metric Views are

Metric Views are Unity Catalog objects that define dimensions and measures in a YAML-structured layer on top of SQL. They behave like views but with additional structure making business meaning explicit.[^src]

Syntax:

```sql
CREATE OR REPLACE VIEW confessions.default.trips_metrics
  (ride_date COMMENT 'Date of trip (from started_at)',
   total_rides COMMENT 'Total rides',
   member_rides COMMENT 'Rides where member_casual = member',
   ...)
  WITH METRICS
  LANGUAGE YAML
  COMMENT 'Metric View for trips: rides by day/month, membership split, ...'
AS $$
version: 0.1
source: confessions.default.trips
filter: TO_TIMESTAMP(started_at) IS NOT NULL
dimensions:
  - name: ride_date
    expr: TO_DATE(TO_TIMESTAMP(started_at))
  - name: member_type
    expr: member_casual
measures:
  - name: total_rides
    expr: COUNT(1)
  - name: member_rides
    expr: COUNT(1) FILTER (WHERE member_casual = 'member')
  - name: avg_trip_minutes
    expr: |
      AVG(
        (UNIX_TIMESTAMP(TO_TIMESTAMP(ended_at)) - UNIX_TIMESTAMP(TO_TIMESTAMP(started_at))) / 60.0
      )
$$;
```[^src]

## Key properties

- **Unity Catalog integration**: inherit permissions, lineage tracking, governance automatically
- **Reusable across tools**: queryable from SQL, dashboards, and AI-driven interfaces
- **Semantic metadata**: display names and synonyms make metrics interpretable by both humans and LLMs
- **Materialization option**: can be computed on demand or materialized (same freshness vs performance tradeoff as regular views)[^src]

## Relevance to AI-driven analytics

"As more systems rely on LLMs and agents to query and interpret data, having well-defined, consistent metrics becomes even more important. Databricks is clearly thinking ahead here, incorporating semantic metadata such as display names and synonyms to help both humans and machines understand the meaning of the data."[^src]

Metric Views are positioned as the interface layer for agentic analytics — agents querying semantic objects rather than raw tables.

## The mindset requirement

"The semantic layer is as much a mindset as it is a technology. It requires teams to be disciplined about how they define and manage metrics, and to treat business logic as a first-class concern rather than an afterthought."[^src]

"The real question isn't whether you should use a semantic layer; it's how you plan to manage your metrics if you don't."[^src]

## Cross-links

- [/data-engineering/semantic-layer.md](/data-engineering/semantic-layer.md) — parent concept page
- [/data-engineering/databricks.md](/data-engineering/databricks.md) — Databricks entity page; Unity Catalog context
- [/data-engineering/lakefs.md](/data-engineering/lakefs.md) — lakefs.io article critiques Unity Catalog's lock-in properties

---

[^src]: raw/web/web-databricks-metric-views-and-the-reality-of-the-semantic-laye-86659572.md

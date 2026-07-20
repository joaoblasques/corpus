---
type: source
domain: data-engineering
status: stub
sources:
  - path: raw/notes/notes-03-resources-articles-scd2-joining-fact-dimension-tables.md
    channel: notes
    ingested_at: 2026-07-20
aliases: []
tags:
  - corpus/data-engineering
  - source
  - doc-quick-intake
created: 2026-07-20
updated: 2026-07-20
provisional: false
url: 
origin: obsidian
---

# Joining Fact Tables and SCD2 Dimension Tables

> **Quick intake** (obsidian). raw stub: `notes-03-resources-articles-scd2-joining-fact-dimension-tables.md`

This article explains Slowly Changing Dimension Type 2 (SCD2) tables and demonstrates how to join fact tables to them in a data warehouse context. It highlights the importance of temporal joins using BETWEEN the dimension's effective and expiration datetimes. The correct SQL pattern for joining fact tables to SCD2 tables is provided.

**Key topics**
- Fact tables
- Dimension tables
- SCD2 pattern
- Temporal join
- CTEs
- dbt snapshots

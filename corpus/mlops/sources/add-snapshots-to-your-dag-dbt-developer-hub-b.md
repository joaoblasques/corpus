---
type: source
domain: mlops
status: stub
sources:
  - path: raw/web/web-add-snapshots-to-your-dag-dbt-developer-hub.md
    channel: web
    ingested_at: 2026-07-21
aliases: []
tags:
  - corpus/mlops
  - source
  - doc-quick-intake
created: 2026-07-21
updated: 2026-07-21
provisional: false
url: https://docs.getdbt.com/docs/building-a-dbt-project/snapshots/
origin: obsidian-list
---

# Add snapshots to your DAG | dbt Developer Hub

> **Quick intake** (obsidian-list). [open source](https://docs.getdbt.com/docs/building-a-dbt-project/snapshots/)

dbt provides a mechanism called snapshots to record changes to mutable tables over time, implementing type-2 Slowly Changing Dimensions. Snapshots can be used to track changes to all columns or specific columns, and can be configured to handle schema changes. dbt snapshot command must be run on a schedule to ensure changes are recorded.

**Key topics**
- dbt snapshots
- Slowly Changing Dimensions
- change data capture
- schema changes
- snapshot strategies
- timestamp strategy

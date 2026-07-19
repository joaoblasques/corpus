---
type: source
domain: data-engineering
status: stub
sources:
  - path: raw/notes/notes-03-resources-articles-full-refresh-vs-incremental-pipeline-design.md
    channel: notes
    ingested_at: 2026-07-19
aliases: []
tags:
  - corpus/data-engineering
  - source
  - doc-quick-intake
created: 2026-07-19
updated: 2026-07-19
provisional: false
url: 
origin: obsidian
---

# Full Refresh vs Incremental Pipelines — Design Decision Framework

> **Quick intake** (obsidian). raw stub: `notes-03-resources-articles-full-refresh-vs-incremental-pipeline-design.md`

Choosing between full refresh and incremental pipeline strategies is a consequential architectural decision that affects compute costs, implementation complexity, and scalability. The right answer depends on understanding the source data's update patterns. Incremental pipelines are efficient at scale but require source data understanding and careful handling of late-arriving data.

**Key topics**
- Full Refresh Pipelines
- Incremental Pipelines
- Data Engineering
- Compute Costs
- Implementation Complexity
- Scalability

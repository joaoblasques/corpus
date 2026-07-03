---
type: entity
domain: data-engineering
status: stub
sources:
  - path: raw/web/web-academic-cto-what-actually-matters-in-data-matthew-housley-c33adeb7.md
    channel: web
    ingested_at: 2026-07-01
aliases:
  - Matthew Housley
  - Data Engineering Fundamentals
  - Ternary Data
tags:
  - corpus/data-engineering
  - entity
created: 2026-07-01
updated: 2026-07-01
---

# Matthew Housley

**TL;DR.** Co-author of *Fundamentals of Data Engineering* (O'Reilly, 2022, with Joe Reis) and former CTO of Ternary Data. Path: mathematics academic → data scientist at Overstock.com → VP/CTO leading data strategy. Known for the "foundations over flashy models" perspective on data teams.

## Core view: foundations over tools

Housley's observation: most companies don't have a tooling problem — they have a **foundation problem**. Modern stacks, cloud platforms, and expensive dashboards don't deliver value if the underlying data quality, governance, and organizational alignment aren't in place [^src1]. The recurring failure pattern: analytics efforts fail *before* they start because the organization has not defined what "delivering value" means in data terms [^src1].

Key distinctions he draws [^src1]:
- **Data science vs. data engineering vs. analytics**: distinct disciplines with different value-delivery mechanisms; conflating them leads to misaligned expectations
- **Academic thinking vs. industry execution**: academic rigor is necessary but not sufficient; the gap is translating models into durable business outcomes
- **"Doing data" vs. delivering value**: activity (models run, dashboards built) ≠ impact (decisions made, revenue influenced)

## See also

- [The Data Engineer Role](/data-engineering/data-engineer-role.md) — foundations vs. tooling tradeoffs
- [Meaning in Data Modeling](/data-engineering/data-modeling-meaning.md) — the semantic foundation layer
- [Data Engineering hub](/data-engineering/README.md)

---

[^src1]: [Academic → CTO: What Actually Matters in Data — Matthew Housley interview (Data Engineering Central Podcast)](../../raw/web/web-academic-cto-what-actually-matters-in-data-matthew-housley-c33adeb7.md)

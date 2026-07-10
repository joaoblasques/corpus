---
type: entity
domain: data-engineering
status: draft
sources:
  - path: raw/web/web-fusion-in-bloom-dbt-labs-98d5a43b.md
    channel: web
    ingested_at: 2026-07-01
aliases:
  - dbt Fusion
  - Fusion engine
  - SDF
  - dbt VS Code Extension
tags:
  - corpus/data-engineering
  - entity
created: 2026-07-01
updated: 2026-07-01
---

# dbt Fusion Engine

**TL;DR.** dbt Fusion is a **Rust-powered compiler and execution engine** for dbt, replacing the Python-based core with ~30× faster parse times, state-aware orchestration (build only when code or data changes), and richer metadata. Shipped as public beta in May 2025; approaching GA as of mid-2026 [^src1].

## Origin

January 14, 2025: **SDF joins dbt Labs** — a major acquisition of a Rust-powered SQL compiler built by Elias DeFaria and co-founders. Development started January 6, 2025 (first commit). 8,611 commits in the first year [^src1].

## Key milestones

| Date | Milestone |
|---|---|
| Jan 2025 | SDF acquisition; development begins |
| May 2025 | Public beta + dbt VS Code Extension public beta (104,200 downloads) |
| Jun 2025 | "Powered by Fusion" program — Snowflake embeds Fusion directly |
| Oct 2025 | State-aware orchestration private preview |
| Nov 2025 | dbt Jobs in Microsoft Fabric announced |
| Dec 2025 | ADE-bench benchmark framework adopted; 25+ preview releases; 450+ weekly projects on Fusion |

## Core capabilities

**~30× faster parse times** — the Rust-based compiler eliminates the Python parsing bottleneck [^src1].

**State-aware orchestration**: builds only when code or data changes; reuses results otherwise. Result: "~40% model reuse and 30% warehouse compute cost savings for projects using state-aware orchestration" [^src1].

**Richer metadata**: enables column-level lineage and deeper semantic understanding of SQL (key for dbt v2 upgrades) [^src1].

**AI-native benchmarking**: adopted the ADE-bench framework for evaluating how well AI agents complete real dbt tasks — Fusion-based agents "complete real-world dbt tasks faster and more efficiently, requiring fewer steps, lower compute cost, and less trial-and-error" [^src1].

## Ecosystem integration

- Snowflake embeds Fusion natively into Snowflake dbt Projects
- Microsoft Fabric: dbt Jobs available (public preview), Fusion support planned
- 4 supported adapters (as of mid-2026)
- dbt VS Code Extension ships alongside Fusion (editor integration)

## Community

- 1,957 members in `#dbt-fusion-engine` Slack channel
- 312 community-opened bug reports and feature requests incorporated
- 16 editions of "Fusion Diaries" newsletter (25,120 subscribers)

## Relationship to dbt v2

The dbt v2 migration path runs *through* Fusion — Fusion provides the deeper SQL comprehension and column-level lineage that makes the v2 upgrade practical. The dbt Summit 2026 training catalog includes "Upgrade to dbt v2" as a dedicated course [^src1].

## See also

- [dbt](/data-engineering/dbt.md) — the transformation framework Fusion powers
- [Apache Spark](/data-engineering/apache-spark.md) — Fusion's state-aware orchestration reduces the "recompute everything" default that plagues Spark-based pipelines
- [Data Quality](/data-engineering/data-quality.md) — Fusion enables tighter CI/CD quality gates by surfacing column-level lineage

---

[^src1]: [Fusion in Bloom — dbt Labs](../../raw/web/web-fusion-in-bloom-dbt-labs-98d5a43b.md)

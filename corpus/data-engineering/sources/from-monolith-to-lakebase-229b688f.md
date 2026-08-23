---
type: source
domain: data-engineering
status: draft
aliases: []
tags:
  - corpus/data-engineering
  - database
  - oltp
  - postgres
  - databricks
  - neon
sources:
  - path: raw/_inbox/web-from-monolith-to-lakebase-to-ltap-rethinking-the-database-fr-229b688f.md
    channel: web
    title: "From monolith to Lakebase to LTAP: rethinking the database from storage up"
    url: https://www.databricks.com/blog/lakebase-ltap-rethinking-database-storage
    author: Reynold Xin
confidence: 0.9
last_confirmed: 2026-08-23
created: 2026-08-23
updated: 2026-08-23
---

# Source: From Monolith to Lakebase to LTAP

**Author**: Reynold Xin (Databricks cofounder)
**URL**: https://www.databricks.com/blog/lakebase-ltap-rethinking-database-storage
**Collected**: 2026-07-01

## Summary

Deep-dive technical post by a Databricks cofounder explaining the architecture of Lakebase (Databricks's serverless Postgres, built on Neon) and LTAP (Lake Transactional/Analytical Processing). The post works from first principles: monolithic OLTP problems → externalized WAL/data-file services → Lakebase architecture → LTAP extension.

## Key claims

- Classic Postgres colocates WAL and data files on one machine; all five major durability/scaling/HA/analytics problems trace to this.[^src]
- Lakebase externalizes WAL to SafeKeeper (Paxos quorum) and data files to PageServer (write-through cache → object storage). Postgres compute becomes stateless.[^src]
- Write latency is **not** increased vs a serious monolithic Postgres HA setup — synchronous replication already requires the network hop; SafeKeeper just makes it explicit and replicated.[^src]
- SafeKeeper + PageServer combination yields "5× higher write throughput and 2× lower read latency" vs classic Postgres HA.[^src]
- Branching/cloning/PITR become metadata operations (pointer in versioned storage layer), not physical copies.[^src]
- LTAP: PageServer transcodes Postgres row format → Parquet columnar as data lands in object storage. Result: one governed copy in Delta/Iceberg readable by both Postgres and Lakehouse engines.[^src]
- Freshness mechanism: analytical query fetches current LSN from Postgres (cheap metadata), reads from object storage, merges very recent unmaterialized changes from PageServer. Postgres serves only the LSN number.[^src]
- Postgres MVCC row versions are preserved internally but not exposed to Iceberg/Delta readers; eventually garbage-collected.[^src]
- Unlike CDC/mirroring: no opt-in, no replication lag, no second copy, no drift.[^src]

## Corpus pages produced

- [/data-engineering/lakebase.md](/data-engineering/lakebase.md) — primary concept page

---

[^src]: raw/_inbox/web-from-monolith-to-lakebase-to-ltap-rethinking-the-database-fr-229b688f.md

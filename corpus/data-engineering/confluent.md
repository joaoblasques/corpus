---
type: entity
domain: data-engineering
status: draft
sources:
  - path: raw/_inbox/web-my-confluent-chapter-from-apache-kafka-startup-to-11-billion-9dcd0637.md
    channel: web
    ingested_at: 2026-08-11
aliases:
  - Confluent
  - Confluent Cloud
  - confluent
  - Confluent Platform
tags:
  - corpus/data-engineering
  - entity
created: 2026-08-11
updated: 2026-08-11
---

# Confluent

**TL;DR.** Confluent is the managed **Apache Kafka** platform company, acquired by IBM for $11 billion in early 2026 — the company that turned Kafka from a messaging system into the de facto standard for real-time data streaming across 150,000+ organizations [^src1].

## Origin

Founded 2014 by Jay Kreps (CEO), Neha Narkhede, and Jun Rao — the engineers who created Apache Kafka at LinkedIn. The pitch was making Kafka enterprise-ready. In May 2017, when [Kai Waehner](/data-engineering/kai-waehner.md) joined as Field CTO, the company had ~100 employees [^src1].

## Growth arc

- **2017**: ~100 employees; Kafka used by a small number of tech companies; enterprises hadn't heard of it [^src1]
- **2021**: IPO on NASDAQ in June [^src1]
- **2025-12**: IBM acquisition announced at $11B enterprise value [^src1]
- **2026**: IBM deal closed; $1.12B revenue at close; Confluent Cloud alone $624M; ~1,500 customers spending $100K+/year [^src1]

## Platform evolution

Confluent grew the Kafka framework progressively [^src1]:
- **Kafka Connect** — hundreds of connectors for data integration
- **Kafka Streams** — stream processing layer
- **Apache Flink** — stateful computation added at scale
- **Apache Iceberg** — open table format connecting streaming to lakehouse/AI pipelines
- **WarpStream (BYOC)** — bring-your-own-cloud diskless Kafka deployment
- **Tiered storage / Diskless Kafka** — separating compute from storage (an instance of [compute–storage decoupling](/data-engineering/compute-storage-decoupling.md), the same object-storage move warehouses and lakehouses made earlier)
- **Queues for Kafka (QfK)** — native queue support (Kafka 4.2)

Confluent is the company that established **data streaming as a recognized software category** (Forrester Wave 2023: Leader; IDC recognition) — no longer confused with "ESB", "ETL", or "iPaaS" [^src1].

## IBM acquisition rationale

IBM brings global enterprise reach; Confluent brings the leading data streaming platform. Together they position to sell Confluent as part of IBM's broader enterprise portfolio [^src1].

> "The new question is how fast real-time data streaming becomes the foundation for agentic AI." — Kai Waehner [^src1]

## Related

- [Apache Kafka](/data-engineering/kafka.md) — the underlying technology
- [Kai Waehner](/data-engineering/kai-waehner.md) — Confluent Field CTO 2017–2026; primary source for this page
- [Stream processing](/data-engineering/stream-processing.md) — processing paradigm
- [Shift Left Architecture](/data-engineering/shift-left-architecture.md) — architectural pattern Confluent championed
- [Data Integration Patterns (2026)](/data-engineering/data-integration-patterns.md) — the IBM/Confluent $11B deal opens the vendor-consolidation argument

[^src1]: [My Confluent Chapter: From Apache Kafka Startup to $11 Billion](../../raw/web/web-my-confluent-chapter-from-apache-kafka-startup-to-11-billion-9dcd0637.md) — Kai Waehner, kai-waehner.de

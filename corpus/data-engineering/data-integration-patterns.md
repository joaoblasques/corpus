---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/_inbox/web-data-integration-landscape-2026-event-streaming-api-and-batc-7a30ee72.md
    channel: web
    ingested_at: 2026-08-10
  - path: raw/_inbox/web-sap-agentic-ai-and-the-data-integration-reckoning-3f3cb445.md
    channel: web
    ingested_at: 2026-08-10
  - path: raw/_inbox/web-kafka-vs-flink-vs-spark-do-you-really-need-real-time-aa493b5d.md
    channel: web
    ingested_at: 2026-08-10
  - path: raw/_inbox/web-edge-to-cloud-and-back-four-data-movement-problems-and-why-o-6e89b591.md
    channel: web
    ingested_at: 2026-08-10
  - path: raw/_inbox/web-data-integration-vs-workflow-orchestration-connecting-system-8dc4b75e.md
    channel: web
    ingested_at: 2026-08-10
  - path: raw/_inbox/web-why-i-joined-kestra-enterprise-workflow-orchestration-for-th-bed6aa45.md
    channel: web
    ingested_at: 2026-08-10
  - path: raw/_inbox/web-erp-migration-to-sap-s-4hana-and-beyond-lessons-learned-from-c3acf82e.md
    channel: web
    ingested_at: 2026-08-10
  - path: raw/_inbox/web-yaml-vs-xml-vs-json-which-format-wins-and-when-a13d6d07.md
    channel: web
    ingested_at: 2026-08-10
  - path: raw/_inbox/web-what-is-apache-arrow-flight-confessions-of-a-data-guy-70dad6f1.md
    channel: web
    ingested_at: 2026-08-11
aliases:
  - data integration
  - data integration patterns
  - data integration landscape
  - event-driven integration
  - three data integration paradigms
  - request-response integration
  - batch integration
  - event streaming integration
  - EDA
  - event-driven architecture
  - SAP API policy
  - agentic data access
  - real-time SLA
  - edge to cloud
  - northbound telemetry
  - southbound control
  - data integration vs workflow orchestration
  - integration vs orchestration
  - Kestra
  - unified orchestration
  - Apache Arrow Flight
  - Arrow Flight
  - gRPC data transport
tags:
  - corpus/data-engineering
  - concept
created: 2026-08-10
updated: 2026-08-11
confidence: 0.85
last_confirmed: 2026-08-10
---

# Data Integration Patterns (2026)

**TL;DR.** Data integration is no longer back-office plumbing — it is a strategic asset. IBM acquired Confluent for $11B, Salesforce acquired Informatica for $8B, Qlik absorbed Talend, and Fivetran merged with dbt Labs [^land1]. The Data Integration Landscape 2026 maps all major vendors across **three communication paradigms**: request-response, batch, and event streaming. The central argument: **event-driven architecture belongs at the center**, with batch and request-response as consumer interfaces on top [^land1].

## The three paradigms

| Paradigm | How it moves data | Strengths | Weaknesses |
|---|---|---|---|
| **Request-response** (REST, GraphQL, API gateways) | System asks, system waits | Simple, familiar, transactional | Couples caller to callee; blocking |
| **Batch** (ETL, Fivetran, scheduled exports) | Bulk on a schedule | Reliable, well-understood, cheap at low frequency | Data always stale (minutes to hours); breaks when you need now |
| **Event streaming** (Kafka + Flink) | Continuous as events occur | Decoupled, persistent, real-time, replay-capable | Higher operational complexity; learning curve |

No large enterprise runs a single integration platform — the real question is **which paradigm sits at the center**, and how the rest connect to it without recreating point-to-point tangles [^land1].

**Event streaming as center**: when a transaction completes or a record changes, the event is published to a stream; any downstream system consumes independently, without asking the source. This decouples producers from consumers — a slow or unavailable system doesn't block everything else [^land1]. Apache Kafka is the de facto standard for event streaming; Apache Flink is the de facto standard for stateful stream processing on top of Kafka [^land1].

**Batch is not dead**: it remains the right model for historical loads, AI model training, regulatory reporting, and analytics where data freshness of hours is acceptable [^land1]. "The mistake is treating the choice as either/or. A business unit running iPaaS workflows, an analytics team pulling batch exports, and an AI agent querying live state can all be served from the same event-driven backbone" [^land1].

## Real-time: SLA-first, not latency-first

"Real-time is the most oversold word in data infrastructure" [^rts1]. Four questions to ask before tool selection:
1. What latency does the business actually require — as a *number tied to a use case*? Not "fast," but 50 milliseconds, 2 seconds, or 10 minutes.
2. Is this operational or analytical?
3. What is the SLA for data loss and uptime? Can you drop a record?
4. Where does the data live and get consumed? Edge, on-prem, one cloud, or many?

**The latency spectrum** [^rts1]:
- **Hard real-time** (deterministic, guaranteed, OT): engine control, flight control, collaborative robots — implemented in C/C++/Rust on embedded systems. Kafka/Flink/Spark are **not** hard real-time and never will be.
- **Critical real-time** (microseconds): stock exchange matching engines — not Kafka/Flink, requires specialized co-located technology.
- **Low-latency real-time** (10s–100s ms): fraud detection in instant payments, sensor analytics, ride-hailing correlation — Kafka/Flink sweet spot.
- **Near real-time** (seconds): streaming ETL into warehouse, regulatory reporting — still real-time enough for most business needs.

Most enterprise use cases live in low-latency or near real-time. The millisecond pitch targets a tier most workloads never reach [^rts1].

## Kafka vs Flink vs Spark: when to use each

| Tool | Primary role | Paradigm |
|---|---|---|
| Apache Kafka | Event backbone; persistent log; publish-subscribe at scale | Event streaming (transport layer) |
| Apache Flink | Stateful stream processing; CEP; real-time ML inference; ETL on streams | Event streaming (processing layer) |
| Apache Spark | Batch processing; large-scale ML training; micro-batch streaming (seconds to minutes) | Batch / micro-batch |

Kafka handles the *movement* of events; Flink processes them *in motion*; Spark processes them *in batch or near-real-time micro-batches*. The operational distinction: Flink's default is streaming (batch as a special case); Spark's default is batch (streaming as a special case) [^rts1].

## SAP API policy and the agentic data access problem

In April 2026, SAP published API Policy v4/2026 §2.2.2 prohibiting use of SAP APIs for "interaction or integration with (semi-)autonomous or generative AI systems that plan, select, or execute sequences of API calls" — i.e., no third-party AI agents on SAP data unless SAP authorizes it [^sap1].

The infrastructure argument is legitimate: SAP systems run mission-critical processes where 90% accuracy is not good enough; autonomous agents create load profiles platforms weren't designed for [^sap1]. But the policy also creates an asymmetry: SAP's own AI products (Joule, Business Data Cloud, Agent Gateway) are exempt; third-party agents (Microsoft Copilot, Salesforce Einstein, independent vendors) face formal restrictions [^sap1].

**The same pattern exists across every major business application platform** [^sap1]:
- Salesforce restricted Slack API access: third-party tools cannot store, index, or use Slack data to train/fine-tune AI models
- ServiceNow enforces strict rate limits on inbound agent traffic — limits that become architectural constraints as agent volumes scale

**The known solution is data independence via streaming**: enterprises have solved this pattern before. The mainframe answer was the same — protect the core system, distribute data via extracted/staged copies. Change Data Capture + Apache Kafka is the modern form: Kafka continuously extracts from the source system and distributes to any consumer that needs it, without coupling to the source's API throttling or policy restrictions [^sap1].

Real enterprise results: Royal Bank of Canada decoupled consumption from mainframe → real-time analytics across 50+ applications; Citizens Bank reflected 99.99% of mainframe changes in cloud apps within 4 seconds [^sap1]. SAP customers building this pattern: the data exits SAP via Kafka Connect, becomes a stream, and AI agents consume the stream — not the SAP API [^sap1].

## Edge-to-cloud: four traffic patterns (not one)

Edge-to-cloud is not one integration problem — it is four, each with different physics [^e2c1]:

1. **Northbound telemetry** — sensor readings, machine states, transactions, logs from edge to central platform. Most settled pattern: MQTT + Kafka, with the edge dialing out (not inbound connections through firewalls).
2. **Southbound control** — commands, configuration, software updates, AI models from central down to machines and gateways. Requires reliable delivery to constrained/intermittently connected devices.
3. **Site-to-site sync** — data synchronization between sites, between site and data center, or between clouds. More data is "fine as periodic batch over a metered link" than teams admit [^e2c1].
4. **Outbound delivery** — live data from central platforms to the applications people use: dashboards, mobile apps, trading screens.

**Network constraints decide the architecture before product selection** [^e2c1]:
- **Store and forward** is the single most important capability: edge must operate offline; data buffers locally; sync resumes on reconnect
- **Edge always dials out** — industrial sites sit behind NAT/firewalls/cellular; no inbound ports. MQTT clients dial out; NATS leaf nodes dial out; Azure IoT Operations dials out. Different stacks, identical constraint.
- **Hardware heterogeneity**: 8-bit microcontroller vs. fanless gateway PC vs. site server → matching technology footprint to tier is half the selection process
- **Data residency** (especially EU): which data leaves the site, country, or jurisdiction must be provable via topic design and routing rules

**The four edge tiers** [^e2c1]: device edge (microcontrollers, sensors) → gateway edge (industrial PCs, protocol converters) → site edge (factory, store, hospital with local compute) → near edge (regional data centers). A technology fitting one tier often fails another.

## Data integration vs workflow orchestration

**Integration** connects systems and moves data. **Orchestration** coordinates what runs, in what order, and what to do when a step fails [^orch1].

The surface similarity (both have connectors to databases, SaaS apps, and APIs) causes confusion. But they serve different jobs: integration uses connectors to *move and reshape data*; orchestration uses them to *trigger and coordinate tasks* [^orch1].

**Integration unit of work**: the dataset, stream, or record. Key question: "Did the data arrive — correct, complete, on time, and consistent across every system that holds it?" [^orch1]

**Orchestration unit of work**: the task, workflow, or process. Key question: "Did the right steps run, in the right sequence, with the right dependencies, and what do we do about the one that failed?" [^orch1]

Consistency is integration's hard problem — same customer record in a dozen systems. Dual-write, out-of-order events, and duplicate delivery all threaten correctness. Most streaming systems offer *at-least-once delivery + idempotent processing* = effectively-once (not true exactly-once). CDC, transactional outbox patterns, and reconciliation hold consistency together [^orch1].

**Orchestration scope is broader than data**: IT/batch job scheduling, business process automation, infrastructure provisioning, and — increasingly — agentic AI (agents' actions must be sequenced, gated, and recovered like any workflow) [^orch1]. See [Process Intelligence](/data-engineering/process-intelligence.md) for the discipline above orchestration.

## ERP migration patterns (SAP S/4HANA, German manufacturing)

Three German manufacturing cases (Fritz Winter Eisengießerei, mid-market valve maker, office furniture producer) produced the same pattern regardless of vendor choice [^erp1]:

1. **Consolidate before migrating**: Fritz Winter chose to move all production logic from a non-SAP system into SAP ERP first (master data, warehouse, manufacturing processes, MM/SD/QM/PP/PLM/PM) — then migrate to S/4HANA. Timeline pushed by 1 year; cutover over an extended weekend + 2-week hypercare [^erp1].
2. **Process layer decides success or failure, not technology**: master data, production logic, material flows, and supply chain traceability must be sorted before migration. No cloud SKU or AI agent compensates for an unsorted process layer [^erp1].
3. **Mid-market alternative**: some manufacturers left SAP for focused mid-market ERP products — better fit for simpler process scope, lower implementation overhead [^erp1].

The relationship to data integration: SAP is the most common source system for enterprise data integration via Kafka/CDC. Clean ERP structure directly determines the quality of operational event streams downstream [^erp1].

## Data format trade-offs: YAML, XML, JSON

These formats serve different jobs [^fmt1]:

| Format | Era | Strength | Best for now |
|---|---|---|---|
| **XML** | Enterprise integration (2000s) | Verbose, rigorous, schema-first (XSD) | Legacy systems, financial/regulatory messaging (AIDX, FIX) |
| **JSON** | Web APIs (2010s) | Compact, universal, human-parseable | REST APIs, LLM tool calling, structured outputs |
| **YAML** | Cloud-native config (2015+) | Human-readable, minimal punctuation, multi-line strings | Kubernetes manifests, CI/CD config, data contracts |

**Validation is a separate layer from serialization** [^fmt1]: XML uses XSD; JSON uses JSON Schema; YAML borrows JSON Schema (no schema language of its own). JSON Schema now underpins LLM tool calling and structured outputs — it is at the center of agentic AI integration.

**Data contracts**: authored in YAML, validated by JSON Schema, enforced in the pipeline — a pattern now common in dbt, Great Expectations, and streaming schema registries [^fmt1].

## Apache Arrow Flight: high-performance columnar data transport

Apache Arrow Flight is a high-performance data transport framework built on top of Apache Arrow and gRPC, enabling applications to move large datasets across networks much faster than JDBC, ODBC, CSV exports, or REST APIs [^arrow1].

The core advantage: Arrow's columnar in-memory format can be sent over the wire as `RecordBatches` without serialization/deserialization at the destination — the data arrives in the format that is already directly usable by Arrow-aware consumers [^arrow1].

**Architecture**:
- **Client-server model**: clients make requests to an Arrow Flight Server via gRPC (Google's HTTP/2-based RPC framework) [^arrow1]
- **Multiple endpoints**: Arrow Flight Servers have multiple endpoints that work together to fulfill requests — making data transfer parallelizable, unlike traditional single-coordinator distributed systems [^arrow1]
- **Tight coupling**: Arrow Flight is a framework for building custom data transport layers; it does not provide ready-made connectors — implementers write `doGet`, `doPut` methods [^arrow1]

**Practical uses**: high-speed data movement between ML pipelines, analytics engines, and storage layers where JDBC/ODBC bandwidth would be the bottleneck. Databricks' Zerobus uses gRPC + Apache Arrow RecordBatches for exactly this pattern (see [Databricks](/data-engineering/databricks.md)).

## Related

- [Apache Kafka](/data-engineering/kafka.md) — event streaming backbone
- [Stream Processing](/data-engineering/stream-processing.md) — Flink, Spark, CEP
- [Shift Left Architecture](/data-engineering/shift-left-architecture.md) — three consumer interfaces on a shared event-driven layer
- [Process Intelligence](/data-engineering/process-intelligence.md) — orchestration layer above integration
- [MCP vs REST vs Kafka](/ai-engineering/mcp.md) — which protocol for which AI use case
- [Confluent](/data-engineering/confluent.md) — the IBM-$11B acquisition anchoring the vendor-consolidation opener
- [Kai Waehner](/data-engineering/kai-waehner.md) — author of most sources on this page
- [Data Engineering hub](/data-engineering/README.md)

---

[^land1]: [Data Integration Landscape 2026: Event Streaming, API, and Batch in the Era of Agentic AI (Kai Waehner)](../../raw/web/web-data-integration-landscape-2026-event-streaming-api-and-batc-7a30ee72.md)
[^sap1]: [SAP, Agentic AI, and the Data Integration Reckoning (Kai Waehner)](../../raw/web/web-sap-agentic-ai-and-the-data-integration-reckoning-3f3cb445.md)
[^rts1]: [Kafka vs Flink vs Spark: Do You Really Need Real-Time? (Kai Waehner)](../../raw/web/web-kafka-vs-flink-vs-spark-do-you-really-need-real-time-aa493b5d.md)
[^kestra1]: [Why I Joined Kestra: Enterprise Workflow Orchestration for the Agentic AI Era (Kai Waehner)](../../raw/web/web-why-i-joined-kestra-enterprise-workflow-orchestration-for-th-bed6aa45.md) — Kestra unifies four legacy categories (IT scheduling, data pipelines, business processes, infrastructure automation) under one declarative event-driven control plane; used at Apple, JPMorgan, Toyota, Xiaomi
[^erp1]: [ERP Migration to SAP S/4HANA and Beyond: Lessons Learned from German Manufacturing (Kai Waehner)](../../raw/web/web-erp-migration-to-sap-s-4hana-and-beyond-lessons-learned-from-c3acf82e.md)
[^fmt1]: [YAML vs XML vs JSON: Which Format Wins, and When (Kai Waehner)](../../raw/web/web-yaml-vs-xml-vs-json-which-format-wins-and-when-a13d6d07.md)
[^e2c1]: [Edge to Cloud and Back: Four Data Movement Problems (Kai Waehner)](../../raw/web/web-edge-to-cloud-and-back-four-data-movement-problems-and-why-o-6e89b591.md)
[^orch1]: [Data Integration vs Workflow Orchestration: Connecting Systems Is Not Coordinating the Work (Kai Waehner)](../../raw/web/web-data-integration-vs-workflow-orchestration-connecting-system-8dc4b75e.md)
[^arrow1]: [What is Apache Arrow Flight?](../../raw/web/web-what-is-apache-arrow-flight-confessions-of-a-data-guy-70dad6f1.md) — confessionsofadataguy.com, "What is Apache Arrow Flight?"

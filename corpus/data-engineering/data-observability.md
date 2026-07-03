---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/web/web-data-observability-fundamentals-for-data-engineers.md
    channel: web
    ingested_at: 2026-06-17
  - path: raw/email/email-2026-06-24-how-i-made-my-data-platform-s-failures-public-and-earned-my.md
    channel: email
    ingested_at: 2026-06-26
aliases:
  - data observability
  - observability patterns
  - flow interruption detector
  - skew detector
  - lag detector
  - SLA misses detector
  - dataset tracker
  - fine-grained tracker
  - MTTD
  - MTTR
tags:
  - corpus/data-engineering
  - concept
created: 2026-06-17
updated: 2026-06-26
---

# Data Observability

**TL;DR.** Data observability is "the capability of a system that generates information on how the data influences its behaviour and, conversely, how the system affects the data" [^src1]. In practice it is the instrumentation layer that catches silent data failures — pipelines that run cleanly and produce nothing, or models that drift without crashing. It is distinct from [data quality](/data-engineering/data-quality.md) (the goal) and [data contracts](/data-engineering/change-data-capture.md) (prevention); observability is the **flashlight** that reveals problems after they occur, while contracts are a **laser** aimed at known risks [^src1].

## Where observability sits in the DE lifecycle

Observability is not a checkpoint — it runs as a thread underneath all pipeline stages: **ingestion → transformation → serving → analytics/BI/AI** [^src1]. Problems grow more expensive as they move downstream:

| Stage | Cost of a problem |
|---|---|
| Ingestion | Quick fix |
| Transformation | Debugging session |
| Serving | Missed SLA |
| Analytics / AI / BI | Business incident |

Most teams start at transformation/serving where tooling is mature. The strongest approach is **end-to-end: start at ingestion, extend through transformation, validate at serving, protect at the consumption layer** [^src1].

## Data quality vs observability vs contracts

| Concept | Role |
|---|---|
| **Data quality** | The goal: data fit for its purpose |
| **Data observability** | The sensors: visibility into when the goal is not met |
| **Data contracts** | Prevention: agreed expectations between producers and consumers |

> *"Most teams start with observability because they need visibility before they can define good contracts."* [^src1]

See [Data Quality](/data-engineering/data-quality.md) for the quality dimensions (validity, completeness, timeliness, uniqueness, consistency) and contract patterns.

## Detection patterns

Detection patterns catch problems in the data stream.

### Flow Interruption Detector

The most underrated pattern — catches the case where a pipeline runs cleanly and produces nothing [^src1]. Three implementation layers (pick the layer that fits your system):

- **Metadata layer**: check when a table was last updated (fast/cheap; caveat: schema changes can update timestamp without new data).
- **Data layer**: compare row counts between runs.
- **Storage layer**: check when the last file was written (caveat: some operations create files without new data).

For high-frequency streams: alert when expected records stop arriving within a defined window. For irregular data: alert only if the gap exceeds what is statistically normal.

### Skew Detector

Catches the case where a batch job runs successfully on a dataset that is a fraction of its expected size — no error, just quietly wrong output built on incomplete input [^src1]. Algorithm:

1. Define comparison window (today vs. yesterday, or current vs. last successful run — always use last *successful* run to avoid the "fatal loop" where one bad dataset makes correct data look wrong next day).
2. Set a tolerance threshold (e.g., ±50%).
3. Calculate: `STDDEV(x) / AVG(x)` for partitioned systems, or simple percentage difference.

Watch for seasonality — campaigns, weekends, seasons cause legitimate volume shifts; thresholds should reflect actual business behavior, not raw math [^src1].

**Use as a gate at the start of the pipeline**: stop before processing rather than cleaning up incorrect output afterwards.

### Lag Detector

Measures how far behind a pipeline is relative to available data [^src1]:

```
lag = last available unit − last processed unit
```

A "unit" is context-dependent: record offset in a queue, version number in a table, or timestamp in a partitioned dataset. In streaming: if the latest Kafka offset is 10,000 and the processed offset is 9,200, lag = 800 records. Growing lag is an early warning sign — catch it before it becomes missing data or missed SLAs.

### SLA Misses Detector

Determines whether the pipeline is breaking commitments to consumers [^src1]. Two dimensions for streaming jobs that must be measured separately:

- **Processing time SLA**: gap between when a record is read and when it is written — reflects the pipeline's own performance.
- **Event time SLA**: gap between when a record was generated and when it was written — includes delays outside your control (e.g., a producer losing connectivity and delivering buffered data late).

*"If you only track one, you'll either take blame for delays that aren't yours or miss delays that are."* [^src1]

For batch jobs: measure start-to-end elapsed time against the SLA threshold. Note that some orchestrators measure from the *scheduled* start rather than actual start — a long-running upstream task can cause SLA breaches without any individual task being "slow".

## Tracking patterns

Tracking patterns answer *where did this problem come from?*

### Dataset Tracker (Lineage)

Builds a dependency graph across all datasets, annotated with owning teams [^src1]. When something goes wrong, you can trace upstream in minutes rather than days. Two implementation paths:

- **Managed / platform-native**: auto-captures lineage within the ecosystem (fast setup; check which ingestion methods are actually covered).
- **Open-source cross-stack** (OpenLineage, Marquez, OpenMetadata): works across multiple tools and clouds; requires more upfront engineering; not locked to one platform.

> *"Most teams know they need lineage. Very few actually build it. It gets deprioritised because it doesn't feel urgent — until something breaks."* [^src1]

### Fine-Grained Tracker (Column-level lineage)

Tracks which input columns feed each output column by analyzing query execution plans [^src1]. Example: a `CONCAT(first_name, delivery_address)` expression producing `user_with_address` is traceable back to `users.first_name` and `addresses.delivery_address`. Supported automatically for standard SQL in most modern platforms.

**Limits**: custom functions and programmatic transformation logic are opaque — the lineage framework sees inputs and outputs but not what happened inside. Row-level lineage (knowing which job produced each specific row) is implemented by decorating records with metadata: job name, version, batch number.

## Implementation paths

Three realistic approaches [^src1]:

| Path | Characteristics |
|---|---|
| **Build with open-source** (Great Expectations, dbt tests, OpenLineage, Marquez, OpenMetadata) | Full control, cost-effective at scale, requires ownership |
| **Buy a dedicated platform** (Monte Carlo, etc.) | Fast time-to-coverage, minimal setup, higher cost, vendor shapes your strategy |
| **AI-generated checks** | Point an agent at the warehouse, sample tables, generate tests — removes the bottleneck of writing hundreds of checks manually; limited by undocumented business logic |

The hardest part of observability has never been the infrastructure — *"every orchestrator supports running SQL checks"* — the hard part is defining what "healthy" looks like for each dataset and writing the right tests. AI removes the time bottleneck; tribal knowledge in team heads remains a gap that must be explicitly documented and fed to the agent [^src1].

## Starting without creating noise

- **Start with one pipeline you know well**, ideally one that has already caused pain.
- **Work backwards from your consumer**: instrument the final dataset first, then trace upstream.
- **One focused alert per objective**: alert fatigue kills observability faster than almost anything else.
- **Measure MTTD and MTTR** before and after implementation — these numbers justify further expansion.
- **Treat new and legacy pipelines differently**: bake observability into new pipelines from day one; for legacy, start with broad scans to find existing problems and prioritise by impact. Some old pipelines due for retirement may not be worth instrumenting [^src1].

## From detection to communication (the status page)

Detection and lineage answer *what broke* and *what it affects* — but stakeholders only benefit if that reaches them without asking. The **consumption-facing** end of observability is a **data platform status page** that turns a declared incident into a stakeholder-readable view of which data products and reports are affected [^src2]. It depends on the column-level lineage above plus one extra hop most lineage tools miss — **mapping dbt models to the specific BI dashboard tiles that query them** (reconstructed by pulling each tile's query from the BI tool's API) — so a failure at ingestion traces all the way to the affected report [^src2]. The **status history** is where MTTD/MTTR become a trust artifact: a year of visible incidents with resolution times converts a vague "the data is always broken" complaint into documented fact [^src2]. See [Data Platform Status Page](/data-engineering/data-status-page.md).

## Relationship to contracts

After building observability, the next step is data contracts. Observability shows you what is going wrong repeatedly — contracts prevent those specific known problems from recurring [^src1]. See [Data Quality](/data-engineering/data-quality.md) for the contract patterns.

## Related

- [Data Quality](/data-engineering/data-quality.md) — the goal that observability monitors; contract patterns
- [Data Orchestration](/data-engineering/data-orchestration.md) — SLA monitoring hooks available natively in most orchestrators
- [Incremental Pipeline Design](/data-engineering/incremental-pipeline-design.md) — lag and backfill scenarios are primary observability targets
- [Change Data Capture](/data-engineering/change-data-capture.md) — CDC streams require flow interruption and lag detection
- [dbt](/data-engineering/dbt.md) — dbt tests + Elementary package for model-level observability
- [Data Platform Status Page](/data-engineering/data-status-page.md) — the consumer-facing surface built on top of lineage + incident detection

[^src1]: [Data Observability Fundamentals for Data Engineers](../../raw/web/web-data-observability-fundamentals-for-data-engineers.md)
[^src2]: [How I Made My Data Platform's Failures Public and Earned My Stakeholders' Trust (Yordan Ivanov, Data Gibberish)](../../raw/email/email-2026-06-24-how-i-made-my-data-platform-s-failures-public-and-earned-my.md)

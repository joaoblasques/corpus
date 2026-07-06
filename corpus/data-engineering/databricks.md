---
type: entity
domain: data-engineering
status: draft
sources:
  - path: raw/email/email-2026-05-25-when-and-when-not-to-use-databricks.md
    channel: email
    ingested_at: 2026-06-11
  - path: raw/web/debunking-8-data-layout-myths-why-liquid-clustering-outperfo.md
    channel: web
    ingested_at: 2026-06-11
  - path: raw/web/unity-catalog.md
    channel: web
    ingested_at: 2026-06-11
  - path: raw/web/databricks-pricing-flexible-plans-for-data-and-ai-solutions.md
    channel: web
    ingested_at: 2026-06-11
  - path: raw/web/lakeflow-spark-declarative-pipelines-databricks-on-aws.md
    channel: web
    ingested_at: 2026-06-11
  - path: raw/youtube/youtube-qndigzfaufs.md
    channel: youtube
    ingested_at: 2026-06-17
  - path: raw/web/web-stop-hand-coding-change-data-capture-pipelines.md
    channel: web
    ingested_at: 2026-06-17
  - path: raw/web/web-why-dbt-is-terrible-for-databricks-switch-to-native-pipeline.md
    channel: web
    ingested_at: 2026-06-17
  - path: raw/email/email-2025-04-17-the-internal-of-bigquery-snowflake-databricks-and-redshift.md
    channel: email
    ingested_at: 2026-06-19
  - path: raw/youtube/youtube-761SQ9Hxbic-databricks-tutorial-databricks-free-edition-tutorial-with-en.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-0Hd5vYqin7w-databricks-data-engineer-associate-certification-course-pass.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/web/web-how-databricks-is-turning-video-into-searchable-actionable-i-f044690d.md
    channel: web
    ingested_at: 2026-07-06
  - path: raw/web/web-how-the-english-office-for-students-leverages-databricks-to-8fc137c4.md
    channel: web
    ingested_at: 2026-07-06
  - path: raw/web/web-how-daikin-applied-americas-builds-consistent-data-pipelines-1bb3ddbe.md
    channel: web
    ingested_at: 2026-07-06
  - path: raw/web/web-what-if-the-answer-was-already-in-your-data-5e70850d.md
    channel: web
    ingested_at: 2026-07-06
  - path: raw/web/web-the-rise-of-sports-intelligence-how-the-lakehouse-turns-trac-3c304692.md
    channel: web
    ingested_at: 2026-07-06
aliases:
  - Databricks
  - Unity Catalog
  - Unity Catalogue
  - Liquid Clustering
  - Lakeflow
  - Lakeflow Spark Declarative Pipelines
  - Databricks Data Engineer Associate
  - DBD-DEA
  - Databricks certification
  - Genie Code
  - Lakebase
  - Databricks Lakebase
  - Serverless GPU Compute
  - Databricks SGC
tags:
  - corpus/data-engineering
  - entity
created: 2026-06-11
updated: 2026-07-06
---

# Databricks

**TL;DR.** Databricks is a **lakehouse platform** that puts warehouse-style SQL, BI, ML, and streaming on top of low-cost object storage (S3, ADLS, GCS) using open table formats such as Delta or Iceberg [^src1]. It earns its keep when the alternative is stitching a warehouse, Spark cluster, streaming engine, notebook environment, feature store, governance layer, and permission model from multiple vendors [^src1]. It is "a powerful platform... also a heavy one" — the adoption question is fit, not quality [^src1]. Key primitives: **Unity Catalog** (governance), **Liquid Clustering** (data layout), **Lakeflow Spark Declarative Pipelines** (orchestration), and **Photon** (vectorised query engine) [^src1].

## Origin and what it actually bundles

Databricks was founded ~2013 by the UC Berkeley AMPLab team behind Apache Spark; Spark itself started in 2009 to balance Hadoop's fault tolerance and scalability while allowing data reuse across processes, formalized in the **RDD (Resilient Distributed Dataset)** paper [^src6]. The progression: people wanted managed Spark (like AWS EMR or GCP Dataproc), and Databricks went "a few steps further" [^src6]. It is **not one open-source tool but several** — at its core **Spark + Delta Lake + MLflow** [^src6]:
- **Spark** — the unavoidable processing engine; most users interact here. See [Apache Spark](/data-engineering/apache-spark.md).
- **Delta Lake** — sets up Delta tables (ACID transactions on files). See [Open Table Formats](/data-engineering/open-table-formats.md).
- **MLflow** — model registry, deployment, and monitoring (the "I built a model, now what?" answer); alternative to Kubeflow [^src6].

## Lakehouse positioning vs Snowflake

Databricks bet on the **data lakehouse** — combining a data lake's cost-effectiveness with a warehouse's management benefits (security, clear table structures) [^src6]. Its ads poke fun at the data warehouse; it pitches itself as "everything: SQL, BI, real-time analytics," whereas **Snowflake leans more toward the data-science use case** for lakehouses [^src6]. A practitioner read: Databricks is **geared heavily toward data scientists** — everything centers on notebooks — though it serves data engineers too via jobs, table streaming from Kafka, and micro-batch/batch ETL [^src6]. Both vendors now sell themselves as **data platforms, not just a lake or a cloud warehouse** [^src6]. See [Snowflake](/data-engineering/snowflake.md) for the competing architecture and the 2021 benchmark dispute.

## Core UI components (user-facing)

The primitives a Databricks user works with [^src6]: **workspaces** (personal or shared), **clusters** (Spark compute — pick node count/size, Spark version, and auto-terminate-on-inactivity to control cost), **tables** (an abstraction over files — external/internal, Delta-backed tables give ACID where plain tables don't), **notebooks** (Python/Scala/SQL/R — multi-language support comes from Spark underneath), **jobs** (productionize a notebook: chain tasks into dependencies, schedule via UI or cron, resize the cluster), and **libraries** [^src6]. The integrated developer experience — Git version control, swappable cluster config, notebook→job promotion — is cited as a Databricks advantage over Snowflake's "purely SQL-based" tasks that aren't visible/creatable in a UI [^src6]. The "table ≈ file" abstraction reflects the broader trend of schema-on-read blurring the table/file distinction even in the Snowflake world [^src6].

## When Databricks makes sense

Five strong-fit situations [^src1]:

1. **Multi-TB data with mixed workloads** — BI, ad-hoc SQL, batch, streaming, and ≥1 ML use case on the same data with one permission story.
2. **Ten or more engineers across disciplines** — shared platform + shared catalogue makes lineage and governance reusable.
3. **Multi-source ingestion with governance requirements** — a dozen sources plus real legal obligations (finance, healthcare, regulated public sector); Unity Catalog, row/column-level security, unified audit logs.
4. **Replatforming off Hadoop or legacy Spark** — biggest immediate win; Spark knowledge transfers, short learning curve.
5. **Streaming, ML, and BI on the same data** — lakehouse is the path of least resistance.

## When Databricks is overkill

The section "that does not get written often enough" [^src1]:

- **Sub-500GB BI-only workloads** — Postgres + dbt + a managed BI tool quietly out-delivers on cost, simplicity, hiring, time-to-dashboard. See [Postgres](/data-engineering/postgres.md), [dbt](/data-engineering/dbt.md).
- **Small teams (1–3 engineers) who have never run Spark** — months lost to cluster configs, shuffle partitions, broadcast joins.
- **Single-cloud, single-source SQL workloads** — one cloud warehouse (BigQuery, Snowflake, Redshift, Synapse) is enough.
- **Pure batch, daily refresh** — managed Airflow + warehouse + dbt is "boring... boring is hireable" [^src1].
- **Early-stage startups still figuring out the data layer** — a lakehouse is a premature commitment to heavy architecture.

## Decision framework

Four questions to run every time the adoption question comes up [^src1]:

1. **Data scale and growth?** Multi-TB and growing → lakehouse. Sub-500GB and linear → Postgres + dbt.
2. **Team size and skill mix?** Small SQL-first team → wrong tool. Larger mixed-discipline team → compounding leverage.
3. **Workload mix?** BI + ML + streaming on same data → lakehouse. BI-only or batch-SQL-only → single warehouse.
4. **Realistic total cost of ownership?** Build a TCO model (compute, storage, egress, governance, engineering time) for both Databricks and the simpler stack, over one and three years [^src1].

## Common adoption mistakes

Seven recurring patterns [^src1]:

1. Picking Databricks "for the logo" — cultural pressure dressed as a decision.
2. Running all-purpose (interactive) clusters 24/7 — they bill for idle; move scheduled jobs to job clusters or serverless, auto-terminate aggressively.
3. Rolling out Unity Catalog before there is anything to govern — UC is genuine setup work; deploy when governance pain is real.
4. Treating Databricks as "just managed Spark" — never adopting Lakeflow, serverless SQL, or Photon. The platform does one thing instead of five.
5. No cost guardrails on day one — budgets, alerts, cluster policies, tags in week one.
6. Underestimating egress and storage — DBU bill is on the Databricks invoice; egress, object storage, snapshot retention, and UC metadata live on the cloud provider's invoice. Monitor both.
7. Picking Databricks without picking who owns it — name an owner before adoption.

## Cost model

Databricks has **several prices, by workload type**, not one [^src1]:

- **All-purpose compute** — most expensive; interactive notebook work. Do not run scheduled jobs here.
- **Jobs compute** — cheaper than all-purpose for the same spec; scheduled work belongs here.
- **SQL warehouses (serverless/classic)** — built for BI; serverless is meaningfully cheaper for bursty workloads.
- **Declarative pipelines (Lakeflow)** — own SKU; value is orchestration, dependency management, incremental processing.

The **DBU** (Databricks Unit) is a normalised measure of processing capacity; matching the workload to the right SKU drops the bill with no code change [^src1]. Most waste lives in cluster lifecycle: auto-terminate interactive clusters, use spot instances for fault-tolerant work, right-size drivers, enforce cluster policies [^src1]. Databricks pricing is pay-as-you-go at per-second granularity with no up-front cost, plus Committed Use Contracts for volume discounts [^src4].

## Unity Catalog

Databricks' governance layer for tables, files, models, and access policies [^src1]. A unified catalog for structured data, unstructured data, business metrics, and AI models across open formats like Delta Lake, Apache Iceberg, Hudi, and Parquet [^src3]. Provides row- and column-level security, unified audit logs, auto-detection/tagging of sensitive data, and a single pane of glass for policy enforcement [^src1][^src3]. Setup is non-trivial: Metastore, catalogues, external locations, storage credentials, and permissions inheritance [^src1].

## Liquid Clustering vs partitioning

Liquid Clustering is Databricks' modern data-layout standard, GA since 2024, positioned to replace Hive-style partitioning [^src2]. Hive-style partitioning forces a commit at table-creation time to a physical file organization; wrong-cardinality columns produce billions of tiny files or slower queries — and in Databricks' analysis it leads to over-partitioning and small-file problems in **more than 75% of cases** [^src2]. Liquid instead treats clustering keys as engine *input*: keys can change at any time (or be auto-selected via Automatic Liquid Clustering), cardinality is not a constraint, and layout evolves without unnecessary rewrites [^src2].

Key points [^src2]:

- **Directory-pruning is a myth on modern OTFs.** Delta uses a transaction log with per-column stats; pruning happens against statistics at file granularity, not directory structure. Liquid uses the same mechanism.
- **Row-level concurrency** vs partitioning's file-level concurrency — two writers on different rows in the same file no longer conflict, removing a main reason teams partitioned (write boundaries).
- **Metadata-only operations** (DELETE, COUNT, DISTINCT, GROUP BY) are supported; metadata-only DELETEs ran ~90% faster than full-rewrite DELETEs in benchmarks.
- **It is a write-side optimization** producing standard Parquet with min/max stats; any compatible reader (open-source Spark, [DuckDB](/data-engineering/duckdb.md), etc.) benefits — not Databricks-only.
- Production: Arctic Wolf runs a 3.8+ PB telemetry table ingesting 1+ trillion events/day on Liquid Clustering [^src2].

> Source caveat: the Liquid Clustering myth-busting is a Databricks blog promoting its own feature over partitioning; benchmark figures are vendor-reported.

See [MERGE INTO](/data-engineering/merge-into.md) and [Parquet](/data-engineering/parquet.md) for related layout mechanics.

## Lakeflow Spark Declarative Pipelines

A framework for batch and streaming pipelines in SQL and Python, formerly known as DLT — you describe tables and the platform handles orchestration and incremental processing [^src1][^src5]. Lakeflow SDP extends and is interoperable with Apache Spark Declarative Pipelines while running on the performance-optimized Databricks Runtime [^src5]. Core concepts: pipelines, flows, streaming tables, and materialized views; common use cases are ingestion from cloud storage (S3, ADLS Gen2, GCS) and message buses (Kafka, Kinesis, Pub/Sub, EventHub, Pulsar) plus incremental transformations [^src5]. See [Kafka](/data-engineering/kafka.md); this complements [Stream Processing](/data-engineering/stream-processing.md) as the Databricks/Spark Structured Streaming path for the streaming-and-micro-batch use cases.

## dbt vs. Lakeflow SDP on Databricks

A practitioner perspective: managing dbt inside Databricks Asset Bundles (DABs) carries a "complexity tax" that becomes harder to justify as the platform matures [^src7]:

- **Lineage black hole**: pushing transformations through an external dbt Core manifest means Unity Catalog loses seamless visibility — breaking native data quality monitoring and Feature Store traceability.
- **Folder inception in DABs**: a dbt directory inside DABs requires managing tool versions, adapter updates, and orchestrating external CLI runs within Databricks Workflows.
- **Native declarative SQL**: Databricks handles DAG construction, dependency tracking, incremental processing, and Spark scaling automatically in Lakeflow SDP without a third-party framework.

Counter-arguments from the comments [^src7]:
- dbt's **platform agnosticism** provides portability, stronger vendor negotiating power, and easier future migrations — especially valuable in hybrid architectures (Databricks for heavy transformation + a separate SQL serving layer).
- dbt still has features SDP lacks or requires workarounds for (pre/post hooks, macros, complex incremental materialization logic).
- Teams with deep dbt expertise may retain it while the platform matures.

**The verdict is context-dependent**: pure Databricks end-to-end shops have strong reasons to prefer native SDP; mixed-platform or portability-sensitive teams have strong reasons to retain dbt.

See [dbt](/data-engineering/dbt.md) for the dbt perspective and [Change Data Capture](/data-engineering/change-data-capture.md) for AutoCDC specifics.

## Photon internals (the query engine)

Databricks faced a structural problem: Spark was **not built as a native query engine**, yet the lakehouse must deliver warehouse-grade performance on everything from clean datasets to raw messy files with no useful statistics [^src8]. Rather than replace Spark (and disrupt existing customers), Databricks **enhanced it** [^src8]:

- **Photon** is a C++ library of physical operators integrated into the **Databricks Runtime (DBR)** — itself a fork of Apache Spark for reliability/performance [^src8]. Photon operators slot into the Spark query plan; customers benefit with **no code changes**, and the system falls back to Spark SQL for unsupported operations [^src8].
- Photon uses a **vectorized model** (process batches of values) rather than Spark's **code-generation** approach, which enables **runtime adaptivity** — it discovers and leverages micro-batch data characteristics with specialized code paths [^src8]. (Contrast Redshift, which chose code specialization — see [Cloud Data Warehouse Internals](/data-engineering/cloud-data-warehouse-internals.md).)
- Photon is written in **C++** (not the JVM) for explicit control over memory management and SIMD [^src8].
- It adopts a **columnar in-memory representation**, eliminating the expensive column-to-row pivot that row-oriented Spark SQL needed when scanning columnar files like Parquet [^src8].

**Delta Lake** is the storage layer: an ACID table layer over cloud object storage whose core idea is keeping track of **which objects belong to a table via a write-ahead log in the object store** [^src8]. Data files are **Apache Parquet** objects (optionally Hive-partitioned); a file unreferenced by the transaction log is unreadable [^src8]. Delta was served to customers in 2017 and open-sourced in 2019 [^src8]. See [Open Table Formats](/data-engineering/open-table-formats.md) and [Parquet](/data-engineering/parquet.md).

## Databricks Free Edition (for learners)

Databricks offers a **free edition** with **serverless compute only** — no cluster creation/management [^src9]. Entry points and features available in the free tier [^src9]:

- **Catalog UI**: the `workspace` catalog → `default` schema → tables and volumes hierarchy; upload CSVs/files via the Data Ingestion page
- **SQL Editor**: runs queries against catalog tables using serverless compute; connects automatically to the serverless pool
- **Notebooks**: pre-initialized `spark` object; support Python, SQL, Scala, R
- **Volumes**: raw file storage within a catalog schema; upload files *as-is* (vs. tables, which register a schema); path format `/Volumes/catalog/schema/volume/file`
- **Genie**: natural-language chat interface over Unity-Catalog-registered datasets; converts English questions to SQL automatically [^src9]
- **Jobs and Pipelines**: schedule ETL jobs without managing clusters
- **AI playground, Model Serving**: for LLM/ML experiments

> "Serverless compute is sort of like AWS Lambda — behind the scenes they have servers but all those details are hidden from you, so you can just focus on your business logic." [^src9]

**Managed vs external tables**: managed tables are owned by Databricks (data and metadata both in Databricks); external tables point to data in external object storage [^src9].

**Three cluster types relevant to cost optimization** (full accounts only; not available in free edition):
- **All-purpose compute** — interactive notebook work; most expensive; don't run scheduled jobs here
- **Jobs compute** — cheaper for scheduled jobs
- **Serverless SQL warehouses** — best for bursty BI workloads

See [Apache Spark](/data-engineering/apache-spark.md) for the PySpark API reference, and the Catalyst / Photon / lazy evaluation details that apply to Databricks notebooks.

## Databricks Data Engineer Associate Certification

Exam code PR000054 (Databricks's internal code) [^src10]. Covers:

- **Databricks Intelligence Platform** overview (10%) — general offerings, workspace navigation
- **Development & Ingestion** — creating ETL workflows (Jobs), working with pipelines
- **Data Processing & Transformations** — PySpark, RDDs, medallion architecture, the three data layers
- **Productionizing Pipelines** — moving pipelines to production
- **Data Governance & Quality** — security features, data masking, quality patterns

Exam format [^src10]: 45 multiple-choice questions, 90-minute time limit, passing grade 70%, valid for 24 months. "Practical knowledge over conceptual" — expect code examples in the exam. Proctor provider: Criterion Online.

Study guidance [^src10]: allocate 15–20 hours (~60% lecture/labs + 40% practice exams). Recommended path: Data Engineer Associate → Data Engineer Professional (skip other Databricks certifications). A certification alone does not validate programming, SQL, or production data engineering skills — it demonstrates platform familiarity [^src10].

## Genie Code (AI-assisted pipeline generation)

Genie Code is Databricks' AI-assisted approach to data engineering that works against governed data in Unity Catalog to plan and generate multi-step pipelines [^src11]. Pipelines that previously took days to prototype can be generated in minutes; iteration cycles shorten, and engineers spend less time on boilerplate and more time refining business logic [^src11].

A recurring structural challenge is that LLMs produce inconsistent outputs when teams rely on varied prompts or loosely defined instructions — the same request can yield architectural drift over time [^src11]. Daikin Applied Americas solved this with a **MECE (Mutually Exclusive, Collectively Exhaustive) skill framework**: each skill defines one coherent competency of the data engineering lifecycle (medallion architecture design, source readiness and grain definition, transformation patterns, canonical alignment, governance standards), non-overlapping and collectively exhaustive [^src11]. Standards are embedded directly into the execution environment rather than stored in prompts:

> "Prompts get you started, but they are a bad place to enforce team standards. If the same rule matters more than once, it should live in the workspace as a skill, where Genie Code can actually use it." [^src12]

The same team uses medallion layer checkpoints as explicit decision boundaries during pipeline generation: before data advances across layers, requirements (source grain definition, join validation, data stability checks) must be satisfied — enforced in the development workflow, not as downstream review steps [^src11]. The outcome: "pipeline prototyping reduced from days to minutes" with governed, consistent outputs [^src11].

Genie Code also supports natural-language queries over Unity-Catalog-registered datasets, converting questions to SQL without requiring BI or SQL expertise [^src13]. In sports analytics contexts, coaches can ask "How have my starting five's third-quarter shot mechanics changed against zone defense over the last ten games?" and receive an immediate data-backed answer [^src14].

## Lakebase (serverless Postgres on Databricks)

Lakebase is Databricks' fully managed, serverless PostgreSQL database built for AI applications and agents [^src15]. It separates compute from storage for transactional data — the architectural differentiator that enables true elastic scaling, eliminates idle compute costs, and keeps data consistently available regardless of whether compute is running [^src15]. Key properties:

- **Co-located with the lakehouse**: Lakebase sits on the same storage and governance layer as the data lakehouse, so operational data, analytics, and AI workloads share a single platform — eliminating ETL pipelines to move data between systems [^src15].
- **Postgres-compatible**: teams continue using familiar drivers, ORMs, and development practices from day one [^src15].
- **Unity Catalog governed**: access controls, lineage, and auditing remain consistent across every layer [^src15].
- **Sub-second query latency**: serves interactive analyst-facing applications and real-time dashboards without waiting on a warehouse [^src14].

In production at Kythera Labs (AI-native healthcare strategy), Lakebase powers the operational layer alongside Delta Lake, Delta Sharing, and Unity Catalog — "No ETL. No data movement. No seams between the question and the answer." [^src13] At Superhuman (AI email platform), feature onboarding and reverse-ETL projects previously taking months were compressed into weeks or hours after adopting Lakebase [^src15].

See [Serverless Databases](/data-engineering/serverless-databases.md) for the broader concept (serverless PostgreSQL, compute-storage decoupling for OLTP, AI workload patterns).

## Video intelligence pipeline (Serverless GPU Compute)

Databricks frames video analytics as a **data engineering problem**, not a computer vision problem [^src11b]. The pipeline:

1. User uploads video to a Databricks Volume and issues a natural-language prompt (e.g., "white box trucks, security guards, solar panels").
2. A Lakeflow job is triggered; **Serverless GPU Compute (SGC)** grabs pre-warmed NVIDIA GPUs within seconds.
3. Meta's **SAM3** segmentation model identifies matching objects in each frame; video is truncated to relevant segments (example: 26-minute traffic camera → 1 minute 55 seconds of relevant footage with original timestamps preserved) [^src11b].
4. Each truncated clip is passed via the **Databricks Foundation Model API (FMAPI)** to a VLM for AI-generated summarization; text is written to tables or flows downstream.
5. Concurrency is trivially configurable: 20 videos → 20 parallel jobs, each grabbing its own GPU compute independently [^src11b].

The pipeline is **model-agnostic via MLflow**: SAM3 can be swapped for YOLO, other transformer-based vision models, or fine-tuned domain-specific models without breaking the pipeline; the summarization/anomaly-detection layer is similarly swappable [^src11b]. The same architecture supports event-driven triggering (video lands in a Volume → auto-triggers Lakeflow) and human-triggered workflows [^src11b].

## Sports intelligence use case (SkeleTRACK + Lakehouse)

Professional sports analytics on the Databricks lakehouse illustrates both scale and the cross-domain analysis problem [^src14]. The **NBA Hawk-Eye SkeleTRACK** system (deployed March 2023 across all 29 arenas) captures 29 skeletal joints on every player and referee at 60 fps — approximately **22,620 positional updates per second**, ~**65 million records per 48-minute game**, and ~**80 billion records** across an 82-game regular season [^src14].

The lakehouse mediates the fragmentation problem: tracking data, wearables, video, opponent scouting, injury analytics, and medical data all arrive from different vendors [^src14]. Without a unified governed platform, this fragmentation produces missed injury signals, slower in-game decisions, and an inability to run cross-domain analysis combining tracking with medical history, workload, and opponent tendencies [^src14]. The medallion pipeline on Databricks:

- **Bronze**: continuous 60 Hz frames from Hawk-Eye, wearable, and event feeds ingested via Lakeflow.
- **Silver**: event catalog — possessions, shots, screens, defensive matchups, with frame ranges correlated to camera output and arena calibration applied.
- **Gold**: analytics-ready feature layer that drives injury-risk, shot-probability, and fatigue-index models [^src14].

Unity Catalog provides lineage and access control across the combined data estate — critical when medical data sits next to performance data [^src14]. The same lakehouse producing the injury risk model also produces broadcast feeds; the NBA's Christmas Day 2024 game was the league's first fully animated broadcast built on SkeleTRACK data [^src14].

## Enterprise case studies

**Office for Students (UK)** — manages data spanning millions of student records over decades from 400+ higher-education providers [^src12]. A 300-million-record data-wrangling job that took 8 hours on legacy systems runs in minutes on Databricks; a student segmentation analysis that required two analysts two weeks now completes in half a day [^src12]. Genie Code reduced a provider-registration-triage task from two to three colleagues reading documents over a month to an automated flagging system [^src12]. Unity Catalog provides the lineage, consistent access controls, and security patterns required in a regulated environment [^src12].

**Kythera Labs (healthcare)** — AI-native healthcare strategy platform built on Databricks that processes 339 billion medical/prescription drug claims (300M patients, 8 years, 3+ petabytes) [^src13]. Claims data is transformed from billing exhaust into event-based structures where a knee replacement is "a surgical event with a pre-operative history, a discharge, and a post-operative care trajectory" — the translation work that makes AI answers trustworthy [^src13]. A Louisiana health system went from contract to first insight in 10 days, achieving 150% increased patient-encounter visibility and $3.8M estimated annualized value from retained encounters [^src13].

## Related

- [Cloud Data Warehouse Internals](/data-engineering/cloud-data-warehouse-internals.md) — Photon vs Dremel/Snowflake/Redshift compared
- [BigQuery](/data-engineering/bigquery.md) · [Redshift](/data-engineering/redshift.md) — the other cloud warehouses
- [Open table formats](/data-engineering/open-table-formats.md) — Delta/Iceberg underpin the lakehouse
- [Data lake](/data-engineering/data-lake.md) · [Apache Iceberg](/data-engineering/apache-iceberg.md) · [Parquet](/data-engineering/parquet.md)
- [dbt](/data-engineering/dbt.md) · [Postgres](/data-engineering/postgres.md) — the "simpler stack" alternatives
- [DuckDB](/data-engineering/duckdb.md) — reads Liquid-Clustered output
- [Snowflake](/data-engineering/snowflake.md) — competing cloud OLAP platform; lakehouse rivalry
- [Apache Spark](/data-engineering/apache-spark.md) — the processing engine at Databricks' core
- [Serverless Databases](/data-engineering/serverless-databases.md) — Lakebase, serverless PostgreSQL, compute-storage decoupling for OLTP

[^src1]: [When (and when not) to use Databricks](../../raw/email/email-2026-05-25-when-and-when-not-to-use-databricks.md)
[^src2]: [Debunking 8 data layout myths: why Liquid Clustering outperforms partitioning](../../raw/web/debunking-8-data-layout-myths-why-liquid-clustering-outperfo.md)
[^src3]: [Unity Catalog (Databricks)](../../raw/web/unity-catalog.md)
[^src4]: [Databricks pricing](../../raw/web/databricks-pricing-flexible-plans-for-data-and-ai-solutions.md)
[^src5]: [Lakeflow Spark Declarative Pipelines (Databricks on AWS)](../../raw/web/lakeflow-spark-declarative-pipelines-databricks-on-aws.md)
[^src6]: [What is Databricks and why people use it (SeattleDataGuy)](../../raw/youtube/youtube-qndigzfaufs.md)
[^src7]: [Why dbt is terrible for Databricks, switch to native pipelines](../../raw/web/web-why-dbt-is-terrible-for-databricks-switch-to-native-pipeline.md)
[^src8]: [The internal of BigQuery, Snowflake, Databricks and Redshift (Vu Trinh)](../../raw/email/email-2025-04-17-the-internal-of-bigquery-snowflake-databricks-and-redshift.md)
[^src9]: [Databricks Tutorial | Databricks Free Edition End-to-End (codebasics)](../../raw/youtube/youtube-761SQ9Hxbic-databricks-tutorial-databricks-free-edition-tutorial-with-en.md)
[^src10]: [Databricks Data Engineer Associate Certification Course – Pass the Exam! (Andrew Brown / freeCodeCamp)](../../raw/youtube/youtube-0Hd5vYqin7w-databricks-data-engineer-associate-certification-course-pass.md)
[^src11]: [How Daikin Applied Americas builds consistent data pipelines at scale with Genie Code](../../raw/web/web-how-daikin-applied-americas-builds-consistent-data-pipelines-1bb3ddbe.md)
[^src11b]: [How Databricks is turning video into searchable, actionable intelligence](../../raw/web/web-how-databricks-is-turning-video-into-searchable-actionable-i-f044690d.md)
[^src12]: [How the English Office for Students leverages Databricks to enhance higher education standards](../../raw/web/web-how-the-english-office-for-students-leverages-databricks-to-8fc137c4.md)
[^src13]: [What if the answer was already in your data? (Kythera Labs)](../../raw/web/web-what-if-the-answer-was-already-in-your-data-5e70850d.md)
[^src14]: [The Rise of Sports Intelligence: How the Lakehouse Turns Tracking Data into Competitive Advantage](../../raw/web/web-the-rise-of-sports-intelligence-how-the-lakehouse-turns-trac-3c304692.md)
[^src15]: [What To Look For in a Serverless Database for AI Applications](../../raw/web/web-what-to-look-for-in-a-serverless-database-for-ai-application-8e1ddee7.md)

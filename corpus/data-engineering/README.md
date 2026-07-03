---
type: hub
domain: data-engineering
status: draft
tags:
  - corpus/data-engineering
  - hub
created: 2026-05-07
updated: 2026-06-26
---

# Data Engineering

Domain covering ETL/ELT pipelines, data modeling, Spark, Iceberg, dbt, orchestration, the lakehouse stack, and data quality. Graduated domain (2026-05-21). Substantially expanded in the 2026-06-11 email-backlog ingest (wave 1), the 2026-06-15 inbox ingest (wave 2: storage fundamentals, DE best practices, Python, CI/CD, data migration, semantic layer, progressive disclosure, AI's impact on DE), the 2026-06-17 web-backlog ingest (wave 3: data observability, BI-as-code, ClickHouse, team OS, AutoCDC, Spark joins, grain/fan-out, WAP pattern, dbt snapshots, dbt complete guide, Claude Code/dbt assessment, API extraction patterns), the 2026-06-17 inbox ingest (wave 4: Markdown Team / 10x data team), the 2026-06-25 inbox ingest (wave 5: PySpark fundamentals PDF series, Databricks free edition tutorial, DuckDB origin story, pgledger, modern data stack 10 components, Azure DE project, Windsor.ai no-code ETL, Dataherald GitHub digest), the 2026-06-25 batch 2 ingest (wave 6: PySpark RDD + Pair RDDs, spark-pdf, Kestra orchestration, streaming scaling + popular systems, SCD2 fact-join, curl/wget/csvkit shell tools, Databricks cert, SQL DW build, FHIR overview, BSL GitHub, Metabase dataset generator), and the 2026-06-25 batch 3 ingest (wave 7: PySpark DataFrame API + SQL ch.3, sql2csv/csvsql/cron shell tools, batch processing fundamentals + event-based computing, database normalization 1NF–5NF, dbt crash course, LangChain+BigQuery NL-to-SQL, DataExpert.io handbook, DA→DE transition, Efficient Data Processing Spark course repo, OMOP CDM, Perspective data viz component).

## Pages

### Concepts
- [Data Observability](/data-engineering/data-observability.md) — concept · draft · 6 patterns (flow interruption, skew, lag, SLA misses, dataset tracker, fine-grained tracker); MTTD/MTTR; 3 implementation paths
- [Data Platform Status Page](/data-engineering/data-status-page.md) — concept · draft · stakeholder-facing incident communication; lineage→dashboard-tile mapping; transparency builds trust; zero questions per incident
- [BI as Code](/data-engineering/bi-as-code.md) — concept · draft · SQL embedded in Markdown; Evidence.dev; git-native dashboards; co-location with dbt models
- [Data Engineering Team OS](/data-engineering/data-engineering-team-os.md) — concept · draft · two-layer leader OS: Rhythm (standup/1:1/sprint check-in/retro) + Memory (team/work/project/meetings)
- [SCD2 (Slowly Changing Dimension Type 2)](/data-engineering/scd2.md) — concept · draft · history-preserving dimension pattern; valid_from/valid_to + is_current flags
- [MERGE INTO](/data-engineering/merge-into.md) — concept · draft · atomic Spark SQL operation combining matched/unmatched/source-only actions in one statement
- [Pipeline Layers](/data-engineering/pipeline-layers.md) — concept · draft · staging → warehouse → marts ELT separation pattern; Raw DB vs Analytics DB
- [Data Lake / Lakehouse](/data-engineering/data-lake.md) — concept · draft · object-storage lake + open table format metadata wrapper; cost hierarchy; partitioning anti-patterns
- [Idempotent Pipelines](/data-engineering/idempotent-pipelines.md) — concept · draft · same-input-same-output guarantee; pitfalls, fixes, and SCD idempotency mapping
- [Dimensional Modeling](/data-engineering/dimensional-modeling.md) — concept · draft · fact + dimension tables; SCD types; streak_identifier pattern; when to skip SCD
- [SQL Window Functions](/data-engineering/sql-window-functions.md) — concept · draft · ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD, running aggregates; frame clauses; interview reference
- [Data Orchestration](/data-engineering/data-orchestration.md) — concept · draft · scheduling vs orchestration vs observability; when cron isn't enough; do you need Airflow
- [Open Table Formats](/data-engineering/open-table-formats.md) — concept · draft · DB-independent metadata layer (Iceberg/Delta/Hudi); open data infrastructure
- [Medallion Architecture](/data-engineering/medallion-architecture.md) — concept · draft · bronze/silver/gold are lifecycle stages, not a data model; Kimball-vs-Inmon
- [Change Data Capture (CDC)](/data-engineering/change-data-capture.md) — concept · draft · full load vs incremental vs CDC; capturing deletes, latency
- [Materialized Views](/data-engineering/materialized-views.md) — concept · draft · cross-platform MV synthesis; incremental vs full refresh; limitations
- [Data Quality](/data-engineering/data-quality.md) — concept · draft · 6-step clean-warehouse framework; data contracts; schema-aware validation
- [Data Ingestion Patterns](/data-engineering/data-ingestion-patterns.md) — concept · draft · two ingestion patterns: stream via event log vs batch extract
- [dlt (data load tool)](/data-engineering/dlt.md) — entity · draft · declarative REST API pipelines (RESTAPIConfig); 4 pagination patterns; dlt AI Workbench
- [Data Flow Patterns](/data-engineering/data-flow-patterns.md) — concept · draft · source/sink replayability+overwritability; extraction (time-ranged/snapshot/lookback/streaming), behavioral (idempotent/self-healing), structural (multi-hop/conditional/disconnected)
- [Scaling Data Pipelines](/data-engineering/scaling-data-pipelines.md) — concept · draft · vertical vs horizontal (independent processes / distributed); strategy-selection questions; beware premature optimization
- [Incremental Pipeline Design](/data-engineering/incremental-pipeline-design.md) — concept · draft · timestamp-driven extraction, model-driven load, parallel backfilling
- [Storage Fundamentals](/data-engineering/storage-fundamentals.md) — concept · draft · storage hierarchy; file/block/object; row vs columnar serialisation
- [Data Engineering Best Practices](/data-engineering/data-engineering-best-practices.md) — concept · draft · six pipeline best practices: 3-hop, DQ, idempotency, DRY, metadata, tests
- [Python for Data Engineering](/data-engineering/python-for-data-engineering.md) — concept · draft · disk vs memory; Python as glue across ETL/DQ/test/orchestrate
- [Pipeline Coding Patterns (Python)](/data-engineering/pipeline-coding-patterns.md) — concept · draft · code design patterns for DE: Factory, Strategy, Singleton/Object pool, functional design, context managers, typing/dataclasses, pytest, decorators
- [DE Portfolio Projects](/data-engineering/de-portfolio-projects.md) — concept · draft · runnable batch/stream/event-driven projects; stack-comparison matrix
- [Data Engineering Interview & Job Search](/data-engineering/data-engineering-interview.md) — concept · draft · the 10 interview skills (SQL-first) + the 5-step job search (companies, LinkedIn, referrals, prep, negotiation)
- [CI/CD for Data Infrastructure](/data-engineering/cicd-for-data-infrastructure.md) — concept · draft · CI plan→PR, CD apply-dev→human-gate→prod; GitHub Actions + Terraform
- [Data Migration at Scale](/data-engineering/data-migration-at-scale.md) — concept · draft · Shadow → Reverse Shadow → Cleanup; row-count/checksum verification; CDC rollback
- [Meaning in Data Modeling](/data-engineering/data-modeling-meaning.md) — concept · draft · semantics, taxonomy, ontology, metadata (Joe Reis)
- [Semantic Layer](/data-engineering/semantic-layer.md) — concept · draft · metric/knowledge layer as critical AI infra; data teams → context teams; agentic architect
- [ETL Pipeline](/data-engineering/etl-pipeline.md) — concept · draft · Extract/Transform/Load; ETL vs ELT vs data pipeline; batch vs streaming; 2026 tools & trends
- [Data Mart](/data-engineering/data-mart.md) — concept · draft · community-specific DSS store; Demarest's hybrid warehouse+marting multitiered model; schema explosion
- [PostgreSQL Views](/data-engineering/postgresql-views.md) — concept · draft · views as rewrite rules (pg_rewrite macros); inlining, SELECT * trap, security_invoker, schema-evolution pain
- [Graph Databases (RDF vs LPG)](/data-engineering/graph-databases.md) — concept · draft · RDF/OWL vs labeled property graph decision framework; index-free adjacency, RDF 1.2, GQL, workload-dependent benchmarks
- [Storing Intermediate Results in SQL](/data-engineering/sql-intermediate-results.md) — concept · draft · CTE vs subquery vs view vs temp table vs materialized view; materialized-or-not decision framework; staging tables
- [Requirements Gathering](/data-engineering/requirements-gathering.md) — concept · draft · the 5-step process (identify end-users, define via a question set, validate, deliver iteratively, gate changes) + output-led engineering
- [Stream Processing](/data-engineering/stream-processing.md) — concept · draft · batch vs stream/micro-batch; latency/throughput/backpressure/state/event-time; engines (Flink/Kafka Streams/Spark SS/Storm); delivery guarantees; Lambda architecture
- [Data Transformation (the "T" in ETL/ELT)](/data-engineering/data-transformation.md) — concept · draft · what the T solves (business logic, standardization, integration, pre-aggregation); transform-focused tools (dbt/SQLMesh/Dataform); common SQL transforms; transform-layer challenges + raw/stage/prod ↔ medallion
- [Small-Scale Pipeline Design](/data-engineering/small-scale-pipeline-design.md) — concept · draft · small ≠ low-stakes; problem-scope questions; design principles; tool choice; the DE's 7-step implementation mindset; signals to refactor/scale up
- [Modern Data Stack (MDS)](/data-engineering/modern-data-stack.md) — concept · draft · 10 components of a cloud-native data platform: storage, ingestion, transformation, visualization, version control, orchestration, containers, IaC, data quality, reverse ETL
- [FHIR (Fast Healthcare Interoperability Resources)](/data-engineering/fhir.md) — concept · draft · HL7 standard for healthcare data exchange; Resources as typed forms; REST/Document/Message/Service paradigms; FHIR analytics pipeline patterns
- [OMOP Common Data Model (CDM)](/data-engineering/omop-cdm.md) — concept · draft · OHDSI standard for observational health data analytics; standardized schema + vocabularies; post-ETL analytic tooling (ACHILLES, ATLAS, HADES)
- [Vibe Engineering](/data-engineering/vibe-engineering.md) — concept · draft · building without theoretical framework (Joe Reis); Spolsky's Law of Leaky Abstractions; 2026 DE context; AI as vibe-engineering accelerant

### Entities
- [PostgreSQL](/data-engineering/postgres.md) — entity · draft · relational database as full-stack data platform via extensions (pgvector, pgcron, tsvector, etc.); pgledger double-entry ledger pattern
- [Windsor.ai](/data-engineering/windsor-ai.md) — entity · stub · no-code ETL/ELT platform; 345+ connectors for marketing/business data; LLM AI chat integration
- [Apache Kafka](/data-engineering/kafka.md) — entity · draft · event streaming platform decoupling services via topics, partitions, and consumer groups
- [dbt](/data-engineering/dbt.md) — entity · draft · SQL-first transformation framework; sources vs models; staging/warehouse/marts materializations
- [dbt Fusion Engine](/data-engineering/dbt-fusion.md) — entity · draft · Rust-powered compiler; SDF acquisition Jan 2025; ~30× parse speedup; state-aware orchestration
- [Apache Parquet](/data-engineering/parquet.md) — entity · draft · binary columnar file format; RLE compression; sort-order strategy
- [Apache Iceberg](/data-engineering/apache-iceberg.md) — entity · draft · open table format: ACID, schema evolution, time travel, hidden partitioning
- [Apache Spark](/data-engineering/apache-spark.md) — entity · draft · distributed engine on immutable RDDs + lazy DAG; DataFrames/Catalyst/Tungsten; caching, OOM tuning
- [Databricks](/data-engineering/databricks.md) — entity · draft · lakehouse platform; Unity Catalog, Liquid Clustering, Lakeflow, cost
- [DuckDB](/data-engineering/duckdb.md) — entity · draft · embedded OLAP engine; Quack protocol, DuckLake, MotherDuck; 1TB benchmark; Zonemap index
- [Matthew Housley](/data-engineering/matthew-housley.md) — entity · stub · Data Engineering Fundamentals co-author; CTO Ternary Data; foundations>tools
- [ingestr](/data-engineering/ingestr.md) — entity · stub · Bruin CLI ELT tool; copy any source → any destination, incremental loading
- [Redis](/data-engineering/redis.md) — entity · draft · in-memory store; new 8.8 array type for position-as-data-model (groups of 4096, free gaps, ARRING/ARGREP/AROP)
- [mondayDB](/data-engineering/mondaydb.md) — entity · draft · monday.com's DuckDB-powered columnar HTAP serving layer; CQRS, external WAL, sync-then-query, rendezvous-hash routing
- [Dataform](/data-engineering/dataform.md) — entity · draft · BigQuery-native SQL/JS transformation orchestration (SQLX, ref-DAG, assertions, Git); dbt analogue in GCP
- [Snowflake](/data-engineering/snowflake.md) — entity · draft · managed cloud OLAP; disaggregated storage/compute, virtual warehouses, micro-partitions, work stealing, flexible compute, Unistore
- [ClickHouse](/data-engineering/clickhouse.md) — entity · draft · OLAP column store; MergeTree (LSM-inspired); vectorized execution; Tinybird managed platform
- [BigQuery](/data-engineering/bigquery.md) — entity · draft · Google serverless warehouse; Dremel + Colossus + Borg; Capacitor format (inspired Parquet); shuffle separation
- [Amazon Redshift](/data-engineering/redshift.md) — entity · draft · MPP column store from ParAccel/PostgreSQL; share-nothing→RMS; code specialization (compiled C++) vs vectorization
- [Orchestra](/data-engineering/orchestra.md) — entity · draft · managed declarative Data&AI workflow platform; UI-first; managed integrations, pipelines/tasks/triggers, lineage, env-as-config, Git version control
- [Perspective](/data-engineering/perspective.md) — entity · stub · WebAssembly/Python/Rust interactive analytics component for large+streaming datasets; DuckDB integration; data grid + 10+ chart types

### Syntheses
- [Query-Engine Routing](/data-engineering/query-engine-routing.md) — synthesis · draft · multi-engine routing over Iceberg; SQL-dialect translation; cost-based routing
- [Pipeline Optimization at Scale](/data-engineering/pipeline-optimization-at-scale.md) — synthesis · draft · 3 FAANG war stories (Airbnb 95% backfill, Meta 12× 50TB, Meta silent failure); anti-patterns + fixes
- [The Data Engineer Role](/data-engineering/data-engineer-role.md) — synthesis · draft · value = business impact + technical fundamentals; seniority
- [Claude Code for Data Engineering](/data-engineering/claude-code-for-data-engineering.md) — synthesis · draft · AI-assisted dbt scaffolding; PRD→ERD→dbt modeling (cross-domain → ai-engineering)
- [AI Observability as a Data Pipeline](/data-engineering/ai-observability-data-pipeline.md) — synthesis · draft · AI observability mapped to the DE pipeline model; LLM-judge vs code metrics (cross-domain → ai-engineering)
- [Agentic Data Modeling](/data-engineering/agentic-data-modeling.md) — synthesis · draft · AI agents for schema design & change-impact analysis (OpenMetadata MCP, SchemaFlow, pg_infer) (cross-domain → ai-engineering)
- [Progressive Disclosure for Analytics Agents](/data-engineering/progressive-disclosure-analytics-agents.md) — synthesis · draft · Discover→Understand→Execute; avoid flat-context trap loading whole schema/semantic layer (cross-domain → ai-engineering)
- [AI's Impact on Data Engineering](/data-engineering/ai-impact-on-data-engineering.md) — synthesis · draft · won't replace DEs soon; Markdown Team model: 3 new jobs (determinism, context encoding, kaizen flywheel); DE→platform architect, analyst→research analyst
- [Data Engineering Agents Landscape](/data-engineering/data-engineering-agents-landscape.md) — synthesis · draft · OSS/vendor DE agents by build-time vs consume-time (text-to-SQL): Vanna, WrenAI, Dataherald, Datus-agent, dbt MCP/Agent Skills, Databricks Genie/Lakeflow; solo-DE recommendation (cross-domain → ai-engineering)
- [The Portfolio Project That Lands a DE Role](/data-engineering/portfolio-project-that-lands-a-de-role.md) — synthesis · draft · what makes ONE end-to-end Databricks+AWS showcase impressive to hiring managers: business framing, rigor checklist (medallion/DQ/idempotency/tests/metadata/IaC/cost), realism/ops, defensible stack choices, junior-tell anti-signals
- [Cloud Data Warehouse Internals](/data-engineering/cloud-data-warehouse-internals.md) — synthesis · draft · BigQuery/Snowflake/Databricks/Redshift compared: shared-disk, object storage, hybrid vs column format, vectorization vs code specialization
- [Compute–Storage Decoupling](/data-engineering/compute-storage-decoupling.md) — synthesis · draft · the separate-compute-from-object-storage move as one convergent pattern across cloud warehouses, the lakehouse, and event streaming (tiered/diskless Kafka)

### Source summaries
- [dbt Kimball reference project](/data-engineering/sources/dbt-kimball-project.md) — source · draft · reference dbt Kimball SCD2 project (BigQuery/DuckDB)
- [DuckDB ETL on ECS Fargate](/data-engineering/sources/aws-duckdb-etl-fargate.md) — source · draft · end-to-end AWS ETL (Terraform, EventBridge, Slack observability)
- [SQL Sales-Funnel Analysis project](/data-engineering/sources/sql-funnel-analysis-project.md) — source · draft · end-to-end BigQuery funnel/conversion/AOV-vs-CAC SQL walkthrough
- [Data Engineering Zoomcamp](/data-engineering/sources/data-engineering-zoomcamp.md) — source · draft · free 9-week DataTalksClub course; end-to-end pipeline; Docker/Terraform/Kestra/dbt/BigQuery/Spark/Kafka
- [Skytrax dbt transformation project](/data-engineering/sources/skytrax-dbt-transformation-project.md) — source · draft · end-to-end dbt+Snowflake transformation: Kimball star schema, RBAC-as-Terraform, OIDC keyless auth, slim CI + manifest-state CD, CloudFront-hosted docs
- [dbt Summit 2026 — Speakers & Training](/data-engineering/sources/dbt-summit-2026-speakers.md) — source · draft · notable speakers (Tristan Handy Co-founder+President Fivetran+dbt Labs, Quigley Malcolm/MetricFlow/OSI, Thomas Antonakis, Sarah Levy/Euno); 6 training courses; dbt v2 keynote context

## Sources ingested
- [SCD2 Table Creation with MERGE INTO in Spark and Iceberg](/03_Resources/Articles/scd2-table-creation-merge-into-spark-iceberg.md) — article note, Joseph Machado / Start Data Engineering, 2026-03-13
- [Data Engineering - Just Use Postgres](/03_Resources/Study Notes/Data Engineering - Just Use Postgres.md) — YouTube clip (Modern Webdev, 3 min), 2026-03-16
- [Kafka Tutorial for Beginners - Core Concepts](/03_Resources/Study Notes/Kafka Tutorial for Beginners - Core Concepts.md) — YouTube tutorial (TechWorld with Nana, 18 min), 2025-03-06
- [dbt Data Architecture - Simple Stack Design](/03_Resources/Study Notes/dbt Data Architecture - Simple Stack Design.md) — YouTube tutorial (Kahan Data Solutions, 9 min), 2025-03-06
- [Data Lake Fundamentals - Apache Iceberg and Parquet](/03_Resources/Study Notes/Data Lake Fundamentals - Apache Iceberg and Parquet.md) — YouTube tutorial (59 min), 2026-03-15
- [Dimensional Data Modeling - Idempotent Pipelines and SCD Patterns](/03_Resources/Study Notes/Dimensional Data Modeling - Idempotent Pipelines and SCD Patterns.md) — YouTube lecture (Data with Zach, 78 min), 2026-03-16
- [SQL - Window Functions Reference](/03_Resources/Study Notes/SQL - Window Functions Reference.md) — YouTube reference (17 min), 2026-03-13

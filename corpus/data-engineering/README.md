---
type: hub
domain: data-engineering
status: draft
tags:
  - corpus/data-engineering
  - hub
created: 2026-05-07
updated: 2026-06-15
---

# Data Engineering

Domain covering ETL/ELT pipelines, data modeling, Spark, Iceberg, dbt, orchestration, the lakehouse stack, and data quality. Graduated domain (2026-05-21). Substantially expanded in the 2026-06-11 email-backlog ingest (wave 1) and the 2026-06-15 inbox ingest (wave 2: storage fundamentals, DE best practices, Python, CI/CD, data migration, semantic layer, progressive disclosure, AI's impact on DE).

## Pages

### Concepts
- [[data-engineering/scd2|SCD2 (Slowly Changing Dimension Type 2)]] — concept · draft · history-preserving dimension pattern; valid_from/valid_to + is_current flags
- [[data-engineering/merge-into|MERGE INTO]] — concept · draft · atomic Spark SQL operation combining matched/unmatched/source-only actions in one statement
- [[data-engineering/pipeline-layers|Pipeline Layers]] — concept · draft · staging → warehouse → marts ELT separation pattern; Raw DB vs Analytics DB
- [[data-engineering/data-lake|Data Lake / Lakehouse]] — concept · draft · object-storage lake + open table format metadata wrapper; cost hierarchy; partitioning anti-patterns
- [[data-engineering/idempotent-pipelines|Idempotent Pipelines]] — concept · draft · same-input-same-output guarantee; pitfalls, fixes, and SCD idempotency mapping
- [[data-engineering/dimensional-modeling|Dimensional Modeling]] — concept · draft · fact + dimension tables; SCD types; streak_identifier pattern; when to skip SCD
- [[data-engineering/sql-window-functions|SQL Window Functions]] — concept · draft · ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD, running aggregates; frame clauses; interview reference
- [[data-engineering/data-orchestration|Data Orchestration]] — concept · draft · scheduling vs orchestration vs observability; when cron isn't enough; do you need Airflow
- [[data-engineering/open-table-formats|Open Table Formats]] — concept · draft · DB-independent metadata layer (Iceberg/Delta/Hudi); open data infrastructure
- [[data-engineering/medallion-architecture|Medallion Architecture]] — concept · draft · bronze/silver/gold are lifecycle stages, not a data model; Kimball-vs-Inmon
- [[data-engineering/change-data-capture|Change Data Capture (CDC)]] — concept · draft · full load vs incremental vs CDC; capturing deletes, latency
- [[data-engineering/materialized-views|Materialized Views]] — concept · draft · cross-platform MV synthesis; incremental vs full refresh; limitations
- [[data-engineering/data-quality|Data Quality]] — concept · draft · 6-step clean-warehouse framework; data contracts; schema-aware validation
- [[data-engineering/data-ingestion-patterns|Data Ingestion Patterns]] — concept · draft · two ingestion patterns: stream via event log vs batch extract
- [[data-engineering/incremental-pipeline-design|Incremental Pipeline Design]] — concept · draft · timestamp-driven extraction, model-driven load, parallel backfilling
- [[data-engineering/storage-fundamentals|Storage Fundamentals]] — concept · draft · storage hierarchy; file/block/object; row vs columnar serialisation
- [[data-engineering/data-engineering-best-practices|Data Engineering Best Practices]] — concept · draft · six pipeline best practices: 3-hop, DQ, idempotency, DRY, metadata, tests
- [[data-engineering/python-for-data-engineering|Python for Data Engineering]] — concept · draft · disk vs memory; Python as glue across ETL/DQ/test/orchestrate
- [[data-engineering/de-portfolio-projects|DE Portfolio Projects]] — concept · draft · runnable batch/stream/event-driven projects; stack-comparison matrix
- [[data-engineering/cicd-for-data-infrastructure|CI/CD for Data Infrastructure]] — concept · draft · CI plan→PR, CD apply-dev→human-gate→prod; GitHub Actions + Terraform
- [[data-engineering/data-migration-at-scale|Data Migration at Scale]] — concept · draft · Shadow → Reverse Shadow → Cleanup; row-count/checksum verification; CDC rollback
- [[data-engineering/data-modeling-meaning|Meaning in Data Modeling]] — concept · draft · semantics, taxonomy, ontology, metadata (Joe Reis)
- [[data-engineering/semantic-layer|Semantic Layer]] — concept · draft · metric/knowledge layer as critical AI infra; data teams → context teams; agentic architect
- [[data-engineering/etl-pipeline|ETL Pipeline]] — concept · draft · Extract/Transform/Load; ETL vs ELT vs data pipeline; batch vs streaming; 2026 tools & trends
- [[data-engineering/data-mart|Data Mart]] — concept · draft · community-specific DSS store; Demarest's hybrid warehouse+marting multitiered model; schema explosion
- [[data-engineering/postgresql-views|PostgreSQL Views]] — concept · draft · views as rewrite rules (pg_rewrite macros); inlining, SELECT * trap, security_invoker, schema-evolution pain
- [[data-engineering/graph-databases|Graph Databases (RDF vs LPG)]] — concept · draft · RDF/OWL vs labeled property graph decision framework; index-free adjacency, RDF 1.2, GQL, workload-dependent benchmarks

### Entities
- [[data-engineering/postgres|PostgreSQL]] — entity · draft · relational database as full-stack data platform via extensions (pgvector, pgcron, tsvector, etc.)
- [[data-engineering/kafka|Apache Kafka]] — entity · draft · event streaming platform decoupling services via topics, partitions, and consumer groups
- [[data-engineering/dbt|dbt]] — entity · draft · SQL-first transformation framework; sources vs models; staging/warehouse/marts materializations
- [[data-engineering/parquet|Apache Parquet]] — entity · draft · binary columnar file format; RLE compression; sort-order strategy
- [[data-engineering/apache-iceberg|Apache Iceberg]] — entity · draft · open table format: ACID, schema evolution, time travel, hidden partitioning
- [[data-engineering/apache-spark|Apache Spark]] — entity · draft · distributed engine on immutable RDDs + lazy DAG; DataFrames/Catalyst/Tungsten; caching, OOM tuning
- [[data-engineering/databricks|Databricks]] — entity · draft · lakehouse platform; Unity Catalog, Liquid Clustering, Lakeflow, cost
- [[data-engineering/duckdb|DuckDB]] — entity · draft · embedded OLAP engine; Quack protocol, DuckLake, MotherDuck
- [[data-engineering/ingestr|ingestr]] — entity · stub · Bruin CLI ELT tool; copy any source → any destination, incremental loading
- [[data-engineering/redis|Redis]] — entity · draft · in-memory store; new 8.8 array type for position-as-data-model (groups of 4096, free gaps, ARRING/ARGREP/AROP)
- [[data-engineering/mondaydb|mondayDB]] — entity · draft · monday.com's DuckDB-powered columnar HTAP serving layer; CQRS, external WAL, sync-then-query, rendezvous-hash routing

### Syntheses
- [[data-engineering/query-engine-routing|Query-Engine Routing]] — synthesis · draft · multi-engine routing over Iceberg; SQL-dialect translation; cost-based routing
- [[data-engineering/data-engineer-role|The Data Engineer Role]] — synthesis · draft · value = business impact + technical fundamentals; seniority
- [[data-engineering/claude-code-for-data-engineering|Claude Code for Data Engineering]] — synthesis · draft · AI-assisted dbt scaffolding; PRD→ERD→dbt modeling (cross-domain → ai-engineering)
- [[data-engineering/ai-observability-data-pipeline|AI Observability as a Data Pipeline]] — synthesis · draft · AI observability mapped to the DE pipeline model; LLM-judge vs code metrics (cross-domain → ai-engineering)
- [[data-engineering/agentic-data-modeling|Agentic Data Modeling]] — synthesis · draft · AI agents for schema design & change-impact analysis (OpenMetadata MCP, SchemaFlow, pg_infer) (cross-domain → ai-engineering)
- [[data-engineering/progressive-disclosure-analytics-agents|Progressive Disclosure for Analytics Agents]] — synthesis · draft · Discover→Understand→Execute; avoid flat-context trap loading whole schema/semantic layer (cross-domain → ai-engineering)
- [[data-engineering/ai-impact-on-data-engineering|AI's Impact on Data Engineering]] — synthesis · draft · won't replace DEs soon but raises judgement/semantics; agents as new query consumer

### Source summaries
- [[data-engineering/sources/dbt-kimball-project|dbt Kimball reference project]] — source · draft · reference dbt Kimball SCD2 project (BigQuery/DuckDB)
- [[data-engineering/sources/aws-duckdb-etl-fargate|DuckDB ETL on ECS Fargate]] — source · draft · end-to-end AWS ETL (Terraform, EventBridge, Slack observability)
- [[data-engineering/sources/sql-funnel-analysis-project|SQL Sales-Funnel Analysis project]] — source · draft · end-to-end BigQuery funnel/conversion/AOV-vs-CAC SQL walkthrough

## Sources ingested
- [[03_Resources/Articles/scd2-table-creation-merge-into-spark-iceberg|SCD2 Table Creation with MERGE INTO in Spark and Iceberg]] — article note, Joseph Machado / Start Data Engineering, 2026-03-13
- [[03_Resources/Study Notes/Data Engineering - Just Use Postgres|Data Engineering - Just Use Postgres]] — YouTube clip (Modern Webdev, 3 min), 2026-03-16
- [[03_Resources/Study Notes/Kafka Tutorial for Beginners - Core Concepts|Kafka Tutorial for Beginners - Core Concepts]] — YouTube tutorial (TechWorld with Nana, 18 min), 2025-03-06
- [[03_Resources/Study Notes/dbt Data Architecture - Simple Stack Design|dbt Data Architecture - Simple Stack Design]] — YouTube tutorial (Kahan Data Solutions, 9 min), 2025-03-06
- [[03_Resources/Study Notes/Data Lake Fundamentals - Apache Iceberg and Parquet|Data Lake Fundamentals - Apache Iceberg and Parquet]] — YouTube tutorial (59 min), 2026-03-15
- [[03_Resources/Study Notes/Dimensional Data Modeling - Idempotent Pipelines and SCD Patterns|Dimensional Data Modeling - Idempotent Pipelines and SCD Patterns]] — YouTube lecture (Data with Zach, 78 min), 2026-03-16
- [[03_Resources/Study Notes/SQL - Window Functions Reference|SQL - Window Functions Reference]] — YouTube reference (17 min), 2026-03-13

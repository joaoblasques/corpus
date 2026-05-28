---
type: hub
domain: data-engineering
status: draft
tags:
  - corpus/data-engineering
  - hub
created: 2026-05-07
updated: 2026-05-07
---

# Data Engineering

Domain covering ETL/ELT pipelines, data modeling, Spark, Iceberg, dbt, Airflow, and cloud data infrastructure. Provisional domain — seeded with 1 source; expected to grow via DE101/DataExpert bootcamp material and data engineering playlists.

## Pages

### Concepts
- [[data-engineering/scd2|SCD2 (Slowly Changing Dimension Type 2)]] — concept · draft · history-preserving dimension pattern; valid_from/valid_to + is_current flags
- [[data-engineering/merge-into|MERGE INTO]] — concept · draft · atomic Spark SQL operation combining matched/unmatched/source-only actions in one statement
- [[data-engineering/pipeline-layers|Pipeline Layers]] — concept · draft · staging → warehouse → marts ELT separation pattern; Raw DB vs Analytics DB
- [[data-engineering/data-lake|Data Lake / Lakehouse]] — concept · draft · object-storage lake + open table format metadata wrapper; cost hierarchy; partitioning anti-patterns
- [[data-engineering/idempotent-pipelines|Idempotent Pipelines]] — concept · draft · same-input-same-output guarantee; pitfalls, fixes, and SCD idempotency mapping
- [[data-engineering/dimensional-modeling|Dimensional Modeling]] — concept · draft · fact + dimension tables; SCD types; streak_identifier pattern; when to skip SCD
- [[data-engineering/sql-window-functions|SQL Window Functions]] — concept · draft · ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD, running aggregates; frame clauses; interview reference

### Entities
- [[data-engineering/postgres|PostgreSQL]] — entity · draft · relational database as full-stack data platform via extensions (pgvector, pgcron, tsvector, etc.)
- [[data-engineering/kafka|Apache Kafka]] — entity · draft · event streaming platform decoupling services via topics, partitions, and consumer groups
- [[data-engineering/dbt|dbt]] — entity · draft · SQL-first transformation framework; sources vs models; staging/warehouse/marts materializations
- [[data-engineering/parquet|Apache Parquet]] — entity · draft · binary columnar file format; RLE compression; sort-order strategy
- [[data-engineering/apache-iceberg|Apache Iceberg]] — entity · draft · open table format: ACID, schema evolution, time travel, hidden partitioning

## Sources ingested
- [[03_Resources/Articles/scd2-table-creation-merge-into-spark-iceberg|SCD2 Table Creation with MERGE INTO in Spark and Iceberg]] — article note, Joseph Machado / Start Data Engineering, 2026-03-13
- [[03_Resources/Study Notes/Data Engineering - Just Use Postgres|Data Engineering - Just Use Postgres]] — YouTube clip (Modern Webdev, 3 min), 2026-03-16
- [[03_Resources/Study Notes/Kafka Tutorial for Beginners - Core Concepts|Kafka Tutorial for Beginners - Core Concepts]] — YouTube tutorial (TechWorld with Nana, 18 min), 2025-03-06
- [[03_Resources/Study Notes/dbt Data Architecture - Simple Stack Design|dbt Data Architecture - Simple Stack Design]] — YouTube tutorial (Kahan Data Solutions, 9 min), 2025-03-06
- [[03_Resources/Study Notes/Data Lake Fundamentals - Apache Iceberg and Parquet|Data Lake Fundamentals - Apache Iceberg and Parquet]] — YouTube tutorial (59 min), 2026-03-15
- [[03_Resources/Study Notes/Dimensional Data Modeling - Idempotent Pipelines and SCD Patterns|Dimensional Data Modeling - Idempotent Pipelines and SCD Patterns]] — YouTube lecture (Data with Zach, 78 min), 2026-03-16
- [[03_Resources/Study Notes/SQL - Window Functions Reference|SQL - Window Functions Reference]] — YouTube reference (17 min), 2026-03-13

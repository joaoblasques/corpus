---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/pdf/pdf-the-10-mds-components.md
    channel: pdf
    ingested_at: 2026-06-25
aliases:
  - modern data stack
  - MDS
  - MDS components
  - 10 MDS components
  - reverse ETL
  - modern data architecture
tags:
  - corpus/data-engineering
  - concept
created: 2026-06-25
updated: 2026-06-25
---

# Modern Data Stack (MDS) — The 10 Components

**TL;DR.** The Modern Data Stack is a set of 10 architectural components that together form a complete cloud-native data platform [^src1]. The first 5 are **essentials** (Storage & Databases, Ingestion, Transformation, Visualization/Analytics, Version Control & CI/CD); the next 5 are **advanced** (Orchestration, Containers, Infrastructure as Code, Data Quality, Reverse ETL) [^src1]. Understanding all 10 tells you where any new tool fits and why it matters.

## The 5 essential components

### 1. Storage & Databases

Store data objects from source systems in any format in a cloud server [^src1]:

- **Storage** (Data Lake): centralized landing zone, split by temperature (hot/warm/cold) for cost, flexible file types (CSV, Parquet, JSON, XML)
  - Tools: S3, Azure Blob, Google Cloud Storage
- **Databases** (Data Warehouse): single source of truth + business logic, well-defined query languages (SQL), structured and performant
  - Tools: Snowflake, Databricks, BigQuery (warehouses); MySQL, Postgres, SQL Server (OLTP); MongoDB, Cassandra (NoSQL)

See [[data-engineering/data-lake|Data Lake]] and [[data-engineering/cloud-data-warehouse-internals|Cloud Data Warehouse Internals]].

### 2. Ingestion

Extract data from various sources and load it into a consolidated landing zone [^src1]:

- **Batch** (scheduled) or **streaming** (real-time) extraction
- Tools with pre-built connectors (Fivetran, Stitch, Airbyte) vs custom Python scripts
- Streaming: Apache Kafka, Kinesis, Debezium
- Destination: data lake or staging area (ETL vs ELT)

See [[data-engineering/data-ingestion-patterns|Data Ingestion Patterns]], [[data-engineering/change-data-capture|Change Data Capture]], [[data-engineering/kafka|Kafka]].

### 3. Transformation

Turn raw loaded data into clean, organized data ready for analytics [^src1]:

- Occurs *after* data is already loaded (ELT), or during ingestion (streaming ETL)
- Code-based tools (dbt) or custom scripts (Python, stored procedures)
- Big data processing (Apache Spark)
- Applies real-world rules: filtering, aggregation, standardization, schema conformance
- Languages: SQL, Python, Jinja; File types: CSV, Parquet, JSON, YAML

See [[data-engineering/data-transformation|Data Transformation]], [[data-engineering/dbt|dbt]], [[data-engineering/apache-spark|Apache Spark]].

### 4. Reporting & Analytics / Visualization

Provides insights from transformed data for better decision-making [^src1]:

- BI tools connect to the warehouse/data marts; may add extra logic
- Tools: Power BI, Looker, Tableau (commercial); Metabase, Apache Superset (open-source)
- ML tools can also sit here
- Languages: SQL, Python, R

See [[data-engineering/bi-as-code|BI as Code]], [[data-engineering/semantic-layer|Semantic Layer]].

### 5. Version Control & CI/CD

Monitor all code changes and automate deployment [^src1]:

- **Version Control**: Git (local) + hosted platforms (GitHub, GitLab, Bitbucket) — revert changes, transparency, avoid conflicts
- **CI/CD**: event-triggered automation (vs schedule-based orchestration) — faster to production, removes manual steps
- Typically YAML-configured (GitHub Actions)

See [[data-engineering/cicd-for-data-infrastructure|CI/CD for Data Infrastructure]].

## The 5 advanced components

### 6. Orchestration

Connect and trigger different parts of a pipeline through a single tool [^src1]:

- Without a central orchestrator, pipelines become hard to manage ("overwhelming to stay in control")
- Orchestrators let you monitor and control at a high level from one location
- **Key distinction from CI/CD**: orchestration is schedule-based (or dependency-based); CI/CD is event-based
- Tools: Airflow, Prefect, Dagster, Luigi (pure orchestration); Kubernetes, OpenShift (container orchestration); Jenkins (CI/CD can double as orchestration); SQL Agent Job, SSIS (server-based)
- Languages: Python, Bash/Zsh; YAML

See [[data-engineering/data-orchestration|Data Orchestration]].

### 7. Containers

Isolated virtual OS instances for running applications and processes [^src1]:

- Create specific runtime environments for automated processes
- Host open-source tools without installing system dependencies
- Create/drop easily for CI/CD automation
- Tool: Docker (dominant); language: Bash/Zsh + Dockerfile + YAML

### 8. Infrastructure as Code (IaC)

Create and manage cloud resources with version-controlled code, rather than manually [^src1]:

- Automate deployments, updates, onboarding
- Manage roles, permissions, and configurations for cloud platforms
- Ensures consistency; reduces manual steps; improves maintenance
- Tools: **Terraform** (primary), Ansible; cloud-native: AWS CloudFormation, Azure Resource Manager, GCP Deployment Manager
- Languages: Bash/Zsh, Python; Terraform `.tf` files, YAML/JSON

See [[data-engineering/cicd-for-data-infrastructure|CI/CD for Data Infrastructure]].

### 9. Data Quality

Ensure data accuracy, completeness, consistency, and reliability [^src1]:

- **Implementation paths**: automated testing at pipeline stages, code linters, data contracts with producers, documentation + lineage, data catalogs
- **Why it matters**: catches errors before reaching end users; provides consistency and confidence in data; enables efficient development
- DQ tools: dbt tests, Great Expectations, SQLFluff, PyLint
- Catalog/observability tools: DataHub, Atlan, Castor, Collibra (catalogs); Monte Carlo, Amundsen (observability)
- Languages: SQL, Python, Bash/Zsh; YAML

See [[data-engineering/data-quality|Data Quality]], [[data-engineering/data-observability|Data Observability]].

### 10. Reverse ETL

Sync data from a central data warehouse **back** to operational tools (SaaS apps, CRMs, etc.) [^src1]:

- Often the last step in the data pipeline, after warehouse is updated
- Helps business users stay in tools they know while benefiting from warehouse-derived insights
- Avoids conflicting data between apps; offloads technical requirements
- Tools: **Census**, **Hightouch**, Rudderstack
- Languages: SQL, Bash/Zsh; YAML

**Gotcha**: Reverse ETL is conceptually the inverse of ingestion — it "closes the loop" by sending analytics results back to source-of-record operational systems. It is distinct from the ETL pipeline's load step [^src1].

## Architecture flow

The 10 components map to a layered architecture [^src1]:

```
Sources → Data Lake → Data Warehouse → Data Models → Analytics/BI
  ↕           ↕             ↕               ↕
Ingestion  Transform    Data Quality   Visualization

                    Orchestration (connects all)
         CI/CD  ·  Containers  ·  IaC  (cross-cutting)
                      ↓ (Reverse ETL)
                  Business Apps
```

## Where tools fit

| MDS Layer | Example tools |
|---|---|
| Storage (lake) | S3, Azure Blob, GCS |
| Storage (warehouse) | Snowflake, BigQuery, Databricks, Redshift |
| Ingestion | Fivetran, Airbyte, Stitch, Debezium, Kafka |
| Transformation | dbt, Apache Spark, AWS Glue, Azure Data Factory |
| Visualization | Power BI, Looker, Tableau, Metabase, Superset |
| Version Control | GitHub, GitLab, Bitbucket |
| CI/CD | GitHub Actions, Jenkins |
| Orchestration | Airflow, Prefect, Dagster, Luigi |
| Containers | Docker |
| IaC | Terraform, Ansible, CloudFormation |
| Data Quality | Great Expectations, dbt tests, SQLFluff |
| Reverse ETL | Census, Hightouch, Rudderstack |

## Related

- [[data-engineering/etl-pipeline|ETL Pipeline]] — the Extract-Transform-Load pattern (MDS component interaction)
- [[data-engineering/data-ingestion-patterns|Data Ingestion Patterns]] — ingestion layer in depth
- [[data-engineering/medallion-architecture|Medallion Architecture]] — bronze/silver/gold within the storage + transformation layers
- [[data-engineering/data-orchestration|Data Orchestration]] — the orchestration component
- [[data-engineering/data-quality|Data Quality]] — the DQ component
- [[data-engineering/cicd-for-data-infrastructure|CI/CD for Data Infrastructure]] — CI/CD and IaC components
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [The 10 MDS Components (Michael)](../../raw/pdf/pdf-the-10-mds-components.md)

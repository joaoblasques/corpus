---
type: source
domain: data-engineering
status: draft
sources:
  - path: raw/web/github-datatalksclub-data-engineering-zoomcamp-data-engineer.md
    channel: web
    ingested_at: 2026-06-19
aliases:
  - Data Engineering Zoomcamp
  - DataTalksClub Zoomcamp
  - DE Zoomcamp
tags:
  - corpus/data-engineering
  - source
created: 2026-06-19
updated: 2026-06-19
---

# Source: Data Engineering Zoomcamp (DataTalksClub)

**What it is.** A **free, 9-week** data-engineering course by **DataTalksClub** (Alexey Grigorev) that teaches the fundamentals by **building an end-to-end data pipeline from scratch** with industry-standard tools [^src1]. Structured modules + hands-on workshops + a final project; aimed at developers, analysts, and data scientists with **basic coding + SQL** (Python helpful, not required); no prior DE experience needed [^src1].

## Format

Two ways to take it [^src1]:

- **Live cohort** (next start January 2027) — pre-recorded lectures, **graded** homework, leaderboard, peer review, and a **certificate** on completing the final project. "Live" means deadlines/community, *not* live classes [^src1].
- **Self-paced** (anytime) — same materials, homework available but unscored, no certificate [^src1].

Both are free and open-source [^src1].

## Curriculum (tool map)

The syllabus is a good index of the modern DE stack [^src1]:

- **Containerization & IaC** — intro to GCP, Docker & Docker Compose, PostgreSQL in Docker, infrastructure setup with **[[mlops/terraform|Terraform]]** [^src1].
- **Workflow orchestration** — data lakes + orchestration with **Kestra** [^src1]. (See [[data-engineering/data-orchestration|Data Orchestration]].)
- **Ingestion** — API reading, pipeline scalability, data normalization, incremental loading [^src1]. (See [[data-engineering/incremental-pipeline-design|Incremental Pipeline Design]].)
- **Data warehouse** — **[[data-engineering/bigquery|BigQuery]]**: partitioning, clustering, best practices, ML in BigQuery [^src1].
- **Analytics engineering** — **[[data-engineering/dbt|dbt]]** with **[[data-engineering/duckdb|DuckDB]]** & BigQuery; testing, documentation, deployment [^src1].
- **End-to-end with Bruin** — ingestion, transformation, data quality, deployment to BigQuery [^src1]. (Bruin/ingestr — see [[data-engineering/ingestr|ingestr]].)
- **Batch processing** — **[[data-engineering/apache-spark|Apache Spark]]**: DataFrames & SQL, internals of GroupBy and Joins [^src1].
- **Streaming** — **[[data-engineering/kafka|Kafka]]**: Kafka Streams & KSQL, schema management with Avro [^src1]. (See [[data-engineering/stream-processing|Stream Processing]].)
- **Final project** — applies all concepts end-to-end, with peer review [^src1].

## Why it's notable

A widely-recommended free entry point into data engineering, emphasizing **fundamentals and principles over ever-evolving tools** (a learner testimonial), with a hands-on, build-a-pipeline structure and an active Slack community [^src1]. Fits the [[data-engineering/data-engineer-role|"learn concepts, not tools"]] thesis and gives a concrete portfolio project (see [[data-engineering/de-portfolio-projects|DE Portfolio Projects]]).

## Related

- [[data-engineering/data-engineer-role|The Data Engineer Role]] — the fundamentals-first learning path this course embodies
- [[data-engineering/de-portfolio-projects|DE Portfolio Projects]] — the final project as a portfolio piece
- [[data-engineering/data-engineering-interview|Data Engineering Interview]] — the skills the curriculum builds
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [DataTalksClub/data-engineering-zoomcamp (course README)](../../raw/web/github-datatalksclub-data-engineering-zoomcamp-data-engineer.md)

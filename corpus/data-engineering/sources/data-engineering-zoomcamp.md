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

- **Containerization & IaC** — intro to GCP, Docker & Docker Compose, PostgreSQL in Docker, infrastructure setup with **[Terraform](/mlops/terraform.md)** [^src1].
- **Workflow orchestration** — data lakes + orchestration with **Kestra** [^src1]. (See [Data Orchestration](/data-engineering/data-orchestration.md).)
- **Ingestion** — API reading, pipeline scalability, data normalization, incremental loading [^src1]. (See [Incremental Pipeline Design](/data-engineering/incremental-pipeline-design.md).)
- **Data warehouse** — **[BigQuery](/data-engineering/bigquery.md)**: partitioning, clustering, best practices, ML in BigQuery [^src1].
- **Analytics engineering** — **[dbt](/data-engineering/dbt.md)** with **[DuckDB](/data-engineering/duckdb.md)** & BigQuery; testing, documentation, deployment [^src1].
- **End-to-end with Bruin** — ingestion, transformation, data quality, deployment to BigQuery [^src1]. (Bruin/ingestr — see [ingestr](/data-engineering/ingestr.md).)
- **Batch processing** — **[Apache Spark](/data-engineering/apache-spark.md)**: DataFrames & SQL, internals of GroupBy and Joins [^src1].
- **Streaming** — **[Kafka](/data-engineering/kafka.md)**: Kafka Streams & KSQL, schema management with Avro [^src1]. (See [Stream Processing](/data-engineering/stream-processing.md).)
- **Final project** — applies all concepts end-to-end, with peer review [^src1].

## Why it's notable

A widely-recommended free entry point into data engineering, emphasizing **fundamentals and principles over ever-evolving tools** (a learner testimonial), with a hands-on, build-a-pipeline structure and an active Slack community [^src1]. Fits the ["learn concepts, not tools"](/data-engineering/data-engineer-role.md) thesis and gives a concrete portfolio project (see [DE Portfolio Projects](/data-engineering/de-portfolio-projects.md)).

## Related

- [The Data Engineer Role](/data-engineering/data-engineer-role.md) — the fundamentals-first learning path this course embodies
- [DE Portfolio Projects](/data-engineering/de-portfolio-projects.md) — the final project as a portfolio piece
- [Data Engineering Interview](/data-engineering/data-engineering-interview.md) — the skills the curriculum builds
- [Data Engineering hub](/data-engineering/README.md)

---

[^src1]: [DataTalksClub/data-engineering-zoomcamp (course README)](../../../raw/web/github-datatalksclub-data-engineering-zoomcamp-data-engineer.md)

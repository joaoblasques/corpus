---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/email/email-2025-11-12-10-data-engineering-projects-for-your-portfolio.md
    channel: email
    ingested_at: 2026-06-15
  - path: raw/web/data-engineering-projects-start-data-engineering.md
    channel: web
    ingested_at: 2026-06-15
  - path: raw/web/build-data-engineering-projects-with-free-template-start-dat.md
    channel: web
    ingested_at: 2026-06-19
  - path: raw/web/designing-a-data-project-to-impress-hiring-managers-start-da.md
    channel: web
    ingested_at: 2026-06-19
  - path: raw/email/email-2025-08-06-set-up-your-next-data-engineering-project-with-this-free-tem.md
    channel: email
    ingested_at: 2026-06-19
  - path: raw/email/email-2025-07-16-setting-up-a-local-dev-environment-using-docker.md
    channel: email
    ingested_at: 2026-06-19
aliases:
  - data engineering projects
  - portfolio projects
  - DE projects
tags:
  - corpus/data-engineering
  - concept
created: 2026-06-15
updated: 2026-06-19
---

# DE Portfolio Projects

**TL;DR.** A curated set of runnable data-engineering projects spanning **batch, streaming, and event-driven** paradigms, designed so the hardest part — setting up data infrastructure — is solved for you (all run on GitHub Codespaces or locally with Docker) [^src1]. A portfolio signals to employers an ability to *learn, adapt, and build pipelines from scratch*, following best practices: version control, standard code organisation, testing/DQ checks, and in-demand tools [^src2].

## Why projects matter

Data infra is "notoriously hard to set up," which blocks practice [^src1]. These templates remove setup friction so you can try a tool/framework, see code changes' impact quickly, and showcase expertise [^src1]. (Apply the [[data-engineering/data-engineering-best-practices|best practices]] within each.)

## Batch pipelines

Each project mixes a source, destination, scheduler, orchestrator, processor, DQ, storage, viz, monitoring, CI/CD, IaC, testing, and linting — useful as a **stack-comparison matrix** [^src1]:

| Project | Source → Dest | Orchestrator | Processor | DQ |
|---|---|---|---|---|
| `bitcoin_monitor` | CoinCap API → Postgres | Python native (cron) | stdlib | — |
| `simple_dbt_project` | CSV → DuckDB | [[data-engineering/dbt|dbt]] | DuckDB | dbt tests |
| `cost_effective_data_pipelines` | sqlite3 (TPC-H) → DuckDB | Python native | [[data-engineering/duckdb|DuckDB]] | — |
| `data_engineering_project_template` | CoinCap API → DuckDB | Airflow | Python + DuckDB | Cuallee |
| `beginner_de_project` | CSV/Postgres → DuckDB | Airflow | [[data-engineering/apache-spark|Spark]] + DuckDB | Cuallee |
| `rainforest` | Postgres → cloud storage | Spark DAG | Spark | Great Expectations |

Common production tooling across the richer projects: Minio (open-source S3), Quarto/Metabase viz, Prometheus+Grafana monitoring, GitHub Actions CI/CD, Terraform IaC, pytest, and black/isort/mypy/flake8 [^src1].

## Stream pipelines

`beginner_de_project_stream` — Postgres tables → Postgres + [[data-engineering/kafka|Kafka]]; a continuously-running stream orchestrated by an **Apache Flink** DAG, Flink as processor, Flink UI + Grafana viz, Prometheus/Grafana monitoring [^src1].

## Event-driven pipelines

- **CDC with Kafka and Debezium** — Postgres insert/update/delete events → DuckDB via Debezium reading the WAL + Kafka Connect + S3 sink [^src1]. See [[data-engineering/change-data-capture|Change Data Capture]].
- **End-to-end test simulating AWS Lambda** — CSV on SFTP → Postgres, triggered by S3 inserts; tested with `moto` + pytest [^src1].

## LLM / RAG pipeline

A retrieval-augmented-generation pipeline (`data_helper`) is also provided, bridging DE and AI workloads [^src1]. (RAG itself is owned by [[ai-engineering/rag|ai-engineering/RAG]].)

## "Show, don't tell" — make a hiring manager *look*

Building the project is only half the job; getting a hiring manager to read your GitHub is harder, and you get seconds, not minutes [^src4]. Work backward from the goal *"impress the hiring manager"* and optimize for **show not tell** [^src4]:

- **Host a live dashboard fed by near-real-time data** (the `bitcoin_monitor` reference pulls CoinCap every 5 min into Postgres/warehouse, served via Metabase) and **link its public URL from your resume and LinkedIn** — the end product is visible without reading code [^src4].
- Make the repo legible: a **concise README** (problem description, architecture diagram, setup), clear project organization, and coding best practices on display — **tests, lint, types, formatting** [^src4].
- Don't expect anyone to read the codebase; lead with the dashboard and the architecture diagram [^src4].

This is the same instinct the [[data-engineering/portfolio-project-that-lands-a-de-role|portfolio synthesis]] generalizes into a full rigor checklist.

### The dev-workflow toolchain these templates standardize on

Every template ships the same "set up data infra with code" workflow so new features deploy quickly [^src3][^src5]: **Docker + Docker Compose** for local dev, **[[mlops/terraform|Terraform]]** for IaC, **GitHub Actions** for CI/CD, **pytest** for testing, **isort + black** for formatting, **flake8** for lint, **mypy** for type checks, and a **Makefile** of command aliases [^src3]. The free starter template runs an **Airflow + Postgres + Metabase** stack on AWS with **yoyo-migrations** (a lightweight Alembic alternative) for DB changes [^src5]. CI runs the format/lint/type/test gate on each PR; CD copies merged code to an EC2 Docker host — see [[data-engineering/cicd-for-data-infrastructure|CI/CD for Data Infrastructure]] [^src3].

*Why* standardize the local environment with Docker: most data pipelines touch multiple systems, which makes a local dev setup hard; good **developer ergonomics** (reproducible Docker environment + automated formatting/lint/tests) reduce bugs, keep morale high, and increase development velocity [^src6].

## How to use

Run on Codespaces (fork → "Create codespace" → `make up` → open the exposed UI port) or locally with Docker (≥4 GB RAM); the recommended order goes least → most complex [^src1]. The Docker images are not production-optimised — for learning only [^src1].

## Related

- [[data-engineering/data-engineering-best-practices|Data Engineering Best Practices]] — the practices these projects embody
- [[data-engineering/python-for-data-engineering|Python for Data Engineering]] — the language glue
- [[data-engineering/change-data-capture|Change Data Capture]] · [[data-engineering/dbt|dbt]] · [[data-engineering/duckdb|DuckDB]]
- [[data-engineering/data-engineer-role|The Data Engineer Role]] — portfolio as a career signal; see the DA→DE transition section for the simpler SQL+cron starting point before tackling these templates
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [10 Data Engineering Projects (Start Data Engineering)](../../raw/web/data-engineering-projects-start-data-engineering.md)
[^src2]: [10 Data Engineering Projects For Your Portfolio! (newsletter)](../../raw/email/email-2025-11-12-10-data-engineering-projects-for-your-portfolio.md)
[^src3]: [Build Data Engineering Projects with a Free Template](../../raw/web/build-data-engineering-projects-with-free-template-start-dat.md)
[^src4]: [Designing a Data Project to Impress Hiring Managers](../../raw/web/designing-a-data-project-to-impress-hiring-managers-start-da.md)
[^src5]: [Set up your next data engineering project with this free template! (Start Data Engineering)](../../raw/email/email-2025-08-06-set-up-your-next-data-engineering-project-with-this-free-tem.md)
[^src6]: [Setting up a local dev environment using Docker (Start Data Engineering)](../../raw/email/email-2025-07-16-setting-up-a-local-dev-environment-using-docker.md)

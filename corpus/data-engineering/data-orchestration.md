---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/web/why-use-apache-airflow-or-any-orchestrator-start-data-engine.md
    channel: web
    ingested_at: 2026-06-11
  - path: raw/email/email-2025-11-19-do-you-really-need-apache-airflow.md
    channel: email
    ingested_at: 2026-06-11
  - path: raw/email/email-2025-08-07-de-101-8-orchestrators-and-schedulers.md
    channel: email
    ingested_at: 2026-06-19
  - path: raw/email/email-2025-05-22-how-to-choose-between-batch-and-stream-processing.md
    channel: email
    ingested_at: 2026-06-19
  - path: raw/github/github-joaoblasques-data-pipeline-orchestration-kestra.md
    channel: github
    ingested_at: 2026-06-25
aliases:
  - Airflow
  - Apache Airflow
  - orchestrator
  - orchestration
  - scheduling
  - Dagster
  - Prefect
  - Kestra
tags:
  - corpus/data-engineering
  - concept
created: 2026-06-11
updated: 2026-06-25
last_confirmed: 2026-06-25
---

# Data Orchestration

**TL;DR**: A data pipeline needs three capabilities — **scheduling** (run at a frequency), **orchestration** (run tasks in a defined dependency order, in the right place), and **observability** (logs, metadata, history, re-runs) [^src1][^src3]. `cron` covers only the first. An orchestrator like Apache Airflow (or Dagster) bundles all three, which is why teams reach for one as pipeline complexity and team size grow — even though it is overkill for a single simple script [^src1][^src2].

## The three concerns

| Concern | What it solves | What a bare script / cron gives you |
|---|---|---|
| **Scheduling** | Run a pipeline at a specified frequency — hourly/daily/monthly, or complex ("2nd Tuesday of every month") | cron handles fixed frequencies only [^src1][^src2] |
| **Orchestration** | Define the *order* of execution: which tasks run in parallel vs. sequentially, dependencies, retries, branching, dynamic task generation, and *where* each task runs | You hand-roll all of it [^src1] |
| **Observability** | Logs + metadata DB capturing current and historical pipeline state; UI for progress, performance, manual re-runs, connections/variables, access control | You build logging/monitoring yourself [^src1] |

## Do you need Airflow?

The framing question: *why use Airflow vs. just cron / a plain Python request?* [^src2] The answer is **not** the schedule — it is everything around it. As pipeline complexity and team size grow, an orchestrator provides a cleaner way to get scheduling + ordering + observability than re-implementing each feature by hand [^src1]. For a single simple pipeline, Airflow is acknowledged to be **overkill** [^src1].

Heuristic: if you only need "run this one script every day" with no inter-task dependencies and no shared operational visibility, cron is enough. Reach for an orchestrator when you have multiple dependent tasks, need parallelism, need retry/backfill semantics, or need a team to observe and re-run pipelines.

### Airflow alternatives

Airflow is the most common orchestrator, but two alternatives recur for batch scheduling [^src4]: **Dagster** brings type safety and **asset-driven** design (easier dependency management and testing), and **Prefect** focuses on simplicity and observability with a Python-native interface for small-to-mid-scale jobs [^src4]. Managed/declarative orchestrators also exist — see [Orchestra](/data-engineering/orchestra.md) (UI-first, fully managed integrations).

## How Airflow implements each concern

### Scheduling
A **Scheduler** process checks every DAG roughly every minute to decide whether it should start; schedules are cron-format or custom reusable timetables [^src1].

### Orchestration via the DAG
A data pipeline is modeled as a **Directed Acyclic Graph (DAG)** — tasks (nodes) connected by dependency edges, with no cycles [^src1].

- **DAG** = the whole pipeline; **Task** = a node; **Dependency** = an edge; **upstream/downstream** = tasks before/after a given task [^src1].
- Dependencies are declared with the `>>` operator, supporting parallel and sequential chains [^src1]:

```python
create_s3_bucket >> [user_purchase_to_s3, movie_review_to_s3]
movie_review_to_s3 >> movie_classifier >> get_movie_review_to_warehouse
```

- Per-task settings: retries, trigger rules, branch logic, and dynamically generated tasks [^src1].
- **Executors** decide *where* tasks run: `Local`/`Sequential` (same machine as scheduler), `Celery` (task queue across machines), `Kubernetes` (each task as a k8s pod), or custom [^src1].
- **Operators** are reusable connectors to external systems (e.g., `S3CreateBucketOperator`, `SqlToS3Operator`, `LocalFilesystemToS3Operator`) so you write less glue code [^src1].

### Observability
All run information is stored in a metadata DB and as logs, giving current + historical state [^src1]. The web UI surfaces progress, failures, per-task logs and inputs, performance metrics (run time, queue wait), manual DAG triggering/re-runs with custom inputs, reusable variables/connections, and role-based access control [^src1].

## Relation to dbt

Orchestration is a *different layer* from transformation: an orchestrator schedules and sequences pipeline steps (including invoking [dbt](/data-engineering/dbt.md) runs), while dbt handles the in-warehouse "T". Note dbt and Elementary also offer **data observability** at the dataset/quality level — distinct from the pipeline-execution observability an orchestrator provides. See [dbt](/data-engineering/dbt.md).

## Kestra: event-driven workflow orchestration

**Kestra** is an open-source workflow orchestration platform with a YAML-first configuration model, launched via Docker Compose [^src5]. Its positioning: make orchestration accessible without the heavy Python DAG overhead of Airflow, by expressing workflows as declarative YAML flows with triggers and tasks.

**Core Kestra concepts** [^src5]:
- **Flows** — YAML workflow definitions (comparable to Airflow DAGs)
- **Tasks** — individual pipeline steps within a flow (download, transform, load)
- **Triggers** — schedule or event-based triggers for flow execution
- **Backfill** — re-running a flow for historical time periods; Kestra supports parametrized backfill runs

**Why separate pipeline steps** (the motivating rationale) [^src5]: a monolithic script that downloads data and inserts it into a DB has problems — if insertion fails, the download must be repeated; testing requires re-downloading every time; adding retry/fail-safe logic per stage is cumbersome. Splitting into discrete tasks (one for download, one for insert) lets each step be retried or skipped independently.

**Typical Kestra pipeline structure** [^src5]:
```yaml
# Simplified Kestra flow example
id: load-data-to-bigquery
namespace: company.data
tasks:
  - id: download
    type: io.kestra.plugin.core.http.Download
    uri: "{{inputs.url}}"
  - id: load_to_gcs
    type: io.kestra.plugin.gcp.gcs.Upload
    from: "{{outputs.download.uri}}"
    to: "gs://bucket/data.csv"
  - id: load_to_bigquery
    type: io.kestra.plugin.gcp.bigquery.Load
    from: "{{outputs.load_to_gcs.uri}}"
    destinationTable: "project.dataset.table"
triggers:
  - id: daily
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "0 6 * * *"
```

**Backfill pattern** [^src5]: adding a `backfill_start_date` parameter to the flow allows re-running from a historical date, with Kestra executing one flow per time window automatically.

**Integration profile** [^src5]: topics include BigQuery, Docker, data-warehouse, orchestration, tutorial — typical starter stack (GCS + BigQuery + Kestra) for cloud ETL pipelines. Launch Kestra locally:
```bash
docker-compose up -d
# UI accessible at localhost:8080
```

See [Data Engineering Zoomcamp](/data-engineering/sources/data-engineering-zoomcamp.md) where Kestra is used as the orchestration layer.

## See also

- [dbt](/data-engineering/dbt.md) — transformation layer typically invoked by an orchestrated task
- [Orchestra](/data-engineering/orchestra.md) — managed, declarative, UI-first orchestrator alternative
- [Idempotent Pipelines](/data-engineering/idempotent-pipelines.md) — a precondition for safe retries/backfills
- [Pipeline Layers](/data-engineering/pipeline-layers.md)
- [Data Engineering hub](/data-engineering/README.md)

---

[^src1]: [Why use Apache Airflow (or any orchestrator)?](../../raw/web/why-use-apache-airflow-or-any-orchestrator-start-data-engine.md)
[^src2]: [Do you really need Apache Airflow?](../../raw/email/email-2025-11-19-do-you-really-need-apache-airflow.md)
[^src3]: [[DE 101] #8 - Orchestrators and Schedulers (Start Data Engineering)](../../raw/email/email-2025-08-07-de-101-8-orchestrators-and-schedulers.md)
[^src4]: [How to Choose Between Batch and Stream Processing? (Pipeline to Insights)](../../raw/email/email-2025-05-22-how-to-choose-between-batch-and-stream-processing.md)
[^src5]: [Workflow Orchestration with Kestra (joaoblasques/data-pipeline-orchestration-kestra)](../../raw/github/github-joaoblasques-data-pipeline-orchestration-kestra.md)

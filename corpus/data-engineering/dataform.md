---
type: entity
domain: data-engineering
status: draft
sources:
  - path: raw/youtube/youtube-285hnxl9-rk.md
    channel: youtube
    ingested_at: 2026-06-17
aliases:
  - Dataform
  - dataform
  - SQLX
  - sqlx
  - Dataform in GCP
tags:
  - corpus/data-engineering
  - entity
created: 2026-06-17
updated: 2026-06-17
---

# Dataform

**TL;DR.** Dataform is an open-source framework, now native to Google Cloud, for **managing and orchestrating SQL-based transformations in BigQuery** — building, testing, and deploying data pipelines using SQL and JavaScript [^src1]. It is the BigQuery-native analogue of [dbt](/data-engineering/dbt.md): it turns a folder of SQL into a dependency-managed DAG, adds Git version control, automated code validation, and data-quality assertions, and runs transformations as a BigQuery service account [^src1]. Its goal is stated as going "from no dependencies between queries other than time of execution, to data pipelines with dependencies maintained in a git repository" [^src1].

## SQLX — the core file format

Dataform's primary authoring unit is **SQLX**, an open-source extension of SQL that adds features "making development faster, more reliable, and scalable" [^src1]. A SQLX file has two parts [^src1]:

- **`config` block** — responsible for dependency management, automated data-quality testing (assertions), and data documentation. Declares the object `type` (`table`, `view`, `assertion`, etc.) and can override the output table name.
- **SQL part** — the actual query / transformation.

Dependencies between objects are declared with a `${ref("name")}` notation inside the SQL; Dataform builds a **dependency tree (DAG)** from these refs that determines execution order [^src1]. The compiled graph must be a DAG — cycles are rejected [^src1]. Dependencies can also be declared manually in the config's `dependencies` array, which is required for statements (e.g. `DELETE`) that reference a table without an explicit `ref` [^src1].

JavaScript extends SQLX with three reuse levels [^src1]:
1. **Within one file** — encapsulate constants/functions in a JS block.
2. **Within a repository** — put `.js` files in the `includes/` folder (e.g. a `docs.js` holding column descriptions reused across tables).
3. **Across repositories** — package and import.

JS can be inline (dynamic modification of a query) or in a block (defining functions/constants), and can generate multiple SQL workflow objects from a single file using Dataform global methods [^src1].

## Key concepts: repository / workspace

- **Repository** — centralized, version-controlled storage of code and assets. Each Dataform repository corresponds to a Git repository [^src1].
- **Workspace** — equivalent to a Git branch: an isolated environment where changes are made and tested before merging to the main code base [^src1]. The Dataform GUI exposes all expected Git operations (commit, push, pull, revert) and suggests opening a pull request after a push [^src1].
- **File types** — `config` files (`dataform.json`, `.sqlx`) and `definitions` (`.sqlx` + `.js` defining tables, views, and SQL operations). `dataform.json` sets the **default schema** (the BigQuery dataset where created assets land) and the **assertion schema** (where assertion results are saved) [^src1].

## Assertions (data-quality tests)

An **assertion** is a data-quality test query that finds rows violating a rule; if the query returns any rows, the assertion fails [^src1]. Dataform runs assertions every time it updates a workflow and alerts on failure [^src1]. Two forms [^src1]:

- **Config-block assertions** on a table — e.g. `uniqueKey` (a column must be unique) or row conditions like `count > 0`.
- **Standalone assertion files** — a SQLX file of `type: assertion` whose SQL pulls violating rows.

Assertions create dependencies, so a downstream step can be **skipped** when an upstream assertion fails — Dataform marks it "skipped because upstream dependencies did not all complete successfully" [^src1]. This gives a built-in data-contract gate inside the pipeline, comparable in spirit to dbt tests. See [Data Quality](/data-engineering/data-quality.md).

## GitHub integration & execution

Linking a Dataform repository to a remote GitHub/GitLab repo requires three things: the remote Git URL, a default branch name, and a **secret** (a GitHub personal access token stored in GCP Secret Manager) [^src1]. The Dataform service account must be granted the **Secret Manager Secret Accessor** role to read the token, and **BigQuery** permissions (e.g. `bigquery.jobs.create`) to execute workflows — missing the latter is a common first-run error [^src1].

Three scheduling options for workflow execution [^src1]:
1. **Workflow configurations** in Dataform.
2. **Cloud Scheduler + Workflows**.
3. **Cloud Composer** (managed Airflow). See [Data Orchestration](/data-engineering/data-orchestration.md).

## Dataform vs dbt

Dataform occupies the same "T-of-ELT" niche as [dbt](/data-engineering/dbt.md) — declarative SQL models, ref-based DAG, version control, tests/assertions, docs — but is **BigQuery-native and bundled into GCP**, authored in SQLX rather than dbt's Jinja-templated `.sql` + YAML. Both feed the broader pattern of treating SQL transformations as software with dependency-managed lineage; for routing transformation work across engines see [Query-Engine Routing](/data-engineering/query-engine-routing.md) and for metric definitions [Semantic Layer](/data-engineering/semantic-layer.md).

## See also

- [dbt](/data-engineering/dbt.md) — the dbt-style transformation tool Dataform parallels
- [Data Quality](/data-engineering/data-quality.md) — assertions as in-pipeline DQ gates
- [Data Orchestration](/data-engineering/data-orchestration.md) — Cloud Composer / Scheduler execution
- [ETL Pipeline](/data-engineering/etl-pipeline.md) — ELT context
- [Data Engineering hub](/data-engineering/README.md)

---

[^src1]: [Introduction to Dataform in Google Cloud Platform](../../raw/youtube/youtube-285hnxl9-rk.md)

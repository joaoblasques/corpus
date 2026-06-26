---
type: entity
domain: data-engineering
status: draft
sources:
  - path: 03_Resources/Study Notes/dbt Data Architecture - Simple Stack Design.md
    channel: notes
    ingested_at: 2026-05-21
  - path: raw/web/about-dbt-seed-command-dbt-developer-hub.md
    channel: web
    ingested_at: 2026-06-11
  - path: raw/web/add-exposures-to-your-dag-dbt-developer-hub.md
    channel: web
    ingested_at: 2026-06-11
  - path: raw/web/uplevel-your-dbt-workflow-with-these-tools-and-techniques-st.md
    channel: web
    ingested_at: 2026-06-11
  - path: raw/web/github-josephmachado-simple-dbt-project-at-uplevel-workflow.md
    channel: web
    ingested_at: 2026-06-11
  - path: raw/web/dbt-core-v2-is-here-still-open-source-now-rebuilt-for-what-s.md
    channel: web
    ingested_at: 2026-06-11
  - path: raw/web/we-need-to-talk-about-dbt.md
    channel: web
    ingested_at: 2026-06-11
  - path: raw/email/email-2026-05-14-how-to-connect-data-models-to-your-bi-with-claude-code-dbt-e.md
    channel: email
    ingested_at: 2026-06-11
  - path: raw/email/email-2025-10-01-uplevel-your-dbt-workflow-with-these-tools-and-techniques.md
    channel: email
    ingested_at: 2026-06-15
  - path: raw/email/email-2026-05-15-how-to-learn-dbt-cheap-and-fast.md
    channel: email
    ingested_at: 2026-06-15
  - path: raw/email/email-2026-05-14-get-hands-on-with-dbt-virtual-events-and-interactive-worksho.md
    channel: email
    ingested_at: 2026-06-15
  - path: raw/email/email-2026-06-04-dbt-core-v2-alpha-cart-prediction-with-llms-ray-vs-daft.md
    channel: email
    ingested_at: 2026-06-15
  - path: raw/web/web-the-complete-dbt-guide-from-sql-to-production-ready-transfor.md
    channel: web
    ingested_at: 2026-06-17
  - path: raw/web/web-claude-code-isnt-going-to-replace-data-engineers-yet.md
    channel: web
    ingested_at: 2026-06-17
  - path: raw/web/web-sql-to-dbt-guide-slowly-changing-dimensions-with-dbt-snapsho.md
    channel: web
    ingested_at: 2026-06-17
  - path: raw/web/web-why-dbt-is-terrible-for-databricks-switch-to-native-pipeline.md
    channel: web
    ingested_at: 2026-06-17
  - path: raw/email/email-2025-07-29-de-101-5-dbt-project.md
    channel: email
    ingested_at: 2026-06-19
  - path: raw/email/email-2025-04-16-understanding-the-t-in-etl-a-back-to-basics-guide-to-data-tr.md
    channel: email
    ingested_at: 2026-06-19
  - path: raw/web/web-sql-to-dbt-guide-your-dbt-starter-pack-project.md
    channel: web
    ingested_at: 2026-06-20
  - path: raw/web/web-sql-to-dbt-guide-how-data-layers-flow-with-medallion-archite.md
    channel: web
    ingested_at: 2026-06-20
  - path: raw/web/web-github-aboyalejandro-sql-to-dbt-series-full-dbt-project-with.md
    channel: web
    ingested_at: 2026-06-20
  - path: raw/youtube/youtube-C6BNAfaeqXY-dbt-data-build-tool-crash-course-for-beginners-zero-to-hero.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/email/email-2026-06-25-i-spent-12-hours-rebuilding-my-junior-year-project-part-2-th.md
    channel: email
    ingested_at: 2026-06-26
  - path: raw/github/github-dbt-labs-dbt-core.md
    channel: github
    ingested_at: 2026-06-26
aliases:
  - dbt
  - data build tool
  - dbt core
  - dbt cloud
  - dbt macros
  - dbt snapshots
  - dbt tests
  - generic tests
  - singular tests
tags:
  - corpus/data-engineering
  - entity
created: 2026-05-21
updated: 2026-06-26
last_confirmed: 2026-06-26
---

# dbt (data build tool)

**TL;DR**: A SQL-first transformation framework that compiles `.sql` model files into warehouse-optimized queries, enforces layer separation via materialization strategies, and treats data transformations as software (version control, testing, lineage) [^src1].

## Role in the data stack

dbt operates on the "T" of ELT — it transforms data **already in the warehouse**. It does not extract or load.

```
Sources → [Extract & Load] → Raw DB → [dbt transforms] → Analytics DB → Reporting
```

## Sources vs Models

| Concept | What it is | How to reference |
|---|---|---|
| **Source** | Pointer to raw, untransformed data in the Raw DB | `{{ source('schema', 'table') }}` |
| **Model** | Transformed output deployed by dbt (`.sql` file) | `{{ ref('model_name') }}` |

Never point a `source` at a table that has already been transformed — sources must reference raw data only [^src1].

## Layer architecture (The Simple Stack)

dbt projects mirror the database schema structure [^src1]:

| dbt directory | DB schema | Materialization | Purpose |
|---|---|---|---|
| `models/staging/` | `staging` | `view` | Clean and standardize raw data; 1:1 with source tables |
| `models/warehouse/` | `warehouse` | `table` | Joined, enriched, business-logic models |
| `models/marts/` | `marts` | `table` | Consumption-ready tables for BI tools and end users |

See [[data-engineering/pipeline-layers|Pipeline Layers]] for the architecture pattern this implements.

## `dbt_project.yml` configuration

Materializations and schema targets are set centrally [^src1]:

```yaml
models:
  my_project:
    staging:
      +materialized: view
      +schema: staging
    warehouse:
      +materialized: table
      +schema: warehouse
    marts:
      +materialized: table
      +schema: marts
```

## Database design

Two separate databases on the same server [^src1]:
- **Raw DB** — one schema per external source (e.g., `stripe`, `google_analytics`)
- **Analytics DB** — `staging`, `warehouse`, `marts` schemas

## Seeds

`dbt seed` loads static CSV files from the project's seed-paths into the warehouse as tables [^src2]. Seeds are for small, version-controlled reference datasets kept alongside the project — e.g., country codes, region mappings, business-defined category lists [^src2]. After loading, seeds are referenced in downstream models like any other relation, and re-run when the CSVs change [^src2].

- Configured in `dbt_project.yml` (seed directories, column types, quoting) [^src2].
- Selectable like models: `dbt seed --select "country_codes"` [^src2].
- `--full-refresh` forces a clean reload from scratch — needed after a structural change such as renamed columns or changed types [^src2].

Seeds are first-class selectable resources (`dbt ls --select "source:*,resource_type:test"` selects by resource type; the same selection grammar applies) [^src5].

## Exposures and lineage

An **exposure** defines and describes a *downstream* use of a dbt project — a dashboard, application, notebook, or ML/data-science pipeline — extending lineage beyond the models dbt itself builds [^src3]. Defining exposures lets you `run`, `test`, and `list` the resources that feed a given consumer, and populates a dedicated docs page for data consumers [^src3].

Exposures are declared under an `exposures:` key in `.yml` files [^src3]:

```yaml
exposures:
  - name: weekly_jaffle_metrics
    type: dashboard            # dashboard | notebook | analysis | ml | application
    maturity: high             # high | medium | low — confidence/stability
    url: https://bi.tool/dashboards/1
    depends_on:
      - ref('fct_orders')
      - source('gsheets', 'goals')
      - metric('count_orders')
    owner:
      name: Callum McData
      email: data@jaffleshop.com
```

- **Required**: `name` (snake_case), `type`, `owner` (name or email) [^src3].
- `depends_on` lists refable nodes (`ref`, `source`, `metric`); depending on a `source` directly is possible but rarely needed [^src3].
- Exposures can be **manual** (YAML) or **automatic** — dbt creates and visualizes downstream exposures for supported integrations, stored in metadata (appear in Catalog) without YAML files [^src3].
- Reference them in commands with the `exposure:` selector: `dbt run -s +exposure:weekly_jaffle_report` [^src3].

Exposures close the "last mile" of lineage: dbt natively provides model-to-model lineage, while an enriched exposure maps model → dashboard → individual card/column [^src7]. A barebones exposure is "a pointer with no payload" — it links to a dashboard but tells AI tooling nothing about what's inside [^src7]. Enriching exposure descriptions (business purpose, cards, key columns) turns them into a lean data catalog supporting impact analysis without a dedicated metadata platform [^src7]. Caveat: enrichment is a snapshot that **drifts** as dashboards change, so it must be periodically refreshed [^src7]. See [[data-engineering/claude-code-for-data-engineering|Claude Code for Data Engineering]] for the AI-assisted enrichment workflow.

> A 2022 critique noted exposures were a promising step but at the time were **manual only**, with "no clear way for vendors to integrate" with them [^src6]. The automatic-exposure capability above is a later development.

## Packages

dbt **packages** let projects reuse existing macros/models rather than rewriting common SQL [^src4]:

- **`dbt-utils`** — standard data-processing functionality missing natively in warehouses (e.g., a `pivot` macro for warehouses lacking native pivot) [^src4].
- **`dbt-expectations`** — a wide range of data tests, inspired by Python's Great Expectations (e.g., column-value comparisons). Tradeoff: you cannot control the implementation, which may be inefficient for a given warehouse [^src4].
- **`elementary`** — data-observability package (see workflow below) [^src4].

## Workflow tooling

A set of techniques to speed up dbt feature delivery while protecting data quality [^src4]:

| Technique | Purpose |
|---|---|
| **Selectors** (`--select`) | Run only the needed models/tests via methods, graph operators (up/down-stream), set operators, and exclude; `dbt ls` previews what a selector resolves to [^src4][^src5] |
| **Tags** | Select arbitrary models/tests by an assigned tag (e.g., `tag:elementary`) regardless of folder path [^src4][^src5] |
| **`defer` + `--state`** | Build only modified models in dev while reading upstream models from another environment's artifacts (prod/UAT). Building only modified models is **slim CI** [^src4] |
| **Thread count** | Raise parallelism via `threads` in `profiles.yml`; bounded by warehouse capacity [^src4] |
| **`manifest.json`** | The lineage graph, compiled SQL, test/macro associations live in `target/manifest.json`; parse it to lint the graph (e.g., flag orphan tests or hardcoded table names) [^src4] |
| **sqlfluff / yamllint** | SQL and YAML lint+format to avoid PR style nits; run as a pre-commit hook to save CI cost [^src4] |
| **Auto-grants** | Native `grants` config (in `dbt_project.yml` or per-model) replaces manual `GRANT` post-hooks [^src4] |

### Production CI/CD: manifest-state incremental deploys

A concrete production pattern that pushes `defer`/slim-CI all the way through deploy, storing the production `manifest.json` in S3 as the shared state between runs [^src19]:

- **Slim CI on PRs** — compute the **merge-base** SHA between the PR branch and `main`, `dbt parse` both, then `dbt ls --state base_state --select state:modified state:new` to find changed models. Merge-base (not latest `main`) avoids false positives from other PRs that merged meanwhile. A **macro change with no flagged model selects all models** (macros can affect any dependent). Use `dbt clone` to zero-copy-clone prod tables into a throwaway `STAGING` schema so unchanged upstream models are available without rebuilding. CI builds its own baseline manifest and never touches the prod state [^src19].
- **Incremental CD on merge** — `dbt build --select state:modified+ --defer --favor-state --state prod_state` after downloading the prior `manifest.json` from S3; rebuilds only modified models + downstream, defers unchanged refs to existing prod tables, and uploads the new manifest for the next deploy to diff against. First deploy (no manifest) falls back to a full `dbt run` + `dbt test`. Concurrency control **queues** rather than cancels a second deploy to avoid races on the shared manifest [^src19].

See [[data-engineering/sources/skytrax-dbt-transformation-project|Skytrax dbt transformation project]] for the full worked example (Snowflake RBAC-as-Terraform, OIDC keyless auth, CloudFront-hosted docs) and [[data-engineering/cicd-for-data-infrastructure|CI/CD for Data Infrastructure]] for the general skeleton.

### data-diff (deprecated)

`data-diff` compared datasets column-by-column to confirm a change did not alter granularity, units, or values (e.g., dev vs. prod after editing a model) [^src4]. **Note: the open-source `data-diff` project has been archived — do not use it for new work** [^src4]. dbt's `audit_helper` is an alternative [^src4].

### Data observability with Elementary

The **elementary** dbt package (plus its Python CLI) adds schema checks, anomaly detection, and a data-quality dashboard [^src4]:

- **Schema checks** — detect unexpected schema changes on upstream source tables, and (via an exposure check) on output models consumed by BI, catching type changes that would break downstream consumers [^src4].
- **Anomaly detection** — monitors a number (row count, freshness, group-by metrics, column statistics such as null rate/min/max) across dbt runs; by default flags values with a standard score ≥ 3 [^src4].
- **Reports** — `elementary` generates a static HTML report of all test results and anomalies [^src4].

A companion reference repo (`josephmachado/simple_dbt_project`, `uplevel-workflow` branch) demonstrates these with a local Postgres warehouse, Poetry, and a `justfile` of command shortcuts [^src5].

## dbt Core v2 (Rust / Fusion foundation)

dbt Core **v2.0** (first alpha, 2026) rebuilds dbt Core on the same foundation as the **dbt Fusion** engine, open-sourcing a large amount of previously proprietary Fusion code under Apache 2.0 [^src8]. Key changes [^src8]:

- A high-performance **Rust** implementation replaces the Python baseline, with significant parse-time improvements on large projects.
- A **tightly-defined language spec** — config typos like `desciptin` for `description` become impossible — giving integrators a stable interface.
- New **Parquet artifacts** as a high-performance alternative to large JSON files, directly queryable via DuckDB or an agent.
- Streamlined adapter authoring via **ADBC / Arrow**; distributed as a **single self-contained binary** with no Python runtime or dependency management required [^src20].

**Branch structure** (as of alpha): the `main` branch hosts v2.0 (alpha); v1 development continues on the `1.latest` branch. Latest v1 stable release: **v1.11.11** [^src20].

**Supported OS/arch matrix** [^src20]:

| OS | x86-64 | ARM |
|---|---|---|
| macOS | supported | supported |
| Linux | supported | supported |
| Windows | supported | not yet |

The "two-engine era" is ending: Core and Fusion now share a runtime [^src8]. Two free v2 distributions exist — **Fusion** (precompiled binary, contains some proprietary code, includes a built-in SQL linter, premium features unlocked via free login or paid plan) and a **pure Apache-2.0 dbt Core** built from the open repo [^src8]. dbt Labs recommends Fusion for almost all users; pure dbt Core targets teams with license constraints or those building on the OSS code [^src8]. Business logic remains portable across both [^src8]. Migration aids: `dbt-autofix`, an agent skill for upgrades, and a Fusion-powered parser available in v1.12 (`dbt parse --use-v2-parser`) [^src8]. The old Python `dbt-core` (v1.12 beta and earlier) remains available on PyPI/GitHub [^src8].

### Fivetran + dbt Labs merger (2026)

dbt Core v2.0 shipped alongside the completed **Fivetran + dbt Labs merger** ("to create the data infrastructure for trusted AI agents") [^src9]. Combined first innovations announced: dbt Core v2.0 (open-sourcing the Fusion runtime), **dbt State** (a caching layer claimed to cut underlying infra costs >30%), **dbt Wizard** (beta — autonomous model authoring/refactoring/debugging), and an **Agents Schema** open standard for agentic context [^src9]. Note: vendor (sponsor) framing — claims are promotional.

## Why dbt exists / learning it

dbt was created because storage got cheaper and SQL OLAP systems more powerful, shifting **ETL → ELT** and moving transformation *inside* the warehouse, written in SQL — democratised so analysts/analytics engineers (not only strong coders) can transform data [^src10]. But that logic still needs to be **tested, modularised, and documented**, which is dbt's purpose [^src10]. A dbt model is "purely Jinja + SQL," so it can be version-controlled, rolled back, and CI/CD-deployed like application code [^src10]. With just **dbt + Airflow + a cloud warehouse**, a company can build a complete analytics pipeline — making dbt one of the most in-demand DE tools [^src10]. Learning resources noted: the `learn_dbt` CLI tool (49 hands-on exercises run locally) [^src10], and dbt Labs' free **"Zero to dbt"** live workshops and on-demand demos [^src11].

dbt rose to prominence as the **transform-focused tool of the MDS (Modern Data Stack) boom** of the early 2020s, especially at startups [^src14]. It wasn't the first transform tool — earlier platforms were typically drag-and-drop UIs with some SQL — but it stood out by embracing **version control, modular SQL, testing, and documentation**, and by making SQL-based workflows accessible to a broader set of users [^src14]. It is not the only option: **SQLMesh** and [[data-engineering/dataform|Dataform]] are alternative SQL-based transform tools [^src14]. See [[data-engineering/data-transformation|Data Transformation]] for the broader "T"-in-ETL context.

## Community criticism (2022 love-letter)

A widely-read 2022 essay framed concerns as **community, core, and cloud** problems, in the context of dbt Labs' rapid VC funding ($30M Series B Nov 2020 → $222M round Feb 2022) and the pressure to generate revenue [^src6]:

- **Community** — the Slack (≈25,000 members by 2022) became hard to follow and a content-distribution/lead-gen channel for vendors [^src6].
- **Core** — lack of transparency on the Core roadmap; macros described as "a jinja-powered hot mess of untestable code"; hard third-party integration (getting model names without a full warehouse run was effectively impossible); no namespaces in `ref`; no language server to catch syntax errors before running [^src6].
- **Cloud** — dbt Cloud's IDE criticized as a slow text editor with poor ecosystem awareness, undocumented Metadata API, and no public webhooks at the time [^src6].

Several of these — Rust parser/language spec, the language server experience, an open metadata story — are directly addressed by the v2/Fusion direction (above) [^src8]. Treat this critique as a **point-in-time** snapshot.

## The sql-to-dbt learning path (Alejandro Aboy series)

An 8-article series covering dbt end-to-end, with a companion `sql-to-dbt-series` GitHub repo (DuckDB + synthetic marketing data + Docker) [^src12]:

1. **Getting started** — mindset shift from ad-hoc SQL to version-controlled, testable transformation pipelines.
2. **Building first project** — project structure, materializations, Jinja macros, essential commands.
3. **Medallion architecture** — Bronze/Silver/Gold pattern; staging vs. intermediate vs. mart layers and why folder structure matters.
4. **Data quality workflows** — data integrity (keeps pipelines running) vs. data quality (prevents bad decisions); data contracts, generic tests, singular tests, `dbt-expectations`.
5. **Macros and reusability** — DRY principles; five project macros (performance classification, safe division, target comparison, percentage calculation, touchpoint attribution); before/after with `LAG` window functions reduced to single invocations.
6. **SCD2 with snapshots** — see [[data-engineering/scd2|SCD2]] for the timestamp vs. check strategy details.
7. **dbt internals** — reverse-engineering dbt's core: dependency parsing with regex, DAG construction, topological sort (Kahn's algorithm), ordered execution in ~500 lines of Python.
8. **Portable data stack** — dbt-core + DuckDB + GitHub Actions (cron) + Google Sheets + Looker Studio. All portable, low-cost, containerized.

Key insight from the series: *"Contracts block bad schemas during compilation, while tests catch quality issues after builds."* [^src12] The series also includes an agentic data modeling demo (OpenMetadata MCP + AI for downstream impact analysis) — see [[data-engineering/agentic-data-modeling|Agentic Data Modeling]].

## Building a dbt project with Claude Code

A hands-on evaluation of Claude Code's capability to build a dbt project from real data (UK Environment Agency flood monitoring API, DuckDB), run in March 2026 using Opus 4.6 [^src13]. Key findings:

**What Claude did well** [^src13]:
- Built a working `staging → dim/fact` model structure with correct key relationships and data contracts.
- Implemented incremental fact table load (`materialized='incremental'`, `unique_key=['date_time', 'measure_id']`).
- Handled messy source data (pipe-delimited multi-values: `split_part(value, '|', 1)`).
- Implemented SCD2 snapshots for station metadata.
- Added documentation, tests, and source freshness checks.
- Autonomously debugged `dbt build` failures: identified Jinja2 escape issues, fixed test syntax deprecations, queried DuckDB directly to verify data quality issues (631 stations with missing coordinates), and downgraded tests to warn severity.

**Where Claude fell short** [^src13]:
- Python ingestion script silently capped at API's 2000-item limit (5,458 actual stations); only 1,493 rows loaded. *"Wrong is worse than absent because you can't trust it."*
- Silently dropped relevant columns (`gridReference`, `datumOffset`, `unit`).
- Only implemented SCD2 for stations, not measures — because the prompt said "station metadata" and it followed literally.
- Did not challenge questionable assumptions (should measures get SCDs too?).

**The verdict** [^src13]: *"Claude Code is an amazing productivity companion. Do not, if you value your job, use it to one-shot a dbt project."* DE + AI > DE alone — agentic coding tools make DEs vastly more productive for specific tasks and iteration, but the net gain still requires the engineer's mental model, verification, and domain knowledge. The prompt and skills (dbt-agent-skills from dbt Labs) matter more than the model — Sonnet 4.5 with good context produces respectable results.

See [[data-engineering/claude-code-for-data-engineering|Claude Code for Data Engineering]] for the broader AI-assisted DE workflow and [[data-engineering/ai-impact-on-data-engineering|AI's Impact on Data Engineering]] for the role-level framing.

## The sql-to-dbt-series reference project

Alejandro Aboy's open-source reference project (`aboyalejandro/sql-to-dbt-series`) demonstrates a complete, portable dbt stack backed by DuckDB and synthetic marketing data — designed to follow alongside the article series [^src17]:

**Stack**: DuckDB (OLAP), dbt (staging → intermediate → marts), Docker Compose, synthetic JSON marketing data from `syntheticdatagen.xyz`.

**Models shipped** [^src17]:
- Attribution models (multi-touch), campaign performance, visitor journey.
- **Snapshots**: `dbt snapshot` tracks campaign performance and visitor segment evolution over time (SCD Type 2 in dbt).
- **dbt-colibri** for column-level lineage visualization at `localhost:8080`.

**Advanced data contracts** [^src17]: built with business-logic constraints; the project is designed to fail on purpose so data contract enforcement and testing can be demonstrated against real failures.

**Reusable macros**: touchpoint attribution and performance classification.

Key dev commands: `dbt run --select staging` (clean raw) → `dbt run --select intermediate` (business logic) → `dbt run --select marts` (final aggregates) → `dbt test` → `dbt snapshot`. The `make run` command chains extract → database → dbt end to end [^src17].

## dbt core concepts: a crash-course overview

From a beginner crash-course (Data Tech, 2023) — useful framing for first-time learners [^src18]:

### What dbt is (and is not)

dbt is **the "T" in ELT** — it executes transformations via SQL; it does not handle ingestion, BI, or data storage. The data stays in the warehouse; dbt does not have its own storage. Crucially, **the computation for dbt transformations is provided by the warehouse**, not by dbt itself [^src18]. This contrasts with Spark, which brings its own compute cluster.

What dbt **cannot** do [^src18]:
- Not an ingestion/loading tool
- Not a BI tool
- Does not store data (data stays in the warehouse)
- Does not provide its own compute (uses warehouse compute)

### dbt Core vs dbt Cloud

| | dbt Core | dbt Cloud |
|---|---|---|
| Form | Open-source Python packages; CLI | Web-based UI built on top of Core |
| Install | `pip install dbt-core` | Browser, no setup |
| Scheduling | External (Airflow, cron) | Built-in job scheduler |
| IDE | Your own editor | Built-in web IDE |
| Git | Manual integration | Native integration |
| Multi-user | Manual | Managed |
| Cost | Free | Free for single users; paid for teams |

dbt Core for teams that want infrastructure control; dbt Cloud for teams that want managed infrastructure without maintenance overhead [^src18].

### Core concepts

- **Models** — the basic building block; each model is a `.sql` file containing a `SELECT` statement. Models can reference other models and tables [^src18].
- **Macros** — reusable SQL code blocks; equivalent to functions in Python. Use when the same SQL pattern recurs across multiple models [^src18].
- **Tests** — verify data quality of models. Two types [^src18]:
  - *Generic tests* — four built-in: `not_null`, `unique`, `accepted_values`, `relationships`
  - *Singular tests* — custom SQL tests for specific business logic
- **Snapshots** — track **SCD Type 2** changes over time. dbt only handles SCD Type 2 (timestamp or check strategy). See [[data-engineering/scd2|SCD2]] [^src18].

### dbt project structure (initial layout)

```
dbt_project.yml     # project config
models/             # .sql model files
snapshots/          # SCD2 snapshot definitions
tests/              # singular test SQL files
macros/             # reusable Jinja macros
seeds/              # static CSV data files
analysis/           # ad-hoc SQL (not materialized)
```

### Data lifecycle with dbt

Sources → **Data Loaders** (raw) → **Warehouse** → **dbt** (transforms based on business rules) → **Transformed data in warehouse** → BI / downstream consumers [^src18]. dbt occupies only the transformation phase, and the warehouse handles all compute.

### Warehouse compatibility

At time of recording (Dec 2023): AlloyDB, BigQuery, Databricks, Dremio, Postgres, Redshift, Snowflake, Spark, Trino, Microsoft Fabric, Azure Synapse Analytics, Teradata — see dbt docs for the current list [^src18].

## See also

- [[data-engineering/pipeline-layers|Pipeline Layers]] — the staging → warehouse → marts architecture pattern
- [[data-engineering/dimensional-modeling|Dimensional Modeling]] — Kimball star schemas dbt commonly builds
- [[data-engineering/scd2|SCD Type 2]] — slowly-changing dimensions via dbt snapshots
- [[data-engineering/data-orchestration|Data Orchestration]] — scheduling dbt runs vs. transforming in dbt
- [[data-engineering/orchestra|Orchestra]] — a managed orchestrator that runs dbt staging/curated tasks via tag selection
- [[data-engineering/dataform|Dataform]] — the BigQuery-native, SQLX-based dbt analogue
- [[data-engineering/claude-code-for-data-engineering|Claude Code for Data Engineering]] — AI-assisted dbt modeling and exposure enrichment
- [[data-engineering/sources/dbt-kimball-project|dbt Kimball reference project]] — SCD2 example project
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [[03_Resources/Study Notes/dbt Data Architecture - Simple Stack Design|dbt Data Architecture - Simple Stack Design]]
[^src2]: [About dbt seed command](../../raw/web/about-dbt-seed-command-dbt-developer-hub.md)
[^src3]: [Add Exposures to your DAG](../../raw/web/add-exposures-to-your-dag-dbt-developer-hub.md)
[^src4]: [Uplevel your dbt workflow with these tools and techniques](../../raw/web/uplevel-your-dbt-workflow-with-these-tools-and-techniques-st.md)
[^src5]: [josephmachado/simple_dbt_project (uplevel-workflow)](../../raw/web/github-josephmachado-simple-dbt-project-at-uplevel-workflow.md)
[^src6]: [We need to talk about dbt](../../raw/web/we-need-to-talk-about-dbt.md)
[^src7]: [How to connect data models to your BI with Claude Code, dbt exposures & MCPs](../../raw/email/email-2026-05-14-how-to-connect-data-models-to-your-bi-with-claude-code-dbt-e.md)
[^src8]: [dbt Core v2 is here: still open source, now rebuilt for what's next](../../raw/web/dbt-core-v2-is-here-still-open-source-now-rebuilt-for-what-s.md)
[^src9]: [TLDR Data — dbt Core v2 Alpha / Fivetran + dbt Labs merger (newsletter)](../../raw/email/email-2026-06-04-dbt-core-v2-alpha-cart-prediction-with-llms-ray-vs-daft.md)
[^src10]: [How to learn dbt cheap and fast (Vu Trinh)](../../raw/email/email-2026-05-15-how-to-learn-dbt-cheap-and-fast.md)
[^src11]: [Get Hands-On with dbt: Virtual Events and Interactive Workshops (dbt Labs)](../../raw/email/email-2026-05-14-get-hands-on-with-dbt-virtual-events-and-interactive-worksho.md)
[^src12]: [The Complete dbt Guide: From SQL to Production-Ready Transformations](../../raw/web/web-the-complete-dbt-guide-from-sql-to-production-ready-transfor.md)
[^src13]: [Claude Code isn't going to replace data engineers (yet)](../../raw/web/web-claude-code-isnt-going-to-replace-data-engineers-yet.md)
[^src14]: [Understanding the "T" in ETL: A Back-to-Basics Guide to Data Transformations](../../raw/email/email-2025-04-16-understanding-the-t-in-etl-a-back-to-basics-guide-to-data-tr.md)
[^src15]: [SQL to dbt Guide — Your dbt Starter Pack Project](../../raw/web/web-sql-to-dbt-guide-your-dbt-starter-pack-project.md) — Alejandro Aboy, Pipeline to Insights
[^src16]: [SQL to dbt Guide — How Data Layers Flow with Medallion Architecture](../../raw/web/web-sql-to-dbt-guide-how-data-layers-flow-with-medallion-archite.md) — Alejandro Aboy, Pipeline to Insights
[^src17]: [GitHub — aboyalejandro/sql-to-dbt-series: Full dbt project with DuckDB, Docker and synthetic Ads campaign data](../../raw/web/web-github-aboyalejandro-sql-to-dbt-series-full-dbt-project-with.md) — Alejandro Aboy
[^src18]: [dbt (Data Build Tool) Crash Course for Beginners: Zero to Hero (Data Tech, YouTube)](../../raw/youtube/youtube-C6BNAfaeqXY-dbt-data-build-tool-crash-course-for-beginners-zero-to-hero.md)
[^src19]: [I spent 12 Hours rebuilding my Junior year project: Part 2 — The Transformation Layer (Minh Pham, guest on Vu Trinh's newsletter)](../../raw/email/email-2026-06-25-i-spent-12-hours-rebuilding-my-junior-year-project-part-2-th.md)
[^src20]: [dbt-labs/dbt-core (GitHub README, v2.0 alpha)](../../raw/github/github-dbt-labs-dbt-core.md)

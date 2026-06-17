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
aliases:
  - dbt
  - data build tool
tags:
  - corpus/data-engineering
  - entity
created: 2026-05-21
updated: 2026-06-15
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
- Streamlined adapter authoring via **ADBC / Arrow**; simplified install that avoids Python virtualenv friction.

The "two-engine era" is ending: Core and Fusion now share a runtime [^src8]. Two free v2 distributions exist — **Fusion** (precompiled binary, contains some proprietary code, includes a built-in SQL linter, premium features unlocked via free login or paid plan) and a **pure Apache-2.0 dbt Core** built from the open repo [^src8]. dbt Labs recommends Fusion for almost all users; pure dbt Core targets teams with license constraints or those building on the OSS code [^src8]. Business logic remains portable across both [^src8]. Migration aids: `dbt-autofix`, an agent skill for upgrades, and a Fusion-powered parser available in v1.12 (`dbt parse --use-v2-parser`) [^src8]. The old Python `dbt-core` (v1.12 beta and earlier) remains available on PyPI/GitHub [^src8].

### Fivetran + dbt Labs merger (2026)

dbt Core v2.0 shipped alongside the completed **Fivetran + dbt Labs merger** ("to create the data infrastructure for trusted AI agents") [^src9]. Combined first innovations announced: dbt Core v2.0 (open-sourcing the Fusion runtime), **dbt State** (a caching layer claimed to cut underlying infra costs >30%), **dbt Wizard** (beta — autonomous model authoring/refactoring/debugging), and an **Agents Schema** open standard for agentic context [^src9]. Note: vendor (sponsor) framing — claims are promotional.

## Why dbt exists / learning it

dbt was created because storage got cheaper and SQL OLAP systems more powerful, shifting **ETL → ELT** and moving transformation *inside* the warehouse, written in SQL — democratised so analysts/analytics engineers (not only strong coders) can transform data [^src10]. But that logic still needs to be **tested, modularised, and documented**, which is dbt's purpose [^src10]. A dbt model is "purely Jinja + SQL," so it can be version-controlled, rolled back, and CI/CD-deployed like application code [^src10]. With just **dbt + Airflow + a cloud warehouse**, a company can build a complete analytics pipeline — making dbt one of the most in-demand DE tools [^src10]. Learning resources noted: the `learn_dbt` CLI tool (49 hands-on exercises run locally) [^src10], and dbt Labs' free **"Zero to dbt"** live workshops and on-demand demos [^src11].

## Community criticism (2022 love-letter)

A widely-read 2022 essay framed concerns as **community, core, and cloud** problems, in the context of dbt Labs' rapid VC funding ($30M Series B Nov 2020 → $222M round Feb 2022) and the pressure to generate revenue [^src6]:

- **Community** — the Slack (≈25,000 members by 2022) became hard to follow and a content-distribution/lead-gen channel for vendors [^src6].
- **Core** — lack of transparency on the Core roadmap; macros described as "a jinja-powered hot mess of untestable code"; hard third-party integration (getting model names without a full warehouse run was effectively impossible); no namespaces in `ref`; no language server to catch syntax errors before running [^src6].
- **Cloud** — dbt Cloud's IDE criticized as a slow text editor with poor ecosystem awareness, undocumented Metadata API, and no public webhooks at the time [^src6].

Several of these — Rust parser/language spec, the language server experience, an open metadata story — are directly addressed by the v2/Fusion direction (above) [^src8]. Treat this critique as a **point-in-time** snapshot.

## See also

- [[data-engineering/pipeline-layers|Pipeline Layers]] — the staging → warehouse → marts architecture pattern
- [[data-engineering/dimensional-modeling|Dimensional Modeling]] — Kimball star schemas dbt commonly builds
- [[data-engineering/scd2|SCD Type 2]] — slowly-changing dimensions via dbt snapshots
- [[data-engineering/data-orchestration|Data Orchestration]] — scheduling dbt runs vs. transforming in dbt
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

---
type: source
domain: data-engineering
status: draft
sources:
  - path: raw/email/email-2026-06-25-i-spent-12-hours-rebuilding-my-junior-year-project-part-2-th.md
    channel: email
    ingested_at: 2026-06-26
aliases:
  - Skytrax reviews transformation project
  - skytrax_reviews_transformation
  - Minh Pham dbt project
  - junior year project part 2
tags:
  - corpus/data-engineering
  - source
created: 2026-06-26
updated: 2026-06-26
---

# Skytrax Reviews — dbt Transformation Layer (portfolio project)

**TL;DR.** A hands-on, end-to-end build of the **transformation half** of a data pipeline: raw airline reviews in Snowflake → a Kimball star schema in dbt, with **all Snowflake RBAC and AWS resources managed by Terraform**, **keyless OIDC auth** for GitHub Actions, a **slim CI** that only rebuilds changed models, an **incremental CD** that deploys via `state:modified+ --defer --favor-state`, and **dbt docs auto-hosted on CloudFront** [^src1]. Part 2 of a guest series by Minh Pham (a data engineer at Insurify) on Vu Trinh's newsletter; Part 1 covered ingestion (scraping → S3 → Snowflake) [^src1].

## Stack

| Layer | Tool |
|---|---|
| Transformation | **dbt** (`dbt-snowflake`) — Kimball star schema |
| Warehouse | **Snowflake** — all RBAC managed by Terraform |
| IaC | **Terraform** — Snowflake + AWS resources |
| CI/CD | **GitHub Actions** — slim CI on PRs, defer/favor-state CD on merge |
| Artifact storage | **AWS S3** — manifests, run results, dbt docs |
| Docs CDN | **AWS CloudFront** (private S3 via Origin Access Control) |
| Auth | **AWS IAM OIDC** — keyless GitHub Actions → AWS |
| Linting | **SQLFluff** — lowercased keywords, trailing commas, explicit aliases |
| Orchestration | **Apache Airflow** (Astronomer + `cosmos`) |

Repo: `MarkPhamm/skytrax_reviews_transformation` [^src1].

## Data model — Kimball star schema

Built with the Kimball four-step process: business process (analyzing customer reviews) → grain (one review submitted) → dimensions (aircraft, customer, airline, date, location) → facts (`fct_reviews`) [^src1]. See [[data-engineering/dimensional-modeling|Dimensional Modeling]].

The transformation follows the classic **staging → intermediate → marts** flow [^src1]:

- **Staging** (`stg__skytrax_reviews`) — a 1:1 view on the raw source; adds a `review_id` via `row_number()`; minimal transformation.
- **Intermediate** (`int_reviews_cleaned`) — where business logic lives: null handling (`coalesce(..., 'unknown')`), column renaming (`verify → is_verified`), type standardization.
- **Marts** — the star schema. All dimensions use `dbt_utils.generate_surrogate_key` for deterministic surrogate keys. `fct_reviews` joins all 5 dimensions, with **role-playing dimensions** for dates (submitted vs. flown) and locations (origin, destination, transit), and computes an `average_rating` and a `rating_band` (bad/medium/good) [^src1].

## Snowflake RBAC as Terraform

The Snowflake Terraform is split across files by concern (`warehouses.tf`, `databases.tf`, `roles.tf`, `grants.tf`, `users.tf`), so adding an analyst or schema means editing a `locals` map and running `terraform apply` rather than clicking in the UI [^src1]. Key patterns [^src1]:

- **Role hierarchy** wired up to `SYSADMIN` (Snowflake best practice — custom roles stay reachable from the top):
  ```
  ACCOUNTADMIN → SYSADMIN → SKYTRAX_ADMIN
       ├── SKYTRAX_TRANSFORMER  (read/write on all production schemas; used by dbt in CI/CD + prod)
       └── SKYTRAX_ANALYST      (read-only on MARTS + write on own dev schema; for humans)
  ```
- **Per-environment schemas** — production models go to `SOURCE/INTERMEDIATE/MARTS`; CI writes to a flat `STAGING` schema wiped after each PR; each developer gets a private `DEV_*` schema so locals don't collide.
- **`for_each` over `locals` maps** — warehouse sizes and schema lists are looped, so new schemas auto-propagate grants.
- **Future grants** — auto-apply permissions to tables/views created later (critical because dbt creates new objects every run).
- **Ownership transfer** to `TRANSFORMER` — needed because dbt uses `CREATE OR REPLACE`, which requires ownership.
- **Two separate service accounts** (`PROD_DBT` for Airflow, `DBT_CICD` for GitHub Actions) both on the `TRANSFORMER` role but kept distinct so you can audit and revoke independently.
- Warehouses set `auto_suspend = 60` + `auto_resume = true` to keep idle cost near zero.

## Keyless auth — GitHub Actions OIDC

Instead of long-lived AWS keys in GitHub Secrets, the project registers GitHub's OIDC issuer (`token.actions.githubusercontent.com`) as an AWS identity provider and lets Actions **assume an IAM role** directly [^src1]. The role's trust policy uses a `StringLike` condition on the `sub` claim scoped to `repo:<owner>/<repo>:*`, so only workflows from that repo can assume it; AWS STS returns temporary (15-min) credentials [^src1]. The role grants just S3 object access on the artifacts bucket plus `cloudfront:CreateInvalidation` [^src1].

## CI/CD — slim CI, incremental CD

This is a concrete instance of the [[data-engineering/cicd-for-data-infrastructure|CI/CD for Data Infrastructure]] pattern, specialized for dbt.

**Slim CI (`pr_checks.yml`, on PRs)** — only lints/compiles/runs/tests the models you actually changed [^src1]:
- Computes the **merge-base SHA** between the PR branch and `main`, runs `dbt parse` on both, and uses `dbt ls --state base_state --select state:modified state:new` to find changed models. Merge-base (not latest `main`) avoids false positives from other PRs merged meanwhile.
- Detects macro changes — if a macro changed but no model was flagged, selects **all** models (macros can affect any dependent model).
- Uses `dbt clone` to zero-copy-clone production tables into `STAGING`, so unchanged upstream models are available without rebuilding.
- Runs downstream models (`model_name+`) and tests to catch breakage further down the DAG.
- CI builds its own baseline manifest from merge-base code and **never touches S3** — fully independent of production deploys.

**Incremental CD (`deploy_main.yml`, on merge)** [^src1]:
```
dbt build --select state:modified+ --defer --favor-state --state prod_state
```
- Downloads the production `manifest.json` from S3, rebuilds only modified models + downstream, `--defer`s unchanged refs to existing production tables, and `--favor-state` prefers the production state when resolving deferred refs — saving Snowflake credits.
- First deploy (no manifest) falls back to a full `dbt run` + `dbt test`.
- Uploads the new manifest + run results to S3 for the next deploy to diff against.
- **Concurrency control** queues (not cancels) a second deploy, preventing races on the production manifest.

A reusable composite action (`dbt-ci-init/action.yml`) factors out Python/venv/`dbt deps` setup so it isn't copy-pasted across 7+ jobs [^src1].

## dbt docs hosting

`dbt docs generate` → `aws s3 sync` to `s3://bucket/docs/` → `cloudfront create-invalidation` on every merge [^src1]. The S3 bucket is **private**; CloudFront reads it via Origin Access Control (OAC), except a public `manifests/*` prefix so developers can `curl` the production manifest for local **defer builds** against prod [^src1]. The author first built an EC2 + nginx host (~$8/mo, OS patching, cron sync, full VPC) and replaced it with CloudFront ($0 on free tier, 3 Terraform resources) — *"for a static site like dbt docs, CloudFront is the right tool"* [^src1].

## Why it matters

A compact, reproducible reference for the **transformation + ops** half of a portfolio-grade pipeline: everything is IaC, every deploy is incremental, no static cloud credentials exist anywhere, and dev/CI/prod are isolated by schema. Maps directly onto the rigor checklist in [[data-engineering/portfolio-project-that-lands-a-de-role|The Portfolio Project That Lands a DE Role]] (medallion/DQ/idempotency/tests/metadata/IaC/cost).

## Related

- [[data-engineering/dbt|dbt]] — slim CI, `defer`/`--favor-state`, `dbt clone`, manifest-state deploys
- [[data-engineering/cicd-for-data-infrastructure|CI/CD for Data Infrastructure]] — the general CI-plan → CD-gate skeleton this specializes
- [[data-engineering/dimensional-modeling|Dimensional Modeling]] — the Kimball star schema + role-playing dimensions
- [[data-engineering/snowflake|Snowflake]] — the warehouse and its RBAC model
- [[mlops/terraform|Terraform]] — the IaC tool managing both Snowflake and AWS
- [[data-engineering/portfolio-project-that-lands-a-de-role|The Portfolio Project That Lands a DE Role]] — the hiring-signal rubric this project satisfies
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [I spent 12 Hours rebuilding my Junior year project: Part 2 — The Transformation Layer (Minh Pham, guest on Vu Trinh's newsletter)](../../raw/email/email-2026-06-25-i-spent-12-hours-rebuilding-my-junior-year-project-part-2-th.md)

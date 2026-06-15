---
type: source
domain: data-engineering
status: draft
sources:
  - path: raw/web/complete-end-to-end-build-of-etl-pipeline-in-aws.md
    channel: web
    ingested_at: 2026-06-11
aliases:
  - DuckDB ETL on Fargate
  - ECS Fargate ETL
  - AWS DuckDB pipeline
tags:
  - corpus/data-engineering
  - source
created: 2026-06-11
updated: 2026-06-11
---

# Source: End-to-End DuckDB ETL on AWS ECS Fargate

**TL;DR**: A full tutorial deploying a modular, reusable ETL pipeline on AWS using **ECS Fargate** + **DuckDB**, provisioned with **Terraform**, scheduled via **EventBridge**, and monitored with **Slack** notifications [^src1].

## Why Fargate over AWS Glue

DuckDB is single-node, so Glue (built for Spark clusters) is the wrong fit — more expensive, and Glue shell jobs are stuck on Python 3.9 (EOL Oct 2025) with limited CPU/RAM and awkward package installs [^src1]. Fargate ("serverless" ECS) lets you control CPU, RAM, ephemeral disk, Python version, and bundled packages via a Docker image [^src1].

## Architecture

- **Docker image** — `amazonlinux 2023` base (ships AWS CLI for DuckDB's `credential_chain` auth) + Python 3.13 + DuckDB 1.5.2 + `httpfs`/`aws` extensions **pre-installed** (orgs often block public-repo access at runtime) [^src1]. Final image ~133 MB [^src1].
- **ECS Task** — analogous to a pipeline; takes the S3 path of an ETL script as a parameter, downloads it via `runner.py` (boto3), and executes it — making the image modular and reusable across scripts [^src1].
- **ECR** — holds the Docker image; **EventBridge** — scheduler; **Secrets Manager** — stores the Slack webhook URL; **CloudWatch Logs** — task stdout; plus IAM roles to pull the image, run the task, and run the scheduler [^src1].
- A separate pre-provisioned Terraform deploy role (`svc-infra-role`) is needed to create the assets; S3 buckets were pre-created (to allow local testing and to hold source dummy data) [^src1].

## The ETL script

Runs an aggregation query against a source Parquet file (TPCH dummy data), then three QA checks — row counts, nulls, and a `total_price < 100` rule. On QA failure it errors and posts a red Slack alert; on pass it writes the result to the destination S3 bucket and posts a green success notification [^src1].

## Observability

A Slack webhook posts success (green), error (red), and info (blue) messages; the webhook URL is secured in Secrets Manager and pulled at runtime via boto3 — the article stresses this as the monitoring layer teams neglect "until they get yelled at by the business" [^src1].

## Deployment & cost

Order: `terraform apply` (as the infra role) → `build_and_deploy.sh` to push the image to ECR. Fargate spins up the task in ~30 seconds [^src1]. Total cost of the full demo run was just under 50 cents (assets destroyed afterward); ECR storage for the 133 MB image is under 10 cents/month [^src1]. The author notes the operational overhead is also why many orgs move to managed platforms like Databricks/Snowflake [^src1].

## See also

- [[data-engineering/parquet|Parquet]] — source/target file format in the pipeline
- [[data-engineering/pipeline-layers|Pipeline Layers]] — ETL staging context
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [Complete End-To-End Build of ETL Pipeline in AWS](../../raw/web/complete-end-to-end-build-of-etl-pipeline-in-aws.md)

---
type: concept
domain: mlops
status: draft
sources:
  - path: raw/web/IaC (Infrastructure-as-Code) fundamentals for data engineers.md
    channel: web
    ingested_at: 2026-06-09
aliases:
  - IaC
  - infrastructure as code
  - infrastructure-as-code
tags:
  - corpus/mlops
  - concept
created: 2026-06-09
updated: 2026-06-09
---

# Infrastructure as Code

**TL;DR**: IaC manages infrastructure through config files instead of manual console clicks or imperative scripts. You declare the desired state; the tool computes and applies the difference against what's currently running. The source's framing: **"IaC is similar to git but for managing infrastructure"** [^src1].

## Why it matters

Data pipelines span many components — S3, Spark, databases, Airflow. Setting these up with `boto3` or the AWS CLI is possible but managing them that way is time-consuming and error-prone. With IaC you modify config files and the tool changes the infrastructure to match [^src1].

## The core loop: desired vs current state

The defining mechanic is **reconciliation** — the tool diffs declared configuration against recorded current state and produces a plan of changes before applying anything [^src1]. In [[mlops/terraform|Terraform]] this is `.tf` files (desired) vs the `.tfstate` file (current); the `plan` command shows the diff, `apply` executes it [^src1].

Change classes to read in a plan [^src1]:

- `~` — in-place update (safe, no cascade)
- `-/+` — destroy and recreate (check downstream cascades)
- `!` — replaced due to an upstream dependency

The tool resolves cascading changes and applies them in dependency order [^src1].

## Environment configuration

Real projects parameterize infrastructure per environment (dev/staging/prod) via variable files rather than hardcoding values, and store shared state in a remote **backend** so a team sees a single source of truth [^src1]. See [[mlops/terraform|Terraform]] for the concrete `.tfvars` + S3-backend mechanics.

## Caveat

A tool only tracks infrastructure *it* created — resources made by other tools or by hand are unmanaged and invisible to its state [^src1]. The source's closing caution: don't blindly prompt an LLM to write infra config — only you have the context for what needs to be built [^src1].

## See also

- [[mlops/terraform|Terraform]] — the IaC tool this concept is taught through
- [[data-engineering/README|Data Engineering]] — IaC provisions the cloud data infrastructure (S3, EC2/EMR) pipelines run on
- [[mlops/README|MLOps hub]]

---

[^src1]: [IaC fundamentals for data engineers](<../../raw/web/IaC (Infrastructure-as-Code) fundamentals for data engineers.md>)

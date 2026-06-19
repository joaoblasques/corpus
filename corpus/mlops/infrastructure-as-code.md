---
type: concept
domain: mlops
status: draft
sources:
  - path: raw/web/IaC (Infrastructure-as-Code) fundamentals for data engineers.md
    channel: web
    ingested_at: 2026-06-09
  - path: raw/youtube/youtube-OGYEXGy8ca4-aws-explained-the-most-important-aws-services-to-know.md
    channel: youtube
    ingested_at: 2026-06-15
  - path: raw/youtube/youtube-ZaA0kNm18pE-cloud-computing-explained-the-most-important-concepts-to-kno.md
    channel: youtube
    ingested_at: 2026-06-15
  - path: raw/youtube/youtube--pX5PjIYTJs-az-900-azure-fundamentals-full-course-2025-azure-complete-tu.md
    channel: youtube
    ingested_at: 2026-06-15
  - path: raw/email/email-2025-08-10-infrastructure-as-code-for-data-engineers.md
    channel: email
    ingested_at: 2026-06-19
aliases:
  - IaC
  - infrastructure as code
  - infrastructure-as-code
  - CloudFormation
  - AWS CDK
  - ARM templates
tags:
  - corpus/mlops
  - concept
created: 2026-06-09
updated: 2026-06-19
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

## The five types of IaC tools

The book *Terraform: Up and Running* (Yevgeniy Brikman) classifies IaC tooling into five categories — a data engineer needn't master all, but should know what each does [^src4]:

1. **Ad-hoc scripts** — the simplest automation: a Bash/Python script doing what you'd otherwise do by hand [^src4].
2. **Configuration management** — Chef, Puppet, **Ansible**: install and manage software on *existing* servers by declaring how each should look [^src4].
3. **Server templating** — **Docker**, Vagrant: bake a reusable image (OS + software + files + settings), a snapshot of a fully set-up machine, then deploy it to many servers [^src4].
4. **Orchestration** — **Kubernetes**, Docker Swarm, Amazon ECS: run containers/VMs *at scale* with auto-healing, auto-scaling, load balancing, and service discovery [^src4]. See [[software-engineering/kubernetes|Kubernetes]].
5. **Provisioning** — **Terraform**, CloudFormation, Pulumi: build the servers/databases/networks *themselves* (vs. configuring what runs on them) [^src4].

This is the historical arc too: from manually racking servers, to CFEngine/Puppet/Chef/Ansible (late-90s→2000s), to the cloud era and the ~2009 rise of "Infrastructure as Code" alongside DevOps [^src4].

## Why data engineers should use IaC

Beyond reproducibility, the data-engineering payoff is concrete [^src4]: **speed & reliability** (spin up warehouses, lakehouse clusters, Kafka topics, S3 buckets, Databricks workspaces in minutes, with no environment drift); **self-service** (no waiting on DevOps to create a Redshift cluster); **living documentation** (the stack lives in versioned code, not someone's head); **version control & instant rollbacks**; **pre-prod validation** of schema/security/policy; **reusable modules** (a compliant S3 bucket, a preconfigured cluster); **faster incident recovery** (recreate the whole stack, lowering MTTR); **governance/security/compliance as code** (encryption, IAM, GDPR/SOC 2/HIPAA policy checks); and **happier teams** with fewer "works on my machine" issues [^src4].

## Declarative vs. imperative (provider-native tools)

The cloud overviews motivate IaC by the pain of clicking through a console: error-prone, hard to replicate to a new region, and unauditable (no code review) [^src2][^src3]. Two flavors recur [^src2][^src3]:

- **Declarative** — describe the desired end state in a template; the provider creates it. **AWS CloudFormation** (YAML/JSON templates) and **Azure ARM templates** (JSON) are examples [^src2][^src3].
- **Imperative / programmatic** — write infra in a real programming language with loops/conditionals. **AWS CDK** (Cloud Development Kit, in Python/TS/Java/etc.) compiles down to CloudFormation and is favored over raw CloudFormation, which "kind of sucks to use" and grows unwieldy [^src2][^src3].

[[mlops/terraform|Terraform]] is the cross-provider third-party option (one tool targeting AWS/Azure/GCP); the AWS-centric source recommends CDK *if you're all-in on AWS*, Terraform for multi-cloud [^src2]. Putting IaC in source control enables code review of infra changes — the discipline IaC exists to provide [^src2][^src3].

## See also

- [[mlops/terraform|Terraform]] — the cross-provider IaC tool this concept is taught through (incl. the local-Docker-platform example)
- [[mlops/aws|AWS]] — CloudFormation/CDK · [[mlops/azure|Azure]] — ARM templates · [[mlops/gcp|GCP]]
- [[mlops/cloud-computing-fundamentals|Cloud Computing Fundamentals]] — IaC sits over the resources defined there
- [[data-engineering/README|Data Engineering]] — IaC provisions the cloud data infrastructure (S3, EC2/EMR) pipelines run on
- [[mlops/README|MLOps hub]]

---

[^src1]: [IaC fundamentals for data engineers](<../../raw/web/IaC (Infrastructure-as-Code) fundamentals for data engineers.md>)
[^src2]: [AWS Explained (Be A Better Dev)](../../raw/youtube/youtube-OGYEXGy8ca4-aws-explained-the-most-important-aws-services-to-know.md#t=54:43) — CloudFormation vs. CDK [[55:35](../../raw/youtube/youtube-OGYEXGy8ca4-aws-explained-the-most-important-aws-services-to-know.md#t=55:35)]
[^src3]: [Cloud Computing Explained (Be A Better Dev)](../../raw/youtube/youtube-ZaA0kNm18pE-cloud-computing-explained-the-most-important-concepts-to-kno.md#t=36:15) — declarative vs. imperative IaC [[39:18](../../raw/youtube/youtube-ZaA0kNm18pE-cloud-computing-explained-the-most-important-concepts-to-kno.md#t=39:18)]; Azure ARM mention from [AZ-900 File2](../../raw/youtube/youtube--pX5PjIYTJs-az-900-azure-fundamentals-full-course-2025-azure-complete-tu.md#t=23:11)
[^src4]: [Infrastructure as Code for Data Engineers (Pipeline to Insights)](../../raw/email/email-2025-08-10-infrastructure-as-code-for-data-engineers.md)

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
  - path: raw/youtube/youtube-iTrxsotFNHA-i-ll-explain-10-years-of-infrastructure-evolution-in-25-minu.md
    channel: youtube
    ingested_at: 2026-06-20
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

The defining mechanic is **reconciliation** — the tool diffs declared configuration against recorded current state and produces a plan of changes before applying anything [^src1]. In [Terraform](/mlops/terraform.md) this is `.tf` files (desired) vs the `.tfstate` file (current); the `plan` command shows the diff, `apply` executes it [^src1].

Change classes to read in a plan [^src1]:

- `~` — in-place update (safe, no cascade)
- `-/+` — destroy and recreate (check downstream cascades)
- `!` — replaced due to an upstream dependency

The tool resolves cascading changes and applies them in dependency order [^src1].

## Environment configuration

Real projects parameterize infrastructure per environment (dev/staging/prod) via variable files rather than hardcoding values, and store shared state in a remote **backend** so a team sees a single source of truth [^src1]. See [Terraform](/mlops/terraform.md) for the concrete `.tfvars` + S3-backend mechanics.

## Caveat

A tool only tracks infrastructure *it* created — resources made by other tools or by hand are unmanaged and invisible to its state [^src1]. The source's closing caution: don't blindly prompt an LLM to write infra config — only you have the context for what needs to be built [^src1].

## The five types of IaC tools

The book *Terraform: Up and Running* (Yevgeniy Brikman) classifies IaC tooling into five categories — a data engineer needn't master all, but should know what each does [^src4]:

1. **Ad-hoc scripts** — the simplest automation: a Bash/Python script doing what you'd otherwise do by hand [^src4].
2. **Configuration management** — Chef, Puppet, **Ansible**: install and manage software on *existing* servers by declaring how each should look [^src4].
3. **Server templating** — **Docker**, Vagrant: bake a reusable image (OS + software + files + settings), a snapshot of a fully set-up machine, then deploy it to many servers [^src4].
4. **Orchestration** — **Kubernetes**, Docker Swarm, Amazon ECS: run containers/VMs *at scale* with auto-healing, auto-scaling, load balancing, and service discovery [^src4]. See [Kubernetes](/software-engineering/kubernetes.md).
5. **Provisioning** — **Terraform**, CloudFormation, Pulumi: build the servers/databases/networks *themselves* (vs. configuring what runs on them) [^src4].

This is the historical arc too: from manually racking servers, to CFEngine/Puppet/Chef/Ansible (late-90s→2000s), to the cloud era and the ~2009 rise of "Infrastructure as Code" alongside DevOps [^src4].

## Why data engineers should use IaC

Beyond reproducibility, the data-engineering payoff is concrete [^src4]: **speed & reliability** (spin up warehouses, lakehouse clusters, Kafka topics, S3 buckets, Databricks workspaces in minutes, with no environment drift); **self-service** (no waiting on DevOps to create a Redshift cluster); **living documentation** (the stack lives in versioned code, not someone's head); **version control & instant rollbacks**; **pre-prod validation** of schema/security/policy; **reusable modules** (a compliant S3 bucket, a preconfigured cluster); **faster incident recovery** (recreate the whole stack, lowering MTTR); **governance/security/compliance as code** (encryption, IAM, GDPR/SOC 2/HIPAA policy checks); and **happier teams** with fewer "works on my machine" issues [^src4].

## Declarative vs. imperative (provider-native tools)

The cloud overviews motivate IaC by the pain of clicking through a console: error-prone, hard to replicate to a new region, and unauditable (no code review) [^src2][^src3]. Two flavors recur [^src2][^src3]:

- **Declarative** — describe the desired end state in a template; the provider creates it. **AWS CloudFormation** (YAML/JSON templates) and **Azure ARM templates** (JSON) are examples [^src2][^src3].
- **Imperative / programmatic** — write infra in a real programming language with loops/conditionals. **AWS CDK** (Cloud Development Kit, in Python/TS/Java/etc.) compiles down to CloudFormation and is favored over raw CloudFormation, which "kind of sucks to use" and grows unwieldy [^src2][^src3].

[Terraform](/mlops/terraform.md) is the cross-provider third-party option (one tool targeting AWS/Azure/GCP); the AWS-centric source recommends CDK *if you're all-in on AWS*, Terraform for multi-cloud [^src2]. Putting IaC in source control enables code review of infra changes — the discipline IaC exists to provide [^src2][^src3].

## 10 years of infrastructure evolution (TechWorld with Nana)

The five-stage journey from console-clicking to AI-driven infrastructure [^src5]:

### Stage 1 — AWS Console (click-ops)
Create resources visually through the web UI. Good for learning (you see VPCs, security groups, subnets in context), but **not repeatable** (can't remember exact settings for a second environment), **not documented**, **error-prone** at scale, and doesn't scale past ~5 servers [^src5].

### Stage 2 — CLI / Python scripts (boto3)
Script AWS API calls. Now repeatable and documentable. But scripts are **stateless** — re-running creates duplicate resources; deleting requires separate delete scripts; updates are manual diffs [^src5]. "You're clicking faster through code, basically."

### Stage 3 — Infrastructure as Code (Terraform, declarative)
Declare desired end-state in `.tf` files; Terraform diffs against `.tfstate` and applies only the delta. Gives you **state management**, **repeatability**, **code review**, and **version history**. Problems: still manually executed (`terraform apply`); **configuration drift** when someone makes a console change; **shared state file** requires locking; team coordination overhead [^src5].

### Stage 4 — GitOps (Argo CD, Flux)
Git is the **single source of truth** for infrastructure; changes to the repo are automatically applied. Eliminates manual `terraform apply`; drift is auto-reverted; full audit trail in git. The mental model shift: infrastructure *pulls* desired state from git rather than a human *pushing* changes [^src5].

### Stage 5 — AI-assisted infrastructure
The emerging layer: AI tools generate IaC from natural language ("create an EC2 instance with port 443 open"), detect drift proactively, suggest cost optimizations, and auto-remediate common misconfigurations. Treats the IaC code generation step as AI-assisted rather than hand-written — but the review and state management disciplines of Stages 3–4 still apply [^src5].

**Progression summary** [^src5]:

| Stage | Tool | Key property added |
|---|---|---|
| Console | AWS web UI | Visual; learnable |
| CLI/scripts | boto3, AWS CLI | Repeatable; documentable |
| IaC | Terraform | State management; code review |
| GitOps | Argo CD, Flux | Auto-reconciliation; drift prevention |
| AI-assisted | LLM + IaC | Config generation; proactive detection |

## See also

- [Terraform](/mlops/terraform.md) — the cross-provider IaC tool this concept is taught through (incl. the local-Docker-platform example)
- [AWS](/mlops/aws.md) — CloudFormation/CDK · [Azure](/mlops/azure.md) — ARM templates · [GCP](/mlops/gcp.md)
- [Cloud Computing Fundamentals](/mlops/cloud-computing-fundamentals.md) — IaC sits over the resources defined there
- [Data Engineering](/data-engineering/README.md) — IaC provisions the cloud data infrastructure (S3, EC2/EMR) pipelines run on
- [MLOps hub](/mlops/README.md)

---

[^src1]: [IaC fundamentals for data engineers](<../../raw/web/IaC (Infrastructure-as-Code) fundamentals for data engineers.md>)
[^src2]: [AWS Explained (Be A Better Dev)](../../raw/youtube/youtube-OGYEXGy8ca4-aws-explained-the-most-important-aws-services-to-know.md#t=54:43) — CloudFormation vs. CDK [[55:35](../../raw/youtube/youtube-OGYEXGy8ca4-aws-explained-the-most-important-aws-services-to-know.md#t=55:35)]
[^src3]: [Cloud Computing Explained (Be A Better Dev)](../../raw/youtube/youtube-ZaA0kNm18pE-cloud-computing-explained-the-most-important-concepts-to-kno.md#t=36:15) — declarative vs. imperative IaC [[39:18](../../raw/youtube/youtube-ZaA0kNm18pE-cloud-computing-explained-the-most-important-concepts-to-kno.md#t=39:18)]; Azure ARM mention from [AZ-900 File2](../../raw/youtube/youtube--pX5PjIYTJs-az-900-azure-fundamentals-full-course-2025-azure-complete-tu.md#t=23:11)
[^src4]: [Infrastructure as Code for Data Engineers (Pipeline to Insights)](../../raw/email/email-2025-08-10-infrastructure-as-code-for-data-engineers.md)
[^src5]: [I'll Explain 10 Years of Infrastructure Evolution in 25 Minutes (TechWorld with Nana)](../../raw/youtube/youtube-iTrxsotFNHA-i-ll-explain-10-years-of-infrastructure-evolution-in-25-minu.md)

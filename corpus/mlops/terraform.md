---
type: entity
domain: mlops
status: draft
sources:
  - path: raw/web/IaC (Infrastructure-as-Code) fundamentals for data engineers.md
    channel: web
    ingested_at: 2026-06-09
  - path: raw/email/email-2025-08-10-infrastructure-as-code-for-data-engineers.md
    channel: email
    ingested_at: 2026-06-19
  - path: raw/web/building-a-local-data-platform-with-terraform-and-docker.md
    channel: web
    ingested_at: 2026-06-19
aliases:
  - Terraform
  - terraform
  - HCL
  - tfstate
  - tfvars
  - OpenTofu
  - HashiCorp Configuration Language
  - Docker provider
tags:
  - corpus/mlops
  - entity
created: 2026-06-09
updated: 2026-06-19
---

# Terraform

**TL;DR**: HashiCorp's IaC tool. Infrastructure is declared in `.tf` files written in HCL (HashiCorp Configuration Language); Terraform compares them against a `.tfstate` record of current infrastructure and applies the difference [^src1]. The concrete instance of [[mlops/infrastructure-as-code|Infrastructure as Code]].

## Config file building blocks

A `.tf` file is composed of four main component types [^src1]:

| Component | Purpose |
|---|---|
| **Provider** | the vendor/system to work with (AWS, GCP, local FS) — like the library for that system |
| **Resource** | infrastructure to create (S3, EC2, EMR) |
| **Data** | reads information from a provider to use elsewhere (e.g. look up an AMI ID) |
| **Output** | prints information (e.g. an EC2 instance ID) |

## CLI workflow

```bash
terraform -chdir=terraform init      # download required_providers
terraform -chdir=terraform validate  # validate .tf files
terraform -chdir=terraform fmt       # format .tf files
terraform -chdir=terraform plan      # compute the change plan
terraform -chdir=terraform apply     # show plan, ask approval, apply
terraform -chdir=terraform destroy   # tear everything down
```

The CLI reads all `.tf` files in the working directory; `-chdir` points it at the conventional `terraform/` folder [^src1]. **Always `destroy` when done** to avoid lingering cloud cost [^src1].

## State

`.tfstate` records active infrastructure. Inspect it with `terraform state list` or directly:

```bash
terraform -chdir=terraform state list
```

`apply` diffs `.tf` (desired) against `.tfstate` (current) to build its plan [^src1]. Terraform only tracks what it created — anything made by other tools is unmanaged [^src1].

## Variables and environments

- **`variables.tf`** declares allowed variables and defaults.
- **`envs/<env>.tfvars`** supplies per-environment values; pass with `-var-file=envs/dev.tfvars` [^src1].

## Remote backend

For team collaboration, store state in a shared **backend** (e.g. S3) so changes reflect in one place [^src1]:

```hcl
backend "s3" {
  bucket  = "your-backend-state-bucket"
  key     = "dev/terraform.tfstate"
  region  = "us-east-1"
  encrypt = true
}
```

Re-run `init` after adding a backend to migrate state [^src1].

## Conventional layout

```
.
└── terraform
    ├── bootstrap.sh      # creates the backend S3 bucket
    ├── envs/dev.tfvars   # environment-specific variables
    ├── main.tf           # key infrastructure
    └── variables.tf      # allowed variables + defaults
```

## Declarative vs. imperative

Terraform takes the **declarative** approach: you describe the *desired end state* and the tool computes the route to get there — like telling a navigator the destination rather than giving **imperative** turn-by-turn directions where every manual step must be correct [^src2]. Its 3-step workflow embodies this: **Code** (write `.tf` blueprint) → **Plan** (`terraform plan` diffs current vs desired, shows what it will create/change/destroy without touching anything) → **Apply** (`terraform apply` calls provider APIs and builds it) [^src2]. Because state is reconciled, re-running after adding one resource (e.g. Azure Databricks alongside existing ADLS/ADF/DB/Key Vault) creates *only* the new resource — preventing configuration drift [^src2].

## Modules & providers

Terraform is **modular and pluggable** [^src2]:

- **Modules** group related resources, accept input variables, and return outputs — reusable building blocks that plug into larger systems.
- **Providers** connect Terraform to a target: IaaS (AWS/Azure/GCP), PaaS (Cloud Foundry), even SaaS (Cloudflare). So Terraform's reach now spans infrastructure, platforms, and SaaS [^src2].

## Licensing: BSL and OpenTofu

Terraform was originally **MPL** (true open source). In **August 2023** HashiCorp relicensed it to the **Business Source License (BSL)** — "source available," not OSI-approved: free to see/use in most cases, but you can't use it to offer a competing paid service [^src2]. The last truly open-source version is **v1.5.x**; **OpenTofu** is the community fork that stays under an open-source license [^src2]. Terraform ships in three editions: Community, HCP Terraform (hosted SaaS), and Terraform Enterprise (self-hosted) [^src2]. The tool is written in **Go** and distributed as a single binary; configs are written in **HCL** [^src2]. The classic reference is *Terraform: Up and Running* by Yevgeniy Brikman [^src2].

## Beyond the cloud: provisioning local Docker infra

The **`provider` abstraction isn't cloud-only** — Terraform can target the **Docker provider** to declaratively provision a *local* data platform [^src3]. A worked example builds a free local analogue of a cloud data stack: Terraform modules (`airflow/`, `localstack/`, `minio/`) each declare a container, image, and volumes, plus a dedicated **Docker network** so containers reach each other by hostname (`http://minio:9000`) instead of dynamic IPs [^src3]. Terraform even **builds custom Docker images** as part of `apply` (e.g. an Airflow image with boto3 + duckdb baked in, an ETL image whose `context = ".."` reaches scripts at the project root) — so provisioning containers/networks *and* building the application images they depend on are all declarative [^src3]. The cloud-service → local-tool mapping: S3→Minio, Lambda→Docker containers, MWAA→Dockerized Airflow, SQS/SNS→LocalStack, Redshift/BigQuery→[[data-engineering/duckdb|DuckDB]] [^src3]. The IaC payoff is identical to cloud use — one `terraform apply` reproduces the whole stack, `destroy` tears it down [^src3]. See [[data-engineering/de-portfolio-projects|DE Portfolio Projects]] for this as a portfolio piece.

## See also

- [[mlops/infrastructure-as-code|Infrastructure as Code]] — the general pattern; the five types of IaC tools
- [[data-engineering/cicd-for-data-infrastructure|CI/CD for Data Infrastructure]] — Terraform plan→gate→apply in a pipeline
- [[data-engineering/de-portfolio-projects|DE Portfolio Projects]] — the local-platform project as a portfolio piece
- [[mlops/README|MLOps hub]]

---

[^src1]: [IaC fundamentals for data engineers](<../../raw/web/IaC (Infrastructure-as-Code) fundamentals for data engineers.md>)
[^src2]: [Infrastructure as Code for Data Engineers (Pipeline to Insights)](../../raw/email/email-2025-08-10-infrastructure-as-code-for-data-engineers.md)
[^src3]: [Building a Local Data Platform with Terraform and Docker (p-munhoz)](../../raw/web/building-a-local-data-platform-with-terraform-and-docker.md)

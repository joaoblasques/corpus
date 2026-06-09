---
type: entity
domain: mlops
status: draft
sources:
  - path: raw/web/IaC (Infrastructure-as-Code) fundamentals for data engineers.md
    channel: web
    ingested_at: 2026-06-09
aliases:
  - Terraform
  - terraform
  - HCL
  - tfstate
  - tfvars
tags:
  - corpus/mlops
  - entity
created: 2026-06-09
updated: 2026-06-09
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

## See also

- [[mlops/infrastructure-as-code|Infrastructure as Code]] — the general pattern
- [[mlops/README|MLOps hub]]

---

[^src1]: [IaC fundamentals for data engineers](<../../raw/web/IaC (Infrastructure-as-Code) fundamentals for data engineers.md>)

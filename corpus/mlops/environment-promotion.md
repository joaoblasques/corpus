---
type: synthesis
domain: mlops
status: draft
sources:
  - path: raw/email/email-2025-08-04-ci-cd-deployment-strategies.md
    channel: email
    ingested_at: 2026-06-19
  - path: raw/web/how-to-set-up-ci-cd-for-data-infrastructure-start-data-engin.md
    channel: web
    ingested_at: 2026-06-15
  - path: raw/email/email-2025-08-03-lecture-7-databricks-asset-bundles.md
    channel: email
    ingested_at: 2026-06-19
aliases:
  - environment promotion
  - dev acc prd
  - dev staging prod
  - deployment promotion
  - environment-scoped deployment
  - human approval gate
tags:
  - corpus/mlops
  - synthesis
created: 2026-06-23
updated: 2026-06-23
confidence: 0.8
last_confirmed: 2026-06-23
---

# Environment Promotion (dev → acc → prd)

**TL;DR.** Independently across ML CI/CD, data-infrastructure CI/CD, and Databricks packaging, the same deployment discipline recurs: **changes are authored only in `dev`, promoted automatically through `acc`/staging, and reach `prd` only behind an automated check plus a human approval gate, executed by a non-human identity — never a person pushing to prod.** This page names that cross-source pattern and maps its four invariants onto each source. It generalizes [CI/CD for ML](/mlops/ci-cd-for-ml.md), [CI/CD for Data Infrastructure](/data-engineering/cicd-for-data-infrastructure.md), and [Databricks Asset Bundles](/mlops/databricks-asset-bundles.md).

## The four invariants

**1. Humans touch only `dev`; higher environments are reached through pipelines.** On Databricks, "users only have direct access to the dev workspace; deployments to acc/prd must go through CI/CD pipelines" [^src1]. The data-infra equivalent: at least **dev** (open access, validate) and **production** (restricted, real workloads), with prod reached only via CD [^src2].

**2. Environment-scoped state/assets, isolated by default.** ML uses a **three-tier Unity Catalog** with environment catalogs (`mlops_dev` / `mlops_acc` / `mlops_prd`); each workspace can only *write* to its own catalog while all can *read* prod data for consistency, with **ISOLATED** workspace binding to control cross-project access [^src1]. Data-infra uses **separate Terraform state per environment** — the backend `key` switches between `dev/terraform.tfstate` and `prod/terraform.tfstate` [^src2]. DAB expresses the same idea declaratively as **`targets`** (`dev` / `acc` / `prd`), each with its own `mode` (`development` vs `production`) in `databricks.yml` [^src3].

**3. CI checks + a plan; CD applies dev-first, then a human-gated prod step.** The data-infra skeleton is explicit: **CI** runs `fmt`/`validate` and a *plan* against dev posted to the PR for review; **CD** applies to dev automatically on merge, then a **second job gated by required reviewers** on a GitHub `environment: production` waits for manual approval before applying to prod [^src2]. ML CI/CD mirrors it with **Git Flow + branch protection**: PRs to `main` trigger CI (pre-commit, unit tests, version checks), **≥2 approvals** are required to merge, and prod deployment is guarded by **deployment protection rules** [^src1]. DAB's deploy step adds an in-pipeline quality gate of its own — a **`condition_task`** that deploys the model only if it improved [^src3].

**4. A non-human identity executes the deployment.** ML CI/CD uses a **Service Principal** — "a special, non-human identity used by applications, automation tools, or CI/CD pipelines" — for security (not tied to a person), least privilege, auditability, and automation; credentials live in environment-scoped secrets [^src1]. Data-infra uses **OIDC to assume an AWS role** rather than long-lived user keys [^src2]. The principle is identical: deployments are attributable to a scoped machine identity, not a developer's account.

## Mapping table

| Invariant | CI/CD for ML (Databricks) [^src1] | CI/CD for Data Infra (Terraform) [^src2] | Databricks Asset Bundles [^src3] |
|---|---|---|---|
| Human-only-in-dev | direct access only to dev workspace | dev open, prod restricted | `mode: development` vs `production` targets |
| Env-scoped state | UC catalogs `mlops_{dev,acc,prd}` | separate `*.tfstate` per env | `targets:` per environment |
| CI check + gated CD | Git Flow, ≥2 approvals, deployment protection rules | plan-on-PR → apply(dev) → human-gated apply(prod) | `databricks bundle deploy` + `condition_task` gate |
| Machine identity | Service Principal (OAuth client-credentials) | OIDC-assumed AWS role | (runs under the pipeline's SPN) |

## Why it matters

- **One mental model, many tools.** Whether the payload is a Terraform plan, a model wheel, or a dbt project, the *shape* is the same — so map any intimidating pipeline onto **CI (check + plan) → CD (apply dev → gate → apply prod)** and it falls into place [^src2].
- **The gate is where high-impact change is made safe.** Infra and prod model deployments are high-blast-radius, which is exactly why every source converges on an explicit human approval before prod rather than auto-applying [^src1][^src2].
- **`databricks bundle deploy` is the seam.** DAB is the deployment *payload* that ML CI/CD invokes per environment via a strategy matrix — the packaging layer and the promotion layer compose [^src1][^src3].

## Related

- [CI/CD for ML](/mlops/ci-cd-for-ml.md) — Unity Catalog tiers + Service Principals + Git Flow (the ML instance)
- [CI/CD for Data Infrastructure](/data-engineering/cicd-for-data-infrastructure.md) — the data-infra sibling: plan-on-PR → gated prod apply
- [Databricks Asset Bundles](/mlops/databricks-asset-bundles.md) — declarative `targets` + the deploy payload
- [Databricks Development](/mlops/databricks-development.md) — where the dev/acc/prd catalog split originates
- [Terraform](/mlops/terraform.md) · [Infrastructure as Code](/mlops/infrastructure-as-code.md) — the IaC substrate both CI/CD flows apply
- [MLOps hub](/mlops/README.md)

---

[^src1]: [CI/CD & Deployment Strategies (Marvelous MLOps, Lecture 8)](../../raw/email/email-2025-08-04-ci-cd-deployment-strategies.md)
[^src2]: [How to set up CI/CD for data infrastructure](../../raw/web/how-to-set-up-ci-cd-for-data-infrastructure-start-data-engin.md)
[^src3]: [Databricks Asset Bundles (Marvelous MLOps, Lecture 7)](../../raw/email/email-2025-08-03-lecture-7-databricks-asset-bundles.md)
</content>

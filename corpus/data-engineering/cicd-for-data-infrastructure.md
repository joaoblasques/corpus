---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/email/email-2026-06-03-ci-cd-patterns-to-deploy-infra-changes.md
    channel: email
    ingested_at: 2026-06-15
  - path: raw/web/how-to-set-up-ci-cd-for-data-infrastructure-start-data-engin.md
    channel: web
    ingested_at: 2026-06-15
  - path: raw/web/build-data-engineering-projects-with-free-template-start-dat.md
    channel: web
    ingested_at: 2026-06-19
aliases:
  - CI/CD for data infrastructure
  - data infrastructure CI/CD
  - infrastructure CI/CD
  - deploy infra changes
tags:
  - corpus/data-engineering
  - concept
created: 2026-06-15
updated: 2026-06-19
---

# CI/CD for Data Infrastructure

**TL;DR.** With the right CI/CD system, deploying data-infrastructure changes becomes "as easy as a code change" [^src2]. The core insight: *AI can write CI/CD YAML, but it cannot design the pipeline for your use case* — you need to understand the pattern [^src1]. The standard pattern: **CI** runs static checks + a *plan* (no apply) and posts it to the PR for human review; **CD** applies to dev automatically on merge, then requires a **manual human approval gate** before applying to production [^src1].

## Why it's worth designing well

Updating pipeline infrastructure risks bringing down prod [^src2]. A good CI/CD flow lets changes flow seamlessly, multiplying delivery speed [^src1]. The reference uses **GitHub Actions** (free tier, easier than Jenkins; steps run on ephemeral/serverless VMs) with **[[mlops/terraform|Terraform]]** for the infrastructure-as-code (see [[mlops/infrastructure-as-code|Infrastructure as Code]], owned by mlops) [^src1].

## CI — make the PR ready for human review

CI runs automated checks so the PR passes everything automatable before a human looks [^src1]. For infra changes specifically [^src1]:

1. **Format checks** (`terraform fmt -check`).
2. **Validation** of the IaC files (`terraform validate`).
3. **Plan** the change against the **dev** state and **post the plan as a PR comment** for review.

CI generally does *not* make infra changes — though some teams create temporary full environments to run checks (dbt's CI does a version of this by creating PR-specific schemas) [^src1]. The workflow triggers on `pull_request` to `main`, uses OIDC to assume an AWS role (`id-token: write`), and needs `pull-requests: write` to comment the plan [^src1].

## CD — deploy across environments

Companies typically have at least **dev** (open access, validate) and **production** (restricted, real workloads) [^src1].

**On PR merge to `main`** the CD job [^src1]:
1. **Applies** infra changes to **dev** (`terraform apply -auto-approve` against the dev state key).
2. **Re-inits against the prod state** (`-reconfigure`) and **plans prod** for review (written to the GitHub step summary).

Then a **second job, gated by required reviewers** on a GitHub `environment: production`, waits for manual approval before `terraform apply` to prod [^src1].

```
PR opened ─► CI: fmt + validate + plan(dev) → comment on PR ─► human review
   merge   ─► CD job 1: apply(dev) + plan(prod) ─► CD job 2 (gated): human approval ─► apply(prod)
```

## Key design choices

- **Separate state per environment** — the backend `key` switches between `dev/terraform.tfstate` and `prod/terraform.tfstate` via partial backend config + `-reconfigure` [^src1].
- **Human gate for prod** — infra changes are high-impact, so production deploys require manual human review (the GitHub `environment` required-reviewers feature) [^src1].
- **Follow-up PRs for dependent code** — code that depends on new infrastructure is deployed in a *follow-up* PR after the infra exists [^src1].
- **Failure tradeoff** — if an infra change fails, you must quickly fix-forward or revert; in the interval other team members are blocked. Since most teams rarely change infra, this is an acceptable tradeoff [^src1].

## The concrete toolchain (portfolio template)

A reference data-project template wires this skeleton with a standard stack [^src3]: **GitHub-flow** branching, **GitHub Actions** for both CI and CD, and a **Makefile** of command aliases. CI runs **isort + black** (formatting), **flake8** (lint/style), **mypy** (type check), and **pytest** (tests) automatically on each pull request before merge to `main` [^src3]. CD then copies the merged code to an **EC2** Docker host, using repository secrets (`SERVER_SSH_KEY`, `REMOTE_HOST`, `REMOTE_USER`) whose values come from **Terraform outputs** — concretely tying the CD step to the IaC layer [^src3]. See [[data-engineering/de-portfolio-projects|DE Portfolio Projects]] for the full template.

## Takeaway

Map any intimidating 1000-line Terraform file or complex YAML workflow onto this **CI (check + plan) → CD (apply dev → gate → apply prod)** skeleton and it falls into place [^src1]. Understanding the *design* is what lets you leverage AI effectively rather than blindly running its generated YAML [^src1].

## Related

- [[mlops/terraform|Terraform]] · [[mlops/infrastructure-as-code|Infrastructure as Code]] — the IaC layer (mlops)
- [[data-engineering/data-engineering-best-practices|Data Engineering Best Practices]] — testing & version control
- [[data-engineering/dbt|dbt]] — slim CI for dbt models (PR-specific schemas)
- [[data-engineering/data-migration-at-scale|Data Migration at Scale]] — safe rollout/rollback patterns
- [[data-engineering/de-portfolio-projects|DE Portfolio Projects]] — the template that ships this CI/CD toolchain
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [How to set up CI/CD for data infrastructure](../../raw/web/how-to-set-up-ci-cd-for-data-infrastructure-start-data-engin.md)
[^src2]: [CI/CD patterns to deploy infra changes (newsletter)](../../raw/email/email-2026-06-03-ci-cd-patterns-to-deploy-infra-changes.md)
[^src3]: [Build Data Engineering Projects with a Free Template](../../raw/web/build-data-engineering-projects-with-free-template-start-dat.md)

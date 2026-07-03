---
type: concept
domain: mlops
status: draft
sources:
  - path: raw/email/email-2025-08-03-lecture-7-databricks-asset-bundles.md
    channel: email
    ingested_at: 2026-06-19
aliases:
  - Databricks Asset Bundles
  - DAB
  - asset bundles
  - databricks.yml
  - lakeflow jobs
  - databricks workflows
  - databricks bundle
tags:
  - corpus/mlops
  - concept
created: 2026-06-19
updated: 2026-06-19
---

# Databricks Asset Bundles (DAB)

**TL;DR.** A Databricks Asset Bundle packages your code, jobs, configuration, and dependencies together in a structured, version-controlled format defined with YAML files [^src1]. When deploying resources on Databricks you have three options — raw **[Terraform](/mlops/terraform.md)** (full IaC control but complex), **Databricks APIs** (flexible but needs custom scripting), or **DAB** (the recommended declarative YAML approach) [^src1]. DAB strikes a balance: *"Under the hood, it leverages Terraform, so you get all the benefits of infrastructure-as-code, without having to manage raw Terraform code yourself"* [^src1]. This page covers the `databricks.yml` structure, Lakeflow Jobs, resource job definitions with task dependencies, and the bundle CLI lifecycle.

## Why DAB (vs Terraform vs raw APIs)

The deployment-tooling tradeoff [^src1]:

| Option | Tradeoff |
|---|---|
| Terraform | Full infrastructure-as-code control, but can be complex |
| Databricks APIs | Flexible, but requires custom scripting |
| Databricks Asset Bundles | Recommended, declarative, YAML-based |

DAB `depends-on` Terraform internally, giving IaC benefits without raw TF [^src1]. Its key features: declarative YAML config (everything in one place), multi-environment support (dev/staging/prod), CI/CD friendliness, and version control of all changes in the repo [^src1]. See [Infrastructure as Code](/mlops/infrastructure-as-code.md) for the underlying declarative model.

## Lakeflow Jobs (orchestration)

**Lakeflow Jobs** (previously Databricks Workflows) provide the execution and orchestration layer: run tasks (notebooks, scripts, SQL) on a schedule or in response to events, with dependencies, retries, parameter passing, and alerts [^src1]. DAB packages the code; Lakeflow Jobs run it.

## `databricks.yml` structure

The bundle config lives in `databricks.yml`; the minimal form contains only a bundle name and target [^src1]. The course's file has these sections [^src1]:

- **`bundle`** — the bundle name (`marvel-characters`).
- **`include`** — pulls in resource definitions (`resources/*`); the main file itself contains no resources.
- **`artifacts`** — how code is packaged (`type: whl`, `build: uv build`); the packaged wheel is referenced by resources.
- **`variables`** — shared variables (`git_sha`, `branch`, `schedule_pause_status`), definable per target or passed at deploy time.
- **`targets`** — deployment targets mapping to separate environments (`dev`, `acc`, `prd`), each with its own settings and `mode` (`development` / `production`).

```yaml
bundle:
  name: marvel-characters
include:
  - resources/*
artifacts:
  default:
    type: whl
    build: uv build
    path: .
targets:
  dev:
    default: true
    mode: development
  prd:
    mode: production
```

The build uses **[uv](/mlops/uv.md)** (`uv build`) to produce the wheel [^src1].

## ML pipeline as a resource job

Resources are defined as separate `.yml` files under `resources/`, pulled in via `include` [^src1]. The `resources/model_deployment.yml` file defines the ML workflow as a Databricks job with tasks, a Quartz cron schedule, an environment spec (`client: "3"`, wheel dependency `../dist/*.whl`), and **`depends_on`** wiring [^src1]:

1. **preprocessing** — runs `scripts/process_data.py`.
2. **train_model** — `depends_on: preprocessing`; trains/evaluates the model via `scripts/train_register_custom_model.py`.
3. **model_updated** — a **`condition_task`** (`EQUAL_TO` on `{{tasks.train_model.values.model_updated}} == "1"`): only proceed if the new model is better [^src1].
4. **deploy_model** — `depends_on: model_updated` with `outcome: "true"`; deploys the registered model by creating/updating a serving endpoint via `scripts/deploy_model.py` [^src1].

Parameters are passed between tasks using DAB templating (e.g. `--root_path ${workspace.root_path}`, `--env ${bundle.target}`, `--git_sha ${var.git_sha}`, `{{job.run_id}}`) [^src1]. The conditional `model_updated` gate means deployment only happens *if the model improved*, with the train step setting `dbutils.jobs.taskValues` to flag `model_updated` [^src1]. This is the same train→register→deploy flow that uses [MLflow](/mlops/mlflow.md) and [Model Serving](/mlops/model-serving.md).

## Managing bundles (CLI lifecycle)

The Databricks CLI drives the bundle lifecycle [^src1]:

```bash
databricks bundle validate   # validate the bundle
databricks bundle deploy     # deploy the bundle (builds the wheel)
databricks bundle run        # run the job
databricks bundle destroy    # tear down resources
```

Once deployed, the workflow appears in the target workspace [^src1]. With DAB you can package all logic/dependencies/configs in one place, define robust multi-step ML workflows, version and automate deployments per environment, and achieve reproducibility and CI/CD best practices [^src1].

## See also

- [Terraform](/mlops/terraform.md) — the IaC tool DAB wraps under the hood
- [Infrastructure as Code](/mlops/infrastructure-as-code.md) — the declarative desired-state model DAB embodies
- [CI/CD for ML](/mlops/ci-cd-for-ml.md) — `databricks bundle deploy` is the CD pipeline's deployment step
- [uv](/mlops/uv.md) — `uv build` produces the deployed wheel
- [MLflow](/mlops/mlflow.md) · [Model Serving](/mlops/model-serving.md) — the train/register/deploy steps the DAB job orchestrates
- [Databricks](/data-engineering/databricks.md) — the platform
- [MLOps hub](/mlops/README.md)

---

[^src1]: [Databricks Asset Bundles (Marvelous MLOps, Lecture 7)](../../raw/email/email-2025-08-03-lecture-7-databricks-asset-bundles.md)
</content>

---
type: concept
domain: mlops
status: draft
sources:
  - path: raw/email/email-2025-07-28-introduction-to-mlops.md
    channel: email
    ingested_at: 2026-06-19
aliases:
  - MLOps
  - MLOps principles
  - machine learning operations
  - MLOps vs DevOps
tags:
  - corpus/mlops
  - concept
created: 2026-06-19
updated: 2026-06-19
---

# MLOps Principles

**TL;DR** — MLOps is the discipline of deploying and maintaining ML models in production reliably and efficiently. Its organizing principle is **traceability and reproducibility**: for any model run you should be able to recover the exact code, environment, data, and artifacts behind it. It is *not* a tool stack — it is a set of principles supported by **categories** of tooling, most of which an org already has. It extends DevOps to ML's extra challenge: a model's behavior can change from a shift in the *data* alone, so data monitoring and retraining are core, not extras [^src1].

## What "production" actually means

A model is in production when its outputs are **consistently delivered to end users or systems and drive real business value** — not when it is "deployed" in any narrow technical sense [^src1]. The source's worked example: a data scientist builds a demand-forecasting model in a Databricks notebook, schedules it weekly, and writes predictions to a Delta table the fulfillment team uses to order products. That *is* production (outputs drive decisions) and it is somewhat efficient (scheduled, not manual) — but it is **not reliable**: no testing, monitoring, error handling, version control, or formal deployment, so a break in the data, code, or environment yields no alert, no rollback, no audit trail [^src1]. MLOps exists to close exactly those gaps.

## The core principle: traceability & reproducibility

The main principle of MLOps is that for any model deployment or run you can unambiguously look up [^src1]:

- the corresponding **code / commit** on git,
- the **infrastructure / environment** used for training and serving,
- the **data** used for training,
- the generated **model artifacts**.

> "MLOps is a paradigm that aims to deploy and maintain machine learning models in production reliably and efficiently." [^src1]

## Supporting principles

Beyond traceability, the source names three further pillars that make ML systems robust, maintainable, and collaborative [^src1]:

- **Documentation** — business goals, KPIs, architectural decisions, and model-selection rationale; ensures continuity across onboarding, handovers, and cross-team integration.
- **Code quality** — code review on all PRs, style/structure conventions, and automated testing (unit, integration, and ideally ML-specific tests). Makes experimentation safer and deployments more reliable.
- **Monitoring** — extends beyond system metrics to **model performance**: offline evaluation metrics tracked over time, plus production business KPIs and model cost. Surfaces unintended outcomes early. See [[mlops/model-monitoring|Model Monitoring]] and [[mlops/drift-detection|Drift Detection]] for the mechanics.

## Tooling: think in categories, not products

Following the principles needs tooling, but the source's key claim is **you need *categories* of tools, not specific ones** — and your org likely already has most of them. Each category exists to *support a principle*, so the goal is covering capabilities, not collecting tools [^src1].

| Category | Example tools | What it enables |
|---|---|---|
| Version control | GitHub, GitLab, Bitbucket | code reproducibility + traceability, code quality |
| CI/CD | Jenkins, GitHub Actions, GitLab CI/CD, Azure DevOps | automated testing, packaging, deployment |
| Orchestration | Apache Airflow, Argo Workflows, Lakeflow Jobs | coordinate multi-step ML workflows |
| Model registry | MLflow, Comet | model versioning + metadata → model traceability |
| Feature store / data versioning | Feast, Hopsworks, Databricks feature store | consistent feature definitions across train/inference → data traceability |
| Compute & serving | Databricks, SageMaker, Kubernetes, REST endpoints | support both dev and production needs |
| Monitoring | Prometheus, Grafana, ELK + custom ML metrics | observability of system + model |
| Container registry | DockerHub, Azure Container Registry, AWS ECR | environment traceability via reproducible images |

The mapping the source draws: version control + orchestration + CI/CD → code reproducibility/traceability and code quality; model registry → model traceability; feature store + data versioning → data traceability; container registry → environment traceability [^src1]. "A simple, purpose-driven stack is all you need to do MLOps well." [^src1]

Several of these categories have dedicated corpus pages: [[mlops/git|Git]] (version control), [[mlops/ci-cd-for-ml|CI/CD for ML]], [[mlops/mlflow|MLflow]] (model registry), [[data-engineering/data-orchestration|Data Orchestration]] / [[data-engineering/kafka|orchestration tooling]], and [[mlops/model-serving|Model Serving]] (compute & serving).

## MLOps vs DevOps

MLOps **builds on** DevOps but adapts it to ML's challenges [^src1]:

- **Same goal, thicker wall.** DevOps breaks the wall between development and IT operations for faster, more reliable delivery. MLOps shares the goal, but the wall is "thicker and taller": ML teams focus on experimentation/modeling, platform teams on infrastructure/reliability, and the two often speak different technical languages [^src1].
- **The deeper difference: data.** In traditional software, consistent code + infrastructure + environment yield consistent results. In ML, a change in the **statistical properties of the data alone** can change behavior — which is why **data monitoring and retraining are core to MLOps**, not operational extras [^src1]. This is a typed *extends* relationship: MLOps ⊃ DevOps + data-awareness.

## MLOps on a managed platform (Databricks framing)

The source argues the build-your-own-platform advice is now dated given the "tooling explosion" in data/AI; the value of a managed platform is having everything **tightly integrated**, even if no single component is best-in-class [^src1]. Its Databricks mapping of MLOps functions [^src1]:

- **Lakeflow Jobs** → orchestration
- **MLflow** (experiment tracking) + **Unity Catalog** (model registry)
- **Delta Tables** → data versioning, also powering feature tables
- **Databricks Compute** → model training
- **Feature Serving / Model Serving** → real-time inference
- **Lakehouse Monitoring** → data + model drift detection
- **Databricks Asset Bundles** → CI/CD and deployment

These map onto existing corpus pages: [[data-engineering/databricks|Databricks]], [[mlops/mlflow|MLflow]], [[mlops/databricks-asset-bundles|Databricks Asset Bundles]], [[mlops/model-serving|Model Serving]], [[mlops/model-monitoring|Model Monitoring]], and [[mlops/ci-cd-for-ml|CI/CD for ML]].

## Context

This page is the foundational "what is MLOps" entry for the domain; the [[mlops/README|MLOps hub]] tool/practice pages are the specific capabilities this overview frames. It is lecture 1 of the Marvelous MLOps "End-to-end MLOps with Databricks" course (Databricks Free Edition); lectures 2–10 (developing on Databricks, MLflow, model serving, Asset Bundles, CI/CD, monitoring) were ingested previously and live in the pages linked above.

[^src1]: [Introduction to MLOps (Marvelous MLOps)](../../raw/email/email-2025-07-28-introduction-to-mlops.md)

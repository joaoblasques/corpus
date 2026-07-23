---
type: concept
domain: mlops
status: draft
sources:
  - path: raw/email/email-2025-07-28-introduction-to-mlops.md
    channel: email
    ingested_at: 2026-06-19
  - path: raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-devops-from-zero-report.md
    channel: notes
    ingested_at: 2026-06-25
  - path: raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-i-wasted-2-years-report.md
    channel: notes
    ingested_at: 2026-06-25
  - path: raw/_inbox/pdf-practitioners-guide-to-mlops.md
    channel: pdf
    ingested_at: 2026-07-23
aliases:
  - MLOps
  - MLOps principles
  - machine learning operations
  - MLOps vs DevOps
  - DevOps loop
  - concepts over tools
tags:
  - corpus/mlops
  - concept
created: 2026-06-19
updated: 2026-07-23
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
- **Monitoring** — extends beyond system metrics to **model performance**: offline evaluation metrics tracked over time, plus production business KPIs and model cost. Surfaces unintended outcomes early. See [Model Monitoring](/mlops/model-monitoring.md) and [Drift Detection](/mlops/drift-detection.md) for the mechanics.

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

Several of these categories have dedicated corpus pages: [Git](/mlops/git.md) (version control), [CI/CD for ML](/mlops/ci-cd-for-ml.md), [MLflow](/mlops/mlflow.md) (model registry), [Data Orchestration](/data-engineering/data-orchestration.md) / [orchestration tooling](/data-engineering/kafka.md), and [Model Serving](/mlops/model-serving.md) (compute & serving).

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

These map onto existing corpus pages: [Databricks](/data-engineering/databricks.md), [MLflow](/mlops/mlflow.md), [Databricks Asset Bundles](/mlops/databricks-asset-bundles.md), [Model Serving](/mlops/model-serving.md), [Model Monitoring](/mlops/model-monitoring.md), and [CI/CD for ML](/mlops/ci-cd-for-ml.md).

## The DevOps loop (foundational model)

Before MLOps, the parent concept: the **DevOps infinity loop** — eight continuous stages [^src2]:

**Plan → Code → Build → Test → Release → Deploy → Operate → Monitor**

CI/CD automates Build + Test + Release + Deploy. Monitoring closes the loop (Operate + Monitor feeding back into Plan). MLOps extends this loop with a *data track* running alongside the code track — the same stages apply to data pipelines and model artifacts, not only application code.

See [DevOps Learning Roadmap](/mlops/devops-learning-roadmap.md) for the practitioner's path through these concepts.

## Concepts-over-tools principle

From DevOps practitioners with >10 years of experience: "Tools come and go. Concepts, however, stay forever." [^src3] The durability hierarchy:

1. **Concepts** — pipeline, declarative IaC, state management, compute/storage/network — transfer across any tool or cloud.
2. **Categories** — CI/CD, orchestration, monitoring, IaC — persist across tool generations.
3. **Tools** — Jenkins → GitHub Actions → Argo CD → next thing — change most frequently.

MLOps' emphasis on *categories of tools* (above) applies the same logic within ML engineering [^src1][^src3].

## The deployment gap (industry data)

Google's 2021 whitepaper quantified the operationalization bottleneck: only 1 in 2 organizations had moved beyond pilots and proofs of concept; 72% of organizations that began AI pilots before 2019 had not deployed even a single application in production; 55% of companies surveyed by Algorithmia had not deployed an ML model. [^src4] Root causes: manual one-off work, no reusable components, difficult data-scientist-to-IT handoffs, lack of talent, and lack of governance. McKinsey identified having standard frameworks and development processes as a differentiating factor of high-performing ML teams. [^src4]

## The MLOps lifecycle (seven phases)

Google's canonical decomposition [^src4] (non-waterfall; phases can be skipped or repeated):

1. **ML development** — experimenting to produce a reproducible training pipeline; primary output is either a registered model (if no ongoing retraining needed) or a continuous training pipeline implementation.
2. **Training operationalization** — CI/CD to package, test, and deploy the training pipeline to a target execution environment.
3. **Continuous training** — orchestrated, automated pipeline execution triggered by schedule, new data, model decay detection, or ad hoc invocation.
4. **Model deployment** — packaging, testing, and progressive delivery of the model to a serving environment.
5. **Prediction serving** — online, streaming, batch, or embedded inference.
6. **Continuous monitoring** — detecting effectiveness decay (data/concept drift) and efficiency degradation (latency, throughput, error rates).
7. **Data and model management** — cross-cutting governance for auditability, traceability, compliance, and asset reuse.

## Training-serving skew

A key production failure mode: "discrepancies between serving data and training data... can occur because the data is extracted from different sources in different forms during training and serving." [^src4] The primary mitigation is a unified feature and dataset repository that serves both the training pipeline and the online inference engine from a single data source, ensuring consistent feature definitions and transformations.

## Model governance

Governance is the process of registering, reviewing, validating, and approving models before deployment. [^src4] Five tasks: **Store** (version models and track property changes in the model registry) → **Evaluate** (compare challenger to champion on evaluation metrics and business KPIs from online experimentation) → **Check** (review business, legal, ethical risks) → **Release** (invoke deployment with specified delivery type and traffic split) → **Report** (aggregate and visualize production performance metrics). Explainability is required for decision-automation use cases: auditors need "a clear view of lineage and accountability." [^src4]

## Context

This page is the foundational "what is MLOps" entry for the domain; the [MLOps hub](/mlops/README.md) tool/practice pages are the specific capabilities this overview frames. It is lecture 1 of the Marvelous MLOps "End-to-end MLOps with Databricks" course (Databricks Free Edition); lectures 2–10 (developing on Databricks, MLflow, model serving, Asset Bundles, CI/CD, monitoring) were ingested previously and live in the pages linked above. The [Practitioners Guide to MLOps](/mlops/sources/practitioners-guide-to-mlops.md) source page covers the full Google lifecycle and capability framework.

[^src1]: [Introduction to MLOps (Marvelous MLOps)](../../raw/email/email-2025-07-28-introduction-to-mlops.md)
[^src2]: [DevOps from Zero to Hero: Build and Deploy a Production API](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-devops-from-zero-report.md) — [01:00](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-devops-from-zero-report.md#t=01:00) DevOps loop diagram
[^src3]: [I Wasted 2 Years Learning DevOps Wrong. Here's What I'd Do Instead. (Nana)](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-i-wasted-2-years-report.md) — [01:26](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-i-wasted-2-years-report.md#t=01:26) tools vs. concepts
[^src4]: [Practitioners guide to MLOps](../../raw/pdf/pdf-practitioners-guide-to-mlops.md) — Khalid Salama, Jarek Kazmierczak, Donna Schut; Google, May 2021; 37 pages

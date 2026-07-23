---
type: source
domain: mlops
status: draft
sources:
  - path: raw/_inbox/pdf-practitioners-guide-to-mlops.md
    channel: pdf
    ingested_at: 2026-07-23
aliases:
  - Practitioners Guide to MLOps
  - Google MLOps whitepaper
  - continuous delivery machine learning
  - Khalid Salama MLOps
tags:
  - corpus/mlops
  - source
created: 2026-07-23
updated: 2026-07-23
---

# Practitioners Guide to MLOps (Google, 2021)

**TL;DR** — 37-page Google whitepaper (May 2021) by Khalid Salama, Jarek Kazmierczak, and Donna Schut. Defines MLOps as "a set of standardized processes and technology capabilities for building, deploying, and operationalizing ML systems rapidly and reliably." [^mlops-p01] Offers a two-part framework: an overview of seven lifecycle phases and eleven core capabilities, followed by deep-dives on six key processes. The central diagnosis is that most ML fails not at modeling but at operationalization—72% of organizations that started AI pilots before 2019 had not deployed a single application in production. [^mlops-p01]

## The deployment gap

Only 1 in 2 organizations has moved beyond pilots and proofs of concept. 55% of companies surveyed by Algorithmia had not deployed an ML model. [^mlops-p01] Root causes identified: high degree of manual and one-off work, no reusable/reproducible components, difficult handoffs between data scientists and IT, lack of talent, lack of governance. [^mlops-p01] McKinsey's finding: having standard frameworks and development processes is one of the differentiating factors of high-performing ML teams. [^mlops-p01]

## MLOps definition and scope

MLOps is "a methodology for ML engineering that unifies ML system development (the ML element) with ML system operations (the Ops element). It advocates formalizing and (when beneficial) automating critical steps of ML system construction." [^mlops-p01]

Unique complexities MLOps addresses that DevOps does not: [^mlops-p01]
- Preparing and maintaining high-quality data for model training
- Tracking models in production for performance degradation
- Ongoing experimentation of data sources, algorithms, and hyperparameters
- Maintaining model veracity via continuous retraining on fresh data
- Avoiding training-serving skew from inconsistencies in runtime dependencies
- Handling model fairness concerns and adversarial attacks

MLOps extends DevOps: "When you deploy a web service, you care about resilience, queries per second, load balancing. When you deploy an ML model, you also need to worry about changes in the data, changes in the model, users trying to game the system." [^mlops-p01]

## The MLOps lifecycle — seven phases

The lifecycle is iterative and non-waterfall; phases can be skipped or repeated: [^mlops-p01]

1. **ML development** — experimenting and developing a robust, reproducible training procedure (pipeline code) covering data preparation, transformation, model training, and evaluation.
2. **Training operationalization** — automating the packaging, testing, and deploying of repeatable and reliable training pipelines.
3. **Continuous training** — repeatedly executing the training pipeline on a schedule, in response to new data, or when code changes, with potentially new training settings.
4. **Model deployment** — packaging, testing, and deploying a model to a serving environment for online experimentation and production serving.
5. **Prediction serving** — serving the deployed model for inference (online, streaming, batch, or embedded).
6. **Continuous monitoring** — monitoring the effectiveness and efficiency of a deployed model.
7. **Data and model management** — a central, cross-cutting governance function supporting auditability, traceability, compliance, shareability, reusability, and discoverability.

## Core technical capabilities (eleven)

These can come from a single integrated ML platform or from combined vendor tools: [^mlops-p01]

| Capability | Purpose |
|---|---|
| Experimentation | Notebooks, experiment tracking, visualization, version-controlled code |
| Data processing | Batch and stream data transformation at scale; feature engineering |
| Model training | Distributed training, AutoML, hyperparameter tuning, ML accelerators |
| Model evaluation | Batch scoring, slice-level metrics, bias/fairness tools, explainability |
| Model serving | Online/batch/streaming prediction, composite routines, autoscaling |
| Online experimentation | Canary/shadow deployments, A/B tests, multi-armed bandit (MAB) |
| Model monitoring | Latency/throughput metrics, schema/distribution drift detection |
| ML pipelines | Trigger on demand/schedule/events, local debug, artifact integration |
| Model registry | Versioning, metadata/dependencies, model cards, govern release lifecycle |
| Dataset & feature repository | Unified storage, point-in-time queries, batch and online serving |
| ML metadata & artifact tracking | Lineage, reproducibility, experiment comparison across all capabilities |

## Six process deep-dives

### ML development
Core activity is experimentation. Pre-requisites: define the task, measure business impact, choose evaluation metric, identify relevant data, set training/serving requirements. [^mlops-p01] Key success factors: experiment tracking, reproducibility, and collaboration. Experiment tracking must capture: code version, model architecture, hyperparameters, data split info, evaluation metrics and validation procedure. [^mlops-p01] Primary output is either (a) a trained model submitted directly to the model registry (if no continuous retraining needed), or (b) the implementation of a continuous training pipeline.

### Training operationalization
Builds a repeatable pipeline through CI/CD stages: (1) CI stage: unit-test source code, build, integration-test pipeline; store artifacts in artifact repository. (2) CD stage: deploy tested pipeline artifacts to target environment, end-to-end testing on subset of production data. (3) Smoke-test newly deployed pipeline; fall back to previous model if new pipeline fails. [^mlops-p01]

### Continuous training
Retraining triggers: scheduled runs, event-driven (new data above threshold, or model decay detected), or ad hoc manual invocation. [^mlops-p01] Canonical pipeline steps: data ingestion → data validation → data transformation → model training and tuning → model evaluation → model validation → model registration. [^mlops-p01]

Critical distinction from experimentation: in an automated pipeline, "data validation and model validation play a critical role in a way that they don't during experimentation; these steps are gatekeepers for the overall ML training process." [^mlops-p01] Data validation detects schema anomalies and distributional shifts; model validation detects performance degradation before registration. Lineage analysis (model → dataset snapshot → intermediate artifacts) is required for debugging and reproducibility. [^mlops-p01]

### Model deployment
Progressive delivery approach: new model does not immediately replace the previous version—it runs in parallel while a subset of users is redirected in stages. A/B testing and MAB testing quantify impact on application-level objectives. Canary and shadow deployments facilitate online experiments. [^mlops-p01] CI stage tests include: model interface (input/output format), infrastructure compatibility, latency. CD stage tests include: smoke testing (service efficiency), then online experimentation (model effectiveness with live traffic). [^mlops-p01]

### Prediction serving
Four serving forms: online inference (REST/gRPC, near-real-time), streaming inference (event-processing pipeline), offline batch inference (ETL bulk scoring), embedded inference (edge devices). [^mlops-p01] Feature lookup pattern: request arrives with entity identifiers → serving engine fetches feature values from feature repository → passes to model → returns prediction. Feature attributions (explainability scores) can be generated per-prediction and logged. [^mlops-p01]

### Continuous monitoring
Monitors model effectiveness (detecting decay) and efficiency (latency, throughput, resource utilization, error rates). [^mlops-p01]

Monitoring process: (1) sample request-response payloads captured to serving logs store; (2) monitoring engine loads logs, generates schema, computes statistics; (3) compare schema and statistics to reference baseline to detect skews; (4) if ground truth is available, evaluate model predictive effectiveness; (5) alert owners or trigger retraining cycle on anomaly detection. [^mlops-p01]

Drift taxonomy: [^mlops-p01]
- **Data drift** — growing skew between training distribution and production data.
- **Concept drift** — evolving relationship between input predictors and the target feature.
- **Schema skew** — training and serving data do not conform to the same schema.
- **Distribution skew** — feature value distributions for training and serving data diverge significantly.

Additional drift detection techniques: novelty detection, outlier detection, feature attributions change. [^mlops-p01]

## Data and model management

Central cross-cutting process underpinning all six processes above.

**Training-serving skew** is a major production risk: "discrepancies between serving data and training data... can occur because the data is extracted from different sources in different forms during training and serving." [^mlops-p01] A unified feature and dataset repository (serving both training and inference from the same source) is the primary mitigation.

**Feature management**: standardized entity features (customer, product, location) in a central repository. "Data scientists spend a significant amount of their ML development time on exploratory data analysis, data preparation, and data transformation. However, other teams might have prepared the same datasets for similar use cases but have no means for sharing and reusing them." [^mlops-p01]

**Dataset management**: datasets are per-task (feature repo + labels for a specific use case); dataset management maintains creation scripts, split definitions, metadata, and lineage tracking across environments. [^mlops-p01]

**ML metadata tracking**: captures pipeline run ID, trigger, process type, step, start/end datetime, status, environment configs, input parameter values, and artifacts (processed data splits, schemas, statistics, hyperparameters, models, evaluation metrics). [^mlops-p01]

**Model governance**: "registering, reviewing, validating, and approving models for deployment." Can be automated, semi-automated, or manual. Five governance tasks: Store (track versions and properties) → Evaluate (challenger vs. champion, business KPIs) → Check (review risks: business, legal, ethical) → Release (type and traffic split) → Report (aggregate production performance). [^mlops-p01] Explainability is particularly important for decision automation; governance must provide auditors "a clear view of lineage and accountability." [^mlops-p01]

## Related corpus pages

- [MLOps Principles](/mlops/mlops-principles.md) — foundational overview; this source provides the canonical Google lifecycle and capability framework
- [Drift Detection](/mlops/drift-detection.md) — univariate drift metrics (the mechanics behind continuous monitoring)
- [Model Monitoring](/mlops/model-monitoring.md) — Databricks-specific implementation of monitoring concepts described here
- [CI/CD for ML](/mlops/ci-cd-for-ml.md) — training operationalization and model deployment CI/CD patterns
- [Model Serving](/mlops/model-serving.md) — serving patterns (online/batch/streaming) cross-reference

[^mlops-p01]: [Practitioners guide to MLOps](../../../raw/pdf/pdf-practitioners-guide-to-mlops.md) — Khalid Salama, Jarek Kazmierczak, Donna Schut; Google, May 2021; 37 pages

---
type: entity
domain: mlops
status: draft
sources:
  - path: raw/pdf/pdf-designing-machine-learning-systems.md
    channel: pdf
    ingested_at: 2026-06-25
aliases:
  - Designing Machine Learning Systems
  - Chip Huyen ML book
  - DMLS
  - CS 329S
tags:
  - corpus/mlops
  - entity
created: 2026-06-25
updated: 2026-06-25
---

# Designing Machine Learning Systems

**TL;DR** — O'Reilly book by **Chip Huyen** (2022, 389 pp), based on her Stanford CS 329S course. A holistic approach to building ML systems that are reliable, scalable, maintainable, and adaptive — covering the full arc from data engineering and training through deployment, monitoring, and continual learning. The guiding principle: every design decision must be evaluated in context of the whole system, not in isolation [^src1].

## Who it is for

Engineers building ML at real scale — ML engineers, data scientists, ML platform engineers. Assumes basic ML knowledge (models, gradient descent, common metrics) but focuses entirely on the practical *systems* layer [^src1].

## Chapter map

| Ch | Topic | Key concern |
|---|---|---|
| 1 | Overview of ML Systems | When to use ML vs. not; research vs. production contrast |
| 2 | ML Systems Design | Business vs. ML objectives; reliability, scalability, maintainability, adaptability |
| 3 | Data Engineering Fundamentals | Data sources, formats (row-major vs. column-major), models, ETL, batch vs. stream |
| 4 | Training Data | Sampling strategies, labeling (hand vs. natural labels), class imbalance, data augmentation |
| 5 | Feature Engineering | Missing values, scaling, encoding, feature crossing, data leakage, feature importance |
| 6 | Model Development & Offline Evaluation | Ensembles, experiment tracking, distributed training, AutoML, evaluation baselines |
| 7 | Model Deployment & Prediction Service | Batch vs. online prediction, model compression (quantization/pruning/distillation), edge ML |
| 8 | Data Distribution Shifts & Monitoring | Covariate/label/concept shift; detecting & addressing drift; observability |
| 9 | Continual Learning & Test in Production | Stateless vs. stateful retraining; shadow deployment, A/B testing, canary releases, bandits |
| 10 | Infrastructure & Tooling for MLOps | Storage+compute; dev environments; cron/schedulers/orchestrators; model store; feature store |
| 11 | Human Side of ML | UX consistency, responsible AI, team structure |

## Four production ML system requirements (Ch 2)

Huyen frames every design decision against four properties [^src1]:

1. **Reliability** — correct outputs even when things go wrong
2. **Scalability** — handles traffic spikes and data growth
3. **Maintainability** — different teams can work on it; infrastructure is reproducible
4. **Adaptability** — can be updated as data distributions and business requirements change

## ML vs. traditional software (Ch 1)

ML systems are unique because they are **data-dependent**: two companies in the same domain (ecommerce) with the same problem (recommender) may have completely different model architectures, features, metrics, and ROI [^src1]. This variability is why the book takes a holistic approach — changes in one component likely affect others.

## Batch vs. online prediction (Ch 7)

Four myths about ML deployment [^src1]:
1. You only deploy one or two models — false; production has many
2. Models hold performance without updates — false; data distributions drift
3. Models won't need frequent updates — false; continual learning is the norm
4. Most ML engineers don't need to worry about scale — false

## Data distribution shifts (Ch 8)

Three types [^src1]:
- **Covariate shift** — input distribution P(X) changes, but P(Y|X) is stable
- **Label shift** — P(Y) changes (e.g., prevalence of a disease)
- **Concept drift** — the relationship P(Y|X) itself changes

Detection: compare reference (training) distribution to analysis (production) distribution using univariate metrics (JS divergence, Wasserstein, KS test, etc.) — see [Drift Detection](/mlops/drift-detection.md) for detail.

## Infrastructure chapter highlights (Ch 10)

Cron, schedulers, and orchestrators occupy a critical niche [^src1]:
- **Cron**: simple periodic triggers; covered in [Cron Scheduling](/mlops/cron-scheduling.md)
- **Schedulers** (Airflow, Prefect): DAG-based; depend on conditions/state
- **Orchestrators** (Kubernetes): manage compute resources across tasks
- **Model store**: versioned model artifacts with metadata (lineage, performance)
- **Feature store**: shared, consistent features for training and serving; eliminates training-serving skew

## Build vs. buy (Ch 10)

The framework: buy when the vendor solution has 80%+ feature overlap and the remaining 20% is non-differentiating; build when your use case has specific requirements that commercial tools can't meet without prohibitive customization [^src1].

## Continual learning (Ch 9)

Stateless vs. stateful retraining [^src1]:
- **Stateless**: retrain from scratch on fresh data; most common
- **Stateful** (fine-tuning): continue training from the last checkpoint; faster but requires careful management

Four stages of maturity: (1) manual triggers, (2) fixed-schedule triggers, (3) performance-degradation triggers, (4) data-distribution-shift triggers.

## Endorsements (signal of community standing)

Praised by [^src1]:
- Josh Wills (WeaveGrid, ex-Slack Director of Data Engineering): "Simply, the very best book you can read about how to build, deploy, and scale machine learning models at a company"
- Goku Mohandas (Made With ML): "A must-read to navigate the ephemeral landscape of tooling"
- Laurence Moroney (Google AI/ML Lead): "If you are serious about ML in production … this book is essential"

## See also

- [MLOps Principles](/mlops/mlops-principles.md) — aligned concepts (traceability, reproducibility, DevOps loop)
- [Model Monitoring](/mlops/model-monitoring.md) — implementation of the Ch 8 monitoring approach
- [Drift Detection](/mlops/drift-detection.md) — univariate drift metrics (expands on Ch 8)
- [Model Serving](/mlops/model-serving.md) — Ch 7 deployment patterns in practice
- [Production ML Workflow](/mlops/production-ml-workflow.md) — training/eval workflow aligned with Ch 4–6
- [MLOps hub](/mlops/README.md)

---

[^src1]: [Designing Machine Learning Systems (Chip Huyen, O'Reilly 2022)](../../raw/pdf/pdf-designing-machine-learning-systems.md) — preface p. ix; ToC pp. iii–vi; Ch 2 requirements; Ch 7 deployment myths; Ch 8 distribution shifts; Ch 10 infrastructure

<!-- RELATED:START (generated by bin/corpus_heal.py related — do not edit inside) -->

## Related across domains

- [Chip Huyen](/ai-engineering/chip-huyen.md) · _ai-engineering_

<!-- RELATED:END -->

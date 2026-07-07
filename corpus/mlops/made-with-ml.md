---
type: entity
domain: mlops
status: draft
sources:
  - path: raw/github/github-gokumohandas-made-with-ml.md
    channel: github
    ingested_at: 2026-06-25
aliases:
  - Made With ML
  - GokuMohandas/Made-With-ML
  - madewithml.com
tags:
  - corpus/mlops
  - entity
created: 2026-06-25
updated: 2026-07-07
---

# Made With ML

**TL;DR** — Open-source ML engineering course (GitHub repo: `GokuMohandas/Made-With-ML`, 48k+ stars) teaching how to **design, develop, deploy, and iterate on production-grade ML applications**. Built around PyTorch + Ray; covers data engineering, data quality, distributed training, LLMs, NLP, and MLOps. Framed explicitly as combining machine learning with software engineering [^src1].

## Key facts

- **Repo**: [github.com/GokuMohandas/Made-With-ML](https://github.com/GokuMohandas/Made-With-ML)
- **Stars**: ~48,317 (as of collection date 2026-06-22)
- **Language**: Jupyter Notebook
- **Topics**: `data-engineering`, `data-quality`, `data-science`, `deep-learning`, `distributed-ml`, `distributed-training`, `llms`, `machine-learning`, `mlops`, `natural-language-processing`, `python`, `pytorch`, `ray`
- **Latest release**: v1.1.0
- **Course site**: [madewithml.com](https://madewithml.com)
- **Community**: 40K+ subscribers/developers [^src1]
- **Tagline**: "Design · Develop · Deploy · Iterate" [^src1]

## Content scope

The course goes "from experimentation (design + development) to production (deployment + iteration)" by "motivating the components that will enable us to build a *reliable* production system" [^src1].

Six explicit pillars from the README [^src1]:

| Pillar | Description |
|---|---|
| **First principles** | Develop a first-principles understanding for every ML concept before code |
| **Best practices** | Implement software engineering best practices during development and deployment |
| **Scale** | Scale ML workloads (data, train, tune, serve) in Python via Ray without new languages |
| **MLOps** | Connect MLOps components — tracking, testing, serving, orchestration — end-to-end |
| **Dev to Prod** | Go from development to production without code or infra changes |
| **CI/CD** | Create mature CI/CD workflows to continuously train and deploy better models |

## Target audience

The course explicitly positions ML as "a powerful way of thinking about data that's not reserved for any one type of person" [^src1]. Three named audiences [^src1]:

- **All developers** — software/infra engineers and data scientists, as ML becomes part of products
- **College graduates** — bridging the gap between university curriculum and industry expectations
- **Product/Leadership** — building a technical foundation to ship reliable ML-powered products

## Infrastructure

- Supports both **local laptop** (single machine, CPU-only, slower) and **Anyscale clusters** (GPU, structured cohorts) [^src1].
- Anyscale integration provides compute (GPUs) and community for accelerated learning [^src1].

## Positioning

Among the "top ML repositories on GitHub" (self-described) [^src1]. Targets developers wanting to "responsibly deliver value with ML" — bridges the gap between research/notebook prototyping and production engineering.

## See also

- [MLOps hub](/mlops/README.md)
- [MLOps Principles](/mlops/mlops-principles.md) — the discipline this course teaches
- [Production ML Workflow](/mlops/production-ml-workflow.md) — production-minded training concepts
- [Model Monitoring](/mlops/model-monitoring.md) — monitoring in production

---

[^src1]: [GokuMohandas/Made-With-ML (GitHub)](../../raw/github/github-gokumohandas-made-with-ml.md) — repository description, topics, README overview

---
type: concept
domain: mlops
status: draft
sources:
  - path: raw/email/email-2025-07-29-developing-on-databricks.md
    channel: email
    ingested_at: 2026-06-19
aliases:
  - developing on databricks
  - databricks development
  - local databricks development
  - databricks cli
  - databricks connect
  - databricks vs code extension
  - serverless environment versions
  - projectconfig
  - databricks local dev
tags:
  - corpus/mlops
  - concept
created: 2026-06-19
updated: 2026-06-19
---

# Databricks Development (Local-First)

**TL;DR.** Most people start developing directly in Databricks notebooks because it's easy and convenient, but "when it comes to MLOps, that convenience can quickly become a bottleneck" — notebooks make it hard to write modular code, apply code-quality standards, or run unit tests, all essential for production-grade ML [^src1]. Databricks developer tools (VS Code extension, Databricks CLI, Databricks Connect) let you develop **locally** with modern engineering workflows while still running PySpark on Databricks [^src1]. This page covers CLI auth, the VS Code extension, Databricks Connect, serverless environment versions, `uv` project management, Git folders vs sync, and pydantic-validated config.

## Why move out of notebooks

Notebooks bottleneck MLOps: no modularity, no straightforward code-quality enforcement, no unit tests [^src1]. The fix is to move development outside notebooks and adopt workflows aligned with MLOps practices, using Databricks' local-dev tooling [^src1].

## CLI authentication

The Databricks CLI is used to authenticate from your local machine [^src1]. The course explicitly recommends **against personal access tokens** ("from a security perspective, this is not the best option") and instead uses **user-to-machine authentication** [^src1]:

```bash
databricks auth login --host <workspace-url>
```

This creates an authentication profile in the `.databrickscfg` file (e.g. profile `[dbc-1234a567-b8c9]` with `auth_type = databricks-cli`) [^src1]. On macOS the Homebrew install of the CLI "works great"; on Windows use winget [^src1].

## VS Code extension & Databricks Connect

Install the Databricks **VS Code extension**, then update `databricks.yml` to match the Free Edition workspace host [^src1]. To execute PySpark code on Databricks you choose a cluster in the extension UI (only serverless compute is available in Free Edition) [^src1].

**Databricks Connect** is what lets local PySpark code run against Databricks — but it *bundles pyspark internally*, so `pyspark` cannot be a project dependency alongside `databricks-connect`: "these two libraries cannot be installed side by side as they would conflict with each other" [^src1]. This is why `SparkSession` is imported from `pyspark` even though pyspark isn't a declared dependency [^src1].

## Serverless environment versions

Databricks supports three serverless environment versions, each with its own requirements [^src1]. The key rule: *"your project's Python version must match the environment Python version."* The course uses Python 3.12, which matches **environment version 3** (Ubuntu 24.04.2 LTS, Python 3.12.3, Databricks Connect 16.3.2) [^src1]. The environment ships pinned package versions, but the project overrides them (e.g. MLflow 3.1.1 instead of the env's 2.21.3) [^src1].

## Python project management with uv

The course uses **[uv](/mlops/uv.md)** for Python project management [^src1]. Python version and dependencies live in `pyproject.toml`, with **exact version pins** for all packages — intentional *because the project is not meant to be reused as a library*; for reusable packages, locking too strictly causes resolution issues [^src1]. The `marvel-characters` package is self-contained: when installed inside a Databricks environment, its specific versions should override the existing ones [^src1]. Setup is one command, building a `.venv` in the project folder [^src1]:

```bash
uv sync --extra dev   # dev extras: databricks-connect, ipykernel, pip, pre-commit
```

## Git folders vs sync

To run project code in a notebook with the right dependencies, you can use **Git Folder** functionality [^src1]. Notebook files are `.py` with first line `# Databricks notebook source` and cells delimited by `# COMMAND ----------`; pick the environment version via the notebook's Environment side panel, then `%pip install -e ..` + `%restart_python` [^src1].

Alternatively, **sync** the project folder to a workspace location via the extension's "Remote Folder" sync button — this allows a nicer install: build the package locally with `uv build`, and if the resulting wheel isn't git-ignored it syncs along with the files, letting you install the wheel directly in the notebook [^src1].

## Environment-specific config with pydantic

Features, model parameters, experiment names, and per-environment catalogs/schemas live in a separate YAML (`project_config_marvel.yml`) — kept separate on purpose for easy adjustment [^src1]. A **`ProjectConfig`** class manages and validates this config using **pydantic**, ensuring correct data types and structure at runtime [^src1]. Its `from_yaml(config_path, env="dev")` classmethod loads environment-specific settings, selecting the right catalog/schema for `dev`/`acc`/`prd` and raising on an invalid environment [^src1]:

```python
config = ProjectConfig.from_yaml(config_path="../project_config_marvel.yml", env="dev")
```

The three environments map to dedicated catalogs `mlops_dev`, `mlops_acc`, `mlops_prd`, each with schema `marvel_characters` — the data is preprocessed and written to Unity Catalog for traceability and consistency across environments, with change data feed enabled on the resulting Delta tables to track row-level changes between versions [^src1].

## See also

- [uv](/mlops/uv.md) — the package/project manager used here
- [VS Code](/mlops/vs-code.md) — the editor hosting the Databricks extension
- [Git](/mlops/git.md) — Git folders and the branch workflow
- [MLflow](/mlops/mlflow.md) — reuses the `is_databricks()` / profile auth pattern set up here
- [CI/CD for ML](/mlops/ci-cd-for-ml.md) — the dev/acc/prd catalog split feeds the deployment strategy
- [Databricks](/data-engineering/databricks.md) — the platform and Unity Catalog this builds on
- [MLOps hub](/mlops/README.md)

---

[^src1]: [Developing on Databricks (Marvelous MLOps, Lecture 2)](../../raw/email/email-2025-07-29-developing-on-databricks.md)
</content>

<!-- RELATED:START (generated by bin/corpus_heal.py related — do not edit inside) -->

## Related across domains

- [Local-First Sync Architecture](/software-engineering/local-first-sync-architecture.md) · _software-engineering_

<!-- RELATED:END -->

---
type: concept
domain: mlops
status: draft
sources:
  - path: raw/email/email-2025-08-05-introduction-to-ml-monitoring.md
    channel: email
    ingested_at: 2026-06-19
  - path: raw/email/email-2025-08-06-lecture-10-implementing-model-monitoring-in-databricks.md
    channel: email
    ingested_at: 2026-06-19
aliases:
  - model monitoring
  - ml monitoring
  - lakehouse monitoring
  - databricks lakehouse monitoring
  - data drift
  - concept drift
  - inference tables
  - profile metrics table
  - drift metrics table
  - quality monitors
tags:
  - corpus/mlops
  - concept
created: 2026-06-19
updated: 2026-06-23
---

# Model Monitoring

**TL;DR.** ML monitoring goes beyond the system metrics (health, errors, latency, cost) of any production system, because *model performance can degrade even if nothing changes in your code or infra* — ML is driven by the statistical properties of its data [^src1]. So MLOps monitoring includes **data drift**, **concept (model) drift**, and statistical health, not just system metrics [^src1]. On Databricks, **Lakehouse Monitoring** + **inference tables** provide built-in tools to track data and model health over time [^src1]. The implementation is a pipeline: log inference → parse into a structured monitoring table → create a `quality_monitors` monitor → schedule refreshes via a DAB job → dashboard [^src2]. This page covers why ML monitoring differs, the drift taxonomy, Databricks' monitoring components, and the implementation pipeline.

## Why ML monitoring differs from classic software

In classic software, if code, data, and environment stay the same, so does behavior [^src1]. ML systems are different: performance can drop with no code or infra change because behavior depends on the *statistical properties of the data* — user behavior shifts, seasonality, or upstream data changes can all cause underperformance "even if everything else is 'the same'" [^src1].

## Drift taxonomy

- **Data drift** — the distribution of the *input* data shifts over time, even if the relationship between inputs and outputs stays the same [^src1]. Housing example: lots of new houses enter a district; preferences and the feature→price relationship are unchanged, but the model hasn't seen enough new-house examples, so its performance drops — data drift is the root cause of the degradation [^src1].
- **Concept drift** — the *relationship* between input features and the target changes, so the model's original assumptions no longer hold [^src1]. Housing example: a government subsidy for families with children leads to larger houses selling for lower prices — a shift in the underlying feature→price relationship; even if the input distribution barely changes, predictions become less accurate [^src1].

**Not all drift is bad.** Sometimes the model is robust to input changes and performance stays stable [^src1]. The canonical example: you detect significant drift in a "temperature" feature via Jensen-Shannon distance, but the model's **MAE** is still within acceptable bounds — so no action is needed [^src1]. The rule: *monitor both data and performance before retraining or raising alarms* [^src1]. The univariate-metric selection behind this (JS, Wasserstein, etc.) is detailed in [[mlops/drift-detection|Drift Detection]].

## Databricks Lakehouse Monitoring

**Databricks Lakehouse Monitoring** lets you monitor the statistical properties and quality of data in Delta tables, and (by creating inference tables with model inputs and predictions) track the performance of models and serving endpoints [^src1]. It auto-generates two key tables [^src1]:

- **Profile Metrics Table** — summary stats per feature per time window (count, nulls, mean, stddev, min/max). For inference logs it also tracks accuracy, confusion matrix, F1, MSE, R², and fairness metrics; supports slicing/grouping (e.g. by model id or feature value).
- **Drift Metrics Table** — tracks how column distributions evolve over time using drift-detection techniques, to identify data-quality issues and shifts. Two primary detection types: **Consecutive Drift** (current window vs the previous one, for short-term anomalies) and **Baseline Drift** (current data vs a fixed reference/baseline, typically built from training data) [^src1]. Drift is computed via a combination of statistical tests, distance metrics, and simple delta metrics, with method depending on data type [^src1] — see [[mlops/drift-detection|Drift Detection]].

### Inference tables

**Inference tables** are a built-in feature that logs model inputs and predictions from a serving endpoint directly into a Delta table in Unity Catalog [^src1]. Once enabled they automatically capture request and response payloads plus metadata (response time, status codes) — used for monitoring quality, debugging, and **training-corpus generation** [^src1]. Enable via the "enable inference table" box when editing a serving endpoint (or programmatically); the workspace needs Unity Catalog and the right permissions [^src1]. Inference tables log *raw* data; to monitor drift/performance you process them into a **structured inference profile table** (timestamp, features, prediction, optionally ground truth) [^src1]. A separate workflow updates the monitor when ground-truth labels arrive, yielding two workflows in total: one for training/deployment, one for monitoring [^src1].

## Implementation pipeline

The monitoring system has four components [^src2]: inference logging → monitoring-table creation → scheduled refreshes → dashboard.

1. **Inference logging.** With inference tables enabled, send requests to the endpoint (via HTTPS or the Workspace Client) to generate logs [^src2].
2. **Monitoring-table creation.** A `create_or_refresh_monitoring` function (in `src/marvel_characters/monitoring.py`) reads the raw inference Delta table, **parses the request and response JSON** into a structured schema (`F.from_json` with explicit `StructType` schemas, then `F.explode` over `dataframe_records`), selects timestamp/features/prediction columns, drops null predictions, and appends to a `model_monitoring` Delta table [^src2].
3. **Monitor creation.** If no monitor exists, `create_monitoring_table` calls **`workspace.quality_monitors.create(...)`** with a **`MonitorInferenceLog`** spec — `problem_type=PROBLEM_TYPE_CLASSIFICATION`, `prediction_col`, `timestamp_col`, `granularities=["30 minutes"]`, `model_id_col` — then enables **Change Data Feed** on the table (`ALTER TABLE ... SET TBLPROPERTIES (delta.enableChangeDataFeed = true)`), which is important for updating monitoring [^src2]. This auto-creates two tables (profile + drift) plus a dashboard [^src2].
4. **Scheduled refresh.** A **[[mlops/databricks-asset-bundles|Databricks Asset Bundle]]** job (`resources/bundle_monitoring.yml`) runs `scripts/refresh_monitor.py` on a weekly Quartz cron (Mondays 6 AM Amsterdam), calling `create_or_refresh_monitoring` — which runs `quality_monitors.run_refresh(...)` on an existing monitor [^src2].
5. **Dashboard & alerts.** The auto-created dashboard has default panels (extendable with SQL queries); you can configure alerts to be notified when performance drops or data shifts [^src1][^src2].

The net effect: inference tables + monitoring pipelines enable end-to-end visibility and alerting, so you can detect issues early and make data-driven retraining decisions [^src1][^src2].

## See also

- [[mlops/drift-detection|Drift Detection]] — the univariate distance-metric/test selection detail under this broader monitoring picture
- [[data-engineering/data-quality|Data Quality]] — complements this: its input-distribution monitoring layer watches for the same data drift from the *upstream data* side (schema/contract checks, `null_rate`/`mean` over time), where this page watches it from the *served-model* side
- [[mlops/model-serving|Model Serving]] — inference tables log the endpoints this monitors
- [[mlops/databricks-asset-bundles|Databricks Asset Bundles]] — the DAB job that schedules monitor refreshes
- [[mlops/mlflow|MLflow]] — the registered models being served and monitored
- [[data-engineering/databricks|Databricks]] — Unity Catalog, Delta tables, and the platform
- [[mlops/README|MLOps hub]]

---

[^src1]: [Introduction to ML monitoring (Marvelous MLOps, Lecture 9)](../../raw/email/email-2025-08-05-introduction-to-ml-monitoring.md)
[^src2]: [Implementing Model Monitoring in Databricks (Marvelous MLOps, Lecture 10)](../../raw/email/email-2025-08-06-lecture-10-implementing-model-monitoring-in-databricks.md)
</content>

---
type: entity
domain: mlops
status: draft
sources:
  - path: raw/email/email-2025-07-30-getting-started-with-mlflow.md
    channel: email
    ingested_at: 2026-06-19
  - path: raw/email/email-2025-07-31-logging-and-registering-models-with-mlflow.md
    channel: email
    ingested_at: 2026-06-19
aliases:
  - MLflow
  - ml flow
  - mlflow tracking
  - mlflow model registry
  - mlflow 3
  - LoggedModel
  - pyfunc
  - mlflow pyfunc
tags:
  - corpus/mlops
  - entity
created: 2026-06-19
updated: 2026-06-19
---

# MLflow

**TL;DR.** MLflow is described as "probably the most popular tool for model registry and experiment tracking out there" — open source, integrating with many platforms and tools [^src1]. Two classes form the foundation of everything else: `mlflow.entities.Experiment` (the organizing unit for training runs) and `mlflow.entities.Run` (a single training execution under which params, metrics, and artifacts are logged) [^src1]. Beyond tracking, MLflow defines a standardized **MLflow Model** format storing the model, its dependencies, and code — essential for downstream tasks like real-time serving [^src2]. The Databricks-flavored MLflow used in the course adds Databricks specifics, but the ideas generalize to any MLflow instance [^src1]. This page covers tracking, experiments/runs, MLflow 3's `LoggedModel`, model logging/flavors/signatures, dataset logging, Unity Catalog registration, and the **pyfunc** wrapper.

## Tracking & registry URIs

By default MLflow tracks runs on the local file system, storing metadata in `./mlruns`; `mlflow.get_tracking_uri()` reveals the current URI [^src1]. To use the Databricks tracking server, call `mlflow.set_tracking_uri()`. Starting with **MLflow 3**, you must *also* set the registry URI via `mlflow.set_registry_uri()`, even when only doing experiment tracking [^src1].

Both URIs must contain the **profile** used to log in (defined in `.databrickscfg`, e.g. `dbc-1234a567-b8c9`), so multiple developers with different profile names can collaborate on the same code base [^src1]. The URIs should only be set when running *outside* Databricks. The course's `is_databricks()` pattern detects the runtime by checking for the `DATABRICKS_RUNTIME_VERSION` environment variable, and only then loads the profile from a git-ignored `.env` file [^src1]:

```python
def is_databricks() -> bool:
    return "DATABRICKS_RUNTIME_VERSION" in os.environ

if not is_databricks():
    load_dotenv()
    profile = os.environ.get("PROFILE")
    mlflow.set_tracking_uri(f"databricks://{profile}")
    mlflow.set_registry_uri(f"databricks-uc://{profile}")
```

Note `databricks-uc://` for the registry URI selects Unity Catalog as the model registry [^src1].

## Experiments

Experiments are "the main unit of organization for ML model training runs"; all runs belong to an experiment [^src1]. Create one with `mlflow.create_experiment` or, more commonly, `mlflow.set_experiment` — the latter activates an existing experiment by name or creates a new one if absent [^src1]. Tags can be passed to `create_experiment`, or added after activation via `mlflow.set_experiment_tags` [^src1]. Experiments can be retrieved with `mlflow.search_experiments(filter_string=...)` by name or tag, or by id via `mlflow.get_experiment(experiment_id)` [^src1].

## Runs

A run "is related to a single execution of ML model training code"; under it you can log params, metrics, and artifacts of various formats [^src1]. Create one with `mlflow.start_run`, typically inside a `with` block to manage the lifecycle (otherwise call `mlflow.end_run` explicitly) [^src1]:

```python
with mlflow.start_run(run_name="marvel-demo-run",
                      tags={"git_sha": "1234567890abcd"}) as run:
    run_id = run.info.run_id
    mlflow.log_params({"type": "marvel_demo"})
    mlflow.log_metrics({"metric1": 1.0, "metric2": 2.0})
```

MLflow auto-creates some tags depending on where the run executes — e.g. a run inside a **Lakeflow job** gets the job id and task run id as tags [^src1]. A run can be restarted by passing its `run_id` to `start_run()`; extra information can be logged, but existing metrics and parameters cannot be overwritten [^src1].

**Artifacts** of many types are logged with `log_artifact`, `log_artifacts`, `log_text`, `log_dict`, `log_figure`, and `log_image` (the last two support a `step` for dynamic logging across iterations) [^src1]. Runs are searchable via `mlflow.search_runs`, filtering on tags, run name, metrics, status, and start time with a `filter_string` [^src1]. Artifacts are loaded back with `mlflow.artifacts.load_dict`, `load_image`, and `download_artifacts` [^src1].

## Logging a model

A model is logged with `mlflow.<flavor>.log_model()`. MLflow supports many **flavors** — `sklearn`, `lightgbm`, `xgboost`, `prophet`, `pytorch`, and more — plus the catch-all **`pyfunc`** flavor for any custom logic via the `PythonModel` base class [^src2]. MLflow's standardized model format goes beyond a bare `.pkl`: it captures the model, its dependencies, and code, which is what makes downstream serving possible [^src2].

### Model signature (required for UC registration)

The **signature** defines how interfaces interact with the model (e.g. the payload of a serving endpoint) [^src2]. It is inferred via `infer_signature(model_input=X_train, model_output=pipeline.predict(X_train))` and passed when logging. Critically: *"If the signature is not provided, we would not be able to register model in Unity Catalog later"* [^src2].

```python
signature = infer_signature(model_input=self.X_train,
                            model_output=self.pipeline.predict(self.X_train))
self.model_info = mlflow.sklearn.log_model(
    sk_model=self.pipeline,
    artifact_path="lightgbm-pipeline-model",
    signature=signature,
    input_example=self.X_test[0:1])
```

Metrics are not logged manually here; they are computed and logged under the same run by `mlflow.models.evaluate()`, which takes the model URI, eval data, target, model type, and evaluators (`["default"]` logs the standard metrics) [^src2].

### Logging input datasets (reproducibility via Delta time-travel)

Train and test sets are logged under the run with `mlflow.data.from_spark(...)` + `mlflow.log_input(dataset, context="training")`, including the **Delta table version** [^src2]. This guarantees the exact data version used for training/evaluation can be recovered later via Delta **time-travel**, even if the table was modified [^src2]. Gotcha: set a proper **retention period** on the Delta table (default is 7 days) — otherwise once `VACUUM` runs you may lose access to that version. Most accounts have **predictive optimization** enabled, so Databricks executes `VACUUM` automatically [^src2]. (Note: `toPandas()` is inefficient for large datasets; logging input data is harder when using `deltatable` + external credential vending instead [^src2].)

## MLflow 3: `LoggedModel`

MLflow 3 introduced the **`LoggedModel`** concept and a separate model tab in the experiments UI [^src2]. After logging, the model can be retrieved by **model id**: `mlflow.get_logged_model(model_info.model_id)` and loaded via `mlflow.sklearn.load_model(f"models:/{model_id}")` — neither possible before MLflow 3 [^src2]. Params and metrics can be accessed directly off the `LoggedModel` class (previously only reachable via the run) [^src2]. The **run object is still needed** to retrieve dataset inputs (`run.inputs.dataset_inputs`) used for training/evaluation [^src2].

## Registering in Unity Catalog

`mlflow.register_model(model_uri, name, tags)` registers the model into Unity Catalog under a three-part `catalog.schema.model` name [^src2]. The course then sets the **`latest-model` alias** via `MlflowClient().set_registered_model_alias(...)` to make the newest version easy to find [^src2]. Caveats [^src2]:

- `"latest"` is a *reserved* alias value and cannot be used; models cannot be referred to as `"latest"` either.
- Searching UC-registered model versions is limited — you can only search **by model name or alias**. Filter-string search is **not supported** for UC-registered models.

## pyfunc wrapper

A registered sklearn pipeline served behind an endpoint returns output like `{"Predictions": [0]}`; a **pyfunc** model flavor becomes useful to **adjust the payload** [^src2]. Other motivations: accessing external systems (e.g. a database) at prediction time, or bundling extra serving artifacts [^src2]. pyfunc acts as a **wrapper** — *"In a certain sense, it's very similar to the functionality of a FastAPI"* — keeping the payload definition separate from the model, so it can be changed without touching the registered model [^src2].

A pyfunc subclasses `mlflow.pyfunc.PythonModel` with `load_context` (loads the wrapped model from `context.artifacts`) and `predict` (runs inference and reshapes output) [^src2]:

```python
class MarvelModelWrapper(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        self.model = mlflow.sklearn.load_model(context.artifacts["lightgbm-pipeline"])
    def predict(self, context, model_input):
        return adjust_predictions(self.model.predict(model_input))
```

### Packaging a private wheel via `code_paths` / `conda_env`

When the `predict` logic depends on a private package (e.g. `marvel_characters`), that package must be logged alongside the pyfunc model [^src2]. `mlflow.pyfunc.log_model()` takes a **`code_paths`** list (local path to the package wheel) used to build the **`conda_env`** (the wheel is referenced as a `code/<whl>` dependency), plus an **`artifacts`** dict containing the wrapped model URI [^src2]. The wheel lands in the model's `code` folder and is referenced in `requirements.txt`, so the private package's dependencies get installed when the serving environment is built [^src2].

Loading: `mlflow.pyfunc.load_model("models:/<name>@latest-model")`; use `unwrap_python_model()` to reach the original wrapper class [^src2]. Running `predict` locally does **not** guarantee successful loading at serving time (it reuses the existing env); `mlflow.models.predict(...)` is a more reliable check that mimics the serving environment (but only runs inside Databricks, not VS Code) [^src2].

## See also

- [[mlops/model-serving|Model Serving]] — where MLflow-registered models are exposed as REST endpoints (Databricks Model Serving)
- [[mlops/databricks-development|Databricks Development]] — the local-dev setup and `is_databricks()` / profile pattern MLflow reuses
- [[mlops/databricks-asset-bundles|Databricks Asset Bundles]] — the DAB jobs that train/register models through MLflow
- [[mlops/model-monitoring|Model Monitoring]] — inference logging and Lakehouse Monitoring downstream of a served MLflow model
- [[data-engineering/databricks|Databricks]] — Unity Catalog and the platform MLflow's Databricks flavor runs on
- [[mlops/README|MLOps hub]]

---

[^src1]: [Getting started with MLflow (Marvelous MLOps, Lecture 3)](../../raw/email/email-2025-07-30-getting-started-with-mlflow.md)
[^src2]: [Logging and registering models with MLflow (Marvelous MLOps, Lecture 4)](../../raw/email/email-2025-07-31-logging-and-registering-models-with-mlflow.md)
</content>
</invoke>

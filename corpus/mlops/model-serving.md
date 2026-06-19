---
type: concept
domain: mlops
status: draft
sources:
  - path: raw/email/email-2025-07-06-serving-ml-with-flask-your-first-spam-detection-api.md
    channel: email
    ingested_at: 2026-06-19
  - path: raw/email/email-2025-07-20-batch-inference-with-airflow-scaling-your-spam-classifier.md
    channel: email
    ingested_at: 2026-06-19
  - path: raw/email/email-2025-08-01-model-serving-architectures.md
    channel: email
    ingested_at: 2026-06-19
  - path: raw/email/email-2025-08-02-lecture-6-deploying-model-serving-endpoint-a-b-testing-on-da.md
    channel: email
    ingested_at: 2026-06-19
aliases:
  - model serving
  - ml serving
  - model deployment
  - batch inference
  - real-time inference
  - inference api
  - flask ml api
  - databricks model serving
  - serving architectures
  - feature serving
  - feature lookup
  - a/b testing
  - sticky assignment
tags:
  - corpus/mlops
  - concept
created: 2026-06-19
updated: 2026-06-19
---

# Model Serving (Real-Time API + Batch Inference)

**TL;DR.** A trained model is useless until it's *served*. Most ML models never reach production; when they do, it's usually through **an API** — a structured interface other software talks to [^src1]. There are two serving shapes: **real-time inference** (a request/response API, e.g. a Flask endpoint, for instant per-item predictions) and **batch inference** (a scheduled job, e.g. an Airflow DAG, that scores large groups of inputs at once) [^src1][^src2]. Both reuse the *exact same preprocessing as training* and a saved model pipeline; they differ only in how predictions are triggered and delivered. (Worked example throughout: a TF-IDF + logistic-regression spam classifier with a tuned decision threshold of `0.620` [^src1][^src2].)

## Real-time serving with a Flask API

[Flask](https://flask.palletsprojects.com/) is a Python micro web framework — ideal for rapid prototyping and ML demos [^src1]. The serving pattern [^src1]:

1. **Load the saved pipeline** (the pickled TF-IDF vectorizer + logistic-regression classifier saved at training time).
2. **Reuse the training preprocessing** verbatim — lowercase, strip punctuation, tokenize, remove stopwords, Porter-stem — so inference matches training.
3. **Apply a custom threshold**, not the default 0.5: `pred = 1 if prob >= BEST_THRESHOLD else 0`.
4. **Expose a `POST /predict` endpoint** that accepts `{"text": "..."}` and returns `{"prediction": "spam|ham", "probability_spam": <float>}`.

```python
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    clean = preprocess_text(data['text'])
    prob = logreg_pipeline.predict_proba([clean])[0][1]
    label = 'spam' if prob >= BEST_THRESHOLD else 'ham'
    return jsonify({'prediction': label, 'probability_spam': prob})
```

Run with `python app.py` (defaults to `http://localhost:5000`) and test with **Postman** (GUI) or **cURL** [^src1]. *"With less than 50 lines of code, you've built a working ML service"* — but a `debug=True` Flask dev server is **not** production-safe [^src1].

### Hardening a serving API for production
Minimal-setup caveats and the fixes [^src1]: add **input validation and logging**, **limit request size and rate**, **disable debug mode**, serve behind a production WSGI/ASGI server (**gunicorn / uvicorn**) rather than the Flask dev server, then **containerize with Docker** and deploy to a cloud platform (AWS / GCP / Heroku). See [[mlops/infrastructure-as-code|Infrastructure as Code]] and [[software-engineering/kubernetes|Kubernetes]] for the deployment substrate, and [[ai-engineering/agent-security|Agent Security]] for the input-validation mindset on any model-facing endpoint.

## Batch inference with Airflow

Real-time isn't always the right fit. Reach for **batch inference** when you're scoring large datasets (e.g. weekly email logs), running jobs overnight, or you don't need instant predictions [^src2]. Batch lets you schedule predictions over groups of inputs reliably and efficiently [^src2].

[Apache Airflow](https://airflow.apache.org/) is the industry-standard orchestrator for data/ML pipelines [^src2]. Core terms: a **DAG** (Directed Acyclic Graph) is a pipeline with dependencies; **tasks** are Python functions/scripts run as steps [^src2]. The example DAG runs daily and chains three `PythonOperator` tasks [^src2]:

```python
ingest >> preprocess >> score
# ingest_data()     -> read raw CSV of messages
# preprocess_data() -> clean/stem text (same logic as training)
# score_model()     -> apply saved model + threshold, write predictions CSV
```

Inputs are passed between tasks via **XCom**; in the Docker-based setup the `dags/`, `models/`, and `data/` directories are mounted as volumes so tasks can read the trained model and the input/output CSVs [^src2]. Output rows carry `prob_spam`, `prediction`, and a `label` column [^src2].

### Production tips for batch jobs
[^src2]: use **dynamic filenames** (`incoming_emails_{{ ds }}.csv`) so each run reads its own partition; **log metrics** (spam rate, volume) to BigQuery or Postgres; **store data on S3/GCS** rather than local disk; and use **Airflow sensors** to trigger the DAG after an upload lands. Airflow itself supplies the scheduling, per-task logs, and dependency visualization — see [[data-engineering/data-orchestration|Data Orchestration]] for why an orchestrator beats bare `cron` here.

## Real-time vs batch — choosing

| | Real-time (Flask API) | Batch (Airflow DAG) |
|---|---|---|
| Trigger | Per-request (HTTP) | Scheduled / sensor-triggered |
| Latency | Instant, one item | Minutes–hours, many items |
| Use when | Interactive apps, low-latency needs [^src1] | Bulk scoring, overnight jobs, no instant need [^src2] |
| Shared | Same saved pipeline + identical preprocessing + tuned threshold [^src1][^src2] | |

Both are stages of one production-minded ML workflow (the "Practical ML Series": lifecycle/MLOps → training → Flask serving → Airflow batch) [^src1][^src2]. Natural next steps are chaining batch prediction to downstream dashboards, **model retraining**, and event triggers [^src2].

## Databricks Model Serving

The same serve-a-saved-model idea scales up on **Databricks Model Serving** — a fully managed, serverless solution that deploys MLflow models as RESTful APIs without managing infrastructure [^src4]. It offers effortless deployment of registered MLflow models, **automatic scaling including scale-to-zero** when idle, built-in monitoring (latency/throughput/error rates) in the UI, both batch and real-time inference, and seamless MLflow Model Registry integration [^src4]. Limits: **no control over the runtime environment** (Databricks picks it), **no control over cluster size** — each replica is capped at **4 GB RAM** — and **workload sizes** (Small/Medium/Large/XL) that set compute units per replica, scalable up to **512 units per endpoint** [^src4].

**How scaling works**: each compute unit handles one request at a time, and autoscaling is driven by **concurrent request demand**, not CPU/RAM [^src4]. The sizing rule: `required units = Queries per second × Model Processing Time (s)` — e.g. 1,000 QPS × 0.02 s = 20 units; the 512-unit max equals ~25,600 QPS at 20 ms latency [^src4]. Deployment is one Python command via a `ModelServing` utility wrapping the serving APIs (`deploy_or_update_serving_endpoint()`), letting data-science teams own deployment end-to-end and minimize hand-offs to other teams [^src3][^src4].

### Three serving architectures

Databricks supports a range of architectures [^src3]:

- **Feature serving (batch predictions)** — predictions are computed in advance by a scheduled Lakeflow job, written to a feature table in Unity Catalog, synced to an **Online Store**, and exposed via a Feature Serving endpoint (defined by a `FeatureSpec` combining feature functions and feature lookups) [^src3]. Popular for low-latency personalized recommendations (e.g. e-commerce product recs) [^src3].
- **Model serving** — the model sits behind an endpoint and **all features arrive in the payload** [^src3]. Less realistic, but fits models embedded in apps relying on user input. This is the architecture the course deploys, since the Databricks Online Store isn't supported in Free Edition [^src3].
- **Model serving with feature lookup** — the most complex and realistic: some features come in the request, others are **fetched from the Online Store by primary key**, combined, run through the model, and returned [^src3]. Used for fraud detection and complex recommendations [^src3].

### A/B testing (sticky assignment)

Serving one model is easy; comparing two in production needs **A/B testing** — and "a common misconception is that simply splitting traffic between model versions qualifies as A/B testing but that's not accurate" [^src4]. True A/B testing requires that a customer *consistently sees the same model version* throughout the experiment, which is critical for accurately measuring performance differences (CTR, conversion) [^src4]. A **naive traffic split** (like Databricks' built-in routing) doesn't guarantee this — a user might hit model A then model B on the next request [^src4].

The fix is **sticky assignment**: assign each user to a variant based on a stable identifier so they always get the same model during the test [^src4]. The course implements this with a pyfunc wrapper ([[mlops/mlflow|MLflow]] `PythonModel`) that **hashes a stable user id** and routes A vs B by parity [^src4]:

```python
hashed_id = hashlib.md5(page_id.encode("UTF-8")).hexdigest()
if int(hashed_id, 16) % 2:
    return {"Prediction": self.model_a.predict(...)[0], "model": "Model A"}
else:
    return {"Prediction": self.model_b.predict(...)[0], "model": "Model B"}
```

Both models (A and B, differing in config/hyperparameters) are trained, logged, and registered with the `latest-model` alias, then the wrapper is registered and deployed so requests are split deterministically and you can see which model served each prediction [^src4]. For serving-endpoint authentication, the course uses a PAT in this lecture but moves to Service Principal OAuth for production — see [[mlops/ci-cd-for-ml|CI/CD for ML]] [^src4].

## Related

- [[mlops/drift-detection|Drift Detection]] — monitoring a served model once it's in production
- [[mlops/mlflow|MLflow]] — the registry/format and pyfunc wrapper behind Databricks Model Serving
- [[mlops/model-monitoring|Model Monitoring]] — inference tables log requests/responses from these endpoints
- [[mlops/production-ml-workflow|Production ML Workflow]] — Part 2 of the series: the training that produces the saved pipeline
- [[data-engineering/data-orchestration|Data Orchestration]] — Airflow DAGs, scheduling vs orchestration vs observability
- [[mlops/infrastructure-as-code|Infrastructure as Code]] · [[software-engineering/kubernetes|Kubernetes]] — the deployment/containerization substrate
- [[ai-engineering/machine-learning|Machine Learning]] — the training half that produces the saved pipeline (ai-engineering)
- [[mlops/README|MLOps hub]]

---

[^src1]: [Serving ML with Flask: Your First Spam Detection API (Vivek Bharti, Practical ML Series Part 3)](../../raw/email/email-2025-07-06-serving-ml-with-flask-your-first-spam-detection-api.md)
[^src2]: [Batch Inference with Airflow: Scaling Your Spam Classifier (Vivek Bharti, Practical ML Series Part 4)](../../raw/email/email-2025-07-20-batch-inference-with-airflow-scaling-your-spam-classifier.md)
[^src3]: [Model serving architectures (Marvelous MLOps, Lecture 5)](../../raw/email/email-2025-08-01-model-serving-architectures.md)
[^src4]: [Deploying Model Serving Endpoint & A/B Testing on Databricks (Marvelous MLOps, Lecture 6)](../../raw/email/email-2025-08-02-lecture-6-deploying-model-serving-endpoint-a-b-testing-on-da.md)

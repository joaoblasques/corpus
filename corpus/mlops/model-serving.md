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
aliases:
  - model serving
  - ml serving
  - model deployment
  - batch inference
  - real-time inference
  - inference api
  - flask ml api
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

## Related

- [[mlops/drift-detection|Drift Detection]] — monitoring a served model once it's in production
- [[data-engineering/data-orchestration|Data Orchestration]] — Airflow DAGs, scheduling vs orchestration vs observability
- [[mlops/infrastructure-as-code|Infrastructure as Code]] · [[software-engineering/kubernetes|Kubernetes]] — the deployment/containerization substrate
- [[ai-engineering/machine-learning|Machine Learning]] — the training half that produces the saved pipeline (ai-engineering)
- [[mlops/README|MLOps hub]]

---

[^src1]: [Serving ML with Flask: Your First Spam Detection API (Vivek Bharti, Practical ML Series Part 3)](../../raw/email/email-2025-07-06-serving-ml-with-flask-your-first-spam-detection-api.md)
[^src2]: [Batch Inference with Airflow: Scaling Your Spam Classifier (Vivek Bharti, Practical ML Series Part 4)](../../raw/email/email-2025-07-20-batch-inference-with-airflow-scaling-your-spam-classifier.md)

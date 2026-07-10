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
  - path: raw/_inbox/web-engineering-tts-inference-in-vllm-omni-3d405d3c.md
    channel: web
    ingested_at: 2026-07-02
aliases:
  - model serving
  - ml serving
  - TTS inference
  - vLLM-Omni
  - text-to-speech serving
  - Qwen3-TTS
  - VoxCPM2
  - Fish Speech
  - Higgs Audio V3
  - stage separation
  - CUDA Graph serving
  - torch.compile inference
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
updated: 2026-07-02
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
Minimal-setup caveats and the fixes [^src1]: add **input validation and logging**, **limit request size and rate**, **disable debug mode**, serve behind a production WSGI/ASGI server (**gunicorn / uvicorn**) rather than the Flask dev server, then **containerize with Docker** and deploy to a cloud platform (AWS / GCP / Heroku). See [Infrastructure as Code](/mlops/infrastructure-as-code.md) and [Kubernetes](/software-engineering/kubernetes.md) for the deployment substrate, and [Agent Security](/ai-engineering/agent-security.md) for the input-validation mindset on any model-facing endpoint.

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
[^src2]: use **dynamic filenames** (`incoming_emails_{{ ds }}.csv`) so each run reads its own partition; **log metrics** (spam rate, volume) to BigQuery or Postgres; **store data on S3/GCS** rather than local disk; and use **Airflow sensors** to trigger the DAG after an upload lands. Airflow itself supplies the scheduling, per-task logs, and dependency visualization — see [Data Orchestration](/data-engineering/data-orchestration.md) for why an orchestrator beats bare `cron` here.

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

The fix is **sticky assignment**: assign each user to a variant based on a stable identifier so they always get the same model during the test [^src4]. The course implements this with a pyfunc wrapper ([MLflow](/mlops/mlflow.md) `PythonModel`) that **hashes a stable user id** and routes A vs B by parity [^src4]:

```python
hashed_id = hashlib.md5(page_id.encode("UTF-8")).hexdigest()
if int(hashed_id, 16) % 2:
    return {"Prediction": self.model_a.predict(...)[0], "model": "Model A"}
else:
    return {"Prediction": self.model_b.predict(...)[0], "model": "Model B"}
```

Both models (A and B, differing in config/hyperparameters) are trained, logged, and registered with the `latest-model` alias, then the wrapper is registered and deployed so requests are split deterministically and you can see which model served each prediction [^src4]. For serving-endpoint authentication, the course uses a PAT in this lecture but moves to Service Principal OAuth for production — see [CI/CD for ML](/mlops/ci-cd-for-ml.md) [^src4].

## TTS Inference Engineering (vLLM-Omni)

Text-to-speech serving has different bottlenecks from text-only LLM inference. vLLM-Omni (Jun 2026) documents the engineering problems and solutions for four TTS models [^src5]:

### Why TTS differs from LLM serving

TTS systems are **multi-stage pipelines**: a Talker predicts codec tokens autoregressively (latency-bound), and a Code2Wav module reconstructs waveform audio in parallel (throughput-bound) [^src5]. If a scheduler treats both stages identically, Talker latency blocks Code2Wav, and Code2Wav parallelism is underused. Additionally:

- **Streaming has a strict latency budget** — users expect the first audio packet within a few hundred milliseconds (TTFP = Time To First Audio Packet).
- **Chunk size is a competing constraint** — small chunks reduce TTFP but hurt audio continuity across chunk boundaries; large chunks do the reverse.

### Optimization techniques by model

| Technique | Model(s) | Result |
|---|---|---|
| Stage separation + connector chunking | Qwen3-TTS, Higgs Audio V3 | Talker latency and Code2Wav throughput tuned independently |
| Batched decode preprocessing | Qwen3-TTS | Python-loop overhead removed from c=64 decode hot path |
| Whole-forward `torch.compile` | VoxCPM2 | Dynamo sees full 28-layer loop; cudaLaunchKernel count −71% |
| CFM/LocDiT decode-tail batching | VoxCPM2 | Per-request tiny diffusion calls batched across requests |
| GPU-resident decode state | Higgs Audio V3 | Multi-codebook state moved from Python dict to GPU tensors |
| Model-specific Triton kernel (q_len=1) | Fish Speech S2 Pro | Bypasses generic paged/varlen overhead for pure-decode shape |

### Key findings

**Qwen3-TTS** (H20×2, c=64, voice cloning): audio throughput +61.5% (26.55 → 42.88 audio-s/s); P99 E2EL −49.4% (17.7s → 9.0s) [^src5]. Achieved by: decoupling codec_chunk_frames (streaming) from decode_chunk_frames (Code2Wav window), batching speaker-embedding mel/STFT on GPU, trailing_text buffer offset trick (avoid tensor allocation per step), CUDA Graph on Code2Wav [^src5].

**VoxCPM2** (H20×1, c=64): audio throughput +172% (12.16 → 33.07 audio-s/s); request throughput +158.8% [^src5]. Key: wrapping the full `Model.forward` in `torch.compile(fullgraph=False)` — not per-layer — so Dynamo sees the whole 28-layer loop and PagedAttention graph breaks are minimised. Plus CFM/LocDiT decode-tail batching (scatter-gather over requests), VAE sliding-window decode (O(N²) → O(N)) [^src5].

**Fish Speech S2 Pro** (H20, c=64): bottleneck is GPU-side q_len=1 attention, not Python preprocessing. Fix: model-specific Triton kernel for SlowAR decode attention — hard-coded to q_len=1, fp16/bf16, head_dim=128, block_size=16; short sequences use standard online softmax; long sequences use split-partial-combine. Dispatches via CPU upper-bound (seq_lens_cpu_upper_bound) to avoid GPU-to-CPU sync on sequence length [^src5].

**Higgs Audio V3** (H20, c=16): 2.70× speedup vs baseline. Bottleneck is multi-codebook Python dict state machine (delay pattern, EOC ramp-down). Fix: GPU-resident batched tensors for per-request decode state; CUDA Graph adapted for dynamic batch shapes by making decode_mask uniform (all True) [^src5].

### General principles extracted

- **Profile before optimizing** — GPU utilization at 14% with c=64 signals the bottleneck is serving-path overhead (Python scheduling, small tensor allocation, kernel launch), not GPU FLOPs.
- **Whole-model compile > per-layer compile** — per-layer torch.compile adds many Python↔compiled transitions; wrapping the full forward pass is usually better despite graph breaks.
- **Avoid `.item()` in tight loops** — `.item()` on a 0-dim GPU tensor forces GPU→CPU sync; one utterance with 60 decode steps × 4 `.item()` calls = ~2,400 synchronizations. Replace with GPU-side `.copy_()`.
- **O(N²) accumulate-and-re-decode is a trap** — any "accumulate all generated tokens then decode from scratch" pattern grows quadratically. Sliding-window decode is always O(N).

## Related

- [Drift Detection](/mlops/drift-detection.md) — monitoring a served model once it's in production
- [MLflow](/mlops/mlflow.md) — the registry/format and pyfunc wrapper behind Databricks Model Serving
- [Model Monitoring](/mlops/model-monitoring.md) — inference tables log requests/responses from these endpoints
- [Production ML Workflow](/mlops/production-ml-workflow.md) — Part 2 of the series: the training that produces the saved pipeline
- [Data Orchestration](/data-engineering/data-orchestration.md) — Airflow DAGs, scheduling vs orchestration vs observability
- [Infrastructure as Code](/mlops/infrastructure-as-code.md) · [Kubernetes](/software-engineering/kubernetes.md) — the deployment/containerization substrate
- [Machine Learning](/ai-engineering/machine-learning.md) — the training half that produces the saved pipeline (ai-engineering)
- [MLOps hub](/mlops/README.md)

---

[^src1]: [Serving ML with Flask: Your First Spam Detection API (Vivek Bharti, Practical ML Series Part 3)](../../raw/email/email-2025-07-06-serving-ml-with-flask-your-first-spam-detection-api.md)
[^src2]: [Batch Inference with Airflow: Scaling Your Spam Classifier (Vivek Bharti, Practical ML Series Part 4)](../../raw/email/email-2025-07-20-batch-inference-with-airflow-scaling-your-spam-classifier.md)
[^src3]: [Model serving architectures (Marvelous MLOps, Lecture 5)](../../raw/email/email-2025-08-01-model-serving-architectures.md)
[^src4]: [Deploying Model Serving Endpoint & A/B Testing on Databricks (Marvelous MLOps, Lecture 6)](../../raw/email/email-2025-08-02-lecture-6-deploying-model-serving-endpoint-a-b-testing-on-da.md)
[^src5]: [Engineering TTS Inference in vLLM-Omni (vLLM blog, Jun 23 2026)](../../raw/web/web-engineering-tts-inference-in-vllm-omni-3d405d3c.md)

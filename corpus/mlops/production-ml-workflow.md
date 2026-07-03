---
type: concept
domain: mlops
status: draft
sources:
  - path: raw/email/email-2025-06-29-build-a-spam-classifier-like-a-production-ml-engineer.md
    channel: email
    ingested_at: 2026-06-19
  - path: raw/youtube/youtube-mvleESOUTRw-production-grade-ai-project-tutorial-build-deploy.md
    channel: youtube
    ingested_at: 2026-06-20
aliases:
  - production ml workflow
  - production-minded training
  - spam classifier
  - holdout set
  - business metric optimization
  - sklearn pipeline serialization
  - practical ml series part 2
tags:
  - corpus/mlops
  - concept
created: 2026-06-19
updated: 2026-06-19
---

# Production-Minded ML Training Workflow

**TL;DR.** This is **Part 2 of the Practical ML Series** — training a spam classifier on the SMS Spam Collection dataset, but taking "a production-minded, real-world approach at every step" [^src1]. The disciplines: a **holdout set** for final unbiased evaluation, robust text preprocessing, comparing multiple models with real-world tradeoffs, **optimizing for the right business metric**, and serializing the model as one sklearn pipeline for seamless deployment [^src1]. The headline lesson: *"it's not about the most optimized score — it's about optimizing for the right business metric"* [^src1]. The serving half of the series (Parts 3 & 4) is covered in [Model Serving](/mlops/model-serving.md); this page is the training half that produces the saved pipeline.

## Holdout set (prevent leakage, final eval)

Most tutorials split into train/test, but in production "you almost always need an unseen holdout set — data that stays hidden until the very end" for realistic final evaluation [^src1]. The data is split with a stratified 10% holdout (`train_test_split(..., test_size=0.1, stratify=df['label'])`) and saved to disk to simulate a real pipeline where training/testing/deployment are separate [^src1]. Why it matters: tuning hyperparameters or writing preprocessing logic against test data indirectly *leaks* information; a holdout set "keeps you honest" about generalization [^src1].

## Robust text preprocessing

Text is noisy — words appear in different forms ("Win" vs "winning"), punctuation adds clutter, and stopwords add little value [^src1]. The preprocessing lowercases text, removes punctuation, eliminates stopwords, and applies **Porter stemming** (via NLTK), reducing dimensionality and improving generalization [^src1]:

```python
def preprocess_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t not in stopwords.words('english')]
    return ' '.join(PorterStemmer().stem(t) for t in tokens)
```

## Compare multiple models

Rather than assume one model is best, train and compare several [^src1]: **Logistic Regression** (strong text baseline), **SVM** (effective in high-dimensional space), **Multinomial Naive Bayes** (classic for NLP), and **Random Forest** (a powerful non-linear baseline), each wrapped in a `TfidfVectorizer` + classifier pipeline and scored with a classification report [^src1].

## Optimize for the right business metric

The dataset is imbalanced (~86% ham), which shapes the choice of evaluation metric [^src1]. Logistic Regression gave the best balance of precision and recall, especially for the minority spam class; SVM had slightly higher overall accuracy but **lower recall**, so Logistic Regression was chosen [^src1]. The reasoning: *"recall is more important as we don't want to misclassify the spam as ham, since then it will come in the inbox"* [^src1]. Even a grid search (scoring recall on the spam class) didn't win: the **default model achieved 92% recall** vs the best grid-search model's 91% (with slightly higher precision), so the default was kept — *missing spam is worse than mistakenly flagging ham* [^src1].

## Serialize as one sklearn Pipeline

The final model is retrained **on all available data** (train + test) before saving, to use every example [^src1]. It is saved as a **single sklearn `Pipeline`** containing both the TF-IDF vectorizer and the logistic-regression classifier, "so the exact same preprocessing steps are applied during inference, making deployment seamless and reproducible" [^src1]:

```python
final_model = Pipeline([('tfidf', TfidfVectorizer(stop_words='english')),
                        ('clf', LogisticRegression(class_weight='balanced', max_iter=1000))])
final_model.fit(X_full, y_full)
pickle.dump(final_model, open('logreg_spam_pipeline.pkl', 'wb'))
```

This bundling of vectorizer + classifier in one `.pkl` is exactly the saved pipeline the [Flask serving API](/mlops/model-serving.md) later loads in Part 3 [^src1].

## Final holdout check

The saved model is validated on the untouched holdout set as the last step, confirming generalization with no overfitting: **97% accuracy and 89% recall** on the spam class — "a solid indicator that the pipeline is production-ready" [^src1].

## Key takeaways

Prepare for deployment from day 1 (holdout sets + robust pipelines); don't just chase accuracy — choose metrics reflecting the real-world cost of errors; and save the model + vectorizer in one pipeline for easy deployment [^src1].

## Enterprise-grade training data curation (freeCodeCamp)

A second reference implementation (Aush Singh, freeCodeCamp) takes the opposite framing: **real ML is pipelines, not accuracy scores** [^src2]. The project is an enterprise-grade LLM training-data curation bot — a system that discovers, processes, classifies, and summarizes source data to produce a clean training corpus.

### Architecture patterns

**Python project structure** [^src2]:
- `__init__.py` as the main entrance pattern — keeps the entry point clean and importable.
- Central `logging` module configured once at startup; all modules import from it.
- Unified error handling pattern: every module's errors bubble up to a top-level handler that logs with context (module name, input, error type) rather than silently swallowing.
- Unified loader class: one `DataLoader` that accepts any source type (PDFs, web pages, emails, databases); callers don't need to know which parser runs underneath.

**Async data pipelines** [^src2]: use `asyncio` for I/O-bound stages (fetching, embedding API calls); keep CPU-bound stages (classification, summarization) synchronous or thread-pool-isolated.

**Prompt engineering at scale** [^src2]: when a pipeline calls an LLM thousands of times, prompts must be:
- Versioned (stored in code, not hardcoded strings).
- Input-length-aware (truncate inputs before the context window fills).
- Output-format-strict (JSON schema in the prompt; validate before storing).

### The 12–14 step build

The full project spans: data discovery → source loading → pre-processing (cleaning/chunking) → embedding → semantic deduplication → quality scoring → classification → summarization → storage → lineage tracking → QA → export for LLM training [^src2]. Each step is a standalone pipeline stage that can be re-run independently — the same idempotency principle as [Idempotent Pipelines](/data-engineering/idempotent-pipelines.md).

> "Real ML engineering is building systems that *reliably produce* good data for the model — not tweaking model hyperparameters." [^src2]

## See also

- [Model Serving](/mlops/model-serving.md) — Parts 3 & 4 of this series: the Flask API and Airflow batch job that serve this saved pipeline
- [MLflow](/mlops/mlflow.md) — the registry/format that wraps a similar sklearn pipeline in the Databricks course
- [Model Monitoring](/mlops/model-monitoring.md) — what watches such a model once it's deployed
- [MLOps hub](/mlops/README.md)

---

[^src1]: [Build a Spam Classifier Like a Production ML Engineer (Vivek Bharti, Practical ML Series Part 2)](../../raw/email/email-2025-06-29-build-a-spam-classifier-like-a-production-ml-engineer.md)
[^src2]: [Production-Grade AI Project Tutorial — Build & Deploy (freeCodeCamp / Aush Singh)](../../raw/youtube/youtube-mvleESOUTRw-production-grade-ai-project-tutorial-build-deploy.md)
</content>

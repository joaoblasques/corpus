---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/youtube/youtube-5NgNicANyqM-harvard-cs50s-artificial-intelligence-with-python-full-unive.md
    channel: youtube
    ingested_at: 2026-06-15
  - path: raw/youtube/youtube-JMUxmLyrhSk-artificial-intelligence-full-course-artificial-intelligence.md
    channel: youtube
    ingested_at: 2026-06-15
  - path: raw/web/github-rohitg00-ai-engineering-from-scratch-learn-it-build-i.md
    channel: web
    ingested_at: 2026-06-15
  - path: raw/youtube/youtube-5DtjQrROUzY-ai-was-hard-until-i-learned-these-10-concepts.md
    channel: youtube
    ingested_at: 2026-06-15
aliases:
  - machine learning
  - ML
  - supervised learning
  - unsupervised learning
  - reinforcement learning
  - fine-tuning
  - classical ML
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-15
updated: 2026-06-15
---

# Machine Learning

**TL;DR**: The subset of [[ai-engineering/ai-fundamentals|AI]] where, instead of programming a solution explicitly, you give a system data and let it learn to perform a task better with more data and experience [^src1]. Classical ML (regression, trees, SVMs, clustering) remains "the backbone of most production AI" and is the layer beneath deep learning and LLMs [^src3].

## The three learning paradigms

| Paradigm | Signal | Examples |
|---|---|---|
| **Supervised** | Labeled input→output pairs | Linear/logistic regression, decision trees, random forests, SVMs, KNN, naive Bayes [^src3] |
| **Unsupervised** | No labels — find structure | K-means, DBSCAN, PCA (dimensionality reduction) [^src1][^src3] |
| **Reinforcement** | Reward signal from actions | Q-learning, SARSA, policy gradients, PPO — the foundation of RLHF [^src1][^src3] |

Supervised learning splits into **classification** (discrete labels — e.g. "is this email spam?") and **regression** (continuous values) [^src1]. The canonical intuition: your email inbox learns which messages are spam from past examples rather than from hand-written rules [^src1].

## How training works (the line-fitting intuition)

A model is a parameterized function; *training* is finding parameter values that fit known input→output pairs (training data) [^src4]. The simplest case — fitting `y = mx + c` from two known points — generalizes to billions of parameters: an LLM "is an equation like this but it contains greater than a billion parameters," and you need correspondingly large training data to pin them down [^src4]. The fit is driven by a **loss function** that measures predicted-vs-actual error and feeds the difference back to adjust parameters, repeated over billions of examples [^src4]. (The full neural-network version of this loop is in [[ai-engineering/neural-network|Neural Networks]].)

## Bias, variance, and overfitting

The central failure mode: a model that memorizes training data but fails to generalize is **overfit** [^src1]. The **bias–variance tradeoff** governs this — too simple (high bias, underfits) vs too flexible (high variance, overfits) [^src1]. Defenses: **cross-validation** (hold out data to estimate true performance), regularization, and ensemble methods (bagging, boosting, stacking) [^src1][^src3]. Evaluation metrics — accuracy, precision, recall — measure whether a model actually worked, not just that it ran [^src3].

## Where ML meets the LLM stack: RAG vs fine-tuning

A practical rule that recurs across sources: **use RAG when a model needs specific facts it wasn't trained on; use fine-tuning when you need it to *behave* differently** (tone, format, domain vocabulary) — and you can combine both [^src5]. Fine-tuning takes a pre-trained model and trains it further on a smaller specialized dataset so it adopts a particular style or output structure [^src5]. See [[ai-engineering/rag|RAG]] and [[ai-engineering/llm|LLM]] (training phases).

## The from-scratch curriculum

The `ai-engineering-from-scratch` curriculum sequences ML as a foundation layer — Phase 2 (classical ML: regression → trees → SVM → KNN → k-means → feature engineering → evaluation → ensembles), built *before* Phase 3 deep learning, on the principle "every algorithm gets built from raw math first... by the time PyTorch shows up, you already know what it's doing under the hood" [^src3]. Classical ML is explicitly "still the backbone of most production AI" [^src3].

## See also

- [[ai-engineering/ai-fundamentals|AI Fundamentals]] — ML is the learning branch of the broader field
- [[ai-engineering/neural-network|Neural Networks]] — deep learning, the multi-layer extension of ML
- [[ai-engineering/statistics-for-ml|Statistics & Probability for ML]] — the math ML rests on (distributions, regression, inference)
- [[ai-engineering/llm|LLM]] — large-scale supervised next-token learning + RLHF
- [[ai-engineering/learning-ai-engineering|Learning AI Engineering]] — the "learn ML in 2026" path
- [[ai-engineering/README|AI Engineering hub]]

---

[^src1]: [Harvard CS50's AI with Python (full course)](../../raw/youtube/youtube-5NgNicANyqM-harvard-cs50s-artificial-intelligence-with-python-full-unive.md) — Brian Yu
[^src2]: [Artificial Intelligence Full Course](../../raw/youtube/youtube-JMUxmLyrhSk-artificial-intelligence-full-course-artificial-intelligence.md) — Edureka
[^src3]: [ai-engineering-from-scratch](../../raw/web/github-rohitg00-ai-engineering-from-scratch-learn-it-build-i.md) — Rohit Ghumare
[^src4]: [AI Product Management Complete Course](../../raw/youtube/youtube-KjYCEiBTHFo-ai-product-management-complete-course-3-5-hours-masterclass.md) — [15:32](../../raw/youtube/youtube-KjYCEiBTHFo-ai-product-management-complete-course-3-5-hours-masterclass.md#t=15:32)
[^src5]: [AI was HARD until I Learned these 10 Concepts](../../raw/youtube/youtube-5DtjQrROUzY-ai-was-hard-until-i-learned-these-10-concepts.md) — Maddy Zhang, [06:31](../../raw/youtube/youtube-5DtjQrROUzY-ai-was-hard-until-i-learned-these-10-concepts.md#t=6:31)

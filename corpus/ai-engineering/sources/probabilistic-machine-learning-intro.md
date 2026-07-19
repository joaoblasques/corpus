---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/pdf/pdf-probabilistic-machine-learning-an-introduction-part-01.md
    channel: pdf
    ingested_at: 2026-07-19
  - path: raw/pdf/pdf-probabilistic-machine-learning-an-introduction-part-02.md
    channel: pdf
    ingested_at: 2026-07-19
  - path: raw/pdf/pdf-probabilistic-machine-learning-an-introduction-part-03.md
    channel: pdf
    ingested_at: 2026-07-19
  - path: raw/pdf/pdf-probabilistic-machine-learning-an-introduction-part-04.md
    channel: pdf
    ingested_at: 2026-07-19
  - path: raw/pdf/pdf-probabilistic-machine-learning-an-introduction-part-05.md
    channel: pdf
    ingested_at: 2026-07-19
  - path: raw/pdf/pdf-probabilistic-machine-learning-an-introduction-part-06.md
    channel: pdf
    ingested_at: 2026-07-19
  - path: raw/pdf/pdf-probabilistic-machine-learning-an-introduction-part-07.md
    channel: pdf
    ingested_at: 2026-07-19
  - path: raw/pdf/pdf-probabilistic-machine-learning-an-introduction-part-08.md
    channel: pdf
    ingested_at: 2026-07-19
  - path: raw/pdf/pdf-probabilistic-machine-learning-an-introduction-part-09.md
    channel: pdf
    ingested_at: 2026-07-19
aliases:
  - PML
  - Probabilistic Machine Learning An Introduction
  - Murphy PML
  - Murphy 2022
tags:
  - corpus/ai-engineering
  - source
created: 2026-07-19
updated: 2026-07-19
---

# Probabilistic Machine Learning: An Introduction (Murphy, 2022)

TL;DR: Modern probabilistic ML textbook by Kevin P. Murphy (MIT Press, 2022; CC-BY-NC-ND). Successor to his 2012 "Machine Learning: A Probabilistic Perspective." Covers supervised/unsupervised learning, deep neural networks, nonparametric methods, and beyond — 860 pages, Python throughout (JAX, PyTorch, scikit-learn). See [Kevin P. Murphy](/ai-engineering/kevin-murphy.md).

## Structure (23 chapters + appendices)

**Part I — Foundations (Chapters 1-8)**

| Chapter | Topic |
|---|---|
| 1 | Introduction: supervised/unsupervised/RL; overfitting and generalization; no-free-lunch theorem |
| 2 | Probability: Univariate Models — Bayes' rule, Bernoulli/Gaussian/Student-t/Beta/Gamma distributions |
| 3 | Probability: Multivariate Models — joint distributions, MVN, exponential family, mixture models, PGMs |
| 4 | Statistics — MLE, empirical risk minimization, regularization (MAP/ridge/lasso/elastic net), Bayesian stats, frequentist decision theory |
| 5 | Decision Theory — Bayesian decision theory, ROC curves, model selection (BIC/AIC), hypothesis testing |
| 6 | Information Theory — entropy, KL divergence, mutual information, data processing inequality, sufficient statistics |
| 7 | Linear Algebra — vector spaces, norms, matrix multiplication, eigenvalue decomposition, SVD, Cholesky |
| 8 | Optimization — gradient descent, momentum, SGD, Newton/quasi-Newton, constrained optimization (KKT, LP/QP), EM |

**Part II — Linear Models (Chapters 9-12)**

Linear/quadratic discriminant analysis, logistic regression, linear regression (Ridge/Lasso/Bayesian), generalized linear models.

**Part III — Deep Neural Networks (Chapters 13-15)**

MLPs, backpropagation (including vector-Jacobian products), training tricks (residual connections, dropout, batch norm), CNNs (LeNet→AlexNet→ResNet→DenseNet), RNNs, transformers, large language models.

**Parts IV-V — Nonparametric & Beyond Supervised (Chapters 16-23)**

KNN, kernel methods (GPs, SVMs), decision trees/forests/boosting; few-shot learning, transfer learning, semi-supervised learning; dimensionality reduction (PCA, VAE, t-SNE, word embeddings); clustering; recommender systems; graph embeddings.

## Key ideas

- **Probabilistic framing**: "all unknown quantities are random variables endowed with probability distributions." This makes ML methods interoperate with stochastic optimization, control theory, information theory, and statistical physics. [^pml-p01]
- **Classification fundamentals** (Chapter 1): a decision tree of depth 2 can separate Iris flowers using only petal-length and petal-width; empirical risk minimization defines model fitting; generalization — not training accuracy — is the actual goal. [^pml-p01]
- **Change of variables** (Chapter 2): for an invertible function y = f(x), p(y) = p(x)|dx/dy|; the multivariate generalization uses the absolute Jacobian determinant. [^pml-p05]
- **Deep learning revolution** (Chapter 13): the 2012 AlexNet win on ImageNet demonstrated that GPU-backed DNNs, pre-trained on large labeled datasets (ImageNet / Mechanical Turk), dramatically outperform handcrafted systems. [^pml-p01]
- Python-first (JAX/PyTorch/scikit-learn); all figures reproducible via linked Jupyter notebooks on Colab.

## Relationship to other corpus sources

- The treatment of SVD (Chapter 7) and PCA (Chapter 20) complements the Brunton-Kutz geometric viewpoint on [Singular Value Decomposition](/ai-engineering/singular-value-decomposition.md).
- The transformer coverage (Chapter 15) gives a probabilistic framing of [Attention Mechanisms](/ai-engineering/attention-mechanisms.md) and [LLM](/ai-engineering/llm.md).
- Word embeddings (Chapter 20) ground the [Embeddings](/ai-engineering/embeddings.md) page.
- The EM/GMM chapter supports [Gaussian Mixture Models](/ai-engineering/gaussian-mixture-models.md).

## Related corpus pages

- [Kevin P. Murphy](/ai-engineering/kevin-murphy.md)
- [Machine Learning](/ai-engineering/machine-learning.md)
- [Probability and Statistics for Machine Learning](/ai-engineering/probability-and-statistics-for-ml.md)
- [Optimization for Machine Learning](/ai-engineering/optimization-for-ml.md)
- [Linear Algebra for Machine Learning](/ai-engineering/linear-algebra-for-ml.md)
- [Singular Value Decomposition](/ai-engineering/singular-value-decomposition.md)
- [Gaussian Mixture Models](/ai-engineering/gaussian-mixture-models.md)
- [Attention Mechanisms](/ai-engineering/attention-mechanisms.md)
- [Embeddings](/ai-engineering/embeddings.md)

[^pml-p01]: raw/pdf/pdf-probabilistic-machine-learning-an-introduction-part-01.md — Preface, table of contents, Chapter 1 (Introduction to ML)
[^pml-p05]: raw/pdf/pdf-probabilistic-machine-learning-an-introduction-part-05.md — Chapter 2: transformations of random variables, change of variables formula

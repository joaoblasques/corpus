---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/pdf/pdf-a-course-in-machine-learning-part-01.md
    channel: pdf
    ingested_at: 2026-07-22
  - path: raw/pdf/pdf-a-course-in-machine-learning-part-02.md
    channel: pdf
    ingested_at: 2026-07-22
  - path: raw/pdf/pdf-a-course-in-machine-learning-part-03.md
    channel: pdf
    ingested_at: 2026-07-22
  - path: raw/pdf/pdf-a-course-in-machine-learning-part-04.md
    channel: pdf
    ingested_at: 2026-07-22
  - path: raw/pdf/pdf-a-course-in-machine-learning-part-05.md
    channel: pdf
    ingested_at: 2026-07-22
  - path: raw/pdf/pdf-a-course-in-machine-learning-part-06.md
    channel: pdf
    ingested_at: 2026-07-22
  - path: raw/pdf/pdf-a-course-in-machine-learning-part-07.md
    channel: pdf
    ingested_at: 2026-07-22
  - path: raw/pdf/pdf-a-course-in-machine-learning-part-08.md
    channel: pdf
    ingested_at: 2026-07-22
  - path: raw/pdf/pdf-a-course-in-machine-learning-part-09.md
    channel: pdf
    ingested_at: 2026-07-22
  - path: raw/pdf/pdf-a-course-in-machine-learning-part-10.md
    channel: pdf
    ingested_at: 2026-07-22
aliases:
  - A Course in Machine Learning
  - CIML
  - Daumé machine learning
  - Hal Daumé III textbook
  - course in machine learning
  - pedagogical machine learning textbook
tags:
  - corpus/ai-engineering
  - source
created: 2026-07-22
updated: 2026-07-22
---

# A Course in Machine Learning (Daumé III, 2015)

**TL;DR**: An open, pedagogically-organized introductory ML textbook by Hal Daumé III (2015, online at hal3.name/courseml/; 193pp). Organized by building intuition before math, focusing on ideas and models over formalism. Unlike research-oriented texts (Bishop, Murphy), it sequences concepts for learners rather than researchers — decision trees before perceptrons, geometrical intuitions before linear algebra. Covers 19 chapters: supervised learning fundamentals through unsupervised, semi-supervised, graphical models, and online learning. All 10 parts ingested (complete). [^ciml-p01]

## Core learning framework

The book's central framing: **inductive machine learning** = given a loss function ℓ and training sample D from unknown distribution D, compute f minimizing expected loss E_{(x,y)~D}[ℓ(y, f(x))]. The training-test split is the cardinal rule: never use test data for any training decisions. [^ciml-p01]

Key concepts introduced in Chapter 1:
- **Generalization**: the goal is performance on unseen test data, not training data
- **Inductive bias**: every learning algorithm embodies preferences; decision trees prefer shallow over deep explanations
- **Underfitting vs. overfitting**: the fundamental tradeoff — too simple (empty tree) vs. too complex (full tree memorizing training data)
- **Hyperparameters**: knobs that control the inductive bias (e.g., max depth of decision tree); cannot be tuned on training data

## Design techniques

### Decision trees (Chapter 1)
Greedy top-down construction: at each node, pick the feature that maximizes majority-vote accuracy on the current partition. Algorithm `DecisionTreeTrain(data, remaining_features)` recurses until data is unambiguous or no features remain. Base cases: all-same-label (return leaf) or no features left (return majority guess). Prediction: recurse down tree following feature values to a leaf. [^ciml-p01]

Two extreme cases:
- Empty tree (depth=0): always predicts majority class; high bias, low variance
- Full tree: memorizes training data; zero training error, ~50% error on unseen data; high variance

### Perceptron (Chapter 3)
Online mistake-driven learner. Represents a linear separator **w** (weight vector). On each example (x, y): predict ŷ = sign(w·x); if ŷ ≠ y, update w ← w + y·x. Convergence theorem: if data is linearly separable with margin γ and all ‖x‖ ≤ R, the perceptron converges in at most (R/γ)² mistakes. Non-separable case → vote/average variants (voted perceptron). [^ciml-p03]

### Linear models (Chapter 6)
Logistic regression uses the sigmoid function σ(a) = 1/(1+e^{-a}) to produce probabilistic predictions. Trained via gradient descent on negative log-likelihood. The gradient update for SGD: w ← w + α·(y − σ(w·x))·x. Equivalent to the perceptron update when probability is near 0/1. [^ciml-p06]

### Neural networks (Chapter 8)
Multi-layer feedforward networks compose linear transformations with nonlinear activations (sigmoid, tanh, ReLU). The key breakthrough is backpropagation: compute gradients layer by layer via chain rule. Hidden layers learn feature representations automatically. Universal approximation: a single hidden layer with enough units approximates any continuous function. [^ciml-p08]

### Kernel methods (Chapter 9)
The **kernel trick**: replace dot products x·z with a kernel function K(x, z) = φ(x)·φ(z), allowing implicit feature maps into very high (or infinite) dimensional spaces. The support vector machine finds the maximum-margin hyperplane; the kernel trick makes it operate in feature space without computing φ explicitly. Key kernels: polynomial K(x,z) = (x·z + c)^d, Gaussian/RBF K(x,z) = exp(−‖x−z‖²/(2σ²)). [^ciml-p09]

### Learning theory (Chapter 10)
**PAC learning** (probably approximately correct): a concept class is PAC-learnable if for any ε, δ there is an algorithm that, with sample size polynomial in 1/ε, 1/δ, and concept complexity, outputs a hypothesis with error ≤ ε with probability ≥ 1−δ. The **VC dimension** of a hypothesis class H is the size of the largest shattered set. Finite VC dimension implies uniform convergence and PAC learnability. Generalization bound: error ≤ training error + O(√(VCdim(H)/m)) (m = sample size). [^ciml-p10]

### Ensemble methods (Chapter 11)
**Bagging**: train L models on bootstrap samples; average predictions. Reduces variance. **Boosting** (AdaBoost): maintain a weight distribution over training examples; at each round, train a weak classifier on the distribution, then upweight misclassified examples. Final classifier is a weighted majority vote. Boosting drives training error to 0 and generalizes via margin theory (margins of correctly-classified examples). [^ciml-p11]

### Unsupervised learning (Chapter 13)
**K-means clustering**: iteratively assign each point to the nearest centroid, then recompute centroids as means of assigned points. Converges to a local optimum. Objective: minimize total squared distance to cluster centers. **PCA** (principal component analysis): finds orthogonal directions of maximum variance; projects data to a lower-dimensional subspace. Computed via SVD of the data matrix. [^ciml-p13]

### Expectation-maximization (Chapter 14)
**EM algorithm**: for models with latent variables (e.g., Gaussian mixture models), alternate between E-step (compute posterior over latent variables given current parameters) and M-step (maximize expected log-likelihood). Monotonically increases the marginal likelihood; converges to a local maximum. Gaussian mixture models: soft-assign each point to a Gaussian component; re-estimate means/variances/mixing weights. [^ciml-p14]

## Connections to other corpus pages

- [Machine Learning](/ai-engineering/machine-learning.md) — conceptual overview; this source is a primary reference for decision tree algorithms, learning theory, and ensemble methods
- [Neural Network](/ai-engineering/neural-network.md) — Chapter 8 is a concise treatment of feedforward nets and backpropagation
- [Reinforcement Learning](/ai-engineering/reinforcement-learning.md) — Chapter 17 (online learning) is related to bandit problems; RL is not covered directly but contextualizes the learning paradigm
- [Probabilistic Machine Learning (Murphy)](/ai-engineering/sources/probabilistic-machine-learning-intro.md) — more rigorous probabilistic treatment of many of the same concepts

---

[^ciml-p01]: raw/pdf/pdf-a-course-in-machine-learning-part-01.md — Chapter 1: decision trees, generalization, inductive bias, underfitting/overfitting, loss functions, PAC setup
[^ciml-p03]: raw/pdf/pdf-a-course-in-machine-learning-part-03.md — Chapter 3: perceptron, online learning, mistake bound, convergence theorem
[^ciml-p06]: raw/pdf/pdf-a-course-in-machine-learning-part-06.md — Chapter 6: linear models, logistic regression, sigmoid, gradient descent
[^ciml-p08]: raw/pdf/pdf-a-course-in-machine-learning-part-08.md — Chapter 8: neural networks, backpropagation, universal approximation
[^ciml-p09]: raw/pdf/pdf-a-course-in-machine-learning-part-09.md — Chapter 9: kernel methods, SVM, polynomial and RBF kernels
[^ciml-p10]: raw/pdf/pdf-a-course-in-machine-learning-part-10.md — Chapter 10: learning theory, PAC learning, VC dimension, generalization bounds
[^ciml-p11]: raw/pdf/pdf-a-course-in-machine-learning-part-11.md — Chapter 11: ensemble methods, bagging, AdaBoost
[^ciml-p13]: raw/pdf/pdf-a-course-in-machine-learning-part-13.md — Chapter 13: unsupervised learning, k-means, PCA
[^ciml-p14]: raw/pdf/pdf-a-course-in-machine-learning-part-14.md — Chapter 14: expectation-maximization, Gaussian mixture models

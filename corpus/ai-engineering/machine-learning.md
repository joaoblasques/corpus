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
  - path: raw/youtube/youtube-URtF_UHYBSo-the-elegant-math-behind-machine-learning.md
    channel: youtube
    ingested_at: 2026-06-20
  - path: raw/youtube/youtube-_hdUddANh_o-how-to-learn-machine-learning-like-a-genius-and-not-waste-ti.md
    channel: youtube
    ingested_at: 2026-06-20
  - path: raw/pdf/pdf-foundations-of-data-science-part-01.md
    channel: pdf
    ingested_at: 2026-07-14
aliases:
  - machine learning
  - ML
  - supervised learning
  - unsupervised learning
  - reinforcement learning
  - fine-tuning
  - classical ML
  - VC dimension
  - Vapnik-Chervonenkis dimension
  - perceptron
  - boosting
  - stochastic gradient descent
  - SGD
  - online learning
  - Occam's Razor
  - generalization
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-15
updated: 2026-07-14
---

# Machine Learning

**TL;DR**: The subset of [AI](/ai-engineering/ai-fundamentals.md) where, instead of programming a solution explicitly, you give a system data and let it learn to perform a task better with more data and experience [^src1]. Classical ML (regression, trees, SVMs, clustering) remains "the backbone of most production AI" and is the layer beneath deep learning and LLMs [^src3].

## The three learning paradigms

| Paradigm | Signal | Examples |
|---|---|---|
| **Supervised** | Labeled input→output pairs | Linear/logistic regression, decision trees, random forests, SVMs, KNN, naive Bayes [^src3] |
| **Unsupervised** | No labels — find structure | K-means, DBSCAN, PCA (dimensionality reduction) [^src1][^src3] |
| **Reinforcement** | Reward signal from actions | Q-learning, SARSA, policy gradients, PPO — the foundation of RLHF [^src1][^src3] |

Supervised learning splits into **classification** (discrete labels — e.g. "is this email spam?") and **regression** (continuous values) [^src1]. The canonical intuition: your email inbox learns which messages are spam from past examples rather than from hand-written rules [^src1].

## How training works (the line-fitting intuition)

A model is a parameterized function; *training* is finding parameter values that fit known input→output pairs (training data) [^src4]. The simplest case — fitting `y = mx + c` from two known points — generalizes to billions of parameters: an LLM "is an equation like this but it contains greater than a billion parameters," and you need correspondingly large training data to pin them down [^src4]. The fit is driven by a **loss function** that measures predicted-vs-actual error and feeds the difference back to adjust parameters, repeated over billions of examples [^src4]. (The full neural-network version of this loop is in [Neural Networks](/ai-engineering/neural-network.md).)

## Bias, variance, and overfitting

The central failure mode: a model that memorizes training data but fails to generalize is **overfit** [^src1]. The **bias–variance tradeoff** governs this — too simple (high bias, underfits) vs too flexible (high variance, overfits) [^src1]. Defenses: **cross-validation** (hold out data to estimate true performance), regularization, and ensemble methods (bagging, boosting, stacking) [^src1][^src3]. Evaluation metrics — accuracy, precision, recall — measure whether a model actually worked, not just that it ran [^src3].

## Where ML meets the LLM stack: RAG vs fine-tuning

A practical rule that recurs across sources: **use RAG when a model needs specific facts it wasn't trained on; use fine-tuning when you need it to *behave* differently** (tone, format, domain vocabulary) — and you can combine both [^src5]. Fine-tuning takes a pre-trained model and trains it further on a smaller specialized dataset so it adopts a particular style or output structure [^src5]. See [RAG](/ai-engineering/rag.md) and [LLM](/ai-engineering/llm.md) (training phases).

## The from-scratch curriculum

The `ai-engineering-from-scratch` curriculum sequences ML as a foundation layer — Phase 2 (classical ML: regression → trees → SVM → KNN → k-means → feature engineering → evaluation → ensembles), built *before* Phase 3 deep learning, on the principle "every algorithm gets built from raw math first... by the time PyTorch shows up, you already know what it's doing under the hood" [^src3]. Classical ML is explicitly "still the backbone of most production AI" [^src3].

## The mathematics of ML: elegant theorems (Why Machines Learn)

An interview with Anil Ananthaswamy (author, *Why Machines Learn*) on Machine Learning Street Talk surfaces the mathematical elegance underlying ML — the proofs that make the field beautiful, not just useful [^src6]:

**Perceptron Convergence Theorem (1959)** — the first elegant ML proof. Given linearly separable data, the perceptron learning rule *provably* converges to a separating boundary in finite steps. The proof uses only linear algebra; the guarantee is mathematically exact [^src6].

**Kernel methods (the kernel trick)** — a technique for taking data in low-dimensional space and projecting it implicitly into very high (or infinite-dimensional) space to find structure that's invisible at the original dimensionality [^src6]. The elegant part: all computations happen in the *original* low-dimensional space (via the kernel function), even though the algorithm is conceptually operating in high-dimensional space. "You get the benefits of high dimensionality without paying the computational cost."

**The unsupervised insight** — Ananthaswamy argues that the most principled future of ML is unsupervised: humans learned from experience, not labeled data, and neural systems that have learned "about patterns that exist in the natural world" without labeling are the direction with the most potential [^src6]. The current supervised learning dominance is partly engineering convenience, not the most fundamental learning principle.

**The mathematical prerequisites** (per the book's pedagogical choice) [^src6]: calculus, linear algebra, and probability/statistics — not because you need every theorem, but because the *intuition from these fields* (gradients, eigenvalues, distributions) is what makes ML results interpretable rather than magical.

## The learn-ML-like-a-genius path (Tech With Tim, video)

The video companion to the "how I'd learn ML in 2026" email: same 70/30 build/theory framework, same 6–9 months timeline, same Python-first → scikit-learn → PyTorch progression [^src7]. The video adds one concrete practice: "spend more time *building* than watching" — a ratio check the email states but doesn't make visual. See [Learning AI Engineering](/ai-engineering/learning-ai-engineering.md) for the full curriculum structure.

## Theoretical generalization — VC dimension (Blum/Hopcroft/Kannan)

The **Vapnik-Chervonenkis (VC) dimension** formalizes when a hypothesis class H can generalize from finite training data. A set S is *shattered* by H if for every labeling of S there exists an h ∈ H consistent with it. VC(H) = the largest set H can shatter [^src_bhk].

**Fundamental theorem of learning**: with m ≥ O(VC(H)/ε² · log(1/δ)) samples, empirical risk minimization (ERM) achieves true error ≤ ε with probability ≥ 1-δ. The sample complexity grows linearly with VC(H). Infinite VC dimension → not PAC-learnable [^src_bhk].

Examples: linear separators in R^d have VC dimension d+1. Neural networks have finite VC dimension polynomial in the number of weights [^src_bhk].

**Online learning**: the halving algorithm — maintain a version space of consistent hypotheses; predict majority vote; on error, eliminate all inconsistent hypotheses. Makes at most log₂|H| mistakes before converging. The perceptron algorithm achieves at most (R/γ)² mistakes for R-bounded data and γ-margin classifier [^src_bhk].

**Boosting** (Adaboost): combine weak learners (each just above 50% accuracy) into a strong learner with arbitrarily low error. Each round re-weights examples: misclassified examples get higher weight. Final classifier is a weighted majority vote. Converts weak learning to strong learning in polynomial time [^src_bhk].

## See also

- [AI Fundamentals](/ai-engineering/ai-fundamentals.md) — ML is the learning branch of the broader field
- [Neural Networks](/ai-engineering/neural-network.md) — deep learning, the multi-layer extension of ML
- [Statistics & Probability for ML](/ai-engineering/statistics-for-ml.md) — the math ML rests on (distributions, regression, inference)
- [LLM](/ai-engineering/llm.md) — large-scale supervised next-token learning + RLHF
- [Learning AI Engineering](/ai-engineering/learning-ai-engineering.md) — the "learn ML in 2026" path
- [Foundations of Data Science (Blum/Hopcroft/Kannan)](/ai-engineering/sources/foundations-of-data-science-blum-hopcroft-kannan.md) — rigorous textbook source
- [AI Engineering hub](/ai-engineering/README.md)

---

[^src1]: [Harvard CS50's AI with Python (full course)](../../raw/youtube/youtube-5NgNicANyqM-harvard-cs50s-artificial-intelligence-with-python-full-unive.md) — Brian Yu
[^src2]: [Artificial Intelligence Full Course](../../raw/youtube/youtube-JMUxmLyrhSk-artificial-intelligence-full-course-artificial-intelligence.md) — Edureka
[^src3]: [ai-engineering-from-scratch](../../raw/web/github-rohitg00-ai-engineering-from-scratch-learn-it-build-i.md) — Rohit Ghumare
[^src4]: [AI Product Management Complete Course](../../raw/youtube/youtube-KjYCEiBTHFo-ai-product-management-complete-course-3-5-hours-masterclass.md) — [15:32](../../raw/youtube/youtube-KjYCEiBTHFo-ai-product-management-complete-course-3-5-hours-masterclass.md#t=15:32)
[^src5]: [AI was HARD until I Learned these 10 Concepts](../../raw/youtube/youtube-5DtjQrROUzY-ai-was-hard-until-i-learned-these-10-concepts.md) — Maddy Zhang, [06:31](../../raw/youtube/youtube-5DtjQrROUzY-ai-was-hard-until-i-learned-these-10-concepts.md#t=6:31)
[^src6]: [The Elegant Math Behind Machine Learning (MLST interview — Anil Ananthaswamy, Why Machines Learn)](../../raw/youtube/youtube-URtF_UHYBSo-the-elegant-math-behind-machine-learning.md)
[^src7]: [How to Learn Machine Learning Like a Genius (Tech With Tim)](../../raw/youtube/youtube-_hdUddANh_o-how-to-learn-machine-learning-like-a-genius-and-not-waste-ti.md)
[^src_bhk]: [Foundations of Data Science (Blum, Hopcroft, Kannan 2018) — Chapter 5](../../raw/pdf/pdf-foundations-of-data-science-part-01.md)

---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-foundations-of-data-science-part-01.md
    channel: pdf
    ingested_at: 2026-07-14
  - path: raw/_inbox/pdf-foundations-of-data-science-part-02.md
    channel: pdf
    ingested_at: 2026-07-14
  - path: raw/_inbox/pdf-foundations-of-data-science-part-03.md
    channel: pdf
    ingested_at: 2026-07-14
  - path: raw/_inbox/pdf-foundations-of-data-science-part-04.md
    channel: pdf
    ingested_at: 2026-07-14
  - path: raw/_inbox/pdf-foundations-of-data-science-part-05.md
    channel: pdf
    ingested_at: 2026-07-14
  - path: raw/_inbox/pdf-foundations-of-data-science-part-06.md
    channel: pdf
    ingested_at: 2026-07-14
  - path: raw/_inbox/pdf-foundations-of-data-science-part-07.md
    channel: pdf
    ingested_at: 2026-07-14
  - path: raw/_inbox/pdf-foundations-of-data-science-part-08.md
    channel: pdf
    ingested_at: 2026-07-14
  - path: raw/_inbox/pdf-foundations-of-data-science-part-09.md
    channel: pdf
    ingested_at: 2026-07-14
  - path: raw/_inbox/pdf-foundations-of-data-science-part-10.md
    channel: pdf
    ingested_at: 2026-07-14
  - path: raw/_inbox/pdf-foundations-of-data-science-part-11.md
    channel: pdf
    ingested_at: 2026-07-14
  - path: raw/_inbox/pdf-foundations-of-data-science-part-12.md
    channel: pdf
    ingested_at: 2026-07-14
  - path: raw/_inbox/pdf-foundations-of-data-science-part-13.md
    channel: pdf
    ingested_at: 2026-07-14
  - path: raw/_inbox/pdf-foundations-of-data-science-part-14.md
    channel: pdf
    ingested_at: 2026-07-14
  - path: raw/_inbox/pdf-foundations-of-data-science-part-15.md
    channel: pdf
    ingested_at: 2026-07-14
  - path: raw/_inbox/pdf-foundations-of-data-science-part-16.md
    channel: pdf
    ingested_at: 2026-07-14
  - path: raw/_inbox/pdf-foundations-of-data-science-part-17.md
    channel: pdf
    ingested_at: 2026-07-14
  - path: raw/_inbox/pdf-foundations-of-data-science-part-18.md
    channel: pdf
    ingested_at: 2026-07-14
  - path: raw/_inbox/pdf-foundations-of-data-science-part-19.md
    channel: pdf
    ingested_at: 2026-07-14
  - path: raw/_inbox/pdf-foundations-of-data-science-part-20.md
    channel: pdf
    ingested_at: 2026-07-14
  - path: raw/_inbox/pdf-foundations-of-data-science-part-21.md
    channel: pdf
    ingested_at: 2026-07-14
  - path: raw/_inbox/pdf-foundations-of-data-science-part-22.md
    channel: pdf
    ingested_at: 2026-07-14
  - path: raw/_inbox/pdf-foundations-of-data-science-part-23.md
    channel: pdf
    ingested_at: 2026-07-14
  - path: raw/_inbox/pdf-foundations-of-data-science-part-24.md
    channel: pdf
    ingested_at: 2026-07-14
  - path: raw/_inbox/pdf-foundations-of-data-science-part-25.md
    channel: pdf
    ingested_at: 2026-07-14
  - path: raw/_inbox/pdf-foundations-of-data-science-part-26.md
    channel: pdf
    ingested_at: 2026-07-14
aliases:
  - Foundations of Data Science
  - Blum Hopcroft Kannan
  - BHK textbook
tags:
  - corpus/ai-engineering
  - source
created: 2026-07-14
updated: 2026-07-14
---

# Foundations of Data Science (Blum, Hopcroft, Kannan, 2018)

**TL;DR**: Rigorous graduate-level textbook (479 pages, 26 parts) covering the mathematical theory expected to underlie data science for the next 40 years. Authors: Avrim Blum (CMU), John Hopcroft (Cornell), Ravindran Kannan (MSR). Free web version; Cambridge University Press print.

## Chapter coverage

| Ch | Title | Key topics |
|---|---|---|
| 1 | Introduction | Motivation: shift from classical CS theory to large-data applications |
| 2 | High-Dimensional Space | Law of Large Numbers; high-dim geometry; unit ball volume; Johnson-Lindenstrauss lemma; Gaussian separation |
| 3 | SVD | Singular vectors; best rank-k approximation; PCA; power method; clustering Gaussian mixtures; ranking via SVD |
| 4 | Random Walks & Markov Chains | Stationary distribution; MCMC (Metropolis-Hastings, Gibbs); conductance; convergence; electrical networks; PageRank |
| 5 | Machine Learning | Perceptron; kernel functions; VC dimension; Occam's Razor; regularization; boosting; SGD; deep learning; GANs; semi-supervised/active learning |
| 6 | Streaming & Sketching | Frequency moments; distinct-element estimation; AMS sketch; matrix sketching; min-hash for document similarity |
| 7 | Clustering | k-means (Lloyd's algorithm); k-center; spectral clustering; Laplacians; approximation stability |
| 8 | Random Graphs | Erdős-Rényi G(n,p) model; phase transitions; giant component; CNF-SAT threshold; preferential attachment (power-law) |
| 9 | Topic Models & Graphical Models | NMF; LDA; HMM; Bayesian networks; Markov random fields; factor graphs; belief propagation |
| 10 | Other Topics | Compressed sensing; linear programming (ellipsoid); SDP; ranking/social choice |
| 11 | Wavelets | Haar wavelet; dilation equations; orthogonal wavelets |
| 12 | Appendix | Probability; tail bounds (Chernoff); eigenvalues/eigenvectors; SVD-eigen relationship; generating functions |

## Notable content

**Johnson-Lindenstrauss lemma**: a random projection from R^d to O(log n / ε²) dimensions preserves all pairwise distances within factor (1±ε) with high probability. Enables dimensionality reduction for nearest-neighbor problems without knowing the data in advance [^src1].

**VC dimension / Vapnik-Chervonenkis dimension**: measures hypothesis class complexity. A class H shatters a set S if for every labeling of S there exists an h ∈ H consistent with it. VC(H) = largest set H can shatter. The fundamental theorem of learning: with m ≥ O(VC(H)/ε² log 1/δ) examples, ERM (empirical risk minimization) achieves ε-error with probability 1-δ [^src1].

**Maximum Likelihood Estimator (MLE)**: given samples x₁,…,xn from unknown distribution f, the MLE is the f that maximizes the joint probability density. Connects statistical learning to information theory [^src1].

**Random graph phase transition**: in G(n, p=c/n), a giant component of size Θ(n) emerges when c > 1 and collapses to O(log n) when c < 1. The transition is sharp. Analogous phase transitions exist for k-SAT satisfiability [^src1].

**Spectral clustering**: project data onto the top-k eigenvectors of the graph Laplacian, then apply k-means. Effective when clusters are non-convex or separated by thin bridges. The normalized conductance of a graph controls how fast random walks mix [^src1].

## Relation to corpus pages

- [Machine Learning](/ai-engineering/machine-learning.md) — Ch 5 (perceptron, VC dimension, boosting, SGD, deep learning) extends coverage
- [Singular Value Decomposition](/ai-engineering/singular-value-decomposition.md) — Ch 3 gives rigorous mathematical treatment of SVD and best rank-k approximation
- [PCA and Dimensionality Reduction](/ai-engineering/pca-and-dimensionality-reduction.md) — Ch 2-3 (Johnson-Lindenstrauss, random projection, PCA via SVD)
- [Clustering Methods](/ai-engineering/clustering-methods.md) — Ch 7 (spectral clustering, k-means, approximation stability)
- [Reinforcement Learning](/ai-engineering/reinforcement-learning.md) — Ch 5.13 (SGD), Ch 5 (online learning)

---

[^src1]: [Foundations of Data Science — Part 1 (TOC, Introduction)](../../../raw/pdf/pdf-foundations-of-data-science-part-01.md)

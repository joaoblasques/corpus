---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-a-brief-introduction-to-machine-learning-for-engin-part-01.md
    channel: pdf
    ingested_at: 2026-07-15
  - path: raw/_inbox/pdf-a-brief-introduction-to-machine-learning-for-engin-part-02.md
    channel: pdf
    ingested_at: 2026-07-15
  - path: raw/_inbox/pdf-a-brief-introduction-to-machine-learning-for-engin-part-03.md
    channel: pdf
    ingested_at: 2026-07-15
  - path: raw/_inbox/pdf-a-brief-introduction-to-machine-learning-for-engin-part-04.md
    channel: pdf
    ingested_at: 2026-07-15
  - path: raw/_inbox/pdf-a-brief-introduction-to-machine-learning-for-engin-part-05.md
    channel: pdf
    ingested_at: 2026-07-15
  - path: raw/_inbox/pdf-a-brief-introduction-to-machine-learning-for-engin-part-06.md
    channel: pdf
    ingested_at: 2026-07-15
  - path: raw/_inbox/pdf-a-brief-introduction-to-machine-learning-for-engin-part-07.md
    channel: pdf
    ingested_at: 2026-07-15
  - path: raw/_inbox/pdf-a-brief-introduction-to-machine-learning-for-engin-part-08.md
    channel: pdf
    ingested_at: 2026-07-15
  - path: raw/_inbox/pdf-a-brief-introduction-to-machine-learning-for-engin-part-09.md
    channel: pdf
    ingested_at: 2026-07-15
aliases:
  - Simeone ML textbook
  - A Brief Introduction to Machine Learning for Engineers
  - Simeone 2018
tags:
  - corpus/ai-engineering
  - source
created: 2026-07-15
updated: 2026-07-15
---

# A Brief Introduction to Machine Learning for Engineers (Simeone, 2018)

**TL;DR**: A compact (237pp), mathematically rigorous monograph by Osvaldo Simeone (King's College London) unifying supervised learning, unsupervised learning, probabilistic graphical models, and approximate inference under a single probabilistic framework. Targeted at engineers with probability and linear algebra backgrounds. The central thread: every ML algorithm is an inference procedure over a probabilistic model, distinguished primarily by whether inference is frequentist (MLE/MAP) or Bayesian, and whether the model is discriminative or generative [^p1].

## Scope and structure

| Part | Topic | Key content |
|---|---|---|
| I | Basics | Linear regression as running example; frequentist vs. Bayesian frameworks; exponential family; GLMs |
| II | Supervised Learning | Classification taxonomy; SGD; SVM; logistic regression; neural networks; PAC learnability; VC dimension |
| III | Unsupervised Learning | K-means; ELBO; EM algorithm; Gaussian mixtures; PPCA; GANs; RBMs; autoencoders |
| IV | Advanced Modelling | Bayesian networks; Markov random fields; belief propagation; variational inference; MCMC |
| V | Conclusions | Open research directions: privacy, robustness, transfer learning, domain adaptation |
| Appendices | Math foundations | Shannon entropy; mutual information; f-divergences; KL divergence; exponential family connections |

## Part I: Learning frameworks

### The core problem
ML is defined as the task of learning a predictive distribution p(t|x) (discriminative) or a joint distribution p(x,t) (generative) from a finite training set D = {(xᵢ, tᵢ)} [^p1]. Generalization to unseen inputs — not memorization — is the goal [^p1].

### Frequentist learning
**Maximum Likelihood Estimation (MLE)** — choose parameters θ that maximize log p(D|θ). Equivalent to **Empirical Risk Minimization (ERM)**: minimize the average loss on training data [^p2].

**MAP (Maximum A Posteriori)** — add a prior p(θ); maximize log p(θ|D) = log p(D|θ) + log p(θ). A Gaussian prior on weights induces **ridge regression** (L2 regularization); a Laplace prior induces **LASSO** (L1 / sparse solutions) [^p2].

**Bias-estimation error decomposition** — total expected loss = irreducible noise + bias² + variance. Underfitting (high bias) → increase model order; overfitting (high variance) → regularize or gather more data. Optimal model order is found via **cross-validation** [^p2].

### Bayesian learning
Instead of a point estimate, maintain the full **posterior** p(θ|D) ∝ p(D|θ) p(θ) and integrate over it for predictions. The **posterior predictive distribution** p(t*|x*, D) = ∫ p(t*|x*, θ) p(θ|D) dθ accounts for parameter uncertainty — automatically more conservative when data is scarce [^p2].

### Minimum Description Length (MDL)
Occam's Razor formalized: the best model is the one that produces the shortest description of the data. MDL recovers MLE as a special case and provides a compression-theoretic grounding for model selection [^p2].

### Information-theoretic grounding
MLE minimizes **KL divergence** KL(p_data ‖ p_model), which equals minimizing **cross-entropy** H(p_data, p_model). KL is asymmetric: the I-projection (KL(q‖p) minimization) forces q to cover all modes of p; the M-projection (KL(p‖q) minimization) allows mode-seeking [^p2][^p8].

## Part I continued: Exponential family and GLMs

The **exponential family** unifies Gaussian, Bernoulli, Categorical, Poisson, Gamma and other common distributions under the form p(x|η) = h(x) exp(η⊤φ(x) − A(η)), where η are natural parameters, φ(x) sufficient statistics, and A(η) the log-partition function [^p3].

Key properties: (1) MLE via **moment matching** — set E[φ(x)] = empirical mean of sufficient statistics; (2) conjugate priors exist in closed form; (3) the log-partition A(η) is convex, making optimization tractable; (4) entropy is maximized subject to fixed sufficient-statistic constraints (maximum entropy property) [^p3].

**Generalized Linear Models (GLMs)** extend linear regression to the exponential family: the conditional mean E[t|x] = g⁻¹(wᵀx) where g is the canonical link function. Logistic regression (Bernoulli + sigmoid) and Poisson regression are instances [^p3].

## Part II: Supervised Learning — Classification

### Taxonomy
Three model classes for classification [^p4]:

| Class | What it learns | Examples |
|---|---|---|
| Discriminative deterministic | Decision boundary f(x) = sign(wᵀx + b) | Linear classifier, perceptron, SVM |
| Discriminative probabilistic | Posterior p(t=1|x) | Logistic regression, GLMs, neural networks |
| Generative probabilistic | Joint p(x,t) | Naive Bayes, QDA, LDA, VAE |

### Stochastic Gradient Descent (SGD)
Update parameters using gradients estimated on mini-batches or single examples: θ ← θ − α ∇L(θ; xᵢ, tᵢ). Convergence properties depend on step-size schedule; SGD generalizes better than full-batch GD because mini-batch noise acts as implicit regularization [^p4].

### Support Vector Machines (SVM)
Find the maximum-margin hyperplane: maximize the geometric margin γ = 2/‖w‖ subject to correct classification. The dual formulation via Lagrange multipliers reveals that only **support vectors** (points on the margin boundary) determine the solution — sparse in training data [^p4][^p5]. The **kernel trick** extends SVMs to nonlinear boundaries via k(x,x') = φ(x)·φ(x') without computing φ explicitly [^p5].

### Neural networks and backpropagation
Multi-layer networks: output = fₗ ∘ ... ∘ f₁(x) where each layer fₖ(h) = σ(Wₖh + bₖ). Training minimizes cross-entropy via **backpropagation** — efficient application of the chain rule to compute gradients of all weights simultaneously [^p4]. GLMs are single-layer special cases; deep networks gain representational capacity by composing nonlinearities [^p4].

## Part II: Statistical Learning Theory

### PAC learnability
A hypothesis class H is **PAC-learnable** if an algorithm can output h with error ≤ ε with probability ≥ 1-δ using a polynomial number of samples. Sample complexity bound for finite H: m ≥ (1/ε)(ln|H| + ln(1/δ)) examples suffice for ERM to achieve error ≤ ε + ε_opt [^p5].

### VC dimension
**Vapnik-Chervonenkis (VC) dimension** measures a hypothesis class's capacity: VC(H) = the largest set S that H can shatter (classify in all 2^|S| possible ways) [^p5]. 

**Fundamental theorem of PAC learning**: H is PAC-learnable iff VC(H) < ∞. Sample complexity: m = O(VC(H)/ε² · log(1/δ)). VC(linear classifiers in Rᵈ) = d+1. Neural networks have finite VC dimension polynomial in the number of weights [^p5].

**Structural Risk Minimization (SRM)**: partition H into a nested sequence H₁ ⊂ H₂ ⊂ ... by complexity. Penalize training error by a complexity term that shrinks with more data — the principled bridge between model selection and generalization theory [^p5].

## Part III: Unsupervised Learning

### ELBO and the EM Algorithm
For models with latent variables z, direct ML maximization is intractable. Introduce a variational distribution q(z|x) and derive:

log p(x|θ) = ELBO(q, θ) + KL(q(z|x) ‖ p(z|x, θ))

where ELBO = E_q[log p(x,z|θ)] − E_q[log q(z|x)]. Since KL ≥ 0, ELBO is a lower bound on log-likelihood [^p6].

**EM algorithm**: iterate E-step (set q = p(z|x, θ_old), maximizing KL → 0) and M-step (maximize ELBO over θ). Converges to a local maximum of log p(x|θ). K-means is a hard-assignment limit of EM on Gaussian mixtures [^p6].

### Directed generative models
- **Mixture of Gaussians (MoG)**: latent cluster assignment c ~ Categorical(π); x|c ~ N(μ_c, Σ_c). EM gives soft cluster assignments [^p6].
- **Probabilistic PCA (PPCA)**: continuous latent z ~ N(0,I); x|z ~ N(Wz + μ, σ²I). ML solution recovers principal components [^p6].
- **GANs**: replace the ML divergence with an adversarially learned divergence. Generator G maps noise z → x; discriminator D learns to distinguish real from fake. Minimax game: min_G max_D E[log D(x)] + E[log(1-D(G(z)))]. Generalizes ML in that the divergence measure is learned, not fixed [^p6].

### Undirected models and autoencoders
**Restricted Boltzmann Machines (RBMs)**: undirected bipartite graph between visible v and hidden h. Energy-based model; learning via contrastive divergence [^p7].

**Autoencoders**: encoder q_φ(z|x) → latent code → decoder p_θ(x|z). Vanilla autoencoders recover PCA with linear encoder/decoder. **Variational Autoencoders (VAEs)** train by maximizing the ELBO: the encoder outputs q_φ(z|x) = N(μ(x), σ²(x)); the **reparametrization trick** z = μ + σ·ε (ε ~ N(0,I)) enables backpropagation through the sampling step [^p7][^p8].

## Part IV: Probabilistic Graphical Models

### Bayesian Networks
Directed Acyclic Graphs (DAGs) where each node is conditionally independent of its non-descendants given its parents: p(x₁,...,xₙ) = ∏ p(xᵢ | pa(xᵢ)) [^p7]. Encode causal structure. **d-separation** is the graphical criterion for conditional independence [^p7]. Instances: Naive Bayes (all features independent given class), Hidden Markov Models (first-order Markov chain with emissions) [^p7].

### Markov Random Fields (MRFs)
Undirected graphs where the joint distribution factorizes over cliques: p(x) = (1/Z) ∏_C ψ_C(x_C). The **Ising model** is a binary MRF on a grid [^p8]. Converting BNs to MRFs requires **moralization** (marrying co-parents), which can introduce new dependencies [^p8].

### Belief propagation and junction tree
Exact inference in tree-structured graphical models via message passing. For general graphs, run belief propagation on the **junction tree** (a triangulated clique tree) — exact inference in O(n · exp(treewidth)) time [^p8].

## Part IV: Approximate Inference

### Monte Carlo methods
**Importance sampling**: estimate E_p[f(x)] by sampling from proposal q: Ê = (1/N) Σ f(xᵢ) p(xᵢ)/q(xᵢ). Variance explodes when p and q differ significantly [^p8].

**MCMC / Gibbs sampling**: construct a Markov chain whose stationary distribution is p(x). Gibbs samples each variable from its conditional given all others. Asymptotically exact but slow mixing [^p8].

### Variational Inference (VI)
Approximate the posterior p(z|x) with a tractable family q(z; λ) by minimizing KL(q‖p). Equivalent to maximizing the ELBO over λ [^p8].

**Mean-field VI**: assume q(z) = ∏ᵢ qᵢ(zᵢ) (fully factored). Optimal factors satisfy log qᵢ*(zᵢ) = E_{j≠i}[log p(x,z)] + const. Iterative coordinate ascent converges to a local optimum [^p8].

**Monte Carlo VI**: use SGD on the ELBO with gradient estimators:
- **REINFORCE** (score function estimator): ∇_λ E_q[f(z)] = E_q[f(z) ∇_λ log q(z|λ)] — high variance.
- **Reparametrization trick**: z = g(ε, λ) with ε ~ p(ε); ∇_λ E[f(g(ε,λ))] = E[∇_λ f(g(ε,λ))] — low variance, applicable when z is continuous [^p8].

**Amortized VI**: train an inference network (encoder) to predict variational parameters from x, enabling fast posterior approximation at test time — the basis of VAEs [^p8].

## Appendices: Information theory foundations

**Shannon entropy** H(X) = -Σ p(x) log p(x) is uniquely characterized (up to scaling) by three axioms: continuity, symmetry, and the chain rule H(X,Y) = H(X) + H(Y|X) [^p9].

**Mutual information** I(X;Y) = KL(p(x,y) ‖ p(x)p(y)) — measures dependence; equals the reduction in uncertainty about X given Y. I(X;Y) = 0 iff X ⊥ Y [^p9].

**f-divergences**: a family generalizing KL. D_f(p‖q) = E_q[f(p(x)/q(x))]. KL divergence is f(t) = t log t; Jensen-Shannon divergence (used in GANs) is a symmetrized, bounded variant; Hellinger distance and chi-squared divergence are also instances [^p9]. All f-divergences have a variational representation via binary hypothesis testing (Neyman-Pearson) [^p9].

**Bregman divergences** generalize KL to non-probabilistic settings (e.g., squared Euclidean distance is a Bregman divergence). The exponential family is in bijection with Bregman divergences via the log-partition function [^p9].

## Pedagogical choices

- Linear regression is the running example through all of Part I, allowing side-by-side comparison of frequentist and Bayesian methods on a single problem.
- The text is notation-heavy but self-contained; prerequisites are probability theory and linear algebra only.
- Reinforcement learning is intentionally excluded (discussed as open direction in Ch. 9).
- Chapter 9 (Concluding Remarks) briefly surveys privacy/robustness/transfer learning as directions the book does not cover, situating itself as a foundations text rather than a complete survey.

## See also

- [Machine Learning](/ai-engineering/machine-learning.md) — primary concept page updated with Simeone content
- [Neural Networks](/ai-engineering/neural-network.md) — backpropagation and architecture detail
- [Generative Adversarial Networks](/ai-engineering/generative-adversarial-networks.md) — GAN deep-dive
- [Support Vector Machines](/ai-engineering/support-vector-machines.md) — SVM deep-dive
- [Gaussian Mixture Models](/ai-engineering/gaussian-mixture-models.md) — EM algorithm detail
- [Probability and Statistics for ML](/ai-engineering/probability-and-statistics-for-ml.md) — exponential family
- [Foundations of Data Science (Blum/Hopcroft/Kannan)](/ai-engineering/sources/foundations-of-data-science-blum-hopcroft-kannan.md) — complementary rigorous textbook source

---

[^p1]: [ML for Engineers — Part 1/9 (Intro + Part I overview)](../../../raw/pdf/pdf-a-brief-introduction-to-machine-learning-for-engin-part-01.md)
[^p2]: [ML for Engineers — Part 2/9 (Ch. 2.3–2.7: MAP, Bayesian, MDL, KL)](../../../raw/pdf/pdf-a-brief-introduction-to-machine-learning-for-engin-part-02.md)
[^p3]: [ML for Engineers — Part 3/9 (Ch. 3: Exponential family, GLMs)](../../../raw/pdf/pdf-a-brief-introduction-to-machine-learning-for-engin-part-03.md)
[^p4]: [ML for Engineers — Part 4/9 (Ch. 4 Part I: SGD, SVM, logistic regression, backprop)](../../../raw/pdf/pdf-a-brief-introduction-to-machine-learning-for-engin-part-04.md)
[^p5]: [ML for Engineers — Part 5/9 (Ch. 4 Part II + Ch. 5: generative models, boosting, PAC, VC)](../../../raw/pdf/pdf-a-brief-introduction-to-machine-learning-for-engin-part-05.md)
[^p6]: [ML for Engineers — Part 6/9 (Ch. 6: ELBO, EM, MoG, PPCA, GANs)](../../../raw/pdf/pdf-a-brief-introduction-to-machine-learning-for-engin-part-06.md)
[^p7]: [ML for Engineers — Part 7/9 (Ch. 6 cont. + Ch. 7: RBMs, autoencoders, BNs, MRFs)](../../../raw/pdf/pdf-a-brief-introduction-to-machine-learning-for-engin-part-07.md)
[^p8]: [ML for Engineers — Part 8/9 (Ch. 7–8: MRFs, belief propagation, VI, MCMC, reparametrization)](../../../raw/pdf/pdf-a-brief-introduction-to-machine-learning-for-engin-part-08.md)
[^p9]: [ML for Engineers — Part 9/9 (Appendices: entropy, mutual information, f-divergences)](../../../raw/pdf/pdf-a-brief-introduction-to-machine-learning-for-engin-part-09.md)

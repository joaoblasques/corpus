---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-the-little-book-of-deep-learning-part-01.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/_inbox/pdf-the-little-book-of-deep-learning-part-02.md
    channel: pdf
    ingested_at: 2026-08-03
aliases:
  - deep learning
  - DL
  - neural network training
  - tensors
  - GPU computation
  - backpropagation
  - gradient descent
  - batch normalization
  - skip connections
  - residual connections
  - dropout
  - activation functions
  - ReLU
  - GELU
tags:
  - corpus/ai-engineering
  - concept
created: 2026-08-03
updated: 2026-08-03
---

# Deep Learning

**TL;DR.** Deep learning is the practice of training long compositions of parameterized mappings (layers) end-to-end via gradient descent on loss functions, executed on parallel hardware (GPUs/TPUs) using tensor abstractions. The "deep" in deep learning refers to the number of sequential transformations — empirically, more depth yields better performance for the same parameter budget [Telgarsky, 2016]. This page covers the cross-cutting mechanics: hardware, tensors, training, and model components (see [MLP](/ai-engineering/mlp.md), [CNNs](/ai-engineering/convolutional-neural-networks.md), [Transformer](/ai-engineering/transformer.md), [Attention Mechanisms](/ai-engineering/attention-mechanisms.md) for architecture details).[^p1]

---

## Hardware: GPUs, TPUs, and computation organization

GPUs were designed for real-time image synthesis, which requires massively parallel computation — the same structure that makes them ideal for deep learning. Modern GPUs include dedicated **tensor cores**; Google's **TPUs** are designed specifically for deep learning.[^p1]

**Bottleneck**: Not the number of compute units, but **memory read/write speed**. The slowest link is CPU↔GPU memory; computation is organized to avoid redundant copies. Multiple cache levels exist within a GPU; optimal designs minimize cross-cache traffic.[^p1]

**Batch processing**: A batch of samples is processed in parallel. For batches small enough to fit in GPU memory, cost is roughly constant — processing 64 samples takes similar time as processing 1. This is the practical justification for mini-batch SGD.[^p1]

**Peak performance**: A standard GPU achieves 10¹³–10¹⁴ FLOPs/second with 8–80 GB memory. FP32 is 32 bits; FP16 (and lower) achieves similar empirical accuracy.[^p1]

---

## Tensors

A **tensor** is a multi-dimensional array — elements of R^(N₁×···×N_D) — generalizing vectors and matrices. Deep learning frameworks (PyTorch, JAX) represent all data as tensors: input signals, trainable parameters (weights), and intermediate results (activations).[^p1]

**Encoding conventions**:
- 1D time series: T×D (duration × features) or D×T (channels × time, for historical reasons)
- 2D images: D×H×W (channels × height × width); RGB → D=3; large models → D up to thousands
- Batches add one more dimension: 50 RGB 32×24 images → 50×3×24×32 tensor[^p1]

**Key advantage**: Separating shape representation from memory storage layout allows reshape, transpose, and extraction operations without coefficient copying — extremely fast. All computation decomposes into elementary tensor operations, avoiding non-parallel language-level loops.[^p1]

---

## Training mechanics

### Loss functions

Three standard patterns:[^p1]
- **Regression**: Mean squared error (MSE) between predicted continuous output and ground truth.
- **Classification**: Cross-entropy loss — model outputs a logit per class, softmax converts to probabilities, loss is −log P(true class).
- **Density modeling**: Negative log-likelihood; for autoregressive models, sum of per-token cross-entropy.

**Weight decay**: Adding λ‖w‖² to the loss (L2 regularization) is equivalent to a Gaussian prior on weights. It degrades training performance slightly but reduces the gap to test performance.[^p1]

**Contrastive loss**: Used for metric learning where supervision is in the form of ranking constraints (e.g., CLIP). For a triplet (xₐ, x_b, x_c) where xₐ, x_b are same-class and x_c different-class: max(0, 1 − f(xₐ, x_c; w) + f(xₐ, x_b; w)).[^p1]

### Autoregressive models

Chain rule: P(X₁,...,X_T) = ∏ P(X_t | X₁,...,X_{t-1}). With tokens from a finite vocabulary, a model f predicts the logits for X_t given previous tokens. A **causal** model computes all output logits in a single forward pass (the output at position t depends only on inputs 1,...,t−1). Training minimizes the sum of per-token cross-entropy. The **perplexity** = exp(cross-entropy) is the standard monitoring metric.[^p1]

**Tokenizer**: Converts raw text to integer tokens. Standard: **Byte Pair Encoding (BPE)** — hierarchically merges character groups to create tokens of similar frequencies, allocating short tokens to rare symbols and long tokens to frequent fragments.[^p1]

### Gradient descent

Starting from random w₀, iterate: w_{n+1} = w_n − η ∇ℒ|_{w_n}. The learning rate η controls step size — too small: slow/trapped; too large: diverges from narrow minima.[^p1]

**Mini-batch SGD**: Splitting data into batches of size B and computing gradients over each batch (rather than the full dataset) is far more efficient under data redundancy. Each batch is an unbiased estimator of the full gradient. In practice, millions of gradient steps are needed.[^p1]

**Adam** [Kingma & Ba, 2014]: Maintains running estimates of per-component gradient mean and variance, normalizing them to avoid scaling issues. Standard optimizer for most deep models.[^p1]

### Backpropagation

For a model f = f^(D) ∘ ··· ∘ f^(1), the **forward pass** computes activations x^(d) sequentially. The **backward pass** computes gradients ∇ℓ|_{x^(d)} recursively using the chain rule (each step multiplies by the Jacobian of f^(d+1)). The gradient of the loss w.r.t. layer parameters ∇ℓ|_{w_d} is a product of the activation gradient with the Jacobian w.r.t. w_d.[^p1]

**Autograd** [Baydin et al., 2015]: Modern frameworks track tensor operations and automatically construct backward operators, enabling gradient computation through arbitrary imperative code.[^p1]

**Resource cost**: Backward pass is roughly 2× the forward pass cost (two Jacobian products vs. one forward product). Memory during training must store all forward-pass activations for Jacobian computation — grows proportional to model depth. Mitigation: gradient checkpointing (recompute some activations during backward, trade compute for memory) or reversible layers.[^p1]

### Vanishing gradient

When gradients traverse many layers, multiplicative Jacobians can shrink exponentially — **vanishing gradient** — or grow exponentially (**exploding gradient**). Solutions:
- **Gradient norm clipping** [Pascanu et al., 2013]: if ‖∇‖ > threshold, rescale to threshold.
- **Careful initialization**: scale random parameters by input dimension to keep activation variance constant [Glorot & Bengio, 2010].
- **Architectural**: ReLU activation, skip connections, normalization layers (see below).[^p1][^p2]

---

## Model components

### Activation functions

Non-linearity is essential — without it, deep models collapse to a single linear operator.[^p2]

- **ReLU** [Glorot et al., 2011]: max(0, x). Standard default. Not differentiable at 0, but gradient is informative on average with proper initialization.
- **Tanh**: saturates exponentially on both sides, aggravates vanishing gradient. Pre-ReLU standard.
- **Leaky ReLU** [Maas et al., 2013]: applies small positive multiplier α to negative inputs. Prevents "dead neuron" problem.
- **GELU** [Hendrycks & Gimpel, 2016]: x · Φ(x) where Φ is the standard normal CDF. Smooth ReLU approximation; used in Transformers (BERT, GPT).[^p2]

### Pooling

**Max pooling**: For each non-overlapping spatial window of size K, retain the maximum activation per channel. Output spatial size = input size / K. Hyperparameters: kernel size, padding, stride, dilation.[^p2]

Max pooling implements a logical disjunction: if convolutional layers compute local presence scores, max pooling encodes "at least one instance present," losing precise location (local translation **invariance**).[^p2]

**Average pooling**: Linear alternative to max pooling; averages over the window instead of taking the max.[^p2]

### Dropout [Srivastava et al., 2014]

A training-time regularizer with no trainable parameters. Hyperparameter p: probability of zeroing each activation. Surviving activations are rescaled by 1/(1−p) to maintain expected values. Inactive at test time.[^p2]

**Rationale**: Prevents the model from relying on groups of co-adapted neurons — joint representations become unreliable when any activation in the group might be zeroed. Equivalent to noisy training.[^p2]

**2D dropout**: For image tensors, individual pixel activations are redundant with neighbors (correlation). 2D dropout zeros entire channels rather than individual values.[^p2]

**Monte Carlo dropout** [Gal & Ghahramani, 2015]: Keeping dropout active at inference time provides empirical confidence estimates via sampling.[^p2]

### Normalizing layers

Forces empirical mean and variance of groups of activations, stabilizing training by preventing early-layer scaling changes from cascading through the network.[^p2]

**Batch normalization** [Ioffe & Szegedy, 2015]:
- Processes a batch of B samples; computes mean m̂_d and variance v̂_d across the batch for each feature dimension d.
- Normalizes to zero mean, unit variance, then scales/shifts with learnable parameters β_d, γ_d.
- For 2D image tensors: normalizes across batch × spatial positions (B×H×W slice), one set of β,γ per channel.
- During inference: uses running averages of m̂, v̂ from training (fixed affine transform per component).[^p2]

**Layer normalization** [Ba et al., 2016]:
- Normalizes across all feature dimensions of a single sample (not across the batch).
- Same behavior during training and inference (no batch dependency).
- Preferred for Transformers and sequence models.[^p2]

### Skip connections [Long et al., 2014; Ronneberger et al., 2015]

Transport signal unchanged across multiple layers, bypassing intermediate processing. Mitigates vanishing gradient: even if some stage kills gradients, the gradient still propagates via the skip path.[^p2]

**Residual connections** [He et al., 2015]: A specific form that sums the original signal with the transformed signal (not concatenates). Usually skips 2–3 layers. Allows models with hundreds of layers. Key insight: the model only needs to learn a differential improvement (residual) rather than a full transformation.[^p2]

**U-Net skip connections**: Connects encoder layers to decoder layers at the same spatial resolution, used in semantic segmentation to preserve fine-grained spatial information through the bottleneck.[^p2]

---

## The value of depth

Empirical evidence over 20 years: state-of-the-art across domains requires tens of layers. Theoretical result [Telgarsky, 2016]: for fixed parameter count, greater depth yields greater mapping complexity. A co-adaptation view: SGD causes the layer sequence to deform input space so that classification becomes linearly separable at the final layer — each layer contributes a progressive geometric warping.[^p1]

---

## See also

- [Scaling Laws](/ai-engineering/scaling-laws.md) — power-law behavior of loss with compute/data/parameters
- [MLP](/ai-engineering/mlp.md) — the foundational deep architecture
- [Convolutional Neural Networks](/ai-engineering/convolutional-neural-networks.md)
- [Attention Mechanisms](/ai-engineering/attention-mechanisms.md)
- [Transformer](/ai-engineering/transformer.md)
- [LoRA and Adapters](/ai-engineering/lora-adapters.md)
- [Quantization](/ai-engineering/quantization.md)
- [François Fleuret](/ai-engineering/francois-fleuret.md)

[^p1]: raw/_inbox/pdf-the-little-book-of-deep-learning-part-01.md
[^p2]: raw/_inbox/pdf-the-little-book-of-deep-learning-part-02.md

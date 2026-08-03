---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-zhang-lipton-li-smola-dive-into-deep-learning-cc-by-sa-4-0-part-11.md
    channel: pdf
    ingested_at: 2026-07-10
  - path: raw/_inbox/pdf-the-little-book-of-deep-learning-part-01.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/_inbox/pdf-the-little-book-of-deep-learning-part-02.md
    channel: pdf
    ingested_at: 2026-08-03
aliases:
  - multilayer perceptron
  - MLP
  - feedforward network
  - hidden layer
  - backpropagation
  - activation function
  - dropout
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-10
updated: 2026-08-03
---

# Multilayer Perceptrons (MLP)

**TL;DR**: The foundational deep learning architecture — layers of affine transformations interleaved with non-linear activation functions. The addition of hidden layers gives networks the ability to represent non-linear functions, and backpropagation (chain rule over computation graphs) enables efficient gradient computation to train them. Key failure modes in deep MLPs: vanishing and exploding gradients, addressed by initialization strategies and activation choice. See also [Neural Networks](/ai-engineering/neural-network.md) and [CNNs](/ai-engineering/convolutional-neural-networks.md).

## Hidden layers

A single-layer linear network (softmax regression) can only represent linear decision boundaries. Hidden layers break this limitation. An MLP with one hidden layer computes [^src1]:

```
z = W^(1) x          (linear transformation, hidden pre-activation)
h = phi(z)           (elementwise non-linearity — the activation function)
o = W^(2) h          (output layer)
```

Adding more hidden layers builds deeper representations. Each layer learns progressively more abstract features: in vision, early layers detect edges, middle layers detect shapes, late layers detect object parts.

**Universal Approximation Theorem** [Cybenko, 1989]: a single hidden layer with sufficient width can approximate any continuous function on a compact domain — specifically, any model of the form l₂ ∘ σ ∘ l₁ where l₁, l₂ are affine and σ is continuous and non-polynomial [^src2]. This holds when the hidden layer width is allowed to grow arbitrarily. In practice, depth (many narrower layers) outperforms width (one very wide layer) for most tasks — theoretical results show that for a fixed parameter budget, depth produces greater mapping complexity [Telgarsky, 2016] [^src2].

## Activation functions

Without non-linear activations, stacking linear layers collapses to a single linear transformation (any product of matrices is a matrix). The activation function phi breaks this [^src1].

| Activation | Formula | Properties |
|---|---|---|
| **Sigmoid** | 1/(1 + exp(-x)) | Squashes to (0,1); saturates at extremes → vanishing gradients; historically popular |
| **tanh** | (exp(x) - exp(-x))/(exp(x) + exp(-x)) | Squashes to (-1,1); zero-centered; also saturates |
| **ReLU** | max(0, x) | No saturation for positive inputs; computationally cheap; default for deep nets |
| **Leaky ReLU** | max(alpha*x, x), alpha small | Fixes "dying ReLU" (units stuck at 0) |
| **GELU** | x * Phi(x) | Smooth; used in BERT, GPT; approximated as x * sigmoid(1.702x) |
| **SwiGLU** | x * sigmoid(beta*x) * gate | Used in LLaMA, Mistral; gated variant outperforms ReLU in practice |

ReLUs have "emerged as the default choice for practitioners" for deep networks because they do not saturate in the positive regime, making gradient flow easier than sigmoid [^src1].

## Forward propagation

Forward propagation traverses the computation graph input → output, computing and storing intermediate variables [^src1]:

1. Input x
2. Hidden pre-activation: z = W^(1) x (+ optional bias)
3. Hidden activation: h = phi(z)
4. Output: o = W^(2) h
5. Loss: L = loss(o, y)
6. Regularized objective: J = L + (lambda/2)(||W^(1)||^2 + ||W^(2)||^2)

The intermediate values (z, h) are stored in memory during the forward pass because backprop needs them.

## Backpropagation

Backpropagation computes gradients of J with respect to all parameters by traversing the computation graph in reverse, applying the chain rule [^src1]:

```
dJ/dW^(2) = (dJ/do)(do/dW^(2)) = (dL/do + lambda*W^(2)) via chain
dJ/dh = W^(2)^T (dJ/do)
dJ/dz = dJ/dh ⊙ phi'(z)    (element-wise multiplication with activation derivative)
dJ/dW^(1) = (dJ/dz) x^T
```

Key insight: backprop is the chain rule applied systematically, not a separate algorithm. Modern deep learning frameworks (PyTorch autograd, JAX) implement this automatically.

**Memory cost of training**: the forward pass must retain all intermediate activations until the backward pass is complete. Training memory is proportional to depth × batch size. This is why training deep networks with large batches requires much more GPU memory than inference [^src1].

## Numerical stability: vanishing and exploding gradients

In a network of L layers, the gradient of the output with respect to early layer parameters is a product of L-l matrices [^src1]:

```
dJ/dW^(l) = M^(L) * M^(L-1) * ... * M^(l+1) * v^(l)
```

If eigenvalues of these matrices are < 1, the product shrinks exponentially → **vanishing gradient**: early layers learn very slowly or not at all. Historically, sigmoid caused this because its gradient is near 0 in the saturation regime [^src1].

If eigenvalues are > 1, the product grows exponentially → **exploding gradient**: parameter updates become huge, destabilizing training. Gradient clipping (capping ||g|| to a maximum norm) is the standard defense.

Solutions:
- **ReLU activations**: gradient is 1 for positive inputs, 0 otherwise — no saturation for positive regime
- **Xavier/Glorot initialization**: set weight variance = 2/(n_in + n_out) so variance is preserved across layers
- **He initialization**: for ReLU networks, set variance = 2/n_in
- **Batch normalization**: see [CNNs](/ai-engineering/convolutional-neural-networks.md)
- **Residual connections**: add skip paths so gradient flows directly (see ResNet in CNNs page)

## Regularization in MLPs

**Dropout** (Srivastava et al. 2014): during training, randomly zero out each hidden unit with probability p (typically 0.5). Forces the network to learn redundant representations; acts as an implicit ensemble method. At test time, scale activations by (1-p) or equivalently use the full network without dropout [^src1].

**Weight decay (L2 regularization)**: add lambda * ||w||^2 to the loss. This shrinks weights toward zero on each update ("weight decay"). Implemented directly in optimizers: `torch.optim.SGD(params, lr=0.01, weight_decay=0.01)` [^src1].

L1 regularization (lasso) promotes sparse weights; L2 distributes weight across features. L1 = feature selection; L2 = weight shrinkage.

**Early stopping**: monitor validation loss; stop when it stops decreasing. The simplest and often most effective regularizer.

## Implementation skeleton (PyTorch)

```python
import torch.nn as nn

mlp = nn.Sequential(
    nn.LazyLinear(256),   # hidden layer, 256 units
    nn.ReLU(),
    nn.Dropout(0.5),
    nn.LazyLinear(10),    # output, 10 classes
)
```

The `from-scratch` version (D2L Chapter 5) implements the forward pass and parameter initialization manually before introducing `nn.Sequential`, illustrating what the framework is doing.

## See also

- [Neural Networks](/ai-engineering/neural-network.md) — broader architecture family; perceptron origins
- [Optimization for ML](/ai-engineering/optimization-for-ml.md) — gradient descent, Adam, the update rules that train MLPs
- [CNNs](/ai-engineering/convolutional-neural-networks.md) — convolutional variant for spatial data
- [Transformer](/ai-engineering/transformer.md) — attention-based architecture; FFN layers are MLPs applied per-token
- [Dive into Deep Learning](/ai-engineering/sources/dive-into-deep-learning.md) — source textbook (Chapter 5)
- [Deep Learning](/ai-engineering/deep-learning.md) — training mechanics, activation functions, dropout, normalization
- [The Little Book of Deep Learning](/ai-engineering/sources/the-little-book-of-deep-learning.md) — Fleuret, § 5.1

---

[^src1]: [D2L Part 11 — Forward Prop, Backprop, Numerical Stability](../../raw/pdf/pdf-zhang-lipton-li-smola-dive-into-deep-learning-cc-by-sa-4-0-part-11.md)
[^src2]: raw/_inbox/pdf-the-little-book-of-deep-learning-part-01.md; raw/_inbox/pdf-the-little-book-of-deep-learning-part-02.md — Fleuret, §§ 3.5, 5.1

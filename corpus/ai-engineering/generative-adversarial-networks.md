---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-zhang-lipton-li-smola-dive-into-deep-learning-cc-by-sa-4-0-part-39.md
    channel: pdf
    ingested_at: 2026-07-11
aliases:
  - GAN
  - generative adversarial network
  - DCGAN
  - adversarial training
  - generator network
  - discriminator network
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-11
updated: 2026-07-11
---

# Generative Adversarial Networks (GANs)

**TL;DR**: GANs train two networks in opposition — a **generator** produces synthetic samples; a **discriminator** classifies samples as real or fake. Adversarial training pushes both to improve until (ideally) the generator produces samples indistinguishable from real data [^src1].

## Core architecture

The generator *G* takes a noise vector *z* (drawn from a simple prior, e.g. N(0,I)) and produces a synthetic sample *G(z)*. The discriminator *D* takes a sample and outputs the probability that it is real [^src1].

**Objective** (minimax game):
- *D* maximizes: `E[log D(x)] + E[log(1 - D(G(z)))]`
- *G* minimizes the same (equivalently, maximizes `E[log D(G(z))]` to avoid gradient saturation early in training)

In the original Goodfellow formulation (2014), Nash equilibrium is reached when *G* perfectly models the data distribution and *D* outputs 0.5 everywhere [^src1].

## Deep Convolutional GAN (DCGAN)

DCGAN (Radford et al., 2016) applies the GAN framework to image synthesis using convolutional architectures [^src1]:

- **Generator**: stack of transposed convolutions (upsampling) + batch normalization + ReLU; final layer uses tanh
- **Discriminator**: stack of strided convolutions (downsampling) + batch normalization + LeakyReLU; final layer is sigmoid

Key design rules (from DCGAN paper): no pooling layers (replace with strided convolutions); use batch norm in both; no fully connected hidden layers; ReLU for generator, LeakyReLU for discriminator [^src1].

## Training instabilities

GANs are notoriously difficult to train. Common failure modes [^src1]:

- **Mode collapse**: generator produces only a few distinct outputs (one or a few modes of the data distribution), ignoring the rest
- **Vanishing gradients**: if discriminator becomes too strong early, gradient signal to generator vanishes
- **Non-convergence**: the minimax game need not converge — oscillations are common

Mitigation approaches: Wasserstein GAN (WGAN) replaces the minimax objective with the Wasserstein distance (more stable gradients); spectral normalization constrains the discriminator's Lipschitz constant; progressive growing of GANs (ProGAN) trains at low resolution first then adds layers [^src1].

## Connections to other corpus pages

- [MLP](/ai-engineering/mlp.md) — discriminator and generator both use feedforward components; backpropagation through both networks.
- [Convolutional Neural Networks](/ai-engineering/convolutional-neural-networks.md) — DCGAN uses convolutional architectures for image synthesis.
- [Optimization for ML](/ai-engineering/optimization-for-ml.md) — training involves simultaneous gradient updates; conflicting objectives make standard SGD convergence theory inapplicable.

---

[^src1]: [D2L Part 39 — Generative Adversarial Networks](../../raw/pdf/pdf-zhang-lipton-li-smola-dive-into-deep-learning-cc-by-sa-4-0-part-39.md)

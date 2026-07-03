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
  - neural network
  - neural networks
  - deep learning
  - perceptron
  - backpropagation
  - gradient descent
  - CNN
  - RNN
  - reasoning model
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-15
updated: 2026-06-15
---

# Neural Networks

**TL;DR**: Computing structures loosely inspired by the brain — layers of weighted "neurons" that transform inputs to outputs and learn by adjusting weights to reduce error [^src1]. **Deep learning** is ML with many such layers; neural networks are the substrate of every modern LLM via the [Transformer](/ai-engineering/transformer.md) [^src2].

## From perceptron to multi-layer network

The **perceptron** is the founding unit: a weighted sum of inputs passed through an activation, producing an output [^src3]. Stacking units into layers (input → hidden → output) gives a **multi-layer network** whose **forward pass** propagates inputs to a prediction [^src3]. Activations (ReLU, sigmoid, GELU) introduce the non-linearity that lets networks model complex functions [^src3].

## How they learn: loss, backprop, gradient descent

Training drives weights to minimize a **loss function** (MSE, cross-entropy) measuring prediction error [^src3]. **Backpropagation** computes how each weight contributed to the error, and **gradient descent** (SGD, Momentum, Adam, AdamW) nudges weights down the error gradient [^src3]. Stability tooling — weight initialization, dropout, batch norm, weight decay, learning-rate schedules and warmup — keeps deep networks trainable [^src3]. The principle "build the algorithm from raw math first, then use the framework" applies: implement backprop by hand before reaching for PyTorch/JAX [^src3].

## Architectures

| Architecture | Best for |
|---|---|
| **Feedforward (MLP)** | General tabular function approximation [^src2] |
| **CNN** (convolutional) | Images / spatial data [^src2] |
| **RNN / LSTM** | Sequences (older NLP, time series) [^src2] |
| **Transformer** | Modern language/multimodal — parallel attention [^src3] |

Transformers (Phase 7 of the from-scratch curriculum: self-attention → multi-head → positional encoding → MoE → KV cache/Flash Attention) superseded RNNs for language because they process sequences in parallel and model long-range dependencies [^src3]. See [Transformer](/ai-engineering/transformer.md).

## Reasoning models: a neural-network training direction

A newer breed of LLM is trained to "think step-by-step before generating an answer" — generating an internal **chain of thought**, breaking problems down and working through logic before producing a final answer [^src4]. These are trained on problems with verifiably correct answers (math, code that compiles) via reinforcement learning, so they learn reasoning steps that lead to correct solutions [^src4]. "This is why you'll sometimes see an LLM say 'thinking' before it responds" [^src4]; reasoning models are especially important for agents, where multi-step tasks need planning, not just pattern matching [^src4]. See [LLM](/ai-engineering/llm.md).

## Multimodal networks

Models trained on multiple data types (text, image, audio, video) "develop a deeper understanding" — a model that has seen both images of cats and text about cats understands the concept more richly than a text-only model [^src4]. Multimodality is now standard in frontier models and opens accessibility, medical-imaging, and document-understanding use cases [^src4].

## See also

- [Machine Learning](/ai-engineering/machine-learning.md) — deep learning is the multi-layer extension of ML
- [Transformer](/ai-engineering/transformer.md) — the attention architecture behind LLMs
- [LLM](/ai-engineering/llm.md) — neural networks at billion-parameter scale; reasoning models
- [AI Fundamentals](/ai-engineering/ai-fundamentals.md) — where neural nets sit in the field
- [AI Engineering hub](/ai-engineering/README.md)

---

[^src1]: [Harvard CS50's AI with Python (full course)](../../raw/youtube/youtube-5NgNicANyqM-harvard-cs50s-artificial-intelligence-with-python-full-unive.md) — Brian Yu
[^src2]: [Artificial Intelligence Full Course](../../raw/youtube/youtube-JMUxmLyrhSk-artificial-intelligence-full-course-artificial-intelligence.md) — Edureka
[^src3]: [ai-engineering-from-scratch](../../raw/web/github-rohitg00-ai-engineering-from-scratch-learn-it-build-i.md) — Rohit Ghumare (Phases 3 & 7)
[^src4]: [AI was HARD until I Learned these 10 Concepts](../../raw/youtube/youtube-5DtjQrROUzY-ai-was-hard-until-i-learned-these-10-concepts.md) — Maddy Zhang, [07:48](../../raw/youtube/youtube-5DtjQrROUzY-ai-was-hard-until-i-learned-these-10-concepts.md#t=7:48)

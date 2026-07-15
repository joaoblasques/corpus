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
  - path: raw/_inbox/pdf-zhang-lipton-li-smola-dive-into-deep-learning-cc-by-sa-4-0-part-06.md
    channel: pdf
    ingested_at: 2026-07-10
  - path: raw/_inbox/pdf-the-quest-for-artificial-intelligence-a-history-of-part-05.md
    channel: pdf
    ingested_at: 2026-07-15
  - path: raw/_inbox/pdf-the-quest-for-artificial-intelligence-a-history-of-part-20.md
    channel: pdf
    ingested_at: 2026-07-15
  - path: raw/_inbox/pdf-the-quest-for-artificial-intelligence-a-history-of-part-24.md
    channel: pdf
    ingested_at: 2026-07-15
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
updated: 2026-07-15
---

# Neural Networks

**TL;DR**: Computing structures loosely inspired by the brain — layers of weighted "neurons" that transform inputs to outputs and learn by adjusting weights to reduce error [^src1]. **Deep learning** is ML with many such layers; neural networks are the substrate of every modern LLM via the [Transformer](/ai-engineering/transformer.md) [^src2].

## Historical arc: Perceptron → AI winter → backprop revival

**Perceptron (Frank Rosenblatt, 1957):** Single-layer linear classifier with weighted inputs summed and thresholded. The **Perceptron Convergence Theorem** proves it learns any linearly separable function in finite steps [^src5]. Rosenblatt's claims of general intelligence triggered a decade of neural-network enthusiasm.

**Minsky-Papert critique (1969):** *Perceptrons* (Minsky & Papert) formally proved that single-layer perceptrons cannot solve linearly inseparable problems (e.g., XOR). The book argued that scaling to multi-layer networks would face fundamental difficulties. Combined with DARPA's refocus on symbolic AI, this triggered a sharp drop in neural-network funding — the first "neural network winter" [^src5].

**Backpropagation revival (Rumelhart, Hinton, Williams, 1986):** Published in *Nature* and the *Parallel Distributed Processing* (PDP) volumes, backpropagation provided efficient gradient computation through multi-layer networks via the chain rule, enabling the training of hidden-layer representations. This restarted the field; NETtalk (1987, learned English pronunciation) and ALVINN (1989, autonomous vehicle) were early demonstrations [^src6].

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

- [AI History](/ai-engineering/ai-history.md) — full arc from Perceptron (1957) through deep learning revival; Nilsson's insider account
- [Machine Learning](/ai-engineering/machine-learning.md) — deep learning is the multi-layer extension of ML
- [MLP](/ai-engineering/mlp.md) — multilayer perceptrons: hidden layers, activation functions, backprop, vanishing gradients
- [Transformer](/ai-engineering/transformer.md) — the attention architecture behind LLMs
- [LLM](/ai-engineering/llm.md) — neural networks at billion-parameter scale; reasoning models
- [AI Fundamentals](/ai-engineering/ai-fundamentals.md) — where neural nets sit in the field
- [AI Engineering hub](/ai-engineering/README.md)

---

[^src1]: [Harvard CS50's AI with Python (full course)](../../raw/youtube/youtube-5NgNicANyqM-harvard-cs50s-artificial-intelligence-with-python-full-unive.md) — Brian Yu
[^src2]: [Artificial Intelligence Full Course](../../raw/youtube/youtube-JMUxmLyrhSk-artificial-intelligence-full-course-artificial-intelligence.md) — Edureka
[^src3]: [ai-engineering-from-scratch](../../raw/web/github-rohitg00-ai-engineering-from-scratch-learn-it-build-i.md) — Rohit Ghumare (Phases 3 & 7)
[^src4]: [AI was HARD until I Learned these 10 Concepts](../../raw/youtube/youtube-5DtjQrROUzY-ai-was-hard-until-i-learned-these-10-concepts.md) — Maddy Zhang, [07:48](../../raw/youtube/youtube-5DtjQrROUzY-ai-was-hard-until-i-learned-these-10-concepts.md#t=7:48)
[^src5]: [The Quest for Artificial Intelligence — Part 5 (Ch. 4: Perceptrons, ADALINE, statistical pattern recognition)](../../raw/pdf/pdf-the-quest-for-artificial-intelligence-a-history-of-part-05.md) — Nils Nilsson (Cambridge, 2010)
[^src6]: [The Quest for Artificial Intelligence — Part 20 (Ch. 25: subsumption, connectionism, backprop, PDP volumes)](../../raw/pdf/pdf-the-quest-for-artificial-intelligence-a-history-of-part-20.md) — Nils Nilsson (Cambridge, 2010)

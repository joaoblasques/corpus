---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-the-little-book-of-deep-learning-part-01.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/_inbox/pdf-the-little-book-of-deep-learning-part-02.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/_inbox/pdf-the-little-book-of-deep-learning-part-03.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/_inbox/pdf-the-little-book-of-deep-learning-part-04.md
    channel: pdf
    ingested_at: 2026-08-03
aliases:
  - Little Book of Deep Learning
  - LBDL
  - Fleuret deep learning book
tags:
  - corpus/ai-engineering
  - source
created: 2026-08-03
updated: 2026-08-03
---

# The Little Book of Deep Learning (Fleuret, 2024)

**TL;DR.** A 189-page compact deep learning textbook by François Fleuret (University of Geneva), released free online at fleuret.org/public/lbdl.pdf. Covers foundations (ML basics, GPU computation, tensors, training), deep model components (layers, activations, normalization, attention, positional encoding), architectures (MLP, CNNs, Transformers/GPT/ViT), applications (image denoising, classification, object detection, semantic segmentation, speech recognition, CLIP, RL, text/image generation), and the "Compute Schism" (prompt engineering, quantization, adapters/LoRA, model merging). More than 500,000 downloads in the 12 months after its 2023 announcement.[^p1]

## Scope and structure

- **Part I — Foundations** (Chapters 1–3): Machine learning (parametric models, overfitting, three categories of learning), GPU/TPU hardware and tensors, training (losses, autoregressive models, SGD/Adam, backpropagation, depth value, training protocols, scaling laws, distributed/parallel training).
- **Part II — Deep Models** (Chapters 4–5): Layer taxonomy (fully connected, convolutional, activation functions, pooling, dropout, batch/layer normalization, skip/residual connections, attention, token embedding, positional encoding). Architectures: MLP, LeNet/AlexNet/VGG/ResNet-50 (CNNs), Transformer encoder-decoder, GPT, ViT.
- **Part III — Applications** (Chapters 6–7): Image denoising (denoising autoencoders), image classification, object detection (SSD), semantic segmentation (PSP network), speech recognition (Whisper-style Transformer), CLIP text-image representations, RL (DQN on Atari), text generation (GPT + RLHF), image generation (denoising diffusion / DDPM).
- **Part IV — The Compute Schism** (Chapter 8): Prompt engineering (few-shot, chain-of-thought, RAG), quantization (PTQ, QAT, llama.cpp), adapters/LoRA, model merging (Task Arithmetic, TIES-Merging).

## Key thesis: the Compute Schism

Training large models requires resources only available to major institutions. The book names this asymmetry the "Compute Schism." The response is a set of techniques — quantization, LoRA adapters, model merging — that allow inference and task-adaptation on consumer hardware without full retraining.[^p3]

## Standout coverage

- **Scaling laws** (§ 3.7): Kaplan et al. [2020] show loss improves power-law with compute, data, and parameter count — as long as the other two scale correspondingly. Vision models: 10–100M params, 10¹⁸–10¹⁹ FLOPs. Language models: 100M–hundreds of billions params, 10²⁰–10²³ FLOPs.[^p1]
- **LoRA** (§ 8.3): Replaces a C×D weight matrix W with W + BA where A is R×D, B is C×R, R ≪ min(C,D). Typically reduces trainable parameter count to a few percent of the base model. QLoRA combines quantized base + unquantized LoRA to reduce memory further.[^p3]
- **Model merging** (§ 8.4): Task vectors τ_t = θ_t − θ (fine-tuned minus pre-trained) can be linearly combined: θ + τ_1 + ··· + τ_T yields multi-task capability. Subtraction degrades specific task performance.[^p3-4]
- **CLIP** (§ 6.6): Jointly trains image encoder (ViT) and text encoder (GPT) on 400M image-text pairs with a contrastive loss over an N×N similarity matrix. Enables zero-shot prediction without task-specific fine-tuning.[^p3]

## Corpus pages produced

- [François Fleuret](/ai-engineering/francois-fleuret.md) — entity
- [Deep Learning](/ai-engineering/deep-learning.md) — concept (GPU computation, tensors, training fundamentals)
- [Scaling Laws](/ai-engineering/scaling-laws.md) — concept
- [LoRA and Adapters](/ai-engineering/lora-adapters.md) — concept
- [Model Merging](/ai-engineering/model-merging.md) — concept
- [Computer Vision Tasks](/ai-engineering/computer-vision-tasks.md) — concept (object detection, segmentation, CLIP, denoising)
- [Quantization](/ai-engineering/quantization.md) — updated
- [Multilayer Perceptrons (MLP)](/ai-engineering/mlp.md) — updated
- [Attention Mechanisms](/ai-engineering/attention-mechanisms.md) — updated
- [Transformer](/ai-engineering/transformer.md) — updated
- [Prompt Engineering](/ai-engineering/prompt-engineering.md) — updated

[^p1]: raw/_inbox/pdf-the-little-book-of-deep-learning-part-01.md
[^p2]: raw/_inbox/pdf-the-little-book-of-deep-learning-part-02.md
[^p3]: raw/_inbox/pdf-the-little-book-of-deep-learning-part-03.md
[^p3-4]: raw/_inbox/pdf-the-little-book-of-deep-learning-part-03.md; raw/_inbox/pdf-the-little-book-of-deep-learning-part-04.md

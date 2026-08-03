---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-the-little-book-of-deep-learning-part-03.md
    channel: pdf
    ingested_at: 2026-08-03
aliases:
  - LoRA
  - Low-Rank Adaptation
  - adapters
  - PEFT
  - parameter-efficient fine-tuning
  - QLoRA
  - fine-tuning adapters
tags:
  - corpus/ai-engineering
  - concept
created: 2026-08-03
updated: 2026-08-03
---

# LoRA and Adapters

**TL;DR.** Adapters are lightweight modules with few parameters added to a frozen pre-trained model to specialize it for a downstream task, avoiding full retraining. **LoRA** (Low-Rank Adaptation, Hu et al. [2021]) is the dominant method: it replaces a weight matrix W (C×D) with W + BA where A (R×D) and B (C×R) are trainable with R ≪ min(C, D). The total trainable parameter count is typically a few percent of the base model. **QLoRA** combines a quantized base model with unquantized LoRA adapters to reduce memory further.[^p3]

---

## Why adapters exist

Fine-tuning a full model (§ 3.6 in LBDL) requires storing gradients and optimizer states for all parameters. For a model with hundreds of billions of parameters, this is prohibitively expensive — both in memory and compute. The Compute Schism (see [Scaling Laws](/ai-engineering/scaling-laws.md)) makes full fine-tuning inaccessible to most practitioners.[^p3]

Adapters solve this by: (1) freezing pre-trained weights, (2) introducing a small number of trainable parameters that capture task-specific adjustments, (3) allowing storage of only the adapter delta separately from the (shared) base model.[^p3]

---

## LoRA: Low-Rank Adaptation [Hu et al., 2021]

### Formulation

Given a linear operation XW^T where X is N×D and W is C×D, LoRA replaces it with:

> X(W + BA)^T

where:
- A is R×D (initialized with random Gaussian values)
- B is C×R (initialized to zero, so fine-tuning starts with identical output to base model)
- R ≪ min(C, D) — the **rank** of the adaptation

W is removed from the trainable parameter set. The total parameter overhead is R×D + C×R = R(C+D), versus C×D for the full matrix.[^p3]

### Where adapters are applied

Standard procedure for fine-tuning a Transformer with LoRA: only modify weight matrices in **attention blocks** (W_Q, W_K, W_V, W_O). The **MLP** of the feed-forward blocks remains unchanged. The same strategy has been used for diffusion model fine-tuning (fine-tuning attention blocks responsible for text-based conditioning).[^p3]

### Advantages

1. **Memory**: Reduces optimizer memory (Adam stores two running averages per parameter) from O(model_params) to O(adapter_params).
2. **Compute**: Reduces backward-pass computation.
3. **Storage**: Adapter pairs (A, B) stored separately from the base model — base stored once, many adapters cheaply.
4. **Zero inference overhead**: After training, add BA to W to merge the adapter into the original architecture. Inference is identical to the base model (no adapter-specific compute path).[^p3]

---

## QLoRA [Dettmers et al., 2023]

QLoRA addresses the observation that gradient descent requires high-precision parameters to accumulate small changes — directly quantizing the trainable parameters would degrade learning. The solution:

- **Quantized base model**: the frozen pre-trained weights are quantized (e.g., 4-bit NF4 format)
- **Unquantized LoRA adapters**: the A and B matrices are kept in full precision (BF16)
- Gradient flows through the quantized base model in a way that does not require high-precision base weights[^p3]

This reduces peak GPU memory during fine-tuning significantly, making 65B-parameter model fine-tuning possible on a single consumer GPU.[^p3]

---

## Relationship to other techniques

- **Quantization** (§ 8.2 in LBDL): Reduces inference memory; QLoRA combines both for fine-tuning memory reduction. See [Quantization](/ai-engineering/quantization.md).
- **Model merging** (§ 8.4 in LBDL): Task vectors from full fine-tuning can be merged; LoRA adapters similarly represent delta vectors but are typically not merged via task arithmetic. See [Model Merging](/ai-engineering/model-merging.md).
- **Full fine-tuning**: Starting from a pre-trained model and updating all parameters; computationally expensive but no approximation. See [Deep Learning](/ai-engineering/deep-learning.md) § training protocols.
- **Unsloth**: An efficient LoRA training toolkit; see [Unsloth](/ai-engineering/unsloth.md).[^p3]

---

## Practical notes

- Typical rank R: 4–64 for most tasks; larger R → more capacity → closer to full fine-tuning.
- Typical coverage: 0.1–3% of original parameter count.
- The rank is a hyperparameter — chosen empirically; performance is often insensitive to exact value within a wide range.
- LoRA is part of the broader **PEFT** (Parameter-Efficient Fine-Tuning) family, which includes prompt tuning, prefix tuning, and adapters in the Houlsby et al. [2019] sense.[^p3]

[^p3]: raw/_inbox/pdf-the-little-book-of-deep-learning-part-03.md

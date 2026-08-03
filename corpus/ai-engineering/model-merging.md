---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-the-little-book-of-deep-learning-part-03.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/_inbox/pdf-the-little-book-of-deep-learning-part-04.md
    channel: pdf
    ingested_at: 2026-08-03
aliases:
  - model merging
  - task arithmetic
  - task vectors
  - model fusion
  - TIES-Merging
  - model soup
tags:
  - corpus/ai-engineering
  - concept
created: 2026-08-03
updated: 2026-08-03
---

# Model Merging

**TL;DR.** Model merging combines multiple fine-tuned versions of a base model into a single model with multi-task capabilities, without additional training. The core insight is that models fine-tuned from the same pre-trained base are compatible in parameter space — their **task vectors** (fine-tuned minus pre-trained parameters) can be added, subtracted, and combined. Ilharco et al. [2022] demonstrated **Task Arithmetic** on CLIP-based models; subsequent methods (TIES-Merging, evolutionary optimization) address interference between task vectors at scale.[^p3][^p4]

---

## Why model merging matters

Training a large model from scratch is resource-intensive (see [Scaling Laws](/ai-engineering/scaling-laws.md)). Fine-tuning reduces cost but still requires storing separate model copies for each task. Model merging offers a path to multi-task models with zero additional training cost — at the price of some performance degradation relative to independent fine-tuned models.[^p3]

---

## Task Arithmetic [Ilharco et al., 2022]

### Core formulation

Let θ be the parameters of a pre-trained base model. After fine-tuning on task t, the model has parameters θ_t. Define the **task vector**:

> τ_t = θ_t − θ

Key empirical findings:
- **Addition**: The model with parameters θ + τ₁ + ··· + τ_T exhibits multi-task capabilities across all T tasks.
- **Subtraction**: The model with parameters θ − τ_t degrades performance on task t (without affecting other tasks much). This can remove unwanted behaviors.
- **Scaling**: Multiplying τ_t by a scalar modulates the strength of task adaptation.[^p3]

### Origin

Demonstrated on CLIP models fine-tuned on several image classification datasets. Ilharco et al. found that the parameter space of fine-tuned models from the same base has arithmetic structure — an unexpected geometric regularity.[^p3]

---

## Addressing interference: TIES-Merging [Yadav et al., 2023]

When many task vectors are merged, they interfere — parameters updated in different directions by different tasks reduce each other's effect. TIES-Merging applies three steps before summing:
1. **Trim**: Zero out small magnitude updates (assume they carry little task-specific signal).
2. **Elect**: For each parameter position, determine the dominant sign across tasks.
3. **Merge**: Sum only the task vectors that agree with the elected sign.[^p3][^p4]

---

## Super Mario: absorbing capabilities [Yu et al., 2023]

A related finding: models trained on similar tasks (e.g., different languages, or related NLP tasks) can merge capabilities with no additional training — "absorbing abilities from homologous models as a free lunch." Suggests that fine-tuned weights encode capabilities in task-decomposable subspaces.[^p4]

---

## Evolutionary optimization of merging recipes [Akiba et al., 2024]

Combines parameter-space merging with layer-level recombination. Instead of merging all layers uniformly, the algorithm uses stochastic optimization to find which layers to merge and which to source from which fine-tuned model. Applied to three fine-tuned Mistral-7B variants: combining parameter merging + layer recombination outperforms either strategy alone.[^p3][^p4]

---

## Relationship to other techniques

- **LoRA adapters**: Task vectors and LoRA adapters both represent deltas over the base model — task arithmetic is typically applied to full fine-tuned models, not LoRA adapters, though adapter merging is an active research area. See [LoRA and Adapters](/ai-engineering/lora-adapters.md).
- **Quantization**: Models are typically merged before quantization; post-merge quantization compresses the merged multi-task model. See [Quantization](/ai-engineering/quantization.md).
- **CLIP**: The original task arithmetic experiments used CLIP models. See [Computer Vision Tasks](/ai-engineering/computer-vision-tasks.md) for CLIP background.
- **Foundation models**: Large pre-trained models are the substrate for task arithmetic — the shared base must be identical for the parameter space to be compatible. See [LLM](/ai-engineering/llm.md).

---

## Practical gotchas

- Merging works well when all models start from the **same base checkpoint**. Merging models fine-tuned from different bases or with different architectures does not work.
- Performance degrades as the number of merged tasks increases; interference mitigation (TIES) helps but does not fully close the gap vs. individual fine-tuned models.
- The approach is primarily validated on models with up to ~7–33B parameters; scaling behavior to much larger models is not yet well characterized.[^p3][^p4]

[^p3]: raw/_inbox/pdf-the-little-book-of-deep-learning-part-03.md
[^p4]: raw/_inbox/pdf-the-little-book-of-deep-learning-part-04.md

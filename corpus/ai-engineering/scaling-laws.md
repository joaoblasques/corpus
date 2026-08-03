---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-the-little-book-of-deep-learning-part-01.md
    channel: pdf
    ingested_at: 2026-08-03
aliases:
  - scaling laws
  - neural scaling laws
  - compute scaling
  - parallel training
  - DDP
  - FSDP
  - pipeline parallelism
  - tensor parallelism
  - Kaplan scaling laws
tags:
  - corpus/ai-engineering
  - concept
created: 2026-08-03
updated: 2026-08-03
---

# Scaling Laws

**TL;DR.** Neural language model test loss follows a power law with compute, dataset size, and parameter count — as long as the other two scale correspondingly [Kaplan et al., 2020]. This empirical regularity has driven exponential growth in model size (AlexNet → GPT-3: 100M → 175B parameters). It also motivates large-scale parallel training strategies to distribute computation and memory across thousands of GPUs.[^p1]

---

## The empirical scaling law

Kaplan et al. [2020] show that test loss L improves as a smooth power law of three independent axes[^p1]:
- **Compute**: petaflop/s-days of training compute
- **Dataset size**: number of tokens in the training set
- **Model size**: number of trainable parameters

The key constraint: if one axis is held fixed while the other two scale, performance saturates. All three must grow together for continued improvement. This motivates very large models trained on very large datasets.

## Model size in practice

**Vision models**: 10–100 million trainable parameters, require 10¹⁸–10¹⁹ FLOPs for training (reference: He et al. [2015], Sevilla et al. [2022]).[^p1]

**Language models**: 100M to hundreds of billions of trainable parameters, require 10²⁰–10²³ FLOPs for training (BERT, GPT-3, PaLM; Devlin et al. [2018], Brown et al. [2020], Chowdhery et al. [2022]).[^p1]

Training cost timeline (Sevilla et al., 2023): AlexNet (2015) ~10¹⁸ FLOPs/1 KWh → GPT-2 (2019) ~10²¹ FLOPs/1 MWh → GPT-3, LaMDA, PaLM (~10²³–10²⁴ FLOPs/1 GWh).[^p1]

Training the largest models may take months on thousands of GPUs and cost millions of dollars. At this scale, training involves many manual interventions driven by loss dynamics.[^p1]

## Training data at scale

Large-scale training relies on automatically assembled internet datasets with minimal curation — detailed ground-truth labels are too costly and would limit dataset size. These datasets may combine multiple modalities (text + images from web pages, audio + video) for large-scale supervised training.[^p1]

Representative datasets by size:
- ImageNet (2012): 1.2M images, 150 GB
- LAION-5B (2022): 5.8B images, 240 TB
- The Pile (2020): 1.6B text "books," 825 GB
- OSCAR (2020): 12B text "books," 6 TB[^p1]

## Paradox: large models and overfitting

Classical theory predicts that high-capacity models should suffer from severe overfitting. In practice, large models often continue to improve as training progresses rather than overfitting. This may be because the **inductive bias** of the model's architecture becomes the dominant driver of optimization once training-set performance is near-perfect [Belkin et al., 2018].[^p1]

---

## Large-scale parallel training

Training very large models requires memory and compute beyond a single GPU. Four main strategies[^p1]:

### 1. Distributed Data Parallelism (DDP)
- Model fully replicated on each GPU; each replica processes a different slice of the batch.
- During backward pass, each GPU communicates its computed gradient to all others → all replicas update identically and remain in sync.
- **Scales**: effective batch size linearly with device count.
- **Constraint**: full model must fit in each device's memory.[^p1]

### 2. Fully Sharded Data Parallelism (FSDP) [Zhao et al., 2023]
- Combines data parallelism memory-efficiency by distributing parameters, gradients, and optimizer states across devices as **shards**.
- When a computation needs a tensor, all shards are temporarily gathered, used, then released.
- **Scales**: maximum model size linearly with device count.
- **Cost**: greater inter-GPU communication (can be overlapped with computation).[^p1]

### 3. Pipeline parallelism
- Dispatches entire layers to different GPUs.
- Trades parameter communication (FSDP) for activation communication.
- Useful when layers don't fit on a single GPU but the parameter sharding approach introduces too much communication overhead.[^p1]

### 4. Tensor parallelism
- For very large models where individual layers cannot fit on a single device.
- Decomposes matrix products into block products whose intermediate results can be combined through simple operations.
- Named after the property of matrix products that allow decomposition into parallel sub-products.[^p1]

---

## Fine-tuning and the Compute Schism

Scaling laws also define a hard boundary: training from scratch requires resources available only to large institutions. This motivates:
- **Fine-tuning** on downstream tasks from pre-trained models (§ 3.6 in [LBDL])
- **LoRA adapters** for parameter-efficient fine-tuning (see [LoRA and Adapters](/ai-engineering/lora-adapters.md))
- **Quantization** for memory-efficient inference (see [Quantization](/ai-engineering/quantization.md))
- **Model merging** to combine capabilities without retraining (see [Model Merging](/ai-engineering/model-merging.md))[^p1]

---

## See also

- [Deep Learning](/ai-engineering/deep-learning.md) — training mechanics
- [LLM](/ai-engineering/llm.md) — large language models as the prime beneficiary of scaling
- [Quantization](/ai-engineering/quantization.md)
- [LoRA and Adapters](/ai-engineering/lora-adapters.md)

[^p1]: raw/_inbox/pdf-the-little-book-of-deep-learning-part-01.md

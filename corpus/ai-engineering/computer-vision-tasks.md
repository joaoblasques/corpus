---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-the-little-book-of-deep-learning-part-02.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/_inbox/pdf-the-little-book-of-deep-learning-part-03.md
    channel: pdf
    ingested_at: 2026-08-03
aliases:
  - computer vision tasks
  - image classification
  - object detection
  - semantic segmentation
  - image denoising
  - denoising autoencoder
  - SSD
  - Single Shot Detector
  - CLIP
  - Contrastive Language-Image Pre-training
  - ViT
  - Vision Transformer
  - zero-shot classification
  - PSP network
  - Pyramid Scene Parsing
  - data augmentation
tags:
  - corpus/ai-engineering
  - concept
created: 2026-08-03
updated: 2026-08-03
---

# Computer Vision Tasks

**TL;DR.** Deep learning has produced standard solution patterns for the core CV prediction tasks: image denoising (denoising autoencoders with MSE), image classification (ResNet/ViT + cross-entropy + data augmentation), object detection (SSD multi-scale convolutional detector), semantic segmentation (downscale-upscale U-Net with skip connections), and multi-modal alignment (CLIP contrastive text-image training enabling zero-shot prediction). Each task builds on [CNNs](/ai-engineering/convolutional-neural-networks.md) and/or [Transformers](/ai-engineering/transformer.md); all benefit from fine-tuning a model pre-trained on a large classification dataset.[^p2][^p3]

---

## Image denoising

**Task**: Given a degraded image X̃, estimate the original clean image X.

**Model**: A **denoising autoencoder** — a convolutional network (possibly with skip connections for multi-resolution fusion and attention layers for distant-dependency modeling) that maps X̃ → X.[^p3]

**Training**: Collect pairs (X, X̃) where X̃ is algorithmically degraded (grayscale conversion, downscaling, lossy compression, noise addition). Minimize pixel-wise MSE: the model learns to compute E[X | X̃].[^p3]

**Gotcha**: MSE loss computes an expectation over the unknown clean signal. When the original X is not fully determined by X̃ (e.g., for texture or color), the model averages over the distribution of plausible clean images → **blurry outputs** in uncertain regions. Perceptual and adversarial losses address this.[^p3]

**Connection**: Denoising autoencoders are the core denoising step in **diffusion models** (§ 7.2 in LBDL) — the denoiser f(x_t, t; w) is exactly a denoising autoencoder trained on noisy images at all noise levels.[^p3]

---

## Image classification

**Task**: Given image X, predict class Y from a fixed set {1,...,C}.

**Models**: Standard architectures are ResNets (see [CNNs](/ai-engineering/convolutional-neural-networks.md)) and ViT (see [Transformer](/ai-engineering/transformer.md) § Vision Transformer). Both output a vector of C logits.[^p3]

**Training**: Minimize cross-entropy loss (see [Deep Learning](/ai-engineering/deep-learning.md) § losses). **Data augmentation** — random crops, scaling, flipping, color jitter — applies semantic-preserving transformations to training images. This effectively multiplies dataset size and improves generalization.[^p3]

**Pre-training**: ImageNet (1.2M images, 1000 classes) is the standard pre-training dataset for downstream vision tasks. Models pre-trained on ImageNet develop feature representations general enough to transfer to object detection and segmentation, even though ImageNet contains only classification labels.[^p3]

---

## Object detection

**Task**: Given image X, predict classes and bounding boxes (x₁, y₁, x₂, y₂) for all objects of interest.

**Approach**: The **Single Shot Detector (SSD)** [Liu et al., 2015] uses a convolutional backbone producing representations Z_s at S scales (spatial resolution decreasing with s, down to 1×1 for s=S).[^p3]

**Multi-scale prediction**: At each scale s and spatial position (h, w), the feature vector Z_s[0:D, h, w] is a descriptor of the **receptive field** centered at (h, w). The SSD adds S convolutional layers, each predicting:
- Bounding box coordinates (x̂₁, ŷ₁, x̂₂, ŷ₂) — 4 values per prediction
- Class logits — C+1 values (C classes + "no object")
- Multiple bounding boxes per (s, h, w), one per hardcoded aspect ratio range[^p3]

**Training**:
- Match each ground-truth box to (s, h, w) by box size and center.
- Loss: cross-entropy for class logits + regression loss (MSE) for box coordinates, at matched positions; cross-entropy for "no object" everywhere else.
- Fine-tune from a pre-trained classification backbone (VGG-16 for original SSD). Classification training transfers detection-relevant features even without bounding box supervision.[^p3]

---

## Semantic segmentation

**Task**: For each pixel, predict the class of the object it belongs to. The finest-grain image understanding task.

**Architecture challenge**: The task requires both:
1. Large receptive fields (to identify context, object identity) → requires downscaling
2. High spatial resolution in the output (per-pixel prediction) → requires upscaling

Standard architecture: **downscale-upscale** with transposed convolutions or bilinear interpolation for upscaling.[^p3]

**Skip connections are essential**: A strict downscale-upscale loses fine spatial detail at the bottleneck. Two solutions:
1. **Serial skip connections** [U-Net, Long et al. 2014; Ronneberger et al. 2015]: skip connections from early encoder layers (at resolution R) directly to later decoder layers at the same resolution R, preserving high-frequency spatial detail.
2. **Parallel multi-scale** [PSP/Pyramid Scene Parsing, Zhao et al. 2016]: Apply the backbone at multiple scales in parallel, concatenate after upscaling, make final per-pixel prediction on concatenated representation.[^p3]

**Training**: Cross-entropy summed over all pixels. Fine-tune from an ImageNet pre-trained backbone.[^p3]

---

## CLIP: Contrastive Language-Image Pre-training [Radford et al., 2021]

**Task**: Learn consistent joint image-text embeddings — an image and its text description should map to similar vectors; unrelated pairs should be dissimilar.

**Architecture**: Two encoders trained jointly:
- **Image encoder**: ViT (see [Transformer](/ai-engineering/transformer.md))
- **Text encoder**: GPT repurposed as an encoder (add "end of sentence" token; use its final-layer representation as the embedding)[^p3]

**Training data**: 400 million image-text pairs collected from the internet.[^p3]

**Contrastive loss**: For a mini-batch of N (image, text) pairs, compute an N×N similarity matrix l_{m,n} = f(i_m) · g(t_n). Train with cross-entropy so that l_{n,n} > l_{n,m} and l_{n,n} > l_{m,n} for all m≠n. This forces the diagonal (matched pairs) to have higher similarity than all off-diagonal (unmatched) entries.[^p3]

**Zero-shot prediction**: After training, classify a new image by:
1. Define text descriptions for candidate classes (e.g., "a photo of a dog")
2. Compute text embeddings for all descriptions
3. Compute image embedding
4. Predict the class whose text embedding is most similar to the image embedding
No task-specific fine-tuning is needed.[^p3]

**Robustness**: CLIP captures richer image representations than standard classifiers because the textual descriptions are more diverse than label names. It achieves excellent performance on adversarial datasets (ImageNet Adversarial [Hendrycks et al., 2019]) that degrade cues used by standard classifiers.[^p3]

**Connection to diffusion models**: Nichol et al. [2021] (GLIDE) extend CLIP-conditioned image generation by biasing the denoising mean in the direction that increases the CLIP matching score between the generated image and a text prompt.[^p3]

---

## Speech recognition

**Task**: Convert a sound sample to a sequence of words.

**Modern approach** [Radford et al., 2022 — Whisper]: Cast as sequence-to-sequence translation, use a standard Transformer encoder-decoder.[^p3]

Pipeline:
1. Convert audio to spectrogram: T×D series encoding energies in D frequency bands at each time step.
2. Encode text with BPE tokenizer (see [Deep Learning](/ai-engineering/deep-learning.md) § autoregressive models).
3. Pass spectrogram through 1D convolutional layers → Transformer encoder.
4. Decoder generates discrete token sequence for any of: English transcription, non-English transcription, English translation, or non-speech label (background music, ambient noise).

Multi-task training enables leveraging very large diverse datasets. Noteworthy: the decoder is functionally identical to a generative autoregressive language model (GPT).[^p3]

---

## See also

- [Convolutional Neural Networks](/ai-engineering/convolutional-neural-networks.md) — the backbone architecture for most CV tasks
- [Transformer](/ai-engineering/transformer.md) — ViT, GPT as text encoder for CLIP
- [Deep Learning](/ai-engineering/deep-learning.md) — skip connections, batch normalization, pooling
- [Reinforcement Learning](/ai-engineering/reinforcement-learning.md) — DQN on Atari (CV + RL)
- [Generative Adversarial Networks](/ai-engineering/generative-adversarial-networks.md) — alternative to diffusion models for image synthesis

[^p2]: raw/_inbox/pdf-the-little-book-of-deep-learning-part-02.md
[^p3]: raw/_inbox/pdf-the-little-book-of-deep-learning-part-03.md

<!-- RELATED:START (generated by bin/corpus_heal.py related — do not edit inside) -->

## Related across domains

- [File Systems](/software-engineering/file-systems.md) · _software-engineering_

<!-- RELATED:END -->

---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-zhang-lipton-li-smola-dive-into-deep-learning-cc-by-sa-4-0-part-16.md
    channel: pdf
    ingested_at: 2026-07-10
aliases:
  - convolutional neural network
  - CNN
  - convolution
  - AlexNet
  - ResNet
  - VGG
  - LeNet
  - batch normalization
  - pooling
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-10
updated: 2026-07-10
---

# Convolutional Neural Networks (CNNs)

**TL;DR**: Neural network architecture exploiting two inductive biases of spatial data — **translation invariance** (a feature at position (i,j) is equally useful at position (i+k,j+k)) and **locality** (nearby pixels are more correlated than distant ones). CNNs replaced hand-crafted features for vision with AlexNet (2012), launching the deep learning era. Modern architectures (ResNet, DenseNet) use residual connections to train extremely deep networks. Batch normalization (2015) made training 100+ layer networks practical. See also [MLP](/ai-engineering/mlp.md) for the foundational non-convolutional architecture.

## Inductive biases: translation invariance and locality

Fully connected layers treat all input-output pairs equivalently — an image with 1M pixels would require 1M weights per hidden unit, ignoring the fact that "the presence of a particular pattern within an image was not critical to the purpose of understanding" its spatial origin [^src1]. Two useful constraints for images:

1. **Translation invariance**: a learned feature detector should respond the same way regardless of where in the image it appears
2. **Locality**: predictions should depend on nearby pixels, not distant ones

These constraints lead naturally to the convolution operation — a shared weight kernel sliding over the input.

## The convolution operation and cross-correlation

In practice, CNNs implement **cross-correlation** (not strict mathematical convolution, which flips the kernel) [^src1]. For a 2D input X and kernel W:

```
(X * W)[i,j] = sum_{a,b} X[i+a, j+b] * W[a, b]
```

The kernel W is learned, shared across all spatial positions. For an h×w kernel applied to an n×m input, the output is (n-h+1) × (m-w+1).

**Padding** adds zeros around the input border, controlling output size. With padding p=(h-1)/2 on each side, output height equals input height (same-convolution). **Stride** s>1 subsamples the output, reducing spatial dimensions by factor s.

## Multiple channels

Real networks use multiple input channels (e.g., RGB: 3 channels) and multiple output channels (feature maps). A convolutional layer with c_i input channels, c_o output channels, and h×w kernel has c_i × c_o × h × w parameters. Each output channel gets its own set of c_i kernels [^src1].

**1×1 convolutions** apply a fully connected transformation channel-wise at each spatial position, enabling channel mixing without spatial mixing — used in Network in Network (NiN) and as bottleneck layers in inception blocks.

## Pooling

Pooling layers reduce spatial resolution, achieving translational robustness by aggregating local regions [^src1]:

- **Max pooling**: take maximum value in each window — extracts dominant feature
- **Average pooling**: take mean — smoother but less discriminative
- **Global average pooling** (GAP): pool to a single value per channel — used in NiN, GoogLeNet as the final layer before classification; removes fully connected layers, reducing parameters drastically

Typical: 2×2 max pooling with stride 2 halves spatial dimensions.

## Classic architectures

### LeNet (LeCun et al., 1998)

The original CNN for handwritten digit recognition [^src1]. Architecture: Conv(6 filters) → Avg Pool → Conv(16 filters) → Avg Pool → FC(120) → FC(84) → Softmax(10). Used sigmoid/tanh activations. Demonstrated that CNNs could learn from raw pixels, but was not widely adopted until hardware caught up.

### AlexNet (Krizhevsky et al., 2012)

Won ImageNet 2012, launching the deep learning era [^src1]. Key innovations:
- **Scale**: 5 conv layers, 3 FC layers, 60M parameters, trained on 2 GPUs
- **ReLU activations**: replaced sigmoid, solving vanishing gradients
- **Dropout** (p=0.5) in FC layers for regularization
- **Data augmentation**: random crops, horizontal flips
- **Local response normalization** (precursor to batch norm)

AlexNet proved that deep CNNs with ReLU trained on large datasets (ImageNet) dramatically outperform hand-crafted features. "This marks the beginning of a much more deliberate network design" [^src1].

### VGG (Simonyan and Zisserman, 2014)

Replaced large kernels (11×11, 5×5 in AlexNet) with stacks of small 3×3 kernels. Two 3×3 conv layers have the same receptive field as one 5×5, but fewer parameters and more non-linearities. Introduced the VGG **block** (conv layers + max pool) as a reusable building block [^src1]. VGG-16 and VGG-19 remain widely used as feature extractors.

### Network in Network (NiN, Lin et al., 2013)

Replaced FC layers with 1×1 convolutions and global average pooling. The 1×1 conv applies a small MLP at each spatial position, allowing complex channel mixing while maintaining spatial structure. GAP summarizes spatial information without a large FC layer [^src1].

### GoogLeNet / Inception (Szegedy et al., 2014)

Key innovation: the **Inception block** — applies multiple kernel sizes (1×1, 3×3, 5×5) and pooling in parallel, concatenating results. This allows the network to capture features at multiple scales simultaneously. Also uses 1×1 convolutions to reduce channels before expensive larger convolutions [^src1].

"GoogLeNet is actually cheaper to compute than its predecessors while simultaneously providing improved accuracy. This marks the beginning of a much more deliberate network design that trades off the cost of evaluating a network with a reduction in errors." [^src1]

### Batch Normalization (Ioffe and Szegedy, 2015)

Training deep networks is difficult because intermediate layer statistics shift as parameters change (internal covariate shift). Batch normalization normalizes each layer's pre-activation using the current mini-batch mean and variance, then applies learned scale and shift [^src1]:

```
x_hat = (x - mu_B) / sqrt(sigma_B^2 + eps)
y = gamma * x_hat + beta        (learned scale and shift)
```

Where mu_B and sigma_B^2 are computed over the mini-batch. At inference time, use running averages from training.

Three benefits: (1) faster training via larger learning rates; (2) mild regularization from mini-batch noise; (3) reduced sensitivity to initialization. "Together with residual blocks, batch normalization has made it possible for practitioners to routinely train networks with over 100 layers." [^src1]

**Layer normalization**: normalizes per sample (not per batch), across features — used in Transformers where batch statistics are ill-defined. Works for mini-batches of size 1 [^src1].

### ResNet (He et al., 2016)

The key challenge of very deep networks: as depth increases, training accuracy can degrade (not just overfitting — the training loss itself degrades). ResNets solve this with **residual connections** [^src1]:

```
output = F(x, {W_i}) + x      (residual block)
```

The shortcut connection lets gradient flow directly through the identity mapping, bypassing any number of layers. This ensures that adding layers can never hurt (the worst case is learning F=0, recovering the identity). ResNet-50, ResNet-101, ResNet-152 became standard backbones.

**ResNeXt** extends ResNets with grouped convolutions (cardinality dimension), achieving better accuracy/compute tradeoffs.

### DenseNet (Huang et al., 2017)

Takes residual connections to the extreme: each layer connects to all subsequent layers [^src1]:

```
h_l = phi(BN(concat(h_0, h_1, ..., h_{l-1})))
```

Dense connectivity encourages feature reuse, reduces parameters (each layer is narrow), and provides implicit deep supervision. **Transition layers** (1×1 conv + 2×2 avg pool) reduce channel count between dense blocks.

## Computer vision applications (Chapter 14)

Beyond classification, CNNs power [^src1]:
- **Image augmentation**: random crops, flips, color jitter during training — cheap regularization
- **Fine-tuning**: take pretrained CNN backbone, replace final FC layer, train on new dataset with lower learning rate (transfer learning)
- **Object detection**: anchor boxes, IoU, non-maximum suppression; architectures: SSD (single-shot), R-CNN family (two-stage: region proposal + classification), Faster R-CNN
- **Semantic segmentation**: fully convolutional networks (FCN), transposed convolutions (upsampling)
- **Neural style transfer**: separate content features (late layers) from style features (gram matrices of early layers)

## Key patterns

| Pattern | Mechanism | Why it works |
|---|---|---|
| Small kernels (3×3) | Stack multiple → same receptive field as large kernel | More non-linearity, fewer parameters |
| Batch norm before ReLU | Normalize then activate | Keeps activations in non-saturating region |
| Residual connection | Output += Input | Direct gradient path; enables 100+ layers |
| Global avg pooling | Replace FC layers | Spatial equivariance, fewer params, less overfitting |
| Bottleneck blocks | 1×1 → 3×3 → 1×1 | Cheap channel mixing + spatial computation |

## See also

- [MLP](/ai-engineering/mlp.md) — fully connected baseline; CNNs are structured MLPs
- [Attention Mechanisms](/ai-engineering/attention-mechanisms.md) — ViT applies attention to image patches
- [NLP Deep Learning](/ai-engineering/nlp-deep-learning.md) — 1D convolutions for text (textCNN)
- [Dive into Deep Learning](/ai-engineering/sources/dive-into-deep-learning.md) — source textbook (Chapters 7–8, 14)

---

[^src1]: [D2L Part 16 — GoogLeNet, Batch Normalization, ResNet, DenseNet](../../raw/pdf/pdf-zhang-lipton-li-smola-dive-into-deep-learning-cc-by-sa-4-0-part-16.md)

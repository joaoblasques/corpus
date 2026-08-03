---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-computer-vision-foundations-and-applications-part-01.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/_inbox/pdf-computer-vision-foundations-and-applications-part-02.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/_inbox/pdf-computer-vision-foundations-and-applications-part-03.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/_inbox/pdf-computer-vision-foundations-and-applications-part-04.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/_inbox/pdf-computer-vision-foundations-and-applications-part-05.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/_inbox/pdf-computer-vision-foundations-and-applications-part-06.md
    channel: pdf
    ingested_at: 2026-08-03
aliases:
  - CS131
  - Stanford CS131
  - Computer Vision Foundations and Applications
  - Ranjay Krishna computer vision
tags:
  - corpus/ai-engineering
  - source
created: 2026-08-03
updated: 2026-08-03
---

# Computer Vision: Foundations and Applications (Ranjay Krishna, Stanford, 2017)

**TL;DR.** Stanford CS131 course notes compiled by Ranjay Krishna (2017, 213 pp, Apache 2.0). Covers classical computer vision (color, filtering, edge detection, feature detection, segmentation, optical flow, tracking) plus applied pattern recognition (face identification, bag of words, deformable parts models). The textbook's main unique contribution to this corpus is its systematic treatment of classical pre-deep-learning CV: Harris corners, SIFT, HoG, Hough transforms, RANSAC, Lucas-Kanade optical flow, and deformable parts models. Deep-learning content is brief (one chapter stub at the end) and is better covered in other corpus sources.

---

## Coverage by chapter

| Chapter | Pages | Unique to this source? |
|---|---|---|
| Introduction to Computer Vision | 17–23 | Minor — interdisciplinary framing, historical note |
| Color | 25–30 | Yes — CIE color spaces, trichromatic theory, white balancing |
| Linear Algebra Primer | 31–43 | No — see [Linear Algebra for ML](/ai-engineering/linear-algebra-for-ml.md) |
| Pixels and Filters | 45–53 | Partially — convolution/correlation formalism supplements [CNNs](/ai-engineering/convolutional-neural-networks.md) |
| Edge Detection | 55–69 | Yes — Sobel, Canny, Hough transform, RANSAC |
| Features and Fitting | 71–80 | Yes — Harris corners, local invariant features |
| Feature Descriptors | 81–88 | Yes — SIFT, HoG, DoG scale-space |
| Image Resizing | 89–99 | Yes — seam carving (content-aware retargeting) |
| Semantic Segmentation | 101–119 | Partially — basic clustering-based segmentation (k-means, mean-shift already in corpus) |
| Object Recognition | 121–131 | No — k-NN, bias-variance overlap with existing pages |
| Dimensionality Reduction | 133–138 | No — SVD/PCA covered in [PCA and Dimensionality Reduction](/ai-engineering/pca-and-dimensionality-reduction.md) |
| Face Identification | 139–149 | Partially — Eigenfaces extends PCA; Fisherfaces/LDA cross-reference |
| Visual Bag of Words | 151–160 | Yes — BoW image representation, TF-IDF retrieval, spatial pyramid matching |
| Object Detection from Deformable Parts | 161–179 | Yes — sliding window, DPM star model, HOG pyramid |
| Semantic Hierarchies & Fine-Grained Recognition | 181–188 | Yes — semantic hierarchy hedging, Bubble/crowd annotation games |
| Motion | 189–199 | Yes — optical flow (Lucas-Kanade, Horn-Schunk), aperture problem |
| Tracking | 201–208 | Yes — KLT tracker, 2D transformations (affine/similarity/projective) |
| Deep Learning | 209 | No — stub only |

---

## Key corpus pages created

- [Classical Feature Detection](/ai-engineering/classical-feature-detection.md) — Harris corners, SIFT, HoG, DoG scale-space
- [Optical Flow](/ai-engineering/optical-flow.md) — Lucas-Kanade, Horn-Schunk, aperture problem, KLT tracker
- [Visual Bag of Words](/ai-engineering/visual-bag-of-words.md) — BoW image retrieval, TF-IDF, spatial pyramid matching
- [Deformable Parts Model](/ai-engineering/deformable-parts-model.md) — DPM object detection, star model, HOG pyramid

---

## Relationship to other sources

This textbook predates the Transformer era (2017) and complements deeper-learning-focused corpus sources:

- Classical edge/feature detection here → deep CNN features in [Convolutional Neural Networks](/ai-engineering/convolutional-neural-networks.md)
- Classical optical flow here → modern video models not yet in corpus
- Classical object detection (DPM) here → SSD/YOLO/Faster-RCNN in [Computer Vision Tasks](/ai-engineering/computer-vision-tasks.md)
- Classical segmentation here → U-Net, PSP semantic segmentation in [Computer Vision Tasks](/ai-engineering/computer-vision-tasks.md)
- PCA/Eigenfaces here → full PCA treatment in [PCA and Dimensionality Reduction](/ai-engineering/pca-and-dimensionality-reduction.md)

[^p1]: raw/_inbox/pdf-computer-vision-foundations-and-applications-part-01.md
[^p2]: raw/_inbox/pdf-computer-vision-foundations-and-applications-part-02.md
[^p3]: raw/_inbox/pdf-computer-vision-foundations-and-applications-part-03.md
[^p4]: raw/_inbox/pdf-computer-vision-foundations-and-applications-part-04.md
[^p5]: raw/_inbox/pdf-computer-vision-foundations-and-applications-part-05.md
[^p6]: raw/_inbox/pdf-computer-vision-foundations-and-applications-part-06.md

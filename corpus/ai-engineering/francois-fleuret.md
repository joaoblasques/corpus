---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-the-little-book-of-deep-learning-part-01.md
    channel: pdf
    ingested_at: 2026-08-03
aliases:
  - François Fleuret
  - Francois Fleuret
  - F. Fleuret
tags:
  - corpus/ai-engineering
  - entity
created: 2026-08-03
updated: 2026-08-03
---

# François Fleuret

**TL;DR.** Professor of computer science at the University of Geneva, Switzerland. Author of *The Little Book of Deep Learning* (fleuret.org, 2023/2024), a 189-page free compact deep learning textbook with 500,000+ downloads in its first year. Also the co-author of linear attention (Katharopoulos et al. 2020 — "Transformers are RNNs"), which linearizes the standard O(n²) attention operator.[^src1]

## Background

Fleuret's book emerged from his teaching at EPFL and the University of Geneva. The goal was a minimal, phone-screen-formatted reference for practitioners who already understand calculus and linear algebra and need to understand modern deep learning architectures.[^src1]

## Key contributions

- **The Little Book of Deep Learning** (LBDL, 2023/2024, CC BY-NC-SA 4.0): Covers foundations → components → architectures → applications → compute schism (LoRA, quantization, model merging). See [source page](/ai-engineering/sources/the-little-book-of-deep-learning.md).
- **Linear attention** (with Katharopoulos et al., ICML 2020): Reformulates the attention operator as a kernel function to linearize the key-value product and reduce O(n²) cost to O(n). This "Transformers are RNNs" paper is cited in the book as a strategy to reduce quadratic attention cost.[^src1]

## Affiliation

University of Geneva, Switzerland (professor). Previously at EPFL.[^src1]

[^src1]: raw/_inbox/pdf-the-little-book-of-deep-learning-part-01.md

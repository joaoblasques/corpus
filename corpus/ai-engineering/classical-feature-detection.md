---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-computer-vision-foundations-and-applications-part-02.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/_inbox/pdf-computer-vision-foundations-and-applications-part-03.md
    channel: pdf
    ingested_at: 2026-08-03
aliases:
  - Harris corner detector
  - Harris corners
  - SIFT
  - Scale-Invariant Feature Transform
  - HoG
  - Histogram of Oriented Gradients
  - DoG
  - Difference of Gaussians
  - feature descriptor
  - keypoint detection
  - scale-space detection
  - local invariant features
  - edge detection
  - Canny edge detector
  - Sobel filter
  - Hough transform
  - RANSAC
confidence: 0.95
last_confirmed: 2026-08-03
tags:
  - corpus/ai-engineering
  - concept
created: 2026-08-03
updated: 2026-08-03
---

# Classical Feature Detection

**TL;DR.** Before deep learning dominated vision, a pipeline of hand-crafted detectors extracted repeatable, distinctive keypoints and described them with local gradient histograms. Harris corners detect interest points robust to rotation; DoG/SIFT extends this across scales; HoG captures shape via oriented gradient histograms; Hough transforms and RANSAC fit geometric models robustly to noisy edge maps. These methods remain reference algorithms and underlie an understanding of what deep CNN features implicitly learn.

---

## Edge Detection

Edges arise where image intensity changes sharply — at depth discontinuities, surface normal changes, color boundaries, or illumination discontinuities.[^p2]

**Goal**: detect edges with (1) low false-positive rate, (2) accurate localization, and (3) one response per edge (no fragmentation).[^p2]

### Gradient-based edge detection

The image gradient at pixel (x, y):

```
∇f = [∂f/∂x, ∂f/∂y]
```

Gradient magnitude = `||∇f||`; gradient direction = `atan2(∂f/∂y, ∂f/∂x)`. Edges occur at gradient magnitude peaks. Discrete approximations: backward, forward, or central difference kernels.[^p2]

**Noise problem**: noise amplifies derivatives. Solution: smooth first with a Gaussian g, then differentiate: `d/dx(g * f) = (d/dx g) * f` (derivative theorem of convolution — saves one operation).[^p2]

### Sobel filter

Two 3×3 kernels approximating the smoothed x- and y-derivatives. Convolve with image; compute magnitude. Limitations: poor localization, biases toward horizontal/vertical edges over oblique edges.[^p2]

### Canny edge detector

Five-step algorithm that optimizes the detection–localization–silence trade-off:[^p2]

1. **Suppress noise**: Gaussian blur
2. **Compute gradient magnitude and direction**
3. **Non-maximum suppression**: at each pixel, keep only if it is the local maximum along its gradient direction (round gradient angle to nearest 45°); zero all others
4. **Hysteresis thresholding**: pixels above high threshold → strong edge; below low threshold → rejected; between → weak edge
5. **Connectivity analysis**: weak edges connected to a strong edge via BFS/DFS are retained; isolated weak edges are dropped

Result: thin, well-localized, connected edge chains.

### Hough transform

Detects parametric structures (lines, circles) in edge images by voting in parameter space.[^p2]

**For line detection** — represent a line as `x·cos θ + y·sin θ = ρ` (ρ,θ space avoids the infinite-slope problem of (a,b) space). Each edge pixel votes for all (ρ,θ) pairs consistent with a line through it — a sinusoidal curve in ρ,θ space. Accumulate votes in a discretized grid; peaks indicate real lines.

**Advantages**: handles noise and partial occlusion well; finds multiple lines simultaneously; generalizes to any shape with a known parametric equation.

**Disadvantages**: computationally expensive with many parameters; cannot detect one-off structures without a known model; cannot separate co-linear segments.[^p2]

### RANSAC (Random Sample Consensus)

Robust model fitting when many outliers are present.[^p2]

**Algorithm**:
1. Randomly select a minimal seed subset of points (e.g., 2 for line fitting)
2. Fit the model to the seed
3. Count **inliers**: points within threshold distance of the fitted model
4. If inlier count exceeds threshold: re-fit using all inliers; keep this as candidate fit
5. Repeat steps 1–4 for k iterations; return the fit with most inliers

**Number of samples k**: governed by desired confidence p (typically 0.99), fraction of inliers w, and model size n:
`k = log(1-p) / log(1 - w^n)`

**RANSAC vs Hough transform**: RANSAC is more efficient when the number of parameters is large (e.g., homography with 8 DOF); Hough is better for small models (2 parameters, low noise).[^p2]

**Applications**: image stitching, lane detection, stereo geometry estimation (fundamental matrix estimation).[^p2]

---

## Harris Corner Detection

**Motivation**: corners are repeatable and distinctive — they change in intensity in all directions (unlike edges, which change in only one direction).[^p3]

**Method**: Slide window w over the image; measure intensity change E(u,v) when shifted by [u,v]:

```
E(u,v) = Σ_{x,y} w(x,y) [I(x+u, y+v) - I(x,y)]²
```

Taylor expansion approximates this as a quadratic form:

```
E(u,v) ≈ [u, v] M [u, v]^T
where M = Σ w · [Ix², IxIy; IxIy, Iy²]
```

M is the **second moment matrix** (Harris matrix). Its eigenvalues λ₁, λ₂ characterize the local patch:
- Both large → **corner** (large response in all directions)
- One large, one small → **edge** (large response only along gradient direction)
- Both small → **flat region**[^p3]

**Corner Response Function** (avoids expensive eigenvalue computation):

```
θ = det(M) - α · trace(M)²  where α ≈ 0.04-0.06
```

High θ → corner; negative θ → edge; small |θ| → flat.[^p3]

**Rotation invariance**: M is computed from gradient magnitudes, which are rotation-invariant. Smooth M with a Gaussian before computing θ to achieve weighted accumulation:

```
M = Σ G_σ · [Ix², IxIy; IxIy, Iy²]
```

**Limitation**: Harris is not scale-invariant. If the image is resized, the same window captures different gradients, misclassifying the patch.[^p3]

---

## Scale-Invariant Keypoint Detection

### Problem

A fixed-size window misses features at other scales — a corner at one scale appears as an edge at a different scale. Need a scale-covariant detection function.[^p3]

### Difference of Gaussians (DoG)

Key insight: look for extrema in scale-space, not just spatial space.[^p3]

**Algorithm**:
1. Convolve image I with Gaussians at increasing σ values, at multiple image resolutions → Gaussian pyramid
2. Compute DoG = difference between adjacent Gaussian-blurred images at same resolution:
   `DoG(σ) = (G(kσ) - G(σ)) * I`
3. Find **local extrema** in the 3D (x, y, scale) space: a point is a keypoint if it is larger or smaller than all 26 neighbors (8 spatial + 9 above + 9 below scale)[^p3]

The DoG approximates the Laplacian of Gaussian (LoG), which is a scale-normalized second derivative. Small σ captures fine detail; large σ captures coarse structure.[^p3]

**Alternative**: Harris-Laplacian — run Harris detector at each scale level, select keypoints that also maximize the Laplacian across scales. More accurate but more expensive than DoG.[^p3]

---

## SIFT: Scale-Invariant Feature Transform

SIFT (Lowe, 2004) combines scale-invariant detection (DoG) with a rotation-invariant orientation-histogram descriptor.[^p3]

### Detection

Use DoG extrema as keypoints (see above). The scale σ at which the extremum occurs defines the characteristic scale.

### Orientation assignment

1. Smooth image at the keypoint's scale
2. Compute gradient magnitude and direction in a neighborhood
3. Build an orientation histogram (36 bins, 10° each); the dominant peak defines the keypoint orientation
4. All subsequent descriptor computation is relative to this orientation → **rotation invariance**[^p3]

### SIFT descriptor

1. Around each keypoint, define a 16×16 region aligned to the keypoint orientation
2. Divide into a 4×4 grid of cells
3. In each cell, build an 8-bin orientation histogram (weighted by gradient magnitude and Gaussian distance from keypoint center)
4. Concatenate 4×4×8 = 128 values into the descriptor vector
5. Normalize to unit length; clamp values > 0.2 (mitigates nonlinear illumination effects); re-normalize[^p3]

**Properties**: invariant to scale, rotation, and partially to illumination/viewpoint changes. Experimentally optimal at 4×4 histogram array with 8 bins.[^p3]

**Matching**: compare SIFT descriptors between images via Euclidean distance; use ratio test (Lowe's ratio) to discard ambiguous matches.

---

## HoG: Histogram of Oriented Gradients

HoG (Dalal & Triggs, 2005) extends the SIFT descriptor idea to dense image windows for **object detection**, not keypoint matching.[^p3]

**Algorithm**:
1. Divide image window into spatial cells (e.g., 8×8 pixels)
2. For each cell, build an orientation histogram: compute gradient direction and magnitude at each pixel; accumulate magnitudes into orientation bins
3. Group cells into blocks (e.g., 2×2 cells); normalize the concatenated histogram over each block (L2-Hys normalization for robustness to illumination changes)
4. Concatenate all block histograms → final HoG descriptor

**Properties**: captures local shape/appearance via edge direction statistics; not directly invariant to scale/rotation (unlike SIFT); designed for a fixed window size.

**HoG vs SIFT**:
- HoG: dense over entire image window; used for detection templates (whole objects)
- SIFT: sparse at keypoints; used for keypoint matching between images
- SIFT orientation histograms are aligned to dominant gradient; HoG are axis-aligned
- SIFT uses weighted distances; HoG uses neighborhood bins[^p3]

**Key application**: Dalal and Triggs trained a linear SVM on HoG descriptors of image windows for human detection — achieving state-of-the-art on PASCAL at the time. The HOG + SVM pipeline was the dominant detection paradigm before deep learning.[^p3]

---

## Image Filtering Foundations

Classical feature detection relies on convolution for smoothing and derivative computation.

**Convolution vs correlation**:[^p2]
- **Convolution** `(f * h)[n,m]`: kernel h is flipped before sliding over input f. Commutative.
- **Cross-correlation** `(f ⊛ h)[n,m]`: kernel h is NOT flipped. Computes similarity (correlation) between a template h and the signal f. Non-commutative.

In practice, deep learning frameworks implement cross-correlation but call it "convolution" — the distinction matters when the kernel is asymmetric. See [Convolutional Neural Networks](/ai-engineering/convolutional-neural-networks.md).

**Linear Shift-Invariant (LSI) systems**: a system is LSI if it is both linear (superposition holds) and shift-invariant (shifting input shifts output by same amount). Any LSI system is fully characterized by its **impulse response** h; its output for any input f is `f * h`.[^p2]

---

## See also

- [Convolutional Neural Networks](/ai-engineering/convolutional-neural-networks.md) — deep learned features supersede HoG/SIFT in most tasks
- [Computer Vision Tasks](/ai-engineering/computer-vision-tasks.md) — SSD object detection, semantic segmentation with U-Net
- [Deformable Parts Model](/ai-engineering/deformable-parts-model.md) — HoG-pyramid-based object detection pipeline
- [Optical Flow](/ai-engineering/optical-flow.md) — Harris corners are the preferred features to track
- [Visual Bag of Words](/ai-engineering/visual-bag-of-words.md) — SIFT features feed into BoW image retrieval

[^p2]: raw/_inbox/pdf-computer-vision-foundations-and-applications-part-02.md
[^p3]: raw/_inbox/pdf-computer-vision-foundations-and-applications-part-03.md

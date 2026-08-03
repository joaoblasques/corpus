---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-computer-vision-foundations-and-applications-part-06.md
    channel: pdf
    ingested_at: 2026-08-03
aliases:
  - optical flow
  - Lucas-Kanade
  - Horn-Schunk
  - aperture problem
  - brightness constancy
  - KLT tracker
  - Kanade-Lucas-Tomasi
  - feature tracking
  - motion estimation
  - 2D transformation
  - affine motion
  - projective transformation
confidence: 0.95
last_confirmed: 2026-08-03
tags:
  - corpus/ai-engineering
  - concept
created: 2026-08-03
updated: 2026-08-03
---

# Optical Flow

**TL;DR.** Optical flow estimates a dense 2D motion field — a vector (u,v) per pixel — between consecutive video frames. The Lucas-Kanade method solves a local least-squares system using the spatial-coherence assumption; Horn-Schunk adds a global smoothness regularizer. Both rest on three core assumptions: brightness constancy, small motion, and spatial coherence. Harris corners are the preferred features to track (KLT tracker) because the resulting least-squares system is well-conditioned at corners. Image pyramids handle large motion by coarse-to-fine estimation.

---

## Core assumptions

**Brightness constancy**: a pixel's intensity does not change between frames:
```
I(x + u(x,y), y + v(x,y), t) = I(x, y, t-1)
```
Linearizing via first-order Taylor expansion (valid when motion is small):
```
Ix·u + Iy·v + It = 0
```
where Ix, Iy are spatial gradients and It is the temporal gradient.[^p6]

**Small motion**: displacements between consecutive frames are small. Necessary for the Taylor linearization to hold. Violated when objects move fast or are close to the camera. Solution: use image pyramids.[^p6]

**Spatial coherence**: nearby pixels move together (because they usually belong to the same object). Necessary because the brightness constancy constraint provides one equation per pixel but two unknowns (u, v) — the system is under-determined.[^p6]

---

## The aperture problem

An inherent ambiguity in optical flow: when viewing a moving edge through a small window (aperture), only the component of motion perpendicular to the edge can be measured. Motion parallel to the edge is invisible.

"In the aperture problem, the line appears to have moved to the right when only in the context of the frame, but the true motion of the line was down and to the right."[^p6]

Consequence: flat regions (λ₁ and λ₂ both small) and edges (λ₁ >> λ₂) produce degenerate flow estimates. **Corners** (both λ₁ and λ₂ large) yield well-conditioned systems — which is why Harris corners are preferred for tracking.

---

## Lucas-Kanade (1981)

**Approach**: apply the spatial coherence assumption in a k×k window around each pixel. All pixels in the window share the same (u, v). For a 5×5 window, this yields 25 equations in 2 unknowns → over-constrained, solved by least squares.[^p6]

**System**: `Ad = b` where A is (k² × 2), b is (k² × 1), d = [u, v]^T.

Least-squares solution:
```
(A^T A) d = A^T b
```

Explicitly:
```
[Σ Ix²,   Σ IxIy] [u]   [-Σ IxIt]
[Σ IxIy,  Σ Iy² ] [v] = [-Σ IyIt]
```

This is the **Harris matrix** `M = A^T A`. The solution exists and is well-conditioned when M has two large eigenvalues — exactly the condition for a Harris corner.[^p6]

**Conditions for solvability**:
- A^T A must be invertible (non-degenerate patch)
- Eigenvalues λ₁, λ₂ must not be too small (not in flat/low-texture region)
- λ₁/λ₂ must not be too large (not pure edge — aperture problem)[^p6]

**Error sources**:
- Brightness constancy violated (lighting changes)
- Motion too large for Taylor linearization
- Window contains depth discontinuities (spatial coherence violated)[^p6]

### Iterative Lucas-Kanade

Higher-order accuracy via Newton's method:
1. Estimate (u, v) using the linearized system
2. Warp I(t-1) toward I(t) using estimated flow
3. Compute residual; add to (u, v)
4. Repeat until convergence[^p6]

---

## Horn-Schunk (1981)

**Formulation**: global energy minimization over the entire image:

```
E(u,v) = ∫∫ [(Ix·u + Iy·v + It)² + α²(||∇u||² + ||∇v||²)] dx dy
```

First term: brightness constancy penalty. Second term: smoothness regularizer — penalizes large spatial gradients of the flow field, encouraging nearby pixels to have similar flow. α controls the trade-off.[^p6]

**Setting gradient to zero** yields a linear system at each pixel:
```
(Ix² + α²) u + IxIy v = α²ū - IxIt
IxIy u + (Iy² + α²) v = α²v̄ - IyIt
```
where ū, v̄ are the weighted averages of u, v in a neighborhood.

**Iterative solution** (Gauss-Seidel):
```
u^(k+1) = ū^k - Ix(Ix·ū^k + Iy·v̄^k + It) / (α² + Ix² + Iy²)
v^(k+1) = v̄^k - Iy(Ix·ū^k + Iy·v̄^k + It) / (α² + Ix² + Iy²)
```
Iterate until convergence.[^p6]

**Properties vs Lucas-Kanade**:
- Horn-Schunk: global, dense, smooth flow field; fills in flat regions; aperture problem partly resolved by smoothness term
- Lucas-Kanade: local, sparse, per-patch estimate; faster but fails at flat regions and large displacements[^p6]

### Michael Black's extension

Replaces the quadratic smoothness term `||∇u||² + ||∇v||²` with a robust function that is concave far from zero — this allows **motion discontinuities** (object boundaries) while still smoothing within regions. The quadratic penalizes discontinuities too heavily, blurring motion boundaries.[^p6]

---

## Pyramidal optical flow (handling large motion)

For large inter-frame displacements, the small-motion assumption fails. Solution: image pyramid (Gaussian pyramid).[^p6]

**Algorithm**:
1. Build a Gaussian image pyramid (halve resolution at each level)
2. Estimate coarse flow at the coarsest (lowest-resolution) level
3. Warp the finer-resolution image using the upsampled coarse flow
4. Estimate the residual flow at the finer level
5. Add residual to coarse flow; continue down the pyramid

At the coarsest level, large motions in the original correspond to small motions → small-motion assumption holds. The pyramid progressively refines the estimate.

---

## Motion segmentation: common fate

Group pixels by shared motion pattern.[^p6] Formalize via affine motion:

```
u(x,y) = a1 + a2·x + a3·y
v(x,y) = a4 + a5·x + a6·y
```

For each image block, estimate the 6-parameter affine vector `a` that minimizes:

```
Σ_{(x,y) in block} (Ix·u(x,y) + Iy·v(x,y) + It)²
```

Cluster affine parameter vectors using k-means → pixels with similar affine motion form a "layer" (independently moving surface).

---

## KLT Feature Tracker (Kanade-Lucas-Tomasi)

The KLT tracker applies Lucas-Kanade iteratively to track Harris corners across many frames.[^p6]

**Algorithm**:
1. Detect Harris corners in the first frame
2. For each frame transition: solve Lucas-Kanade for translation (u,v) at each tracked corner
3. Accept the match if the patch appearance does not change too much (SSD threshold)
4. Every 10–15 frames: detect new Harris corners to replace lost tracks

**2D transformation variants**: the simple KLT uses translation. The full iterative KLT solves for more general transforms:[^p6]

| Transform | DOF | Use case |
|---|---|---|
| Translation | 2 | Fixed overhead cameras |
| Similarity (scale + rotation + translation) | 4 | Fixed cameras of sports |
| Affine | 6 | Pedestrian detection |
| Projective (homography) | 8 | Moving cameras |

For each transform, the objective minimizes `Σ [T(x) - I(W(x; p))]²` over warp parameters p, where T is the template patch. The iterative solution uses the Jacobian of the warp:

```
∆p = H^{-1} Σ_x [∇I · (∂W/∂p)]^T [T(x) - I(W(x;p))]
where H = Σ_x [∇I · (∂W/∂p)]^T [∇I · (∂W/∂p)]
```

For translation, H reduces to the Harris matrix — explaining why Harris corners are optimal features to track.[^p6]

---

## Applications

- **Autonomous vehicles**: detect motion of other cars/pedestrians relative to the camera
- **Action recognition**: flow fields encode motion patterns for classifying activities
- **Video stabilization**: estimate and compensate for camera motion
- **3D reconstruction from video**: multi-view geometry uses correspondence across frames
- **Security surveillance**: detect moving objects via flow anomalies[^p6]

---

## See also

- [Classical Feature Detection](/ai-engineering/classical-feature-detection.md) — Harris corners (the preferred features to track), SIFT, HoG
- [Computer Vision Tasks](/ai-engineering/computer-vision-tasks.md) — image classification, segmentation, detection baselines
- [Convolutional Neural Networks](/ai-engineering/convolutional-neural-networks.md) — deep learned features used in modern flow networks (FlowNet, PWC-Net)

[^p6]: raw/_inbox/pdf-computer-vision-foundations-and-applications-part-06.md

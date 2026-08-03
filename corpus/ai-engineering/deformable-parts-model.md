---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-computer-vision-foundations-and-applications-part-05.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/_inbox/pdf-computer-vision-foundations-and-applications-part-06.md
    channel: pdf
    ingested_at: 2026-08-03
aliases:
  - deformable parts model
  - DPM
  - star model
  - sliding window detector
  - HOG pyramid detector
  - feature pyramid
  - object detection pipeline
  - PASCAL VOC
  - IoU
  - precision-recall curve
  - average precision
  - Fischler Elschlager
  - Dalal Triggs
confidence: 0.93
last_confirmed: 2026-08-03
tags:
  - corpus/ai-engineering
  - concept
created: 2026-08-03
updated: 2026-08-03
---

# Deformable Parts Model (DPM)

**TL;DR.** The Deformable Parts Model (DPM) was state-of-the-art for object detection 2008–2012, before deep learning replaced it. The core idea: detect an object via a global root filter plus a set of part filters with spring-like deformation costs, all implemented as HoG template matches across a feature pyramid. Failure mode: DPM does not reason about object identity — it only matches local appearance patterns. Modern R-CNN/SSD/YOLO-family detectors supersede DPM by learning features end-to-end, but the concepts of multi-scale sliding windows, HOG features, and part-based scoring remain influential.

---

## Evaluation framework for object detection

Before describing DPM, the key evaluation concepts used to compare detectors:[^p5]

### Intersection over Union (IoU)

Compare predicted bounding box P with ground truth G:
```
IoU = |P ∩ G| / |P ∪ G|
```
Standard threshold: IoU > 0.5 → True Positive.

### Precision and Recall

- **Precision** = TP / (TP + FP): fraction of detections that are correct
- **Recall** = TP / (TP + FN): fraction of ground truth objects detected

The precision-recall curve (PR curve) sweeps the detection confidence threshold. **Average Precision (AP)** = area under the PR curve per class. **mAP** = mean AP across all classes.[^p5]

### Benchmarks

- **PASCAL VOC** (2005–2012): 20 object categories; high intra-class variability; bounding box + segmentation annotations
- **ImageNet LSVRC** (2013–): 200 object categories; much larger scale
- **COCO**: 80 categories; instance segmentation masks; stricter IoU thresholds (0.5–0.95 averaged)[^p5]

---

## Simple sliding window detector

**Approach**: treat detection as classification. Slide a fixed-size window over the image at all positions; classify each window as "object present" or "background."[^p5]

### Feature extraction: HoG descriptors

"Dalal and Triggs showed the effectiveness of using Histograms of Oriented Gradient (HOG) descriptors for human detection."[^p5] See [Classical Feature Detection](/ai-engineering/classical-feature-detection.md) for HoG details.

**Template**: average many aligned positive example windows and extract the HoG descriptor of the average → a prototypical HoG template for the object.

**Scoring**: for each window position, compute dot product of window HoG descriptor with template HoG descriptor. If score > threshold → detection.[^p5]

### Multi-scale sliding window

Objects appear at different sizes. Solution: **feature pyramid** — resize the image at multiple scales; apply the same fixed-size window template at each scale. Take the detection at the scale/position with highest score.[^p5]

**Limitation**: fixed template cannot handle intra-class shape variation (e.g., a person bending over, a car seen from an unusual angle).

---

## Deformable Parts Model

### Motivation

"The simple sliding window detector is not robust to small changes in shape... We want a new detection model that can handle these situations... detect an object by its parts instead of detecting the whole singular object."[^p5]

Early work: Fischler & Elschlager (1973) — parts of a face (eyes, nose, mouth) connected by "springs" that allow relative position to vary with an increasing deformation penalty.[^p5]

### Star model architecture

The DPM uses a **star-shaped** model (Felzenszwalb et al., 2008):
- One **root filter** F₀ — a coarse global HoG template for the entire object
- N **part filters** F₁,...,Fₙ — finer-detail HoG templates for object parts
- Each part has an **anchor position** vᵢ (expected position relative to root) and a **deformation cost** dᵢ parameterizing position penalty[^p5]

The entire model is an (n+2)-tuple: (F₀, P₁, ..., Pₙ, b) where b is a bias term, and each Pᵢ = (Fᵢ, vᵢ, dᵢ).

**Deformation cost**: for part i at position offset (dx, dy) from its anchor:
```
deformation_penalty_i = dᵢ · [dx, dy, dx², dy²]
```
The quadratic terms penalize large deviations more steeply (spring-like behavior). If dᵢ = (0,0,1,0), the penalty is the squared x-distance only.[^p5]

### Detection score

Compute scores across a HOG pyramid (same idea as the multi-scale sliding window):

```
score(position, parts) = F₀·φ(p₀,H) + Σᵢ Fᵢ·φ(pᵢ,H) - Σᵢ dᵢ·[dxᵢ, dyᵢ, dxᵢ², dyᵢ²] + b
```

where `φ(p,H)` is the HoG feature vector at position p in the HOG pyramid H.[^p5]

- The left term rewards appearance match of global and part filters
- The right term penalizes deviation of parts from their anchor positions
- High score = good appearance match with small deformation from expected layout

### Detection pipeline

1. Build HOG pyramid (HOG features at multiple image resolutions)
2. Apply root filter over the pyramid; find high-scoring locations
3. For each high-scoring root location, apply all part filters at twice the resolution of the root (parts capture finer details)
4. Compute deformation penalties for each part's actual position vs anchor
5. Compute total detection score; threshold to produce final detections[^p5][^p6]

### Multi-orientation models

Objects look different from different viewpoints. A complete DPM for cars has 8 orientations, each with its own root filter and part filters. The appropriate orientation model "fires" depending on which aspect of the car is visible.[^p6]

### DPM failure modes

"DPM assumes that these parts are related to each other because they are spatially close... when in reality, there is not one but two cars in the image providing the parts."[^p6]

Also: DPM lacks any global reasoning about what cannot be a car — it matches parts patterns but cannot rule out false positives based on missing features (e.g., a school bus roof visible above a car-shaped body).[^p6]

---

## DPM advantages and disadvantages

**Advantages**:
- Parts have intuitive semantic meaning
- Standard detection methods (HoG + linear classifier) apply per part
- Works well for specific object categories with consistent part structure
- Explicit deformation model enables robustness to pose variation[^p6]

**Disadvantages**:
- Parts must be selected manually; switching categories requires rebuilding from scratch
- Semantically motivated parts may not have simple appearance distributions
- No guarantee of completeness — important parts may be missed
- Cannot reason about what is NOT there
- Superseded by deep learning detectors (R-CNN 2014, SSD 2015, YOLO 2015) which learn both features and spatial relationships end-to-end[^p6]

---

## Relationship to modern detection

| Method | Era | Feature | Spatial model |
|---|---|---|---|
| DPM (Felzenszwalb et al.) | 2008–2012 | HoG (hand-crafted) | Part + spring deformation |
| R-CNN (Girshick et al.) | 2014 | CNN (learned) | None (region proposals) |
| SSD (Liu et al.) | 2015 | CNN (learned) | Multi-scale anchor boxes |
| YOLO (Redmon et al.) | 2015+ | CNN (learned) | Grid-based anchors |

DPM's multi-scale pyramid idea (feature pyramid) persists in modern **Feature Pyramid Networks (FPN)** used in Faster R-CNN and RetinaNet. The notion of explicit spatial structure for parts re-emerges in **pose estimation** architectures (stacked hourglass networks, OpenPose).

---

## See also

- [Classical Feature Detection](/ai-engineering/classical-feature-detection.md) — HoG features used in DPM; Harris corners
- [Computer Vision Tasks](/ai-engineering/computer-vision-tasks.md) — SSD, U-Net, CLIP — deep learning successors
- [Visual Bag of Words](/ai-engineering/visual-bag-of-words.md) — alternative classical recognition approach
- [Convolutional Neural Networks](/ai-engineering/convolutional-neural-networks.md) — deep learned features replacing HoG in modern detectors

[^p5]: raw/_inbox/pdf-computer-vision-foundations-and-applications-part-05.md
[^p6]: raw/_inbox/pdf-computer-vision-foundations-and-applications-part-06.md

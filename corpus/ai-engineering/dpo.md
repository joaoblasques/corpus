---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/web-direct-preference-optimization-beyond-chatbots-bc0be78c.md
    channel: web
    ingested_at: 2026-07-04
aliases:
  - Direct Preference Optimization
  - DPO
  - preference optimization
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-04
updated: 2026-07-04
---

# Direct Preference Optimization (DPO)

**TL;DR.** DPO is a fine-tuning technique applied after supervised fine-tuning (SFT) that trains a model using explicit *preference pairs* — a chosen output and a rejected output — to directly optimize away failure modes that SFT cannot reach [^src1]. Published applications go far beyond chatbot alignment: DPO has been demonstrated as a targeted mitigation tool for **text degeneration** (repetition loops) in specialized OCR models [^src1].

## How DPO differs from SFT

SFT optimizes token-by-token: each prediction is evaluated in isolation. A **repetition loop** is never penalized as a completion-level failure because SFT has no term that penalizes loops — the training objective simply maximizes the likelihood of observed sequences [^src1].

DPO inverts this logic: the training signal is the *full output* (chosen or rejected). A degenerated completion can be explicitly labeled as the wrong outcome, not just a sequence of locally probable tokens [^src1].

### Why text degeneration is hard to fix with SFT alone

"When a training objective maximizes the likelihood of observed sequences, it concentrates probability mass in the regions of distribution space those sequences occupy. A model that enters one of those high-probability attractor regions during inference assigns elevated probability to the same token at the next step — which increases the probability further, which sustains the loop until the sequence hits the maximum token limit." [^src1]

Inference-layer interventions (repetition penalties, temperature, early-abort) treat the symptom; DPO attacks the distribution that produces it [^src1].

## Constructing DPO training pairs without human labels

A key insight from the DharmaOCR case study: **the model's own failures become the training signal** [^src1].

1. Run SFT-fine-tuned model on training documents
2. Collect outputs where the model *succeeded* (correct transcription) → **chosen**
3. Collect outputs where the model *failed* (degeneration loop) → **rejected**
4. Train DPO on these pairs, without any human annotation

This approach works for any task with an objective success/failure criterion (not just alignment, where human preference judgments are needed) [^src1].

## Empirical results (DharmaOCR, OCR degeneration)

Applied to a structured OCR task (Brazilian Portuguese documents) across multiple model families [^src1]:

| Outcome | Result |
|---|---|
| Degeneration rate reduced | Every model family tested — no exceptions |
| Average reduction vs. SFT baseline | 59.4% |
| Best case (Nanonets-OCR2–3B) | 87.6% (1.61% → 0.20%) |

"The direction is invariant; only the magnitude varies." [^src1]

## When to use DPO

- After SFT, when a specific failure mode persists that SFT cannot eliminate
- When there is a clear objective preference signal (correct vs. incorrect output), not just subjective human preference
- When inference-layer workarounds (repetition penalties etc.) are insufficient
- As a second-stage fine-tuning pass on the same data the SFT used

## Related

- [Unsloth](/ai-engineering/unsloth.md) — DPO training toolkit (fast RLHF/DPO on consumer hardware)
- [AI Fundamentals](/ai-engineering/ai-fundamentals.md) — RLHF and alignment training context
- [AI Engineering hub](/ai-engineering/README.md)

---

[^src1]: [Direct Preference Optimization Beyond Chatbots](../../raw/_inbox/web-direct-preference-optimization-beyond-chatbots-bc0be78c.md) — Hugging Face blog, DharmaAI, 2026-06

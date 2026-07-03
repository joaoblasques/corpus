---
type: concept
domain: mlops
status: draft
sources:
  - path: raw/notes/00-03-gpu-setup-and-cloud-kb.md
    channel: notes
    ingested_at: 2026-06-09
aliases:
  - cloud GPU
  - GPU rental
  - Colab
  - RunPod
  - Lambda Labs
  - Vast.ai
tags:
  - corpus/mlops
  - concept
created: 2026-06-09
updated: 2026-06-09
---

# Cloud GPU Providers

**TL;DR**: When local hardware lacks a usable GPU (see [GPU & VRAM](/mlops/gpu-and-vram.md)), compute moves to the cloud. Google Colab (free T4) is the zero-setup default for early work; cost and reliability needs escalate you to RunPod, Lambda, or Vast.ai as workloads grow [^src1].

## Provider comparison (May 2026 snapshot)

| Provider | Cheap tier | Best for |
|---|---|---|
| Colab | Free T4; $9.99 / 100 CU (~57 hr) | zero setup, early phases |
| RunPod | RTX 4090 $0.34–0.69/hr; H100 spot $1.49/hr | beyond Colab limits |
| Lambda | A100 $1.29/hr | long runs needing reliability |
| Vast.ai | RTX 4090 from $0.29/hr | cost-sensitive, handle failures yourself |

> Prices drift — re-verify before spending [^src1].

A free Colab T4 offers 15.6 GB VRAM (compute capability 7.5) and was observed at ~20× CPU speedup on a 4000×4000 matmul [^src1].

## Operational escalation pattern

The course's decision ladder [^src1]:

- **Early/CPU-friendly work** → free Colab; lessons fit under the 90-min idle / 12-hr session caps.
- **Fine-tuning** → Colab pay-as-you-go ($9.99 ≈ 57 hr T4) or RunPod for cheaper A100 time.
- **End-of-course / production** → Lambda for reliability on long runs; Vast.ai for cost optimization when failures are tolerable.

The trade-off axis: **reliability (Lambda) vs cost (Vast.ai)**, with Colab/RunPod in between by convenience [^src1].

## See also

- [GPU & VRAM](/mlops/gpu-and-vram.md) — the VRAM math that sizes which tier you need
- [MLOps hub](/mlops/README.md)

---

[^src1]: [AI Engineering from Scratch — Phase 00 / 03 GPU Setup & Cloud](../../raw/notes/00-03-gpu-setup-and-cloud-kb.md)

---
type: concept
domain: mlops
status: draft
sources:
  - path: raw/notes/00-03-gpu-setup-and-cloud-kb.md
    channel: notes
    ingested_at: 2026-06-09
aliases:
  - GPU
  - VRAM
  - GPU memory
  - VRAM math
tags:
  - corpus/mlops
  - concept
created: 2026-06-09
updated: 2026-06-09
---

# GPU & VRAM

**TL;DR**: GPUs win for ML because thousands of cores do matrix multiplication in parallel — the operation that dominates neural-net training and inference. **VRAM, not system RAM, is the hard ceiling**: model weights, gradients, optimizer state, and activations all live in VRAM. Training needs ~6× more VRAM than inference; LoRA collapses that gap by training a tiny adapter instead of the full model [^src1].

## VRAM math

- **fp16 rule of thumb**: each parameter ≈ 2 bytes. So 8B params at fp16 ≈ 16 GB. It inverts cleanly: 24 GB VRAM ≈ 12B params max [^src1].
- **Training ≈ 6× inference**: weights (1×) + gradients (1×) + Adam optimizer state in fp32 (~4×) + activations. Example: Llama 3 8B ≈ 16 GB to infer, but ~96 GB to train naively [^src1].
- **LoRA bridges the gap**: freeze the base model, train a small adapter (a few million params). Gradients and optimizer state shrink to adapter size → 10–20× less VRAM. Llama 3 8B with LoRA ≈ 21 GB, tractable on a T4 with extra tricks [^src1]. *(LoRA is a fine-tuning technique covered in depth in a later course phase; forward reference.)*

## Local accelerator availability

PyTorch acceleration requires matching hardware [^src1]:

| Backend | Requires | Example failure |
|---|---|---|
| CUDA | NVIDIA GPU | absent on any Mac |
| MPS | Apple Silicon | absent on Intel Macs |
| CPU | always available | usable for dev + small experiments, not GPU-bound training |

On an Intel Mac, neither CUDA nor MPS is available, so all GPU work moves to the cloud — see [Cloud GPU Providers](/mlops/cloud-gpu-providers.md) [^src1].

## Timing gotcha

GPU ops are **asynchronous** — Python returns before the GPU finishes. Forgetting `torch.cuda.synchronize()` before stopping a timer measures dispatch overhead, not actual work [^src1].

## See also

- [Cloud GPU Providers](/mlops/cloud-gpu-providers.md) — where to rent VRAM when local hardware can't
- [Dev Environment Stack](/mlops/dev-environment-stack.md) — GPU as the optional Layer-1 capability
- [MLOps hub](/mlops/README.md)

---

[^src1]: [AI Engineering from Scratch — Phase 00 / 03 GPU Setup & Cloud](../../raw/notes/00-03-gpu-setup-and-cloud-kb.md)

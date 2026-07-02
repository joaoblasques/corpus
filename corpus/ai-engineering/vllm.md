---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-minimax-m3-in-vllm-day-0-serving-for-1m-token-multimodal-rea-5d5564f8.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/web/web-diffusiongemma-the-first-diffusion-llm-dllm-natively-support-646d34df.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/web/web-announcing-vime-a-simple-stable-and-efficient-rl-framework-f-9a392163.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/web/web-announcing-day-0-support-for-nvidia-nemotron-3-ultra-on-vllm-bc7c306b.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/web/web-fast-efficient-llm-inference-with-vllm-a-new-course-with-dee-f75c7aa9.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/web/web-vllm-on-the-dgx-spark-architecture-configuration-and-local-e-543e2b72.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/web/web-accelerating-laguna-xs-2-inference-with-vllm-speculators-and-afda11cd.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/web/web-native-rl-apis-in-vllm-a83f1153.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/web/web-vllm-x-novita-ai-pegaflow-for-production-grade-external-kv-c-4b8a8880.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/web/web-elastic-expert-parallelism-in-vllm-e7f766b6.md
    channel: web
    ingested_at: 2026-07-02
aliases:
  - vLLM
  - vllm
tags:
  - corpus/ai-engineering
  - entity
created: 2026-07-02
updated: 2026-07-02
---

# vLLM

**TL;DR.** vLLM is an open-source LLM inference-serving engine and ecosystem. Beyond the core serving runtime (scheduler, paged KV cache, prefix caching, chunked prefill, speculative decoding), the vLLM project has grown a family of adjacent tools: [[ai-engineering/vllm-semantic-router|vLLM Semantic Router]] for request-level model routing, and [[ai-engineering/vime|vime]] for RL post-training. vLLM ships day-0 support for major new model architectures, including sparse-attention long-context models ([[ai-engineering/minimax-m3|MiniMax M3]]), diffusion language models ([[ai-engineering/diffusiongemma|DiffusionGemma]]), a hybrid Transformer-Mamba agentic reasoning model ([[ai-engineering/nemotron-3-ultra|Nemotron 3 Ultra]]), and an agentic-coding MoE model with a novel speculative decoder ([[ai-engineering/laguna-xs2|Laguna XS.2]]) [^src1][^src2][^src3][^src4][^src7].

## Serving engine internals (as exercised by day-0 model integrations)

- **Scheduler + paged KV cache** — manages per-request cache blocks; extended via hooks (e.g. `ModelState`) rather than forked for new model architectures [^src2].
- **Prefix caching** — reuses cached KV for shared prompt prefixes across requests [^src1][^src2].
- **Chunked prefill** — splits very long prompts into chunks so one giant prefill doesn't monopolize the engine [^src1].
- **Speculative decoding data path** — a mature subsystem (draft tokens proposed, verified in a batch, accepted/rejected) that other features can be built on top of. [[ai-engineering/diffusiongemma|DiffusionGemma]]'s diffusion denoising loop reuses this path by treating each denoising step's canvas as a set of draft tokens that are fully accepted or rejected together [^src2]. [[ai-engineering/minimax-m3|MiniMax M3]] uses EAGLE3 speculative decoding for latency reduction [^src1].
- **Tensor/expert parallelism (TP/EP)** — splits attention, projections, and MoE experts across GPUs [^src1].
- **Multi-backend hardware support** — NVIDIA (H100/H200/GB200/B300), AMD ROCm (MI300/MI350), with backend-specific attention kernel selection (e.g. FlashAttention/FlashInfer on NVIDIA vs. Triton/AITER on AMD) [^src1][^src2].

## ModelState abstraction (model runner v2)

Introduced to support [[ai-engineering/diffusiongemma|DiffusionGemma]], `ModelState` lets a model define custom input preparation and per-request state without forking the model runner [^src2]:

| Hook | Purpose |
|---|---|
| `prepare_inputs()` | Build/modify per-request input embeddings (e.g. apply self-conditioning) |
| `prepare_attn()` | Set per-request attention metadata (e.g. causal vs. bidirectional) |
| `custom_sampler()` | Swap in a model-specific sampler |
| `add_request()`/`remove_request()` | Initialize/tear down per-request custom state |

A model self-registers its `ModelState` via `get_model_state_cls()` on the model class — no changes to the shared scheduler, model runner, or other infrastructure are required. The vLLM team frames this as a blueprint for adding future non-autoregressive architectures (e.g. more diffusion LLMs) [^src2].

## Day-0 model support pattern

vLLM's "day-0" releases pair a new open-weight model with same-day serving support, including: architecture-specific attention kernels, tool-call/reasoning-output parsers, speculative decoding draft models, quantized checkpoint validation, and deployment recipes across accelerators. Both [[ai-engineering/minimax-m3|MiniMax M3]] (sparse attention, 1M-token context) and [[ai-engineering/diffusiongemma|DiffusionGemma]] (diffusion decoding) required non-trivial engine extensions rather than being drop-in autoregressive models [^src1][^src2].

## Ecosystem projects

- [[ai-engineering/vllm-semantic-router|vLLM Semantic Router]] — request routing control plane (signals → decisions → model selection) sitting in front of vLLM and other backends.
- [[ai-engineering/vime|vime]] — RL post-training framework pairing Megatron training with vLLM as the rollout/inference backend.

## Local single-GPU deployment: DGX Spark

vLLM also targets **NVIDIA DGX Spark**, a desk-side GB10 Grace Blackwell system for local inference, bridging laptop-scale development and datacenter GPU serving [^src5]. Spark's architecture reshapes the usual serving-flag defaults:

- **Unified CPU+GPU memory pool (128 GB)** — CPU, GPU, OS, container runtime, model weights, and KV cache all share one pool, so `--gpu-memory-utilization` must leave headroom for the rest of the system rather than assuming a dedicated GPU-memory budget [^src5].
- **`--max-num-seqs` should stay low** (e.g. `4`) — Spark suits small-batch/single-user inference, not high-concurrency serving; above ~4 concurrent decode streams the per-token bandwidth tax outweighs continuous-batching gains and TTFT spikes [^src5].
- **NVFP4 MoE models with ~10–15B active parameters are a strong fit** — active parameter count (not total parameters) bounds decode speed; unified memory makes it practical to load NVFP4 models up to ~200B total parameters on a single Spark [^src5]. See [[ai-engineering/quantization|Quantization]].
- **sm_121-specific validation** — Spark's Blackwell-consumer silicon needs vLLM builds/images validated specifically for `sm_121`; configs tuned on datacenter GPUs are a compatibility checklist, not a performance expectation, when ported to Spark [^src5].
- **Cold-start / JIT warmup** — first request after `vllm serve` boots triggers Inductor/FlashInfer JIT codegen (~25s in one Nemotron-3-Super setup); production setups should fire a warmup ping at startup rather than exposing this latency to the first real user request [^src5].
- **Measured example** (Nemotron-3-Super-120B-A12B-NVFP4 on one Spark): decode throughput held in a narrow 22.7–23.7 tok/s band across scenarios regardless of prompt length; prefill scaled from ~140 tok/s (58-token prompt) to ~1,884 tok/s (7,234-token prompt) as prompt length amortized per-request overhead [^src5]. Recipe-specific numbers, not a universal DGX Spark ceiling.

## Native RL post-training APIs

vLLM introduces standardized weight-syncing and pause/resume APIs so RL frameworks no longer need custom worker extensions, addressing duplicated effort and version-locked implementations across frameworks [^src8].

- **Weight transfer**: four-phase pluggable-backend API — `init_weight_transfer_engine` (once, before training), `start_weight_update` (per step, prepares workers), `update_weights` (invokable multiple times for chunked transfers), `finish_weight_update` (post-processing, e.g. quantization). Backends: NCCL broadcast (cross-GPU) and CUDA IPC (same-device); both support packed-tensor transfer to cut serialization overhead [^src8].
- **Pause/resume for async RL**: `pause_generation`/`resume_generation` (also `POST /pause`/`/resume`) gained a third **keep** mode alongside existing `abort` and `wait` modes — pauses in-flight requests without discarding them (scheduler stops, state preserved), the only mode that keeps client retries unnecessary *and* allows async weight updates [^src8].
- **DPEP deadlock fix**: async RL in data-parallel + expert-parallel (DPEP) deployments previously deadlocked because pause state lived in the `AsyncLLM` entrypoint while DP-wave coordination happened between `EngineCore` and the `DPCoordinator`. Fixed by (1) moving pause logic into `EngineCore`/the scheduler, and (2) a two-phase pause: local pause (an engine stops scheduling but still answers `START_DP_WAVE`) then global pause (all ranks confirm local-pause via periodic all-reduce before fully stopping) [^src8].
- **Validated at scale**: the Prime-RL team ran fully-async RL on zai-org/GLM-5.1-FP8 across a P/D-disaggregated, DPEP32, 16×8×H200-node deployment (32 GPUs total) with 1TB/node CPU KV-cache offload and cache-aware sticky routing via vllm-router; stable over 100+ training steps with a growing eval curve [^src8]. See also [[ai-engineering/vime|vime]], the vLLM-ecosystem RL post-training framework this API standardizes for.

## External KV cache: PegaFlow (with Novita AI)

**PegaFlow** moves KV cache out of the vLLM worker process into a standalone Rust daemon, integrated via vLLM's existing `kv_transfer_config` external-connector path (no vLLM source changes or fork required) [^src9].

- **Architecture**: one PegaFlow server per host owns the KV pool, SSD cache, RDMA resources, and indexing state; vLLM workers connect via CUDA IPC (data path) and gRPC (local control path). A three-level hierarchy spans pinned local DRAM (L1) → RDMA-accessible remote DRAM (L2) → local SSD via `io_uring` (L3) [^src9].
- **Faster restarts**: with a pre-warmed 500 GiB host KV pool already owned by PegaFlow, vLLM reached ready state in 33.2s vs. 71.4s when vLLM itself owned the pool — a 2.15x startup speedup (measured on 8×RTX 5090, Qwen3-8B TP8, dummy weights/eager mode) [^src9].
- **Shared-pool throughput**: eight Qwen3-8B instances sharing one 500 GiB PegaFlow pool hit 11.97 req/s vs. 7.68 req/s for eight isolated 62.5 GiB pools — 56% higher throughput, 36% lower mean TTFT, 4.4x higher cache-hit rate [^src9].
- **MLA dedup**: for DeepSeek-V3.2 MLA with TP8, storing the logical KV once (vs. once per TP rank) delivered 72% higher throughput and a hit rate of 97.23% vs. 65.18% [^src9].
- **Cross-node RDMA**: sustained 194 GB/s average remote-read throughput (250 GB/s P99) for large (≥1GiB) prefix pulls over 8×400Gbps RDMA NICs/node — fast enough that a 24 GiB remote KV segment (~100ms to fetch) can substitute for seconds of prefill recomputation [^src9].
- Ships as `novitalabs/pegaflow` on GitHub; requires `vllm>=0.20.0` [^src9].

## Elastic Expert Parallelism (Elastic EP)

vLLM's expert-parallel (EP) group size was previously fixed at deployment start; **Elastic EP** lets a running MoE deployment reconfigure its data-parallel (DP) worker count at runtime via `POST /scale_elastic_ep`, redistributing experts with minimal serving interruption [^src10]. See [[ai-engineering/mixture-of-experts|Mixture of Experts]] for the EP/DP-attention background this builds on.

- **Scale-up flow**: new DP ranks initialize with placeholder weights; existing ranks build *standby* communication groups (via `StatelessGroupCoordinator`, independent of PyTorch's global `WORLD` state) spanning the target rank set while the old topology keeps serving; non-expert weights transfer over standby groups; then all ranks execute a coordinated **switch** (release CUDA graphs, promote standby → active groups, destroy old groups, re-warm); only after the switch does an EPLB reshuffle move expert weights onto the new ranks [^src10].
- **Scale-down** runs EPLB reshuffle *first* (departing ranks' expert weights must migrate off before those ranks are removed), then follows the same teardown pattern [^src10].
- **Cross-rank coordination**: because DP engine cores run asynchronously, a two-stage barrier (timeout-based local barrier → untimed global barrier) prevents a race where some ranks proceed to reconfiguration while others are mid-forward-pass, which would otherwise deadlock the group [^src10].
- **Fault-tolerance building block**: the same scale-down/scale-up path is the mechanism for removing a failed rank, redistributing its experts, and later adding replacement capacity — part of vLLM's broader fault-tolerance RFC (#30112) [^src10]. **NIXL EP** (an alternate EP communication backend) makes rank add/remove incremental via `connect_ranks()`/`disconnect_ranks()` instead of full connection teardown, and adds EP-side failure detection/recovery [^src10].
- **Current scope limits**: `tensor_parallel_size=1` only, `api_server_count=1` only, no DBO or MoE draft/drafter models yet, and scaling depends on the Ray DP backend [^src10].

## Learning resource: DeepLearning.AI course

Red Hat and Andrew Ng's DeepLearning.AI published **"Fast & Efficient LLM Inference with vLLM"** (Cedric Clyburn, Red Hat; ~1.5 hours, 9 lessons, 3 hands-on labs), covering the full compress → serve → benchmark lifecycle: quantizing a model with LLM Compressor, serving it with vLLM (observing continuous batching and prefix caching via live metrics), and benchmarking throughput/latency with GuideLLM plus quality validation with lm-eval [^src6].

## Related

- [[ai-engineering/mixture-of-experts|Mixture of Experts]] — MoE execution is a first-class vLLM serving concern (expert parallelism, Elastic EP runtime scaling, quantized MoE backends)
- [[ai-engineering/quantization|Quantization]] — AutoRound/NVFP4/LLM Compressor checkpoint quantization, used across DGX Spark, Nemotron 3 Ultra, and Laguna XS.2 deployments
- [[ai-engineering/nemotron-3-ultra|Nemotron 3 Ultra]] — hybrid Transformer-Mamba MoE agentic reasoning model with vLLM day-0 support
- [[ai-engineering/laguna-xs2|Laguna XS.2]] — Poolside's agentic-coding MoE model with a DFlash speculative decoder
- [[ai-engineering/speculative-decoding|Speculative Decoding]] — draft/verify latency-reduction technique underlying vLLM's spec-decode data path (Eagle 3/3.1, DFlash)
- [[ai-engineering/vime|vime]] — RL post-training framework consuming vLLM's native weight-sync/pause-resume RL APIs
- [[ai-engineering/vllm-semantic-router|vLLM Semantic Router]] — request-routing control plane sitting in front of vLLM
- [[ai-engineering/ollama|Ollama]] — contrasting local-first single-user serving tool vs. vLLM's production/datacenter serving focus
- [[ai-engineering/README|AI Engineering hub]]

---

[^src1]: [MiniMax M3 in vLLM: Day-0 Serving for 1M-Token Multimodal Reasoning](../../raw/web/web-minimax-m3-in-vllm-day-0-serving-for-1m-token-multimodal-rea-5d5564f8.md) — vLLM blog, 2026-06-12
[^src2]: [DiffusionGemma: The First Diffusion LLM (dLLM) Natively Supported in vLLM](../../raw/web/web-diffusiongemma-the-first-diffusion-llm-dllm-natively-support-646d34df.md) — vLLM blog, 2026-06-10
[^src3]: [Announcing vime: A Simple, Stable, and Efficient RL Framework for LLMs](../../raw/web/web-announcing-vime-a-simple-stable-and-efficient-rl-framework-f-9a392163.md) — vLLM blog, 2026-06-09
[^src4]: [Announcing Day-0 Support for NVIDIA Nemotron 3 Ultra on vLLM](../../raw/web/web-announcing-day-0-support-for-nvidia-nemotron-3-ultra-on-vllm-bc7c306b.md) — vLLM blog, 2026-06-04
[^src5]: [vLLM on the DGX Spark: Architecture, Configuration, and Local Evaluation](../../raw/web/web-vllm-on-the-dgx-spark-architecture-configuration-and-local-e-543e2b72.md) — vLLM blog / Inferact, 2026-06-01
[^src6]: [Fast & Efficient LLM Inference with vLLM: A New Course with DeepLearning.AI](../../raw/web/web-fast-efficient-llm-inference-with-vllm-a-new-course-with-dee-f75c7aa9.md) — vLLM blog, 2026-06-03
[^src7]: [Accelerating Laguna XS.2 Inference with vLLM, Speculators, and LLM Compressor](../../raw/web/web-accelerating-laguna-xs-2-inference-with-vllm-speculators-and-afda11cd.md) — vLLM blog, 2026-05-28

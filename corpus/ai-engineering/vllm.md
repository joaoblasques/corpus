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
  - path: raw/web/web-announcing-verl-omni-easy-fast-and-stable-rl-training-for-di-2040adf3.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/web/web-vllm-tops-the-artificial-analysis-leaderboard-762bd790.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/web/web-serving-agentic-workloads-at-scale-with-vllm-x-mooncake-78c3044b.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/web/web-run-highly-efficient-multimodal-agentic-ai-with-nvidia-nemot-b0ef6e3c.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/web/web-run-a-vllm-server-on-hf-jobs-in-one-command-7f1a19cb.md
    channel: web
    ingested_at: 2026-07-03
aliases:
  - vLLM
  - vllm
tags:
  - corpus/ai-engineering
  - entity
created: 2026-07-02
updated: 2026-07-03
---

# vLLM

**TL;DR.** vLLM is an open-source LLM inference-serving engine and ecosystem. Beyond the core serving runtime (scheduler, paged KV cache, prefix caching, chunked prefill, speculative decoding), the vLLM project has grown a family of adjacent tools: [vLLM Semantic Router](/ai-engineering/vllm-semantic-router.md) for request-level model routing, and [vime](/ai-engineering/vime.md) for RL post-training. vLLM ships day-0 support for major new model architectures, including sparse-attention long-context models ([MiniMax M3](/ai-engineering/minimax-m3.md)), diffusion language models ([DiffusionGemma](/ai-engineering/diffusiongemma.md)), a hybrid Transformer-Mamba agentic reasoning model ([Nemotron 3 Ultra](/ai-engineering/nemotron-3-ultra.md)), and an agentic-coding MoE model with a novel speculative decoder ([Laguna XS.2](/ai-engineering/laguna-xs2.md)) [^src1][^src2][^src3][^src4][^src7].

## Serving engine internals (as exercised by day-0 model integrations)

- **Scheduler + paged KV cache** — manages per-request cache blocks; extended via hooks (e.g. `ModelState`) rather than forked for new model architectures [^src2].
- **Prefix caching** — reuses cached KV for shared prompt prefixes across requests [^src1][^src2].
- **Chunked prefill** — splits very long prompts into chunks so one giant prefill doesn't monopolize the engine [^src1].
- **Speculative decoding data path** — a mature subsystem (draft tokens proposed, verified in a batch, accepted/rejected) that other features can be built on top of. [DiffusionGemma](/ai-engineering/diffusiongemma.md)'s diffusion denoising loop reuses this path by treating each denoising step's canvas as a set of draft tokens that are fully accepted or rejected together [^src2]. [MiniMax M3](/ai-engineering/minimax-m3.md) uses EAGLE3 speculative decoding for latency reduction [^src1].
- **Tensor/expert parallelism (TP/EP)** — splits attention, projections, and MoE experts across GPUs [^src1].
- **Multi-backend hardware support** — NVIDIA (H100/H200/GB200/B300), AMD ROCm (MI300/MI350), with backend-specific attention kernel selection (e.g. FlashAttention/FlashInfer on NVIDIA vs. Triton/AITER on AMD) [^src1][^src2].

## ModelState abstraction (model runner v2)

Introduced to support [DiffusionGemma](/ai-engineering/diffusiongemma.md), `ModelState` lets a model define custom input preparation and per-request state without forking the model runner [^src2]:

| Hook | Purpose |
|---|---|
| `prepare_inputs()` | Build/modify per-request input embeddings (e.g. apply self-conditioning) |
| `prepare_attn()` | Set per-request attention metadata (e.g. causal vs. bidirectional) |
| `custom_sampler()` | Swap in a model-specific sampler |
| `add_request()`/`remove_request()` | Initialize/tear down per-request custom state |

A model self-registers its `ModelState` via `get_model_state_cls()` on the model class — no changes to the shared scheduler, model runner, or other infrastructure are required. The vLLM team frames this as a blueprint for adding future non-autoregressive architectures (e.g. more diffusion LLMs) [^src2].

## Day-0 model support pattern

vLLM's "day-0" releases pair a new open-weight model with same-day serving support, including: architecture-specific attention kernels, tool-call/reasoning-output parsers, speculative decoding draft models, quantized checkpoint validation, and deployment recipes across accelerators. Both [MiniMax M3](/ai-engineering/minimax-m3.md) (sparse attention, 1M-token context) and [DiffusionGemma](/ai-engineering/diffusiongemma.md) (diffusion decoding) required non-trivial engine extensions rather than being drop-in autoregressive models [^src1][^src2].

## Ecosystem projects

- [vLLM Semantic Router](/ai-engineering/vllm-semantic-router.md) — request routing control plane (signals → decisions → model selection) sitting in front of vLLM and other backends.
- [vime](/ai-engineering/vime.md) — RL post-training framework pairing Megatron training with vLLM as the rollout/inference backend.

## Local single-GPU deployment: DGX Spark

vLLM also targets **NVIDIA DGX Spark**, a desk-side GB10 Grace Blackwell system for local inference, bridging laptop-scale development and datacenter GPU serving [^src5]. Spark's architecture reshapes the usual serving-flag defaults:

- **Unified CPU+GPU memory pool (128 GB)** — CPU, GPU, OS, container runtime, model weights, and KV cache all share one pool, so `--gpu-memory-utilization` must leave headroom for the rest of the system rather than assuming a dedicated GPU-memory budget [^src5].
- **`--max-num-seqs` should stay low** (e.g. `4`) — Spark suits small-batch/single-user inference, not high-concurrency serving; above ~4 concurrent decode streams the per-token bandwidth tax outweighs continuous-batching gains and TTFT spikes [^src5].
- **NVFP4 MoE models with ~10–15B active parameters are a strong fit** — active parameter count (not total parameters) bounds decode speed; unified memory makes it practical to load NVFP4 models up to ~200B total parameters on a single Spark [^src5]. See [Quantization](/ai-engineering/quantization.md).
- **sm_121-specific validation** — Spark's Blackwell-consumer silicon needs vLLM builds/images validated specifically for `sm_121`; configs tuned on datacenter GPUs are a compatibility checklist, not a performance expectation, when ported to Spark [^src5].
- **Cold-start / JIT warmup** — first request after `vllm serve` boots triggers Inductor/FlashInfer JIT codegen (~25s in one Nemotron-3-Super setup); production setups should fire a warmup ping at startup rather than exposing this latency to the first real user request [^src5].
- **Measured example** (Nemotron-3-Super-120B-A12B-NVFP4 on one Spark): decode throughput held in a narrow 22.7–23.7 tok/s band across scenarios regardless of prompt length; prefill scaled from ~140 tok/s (58-token prompt) to ~1,884 tok/s (7,234-token prompt) as prompt length amortized per-request overhead [^src5]. Recipe-specific numbers, not a universal DGX Spark ceiling.

## Native RL post-training APIs

vLLM introduces standardized weight-syncing and pause/resume APIs so RL frameworks no longer need custom worker extensions, addressing duplicated effort and version-locked implementations across frameworks [^src8].

- **Weight transfer**: four-phase pluggable-backend API — `init_weight_transfer_engine` (once, before training), `start_weight_update` (per step, prepares workers), `update_weights` (invokable multiple times for chunked transfers), `finish_weight_update` (post-processing, e.g. quantization). Backends: NCCL broadcast (cross-GPU) and CUDA IPC (same-device); both support packed-tensor transfer to cut serialization overhead [^src8].
- **Pause/resume for async RL**: `pause_generation`/`resume_generation` (also `POST /pause`/`/resume`) gained a third **keep** mode alongside existing `abort` and `wait` modes — pauses in-flight requests without discarding them (scheduler stops, state preserved), the only mode that keeps client retries unnecessary *and* allows async weight updates [^src8].
- **DPEP deadlock fix**: async RL in data-parallel + expert-parallel (DPEP) deployments previously deadlocked because pause state lived in the `AsyncLLM` entrypoint while DP-wave coordination happened between `EngineCore` and the `DPCoordinator`. Fixed by (1) moving pause logic into `EngineCore`/the scheduler, and (2) a two-phase pause: local pause (an engine stops scheduling but still answers `START_DP_WAVE`) then global pause (all ranks confirm local-pause via periodic all-reduce before fully stopping) [^src8].
- **Validated at scale**: the Prime-RL team ran fully-async RL on zai-org/GLM-5.1-FP8 across a P/D-disaggregated, DPEP32, 16×8×H200-node deployment (32 GPUs total) with 1TB/node CPU KV-cache offload and cache-aware sticky routing via vllm-router; stable over 100+ training steps with a growing eval curve [^src8]. See also [vime](/ai-engineering/vime.md), the vLLM-ecosystem RL post-training framework this API standardizes for.

## External KV cache: PegaFlow (with Novita AI)

**PegaFlow** moves KV cache out of the vLLM worker process into a standalone Rust daemon, integrated via vLLM's existing `kv_transfer_config` external-connector path (no vLLM source changes or fork required) [^src9].

- **Architecture**: one PegaFlow server per host owns the KV pool, SSD cache, RDMA resources, and indexing state; vLLM workers connect via CUDA IPC (data path) and gRPC (local control path). A three-level hierarchy spans pinned local DRAM (L1) → RDMA-accessible remote DRAM (L2) → local SSD via `io_uring` (L3) [^src9].
- **Faster restarts**: with a pre-warmed 500 GiB host KV pool already owned by PegaFlow, vLLM reached ready state in 33.2s vs. 71.4s when vLLM itself owned the pool — a 2.15x startup speedup (measured on 8×RTX 5090, Qwen3-8B TP8, dummy weights/eager mode) [^src9].
- **Shared-pool throughput**: eight Qwen3-8B instances sharing one 500 GiB PegaFlow pool hit 11.97 req/s vs. 7.68 req/s for eight isolated 62.5 GiB pools — 56% higher throughput, 36% lower mean TTFT, 4.4x higher cache-hit rate [^src9].
- **MLA dedup**: for DeepSeek-V3.2 MLA with TP8, storing the logical KV once (vs. once per TP rank) delivered 72% higher throughput and a hit rate of 97.23% vs. 65.18% [^src9].
- **Cross-node RDMA**: sustained 194 GB/s average remote-read throughput (250 GB/s P99) for large (≥1GiB) prefix pulls over 8×400Gbps RDMA NICs/node — fast enough that a 24 GiB remote KV segment (~100ms to fetch) can substitute for seconds of prefill recomputation [^src9].
- Ships as `novitalabs/pegaflow` on GitHub; requires `vllm>=0.20.0` [^src9].

## Elastic Expert Parallelism (Elastic EP)

vLLM's expert-parallel (EP) group size was previously fixed at deployment start; **Elastic EP** lets a running MoE deployment reconfigure its data-parallel (DP) worker count at runtime via `POST /scale_elastic_ep`, redistributing experts with minimal serving interruption [^src10]. See [Mixture of Experts](/ai-engineering/mixture-of-experts.md) for the EP/DP-attention background this builds on.

- **Scale-up flow**: new DP ranks initialize with placeholder weights; existing ranks build *standby* communication groups (via `StatelessGroupCoordinator`, independent of PyTorch's global `WORLD` state) spanning the target rank set while the old topology keeps serving; non-expert weights transfer over standby groups; then all ranks execute a coordinated **switch** (release CUDA graphs, promote standby → active groups, destroy old groups, re-warm); only after the switch does an EPLB reshuffle move expert weights onto the new ranks [^src10].
- **Scale-down** runs EPLB reshuffle *first* (departing ranks' expert weights must migrate off before those ranks are removed), then follows the same teardown pattern [^src10].
- **Cross-rank coordination**: because DP engine cores run asynchronously, a two-stage barrier (timeout-based local barrier → untimed global barrier) prevents a race where some ranks proceed to reconfiguration while others are mid-forward-pass, which would otherwise deadlock the group [^src10].
- **Fault-tolerance building block**: the same scale-down/scale-up path is the mechanism for removing a failed rank, redistributing its experts, and later adding replacement capacity — part of vLLM's broader fault-tolerance RFC (#30112) [^src10]. **NIXL EP** (an alternate EP communication backend) makes rank add/remove incremental via `connect_ranks()`/`disconnect_ranks()` instead of full connection teardown, and adds EP-side failure detection/recovery [^src10].
- **Current scope limits**: `tensor_parallel_size=1` only, `api_server_count=1` only, no DBO or MoE draft/drafter models yet, and scaling depends on the Ray DP backend [^src10].

## Learning resource: DeepLearning.AI course

Red Hat and Andrew Ng's DeepLearning.AI published **"Fast & Efficient LLM Inference with vLLM"** (Cedric Clyburn, Red Hat; ~1.5 hours, 9 lessons, 3 hands-on labs), covering the full compress → serve → benchmark lifecycle: quantizing a model with LLM Compressor, serving it with vLLM (observing continuous batching and prefix caching via live metrics), and benchmarking throughput/latency with GuideLLM plus quality validation with lm-eval [^src6].

## RL post-training for multimodal/diffusion models: VeRL-Omni

**VeRL-Omni** is a general RL post-training framework for multimodal generative models (diffusion + omni-modality), built on `verl` and **vLLM-Omni**, addressing needs the text-only LLM RL stack doesn't cover: non-autoregressive denoising-trajectory rollouts, multi-stage pipelines (text encoder → DiT → VAE), and multimodal reward models (VLM/OCR judges) [^src11].

- **vLLM-Omni integration**: high-throughput async serving for multimodal generation (accuracy on par with `diffusers`), continuously optimized via step-wise continuous batching and embedding caching; reward computation overlaps with ongoing rollout/training to cut end-to-end latency [^src11].
- **Model/algorithm coverage**: Qwen-Image (FlowGRPO/MixGRPO/GRPO-Guard, released), Qwen3-Omni-Thinker (GSPO, PR-ready), BAGEL (FlowGRPO, PR-ready), Wan2.2 and SD3.5 (DanceGRPO/DPO, WIP) [^src11].
- **Measured throughput** (Qwen-Image FlowGRPO OCR-reward training, NVIDIA H800): 0.305 images/GPU/s colocated; moving the reward model to its own GPU (async reward) cut wall-clock time per step by ~14% (420s → 360s) despite using an extra GPU [^src11].
- Supports both NVIDIA GPUs and Ascend NPUs [^src11].

## Leaderboard performance: DeepSeek V3.2, MiniMax-M2.5, Qwen 3.5 397B

An Artificial Analysis benchmark (via DigitalOcean, May 2026) found vLLM's community-built engine topped inference-performance rankings for three frontier open-weight models on NVIDIA Blackwell Ultra silicon, contradicting the assumption that best-in-class inference requires a proprietary stack [^src12]:

- **DeepSeek V3.2**: 230 TPS best per-user output throughput (>4x most other providers on the same model). Fix: op fusion across the attention path (Q/KV normalization, rotary embedding, indexer layernorm+rotary, FP8 quant, KV cache writes collapsed from ~33 kernels/layer toward ~10) — 1.28x speedup at batch 1. A new router GEMM kernel specialized for DeepSeek V3's MoE routing added +6% at batch 1; a new TopK kernel for the sparse-attention indexer (picks the right algorithm per row, fits one CUDA graph) cut 128K-context decode latency up to 17%. With MTP + prefill/decode disaggregation: 262 tok/s on one 8×B300 node at concurrency 1. This fusion work now underpins vLLM's DeepSeek V4 support [^src12].
- **MiniMax-M2.5**: ranked first across all 12 providers measured, TTFT under 1s on 10K-token prompts. Fix: a custom EAGLE3 draft model trained via **TorchSpec** (torch-native online speculative decoding — FSDP draft training + vLLM target inference running concurrently), consuming live vLLM-generated hidden states rather than a generic supervised dataset, plus a custom QK-norm fusion (`fuse_minimax_qk_norm`) for the model's non-standard cross-TP-rank normalization. Ceiling experiment (perfect draft, synthetic 100% acceptance): 326 tok/s at concurrency 1, TP=4 [^src12]. See [Speculative Decoding](/ai-engineering/speculative-decoding.md).
- **Qwen 3.5 397B**: first across all 12 providers, TTFT under 1s on 10K-token prompts. Fix: Qwen's linear attention + non-standard normalization missed vLLM's `allreduce_rmsfusion` pattern, leaving ~half of decode time in un-fused cross-device reduces; four fixes (fusion-pattern recognition, qk-norm+rope kernel work, post-conv-path fusion for the linear-attention architecture, dual-stream execution) closed the gap. Production result at TP=8 + expert parallelism: 163 tok/s at concurrency 1; 7.33 req/s at concurrency 256 (+10% vs. 6.69 req/s baseline) [^src12].

## Distributed KV cache for agentic serving: Mooncake Store integration

Agentic workloads (Claude Code, OpenClaw-style long-horizon tool-use loops) generate massive shared prefixes recomputed across turns — traced from Codex/GPT-5.4 on SWE-bench Pro: ~131:1 input-to-output token ratio, context growing from 12K to 80K+ tokens over a median 33 turns, 94.2% cache-hit rate if prefixes are cached [^src13].

- **Why local KV offload isn't enough**: CPU/DRAM/disk offloading hits capacity limits (a 100K-token context can be several GB) and, when a router migrates a session's next turn to a different instance for load balancing, that instance has never seen the prefix and must recompute from scratch [^src13].
- **Mooncake Store architecture**: a cluster-wide master server tracks KV block hashes/metadata and client health; GPU-node clients manage local CPU/DRAM/SSD and connect via RDMA, forming a distributed KV cache pool. Integrates through vLLM's existing `KVConnector` interface (the same abstraction used for prefill/decode disaggregation) [^src13].
- **SM-free, zero-copy transfer**: uses GPUDirect RDMA to move KV blocks directly between GPU HBM and CPU memory — no staging buffer, no SM consumption (unlike kernel-based copying), all RDMA prep/issue work runs on a dedicated background I/O thread so the transfer path is fully asynchronous from vLLM's perspective. Multi-NIC pooling + topology-aware path selection via the Mooncake Transfer Engine aggregates bandwidth across multiple RNICs per node [^src13].
- **MultiConnector composition**: chains the Mooncake Store connector alongside the existing PD connector — prefill instances store KV in the distributed pool AND prepare PD-connector blocks; decode instances write into the pool (visible immediately to prefill instances) but don't read from it directly [^src13].
- **Measured results** (Kimi-2.5 NVFP4 on GB200, 1P1D, 12 GPUs, realistic Codex traces): 3.8x throughput, 46x lower P50 TTFT, 8.6x lower end-to-end latency — driven by cache-hit rate rising from 1.7% (system-prompt-only caching) to 92.2%. Scaling test (round-robin routing across up to 60 GPUs, synthetic Codex-derived workload): >95% cache-hit rate sustained, near-linear scaling [^src13].

## Multimodal perception sub-agent: NVIDIA Nemotron 3 Nano Omni

**Nemotron 3 Nano Omni** is NVIDIA's open multimodal model (part of the Nemotron 3 family) built to power perception sub-agents — one model reasoning across vision, audio, and language in a single loop, replacing the fragmented separate-vision/speech/language-model stacks that multiply inference hops and fragment context [^src14].

- **Architecture**: hybrid Transformer-Mamba MoE, 30B total / 3B active parameters, 256K context; unified vision + audio encoders (no separate perception models); Conv3D layers for efficient video temporal-spatial handling [^src14].
- **Efficiency**: 9x higher throughput than other open omni models at matched interactivity (7.4x for multi-document, 9.2x for video use cases specifically); Efficient Video Sampling (EVS) lowers compute for video reasoning via temporal-aware perception; supports FP8 and NVFP4 quantization [^src14]. See [Quantization](/ai-engineering/quantization.md).
- **Accuracy**: 20% higher multimodal intelligence vs. the best open alternative; top placements across six multimodal leaderboards (document intelligence: MMlongbench-Doc, OCRBenchV2; video/audio: WorldSense, DailyOmni, VoiceBench); highest throughput + lowest inference cost for video-level tagging on MediaPerf [^src14].
- **Post-training**: multi-environment RL via NVIDIA NeMo RL and NeMo Gym across text/image/audio/video environments [^src14].
- **Role in an agent system**: functions as the perception/context sub-agent feeding structured understanding into downstream orchestration/execution agents — targeted at computer-use agents, document-intelligence workflows, and audio-video understanding pipelines [^src14]. Supported on B200, H100, H200, A100, L40S, DGX Spark, RTX 6000 [^src14]. See [Nemotron 3 Ultra](/ai-engineering/nemotron-3-ultra.md) for NVIDIA's related agentic-reasoning model.

## Ad-hoc serving on Hugging Face Jobs

`hf jobs run` provisions a container ("`docker run` for HF infrastructure") that can boot a vLLM server on demand, billed per-second — a fit for tests, evals, and batch generation rather than a durable production endpoint [^src15]:

```
hf jobs run --flavor a10g-large --expose 8000 --timeout 2h \
  vllm/vllm-openai:latest \
  vllm serve Qwen/Qwen3-4B --host 0.0.0.0 --port 8000
```

- **`--expose`** routes the container's port through HF's public jobs proxy; the resulting `https://<job_id>--8000.hf.jobs` URL is gated (requires an HF token with read access to the job's namespace), not a public endpoint [^src15].
- **OpenAI-compatible**: the exposed server speaks the OpenAI API — an `OpenAI` client can point `base_url` at the job URL and pass `get_token()` as the API key, same interface as any other vLLM deployment [^src15].
- **Scaling to large models**: `--flavor h200x2`/`h200x8` + `--tensor-parallel-size` matching the GPU count shards a model across GPUs (example: a 122B hybrid Mamba/attention MoE model on 2×H200, with `--max-model-len`/`--max-num-seqs` capped down from vLLM's defaults to fit a 256K-context model's memory footprint) [^src15].
- **`--ssh`** opens a shell directly into the running job container (`hf jobs ssh <job_id>`) for interactive debugging — `nvidia-smi`, log tailing, process inspection — without relying on log output alone; requires registering a public key and `huggingface_hub >= 1.20.0` [^src15].
- **Coding-agent backend**: launching with `--enable-auto-tool-choice --tool-call-parser hermes` (parser matched to the model family) lets a self-hosted vLLM job back a terminal coding agent (e.g. [Pi Agent](/ai-engineering/pi-agent.md)) as a custom OpenAI-compatible provider [^src15].
- **HF Jobs vs. Inference Endpoints**: Jobs is billed per-second, maximally flexible (pick the image, flags, hardware), and best for one-off/experimental use; [Hugging Face](/ai-engineering/hugging-face.md) Inference Endpoints are the managed counterpart — access control tiers (public/protected/private) and scale-to-zero — for a durable, production-facing service [^src15].

## One-command serving on HF Jobs

[Hugging Face](/ai-engineering/hugging-face.md) **Jobs** (`hf jobs run`) is a `docker run`-style, per-second-billed way to stand up a vLLM server on demand — the quickest path to a running endpoint for tests, evals, or batch generation, as distinct from HF's managed Inference Endpoints product [^src15]:

```
hf jobs run --flavor a10g-large --expose 8000 --timeout 2h \
  vllm/vllm-openai:latest \
  vllm serve Qwen/Qwen3-4B --host 0.0.0.0 --port 8000
```

`--expose` routes the container's port through HF's public jobs proxy; requests need an HF token as a bearer token (the endpoint is gated, not public). The same pattern scales to large hybrid Mamba/attention MoE models on multi-GPU flavors (e.g. `h200x2` with `--tensor-parallel-size 2`), with `--max-model-len`/`--max-num-seqs` capped to fit long-context models within GPU memory. `--ssh` opens a shell into the running job for debugging, and the exposed endpoint can back **Pi** (a provider-agnostic terminal coding-agent harness) once tool calling is enabled via `--enable-auto-tool-choice --tool-call-parser hermes` [^src15]. See [Hugging Face](/ai-engineering/hugging-face.md) for the full HF Jobs reference and the billing/access-control tradeoffs vs. Inference Endpoints.

## Related

- [Hugging Face](/ai-engineering/hugging-face.md) — HF Jobs (`hf jobs run`) is a one-command way to launch a vLLM server on demand, per-second billed
- [Mixture of Experts](/ai-engineering/mixture-of-experts.md) — MoE execution is a first-class vLLM serving concern (expert parallelism, Elastic EP runtime scaling, quantized MoE backends)
- [Quantization](/ai-engineering/quantization.md) — AutoRound/NVFP4/LLM Compressor checkpoint quantization, used across DGX Spark, Nemotron 3 Ultra, and Laguna XS.2 deployments
- [Nemotron 3 Ultra](/ai-engineering/nemotron-3-ultra.md) — hybrid Transformer-Mamba MoE agentic reasoning model with vLLM day-0 support
- [Laguna XS.2](/ai-engineering/laguna-xs2.md) — Poolside's agentic-coding MoE model with a DFlash speculative decoder
- [Speculative Decoding](/ai-engineering/speculative-decoding.md) — draft/verify latency-reduction technique underlying vLLM's spec-decode data path (Eagle 3/3.1, DFlash)
- [vime](/ai-engineering/vime.md) — RL post-training framework consuming vLLM's native weight-sync/pause-resume RL APIs
- [vLLM Semantic Router](/ai-engineering/vllm-semantic-router.md) — request-routing control plane sitting in front of vLLM
- [Ollama](/ai-engineering/ollama.md) — contrasting local-first single-user serving tool vs. vLLM's production/datacenter serving focus
- [Hugging Face](/ai-engineering/hugging-face.md) — the platform hosting HF Jobs, Inference Endpoints, and the models vLLM serves
- [Pi Agent](/ai-engineering/pi-agent.md) — minimal coding agent that can point at a self-hosted HF Jobs vLLM endpoint as a custom provider
- [AI Engineering hub](/ai-engineering/README.md)

---

[^src1]: [MiniMax M3 in vLLM: Day-0 Serving for 1M-Token Multimodal Reasoning](../../raw/web/web-minimax-m3-in-vllm-day-0-serving-for-1m-token-multimodal-rea-5d5564f8.md) — vLLM blog, 2026-06-12
[^src2]: [DiffusionGemma: The First Diffusion LLM (dLLM) Natively Supported in vLLM](../../raw/web/web-diffusiongemma-the-first-diffusion-llm-dllm-natively-support-646d34df.md) — vLLM blog, 2026-06-10
[^src3]: [Announcing vime: A Simple, Stable, and Efficient RL Framework for LLMs](../../raw/web/web-announcing-vime-a-simple-stable-and-efficient-rl-framework-f-9a392163.md) — vLLM blog, 2026-06-09
[^src4]: [Announcing Day-0 Support for NVIDIA Nemotron 3 Ultra on vLLM](../../raw/web/web-announcing-day-0-support-for-nvidia-nemotron-3-ultra-on-vllm-bc7c306b.md) — vLLM blog, 2026-06-04
[^src5]: [vLLM on the DGX Spark: Architecture, Configuration, and Local Evaluation](../../raw/web/web-vllm-on-the-dgx-spark-architecture-configuration-and-local-e-543e2b72.md) — vLLM blog / Inferact, 2026-06-01
[^src6]: [Fast & Efficient LLM Inference with vLLM: A New Course with DeepLearning.AI](../../raw/web/web-fast-efficient-llm-inference-with-vllm-a-new-course-with-dee-f75c7aa9.md) — vLLM blog, 2026-06-03
[^src7]: [Accelerating Laguna XS.2 Inference with vLLM, Speculators, and LLM Compressor](../../raw/web/web-accelerating-laguna-xs-2-inference-with-vllm-speculators-and-afda11cd.md) — vLLM blog, 2026-05-28
[^src8]: [Native RL APIs in vLLM](../../raw/web/web-native-rl-apis-in-vllm-a83f1153.md) — vLLM blog, 2026-05-28
[^src9]: [vLLM x Novita AI: PegaFlow for Production-Grade External KV Cache](../../raw/web/web-vllm-x-novita-ai-pegaflow-for-production-grade-external-kv-c-4b8a8880.md) — vLLM blog, 2026-05-18
[^src10]: [Elastic Expert Parallelism in vLLM](../../raw/web/web-elastic-expert-parallelism-in-vllm-e7f766b6.md) — vLLM blog, 2026-05-14
[^src11]: [Announcing VeRL-Omni: Easy, Fast, and Stable RL Training for Diffusion and Omni-Modality Models](../../raw/web/web-announcing-verl-omni-easy-fast-and-stable-rl-training-for-di-2040adf3.md) — vLLM blog, 2026-05-14
[^src12]: [vLLM Tops the Artificial Analysis Leaderboard](../../raw/web/web-vllm-tops-the-artificial-analysis-leaderboard-762bd790.md) — vLLM blog, 2026-05-11
[^src13]: [Serving Agentic Workloads at Scale with vLLM x Mooncake](../../raw/web/web-serving-agentic-workloads-at-scale-with-vllm-x-mooncake-78c3044b.md) — vLLM blog, 2026-05-06
[^src14]: [Run Highly Efficient Multimodal Agentic AI with NVIDIA Nemotron 3 Nano Omni Using vLLM](../../raw/web/web-run-highly-efficient-multimodal-agentic-ai-with-nvidia-nemot-b0ef6e3c.md) — vLLM blog, 2026-04-28
[^src15]: [Run a vLLM Server on HF Jobs in One Command](../../raw/web/web-run-a-vllm-server-on-hf-jobs-in-one-command-7f1a19cb.md) — Hugging Face blog, 2026-06-28
[^src15]: [Run a vLLM Server on HF Jobs in One Command](../../raw/web/web-run-a-vllm-server-on-hf-jobs-in-one-command-7f1a19cb.md) — Hugging Face blog

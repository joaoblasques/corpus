---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-improving-lm-studio-s-mlx-engine-for-agentic-workflows-bef5274a.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/web/web-introducing-lm-studio-0-4-0-b88bc367.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/web/web-use-your-lm-studio-models-in-claude-code-b135bf20.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/web/web-open-responses-with-local-models-via-lm-studio-7f2e59f2.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/web/web-locally-ai-joins-lm-studio-5feeb57f.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/web/web-run-your-largest-local-models-from-your-iphone-eede015a.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/web/web-run-open-models-on-nvidia-dgx-station-gb300-cf971dfe.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/web/web-lm-studio-0-3-34-c750f642.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/web/web-lm-studio-0-3-35-58e525e5.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/web/web-lm-studio-0-3-36-80332211.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/web/web-lm-studio-0-3-37-e14de702.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/web/web-lm-studio-0-3-38-e91acb98.md
    channel: web
    ingested_at: 2026-07-02
aliases:
  - LM Studio
  - lmstudio
  - mlx-engine
  - llmster
  - Locally
  - LM Link
tags:
  - corpus/ai-engineering
  - entity
created: 2026-07-02
updated: 2026-07-02
---

# LM Studio

**TL;DR.** LM Studio is a local LLM app that ships **mlx-engine**, an MIT-licensed inference engine optimized for Apple Silicon (built on `mlx-lm`/`mlx-vlm`, Apple's MLX ML library). It exposes an Anthropic-compatible API (so [[ai-engineering/claude-code|Claude Code]] can run against any local model), and mlx-engine v1.8.5 added disk-backed KV-cache checkpointing plus continuous batching for vision-model requests, aimed at repeated long-context agentic workflows [^src1]. Version 0.4.0 introduced **llmster**, a headless daemon that decouples the LM Studio core from its GUI for server/CI/cloud deployment, plus parallel request batching and a stateful REST API [^src2]. Version 0.4.1 added a native Anthropic-compatible `/v1/messages` endpoint for direct [[ai-engineering/claude-code|Claude Code]] use [^src3], and 0.3.39 added support for the provider-agnostic **Open Responses** spec (logprobs, cached-token stats, remote image URLs) [^src4]. LM Studio has also expanded beyond desktop: it acquired the **Locally** mobile app to bring a native mobile surface [^src5], and shipped **LM Link**, an end-to-end-encrypted remote-connection feature letting a phone or laptop drive models running on a larger machine — including an NVIDIA DGX Station GB300 [^src6][^src7].

## The problem: KV cache isn't arbitrarily rewindable

Modern open-weight models use memory-reduction tricks in their attention architecture that break naive KV-cache rewinding — the operation an agent loop needs whenever it trims a reasoning turn and appends a shorter assistant message instead [^src1]:

- **Qwen 3.5/3.6**: hybrid attention architecture.
- **Gemma 4**: sliding-window architecture — interleaves "local" attention layers (512-token window) with "global" attention layers. Rewinding after a reasoning-heavy turn can leave parts of the local KV cache missing, forcing recomputation.

## Fix: disk-backed KV cache with 256-token checkpointing

mlx-engine now streams KV cache to a disk-writer backend at every 256-token boundary, evicting the local-attention KV cache from unified memory once persisted (Apple Silicon's unified-memory architecture means committing to disk directly frees active RAM) [^src1]:

- **Save**: at each 256-token boundary, a background disk-writing thread persists the most recent block while the model keeps processing — write doesn't block generation.
- **Restore**: for a follow-up request, mlx-engine computes a key per 256-token block, determines which global/local blocks are cached, and loads the longest available cached prefix; only uncached or evicted suffixes are re-prefilled. 256 tokens balances recompute waste against disk-cache efficiency [^src1].
- **LRU eviction**: the disk store is one scratch file (not a folder of files) holding serialized safetensors blobs with an in-memory offset/length index; evicted entries return their byte range to a free list; the file shrinks when free space reaches the end. Usage-pattern-aware — a stable system prompt across many short requests stays cached while stale conversations get evicted, and vice versa for one long-growing conversation [^src1].
- **Temporary by design**: lives in `/tmp`, cleared on model unload; no persistent files survive a process exit [^src1].
- **Continuous batching** was also added for the vision-model runner, enabling concurrent request processing for the same model [^src1].

## Benchmarks (M3 Max MacBook Pro, 36GB RAM, Qwen3.6-27B-MLX-4bit)

| Workload | Result |
|---|---|
| 4-way parallel chat (parallel=4) | ~2.2x faster end-to-end, similar output token counts |
| 4 concurrent long prompts, RAM after run | ~82% less extra RAM, similar wall-clock, slightly higher throughput |
| Repeated high-res image prompt (same prompt twice) | ~3.5x faster on the second request (image-expanded prompt cache restored) |

[^src1]

## LM Studio 0.4.0: llmster daemon + parallel requests + stateful API

0.4.0 rearchitected LM Studio to separate the GUI from the core, producing **llmster** — a standalone daemon deployable headless on Linux boxes, cloud servers, GPU rigs, or Google Colab (install via `curl -fsSL https://lmstudio.ai/install.sh | bash`) [^src2]:

- **Parallel requests with continuous batching**: the llama.cpp engine graduated to v2.0.0, adding concurrent-inference support to the same model. New load options: **Max Concurrent Predictions** (queues requests beyond the limit) and **Unified KV Cache** (default on; preallocated resources aren't hard-partitioned per request, so request sizes can vary). Default parallel slots: 4. Not yet in the MLX engine [^src2].
- **New stateful REST endpoint `/v1/chat`**: unlike stateless chat APIs, a request returns a `response_id`; a follow-up passes `previous_response_id` to continue the conversation, keeping requests small for multi-step workflows. Responses include token/speed/TTFT stats and can invoke locally configured MCPs, gated by **permission keys** managed under Settings > Server [^src2].
- Also shipped: chat export (PDF/markdown/text), Split View (side-by-side chat panes), Developer Mode (merges the old Developer/Power User/User modes), and in-app docs [^src2].

## LM Studio 0.4.1: native Anthropic `/v1/messages` endpoint for Claude Code

0.4.1 added a first-party Anthropic-compatible `/v1/messages` endpoint, meaning any Anthropic-API tool — including Claude Code — can point at a local model by changing only the base URL [^src3]:

```
lms server start --port 1234
export ANTHROPIC_BASE_URL=http://localhost:1234
export ANTHROPIC_AUTH_TOKEN=lmstudio
claude --model openai/gpt-oss-20b
```

- Full `/v1/messages` support: streaming (SSE `message_start`/`content_block_delta`/`message_stop`), and tool use/function calling out of the box [^src3].
- Works with GGUF and MLX local models; LM Studio recommends starting Claude Code's context size at ≥25K tokens given how context-heavy the agent is [^src3].
- The Anthropic Python SDK works unmodified against the endpoint by overriding `base_url` and `api_key` [^src3].

## Open Responses support (0.3.39)

LM Studio partnered with OpenAI to support **Open Responses**, an open-source, provider-agnostic specification built on the OpenAI Responses API — a shared schema/tooling layer for calling LLMs, streaming, and composing agentic workflows independent of where the model runs [^src4]. LM Studio's existing `/v1/responses` compatibility endpoint (added in October) became Open-Responses-compliant, adding:

- **Logprobs**: per-token log-probabilities plus candidate tokens (`top_logprobs`), showing model confidence in the chosen token.
- **Token-caching stats**: `usage.input_tokens_details.cached_tokens` reports how many input tokens were reused from a prior turn via `previous_response_id` — token caching is on by default and always reported.
- **Remote image URLs**: vision-enabled models can take a hosted `image_url` directly in `input_image` content blocks, rather than requiring a local file [^src4].

## Mobile + remote access: Locally acquisition and LM Link

LM Studio acquired **Locally AI**, an app for running local models on iPhone/iPad/Mac, bringing its creator (Adrien Grondin) onto the LM Studio team to lead native mobile work [^src5]. The Locally app is now also the vehicle for **LM Link**: a feature that securely (end-to-end encrypted) connects a user's own LM-Studio-running devices so a phone can use models loaded on a more powerful machine at home or work, with all chats saved locally on-device. LM Link on iPhone/iPad is currently limited to a user's own devices; group links (sharing to team members) are in development [^src6].

## Enterprise/on-prem: NVIDIA DGX Station GB300

LM Studio collaborated with NVIDIA on DGX Station's general-availability launch — a deskside AI supercomputer built on the GB300 Blackwell Ultra Superchip, with 748GB of coherent memory and up to 20 petaFLOPS of AI compute [^src7]. The recommended on-prem pattern pairs **llmster** (headless daemon) with **LM Link** so teams can securely share frontier open models from the Station even across networks; models downloaded to the Station become available to all linked devices for inference (e.g., driving `gpt-oss-120b` from a laptop while the Station executes it). LM Studio's SDKs (`lmstudio-js`, `lmstudio-python`), native API, and Anthropic/OpenAI-compatible APIs all work against a Station-hosted server [^src7].

## Earlier releases: 0.3.34–0.3.38

A run of patch releases preceding 0.4.0, chiefly model-support additions and MLX/tool-call bugfixes [^src8][^src9][^src10][^src11][^src12]:

| Version | Notes |
|---|---|
| 0.3.34 | Support for EssentialAI's rnj-1 model; fixed a Jinja prompt-formatting bug where EOS tokens were not included properly for some models [^src8] |
| 0.3.35 | [MLX] Support for Devstral-2 and GLM-4.6V; fixed a bug sending the default system prompt to the model even after the system-prompt field was cleared; fixed an associated incorrect token count; fixed tool-call results sometimes not being added to context correctly [^src9] |
| 0.3.36 | Support for Google's [[ai-engineering/functiongemma|FunctionGemma]] (270M) [^src10] |
| 0.3.37 | Support for the LFM2 tool-call format; fixed a "Cannot read properties of null (reading 'architecture')" crash when using a generator [^src11] |
| 0.3.38 | [Mac][M5] Enabled auto-upgrade to the optimized MLX NAX engine, fixing MLX model crashes on macOS 26.2 and improving performance (0.3.38 shipped Mac-only; other platforms remained on 0.3.37) [^src12] |

## Fine-tuning workflow: [[ai-engineering/functiongemma|FunctionGemma]] via [[ai-engineering/unsloth|Unsloth]]

LM Studio published a walkthrough for fine-tuning Google's FunctionGemma (270M, tool-call-specialized) using Unsloth and running the result locally [^src13]:

1. **Fine-tune** — use an Unsloth starter notebook (Colab or local Jupyter/VS Code) to load the base model, apply LoRA fine-tuning, and handle tokenization/chat templates. Unsloth supports NVIDIA/AMD/Intel GPUs; local fine-tuning is not yet supported on Apple Silicon (a separate notebook targets that case) [^src13].
2. **Export to GGUF** — either Unsloth's native GGUF/llama.cpp conversion (direct to Q8_0/F16/BF16) or merge LoRA adapters into the base model (FP16) and convert separately to a chosen quantization (e.g., Q4_K_M) [^src13].
3. **Import** — `lms import <path/to/model.gguf>` registers the model under "My Models" in LM Studio [^src13].
4. **Serve** — `lms load <model identifier>` (optionally with `--ttl <seconds>` to auto-unload) then `lms server start` exposes the model over LM Studio's OpenAI-compatible local API [^src13].

LM Studio's example shows FunctionGemma failing to produce a useful response pre-fine-tuning and successfully calling a Wikipedia search tool after just 10 minutes of fine-tuning (LM Studio recommends ≥1 hour for better results) [^src13].

## Related

- [[ai-engineering/ollama|Ollama]] — competing local-model serving tool; also ships Anthropic API compatibility for Claude Code and an MLX Apple Silicon backend
- [[ai-engineering/functiongemma|FunctionGemma]] — Google's 270M tool-calling-specialized model, importable into LM Studio after Unsloth fine-tuning
- [[ai-engineering/unsloth|Unsloth]] — fine-tuning toolkit used in LM Studio's model-import workflow
- [[ai-engineering/claude-code|Claude Code]] — the agentic coding client LM Studio's Anthropic-compatible API and KV-cache rewind fix specifically target
- [[ai-engineering/vllm|vLLM]] — contrasting production/datacenter serving engine also solving agentic-workload KV-cache reuse (via distributed Mooncake Store rather than local disk); also targets NVIDIA DGX Spark, a smaller desk-side single-GPU sibling of the DGX Station GB300
- [[ai-engineering/quantization|Quantization]] — MLX 4-bit quantized model used in the benchmarks
- [[ai-engineering/README|AI Engineering hub]]

---

[^src1]: [Improving LM Studio's MLX Engine for Agentic Workflows](../../raw/web/web-improving-lm-studio-s-mlx-engine-for-agentic-workflows-bef5274a.md) — LM Studio blog, 2026-06-28
[^src2]: [Introducing LM Studio 0.4.0](../../raw/web/web-introducing-lm-studio-0-4-0-b88bc367.md) — LM Studio blog
[^src3]: [Use your LM Studio Models in Claude Code](../../raw/web/web-use-your-lm-studio-models-in-claude-code-b135bf20.md) — LM Studio blog
[^src4]: [Open Responses with local models via LM Studio](../../raw/web/web-open-responses-with-local-models-via-lm-studio-7f2e59f2.md) — LM Studio blog
[^src5]: [Locally AI joins LM Studio](../../raw/web/web-locally-ai-joins-lm-studio-5feeb57f.md) — LM Studio blog
[^src6]: [Run (your largest) local models from your iPhone](../../raw/web/web-run-your-largest-local-models-from-your-iphone-eede015a.md) — LM Studio blog
[^src7]: [Run open models on NVIDIA DGX Station GB300](../../raw/web/web-run-open-models-on-nvidia-dgx-station-gb300-cf971dfe.md) — LM Studio blog
[^src8]: [LM Studio 0.3.34](../../raw/web/web-lm-studio-0-3-34-c750f642.md) — LM Studio blog
[^src9]: [LM Studio 0.3.35](../../raw/web/web-lm-studio-0-3-35-58e525e5.md) — LM Studio blog
[^src10]: [LM Studio 0.3.36](../../raw/web/web-lm-studio-0-3-36-80332211.md) — LM Studio blog
[^src11]: [LM Studio 0.3.37](../../raw/web/web-lm-studio-0-3-37-e14de702.md) — LM Studio blog
[^src12]: [LM Studio 0.3.38](../../raw/web/web-lm-studio-0-3-38-e91acb98.md) — LM Studio blog
[^src13]: [How to fine-tune FunctionGemma and run it locally](../../raw/web/web-how-to-fine-tune-functiongemma-and-run-it-locally-9eeb0a45.md) — LM Studio blog

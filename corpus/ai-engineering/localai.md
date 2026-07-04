---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/web-localai-b97b21bd.md
    channel: web
    ingested_at: 2026-07-04
  - path: raw/_inbox/web-overview-localai-f93ff9ac.md
    channel: web
    ingested_at: 2026-07-04
  - path: raw/_inbox/web-installation-localai-4b274918.md
    channel: web
    ingested_at: 2026-07-04
  - path: raw/_inbox/web-getting-started-localai-3f5f8906.md
    channel: web
    ingested_at: 2026-07-04
  - path: raw/_inbox/web-news-localai-0129d5ef.md
    channel: web
    ingested_at: 2026-07-04
  - path: raw/_inbox/web-features-localai-19ba43e1.md
    channel: web
    ingested_at: 2026-07-04
  - path: raw/_inbox/web-integrations-localai-db59f9a3.md
    channel: web
    ingested_at: 2026-07-04
  - path: raw/_inbox/web-references-localai-36eca587.md
    channel: web
    ingested_at: 2026-07-04
  - path: raw/_inbox/web-faq-localai-43dbfa32.md
    channel: web
    ingested_at: 2026-07-04
  - path: raw/_inbox/web-face-recognition-localai-72509bfe.md
    channel: web
    ingested_at: 2026-07-04
  - path: raw/_inbox/web-voice-recognition-localai-8608645d.md
    channel: web
    ingested_at: 2026-07-04
  - path: raw/_inbox/web-model-compatibility-table-localai-064c4d80.md
    channel: web
    ingested_at: 2026-07-04
  - path: raw/_inbox/web-distributed-mode-localai-6d6b1d04.md
    channel: web
    ingested_at: 2026-07-04
  - path: raw/_inbox/web-macos-installation-localai-6786106b.md
    channel: web
    ingested_at: 2026-07-04
  - path: raw/_inbox/web-text-generation-gpt-localai-a52df1f2.md
    channel: web
    ingested_at: 2026-07-04
  - path: raw/_inbox/web-tls-reverse-proxy-configuration-localai-20aeab6e.md
    channel: web
    ingested_at: 2026-07-04
  - path: raw/_inbox/web-model-configuration-localai-7520643d.md
    channel: web
    ingested_at: 2026-07-04
  - path: raw/_inbox/web-middleware-pii-filtering-and-intelligent-routing-localai-b630efa4.md
    channel: web
    ingested_at: 2026-07-04
  - path: raw/_inbox/web-realtime-api-localai-f17b6e47.md
    channel: web
    ingested_at: 2026-07-04
  - path: raw/_inbox/web-setting-up-models-localai-0352bf55.md
    channel: web
    ingested_at: 2026-07-04
aliases:
  - LocalAI
  - LocalAGI
  - LocalRecall
  - local-ai
tags:
  - corpus/ai-engineering
  - entity
created: 2026-07-04
updated: 2026-07-04
---

# LocalAI

**TL;DR.** LocalAI is an MIT-licensed, OpenAI/Anthropic-API-compatible local inference server — a small, composable AI stack that runs models on your own hardware with no cloud dependency [^src1]. The core binary is minimal; each inference backend (llama.cpp, vLLM, whisper.cpp, stable-diffusion, MLX, and others) is installed on demand via a Backend Gallery [^src2]. Three products compose: **LocalAI** (core API server), **LocalAGI** (autonomous agent platform), **LocalRecall** (semantic search/memory) [^src1].

## Architecture

LocalAI is "a small core that pulls model backends on demand, so you install only what you use" [^src1]. The core binary provides:

- **OpenAI-compatible API** — drop-in replacement for OpenAI and Anthropic APIs; compatible with existing SDKs and applications [^src2]
- **Built-in Web UI** — chat, model management, agent creation, image generation, system monitoring [^src2]
- **AI Agents** — MCP (Model Context Protocol) tool support for autonomous agents, configurable from the UI [^src2]
- **Multi-modal backends** — LLMs, image/video generation, text-to-speech, speech-to-text, vision, embeddings [^src2]

Backends are separate artifacts, not bundled. The FAQ is explicit: "You install only the backends your models use" [^src3]. This keeps the core binary small and avoids pulling in frameworks (Python, ONNX Runtime, PyTorch) unless a model backend specifically needs them.

## Backend model compatibility

Models are configured via YAML files that map a model name to a backend and its parameters [^src7]. The compatibility table ([Model Compatibility Table](../../raw/_inbox/web-model-compatibility-table-localai-064c4d80.md)) lists all backends (llama.cpp, vLLM, whisper.cpp, stable-diffusion, MLX, etc.) and compatible model families. LocalAI attempts automatic backend detection; YAML config overrides it [^src8].

Key text-generation backends: `llama.cpp` (default for GGUF models), `vLLM` (for high-throughput serving), `rwkv.cpp` [^src9].

## Face and voice recognition

Two biometric endpoints, both sharing the same C++/ggml "no-Python" design philosophy [^src10][^src11]:

- **Face recognition** (`/v1/face/*`): verification (1:1), identification (1:N), embedding, detection, demographics, antispoofing. Backend: `face-detect.cpp` (recommended) or `insightface` (Python) [^src10].
- **Voice recognition** (`/v1/voice/*`): speaker verification, identification, embedding, demographics (age/gender/emotion). Backend: `voice-detect.cpp` (recommended) [^src11].

Both store gallery entries as self-describing GGUF files.

## Distributed mode

Horizontal scaling across multiple machines uses **PostgreSQL** for state and node registry and **NATS** for real-time coordination [^src12]. Designed for Kubernetes production deployments; separate from the simpler P2P/federation mode.

## Middleware: PII filtering and intelligent routing

A request-middleware layer sits between the HTTP API and model backends [^src13]:
- **PII filtering** — detect and redact PII before it reaches the model
- **Intelligent routing** — route requests to different models/backends based on content, cost, latency, or custom rules

## Realtime API (WebSocket)

LocalAI supports the OpenAI Realtime API spec — low-latency, multi-modal (voice + text) conversations over WebSocket [^src14]. Same endpoint pattern as OpenAI's `wss://api.openai.com/v1/realtime`.

## Model configuration (YAML)

Models are configured with YAML files in the `models/` directory. Key fields: `name`, `backend`, `parameters`, `template`, `system_prompt`, `context_size`, `gpu_layers`, `f16` [^src7]. LocalAI resolves the backend from the YAML; without a YAML it auto-detects from the GGUF metadata.

## Installation paths

- **macOS**: DMG application — simplest path; no GPU required for CPU inference [^src5]
- **Docker** (Linux/Windows): `docker run -p 8080:8080 -v $PWD/models:/models localai/localai:latest`
- **Homebrew**, binary download, source build [^src6]

## News highlights (2026)

- April 2026: **Audio Transform** — generic audio-in/audio-out endpoint; first implementation: LocalVQE C++ backend (joint AEC + noise suppression + dereverberation); bidirectional WebSocket streaming at `/audio/transformations/stream` [^src4].

## Related

- [Ollama](/ai-engineering/ollama.md) — alternative local LLM runtime; simpler single-model serving; different philosophy (Ollama is more opinionated, LocalAI is more composable)
- [LM Studio](/ai-engineering/lm-studio.md) — desktop GUI for local models
- [vLLM](/ai-engineering/vllm.md) — high-throughput GPU serving; available as a LocalAI backend
- [Local AI Agents](/ai-engineering/local-ai-agents.md) — how LocalAGI/LocalRecall fit in the local agent stack
- [AI Engineering hub](/ai-engineering/README.md)

---

[^src1]: [LocalAI](../../raw/_inbox/web-localai-b97b21bd.md) — localai.io homepage
[^src2]: [Overview :: LocalAI](../../raw/_inbox/web-overview-localai-f93ff9ac.md) — localai.io docs overview
[^src3]: [FAQ :: LocalAI](../../raw/_inbox/web-faq-localai-43dbfa32.md) — localai.io FAQ
[^src4]: [News :: LocalAI](../../raw/_inbox/web-news-localai-0129d5ef.md) — localai.io release notes
[^src5]: [macOS Installation :: LocalAI](../../raw/_inbox/web-macos-installation-localai-6786106b.md) — localai.io macOS guide
[^src6]: [Installation :: LocalAI](../../raw/_inbox/web-installation-localai-4b274918.md) — localai.io installation guide
[^src7]: [Model Configuration :: LocalAI](../../raw/_inbox/web-model-configuration-localai-7520643d.md) — localai.io model config reference
[^src8]: [Model compatibility table :: LocalAI](../../raw/_inbox/web-model-compatibility-table-localai-064c4d80.md) — localai.io model compat table
[^src9]: [Text Generation (GPT) :: LocalAI](../../raw/_inbox/web-text-generation-gpt-localai-a52df1f2.md) — localai.io text generation docs
[^src10]: [Face Recognition :: LocalAI](../../raw/_inbox/web-face-recognition-localai-72509bfe.md) — localai.io face recognition docs
[^src11]: [Voice Recognition :: LocalAI](../../raw/_inbox/web-voice-recognition-localai-8608645d.md) — localai.io voice recognition docs
[^src12]: [Distributed Mode :: LocalAI](../../raw/_inbox/web-distributed-mode-localai-6d6b1d04.md) — localai.io distributed mode docs
[^src13]: [Middleware: PII filtering and intelligent routing :: LocalAI](../../raw/_inbox/web-middleware-pii-filtering-and-intelligent-routing-localai-b630efa4.md) — localai.io middleware docs
[^src14]: [Realtime API :: LocalAI](../../raw/_inbox/web-realtime-api-localai-f17b6e47.md) — localai.io realtime API docs

---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/web-ollama-s-new-app-ollama-blog-1344542b.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/_inbox/web-openai-gpt-oss-ollama-blog-0a0ad7a4.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/_inbox/web-cloud-models-ollama-blog-ec2bfe12.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/_inbox/web-new-model-scheduling-ollama-blog-9f9b5356.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/_inbox/web-web-search-ollama-blog-aa148e97.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/_inbox/web-ollama-launch-ollama-blog-bb057651.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/_inbox/web-openclaw-ollama-blog-ba2f528e.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/_inbox/web-subagents-and-web-search-in-claude-code-ollama-blog-198284bb.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/_inbox/web-improved-performance-and-model-support-with-gguf-ollama-blog-6d9dbd48.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/_inbox/web-ollama-is-now-powered-by-mlx-on-apple-silicon-in-preview-oll-23d29d28.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/_inbox/web-ollama-s-highest-performance-on-apple-silicon-yet-with-mlx-o-c1ddb6ae.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/_inbox/web-nvidia-dgx-spark-performance-ollama-blog-ed001519.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/_inbox/web-nvidia-nemotron-3-ultra-ollama-blog-6c770119.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/_inbox/web-claude-code-with-anthropic-api-compatibility-ollama-blog-eb664f1b.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/_inbox/web-runlocal-local-ai-on-your-own-hardware-a5000279.md
    channel: web
    ingested_at: 2026-07-04
  - path: raw/_inbox/web-runlocal-local-ai-on-your-own-hardware-94e161ca.md
    channel: web
    ingested_at: 2026-07-04
aliases:
  - Ollama
  - ollama
  - ollama run
  - ollama launch
  - ollama cloud
tags:
  - corpus/ai-engineering
  - entity
created: 2026-07-02
updated: 2026-07-04
---

# Ollama

**TL;DR.** Ollama is a tool for running LLMs locally and accessing cloud-hosted models through a unified OpenAI-compatible API. It has grown from a CLI for pulling and running GGUF models into a full platform: desktop app with multimodal drag-and-drop, cloud-hosted large models, web search, `ollama launch` for one-command agentic coding toolchains, and Anthropic Messages API compatibility for Claude Code workflows [^src1][^src2][^src3][^src14].

## Core features

- **OpenAI-compatible REST API** — `POST /api/generate` and `POST /api/chat` endpoints; models referenced by name (`ollama run llama3.1`).
- **Model library** — pull any supported model with `ollama pull <model>`; GGUF models from Hugging Face are supported directly via their registry URL [^src9].
- **Desktop app (macOS/Windows, Jul 2025)** — GUI for chat, multimodal file drag-and-drop (images, PDFs, documents), model switching. The first consumer-facing Ollama surface beyond the CLI [^src1].

## Cloud models

Ollama added **cloud model support** (preview, Sep 2025) to run large models on datacenter hardware when local capacity is insufficient [^src3]:

- Use via `ollama run <cloud-model-name>` — same API surface as local models.
- **Privacy**: Ollama states no data is retained between requests.
- Cloud models include large open-weight models not practical to run locally (e.g. 120B quantized, 550B MoE).
- Authentication: `ollama signin` / `ollama signout`.

OpenAI's **gpt-oss** models (20B and 120B) landed on Ollama cloud in Aug 2025, featuring MXFP4 quantization, chain-of-thought reasoning, and configurable reasoning effort for agentic tasks [^src4].

NVIDIA **Nemotron 3 Ultra** (Jun 2026) is available on Ollama cloud: 550B/55B active MoE, 1M context window, agent-tuned, supporting 12+ languages [^src13].

Ollama DGX Spark benchmarks document cloud performance for gpt-oss, Gemma 3, Llama 3.1, DeepSeek-R1, and Qwen3 [^src12].

## ollama launch (Jan 2026)

`ollama launch <tool>` is a one-command setup for agentic coding environments, removing multi-step configuration [^src7]:

```bash
ollama launch claude-code   # Claude Code with local model backend
ollama launch opencode      # OpenCode
ollama launch codex         # OpenAI Codex CLI
ollama launch droid         # Droid
```

Each launch command provisions a **cloud session window of 5 hours** — enough for extended agentic coding runs without keeping a local daemon running indefinitely.

## Web search API (Sep 2025)

Ollama added a native web search capability, available through [^src5]:

- **REST API** — `tools: [{type: "web_search"}]` in the chat request body
- **Python/JS client libraries** — `client.chat(tools=[{"type": "web_search"}])`
- **MCP server** — works with Cline, Codex, Goose and other MCP-compatible agents
- Two built-in tools: `web_search` (keyword query) and `web_fetch` (retrieve a URL)

## Model scheduling improvements (Sep 2025)

Prior to this release, Ollama used estimated memory for model scheduling, causing OOM crashes when estimates were wrong [^src6]. The new scheduler:

- **Exact memory measurement** — probes actual GPU memory allocation before committing to run a model.
- Multi-GPU improvements: better allocation across multiple devices.
- Result: throughput example jumped from 52 → 85.54 tokens/s after the update for a representative workload.

## GGUF / llama.cpp integration (v0.30)

Ollama 0.30 ships improved GGUF support via llama.cpp [^src9]:

- **~20% faster inference on NVIDIA GPUs**.
- Vulkan is now the default backend (was opt-in).
- Pull GGUF models directly from Hugging Face: `ollama pull hf.co/<org>/<repo>`.
- `ollama launch` integrations included in this release.

## MLX on Apple Silicon

Ollama added MLX as a native inference backend for Apple Silicon (preview, Mar 2026; GA, Jun 2026) [^src10][^src11]:

- **~20% faster output tokens** vs the previous llama.cpp backend on Apple Silicon.
- **NVFP4 format support** — a new compression format for smaller models with minimal accuracy loss.
- **Snapshot system** for agent workflows (Jun 2026): save and restore model state mid-conversation; enables branching, retries, and parallel agent instances without reloading the model [^src11].
- Improved cache: reuse KV cache across conversations, intelligent checkpointing, smarter eviction.

## Anthropic API compatibility (v0.14+)

Ollama exposes an Anthropic Messages API-compatible endpoint, allowing Claude Code and Anthropic SDK clients to point at a local Ollama instance [^src14]:

```python
import anthropic

client = anthropic.Anthropic(
    base_url="http://localhost:11434",  # Ollama local endpoint
    api_key="ollama",                   # any string
)

message = client.messages.create(
    model="llama3.1",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}]
)
```

This is the bridge that lets practitioners use Claude Code's agent harness with local or open-weight models for cost control. See [Pi Agent](/ai-engineering/pi-agent.md) for a similar multi-model-via-Ollama pattern.

## Subagents and web search in Claude Code (Feb 2026)

Ollama documented Claude Code integration with subagents + web search enabled [^src8]:

```
# Spawn parallel subagents via a single prompt:
"Create 3 Claude agents in parallel. Agent 1: research X. Agent 2: research Y. Agent 3: synthesize."
```

This uses Claude Code's native subagent feature (`.claude/agents/`) but with Ollama as the model backend, enabling local-model-powered parallel research loops at near-zero cost.

## OpenClaw integration (Feb 2026)

Ollama published documentation for running [OpenClaw](/ai-engineering/openclaw.md) via `ollama launch openclaw` [^src_oc]:

- One command sets up an OpenClaw local agent with Ollama as the model server.
- Recommended models by role:

| Role | Recommended model |
|---|---|
| General assistant | llama3.1:8b |
| Code tasks | qwen2.5-coder:7b |
| Vision tasks | llava:13b |

## OpenJarvis integration

[OpenJarvis](/ai-engineering/openjarvis.md), a local-first personal-AI framework from Stanford's Hazy Research and Scaling Intelligence labs, ships v1.0 with built-in Ollama support — auto-detecting an existing Ollama install and defaulting to local models with cloud as optional fallback [^src_oj].

## Related

- [OpenClaw](/ai-engineering/openclaw.md) — local agent framework; `ollama launch openclaw` integration
- [OpenJarvis](/ai-engineering/openjarvis.md) — Stanford local-first personal-AI framework built on Ollama
- [Pi Agent](/ai-engineering/pi-agent.md) — minimal coding agent with Ollama/OpenRouter multi-model backend
- [Gemini CLI](/ai-engineering/gemini-cli.md) — competing open-source agentic CLI
- [Claude Code](/ai-engineering/claude-code.md) — Anthropic API compatibility bridge
- [MCP](/ai-engineering/mcp.md) — web search MCP server for Cline/Codex/Goose integration
- [LM Studio](/ai-engineering/lm-studio.md) — competing local-model app; also ships Anthropic API compatibility + an MLX Apple Silicon engine
- [AI Engineering hub](/ai-engineering/README.md)

---

[^src1]: [Ollama's New App](../../raw/_inbox/web-ollama-s-new-app-ollama-blog-1344542b.md) — Ollama blog, Jul 30 2025
[^src4]: [OpenAI gpt-oss on Ollama](../../raw/_inbox/web-openai-gpt-oss-ollama-blog-0a0ad7a4.md) — Ollama blog, Aug 5 2025
[^src3]: [Cloud Models](../../raw/_inbox/web-cloud-models-ollama-blog-ec2bfe12.md) — Ollama blog, Sep 19 2025
[^src6]: [New Model Scheduling](../../raw/_inbox/web-new-model-scheduling-ollama-blog-9f9b5356.md) — Ollama blog, Sep 23 2025
[^src5]: [Web Search](../../raw/_inbox/web-web-search-ollama-blog-aa148e97.md) — Ollama blog, Sep 24 2025
[^src7]: [ollama launch](../../raw/_inbox/web-ollama-launch-ollama-blog-bb057651.md) — Ollama blog, Jan 23 2026
[^src_oc]: [OpenClaw on Ollama](../../raw/_inbox/web-openclaw-ollama-blog-ba2f528e.md) — Ollama blog, Feb 1 2026
[^src8]: [Subagents and Web Search in Claude Code](../../raw/_inbox/web-subagents-and-web-search-in-claude-code-ollama-blog-198284bb.md) — Ollama blog, Feb 16 2026
[^src9]: [Improved Performance and Model Support with GGUF](../../raw/_inbox/web-improved-performance-and-model-support-with-gguf-ollama-blog-6d9dbd48.md) — Ollama blog, v0.30
[^src10]: [Ollama is Now Powered by MLX on Apple Silicon (Preview)](../../raw/_inbox/web-ollama-is-now-powered-by-mlx-on-apple-silicon-in-preview-oll-23d29d28.md) — Ollama blog, Mar 30 2026
[^src11]: [Ollama's Highest Performance on Apple Silicon Yet with MLX](../../raw/_inbox/web-ollama-s-highest-performance-on-apple-silicon-yet-with-mlx-o-c1ddb6ae.md) — Ollama blog, Jun 11 2026
[^src12]: [NVIDIA DGX Spark Performance](../../raw/_inbox/web-nvidia-dgx-spark-performance-ollama-blog-ed001519.md) — Ollama blog, Oct 23 2025
[^src13]: [NVIDIA Nemotron 3 Ultra](../../raw/_inbox/web-nvidia-nemotron-3-ultra-ollama-blog-6c770119.md) — Ollama blog, Jun 4 2026
[^src14]: [Claude Code with Anthropic API Compatibility](../../raw/_inbox/web-claude-code-with-anthropic-api-compatibility-ollama-blog-eb664f1b.md) — Ollama blog, v0.14+
[^src_oj]: [OpenJarvis: a local-first personal AI is now available to run with Ollama](../../raw/web/web-openjarvis-a-local-first-personal-ai-is-now-available-to-run-559ec7e6.md) — Ollama Blog, 2026-05-28

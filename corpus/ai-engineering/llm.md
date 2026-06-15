---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: 03_Resources/Study Notes/AI - How Large Language Models Work.md
    channel: notes
    ingested_at: 2026-05-21
  - path: raw/web/google-diffusiongemma-26b-a4b-it-hugging-face.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/coherelabs-command-a-plus-05-2026-w4a4-hugging-face.md
    channel: web
    ingested_at: 2026-06-12
aliases:
  - LLM
  - large language model
  - language model
  - foundation model
  - diffusion language model
  - mixture of experts
  - MoE
  - open-weights model
tags:
  - corpus/ai-engineering
  - concept
created: 2026-05-21
updated: 2026-06-12
---

# LLM (Large Language Model)

**TL;DR**: A mathematical function trained on massive text corpora that assigns probabilities to the next token in a sequence. All behavior emerges from hundreds of billions of continuous numeric weights [^src1].

## Core mechanism: next-token prediction

An LLM is fundamentally a probability distribution over the vocabulary given a context. A chatbot interaction works as [^src1]:
1. Construct a prompt (system instructions + user message)
2. Sample the next token from the output distribution
3. Append it and repeat until the response is complete

Sampling is probabilistic — the same prompt produces different outputs each run.

## Parameters (weights)

Model behavior is entirely encoded in continuous numeric values (weights). GPT-3: ~175 billion parameters. Training starts with random weights; the model outputs gibberish. After training on trillions of examples, weights encode generalizable language knowledge [^src1].

## Training phases

| Phase | Goal | Compute |
|---|---|---|
| **Pre-training** | Predict next word across internet-scale text | The bulk of compute (100M+ CPU-years equivalent for largest models) |
| **RLHF** | Align outputs with human preferences; workers flag bad outputs | Fine-tuning phase; much smaller compute budget |

Scale context: GPT-3's training data would take a human 2,600+ years to read continuously. Only feasible via GPU parallelism [^src1].

## Architecture: Transformer

The [[ai-engineering/transformer|Transformer]] (Google, 2017) is the architecture that makes parallel sequence processing feasible. Key mechanism: **attention** — embeddings update their representations by attending to other tokens in context [^src1].

The specific model behavior is *emergent* — researchers design the framework, but the billions of parameters determine exactly what the model does [^src1].

## Beyond dense autoregression: two architectural directions

The next-token, dense-Transformer baseline above is not the only shape modern open-weights LLMs take. Two 2026 model families illustrate divergence on both axes — *how* tokens are generated and *how* parameters are activated.

**Mixture-of-Experts (MoE) — sparse activation.** Both families are MoE: only a fraction of total parameters fire per token. Cohere's **Command A+** is a decoder-only sparse-MoE Transformer with **25B active / 218B total** parameters — 128 experts, 8 active per token plus one shared expert, with a token-choice router using a normalized-sigmoid (not softmax) activation [^src3]. This decouples capacity (total params) from inference cost (active params), so a 218B-class model serves on a single B200 at 4-bit (W4A4) quantization [^src3]. Architectural details worth noting: sliding-window + global attention interleaved 3:1, RoPE on the windowed layers only, and native conversational tool use with optional grounding-span **citations** (`<co>…</co>` tags mapping spans to tool results) — see [[ai-engineering/tool-calling|Tool Calling]] and [[ai-engineering/structured-outputs|Structured Outputs]] [^src3].

**Diffusion LMs — parallel denoising instead of token-by-token.** Google DeepMind's **DiffusionGemma** (26B-A4B, also MoE: 3.8B active / 25.2B total) replaces left-to-right autoregression with **discrete text diffusion** — it "generates text by iteratively denoising blocks of tokens (a 'canvas') in parallel" [^src2]. An autoregressive encoder prefills/caches the prompt; a decoder applies *bidirectional* attention over the canvas and denoises ~15–20 tokens per forward pass, reaching >1,100 tokens/sec at low batch size [^src2]. Compute is **adaptive**: simpler prompts need fewer denoising steps. The cost is a measurable quality gap vs the autoregressive Gemma 4 sibling on hard benchmarks (e.g. AIME 69.1% vs 88.3%, GPQA Diamond 73.2% vs 82.3%) — the speed/quality tradeoff of the diffusion approach is explicit [^src2].

Both ship **open weights** (Apache 2.0), with multimodal input, long context (DiffusionGemma 256K; Command A+ 128K), and "thinking"/reasoning modes — the now-standard feature surface for frontier-adjacent open models [^src2][^src3].

## Relationship to agents and context engineering

An LLM is the reasoning engine at the center of an [[ai-engineering/ai-agent|AI Agent]]. The agent's context window — the input to the LLM — is what [[ai-engineering/context-engineering|Context Engineering]] optimizes. Everything the agent knows at any moment is what fits in the context window.

## See also

- [[ai-engineering/transformer|Transformer]] — the architecture underlying all modern LLMs
- [[ai-engineering/ai-agent|AI Agent]] — LLM + tools + memory + orchestration
- [[ai-engineering/context-engineering|Context Engineering]] — optimizing the LLM's context window
- [[ai-engineering/rag|RAG]] — injecting external knowledge into the context window at inference time

---

[^src1]: [[03_Resources/Study Notes/AI - How Large Language Models Work|AI - How Large Language Models Work]]
[^src2]: [DiffusionGemma 26B-A4B-it (model card)](../../raw/web/google-diffusiongemma-26b-a4b-it-hugging-face.md) — Google DeepMind, Hugging Face
[^src3]: [Command A+ (command-a-plus-05-2026-w4a4, model card)](../../raw/web/coherelabs-command-a-plus-05-2026-w4a4-hugging-face.md) — Cohere Labs, Hugging Face

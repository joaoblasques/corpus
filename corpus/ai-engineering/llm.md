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
  - path: raw/youtube/youtube-9vM4p9NN0Ts-stanford-cs229-i-machine-learning-i-building-large-language.md
    channel: youtube
    ingested_at: 2026-06-20
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

The [Transformer](/ai-engineering/transformer.md) (Google, 2017) is the architecture that makes parallel sequence processing feasible. Key mechanism: **attention** — embeddings update their representations by attending to other tokens in context [^src1].

The specific model behavior is *emergent* — researchers design the framework, but the billions of parameters determine exactly what the model does [^src1].

## Beyond dense autoregression: two architectural directions

The next-token, dense-Transformer baseline above is not the only shape modern open-weights LLMs take. Two 2026 model families illustrate divergence on both axes — *how* tokens are generated and *how* parameters are activated.

**Mixture-of-Experts (MoE) — sparse activation.** Both families are MoE: only a fraction of total parameters fire per token. Cohere's **Command A+** is a decoder-only sparse-MoE Transformer with **25B active / 218B total** parameters — 128 experts, 8 active per token plus one shared expert, with a token-choice router using a normalized-sigmoid (not softmax) activation [^src3]. This decouples capacity (total params) from inference cost (active params), so a 218B-class model serves on a single B200 at 4-bit (W4A4) quantization [^src3]. Architectural details worth noting: sliding-window + global attention interleaved 3:1, RoPE on the windowed layers only, and native conversational tool use with optional grounding-span **citations** (`<co>…</co>` tags mapping spans to tool results) — see [Tool Calling](/ai-engineering/tool-calling.md) and [Structured Outputs](/ai-engineering/structured-outputs.md) [^src3].

**Diffusion LMs — parallel denoising instead of token-by-token.** Google DeepMind's **DiffusionGemma** (26B-A4B, also MoE: 3.8B active / 25.2B total) replaces left-to-right autoregression with **discrete text diffusion** — it "generates text by iteratively denoising blocks of tokens (a 'canvas') in parallel" [^src2]. An autoregressive encoder prefills/caches the prompt; a decoder applies *bidirectional* attention over the canvas and denoises ~15–20 tokens per forward pass, reaching >1,100 tokens/sec at low batch size [^src2]. Compute is **adaptive**: simpler prompts need fewer denoising steps. The cost is a measurable quality gap vs the autoregressive Gemma 4 sibling on hard benchmarks (e.g. AIME 69.1% vs 88.3%, GPQA Diamond 73.2% vs 82.3%) — the speed/quality tradeoff of the diffusion approach is explicit [^src2].

Both ship **open weights** (Apache 2.0), with multimodal input, long context (DiffusionGemma 256K; Command A+ 128K), and "thinking"/reasoning modes — the now-standard feature surface for frontier-adjacent open models [^src2][^src3].

## Autoregressive pre-training: tokenization and perplexity (Stanford CS229)

The Stanford CS229 LLM lecture grounds the mechanics formally [^src4]:

### Autoregressive generation

An LLM is **autoregressive**: it generates text one token at a time, each token conditioned on all previous tokens. At training time, the model sees a long sequence of text and learns to predict the next token at every position simultaneously (via teacher-forcing); at inference time, it samples one token, appends it to the context, and predicts the next one, repeating until done [^src4].

The training objective is **cross-entropy loss** averaged over all tokens:

```
L = - (1/T) ∑ₜ log P(token_t | token_1, ..., token_{t-1})
```

Minimizing this is equivalent to maximizing the likelihood of the training corpus under the model [^src4].

### BPE tokenization (Byte Pair Encoding)

LLMs do not process raw characters or words — they operate on **tokens**, sub-word units produced by BPE [^src4]:

1. Start with individual characters as the vocabulary.
2. Repeatedly find the most frequent pair of adjacent tokens and merge them into a single token.
3. Stop when the vocabulary reaches the target size (e.g., 50,000 tokens for GPT-2).

Result: common words become a single token; rare words are split into sub-word pieces. "unhappiness" might tokenize as ["un", "happiness"] or ["un", "happy", "ness"]. BPE balances vocabulary size against sequence length — fewer tokens per sequence means faster attention, but the vocabulary table grows [^src4].

Token count differs from word count: roughly 1 word ≈ 1.3–1.5 tokens for English; code and non-Latin scripts may tokenize much less efficiently [^src4].

### Perplexity

**Perplexity** is the standard intrinsic evaluation metric for language models [^src4]:

```
Perplexity = 2^H    where H = - (1/T) ∑ₜ log₂ P(token_t | context)
```

H is the average per-token cross-entropy loss in bits. Perplexity measures "how surprised the model is on average" — a model assigning uniform probability over a V-word vocabulary has perplexity V; a perfect model has perplexity 1 [^src4].

Lower perplexity = better model (more confident and correct). The key interpretation: *perplexity is the effective branching factor at each step* — a perplexity of 50 means the model is roughly choosing among 50 equally likely next tokens on average [^src4].

Perplexity does not directly measure downstream task quality (a model with low perplexity can still fail at reasoning tasks), but it tracks training progress reliably and enables fair comparison across model sizes trained on the same data [^src4].

## Relationship to agents and context engineering

An LLM is the reasoning engine at the center of an [AI Agent](/ai-engineering/ai-agent.md). The agent's context window — the input to the LLM — is what [Context Engineering](/ai-engineering/context-engineering.md) optimizes. Everything the agent knows at any moment is what fits in the context window.

## See also

- [Transformer](/ai-engineering/transformer.md) — the architecture underlying all modern LLMs
- [AI Agent](/ai-engineering/ai-agent.md) — LLM + tools + memory + orchestration
- [Context Engineering](/ai-engineering/context-engineering.md) — optimizing the LLM's context window
- [RAG](/ai-engineering/rag.md) — injecting external knowledge into the context window at inference time

---

[^src1]: [AI - How Large Language Models Work](/03_Resources/Study Notes/AI - How Large Language Models Work.md)
[^src2]: [DiffusionGemma 26B-A4B-it (model card)](../../raw/web/google-diffusiongemma-26b-a4b-it-hugging-face.md) — Google DeepMind, Hugging Face
[^src3]: [Command A+ (command-a-plus-05-2026-w4a4, model card)](../../raw/web/coherelabs-command-a-plus-05-2026-w4a4-hugging-face.md) — Cohere Labs, Hugging Face
[^src4]: [Stanford CS229 — Building Large Language Models](../../raw/youtube/youtube-9vM4p9NN0Ts-stanford-cs229-i-machine-learning-i-building-large-language.md) — Stanford, YouTube

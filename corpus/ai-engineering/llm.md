---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: 03_Resources/Study Notes/AI - How Large Language Models Work.md
    channel: notes
    ingested_at: 2026-05-21
aliases:
  - LLM
  - large language model
  - language model
  - foundation model
tags:
  - corpus/ai-engineering
  - concept
created: 2026-05-21
updated: 2026-05-21
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

## Relationship to agents and context engineering

An LLM is the reasoning engine at the center of an [[ai-engineering/ai-agent|AI Agent]]. The agent's context window — the input to the LLM — is what [[ai-engineering/context-engineering|Context Engineering]] optimizes. Everything the agent knows at any moment is what fits in the context window.

## See also

- [[ai-engineering/transformer|Transformer]] — the architecture underlying all modern LLMs
- [[ai-engineering/ai-agent|AI Agent]] — LLM + tools + memory + orchestration
- [[ai-engineering/context-engineering|Context Engineering]] — optimizing the LLM's context window
- [[ai-engineering/rag|RAG]] — injecting external knowledge into the context window at inference time

---

[^src1]: [[03_Resources/Study Notes/AI - How Large Language Models Work|AI - How Large Language Models Work]]

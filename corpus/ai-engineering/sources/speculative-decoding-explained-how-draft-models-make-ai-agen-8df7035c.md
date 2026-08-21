---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/web-speculative-decoding-explained-how-draft-models-make-ai-agen-8df7035c.md
    channel: web
    ingested_at: 2026-08-21
aliases:
  - MindStudio speculative decoding explainer
tags:
  - corpus/ai-engineering
  - source
created: 2026-08-21
updated: 2026-08-21
---

# Speculative Decoding Explained: How Draft Models Make AI Agents Faster

**TL;DR.** Speculative decoding uses a small draft model to propose 4–8 tokens; the large target model verifies all of them in one batched forward pass — accepting correct guesses and rejecting wrong ones — yielding 2–3× speedups with no output quality loss. AI agents benefit disproportionately because latency compounds across multi-step workflows. [^src1]

## Key concepts

**The autoregressive bottleneck.** LLMs generate one token per full forward pass through the network. Parallelism (GPU cores) helps training but not sequential token generation — you can't generate token 10 without token 9. Memory bandwidth, not compute, is typically the limiting factor. [^src1]

**Draft-and-verify loop:**
1. Small draft model generates 4–8 candidate tokens (fast; model is small)
2. Large target model evaluates all candidates in a *single* parallel forward pass (verification is parallelizable because all draft tokens are known)
3. Accepted tokens kept; first rejected token → replaced by target model's own sample; process restarts [^src1]

**Output quality guarantee.** The verification step is a rejection-sampling procedure that preserves the target model's output distribution exactly. "You're not trading quality for speed." [^src1]

**Acceptance rate.** The fraction of draft tokens the target accepts. Well-matched model pairs on structured output (code, JSON, templated text) achieve 80%+ acceptance rates → 2–3× speedup. Poorly matched pairs may barely beat naive generation. Structured agentic tasks tend to get the highest acceptance rates. [^src1]

**Rough speedup math (example):** Draft model 5ms/token; target 100ms/forward pass; 5 draft tokens at 75% acceptance rate → ~3.75 tokens per 125ms ≈ 33ms/token vs. original 100ms. [^src1]

**Draft model variants:**
- Same-family smaller model (CodeLlama 7B → 70B)
- Self-speculative decoding (skip layers during draft phase; same model)
- Medusa/multi-head: extra prediction heads on the target model; no separate model required
- Training a purpose-built lightweight drafter [^src1]

**Where Anthropic, Google, vLLM, Groq use it.** Anthropic uses speculative decoding internally for Claude (Claude Haiku as draft for Sonnet/Opus). Google integrates it in Gemini serving. vLLM and TGI (open-source inference servers) support it. [^src1]

**Why agents benefit most.** An agent doesn't make one LLM call — it makes many. 2–3× per call compounds across the whole pipeline. Structured tool-call outputs (JSON, function arguments) produce high acceptance rates, amplifying the gain. [^src1]

**Limitations:** highly creative/unpredictable generation (high temperature) → lower acceptance rates; very short responses → overhead doesn't amortize; mismatched model families → low acceptance rates; memory-constrained deployments → running two models costs more VRAM. [^src1]

## Related pages

- [Speculative Decoding](/ai-engineering/speculative-decoding.md)
- [vLLM](/ai-engineering/vllm.md)
- [AI Agent](/ai-engineering/ai-agent.md)

[^src1]: raw/_inbox/web-speculative-decoding-explained-how-draft-models-make-ai-agen-8df7035c.md (MindStudio, channel: web, 2026-06-30)

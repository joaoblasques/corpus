---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/web/instructor-top-multi-language-library-for-structured-llm-out.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/github-openai-tiktoken-tiktoken-is-a-fast-bpe-tokeniser-for.md
    channel: web
    ingested_at: 2026-06-12
aliases:
  - structured outputs
  - structured LLM output
  - Instructor
  - Pydantic outputs
  - tokenization
  - tiktoken
  - BPE
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-12
updated: 2026-06-12
---

# Structured Outputs

**TL;DR**: Forcing an LLM to return data conforming to a declared schema (e.g. a Pydantic model) instead of free text, with validation and automatic retries on failure. The reference Python library is **Instructor** — Pydantic-based, type-safe, provider-agnostic across 15+ LLM providers [^src1]. Beyond formatting convenience, structured outputs are a reliability and security layer: they prevent downstream pipeline failures and stop agents fabricating data to fit a schema (see [[ai-engineering/agent-security|agent security]]).

## Why structured outputs

Raw LLM text is unreliable for programmatic use. Structured outputs let you "define exactly what data you want" and get it back validated [^src1]. They are not just about formatting — they are "a critical security layer" that prevents downstream failures and data fabrication [^src1] (cited from the secure-agents path). Schema enforcement with automatic retries means "no more manual error handling" [^src1].

## Instructor

The most popular Python library for extracting structured data from LLMs — 3M+ monthly downloads, built on Pydantic [^src1]. Key features [^src1]:
- **Schema-first extraction** — define a Pydantic `BaseModel`; the model fills it.
- **Automatic retries** — built-in retry logic (Tenacity) re-asks the model when validation fails.
- **Data validation** — Pydantic validators (including `field_validator`, constraints like `min_length`, `gt`/`le`) enforce response quality; an `llm_validator` can even validate semantically ("don't say objectionable things").
- **Streaming** — partial responses and iterables in real time.
- **Multi-provider** — a unified `from_provider` interface works the same across OpenAI, Anthropic, Google, Mistral, Cohere, Ollama, DeepSeek, and 15+ providers; switching provider is a one-line change.
- **Type safety** — full IDE inference and autocomplete.
- **Templating** — Jinja templates for dynamic prompts with injected `context`.
- **Hooks** — intercept events (`completion:kwargs`, `completion:error`) for logging/monitoring.

Minimal pattern: define a `BaseModel`, call `client.create(response_model=Model, messages=[...])`, get a validated instance back [^src1].

### Instructor vs. PydanticAI

Instructor "shines when you need fast, schema-first extraction without extra agents." For "quality gates, shareable runs, or built-in observability," PydanticAI (the official agent runtime from the Pydantic team) adds typed tools, dataset replays, and dashboards while keeping existing Instructor models [^src1]. Instructor does one thing well: reliable, validated data from LLMs [^src1].

## Related: tokenization (tiktoken)

Schema enforcement and prompt budgeting both depend on how text becomes tokens. **tiktoken** is OpenAI's fast BPE tokenizer — 3–6x faster than a comparable open-source tokenizer [^src2].

Language models "don't see text like you and I, instead they see a sequence of numbers (known as tokens)" [^src2]. Byte pair encoding (BPE) converts text to tokens with useful properties [^src2]:
- **Reversible and lossless** — tokens convert back to the original text.
- **Works on arbitrary text**, even text outside the tokenizer's training data.
- **Compresses** — the token sequence is shorter than the raw bytes; on average each token is ~4 bytes.
- **Surfaces common subwords** — e.g. splitting "encoding" into "encod" + "ing" so the model sees "ing" repeatedly across contexts, helping it generalize grammar.

Usage: `tiktoken.encoding_for_model("gpt-4o")` returns the model's tokenizer; encodings (e.g. `o200k_base`, `cl100k_base`) can be extended with custom special tokens [^src2]. Token counts drive context-window budgeting (see [[ai-engineering/context-engineering|context engineering]] and the tokenization note in [[ai-engineering/prompt-engineering|prompt engineering]]).

## See also

- [[ai-engineering/agent-security|Agent Security]] — structured outputs as Layer 3 (output control) in defense in depth
- [[ai-engineering/prompt-engineering|Prompt Engineering]] — schema/example specification steers output format; tokens and context window
- [[ai-engineering/context-engineering|Context Engineering]] — token budgeting depends on tokenization

---

[^src1]: [Instructor: Top Multi-Language Library for Structured LLM Outputs](../../raw/web/instructor-top-multi-language-library-for-structured-llm-out.md)
[^src2]: [tiktoken — fast BPE tokeniser for OpenAI's models](../../raw/web/github-openai-tiktoken-tiktoken-is-a-fast-bpe-tokeniser-for.md)

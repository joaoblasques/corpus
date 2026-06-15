---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/web/prompt-engineering-overview.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/prompting-best-practices.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/codex-prompting-guide.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/write-better-prompts-for-cursor-claude-copilot.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-06-08-how-openai-engineers-prompt.md
    channel: inbox
    ingested_at: 2026-06-12
  - path: raw/email/email-2025-11-04-practical-prompt-engineering-tips-from-sabrina-on-the-github.md
    channel: inbox
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-06-07-being-good-at-ai-is-stupidly-simple.md
    channel: email
    ingested_at: 2026-06-15
aliases:
  - prompting
  - prompt design
  - few-shot prompting
  - zero-shot prompting
  - chain-of-thought
  - AskUserQuestion
  - ask me questions first
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-12
updated: 2026-06-15
---

# Prompt Engineering

**TL;DR**: The craft of writing instructions, examples, and structured input that steer an LLM toward higher-quality output. Core levers: clarity and explicitness, examples (zero/one/few-shot), XML/delimiter structuring, role assignment, chain-of-thought, and output-format control. Distinct from [[ai-engineering/context-engineering|context engineering]] — prompting shapes *what you say to the model in a single instruction*; context engineering manages *what information occupies the window over a session*.

## Prompt engineering vs. context engineering

Prompt engineering is "success criteria that are controllable through prompt engineering" [^src1] — crafting the instruction, examples, and formatting of a request. Not every failure is a prompting problem: latency and cost "can be sometimes more easily improved by selecting a different model" [^src1]. Context engineering (managing window contents, compaction, memory across a long session) is a sibling discipline; this page covers instruction-crafting only.

## Core techniques

The full technique set spans "clarity and examples to XML structuring, role prompting, thinking, and prompt chaining" [^src2].

**Be clear and explicit.** "Claude responds well to clear, explicit instructions" [^src2]. The golden rule: show your prompt to a colleague with minimal context — if they'd be confused, the model will be too [^src2]. Providing the motivation behind an instruction helps the model generalize from the explanation [^src2].

**Examples (few-shot / multishot).** Examples are "one of the most reliable ways to steer Claude's output format, tone, and structure" [^src2]. Progression of precision [^src6]:
- **Zero-shot** — direct task request, no examples; relies entirely on pre-training knowledge.
- **One-shot** — one example; the model learns pattern, format, and style.
- **Few-shot** — two or more examples plus edge cases; the model learns nuances and variations.

Wrap examples in `<example>` tags (and multiple in `<examples>`) so the model distinguishes them from instructions [^src2].

**XML tags / delimiters.** XML tags "help Claude parse complex prompts unambiguously" when mixing instructions, context, examples, and variable inputs [^src2]. Delimiters (quotes, dashes, XML, markdown) create boundaries and structure, making prompts easier to parse and output more readable [^src6].

**Role prompting / personas.** Setting a role in the system prompt focuses behavior and tone; "even a single sentence makes a difference" [^src2]. Personas don't add capability — they "provide a perspective to steer the model toward a subset of data" [^src6].

**Chain-of-thought (CoT).** Asking the model to show reasoning step-by-step breaks complex problems into intermediate steps; especially effective combined with few-shot [^src6].

**Output-format control.** Tell the model what to do instead of what not to do; use XML format indicators; match prompt style to desired output style (e.g. removing markdown from the prompt reduces markdown in output) [^src2].

## Long-document and data-rich prompts

For 20k+ token inputs [^src2]:
- **Put longform data at the top** — above the query, instructions, and examples; "can significantly improve performance."
- **Structure with XML** — wrap each document in `<document>` tags with `<document_content>` and `<source>` subtags.
- **Ground responses in quotes** — ask the model to quote relevant parts first to "cut through the noise."

Context placement matters: providing context at the beginning *and* end of a prompt is much more effective than in the middle [^src6] (the "lost in the middle" effect — see [[ai-engineering/context-engineering|context engineering]]).

## LLM controls behind prompting

Output is non-deterministic by default [^src6]. Knobs that interact with prompting [^src6]:
- **Temperature** — 0 (deterministic) to 2 (random); controls how often the model picks the next-most-likely token.
- **Top-P** — alternative to temperature; removes low-probability candidates from the sampling set.
- **Tokens / context window** — tokens are ~0.75 words on average; the full conversation is re-sent each turn since the model has no memory, and long conversations risk filling the window and inducing hallucinations. (See [[ai-engineering/structured-outputs|tokenization]].)

## Steering agentic models (current generation)

Newer Claude models follow instructions literally and are more responsive to the system prompt, so prompts written to *force* behavior on older models can now overtrigger — "dial back any aggressive language" and replace "CRITICAL: You MUST..." with "Use this tool when..." [^src2]. Specific agentic levers [^src2]:
- **Action vs. hesitation** — explicit `<default_to_action>` or `<do_not_act_before_instructions>` blocks control whether the model implements changes or only suggests them.
- **Parallel tool calls** — promptable to ~100% reliability with a `<use_parallel_tool_calls>` block.
- **Thinking depth** — adaptive thinking is steered by the `effort` parameter and promptable guidance, not `budget_tokens` (deprecated).
- **Over-engineering / scope** — models tend to add extra files and abstractions; explicit minimalism instructions curb this.
- **Anti-hallucination** — an `<investigate_before_answering>` block ("Never speculate about code you have not opened") grounds answers.

OpenAI's Codex guidance converges on similar themes for agentic coding: a starter prompt covering "autonomy and persistence, codebase exploration, tool use, and frontend quality," with the note to *remove* prompting for upfront plans or status preambles because it "can cause the model to stop abruptly before the rollout is complete" [^src3]. Codex also documents **metaprompting** — asking the model at the end of a turn how to improve its own instructions, then generalizing the suggestions across several runs [^src3].

## The "ask me questions first" pattern (model-led elicitation)

The single most useful trick for non-technical users inverts the prompt entirely: instead of writing a good prompt, append **"ask me questions first"** so the model interviews *you* — Claude's `AskUserQuestion` tool surfaces 3–5 clickable questions and builds context from your answers, "and you're already using AI better than 99.9% of the population" [^src7]. Going pro: "give me 3 different strategies" lets the model lay out options for you to pick [^src7]. This is the elicitation counterpart to the [[ai-engineering/agent-harness|harness]] principle that models should *manage their confusion and ask for clarification* rather than guessing silently — and it overlaps with the [[ai-engineering/vibe-coding|spec-driven]] habit of pinning down intent before building. (The "interview me" framing also drives the project-setup loop in [[ai-engineering/ai-product-management|AI Product Management]].)

## Practical gotchas

- The same prompt can give different results each time — that is the non-deterministic nature of LLMs [^src5].
- Agents can go beyond scope and deliver unrequested features; a vague standard prompt invites this [^src6].
- **Emotional prompts** can improve accuracy by making the model attend more to important parts of the prompt — but this is not universal across models and may evolve [^src6].
- **Future-proof prompts**: document how prompts are used and which models they succeed on, so they can be re-tested as new models ship; smaller models may need different techniques than larger ones [^src6].
- A 10x scale-up of an LLM can deliver ~100x the capabilities [^src6].

## See also

- [[ai-engineering/context-engineering|Context Engineering]] — sibling discipline; managing window contents over a session
- [[ai-engineering/structured-outputs|Structured Outputs]] — enforcing schema on prompt results; tokenization
- [[ai-engineering/agent-harness|Agent Harness]] — where prompt scaffolding lives in coding agents
- [[ai-engineering/claude-code|Claude Code]] — agent harness whose behavior is shaped by these techniques
- [[ai-engineering/agent-security|Agent Security]] — prompt injection is the adversarial side of prompting

---

[^src1]: [Prompt engineering overview](../../raw/web/prompt-engineering-overview.md)
[^src2]: [Claude prompting best practices](../../raw/web/prompting-best-practices.md)
[^src3]: [Codex prompting guide](../../raw/web/codex-prompting-guide.md)
[^src5]: [Practical Prompt Engineering tips from Sabrina (email)](../../raw/email/email-2025-11-04-practical-prompt-engineering-tips-from-sabrina-on-the-github.md)
[^src6]: [Write better prompts for Cursor, Claude, Copilot (Frontend Masters)](../../raw/web/write-better-prompts-for-cursor-claude-copilot.md)
[^src7]: [Being good at AI is (stupidly) simple](../../raw/email/email-2026-06-07-being-good-at-ai-is-stupidly-simple.md) — Ruben Hassid

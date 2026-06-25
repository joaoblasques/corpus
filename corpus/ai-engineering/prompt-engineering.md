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
  - path: raw/notes/notes-02-the-art-of-the-prompt-communicating-effectively-with-ai.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-metaprompt.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-cowork-prompt-optimizer.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-2-pass-editor-structure-tone.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-fact-spotter-verify-before-you-ship.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-the-decision-maker-summary.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-the-expert-extraction-summary.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-the-red-flag-summary.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/web/web-prompting-best-practices.md
    channel: web
    ingested_at: 2026-06-23
  - path: raw/github/github-mgalpert-msgprompt.md
    channel: github
    ingested_at: 2026-06-25
  - path: raw/github/github-anthropics-prompt-eng-tutorial.md
    channel: github
    ingested_at: 2026-06-25
aliases:
  - prompting
  - prompt design
  - few-shot prompting
  - zero-shot prompting
  - chain-of-thought
  - AskUserQuestion
  - ask me questions first
  - metaprompting
  - ReAct prompting
  - self-consistency prompting
  - contextual prompting
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-12
updated: 2026-06-18
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

## Vibe-coding-specific prompt antipatterns

Beyond general prompt quality, vibe coding introduces antipatterns tied to how people actually work with AI on code [^src8]:

- **Vague prompt** — no concrete output described; the model guesses scope.
- **Overloaded prompt** — too many requirements in one message; the model addresses some and silently drops others.
- **Missing success criteria** — no definition of done; the agent calls it finished when it runs at all.
- **Ignoring AI clarification requests** — when the model asks a question and you answer with "just do it," you lose the disambiguation that would have prevented a wrong result.
- **Inconsistency across turns** — using different terminology for the same concept in different messages; the model can't reliably unify them.
- **Vague references** — "fix that bug" without identifying which one; in code especially, reference must be precise.

The prompt-antipattern discipline connects directly to the [[ai-engineering/vibe-coding|70% problem]]: vague prompts are how human judgment fails to guard the 30% the AI cannot fill independently.

## Advanced techniques (ch2 additions)

**Self-consistency.** Run the same prompt multiple times and take the majority answer, particularly useful for reasoning tasks where single-pass answers are unreliable [^src8].

**ReAct (Reason + Act).** Interleave reasoning steps with action calls (tool use) so the model can observe results of each action before deciding the next step — grounding multi-step agentic tasks in real feedback rather than up-front planning only [^src8].

**Contextual prompting.** Provide all context the model needs within the same prompt — role, relevant background, constraints, output format — rather than relying on what the model may have "learned." This is the prompt-level version of the [[ai-engineering/context-engineering|context engineering]] principle of supplying unique context rather than general knowledge [^src8].

## Practical gotchas

- The same prompt can give different results each time — that is the non-deterministic nature of LLMs [^src5].
- Agents can go beyond scope and deliver unrequested features; a vague standard prompt invites this [^src6].
- **Emotional prompts** can improve accuracy by making the model attend more to important parts of the prompt — but this is not universal across models and may evolve [^src6].
- **Future-proof prompts**: document how prompts are used and which models they succeed on, so they can be re-tested as new models ship; smaller models may need different techniques than larger ones [^src6].
- A 10x scale-up of an LLM can deliver ~100x the capabilities [^src6].

## Reusable prompt patterns (first-party templates)

These patterns emerged from a set of personal prompt templates [^src9][^src10][^src11][^src12]. They are generalizable techniques, not domain-specific canned prompts.

**Metaprompting (prompt-that-writes-prompts).** Instead of writing a prompt from scratch, describe the goal to a meta-prompt whose role is to produce a well-structured output prompt. The pattern decomposes: gather task goal + clarifications → assign specialized "expert" personas for complex sub-tasks → minimize hallucination by instructing explicit disclaimers when uncertain → consolidate into a canonical prompt structure (Role, Context, Instructions, Constraints, Output Format) [^src9]. Useful when you don't yet know what the right prompt looks like.

**Prompt optimizer (rewrite-before-execute).** Rather than fixing a vague prompt at the output end, pass it through a rewriting step first. The optimizer applies a priority-ordered set of principles — goal over process, concrete success criteria (verifiable, not "high quality"), explicit boundaries and failure-handling — and restructures the raw request accordingly before any execution [^src10]. The technique is particularly valuable for agentic systems where a bad prompt can cause irreversible side-effects.

**Two-pass editing (structure first, tone second).** When editing any long-form text, separate the two concerns into sequential passes: Pass 1 reorganizes logic and cuts redundancy (no tone changes); Pass 2 applies tone and polish. "Rules: Preserve meaning. No new facts. Keep length within ±10%." [^src11] The pattern generalizes to any rewriting task where structural concerns and stylistic concerns contaminate each other if done simultaneously.

**Verify-before-ship (fact-spotter).** A dedicated verification pass that flags "all factual/quantitative claims needing verification" as bullets, suggests how to verify each, then rewrites the text with citation placeholders like `[VERIFY-1]`, `[VERIFY-2]`. Rule: "Don't invent sources. If a claim is weak, propose safer wording." [^src12] The pattern operationalizes §7's provenance discipline as a reusable prompt rather than a checklist.

**Task-specific summarization framings.** The same source document yields very different value depending on the *framing* of the summary request. Three distinct framings [^src13][^src14][^src15]:
- **Decision-maker framing** — "summarize to help me decide [X]": extracts only decision-relevant information, surfaces pros/cons, flags critical considerations.
- **Expert-extraction framing** — "summarize like an expert in [field]": skips basics, focuses on "nuanced, high-level takeaways that separate beginners from experts."
- **Red-flag / adversarial framing** — "summarize with a skeptical eye": surfaces assumptions the author makes, missing evidence, counterarguments not addressed, and reasoning flaws.

Each framing produces a categorically different output from identical input. Choosing the right framing is itself a prompt-engineering decision.

## The 7 deadly sins of prompting (R-E-X framework)

A prompt is a brief, not a wish — "Most prompts fail because they're wishes, not briefs" [^src16]. Seven recurring failure modes and their fixes [^src16]:

1. **No context** → add role + task scope + constraints.
2. **Vague instructions** → define success and explicit acceptance tests.
3. **Treating it like Google** → turn questions into jobs with concrete deliverables.
4. **Asking for everything at once** → split into steps and chain the outputs.
5. **Not iterating** → run a critique-then-revise loop rather than one-shotting.
6. **No format or tone** → force the shape (length, structure) and the voice.
7. **No examples** → add 1–2 gold standards (optionally an anti-example); examples are how a model learns your taste.

**R-E-X** condenses these into three moves [^src16]: **Role** (who the model is; domain, audience, risk tolerance), **Examples** (1–2 gold outputs to imitate), **Expectations** (format, length, tone, banned words, a scoring rubric, and the iteration loop). The throughline: iterate faster rather than write ever-longer prompts.

## Prompt enhancement tools

**MSGPrompt** (`mgalpert/MSGPrompt`, ★20) is a TypeScript browser extension that auto-enhances raw user prompts before sending them to Claude or ChatGPT [^src17]. The pattern: user types a short natural-language intent; MSGPrompt reformulates it following prompt-engineering best practices before the API call. The extension addresses the gap between "what you mean" and "what the model needs to hear" without requiring the user to learn prompting techniques [^src17].

This is the same "pre-prompting" insight as the Cowork Prompt Optimizer template [^src10] applied as a browser-layer intermediary — the user never sees the enhanced prompt, the model always receives it.

## See also

- [[ai-engineering/context-engineering|Context Engineering]] — sibling discipline; managing window contents over a session
- [[ai-engineering/structured-outputs|Structured Outputs]] — enforcing schema on prompt results; tokenization
- [[ai-engineering/agent-harness|Agent Harness]] — where prompt scaffolding lives in coding agents
- [[ai-engineering/claude-code|Claude Code]] — agent harness whose behavior is shaped by these techniques
- [[ai-engineering/agent-security|Agent Security]] — prompt injection is the adversarial side of prompting
- [[ai-engineering/vibe-coding|Vibe Coding]] — where prompt antipatterns cause the 70% problem
- [[ai-engineering/sources/beyond-vibe-coding-book|Beyond Vibe Coding (Book)]] — ch2 as the fullest treatment of the vibe-coding prompt toolkit

---

[^src1]: [Prompt engineering overview](../../raw/web/prompt-engineering-overview.md)
[^src2]: [Claude prompting best practices](../../raw/web/prompting-best-practices.md)
[^src3]: [Codex prompting guide](../../raw/web/codex-prompting-guide.md)
[^src5]: [Practical Prompt Engineering tips from Sabrina (email)](../../raw/email/email-2025-11-04-practical-prompt-engineering-tips-from-sabrina-on-the-github.md)
[^src6]: [Write better prompts for Cursor, Claude, Copilot (Frontend Masters)](../../raw/web/write-better-prompts-for-cursor-claude-copilot.md)
[^src7]: [Being good at AI is (stupidly) simple](../../raw/email/email-2026-06-07-being-good-at-ai-is-stupidly-simple.md) — Ruben Hassid
[^src8]: [Ch2 — The Art of the Prompt](../../raw/notes/notes-02-the-art-of-the-prompt-communicating-effectively-with-ai.md)
[^src9]: [Metaprompt template](../../raw/notes/notes-metaprompt.md)
[^src10]: [Cowork Prompt Optimizer template](../../raw/notes/notes-cowork-prompt-optimizer.md)
[^src11]: [2-Pass Editor template](../../raw/notes/notes-2-pass-editor-structure-tone.md)
[^src12]: [Fact-spotter template](../../raw/notes/notes-fact-spotter-verify-before-you-ship.md)
[^src13]: [The Decision-Maker Summary template](../../raw/notes/notes-the-decision-maker-summary.md)
[^src14]: [The Expert Extraction Summary template](../../raw/notes/notes-the-expert-extraction-summary.md)
[^src15]: [The Red Flag Summary template](../../raw/notes/notes-the-red-flag-summary.md)
[^src16]: [The 7 deadly sins of prompting](../../raw/email/email-2025-08-24-sins.md) — Ruben Hassid
[^src17]: [mgalpert/MSGPrompt — pre-prompting tool for Claude/ChatGPT (★20)](../../raw/github/github-mgalpert-msgprompt.md) — GitHub
[^src18]: [anthropics/prompt-eng-tutorial — GitHub ★36,609](../../raw/github/github-anthropics-prompt-eng-tutorial.md) — Anthropic (9-chapter Jupyter series: Basic Structure → Clear/Direct → Roles → Data/Instructions → Formatting → Precognition → Few-Shot → Hallucinations → Complex/Power Users)

---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/web/how-to-use-the-claude-api-in-python-real-python.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-05-20-how-to-use-the-claude-api-in-python.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/web/anthropic-courses.md
    channel: web
    ingested_at: 2026-06-12
aliases:
  - Claude API
  - claude-api
  - Anthropic API
  - Messages API
  - anthropic SDK
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-12
updated: 2026-06-12
---

# Claude API

**TL;DR.** The Claude API is Anthropic's REST API for the Claude models, with an official Python SDK (`anthropic`). The fastest path: install `anthropic`, set `ANTHROPIC_API_KEY`, and call `client.messages.create()` — a working response in a handful of lines [^src1]. The package "gets you to a working response in a handful of lines" without wiring up heavier frameworks [^src1]. Billed by token (input + output); responses are non-deterministic [^src1]. See [[ai-engineering/anthropic|Anthropic]] for model ids and [[ai-engineering/claude-code|Claude Code]] for the agent CLI.

## Setup

Requires Python 3.9+ and an Anthropic account; new accounts can start after adding $5 of credits [^src1]. Create an API key in the Claude Console and store it as the `ANTHROPIC_API_KEY` environment variable — the SDK reads it automatically, so it "never need[s] to reference it explicitly in your scripts" [^src1]. Never hardcode the key or commit it; rotate immediately if exposed [^src1].

## The Messages API

```python
import anthropic
client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "What is the Zen of Python?"}],
)
print(response.content[0].text)
```

Key parameters [^src1]:

- **`model`** — which Claude model (`claude-sonnet-4-6` is a "capable and cost-efficient" default; names can change) [^src1].
- **`max_tokens`** — a hard ceiling on output, not a target [^src1].
- **`messages`** — a list of turns, each a dict with `"role"` (`"user"` or `"assistant"`) and `"content"` [^src1].

The call returns a `Message`; text lives at `response.content[0].text`. `content` is a list because Claude can return multiple content blocks, but for plain text the first block is the one you want [^src1].

## System prompts

The top-level **`system`** parameter defines Claude's role, tone, and constraints once, before any user input; Claude reads it before processing messages so it shapes every response [^src1]. It is **not** a message — passing `{"role": "system", ...}` inside `messages` raises an error because `"system"` isn't a valid role there [^src1]. The system prompt gets highest priority, making it "much harder for user messages to override" — but "no prompt-based guardrail is absolute", so combine it with server-side validation for hard constraints in production [^src1]. This makes the API reliable for constrained tools (on-topic support bots, scoped assistants) [^src1].

## Structured output

Two ways to force schema-conforming output instead of fragile string parsing [^src1]:

**1. Handwritten JSON schema** via `output_config`:

```python
output_config={"format": {"type": "json_schema", "schema": {...}}}
```

`"additionalProperties": False` tells Claude not to add fields outside those declared. The response is a JSON string; `json.loads()` turns it into a dict. No extra dependencies [^src1].

**2. Pydantic shortcut** via `client.messages.parse()`:

```python
class FunctionDescription(BaseModel):
    function_name: str
    code: str
    explanation: str

response = client.messages.parse(..., output_format=FunctionDescription)
result = response.parsed_output  # a validated model instance
```

This returns a typed, validated object with attribute access; if Claude's response doesn't match, Pydantic raises before downstream code sees it [^src1]. Use the handwritten schema for simple scripts with no extra dependencies; use Pydantic + `parse()` for production and type safety [^src1]. See [[ai-engineering/tool-calling|Tool Calling]] for the related `tool_use` path to structured output.

## Common errors & costs

- **`AuthenticationError`** — usually `ANTHROPIC_API_KEY` not set in the current shell [^src1].
- **`RateLimitError`** — too many requests; Anthropic enforces per-minute and per-day request/token limits by tier. Add exponential backoff for production [^src1].
- **`BadRequestError`** — malformed `messages`; each entry needs `role` and `content`, and `role` must be `user` or `assistant` [^src1].

Every call is billed by token (input + output counted together); set `max_tokens` realistically and watch usage in the Claude Console [^src1].

## Next steps

Beyond the three basics, the SDK supports **streaming** (`stream=True`) for chat UIs, **structured output via `tool_use`** (a different mental model, more powerful for agentic workflows), and **multi-turn conversations** by accumulating `user`/`assistant` turns in `messages` [^src1]. Real Python organizes these into an **LLM application development learning path** [^src1][^src2]. Anthropic hosts its own course materials on a Skilljar LMS [^src3].

## See also

- [[ai-engineering/anthropic|Anthropic]] — model lineup and ids
- [[ai-engineering/claude-code|Claude Code]] — the agent CLI built on the same models
- [[ai-engineering/tool-calling|Tool Calling]], [[ai-engineering/llm|LLM]]

[^src1]: [How to Use the Claude API in Python (Real Python)](../../raw/web/how-to-use-the-claude-api-in-python-real-python.md)
[^src2]: [How to Use the Claude API in Python (email)](../../raw/email/email-2026-05-20-how-to-use-the-claude-api-in-python.md)
[^src3]: [Anthropic courses (Skilljar)](../../raw/web/anthropic-courses.md)

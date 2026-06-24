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
  - path: raw/notes/notes-clippings-introducing-the-claude-platform-on-aws.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-clippings-the-advisor-strategy-give-sonnet-an-intelligence-boost-with.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/_inbox/web-claude-enterprise-analytics-api-reference-guide-claude-help.md
    channel: web
    ingested_at: 2026-06-24
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
updated: 2026-06-24
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

## Advisor tool (beta)

The **advisor tool** formalizes the advisor strategy as a server-side primitive: declare it in the tools list and Sonnet/Haiku know to invoke it when they need guidance [^src5]. The handoff happens inside a single `/v1/messages` request — no extra round-trips or context management needed.

```python
response = client.messages.create(
    model="claude-sonnet-4-6",  # executor
    tools=[
        {
            "type": "advisor_20260301",
            "name": "advisor",
            "model": "claude-opus-4-6",
            "max_uses": 3,
        },
        # ... your other tools
    ],
    messages=[...]
)
# Advisor tokens reported separately in the usage block
```

**Pricing**: advisor tokens billed at the advisor model's rate; executor tokens at the executor's (lower) rate. Since the advisor generates only a short plan (typically 400–700 tokens) and never calls tools or produces user-facing output, the combined cost stays well below running Opus end-to-end [^src5]. Set `max_uses` to cap advisor calls per request; advisor tokens appear separately in the usage block [^src5].

**Benchmark results** (Anthropic evals) [^src5]:
- Sonnet + Opus advisor: +2.7 pp on SWE-bench Multilingual vs Sonnet alone; 11.9% cost reduction per task
- Haiku + Opus advisor on BrowseComp: 41.2% vs Haiku solo 19.7% (more than double); 85% cheaper than Sonnet solo

See [[ai-engineering/optimizing-claude|Optimizing a Claude Setup]] §7 for the full advisor-strategy discussion.

## Enterprise Analytics API

The Enterprise Analytics API provides per-user and per-project engagement metrics for Enterprise organizations [^src6].

**Base URL**: `https://api.anthropic.com/v1/organizations/analytics/`

**Authentication** [^src6]:
- Requires `read:analytics` scope on the API key
- Only a **Primary Owner** can create API keys with this scope

**Endpoints** [^src6]:
- `/users` — per-user engagement (default limit 20 per page)
- `/projects` — project-level adoption data (default limit 100 per page)

**Data characteristics** [^src6]:
- Aggregated **per organization per day**
- **D+3 freshness**: data for day N is available starting day N+3
- **Cursor-based pagination**: max 1000 results per page; use the cursor from each response to paginate
- Error codes: 400 (bad request), 401 (auth), 404 (not found), 410 (gone), 429 (rate limit), 500/504 (server errors)

## Claude Platform on AWS

As of mid-2026, the full Claude Platform is available on AWS under AWS IAM authentication, CloudTrail audit logging, and billing through a single AWS invoice (retires existing AWS commitments). New features ship same-day as the native Claude API [^src4].

**Platform features included**: Claude Managed Agents, Advisor strategy, web search/fetch, code execution, Files API, Skills, MCP connector, prompt caching, citations, and batch processing — plus access to the Claude Console (agents, skills, environments, vaults, observability) [^src4].

**Models available**: Claude Opus 4.7, Sonnet 4.6, and Haiku 4.5 (new models ship same-day) [^src4].

**Choosing between paths** [^src4]:
- **Claude Platform on AWS** — Anthropic operates the service; data processed outside the AWS boundary. Best for companies that want the full platform experience.
- **Claude on Amazon Bedrock** — AWS is the data processor, within the AWS boundary. Best for strict regional data residency requirements.

## See also

- [[ai-engineering/anthropic|Anthropic]] — model lineup and ids
- [[ai-engineering/claude-code|Claude Code]] — the agent CLI built on the same models
- [[ai-engineering/claude-managed-agents|Claude Managed Agents]] — available via the Claude Platform on AWS
- [[ai-engineering/tool-calling|Tool Calling]], [[ai-engineering/llm|LLM]]

[^src1]: [How to Use the Claude API in Python (Real Python)](../../raw/web/how-to-use-the-claude-api-in-python-real-python.md)
[^src2]: [How to Use the Claude API in Python (email)](../../raw/email/email-2026-05-20-how-to-use-the-claude-api-in-python.md)
[^src3]: [Anthropic courses (Skilljar)](../../raw/web/anthropic-courses.md)
[^src4]: [Introducing the Claude Platform on AWS](../../raw/notes/notes-clippings-introducing-the-claude-platform-on-aws.md) — Anthropic announcement
[^src5]: [The advisor strategy: Give Sonnet an intelligence boost with Opus](../../raw/notes/notes-clippings-the-advisor-strategy-give-sonnet-an-intelligence-boost-with.md) — Anthropic
[^src6]: [Claude Enterprise Analytics API Reference Guide](../../raw/_inbox/web-claude-enterprise-analytics-api-reference-guide-claude-help.md) — Anthropic Help Center

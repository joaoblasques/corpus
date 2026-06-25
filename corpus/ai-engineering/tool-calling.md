---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: 03_Resources/Study Notes/AI Agents - Complete Course Beginner to Pro.md
    channel: notes
    ingested_at: 2026-05-07
  - path: raw/web/web-writing-effective-tools-for-ai-agentsusing-ai-agents.md
    channel: web
    ingested_at: 2026-06-23
  - path: raw/_inbox/web-programmatic-tool-calling.md
    channel: web
    ingested_at: 2026-06-25
  - path: raw/email/email-2026-06-21-agents-in-action-2-how-agents-interact-with-the-real-world.md
    channel: email
    ingested_at: 2026-06-25
  - path: raw/web/web-web-fetch-tool.md
    channel: web
    ingested_at: 2026-06-25
  - path: raw/web/web-files-api.md
    channel: web
    ingested_at: 2026-06-25
aliases:
  - tool use
  - function calling
  - tool calls
  - programmatic tool calling
  - allowed_callers
  - code_execution_20260120
tags:
  - corpus/ai-engineering
  - concept
created: 2026-05-07
updated: 2026-06-25
---

# Tool Calling

**TL;DR**: The mechanism by which an LLM requests execution of external functions. The LLM decides *which* tool to call and *with what arguments*; the framework executes and returns results [^src1].

## Mechanics

The LLM does not execute tools directly — it emits a structured request. The orchestration layer intercepts, runs the function, and injects the result back into context [^src1].

```python
@tool
def get_current_time() -> str:
    """Get the current date and time"""
    return datetime.now().isoformat()
```

## Best practices

- Clear, descriptive tool names and docstrings — the LLM reads these to decide when to call [^src1]
- Validate inputs before execution [^src1]
- Return structured JSON results [^src1]
- Memoize results for identical inputs to avoid redundant calls [^src1]

## Production tool design principles (Anthropic guidance)

Anthropic's agent documentation identifies patterns for tools that work well at scale [^src2]:

**Consolidate tools around user intent, not implementation.** Fewer well-described tools outperform exhaustive API mirrors. A single `create_issue_from_thread` tool beats `get_thread` + `parse_messages` + `create_issue` + `link_attachment` — the agent doesn't need to understand the implementation steps, only the goal [^src2].

**Namespace tool names** to prevent collisions when multiple systems are connected: `github_create_pr`, `linear_create_issue`, not `create_issue` [^src2].

**Optimize descriptions for context efficiency.** Tool descriptions are injected into the prompt on every turn; verbose descriptions waste tokens. A 50-word description with a clear name outperforms a 200-word description with a generic name [^src2].

**Eval-driven tool development.** Before adding a tool, write an eval for it (an example of when it should and shouldn't be called). If you can't write the eval, the tool's contract is unclear [^src2].

**Replace UUIDs with natural language identifiers.** Tools that return or accept `"user-id: 9f2a3b"` force the model to manage opaque references; tools that return `"user: Alice Chen (alice@example.com)"` let the model reason about the objects themselves. "Use natural language identifiers and descriptions whenever possible" [^src2].

See also the MCP "One Thing" principle in [[ai-engineering/mcp|MCP]] — the same discipline applied to MCP server tools.

## Programmatic tool calling

Programmatic tool calling lets Claude write Python code inside a **code execution container** that calls tools — instead of emitting individual `tool_use` content blocks one at a time [^src3]. The code runs in a sandboxed container with access to the defined tool set; intermediate results stay in the container and don't flood the conversation context.

**Performance results** (Anthropic benchmarks) [^src3]:
- **+11% on BrowseComp benchmark** — complex multi-step browsing tasks
- **+24% fewer input tokens on DeepSearchQA** — code loops filter/aggregate data before returning to the model
- The improvement comes from two effects: (1) code can loop over tool results without each intermediate result entering context, and (2) the model can express complex multi-tool orchestration in fewer turns

**Required beta flag** [^src3]: enable with `anthropic-beta: code-execution-20260120` in the API header (or the equivalent SDK parameter).

**Model support** (as of 2026-06-25) [^src3]:
- Claude Fable 5 (`claude-fable-5-20260901`)
- Claude Mythos 5 (`claude-mythos-5-20260701`)
- Claude Opus 4.8 / 4.7 / 4.6
- Claude Sonnet 4.6
- Claude Opus 4.5, Sonnet 4.5

**`allowed_callers` field** [^src3]: on each tool definition, `allowed_callers` specifies which entities may invoke the tool. Accepted values: `"claude"` (model direct call), `"code_execution"` (the code sandbox), or `"both"`. Restricting a dangerous tool to `"claude"` only prevents code loops from calling it autonomously; `"code_execution"` tools are hidden from the model's direct tool list.

**`caller` field in responses** [^src3]: tool result blocks include a `caller` field indicating whether the call came from the model directly or from the code sandbox. Useful for audit trails and debugging.

**When to use** [^src3]:
- Multi-step data transformations (fetch → filter → aggregate → format) where intermediate results don't belong in the conversation
- Bulk tool calls in a loop (N API calls with only the final summary needed in context)
- Tasks where logic complexity warrants code (conditionals, retry loops, data normalization) rather than sequential tool use

**When NOT to use**: single tool calls or tasks where the intermediate results are themselves the valuable output (research, browsing summaries).

[^src3]: [Programmatic tool calling — Anthropic API docs](../../raw/_inbox/web-programmatic-tool-calling.md) — Anthropic

## Writing tool descriptions that actually fire

A practitioner pattern from the "Agents in Action" email series [^src4]:

A tool description must answer three questions for the model:
1. **What does this do?** — "Returns the row count of a table."
2. **When should it be used?** — "Use when the user asks about table size or record counts."
3. **What does it need?** — "Requires the exact table name as a string."

Weak: "Counts rows." Strong: "Returns the number of rows in a database table. Use this whenever the user asks how many records exist, how large a table is, or whether a table has any data. Requires the exact table name." — "The second one tells the model when to reach for it. That single sentence is the difference between a tool that fires correctly and one that sits unused" [^src4].

A clear description also reduces cost: "A clear description helps the model decide quickly, while an unclear description makes it think longer and use more tokens" [^src4].

## Web fetch tool

The web fetch tool (`web_fetch_20260209`) allows Claude to retrieve content from specified URLs and PDFs, with dynamic filtering on supported models [^src5]. Key properties:

- **Dynamic filtering** (v20260209 only, requires code execution enabled): Claude writes and runs code to filter fetched content before it reaches context — reduces token consumption while keeping relevance [^src5]
- **Security constraint**: can only fetch URLs that have previously appeared in the conversation context (user-provided or from prior search/fetch results); cannot fetch arbitrary Claude-generated URLs [^src5]
- **Domain controls**: `allowed_domains`, `blocked_domains`, `max_uses`, `max_content_tokens` parameters [^src5]
- **Supported models**: Fable 5, Opus 4.8, Mythos 5, Mythos Preview, Opus 4.7, Opus 4.6, Sonnet 4.6 [^src5]
- **Citations**: optional (`"citations": {"enabled": true}`) — unlike web search where citations are always on [^src5]
- **Pricing**: no additional charges beyond standard token costs for fetched content [^src5]

Common use: pair with web search to first discover URLs then deeply fetch specific pages [^src5].

## Files API

The Files API allows pre-uploading files (PDFs, images, text, datasets) once and referencing them by `file_id` across multiple API requests — avoiding re-upload per call [^src6]. Key details:

- Beta (requires `anthropic-beta: files-api-2025-04-14` header) [^src6]
- Supported file types: PDFs and plain text → `document` blocks; images → `image` blocks; datasets → `container_upload` (code execution) [^src6]
- Files persist until explicitly deleted; no ZDR eligibility [^src6]
- File API operations are free; content counts as input tokens when used in messages [^src6]
- Only files created by skills or code execution can be downloaded; uploaded files cannot [^src6]
- Available on Claude API, Claude Platform on AWS, Microsoft Foundry — not on Bedrock or Vertex AI [^src6]

## Relationship to context engineering

Tool results are one of the four context components injected into an agent's context window after each call. See [[ai-engineering/context-engineering|Context Engineering]].

## See also

- [[ai-engineering/ai-agent|AI Agent]] — tool calling is a core part of the agent loop
- [[ai-engineering/context-engineering|Context Engineering]] — tool results as a context component
- [[ai-engineering/tool-calling-and-context-engineering|Tool Calling & Context Engineering]] — synthesis: how tool results drive context growth and the compounding-window problem

---

[^src1]: [[03_Resources/Study Notes/AI Agents - Complete Course Beginner to Pro|AI Agents - Complete Course Beginner to Pro]]
[^src2]: [Writing Effective Tools for AI Agents](../../raw/web/web-writing-effective-tools-for-ai-agentsusing-ai-agents.md) — Anthropic
[^src4]: [Agents in Action #2: How Agents Interact with the Real World](../../raw/email/email-2026-06-21-agents-in-action-2-how-agents-interact-with-the-real-world.md) — Pipeline to Insights newsletter
[^src5]: [Web fetch tool — Claude Platform docs](../../raw/web/web-web-fetch-tool.md) — Anthropic
[^src6]: [Files API — Claude Platform docs](../../raw/web/web-files-api.md) — Anthropic

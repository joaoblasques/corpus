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
  - path: raw/web/web-programmatic-tool-calling.md
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
  - path: raw/web/web-bash-tool.md
    channel: web
    ingested_at: 2026-06-25
  - path: raw/web/web-web-search-tool.md
    channel: web
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-V2qjnBDZZ7A-playwright-cli-vs-mcp-server-which-is-actually-better-for-cl.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/web/web-code-execution-tool.md
    channel: web
    ingested_at: 2026-06-25
  - path: raw/web/web-tool-search-tool.md
    channel: web
    ingested_at: 2026-06-25
  - path: raw/web/web-tool-use-with-claude.md
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

See also the MCP "One Thing" principle in [MCP](/ai-engineering/mcp.md) — the same discipline applied to MCP server tools.

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

[^src3]: [Programmatic tool calling — Anthropic API docs](../../raw/web/web-programmatic-tool-calling.md) — Anthropic

## Writing tool descriptions that actually fire

A practitioner pattern from the "Agents in Action" email series [^src4]:

A tool description must answer three questions for the model:
1. **What does this do?** — "Returns the row count of a table."
2. **When should it be used?** — "Use when the user asks about table size or record counts."
3. **What does it need?** — "Requires the exact table name as a string."

Weak: "Counts rows." Strong: "Returns the number of rows in a database table. Use this whenever the user asks how many records exist, how large a table is, or whether a table has any data. Requires the exact table name." — "The second one tells the model when to reach for it. That single sentence is the difference between a tool that fires correctly and one that sits unused" [^src4].

A clear description also reduces cost: "A clear description helps the model decide quickly, while an unclear description makes it think longer and use more tokens" [^src4].

## Bash tool

The bash tool (`bash_20250124`) provides a persistent bash session for code execution within the agent's context [^src7]. Key properties:

- **Persistent session** — the bash environment persists across tool calls within a session; environment variables and working directory carry forward [^src7]
- **Token overhead** — approximately **245 input tokens** per bash tool call (tool description overhead) [^src7]
- **Security model** — Anthropic recommends an **allowlist approach** (explicitly permit needed commands) rather than a blocklist (deny dangerous commands); a blocklist is harder to keep exhaustive [^src7]
- **Terminal-Bench 2.0** — the benchmark that measures bash tool quality; Claude 4 series shows significantly improved performance on long-horizon terminal tasks [^src7]
- **Output limits** — bash output is truncated if it exceeds the limit; structure output to put important results first; use file writes for large intermediate outputs [^src7]

Best pattern: use bash for multi-step shell workflows, but avoid accumulating huge output in the conversation — pipe large data to files, then read selectively [^src7].

## Web search tool

The web search tool (`web_search_20250305`) provides internet search capability with optional dynamic filtering [^src8]. Key properties:

- **Dynamic filtering** (requires code execution enabled): Claude can post-process search results by writing and running code to filter/rank results before injecting into context — reduces token cost when many results are noisy [^src8]
- **Pricing**: **$10 per 1,000 searches** (as of 2026-06-25) [^src8]
- **Streaming support**: search results stream progressively [^src8]
- **Model support**: all Claude 4 / Opus 4 series models [^src8]
- **Citations**: always enabled on web search results (unlike web fetch, where citations are optional) [^src8]
- **`search_depth`** parameter: `"basic"` (fast, lower cost) vs `"advanced"` (more sources, higher quality) [^src8]

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

## CLI vs MCP server: browser tool token trade-offs

A direct comparison using Playwright CLI vs Playwright MCP server illuminates a general pattern [^src9]:

| Dimension | CLI (bash skill) | MCP server |
|---|---|---|
| Token overhead | **~68 tokens** (skill loads tool descriptions on demand) | **~3.6K tokens** (all tool definitions pre-loaded at session start) |
| Tool completeness | All tools available by default (PDF, tracing, etc.) | Must opt-in to extra tools to avoid context bloat |
| Execution mode | **Headless** (designed for background agents) | **Headed** by default (good for visual debugging) |
| Portability | Terminal-only | Any runtime that supports the JS runtime; works in browser, desktop, mobile |
| Human scripting | Can be wrapped in bash scripts for human and agent use | More programmatic API |

**Key insight** [^src9]: the MCP protocol loads all tool descriptions into context at session start, even if most tools are never used. A CLI skill loads descriptions only when the skill is invoked. For frequently used browser tools (web scraping, E2E tests), the CLI pattern can save significant context per session.

**Why MCP is still preferred for agentic loops** [^src9]: when the agent needs to run in environments beyond the terminal (browser, desktop app, mobile automation), MCP's standard protocol is more portable. The CLI wins on context economy in terminal-only coding agent use cases.

**If token minimization is the goal** [^src9]: neither Playwright CLI nor Playwright MCP is optimal — Steel's browser uses Playwright under the hood but wraps it in a Rust CLI, reducing token overhead further.

## Tool Search Tool (deferred loading)

The Tool Search Tool enables deferred loading of tools — preventing all tool schemas from occupying the prompt at session start [^src10].

**Two variants** [^src10]:
- `tool_search_tool_regex_20251119` — searches tool names via Python regex (exact or partial matches)
- `tool_search_tool_bm25_20251119` — natural language / semantic search over tool descriptions

**Mechanism** [^src10]: tools marked `defer_loading: true` in the tool registry do not appear in the initial prompt's tool list. Instead, the model calls `tool_search_tool` with a query; the result returns the matched tool schemas as `tool_reference` blocks. The model can then use those tools normally.

**Benefits** [^src10]: preserves prefix cache (tool list changes bust the cache; deferred loading keeps stable tools in the cached prefix), reduces prompt length for sessions with large tool libraries, allows tool discovery via natural language when the exact tool name isn't known.

**ZDR-eligible**: the Tool Search Tool is eligible for Zero Data Retention (ZDR) configurations [^src10].

## Relationship to context engineering

Tool results are one of the four context components injected into an agent's context window after each call. See [Context Engineering](/ai-engineering/context-engineering.md).

## Client tools vs server tools (official API overview)

The distinction between where tool code runs is fundamental [^src11]:

**Client tools** (user-defined + Anthropic-schema tools like `bash`, `text_editor`): Claude responds with `stop_reason: "tool_use"` and tool_use blocks; the client application executes the code and sends back a `tool_result`. All execution happens in the user's infrastructure.

**Server tools** (`web_search`, `code_execution`, `web_fetch`, `tool_search`): run on Anthropic's infrastructure; results come back directly in the response without client execution. No round-trip needed.

**Strict tool use** [^src11]: add `strict: true` to tool definitions to ensure Claude's tool calls always match the schema exactly — guaranteed schema conformance at the cost of some flexibility.

**Tool trigger control** [^src11]:
- Default `tool_choice: {"type": "auto"}` — Claude decides per turn
- System prompt nudges: "Use the tools to investigate before responding" (increases call rate); "Use your judgment about whether to call a tool" (keeps behavior conservative)
- Hard guarantee: use the `tool_choice` parameter

**Token cost of tool use** (system prompt overhead per model) [^src11]:
| Model | `auto`/`none` | `any`/`tool` |
|---|---|---|
| Opus 4.8 | 290 tokens | 410 tokens |
| Opus 4.7 | 675 tokens | 804 tokens |
| Sonnet 4.6 | 497 tokens | 589 tokens |
| Haiku 4.5 | 496 tokens | 588 tokens |

These are added on top of normal input/output tokens and apply whenever ≥1 tool is in the `tools` array.

## See also

- [AI Agent](/ai-engineering/ai-agent.md) — tool calling is a core part of the agent loop
- [Context Engineering](/ai-engineering/context-engineering.md) — tool results as a context component
- [Tool Calling & Context Engineering](/ai-engineering/tool-calling-and-context-engineering.md) — synthesis: how tool results drive context growth and the compounding-window problem

---

[^src1]: [AI Agents - Complete Course Beginner to Pro](/03_Resources/Study Notes/AI Agents - Complete Course Beginner to Pro.md)
[^src2]: [Writing Effective Tools for AI Agents](../../raw/web/web-writing-effective-tools-for-ai-agentsusing-ai-agents.md) — Anthropic
[^src4]: [Agents in Action #2: How Agents Interact with the Real World](../../raw/email/email-2026-06-21-agents-in-action-2-how-agents-interact-with-the-real-world.md) — Pipeline to Insights newsletter
[^src5]: [Web fetch tool — Claude Platform docs](../../raw/web/web-web-fetch-tool.md) — Anthropic
[^src6]: [Files API — Claude Platform docs](../../raw/web/web-files-api.md) — Anthropic
[^src7]: [Bash tool — Anthropic docs](../../raw/web/web-bash-tool.md) — Anthropic
[^src8]: [Web search tool — Anthropic docs](../../raw/web/web-web-search-tool.md) — Anthropic
[^src9]: [Playwright CLI vs MCP Server: Which is Actually BETTER for Claude Code?](../../raw/youtube/youtube-V2qjnBDZZ7A-playwright-cli-vs-mcp-server-which-is-actually-better-for-cl.md) — Better Stack, YouTube
[^src10]: [Tool Search Tool — Claude Code docs](../../raw/web/web-tool-search-tool.md) — Anthropic
[^src11]: [Tool use with Claude — official API docs](../../raw/web/web-tool-use-with-claude.md) — Anthropic

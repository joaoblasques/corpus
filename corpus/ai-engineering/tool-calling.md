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
aliases:
  - tool use
  - function calling
  - tool calls
tags:
  - corpus/ai-engineering
  - concept
created: 2026-05-07
updated: 2026-06-23
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

## Relationship to context engineering

Tool results are one of the four context components injected into an agent's context window after each call. See [[ai-engineering/context-engineering|Context Engineering]].

## See also

- [[ai-engineering/ai-agent|AI Agent]] — tool calling is a core part of the agent loop
- [[ai-engineering/context-engineering|Context Engineering]] — tool results as a context component
- [[ai-engineering/tool-calling-and-context-engineering|Tool Calling & Context Engineering]] — synthesis: how tool results drive context growth and the compounding-window problem

---

[^src1]: [[03_Resources/Study Notes/AI Agents - Complete Course Beginner to Pro|AI Agents - Complete Course Beginner to Pro]]
[^src2]: [Writing Effective Tools for AI Agents](../../raw/web/web-writing-effective-tools-for-ai-agentsusing-ai-agents.md) — Anthropic

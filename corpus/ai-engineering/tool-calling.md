---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: 03_Resources/Study Notes/AI Agents - Complete Course Beginner to Pro.md
    channel: notes
    ingested_at: 2026-05-07
aliases:
  - tool use
  - function calling
  - tool calls
tags:
  - corpus/ai-engineering
  - concept
created: 2026-05-07
updated: 2026-05-07
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

## Relationship to context engineering

Tool results are one of the four context components injected into an agent's context window after each call. See [[ai-engineering/context-engineering|Context Engineering]].

## See also

- [[ai-engineering/ai-agent|AI Agent]] — tool calling is a core part of the agent loop
- [[ai-engineering/context-engineering|Context Engineering]] — tool results as a context component
- [[ai-engineering/tool-calling-and-context-engineering|Tool Calling & Context Engineering]] — synthesis: how tool results drive context growth and the compounding-window problem

---

[^src1]: [[03_Resources/Study Notes/AI Agents - Complete Course Beginner to Pro|AI Agents - Complete Course Beginner to Pro]]

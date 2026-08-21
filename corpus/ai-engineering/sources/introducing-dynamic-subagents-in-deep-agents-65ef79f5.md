---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/web-introducing-dynamic-subagents-in-deep-agents-65ef79f5.md
    channel: web
    ingested_at: 2026-08-21
aliases:
  - LangChain dynamic subagents
  - Deep Agents dynamic subagents
  - dcode terminal agent
tags:
  - corpus/ai-engineering
  - source
created: 2026-08-21
updated: 2026-08-21
---

# Introducing Dynamic Subagents in Deep Agents

**TL;DR.** Dynamic subagents replace turn-by-turn tool calls with a short orchestration *script* the agent writes; a lightweight JS interpreter (QuickJS) executes the script and dispatches subagents. This enables deterministic coverage at scale and reliable multi-phase pipelines that break down under unstructured tool calling. [^src1]

## Key concepts

**Why normal subagents fail at scale.** Standard subagent dispatch (one tool call → one subagent) is sequential and ad-hoc. At 100+ items or conditional/multi-phase logic, models make scope judgment calls ("screened 75 of 500 and called it done") and reproduce complex orchestration as unreliable sequences of tool calls. [^src1]

**Dynamic subagents: the model writes orchestration code.** Instead of calling tools, the agent writes a JS script that drives subagent dispatch. The interpreter (QuickJS) runs the script deterministically. Code patterns the model is good at — loops, branches, `Promise.all` — become the orchestration substrate. [^src1]

**Example (300-page document):**
```js
const results = await Promise.all(pages.map(page =>
  task({ description: `Summarize page ${page.number}`, subagentType: "summarizer" })
));
```
Coverage becomes a structural guarantee, not a prompt engineering problem. [^src1]

**Orchestration patterns** (same concepts as Anthropic's workflow documentation):

| Pattern | Use case |
|---|---|
| Classify and act | Mixed inputs needing different handlers (e.g. ticket triage) |
| Fanout and synthesize | Same work across many items in parallel (code review, doc batch) |
| Adversarial verification | Two-pass: find → independently verify; only confirmed findings survive |
| Generate and filter | Multiple independent solutions scored and compared in code |
| Tournament | Pairwise head-to-head judging through elimination rounds |
| Loop until done | Dedup-and-continue until no new results appear (exhaustive sweep) |

[^src1]

**`task()` global.** Inside the interpreter, `task(description, subagentType, responseSchema)` dispatches a subagent. `responseSchema` (JSON Schema) makes the result a typed object directly usable in code without parsing. [^src1]

**Recursive Language Model.** Dynamic subagents are described as an instance of the RLM pattern: a model writes code, and that code dispatches more agents. "An agent that writes code, and that code dispatches more agents." [^src1]

**dcode terminal agent.** LangChain's terminal coding agent ships with the code interpreter enabled out-of-the-box; trigger dynamic subagents with the word "workflow" in the prompt. [^src1]

## Related pages

- [Agent Harness](/ai-engineering/agent-harness.md)
- [AI Agent](/ai-engineering/ai-agent.md)
- [Context Engineering](/ai-engineering/context-engineering.md)

[^src1]: raw/_inbox/web-introducing-dynamic-subagents-in-deep-agents-65ef79f5.md (LangChain blog, channel: web, 2026-06-30)

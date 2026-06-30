---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/youtube-sNvuH-iTi4c-ai-agents-in-38-minutes-complete-course-from-beginner-to-pro.md
    channel: youtube
    ingested_at: 2026-06-30
tags:
  - corpus/ai-engineering
  - source
created: 2026-06-30
updated: 2026-06-30
---

# AI Agents in 38 Minutes (Marina Wyss)

**Source**: [AI Agents in 38 Minutes — Complete Course from Beginner to Pro](../../raw/_inbox/youtube-sNvuH-iTi4c-ai-agents-in-38-minutes-complete-course-from-beginner-to-pro.md) — Marina Wyss (Senior Applied Scientist, Amazon), YouTube, December 2025.

**Summary**: A practitioner's compressed course from a production ML perspective. Covers the ReAct loop, agent autonomy spectrum, context engineering, use-case selection matrix, the four quality-boosting design patterns (reflection, tool use, planning, multi-agent), and evaluation discipline. Notable for the complexity/precision matrix and tool-anatomy breakdown.

## Key claims

### The ReAct loop
Marina's formulation: "Reason about what to do next, Act (often by calling a tool), Observe the result, then either give you an answer or loop back to reason again" [^src1]. The name ReAct = **Re**ason + **Act**. The iterative loop adds depth: stronger reasoning, fewer hallucinations, better organization vs. single-shot generation [^src1].

### Agent autonomy spectrum
- **Scripted agent**: every step hardcoded; deterministic, easy to control; model only generates text [^src1]
- **Semi-autonomous agent**: model picks from defined tools, makes decisions within guardrails [^src1]
- **Highly autonomous agent**: model decides whether to search, which tools to use, may write and run new functions — more powerful but unpredictable [^src1]

Most production agents sit in the middle (semi-autonomous) [^src1].

### Context engineering for agents
"It's not the model alone, it's how you engineer the context around it" [^src1]. Context includes: background of the task, agent's role, memory of past actions, available tools. Context steers non-deterministic models toward consistent outputs [^src1]. See [[ai-engineering/context-engineering|Context Engineering]].

### Task decomposition methodology
1. Start with how *you* would do the task
2. For each step, ask: "Can an LLM do this?" If no, split smaller until yes
3. Each step = small, checkable, clear → when output is poor, you know exactly which step to improve [^src1]

### Use-case selection matrix (complexity × precision)
| | Low Precision | High Precision |
|---|---|---|
| **High Complexity** | ⭐ Best early wins (fast wins, tolerate imperfect output) | ✓ High value (legal, healthcare) |
| **Low Complexity** | Not worth it | Simple automation |

Agents shine on high-complexity work; start with lower precision side for fastest ROI [^src1].

### Four design patterns
1. **Reflection** — produce → critique → rewrite; especially powerful when external feedback available (run code, validate schema, check citations) [^src1]
2. **Tool use** — give agent a menu of functions; model decides when/which to call; chains tools dynamically for multi-step tasks [^src1]
3. **Planning** — let LLM decide tool order dynamically rather than hardcoding; strongest use case = coding agents [^src1]
4. **Multi-agent collaboration** — specialized agents for distinct sub-tasks (research, curate, write, format) [^src1]

### Guardrails (3 types)
1. **Code snippets** — deterministic checks (format, length, schema); fast and cheap; prefer when possible [^src1]
2. **LLM judge** — nuanced checks (factual consistency, tone); agent revised on judge failure with explanation [^src1]
3. **Human in the loop** — stop and ask for approval before finalizing; for high-stakes outputs [^src1]

### Tool anatomy
Every tool has two parts [^src1]:
- **Interface** (what the agent sees): name + plain-English description of when to use + typed input schema
- **Implementation** (hidden): SQL, auth, retries, throttling, parsing, caching, async support

Good tools: error handling, caching (memoize identical inputs), async support, versioning, documentation, internal registry [^src1].

### Evaluation
- Component-level + end-to-end evaluation
- Inspect the trace (intermediate steps — search queries, drafts, thinking steps) to find failure patterns → become evals or fixes [^src1]
- LLM-as-judge: rate output on 1–5 scale using consistent rubric [^src1]

## Pages populated

- [[ai-engineering/ai-agent|AI Agent]] — ReAct loop name, use-case matrix, task decomposition, guardrails
- [[ai-engineering/agent-evaluation|Agent Evaluation]] — trace inspection, component + end-to-end eval
- [[ai-engineering/tool-calling|Tool Calling]] — tool anatomy (interface vs implementation), tool design best practices

---

[^src1]: [AI Agents in 38 Minutes — Complete Course from Beginner to Pro](../../raw/_inbox/youtube-sNvuH-iTi4c-ai-agents-in-38-minutes-complete-course-from-beginner-to-pro.md) — Marina Wyss (Senior Applied Scientist, Amazon), YouTube, December 2025

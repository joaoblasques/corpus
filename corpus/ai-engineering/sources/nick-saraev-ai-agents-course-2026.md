---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/youtube-EsTrWCV0Ph4-ai-agents-full-course-2026-master-agentic-ai-2-hours.md
    channel: youtube
    ingested_at: 2026-06-30
tags:
  - corpus/ai-engineering
  - source
created: 2026-06-30
updated: 2026-06-30
---

# AI Agents Full Course 2026 (Nick Saraev)

**Source**: [AI Agents Full Course 2026 — Master Agentic AI (2 hours)](../../raw/_inbox/youtube-EsTrWCV0Ph4-ai-agents-full-course-2026-master-agentic-ai-2-hours.md) — Nick Saraev, YouTube, 2026. Playlist: AI Agents.

**Summary**: A practitioner's 2-hour course on agentic AI covering the core agent loop, multi-agent MCP orchestration, self-modifying agent instructions, platform comparison, and advanced patterns including stochastic consensus and video-to-action pipelines.

## Core agent loop

The loop Nick Saraev frames as foundational [^src1]:

```
Observe → Think (reason) → Act → repeat until "definition of done"
```

Unlike a one-shot prompt, the agent checks intermediate outputs and loops. The "definition of done" must be explicit in the agent's system prompt — without it, the loop either runs forever or stops prematurely [^src1].

## Multi-agent MCP orchestration

A multi-model architecture where Claude Code acts as orchestrator and other models are specialized workers, connected via MCP [^src1]:

| Role | Model | Strength |
|---|---|---|
| **Orchestrator** | Claude (Sonnet/Opus) | Best interpretability + orchestration; reads context well |
| **UI/frontend worker** | Gemini | Best for frontend/multimodal tasks |
| **Backend/TDD worker** | GPT/Codex (OpenAI) | Best for backend code + TDD workflows |

Each worker has its own MCP connection; Claude routes tasks by observing capability fit. This is a concrete instantiation of the [[ai-engineering/multi-agent-systems|orchestrator-subagent]] pattern [^src1].

## Self-modifying agent instructions (AGENTS.md / CLAUDE.md / GEMINI.md)

Agents can extend their own instruction files as they learn from corrections [^src1]:

1. Human corrects an agent output ("Don't do it that way, do it like this")
2. Agent appends the preference rule to `AGENTS.md` / `CLAUDE.md` / `GEMINI.md`
3. Next session, the rule loads automatically — the agent doesn't repeat the mistake

This creates a **compounding preference loop**: each correction makes the agent better at this person's specific workflows. Over time the instruction file becomes a rich behavioral profile [^src1].

Different platforms have different convention files: Claude reads `CLAUDE.md`, Gemini reads `GEMINI.md`, Codex reads `AGENTS.md`. In a multi-model setup, each model reads its own file [^src1]. See [[ai-engineering/claude-md-conventions|CLAUDE.md Conventions]].

## Advanced patterns (mentioned in outline)

- **Agent chat rooms**: multiple agents communicating with each other asynchronously, not just hub-and-spoke via an orchestrator [^src1]
- **Stochastic multi-agent consensus**: running the same task through multiple agents, resolving disagreements by majority vote or weighted confidence [^src1]
- **Video-to-action pipelines**: feeding video content (screen recordings, tutorials) directly into agent context to extract and execute the actions shown [^src1]
- **Verification loops**: sub-agents that check the output of peer agents before surfacing results to the user [^src1]

## Pages populated

- [[ai-engineering/multi-agent-systems|Multi-Agent Systems]] — MCP orchestration, platform comparison, self-modifying AGENTS.md
- [[ai-engineering/ai-agent|AI Agent]] — core loop (observe→think→act)
- [[ai-engineering/claude-md-conventions|CLAUDE.md Conventions]] — per-platform instruction files

---

[^src1]: [AI Agents Full Course 2026 — Master Agentic AI (2 hours)](../../raw/_inbox/youtube-EsTrWCV0Ph4-ai-agents-full-course-2026-master-agentic-ai-2-hours.md) — Nick Saraev, YouTube, 2026

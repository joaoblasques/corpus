---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/youtube/youtube-e18sdZLwP7o-how-to-build-claude-subagents-better-than-99-of-people.md
    channel: youtube
    ingested_at: 2026-06-30
aliases:
  - Claude sub-agents
  - Claude Code sub-agents
  - custom sub-agents
  - .claude/agents
  - ultracode
  - dynamic workflows
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-30
updated: 2026-06-30
---

# Claude Sub-Agents

**TL;DR** — Claude Code sub-agents are isolated AI workers defined as markdown files in `.claude/agents/<name>.md`. Unlike [Agent Skills](/ai-engineering/agent-skills.md), sub-agents get a clean context window, can run in parallel, and can use a different model than the orchestrating session — enabling cost-efficient parallel work and separation of concerns [^src1].

## Sub-agents vs Skills

Both use the same markdown file format, but the execution model differs [^src1]:

| Dimension | Sub-agents | Skills |
|---|---|---|
| Context | Clean context window (isolated) | Runs in the current session (shared context) |
| Concurrency | Can run in parallel | Sequential in main session |
| Model | Can use a different model than orchestrator | Inherits session model |
| Use case | Independent parallel tasks; unbiased review; repeated specialized jobs | Repeatable in-session workflows |

The sub-agent gets no memory of the parent session — it starts fresh every time. This isolation is both the strength (unbiased review) and the limit (no implicit handoff of session state) [^src1].

## File format: YAML front matter

Sub-agent files live at `.claude/agents/<name>.md`. The YAML front matter controls routing and behavior [^src1]:

```yaml
---
name: code-reviewer
description: Reviews code for bugs, security issues, and style violations.
  Use when asked to review a PR or check code quality.
model: claude-haiku-4-5-20251001
color: purple
memory: none          # none | project | global
tools:
  - read
  - grep
  - bash
---

<system prompt for this sub-agent>
```

Key fields:
- **`name`** — identifier used to invoke the agent
- **`description`** — the routing trigger (see Progressive Disclosure below)
- **`model`** — can be any Claude model; omit to inherit session model
- **`color`** — visual label in the UI
- **`memory`** — `none` (truly clean), `project` (sees `.claude/` project memory), `global` (sees `~/.claude/` global memory)
- **`tools`** — explicit tool whitelist; unlisted tools are disallowed

## Progressive disclosure

Claude reads only the YAML front matter to decide whether a sub-agent applies — the full system prompt is loaded only when the sub-agent is invoked [^src1]. This means the `description` field doubles as a **routing rule**: it must precisely describe the trigger condition.

> "The description is doing a lot of work. It tells Claude when to use this sub-agent. It has to be precise enough that Claude doesn't fire it for the wrong thing." [^src1]

Ambiguous descriptions cause misfires. The description should name the exact context (e.g., "Use when asked to review a PR, not for general questions") rather than a generic capability label [^src1].

This mirrors the [Agent Skills](/ai-engineering/agent-skills.md) progressive-disclosure pattern where SKILL.md files are indexed but not loaded until invoked.

## Model routing and cost management

The orchestrator can be expensive (Opus 4.8 for complex reasoning) while workers are cheap (Haiku 4.5 for mechanical tasks). Assigning a cheaper `model:` to sub-agents that do reading, formatting, or simple classification produces real cost savings with no quality loss on those sub-tasks [^src1].

Pattern: "Opus boss, Haiku workers" — the main session reasons about what to delegate, the workers execute narrow tasks at low cost [^src1].

## Dynamic workflows

The **ultracode** trigger (Opus 4.8 with dynamic workflows enabled) can spawn 40–210 sub-agents in a single session to parallelize large tasks [^src1]. This is the most extreme expression of the orchestrator-subagent pattern.

Use cases for dynamic fan-out: running tests across all files in parallel, reviewing multiple PRs simultaneously, generating variations for evaluation.

See [Agentic Workflows](/ai-engineering/agentic-workflow.md) for the fan-out/tournament/adversarial patterns this enables.

## Security

Security is achieved through **explicit tool restrictions**, not prompting [^src1]:

- `tools:` whitelist in the YAML front matter restricts what the sub-agent can do
- Omitting destructive tools (e.g., `bash` with broad permissions) from a review-only agent prevents unintended writes
- **Security note**: tool restrictions are more reliable than prompt-level instructions — a sub-agent with `read` and `grep` in its toolset literally cannot write files, regardless of prompt injection [^src1]

The `disallowed_tools` field (specified in the YAML) explicitly blocks tools even if the session model would otherwise offer them [^src1].

## Project vs global scope

Sub-agents can be scoped at two levels [^src1]:
- **Project-level** (`.claude/agents/`): available only when working in that repository
- **Global** (`~/.claude/agents/`): available in all Claude Code sessions across all projects

Global agents are useful for cross-project tools (e.g., a research agent, a PR-format checker). Project-level agents encode project-specific conventions.

## `max_turns`

The YAML front matter supports a `max_turns` field capping how many tool-call iterations the sub-agent can take before returning control. Prevents runaway agents on sub-tasks that should complete in a bounded number of steps [^src1].

## Community resources

**Awesome-Claude-Code-Subagents** (GitHub): a community-sourced collection of pre-built sub-agent definitions covering common specialist roles (security reviewer, accessibility auditor, documentation writer, etc.) [^src1]. Functions like a sub-agent template library.

## See also

- [Agent Skills](/ai-engineering/agent-skills.md) — skill.md files (same format, session-level execution)
- [Multi-Agent Systems](/ai-engineering/multi-agent-systems.md) — coordination patterns for multiple agents
- [Agentic Workflows](/ai-engineering/agentic-workflow.md) — fan-out, tournament, adversarial patterns
- [Claude Code](/ai-engineering/claude-code.md) — the host harness for sub-agents
- [CLAUDE.md Conventions](/ai-engineering/claude-md-conventions.md) — the `.claude/` directory structure
- [Agent Cost Management](/ai-engineering/agent-cost-management.md) — model routing as a cost-reduction strategy

---

[^src1]: [How to Build Claude Subagents (Better Than 99% of People)](../../raw/youtube/youtube-e18sdZLwP7o-how-to-build-claude-subagents-better-than-99-of-people.md) — Nate Herk, YouTube, 2026

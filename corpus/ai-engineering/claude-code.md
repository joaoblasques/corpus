---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/web/how-claude-code-works-in-large-codebases-best-practices-and.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/model-configuration-claude-code-docs.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/catch-security-issues-as-claude-writes-code-claude-code-docs.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-02-20-your-claude-code-guide-tutorials.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-05-20-build-your-own-developer-tools-with-claude-code.md
    channel: email
    ingested_at: 2026-06-12
aliases:
  - Claude Code
  - claude-code
  - Claude Code CLI
tags:
  - corpus/ai-engineering
  - entity
created: 2026-06-12
updated: 2026-06-12
---

# Claude Code

**TL;DR.** Anthropic's CLI coding agent that runs locally on the developer's machine. It navigates a codebase the way an engineer would — traversing the file system, reading files, using grep, following references — with no embedding index to build or maintain [^src1]. Its effectiveness is determined as much by the *harness* (CLAUDE.md, hooks, skills, plugins, MCP servers, LSP, subagents) as by the underlying model [^src1]. Model selection, effort levels, and context window are configurable; a security plugin can review code as Claude writes it [^src2][^src3].

## Agentic search vs. RAG indexing

Claude Code uses **agentic search**: each instance works from the live codebase on the developer's machine, with no embedding pipeline or centralized index [^src1]. RAG-powered tools embed the whole codebase and retrieve chunks at query time; at scale those pipelines fall behind active teams, so retrieval can return a function renamed two weeks ago or a deleted module with no indication it is stale [^src1]. The tradeoff: agentic search "works best when Claude has enough starting context to know where to look" [^src1]. A vague query across a billion-line codebase hits context-window limits before work begins, so codebase setup quality bounds navigation quality [^src1].

## The harness matters as much as the model

A common misconception is that capability is defined solely by the model [^src1]. In practice the **harness** — the ecosystem built around the model — determines performance more than the model alone [^src1]. Five extension points, built in order because each layer builds on the last [^src1]:

| Component | What it is | Loads | Common mistake |
|---|---|---|---|
| **CLAUDE.md** | Context files Claude reads automatically | Every session | Using it for reusable expertise that belongs in a skill [^src1] |
| **Hooks** | Code run at lifecycle points | At their event | Treating them only as guards, not for self-improvement [^src1] |
| **Skills** | Packaged instructions for task types | On demand | Loading everything into CLAUDE.md instead [^src1] |
| **Plugins** | Bundled skills, hooks, MCP configs | Always once configured | Letting good setups stay tribal [^src1] |
| **MCP servers** | Connections to external tools/data | Always once configured | Building them before the basics work [^src1] |

Two further capabilities round out the setup: **LSP integrations** give symbol-level navigation ("go to definition", "find all references"), which is one of the highest-value investments for multi-language codebases — without it Claude pattern-matches on text and can land on the wrong symbol [^src1]. **Subagents** are isolated Claude instances with their own context window that take a task and return only the final result, splitting exploration from editing [^src1].

Hooks' most valuable use is continuous improvement, not just prevention: a stop hook can reflect on a session and propose CLAUDE.md updates while context is fresh; a start hook can load module-specific context dynamically [^src1]. See [[ai-engineering/agent-skills|Agent Skills]] for progressive disclosure and [[ai-engineering/mcp|MCP]].

## Large-codebase practices

Configuration depends on codebase structure, but consistent patterns appeared across successful deployments [^src1]:

- **Keep CLAUDE.md lean and layered.** Claude loads them additively — root file for the big picture, subdirectory files for local conventions. The root file should be "pointers and critical gotchas only" [^src1].
- **Initialize in subdirectories, not the repo root.** Claude automatically walks up the directory tree and loads every CLAUDE.md it finds, so root context is never lost [^src1].
- **Scope test and lint commands per subdirectory** so Claude doesn't run the full suite (and burn context) for a one-service change [^src1].
- **Use `.ignore` files and version-controlled `permissions.deny` rules** to exclude generated files, build artifacts, and third-party code [^src1].
- **Build a lightweight codebase map** (markdown table of contents) when the directory structure doesn't make the codebase legible on its own [^src1].
- **Run LSP servers so Claude searches by symbol, not string** — grep for a common function name returns thousands of matches and wastes context [^src1].

Maintain CLAUDE.md as models evolve: instructions written to compensate for a current model's limitations can constrain a future one (e.g. a rule forcing single-file refactors blocks a newer model's coordinated cross-file edits). Expect a configuration review every three to six months [^src1].

**Organizational layer.** Technical config alone doesn't drive adoption [^src1]. The fastest rollouts had dedicated infrastructure investment before broad access and a DRI or **agent manager** (a hybrid PM/engineer role) owning conventions, permissions, and the plugin marketplace [^src1].

## Model configuration

The `model` setting accepts an alias or a full model name [^src2]. Key aliases: `opus` (resolves to Opus 4.8), `sonnet` (Sonnet 4.6), `haiku`, `fable` (Claude Fable 5, the most capable for the hardest/longest tasks), `best` (Fable 5 where available, else latest Opus), and `opusplan` (Opus during plan mode, switches to Sonnet for execution) [^src2]. Append `[1m]` for the 1M-token context window [^src2]. See [[ai-engineering/anthropic|Anthropic]] for the model lineup.

**Effort levels** control adaptive reasoning (`low`/`medium`/`high`/`xhigh`/`max`); higher effort gives deeper reasoning at higher token spend, default is `high` on Fable 5 and Opus 4.8 [^src2]. `ultracode` is a Claude Code setting (not a model effort level) that sends `xhigh` and additionally has Claude orchestrate dynamic workflows [^src2]. Including `ultrathink` in a prompt requests deeper reasoning for that turn only [^src2]. **Fallback model chains** let Claude switch to a backup model when the primary is overloaded [^src2].

## Security review as Claude writes code

The official security-guidance plugin (from the Anthropic marketplace) reviews Claude's work at three depths [^src3]:

1. **On each file edit** — a fast deterministic pattern match for risky calls (`eval(`, `os.system`, `pickle`, `dangerouslySetInnerHTML`, workflow-file edits), with no model call and no cost [^src3].
2. **At the end of each turn** — a background model review of everything the turn changed, catching authorization bypass, IDOR, injection, SSRF, and weak crypto that string matching cannot [^src3].
3. **On each commit or push Claude makes** — a deeper agentic review that reads surrounding code (callers, sanitizers) to keep false positives low [^src3].

Review independence is the core design: the plugin "does not ask the same Claude instance that wrote the code to grade itself" — the model-backed reviews run as a separate call with fresh context and a security-focused prompt [^src3]. Both model-backed reviews default to Opus 4.7 [^src3]. It is built entirely on hooks (`SessionStart`, `UserPromptSubmit`, `PostToolUse`, `Stop`) and is one layer of defense in depth, not a complete solution [^src3].

## Building your own developer tools

A reusable framework for custom tooling that integrates natively with the agent is a 3-step process: build the app, wrap it in a CLI, give the agent a skill [^src4]. Concretely: scope requirements with brainstorming and voice mode, build the app, add an API-backed CLI, link it globally so Claude can call it, then wrap it as a (user-scoped) skill so it works across repositories [^src4]. CLAUDE.md plus repo instructions reduce mistakes, and hooks keep the app, API, CLI, and skill evolving together [^src4]. The takeaway: "Treat custom tooling as a practical layer of personal developer workflow" [^src4]. Third-party guides and tutorial collections also circulate for Claude Code and the Claude Agent SDK [^src5].

## See also

- [[ai-engineering/claude-cowork|Claude Cowork]] — the non-developer counterpart to Claude Code
- [[ai-engineering/anthropic|Anthropic]] — model lineup and provider
- [[ai-engineering/agent-skills|Agent Skills]], [[ai-engineering/mcp|MCP]], [[ai-engineering/optimizing-claude|Optimizing a Claude Setup]]

[^src1]: [How Claude Code works in large codebases](../../raw/web/how-claude-code-works-in-large-codebases-best-practices-and.md)
[^src2]: [Model configuration — Claude Code docs](../../raw/web/model-configuration-claude-code-docs.md)
[^src3]: [Catch security issues as Claude writes code — Claude Code docs](../../raw/web/catch-security-issues-as-claude-writes-code-claude-code-docs.md)
[^src4]: [Build your own Developer Tools with Claude Code](../../raw/email/email-2026-05-20-build-your-own-developer-tools-with-claude-code.md)
[^src5]: [Your Claude Code Guide + Tutorials](../../raw/email/email-2026-02-20-your-claude-code-guide-tutorials.md)

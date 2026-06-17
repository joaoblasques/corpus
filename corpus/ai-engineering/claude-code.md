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
  - path: raw/web/tuesday-12-may-claude-code-2-1-139.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/youtube/youtube-we7bzvkbcvw.md
    channel: youtube
    ingested_at: 2026-06-17
  - path: raw/notes/notes-clippings-auto-mode-for-claude-code.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-clippings-agent-view-in-claude-code.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-clippings-a-harness-for-every-task-dynamic-workflows-in-claude-code.md
    channel: notes
    ingested_at: 2026-06-17
aliases:
  - Claude Code
  - claude-code
  - Claude Code CLI
tags:
  - corpus/ai-engineering
  - entity
created: 2026-06-12
updated: 2026-06-17
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

## The fire-and-forget loop (`/goal` + agent view)

Claude Code 2.1.139 (May 2026) added two features that together enable a workflow "that didn't exist before" [^src6]. **`/goal`** sets a completion condition and Claude "keeps working across turns until it's met" — across interactive, `-p`, and Remote Control modes, with a live overlay showing elapsed time, turns, and tokens [^src6]. **Agent view** (`claude agents`) lists every session in one place, grouped by state — running, blocked on you, or done [^src6]. The pattern: set a `/goal` ("all tests pass and the PR is ready"), walk away, and check `claude agents` later to see which sessions need input [^src6]. This is the harness-level expression of the autonomous, long-running agent loop ([[ai-engineering/agent-testing|Agent Testing]]'s verification loops are what make a `/goal` exit condition trustworthy).

Other notable harness mechanics from the same release [^src6]:
- **Compaction now preserves sensitive user instructions** — directly targeting the failure mode where compaction dropped CLAUDE.md directives mid-session (see [[ai-engineering/context-window-management|Context Window Management]]).
- **Hook exec form** (`args: string[]`) spawns commands without a shell, so path placeholders never need quoting; `continueOnBlock` on `PostToolUse` feeds a hook's rejection reason back to Claude instead of blocking the turn.
- **MCP stdio servers now receive `CLAUDE_PROJECT_DIR`**, closing a gap where hooks had project context but MCP servers did not.
- **API-key gating**: setting `ANTHROPIC_API_KEY`/`apiKeyHelper`/`ANTHROPIC_AUTH_TOKEN` disables Remote Control, `/schedule`, claude.ai MCP connectors, and notifications even with a Claude.ai login present — unset the key to re-enable.
- Subagent API requests now carry `x-claude-code-agent-id`/`parent-agent-id` headers (and matching OTEL span attributes) for tracing multi-agent sessions.

## Auto mode (permission classifier)

Auto mode is a middle path between conservative default permissions (every write/bash command asks approval) and `--dangerously-skip-permissions` (no checks at all) [^src8]. Before each tool call runs, a classifier reviews it for potentially destructive actions — mass file deletion, sensitive data exfiltration, malicious code execution — and blocks those while letting safe actions proceed automatically [^src8]. If Claude keeps attempting blocked actions, it eventually surfaces a permission prompt to the user [^src8].

Key points [^src8]:
- Available as a research preview for Team plan; rolling out to Enterprise and API in the near term.
- Enable via `claude --enable-auto-mode`, then cycle to it with Shift+Tab in the terminal. In the desktop app or VS Code extension, toggle in Settings → Claude Code, then select from the permission-mode dropdown.
- Works with both Claude Sonnet 4.6 and Opus 4.6.
- Admins on Enterprise/Team can disable it org-wide: `"disableAutoMode": "disable"` in managed settings.
- Auto mode is disabled by default in the desktop app.
- Reduces risk vs skip-permissions but doesn't eliminate it; still recommended to use in isolated environments. Small impact on token consumption and latency for tool calls.

## Agent view (multi-session management)

Agent view (`claude agents` or press left-arrow from any session) is a single dashboard for all Claude Code sessions [^src9]:

- Each row shows session name, whether it needs input, the last response, and when it was last touched.
- **Peek and reply**: select a session to see the last turn; answer inline if it's waiting for input; press Enter to attach for the full transcript.
- **Background anything**: send existing sessions to the background with `/bg`; launch a new background session directly via `claude --bg [task]`.
- Available as a Research Preview on Pro, Max, Team, Enterprise, and API plans.

Patterns observed from early users [^src9]:
- **Scaling parallel sessions**: dispatch several independent tasks at once, return to a list of PRs ready for review.
- **Long-running agent management**: looping jobs (PR babysitter, dashboard updater) show their next run time in the list.
- **Fast context switching**: left-arrow mid-session → start a related task → arrow right back; the peek shows the answer without losing your place.
- **Shipping status scan**: status indicators + peek title make it easy to see which sessions produced a PR.

Agent view is the harness-level expression of parallel agentic work — see also `[[ai-engineering/long-running-agents|Long-Running Agents]]` and the `/goal` discussion above.

## Dynamic workflows

Dynamic workflows let Claude write its own harness on the fly — a JavaScript orchestration file custom-built for the task at hand [^src10]. The default Claude Code harness is built for coding but breaks down on long-running, massively parallel, adversarial, or highly structured tasks because of three failure modes [^src10]:

- **Agentic laziness**: Claude stops before finishing a complex multi-part task (e.g. addresses 35 of 50 items) and declares done.
- **Self-preferential bias**: Claude prefers its own results when asked to verify or judge against a rubric.
- **Goal drift**: fidelity to the original objective erodes across many turns and compaction events; edge-case requirements or "don't do X" constraints get lost in summarization.

Dynamic workflows counter these by orchestrating **separate subagents with their own context windows and isolated goals** [^src10]. Key mechanics [^src10]:
- Execute a JavaScript file with special functions to spawn/coordinate subagents; also includes standard JS (JSON, Math, Array) for data processing.
- Workflows can choose which model each agent uses and whether subagents run in their own worktree.
- Interrupted workflows are resumable — the session picks up where it left off.
- Trigger by asking Claude to "make a workflow" or by using the keyword `ultracode`.
- Save a workflow by pressing "s" in the workflow menu; stored in `~/.claude/workflows`, distributable via a skill.

**Common orchestration patterns** [^src10]:

| Pattern | Use case |
|---|---|
| **Classify-and-act** | Route to different agents/behavior based on task type; or use a classifier to select final output |
| **Fan-out-and-synthesize** | Parallelize subtasks across N agents; synthesize step acts as a barrier waiting for all results |
| **Adversarial verification** | For each spawned agent, run a separate verifier to adversarially check its output against a rubric |
| **Generate-and-filter** | Produce many ideas, filter by rubric, dedupe, return only highest quality |
| **Tournament** | Spawn N agents attempting the same task; a judging agent does pairwise comparison until a winner emerges |
| **Loop until done** | Spawn agents until a stop condition is met (no new findings, no more errors) rather than a fixed number of passes |

**When to use** [^src10]: complex, high-value, parallelizable, long-running, adversarial, or structurally repetitive tasks — migrations, deep research, deep verification, at-scale triage, sorting/ranking, evals, root-cause investigation. Dynamic workflows often use significantly more tokens; they are not needed for regular coding tasks. Combine with `/loop` for recurring execution and `/goal` for hard completion conditions.

See [[ai-engineering/agent-harness|Agent Harness]] for the underlying harness concepts, and [[ai-engineering/agentic-workflow|Agentic Workflows]] for the broader workflow patterns.

## Practitioner workflow (head-of-Claude-Code usage)

Boris Cherny, who leads Claude Code, runs the tool at its full-agentic limit and offers concrete usage tips [^src7]:

- **Parallel sessions ("multi-clouding").** "At the moment I have like five agents running"; "I always have a bunch of agents running" [^src7]. He spreads work across surfaces — "maybe a third of my code now is in the terminal but also a third is using the desktop app and then a third is the iOS app" — all "the same quad agent running everywhere" [^src7]. Designers and non-engineers favor the desktop app's code tab specifically because you can "run as many cloud sessions in parallel as you want" without opening many terminals [^src7].
- **Tip 1 — use the most capable model.** "Just use the most capable model... I have maximum effort enabled always." A weaker model can be *more* expensive: "because it's less intelligent, it actually takes more tokens in the end to do the same task" [^src7]. (See effort levels above and [[ai-engineering/agent-cost-management|Agent Cost Management]].)
- **Tip 2 — plan mode for ~80% of tasks.** "I start almost all of my tasks in plan mode, maybe like 80%." Plan mode is mechanically trivial — "we inject one sentence into the model's prompt to say, 'Please don't write any code yet'" (terminal: shift-tab twice). After a solid plan he auto-accepts edits because "it's just going to one-shot it... almost every time with Opus 4.6" [^src7].
- **Tip 3 — try different interfaces.** Terminal, iOS/Android, desktop, Slack — "there's no one right way to use Claude Code"; and Claude Code "kind of knows about itself, so it can help" edit settings and recommend a setup [^src7].
- **Build for the model 6 months out.** Claude Code's enduring design bet: build for where the model will be, not where it is — accept poor PMF for ~6 months, then "the product is going to click" when the model lands. The inflection arrived with Opus 4 / Sonnet 4 [^src7]. The original Claude CLI demo shocked Cherny by using a bare bash tool to answer "what music am I listening to" with no tool-specific instruction — the seed of the minimal-harness philosophy [^src7].

> **Internal stat:** at Anthropic, Claude reviews 100% of pull requests (with a human review layer after), and per-engineer PR productivity rose ~200% since Claude Code launched [^src7].

## See also

- [[ai-engineering/sources/boris-cherny-100-percent-claude-code|Boris Cherny — 100% Claude Code]] — the full interview source page
- [[ai-engineering/claude-cowork|Claude Cowork]] — the non-developer counterpart to Claude Code
- [[ai-engineering/anthropic|Anthropic]] — model lineup and provider
- [[ai-engineering/agent-skills|Agent Skills]], [[ai-engineering/mcp|MCP]], [[ai-engineering/optimizing-claude|Optimizing a Claude Setup]]

[^src1]: [How Claude Code works in large codebases](../../raw/web/how-claude-code-works-in-large-codebases-best-practices-and.md)
[^src2]: [Model configuration — Claude Code docs](../../raw/web/model-configuration-claude-code-docs.md)
[^src3]: [Catch security issues as Claude writes code — Claude Code docs](../../raw/web/catch-security-issues-as-claude-writes-code-claude-code-docs.md)
[^src4]: [Build your own Developer Tools with Claude Code](../../raw/email/email-2026-05-20-build-your-own-developer-tools-with-claude-code.md)
[^src5]: [Your Claude Code Guide + Tutorials](../../raw/email/email-2026-02-20-your-claude-code-guide-tutorials.md)
[^src6]: [Claude Code 2.1.139 changelog (notes: agent view, /goal)](../../raw/web/tuesday-12-may-claude-code-2-1-139.md) — matins.news
[^src7]: [100% of my code is written by Claude — Boris Cherny (Lenny's Podcast)](../../raw/youtube/youtube-we7bzvkbcvw.md)
[^src8]: [Auto mode for Claude Code](../../raw/notes/notes-clippings-auto-mode-for-claude-code.md) — Anthropic announcement
[^src9]: [Agent view in Claude Code](../../raw/notes/notes-clippings-agent-view-in-claude-code.md) — Anthropic announcement
[^src10]: [A harness for every task: dynamic workflows in Claude Code](../../raw/notes/notes-clippings-a-harness-for-every-task-dynamic-workflows-in-claude-code.md) — Thariq Shihipar & Sid Bidasaria, Anthropic

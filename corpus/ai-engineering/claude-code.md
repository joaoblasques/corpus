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
  - path: raw/notes/notes-clippings-every-claude-code-command-118-the-complete-guide.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-clippings-best-practices-for-using-claude-opus-4-7-with-claude-code.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-clippings-introducing-dynamic-workflows.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-clippings-how-and-when-to-use-subagents-in-claude-code.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-clippings-how-claude-code-works-in-large-codebases-best-practices-and.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-clippings-onboarding-claude-code-like-a-new-developer-lessons-from-17.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-clippings-seeing-like-an-agent-how-we-design-tools-in-claude-code.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-clippings-running-an-ai-native-engineering-org.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-clippings-introducing-routines-in-claude-code.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/web/web-claude-code-for-devops-using-the-loop-skill.md
    channel: web
    ingested_at: 2026-06-17
  - path: raw/web/web-claude-code-routines-8-production-prompts-real-costs-and-whe.md
    channel: web
    ingested_at: 2026-06-17
  - path: raw/web/web-automate-work-with-routines-claude-code-docs.md
    channel: web
    ingested_at: 2026-06-17
  - path: raw/web/web-how-to-set-up-your-coding-agent-a-step-by-step-guide.md
    channel: web
    ingested_at: 2026-06-17
  - path: raw/web/web-claude-code-beginner-advanced.md
    channel: web
    ingested_at: 2026-06-17
  - path: raw/notes/notes-boris-cherny-14-hidden-claude-code-features.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/web/web-auto-mode-for-claude-code-claude.md
    channel: web
    ingested_at: 2026-06-23
  - path: raw/web/web-manage-multiple-agents-with-agent-view-claude-code-docs.md
    channel: web
    ingested_at: 2026-06-23
  - path: raw/web/web-orchestrate-subagents-at-scale-with-dynamic-workflows-claude.md
    channel: web
    ingested_at: 2026-06-23
  - path: raw/_inbox/web-choose-a-permission-mode-claude-code-docs.md
    channel: web
    ingested_at: 2026-06-24
  - path: raw/_inbox/web-automated-security-reviews-in-claude-code-claude-help-center.md
    channel: web
    ingested_at: 2026-06-24
  - path: raw/_inbox/web-push-events-into-a-running-session-with-channels-claude-code.md
    channel: web
    ingested_at: 2026-06-24
  - path: raw/_inbox/email-2026-06-19-anthropic-drops-claude-code-artifacts.md
    channel: email
    ingested_at: 2026-06-24
aliases:
  - Claude Code
  - claude-code
  - Claude Code CLI
  - AskUserQuestion tool
  - TodoWrite
  - Task tool
  - Claude Code Guide agent
  - JIT planning
tags:
  - corpus/ai-engineering
  - entity
created: 2026-06-12
updated: 2026-06-24
---

# Claude Code

**TL;DR.** Anthropic's CLI coding agent that runs locally on the developer's machine. It navigates a codebase the way an engineer would — traversing the file system, reading files, using grep, following references — with no embedding index to build or maintain [^src1]. Its effectiveness is determined as much by the *harness* (CLAUDE.md, hooks, skills, plugins, MCP servers, LSP, subagents) as by the underlying model [^src1]. Model selection, effort levels, and context window are configurable; a security plugin can review code as Claude writes it [^src2][^src3].

## Agentic search vs. RAG indexing

Claude Code uses **agentic search**: each instance works from the live codebase on the developer's machine, with no embedding pipeline or centralized index [^src1]. RAG-powered tools embed the whole codebase and retrieve chunks at query time; at scale those pipelines fall behind active teams, so retrieval can return a function renamed two weeks ago or a deleted module with no indication it is stale [^src1]. The tradeoff: agentic search "works best when Claude has enough starting context to know where to look" [^src1]. A vague query across a billion-line codebase hits context-window limits before work begins, so codebase setup quality bounds navigation quality [^src1].

## Tool design philosophy ("seeing like an agent")

Claude Code's internal tooling decisions are guided by a principle: **design tools that are shaped to the model's abilities, not to what a human would expect** [^src18]. Anthropic's framing: imagine being given a hard math problem — the right tool depends on your skill set. Giving the model tools calibrated to what it can actually do (vs. what seems intuitive to engineers) is the core discipline [^src18].

Three documented tool design episodes from building Claude Code:

**AskUserQuestion tool**: the goal was to improve Claude's ability to ask clarifying questions (elicitation). Two failed attempts — (1) adding a question array to the ExitPlanTool (confused Claude with conflicting semantics) and (2) a modified markdown format (inconsistently produced) — led to a dedicated tool that Claude calls at any point but is especially prompted to use during plan mode [^src18]. Result: structured output with multiple-choice options, blockable loop until user answers. The key criterion: "even the best designed tool doesn't work if Claude doesn't understand how to call it" [^src18].

**TodoWrite → Task tool**: early Claude Code gave Claude a `TodoWrite` tool and injected system reminders every 5 turns to prevent it from forgetting objectives. As models improved (especially Opus 4.5), the todo list became *constraining* — system reminders made Claude think it had to stick to a fixed list rather than adapt when conditions changed. Subagent use also grew, creating coordination problems on a shared list. Solution: replace with a **Task tool** — tasks include dependencies, share updates across subagents, and the model can alter and delete them [^src18]. **Lesson: as model capabilities increase, tools that once helped start getting in the way. Constantly revisit previous assumptions about what tools are needed** [^src18].

**Agentic search replacing RAG**: Claude Code initially used RAG (pre-indexed vector DB, retrieved snippets handed to Claude before each response). RAG was powerful and fast but required indexing, was fragile across environments, and — crucially — Claude was *given* context instead of *finding* it [^src18]. Giving Claude a Grep tool let it build its own context. Combined with progressive disclosure via skills (a skill can reference other files that Claude reads recursively, adding search capabilities layer by layer), "over the course of a year, Claude went from not really being able to build its own context to being able to do nested search across several layers of files to find the exact context it needed" [^src18].

**Progressive disclosure without adding a tool**: Claude Code has ~20 tools and the bar to add a new one is high — each additional tool is one more option the model must reason about [^src18]. When Claude didn't know enough about its own commands (it couldn't answer "how do I add an MCP?"), the options were: (a) add to system prompt (causes context rot, interferes with the main coding job) or (b) progressive disclosure — a link to docs Claude loads when needed. That worked, but Claude pulled large chunks into context to find one-sentence answers. Final solution: the **Claude Code Guide subagent** — a subagent that does the doc-searching in its own context and hands back only the answer. Main agent context stays clean [^src18].

The unifying line: "designing the tools for your models is as much an art as it is a science" — it depends on the model, the agent's goal, and its operating environment. The method: experiment often, read outputs, try new things [^src18].

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

**Organizational layer.** Technical config alone doesn't drive adoption [^src1][^src15]. The fastest rollouts had dedicated infrastructure investment before broad access and a DRI or **agent manager** (a hybrid PM/engineer role) owning conventions, permissions, and the plugin marketplace [^src1]. In large organizations, especially regulated industries, governance questions come up early: who controls which skills and plugins are available, how to prevent thousands of engineers from independently rebuilding the same thing, how to ensure AI-generated code goes through the same review process as human-generated code [^src15]. The smoothest deployments establish cross-functional working groups (engineering, infosec, governance) early and start with a defined set of approved skills, required code review processes, and limited initial access, expanding as confidence builds [^src15].

**Process norms that change when agentic coding becomes the default** (Claude Code team experience) [^src19]: planning shifts from multi-month roadmaps to **just-in-time (JIT)** prototyping — engineering speed changes so fast that a six-month roadmap is stale by month three; context-gathering shifts from "find the person who wrote the code" to "ask Claude that question directly — and ask whether it can be automated"; code review shifts from "humans review everything" to "Claude handles style, bugs, and tests; humans review where domain expertise is irreplaceable" (legal, trust boundaries, product taste). Three metrics for monitoring whether new norms are working: onboarding ramp time (new engineers now ship code in week one), PR cycle time (can expose CI/CD as the new bottleneck), and Claude-assisted commits as a directional signal [^src19].

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

**At-scale real-world example.** Jarred Sumner used dynamic workflows to port Bun from Zig to Rust: 750,000 lines of Rust, 99.8% of the existing test suite passing, eleven days from first commit to merge [^src13]. One workflow mapped the correct Rust lifetime for every struct field in the Zig codebase. A second wrote every `.rs` file as a behavior-identical port of its `.zig` counterpart, hundreds of agents working in parallel with two reviewers on each file. A fix loop then drove the build and test suite until both ran clean. An overnight workflow addressed unnecessary data copies and opened a PR for each finding. This is the orchestration pattern (fan-out-and-synthesize + adversarial verification + loop until done) applied end-to-end [^src13].

**Availability** (as of 2026-06-17): research preview in Claude Code CLI, Desktop, and VS Code extension for Max, Team, and Enterprise plans; also available via the Claude API, Amazon Bedrock, Vertex AI, and Microsoft Foundry [^src13]. Dynamic workflows are on by default for Max/Team/API; Enterprise admins must enable them. The first time a workflow triggers, Claude Code shows a confirmation prompt [^src13].

See [[ai-engineering/agent-harness|Agent Harness]] for the underlying harness concepts, and [[ai-engineering/agentic-workflow|Agentic Workflows]] for the broader workflow patterns.

## Subagents

A subagent is an isolated Claude instance with its own context window: it takes a task, does the work, and returns only the relevant result to the parent conversation [^src14]. Think of them as "the browser tabs of a Claude Code session" — a place to chase a tangent without losing the main thread [^src14]. Multiple subagents can run in parallel, each with different permissions (a research subagent may be read-only; an implementation subagent has full editing access) [^src14].

**Built-in subagent types** in Claude Code [^src14]:
- **General-purpose agents** — complex multi-step tasks
- **Plan agents** — research codebases before presenting implementation strategies
- **Explore agents** — optimized for fast, read-only code search

**When to use subagents** [^src14]:
- *Research-heavy tasks* — gathering context requires reading dozens of files; a subagent synthesizes findings without dumping raw content into the main session
- *Multiple independent tasks* — parallel subagents on tasks with no dependency between them finish faster than sequential execution
- *Fresh perspective* — a subagent starts without conversation history, giving cleaner unbiased review (same effect as `/clear` but without losing the main thread)
- *Verification before committing* — an independent subagent checks for overfitting or missed edge cases
- *Pipeline workflows* — sequential stages (design → implement → test) each benefit from focused attention

Rule of thumb: ten or more files to explore, or three or more independent work items, is a strong signal to delegate to subagents [^src14].

**When NOT to use subagents** [^src14]:
- Sequential work where step two needs the full output of step one
- Same-file edits — two subagents editing the same file in parallel causes conflicts
- Small tasks — overhead of delegation outweighs the benefit
- Too many custom agents — a large roster makes automatic delegation less reliable
- Tasks requiring agents to coordinate with each other — use Agent Teams (agents coordinate across sessions, heavier and more expensive than subagents that only report back to the main conversation)

**Invocation methods** (from simplest to most automated) [^src14]:
1. **Conversational** — ask Claude to "use a subagent to explore how authentication works" or "research these three things in parallel." Specify scope, request parallelization explicitly, and name the output format.
2. **Custom subagents** — markdown files in `.claude/agents/` (project, shared with team) or `~/.claude/agents/` (user, across all projects), each with its own system prompt, tool permissions, and optionally a dedicated model. Create via `/agents` command. The `description` field is what Claude uses to decide when to auto-delegate — "Reviews code for security issues before commits" routes better than "security expert."
3. **CLAUDE.md instructions** — policy for when Claude should reach for specific subagents ("Code reviews ALWAYS use a read-only subagent").
4. **Skills** — `/deep-review` triggers a three-part parallel subagent analysis on staged changes; load on demand, not always-on.
5. **Hooks** — a Stop hook can fire a subagent test suite check and block Claude from finishing until tests pass (the most automated, rightmost approach).

> **Background execution.** Ctrl+B sends a running subagent to the background; the conversation continues and results surface automatically. `/tasks` shows anything running in the background [^src14].

See [[ai-engineering/multi-agent-systems|Multi-Agent Systems]] for the broader orchestration patterns and [[ai-engineering/agent-skills|Agent Skills]] for the skill-based invocation pattern.

## Practitioner workflow (head-of-Claude-Code usage)

Boris Cherny, who leads Claude Code, runs the tool at its full-agentic limit and offers concrete usage tips [^src7]:

- **Parallel sessions ("multi-clouding").** "At the moment I have like five agents running"; "I always have a bunch of agents running" [^src7]. He spreads work across surfaces — "maybe a third of my code now is in the terminal but also a third is using the desktop app and then a third is the iOS app" — all "the same quad agent running everywhere" [^src7]. Designers and non-engineers favor the desktop app's code tab specifically because you can "run as many cloud sessions in parallel as you want" without opening many terminals [^src7].
- **Tip 1 — use the most capable model.** "Just use the most capable model... I have maximum effort enabled always." A weaker model can be *more* expensive: "because it's less intelligent, it actually takes more tokens in the end to do the same task" [^src7]. (See effort levels above and [[ai-engineering/agent-cost-management|Agent Cost Management]].)
- **Tip 2 — plan mode for ~80% of tasks.** "I start almost all of my tasks in plan mode, maybe like 80%." Plan mode is mechanically trivial — "we inject one sentence into the model's prompt to say, 'Please don't write any code yet'" (terminal: shift-tab twice). After a solid plan he auto-accepts edits because "it's just going to one-shot it... almost every time with Opus 4.6" [^src7].
- **Tip 3 — try different interfaces.** Terminal, iOS/Android, desktop, Slack — "there's no one right way to use Claude Code"; and Claude Code "kind of knows about itself, so it can help" edit settings and recommend a setup [^src7].
- **Build for the model 6 months out.** Claude Code's enduring design bet: build for where the model will be, not where it is — accept poor PMF for ~6 months, then "the product is going to click" when the model lands. The inflection arrived with Opus 4 / Sonnet 4 [^src7]. The original Claude CLI demo shocked Cherny by using a bare bash tool to answer "what music am I listening to" with no tool-specific instruction — the seed of the minimal-harness philosophy [^src7].

> **Internal stat:** at Anthropic, Claude reviews 100% of pull requests (with a human review layer after), and per-engineer PR productivity rose ~200% since Claude Code launched [^src7].

## Command taxonomy (118 commands)

Claude Code has 118 commands across four categories [^src11]: **slash commands** (`/init`, `/plan`, `/compact`, etc.) typed inside a running session; **CLI commands** (`claude update`, `claude mcp add`) run in the terminal outside a session; **flags** (`--worktree`, `--permission-mode auto`) added at launch; and **shortcuts** (`Shift+Tab`, `Ctrl+B`) pressed mid-session.

**High-leverage commands most practitioners under-use** [^src11]:

| Command / Flag | What it does | When to use |
|---|---|---|
| `/goal` | Sets a finish condition; Claude works until it's met | Any non-trivial session instead of polling |
| `/workflows` | Watch, pause, and steer a multi-agent workflow | Fan-out / adversarial / parallelizable tasks |
| `/effort` | Single dial for thinking depth (low → ultracode) | Tune tokens vs quality per task |
| `/advisor` | A second model advises on in-progress work | Architecture decisions, ambiguous specs |
| `--max-budget-usd` | Hard session spend cap | Prevent runaway costs on long agentic runs |
| `--worktree` | Isolated worktree per session | Running two or three Claudes in parallel on the same repo |
| `--permission-mode auto` | Auto Mode at launch | Long runs where you've pre-authorized the safe commands |
| `/code-review` | Review diff for bugs; three agents in parallel | Before every push |
| `/btw` | Ask a side question without interrupting the task | Quick lookups mid-session |
| `/schedule` | Recurring run on Anthropic's cloud | Cron-style automations that shouldn't run on your laptop |
| `claude -c` | Resume the most recent session | Daily restart — drops you back with full context |
| `!command` | Execute a shell command; output lands in Claude's context | Running tests, builds, scripts inline |

**The three context rules** that matter most [^src11]: (1) plan first — `/plan` before anything non-trivial saves "twenty minutes of wasted output for thirty seconds of alignment"; (2) guard your context — check with `/context`, compact at 50% usage, reset with `/clear` between unrelated tasks; (3) match the model to the task — Sonnet for 90% of work, Opus when it is genuinely hard, Haiku for bulk.

**Three workflow recipes** [^src11]:
- **Daily setup**: `claude -c` → `/context` → `/plan` → work → `/compact` at 50% → `/clear` between tasks.
- **Safety net**: `git commit` before Claude starts → `/permissions` to pre-allow safe commands once → `/diff` before accepting large batches → `/rewind` when off-track → `/code-review` before push.
- **Autopilot**: `/agents` one specialist per job → `claude --worktree` for parallel Claudes → `/schedule` for recurring cloud runs → `/goal` to define done → `ultracode` for big multi-agent jobs.

New in 2026 (marked ● in the source): `/branch`, `/fork`, `/cd`, `/goal`, `/advisor`, `/tui`, `/reload-skills`, `/reload-plugins`, `--tmux`, `--permission-mode auto`, `--fallback-model`, `--max-budget-usd`, `--bare`, `--safe-mode`, `/usage-credits`, `/insights`, `/release-notes`, `/recap`, `/powerup`, `/workflows`, `/run`, `/verify`, `/run-skill-generator`, `/ultraplan`, `/ultrareview`, `/autofix-pr`, `/deep-research`, `/schedule`, `/stop`, `Ctrl+B`, `/install-slack-app`, `/desktop`, `/mobile`, `/teleport`, `/remote-env` [^src11].

## Routines (scheduled automations)

Routines are a Claude Code automation you configure once — including a prompt, repo, and connectors — and run on a schedule, from an API call, or in response to an event [^src16]. They run on Claude Code's web infrastructure, so nothing depends on your laptop being open. If you've used `/schedule` in the CLI, those tasks are now scheduled routines [^src16].

**Three routine trigger types** [^src16]:

| Type | Description | Example use |
|---|---|---|
| **Scheduled** | Run on a cron cadence (hourly / nightly / weekly) | Nightly: pull top bug from Linear, attempt fix, open draft PR |
| **API-triggered** | Every routine gets its own endpoint + auth token; POST a message, get back a session URL | Alert triage: point Datadog at the endpoint; Claude pulls the trace and has a draft fix ready before on-call opens the page |
| **Webhook (GitHub)** | Subscribe to GitHub repo events; Claude creates one session per matching PR | Flag PRs touching the `/auth-provider` module, summarize and post to `#auth-changes` |

**Daily limits** (research preview, as of mid-2026): Pro — 5 routines/day; Max — 15; Team/Enterprise — 25. Extra routines beyond limits run on extra usage. Routines draw down subscription usage limits in the same way as interactive sessions [^src16].

**Common routine patterns observed** [^src16]:
- *Backlog management*: triage new issues nightly, label, assign, and post a summary to Slack
- *Docs drift detection*: scan merged PRs weekly, flag docs referencing changed APIs, open update PRs
- *Deploy verification*: CD pipeline triggers after each deploy; Claude runs smoke checks and posts go/no-go to release channel
- *Library port*: every PR merged to a Python SDK triggers a routine that ports the change to the parallel Go SDK

See [[ai-engineering/ralph-loop|Ralph Loop]] for the underlying "loop engineering" concept; routines are the native Claude Code implementation of that pattern, without the DIY cron and MCP server management.

### Routines in production: patterns, costs, failure modes

Production experience with routines surfaces failure modes rarely discussed in launch posts [^src20]:

**Cost benchmarks**: a nightly bug-triage routine typically costs $0.20–$0.80; a weekly codebase audit $1.50–$4.00; a CI/CD verify-and-fix routine per PR $0.45–$1.20 [^src20]. Per-daily-run costs add up quickly; set `--max-budget-usd` on long workflows.

**Failure modes to plan for** [^src20]:
- *Loop-break failures*: the routine completes the task but doesn't stop cleanly — session left hanging, accrues idle charges. Always test stop conditions explicitly.
- *Permission failures*: routines need permissions pre-granted. "routine-triggered Claude sessions don't inherit your interactive session's approved permissions" [^src20]. Use `--permission-mode auto` only after auditing what it actually allows.
- *Context contamination*: long-running routines accumulate context rot across many consecutive sessions. Schedule a forced `/compact` or session reset every N runs.
- *Prompt-injection via issue content*: routines that read GitHub issues and act on them are vulnerable to crafted issue text. Sanitize inputs or scope permissions to read-only + specific repo paths [^src20].

### /loop skill for DevOps monitoring

The `/loop` skill (a Claude Code community skill, separate from `/schedule`) enables a local polling loop — running every N minutes inside a running session — for DevOps monitoring workflows that need to stay alive for hours without a cloud routine [^src21].

**Primary use cases** [^src21]:
- Alert queue monitoring: wake on new pages, pull Datadog/PagerDuty context, post triage notes to Slack
- PR watch loop: every 15 min, fetch merged PRs from GitHub API, summarize diff, estimate effort/risk
- Deployment health: poll a health endpoint, report anomalies, escalate on repeated failures

**Key discipline**: set both `interval` and `stop_after` — a loop without an exit condition runs until the session times out. Combine with `/goal` to set a done-condition that breaks the loop early [^src21].

The `/loop` + `/goal` + `/schedule` trilogy is the full local-to-cloud automation ladder: loop for local polling, goal for autonomous agentic runs, schedule for infrastructure-hosted recurring jobs.

## Onboarding Claude Code to a legacy codebase (Skyline case study)

Brendan MacLean (Skyline protein analysis software, 700,000+ lines of C#, maintained 17 years) applied the same methodology he uses for new human developers — onboard through a contained project, expand scope as understanding grows — to Claude Code [^src17].

**Key architecture**: all AI context lives in a separate repository (`pwiz-ai`), kept outside the main codebase so it applies across all branches and time points [^src17]. The `CLAUDE.md` at the root handles environment setup and points to relevant documentation: "the 'lay of the land', not the expertise itself" [^src17]. Expertise lives in skills; skills follow a **"reference don't embed"** principle — each skill points into a central documentation knowledgebase rather than duplicating content, keeping them lightweight [^src17].

**Three headline results** [^src17]:
- A year-long unfinished Files View panel (developer had left) completed by Brendan + Claude Code in two weeks.
- Three years of frozen Java module (LabKey test management) unfrozen; Brendan added features in less than a day.
- Screenshot reproduction for 2,000+ tutorial images now fully automated with diff-only views and pixel change amplification; daily summary email generated automatically each morning from nightly test infrastructure.

**Advice for legacy codebase practitioners** [^src17]:

> "Understand that Claude can't learn without you recording 'context.' Don't expect magic. Invest in building and maintaining your context layer. And treat it like any other project artifact: version it, grow it, maintain it." [^src17]

1. **Context is your best friend.** Context is what persists across sessions; the to-do lists and plans Claude generates do not. "Keeping context in the same repo is a valid alternative; what matters is that it's versioned, maintained, and available when needed" [^src17].
2. **Invest in a skill library.** Use skills to encode domain knowledge any Claude instance can load — debugging skill, version-control conventions skill, project-orientation skill.
3. **Use MCP integrations when data access is key.** Build MCP integrations wherever Claude needs access to real data (test results, exception reports, support threads).

**For open-source projects**: "There's no onboarding budget, no institutional memory beyond what gets written down, no guarantee that any contributor will still be around next year. Context, once built, is available to every contributor and persists across the project's lifetime in a way that human institutional knowledge never does" [^src17]. The `pwiz-ai` repository is itself an open-source artifact — context that belongs to the project, not any one contributor.

## Using Opus 4.7 effectively in Claude Code

Opus 4.7 reasons more after each user turn — improving coherence and coding quality over long sessions but increasing token usage [^src12]. Two behavior modes:

- **Interactive (multi-turn)**: reasons more between turns. Treat it "like a capable engineer you're delegating to, not a pair programmer you're guiding line by line" [^src12].
- **Asynchronous (single-turn)**: more predictable token usage. Well-specified first-turn descriptions (intent, constraints, acceptance criteria, file locations) produce the strongest outputs [^src12].

**Effort levels for Opus 4.7** [^src12]:
- Default is now **`xhigh`** — a new level between `high` and `max` that adds reasoning depth without the runaway token usage `max` can produce on long agentic runs.
- `high` — balances intelligence and cost; use for concurrent sessions.
- `max` — for the hardest evals and non-cost-sensitive work; prone to overthinking.
- `medium`/`low` — cost/latency sensitive work; still outperforms Opus 4.6 at the same level.

**Adaptive thinking.** Fixed thinking budgets are not supported in Opus 4.7. Instead, it uses adaptive thinking — decides per-step whether to use more thinking. To steer: prompt "Think carefully and step-by-step" for more thinking; "Prioritize responding quickly" for less [^src12].

**Behavior changes from Opus 4.6 to 4.7** [^src12]:
- Response length calibrated to task complexity (shorter for lookups, longer for analysis).
- Calls tools less often, reasons more — improve tool-use by explicitly describing when and why each tool should be used.
- Spawns fewer subagents by default — spell out fan-out expectations: "Spawn multiple subagents in the same turn when fanning out across items."

**Auto mode** recommendation: for long-running tasks with full context provided up front, auto mode cuts cycle time; toggle with `Shift+Tab` [^src12].

## Lesser-known flags and features (Cherny's 14)

Boris Cherny's viral X thread (2026) catalogued features "most people use maybe 3 of" [^src22]. Several are already documented above (mobile app, `/loop`, `/schedule`, hooks, worktrees, subagents, `/btw`). The genuinely under-documented entries:

**Verification tip (the most important).** "Give Claude a way to verify its output. Once you do that, Claude will iterate until the result is great" [^src22]. Two concrete mechanisms:

- **Chrome extension** — gives Claude eyes on the browser: it sees what it builds, observes the rendered result, and iterates until the visual output is correct. Cherny calls it his most important tip [^src22].
- **Desktop app built-in browser** — the desktop app bundles a browser that auto-starts your web server and tests it visually, giving a full feedback loop with zero setup [^src22].

**Session branching (`/branch`, `--fork-session`).** `/branch` forks a running session into two, preserving the current context while exploring an alternative approach. Equivalent CLI invocation: `claude --resume --fork-session` [^src22]. This is distinct from `--worktree` (file isolation) — `/branch` is context isolation without a new working tree.

**`/batch`.** Interviews the user, then fans out the work to as many worktree agents as needed — "dozens, hundreds, even thousands." Designed for large code migrations and any parallelizable work [^src22]. Complements `/workflows` (programmer-defined fan-out) with a conversational dispatch interface.

**`--bare`.** Skips auto-loading of `CLAUDE.md`, settings, and MCP servers. Approximately 10x faster startup. Intended for non-interactive usage and SDK automations where you explicitly specify what to load instead of relying on auto-discovery [^src22].

**`--add-dir`.** Grants Claude access (full read/write) to additional folders or repositories beyond the working directory. Also usable mid-session as `/add-dir` [^src22].

**`--agent` (custom agent loader).** Loads a custom system prompt and tool set from `.claude/agents/<name>` at launch — defining specialized agents (reviewer, deployer, researcher) each with scoped rules and tools. Cherny calls it "the most overlooked feature in Claude Code" [^src22]. (Note: custom agent *files* are documented above in the Subagents section; `--agent` is the CLI flag to load one at startup without entering a general session first.)

**Cowork dispatch.** Secure remote control of your entire laptop via Claude Code — not just code, but Slack, file management, any desktop action. Cherny uses it daily when away from his computer [^src22]. See [[ai-engineering/claude-cowork|Claude Cowork]] for the full product page.

## Permission modes

Claude Code supports six permission modes that control how autonomously Claude acts [^src23]:

| Mode | Behavior |
|---|---|
| **default** | Prompts before most tool calls; safest for interactive use |
| **acceptEdits** | Auto-accepts file edits; still prompts for commands |
| **plan** | Read-only; proposes a plan without executing it |
| **auto** | Fully autonomous — no prompts; uses judgment on risky operations |
| **dontAsk** | Never pauses; less permission-aware than auto |
| **bypassPermissions** | No safety checks; for scripted/CI contexts only (API only) |

**Auto mode requirements** [^src23]: minimum Claude Code v2.1.83; Opus 4.6+ or Sonnet 4.6 (Bedrock/Vertex: Opus 4.7+/4.8); Team/Enterprise plan with admin-enabled access. Modes are set through controls, not by asking Claude in the chat.

**Auto mode classifier defaults** — auto-mode blocks these actions by default [^src23]:
- Shell commands piped directly into bash (`curl | bash` pattern)
- Sending sensitive data to external services
- Production deploys in critical-path workflows
- Mass file deletion
- Force-pushing to `main`

## /security-review command and GitHub Action

The `/security-review` command scans the current session's code changes for vulnerabilities including SQL injection, XSS, authentication flaws, insecure data handling, and dependency vulnerabilities [^src24]. Available to all Claude Code users (Pro/Max/Team/Enterprise/API).

Two delivery modes [^src24]:
- **In-session**: type `/security-review` during a coding session to scan current changes.
- **GitHub Action**: install the Claude Code GitHub Action in a repository for automatic PR security review; results post as inline comments on each PR.

## Channels (push events into a running session)

Channels lets external services push events into a live Claude Code session, enabling reactive automation without polling [^src25]. Research preview as of mid-2026; requires Anthropic auth (not Bedrock/Vertex/Foundry).

**Supported integrations** (all run as Bun plugins) [^src25]:
- **Telegram** — a Claude bot in a Telegram channel
- **Discord** — a Claude bot in a Discord server
- **iMessage** — receive and act on iMessages in a Claude session

Enable with the `--channels` flag at session start. Team/Enterprise admins must enable `channelsEnabled` in org settings; optionally configure a sender allowlist.

**Comparison with other event mechanisms** [^src25]:

| Mechanism | State | Best for |
|---|---|---|
| Web sessions / Slack | No session state | Notifications |
| Standard MCP | Per-call | Tool integrations |
| Remote Control | Persistent session | Remote laptop access |
| **Channels** | Persistent session | External event-driven workflows |

## Artifacts (coding session as a live shareable page)

Claude Code Artifacts turn a coding session into a **live, shareable web page** using the full session context — codebase, connectors, and conversation [^src26].

**Use cases** [^src26]:
- PR walkthroughs that update as the PR evolves
- Team dashboards pulling from connected data sources
- Incident timelines that update in real time

Artifacts are private to the org by default. Beta available to Team and Enterprise plan users.

## See also

- [[ai-engineering/sources/boris-cherny-100-percent-claude-code|Boris Cherny — 100% Claude Code]] — the full interview source page
- [[ai-engineering/claude-cowork|Claude Cowork]] — the non-developer counterpart to Claude Code
- [[ai-engineering/anthropic|Anthropic]] — model lineup and provider
- [[ai-engineering/claude-managed-agents|Claude Managed Agents]] — cloud-hosted agent runtime; integrates via built-in `claude-api` skill
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
[^src11]: [Every Claude Code Command (118) — The Complete Guide](../../raw/notes/notes-clippings-every-claude-code-command-118-the-complete-guide.md) — Charlie Hills / charliehills.substack.com
[^src12]: [Best practices for using Claude Opus 4.7 with Claude Code](../../raw/notes/notes-clippings-best-practices-for-using-claude-opus-4-7-with-claude-code.md) — Anthropic
[^src13]: [Introducing dynamic workflows](../../raw/notes/notes-clippings-introducing-dynamic-workflows.md) — Anthropic
[^src14]: [How and when to use subagents in Claude Code](../../raw/notes/notes-clippings-how-and-when-to-use-subagents-in-claude-code.md) — Anthropic
[^src15]: [How Claude Code works in large codebases: Best practices and where to start](../../raw/notes/notes-clippings-how-claude-code-works-in-large-codebases-best-practices-and.md) — Anthropic Applied AI team
[^src16]: [Introducing routines in Claude Code](../../raw/notes/notes-clippings-introducing-routines-in-claude-code.md) — Anthropic
[^src17]: [Onboarding Claude Code like a new developer: Lessons from 17 years of development](../../raw/notes/notes-clippings-onboarding-claude-code-like-a-new-developer-lessons-from-17.md) — Brendan MacLean / MacCoss Lab / Anthropic case study
[^src18]: [Seeing like an agent: how we design tools in Claude Code](../../raw/notes/notes-clippings-seeing-like-an-agent-how-we-design-tools-in-claude-code.md) — Thariq Shihipar, Anthropic
[^src19]: [Running an AI-native engineering org](../../raw/notes/notes-clippings-running-an-ai-native-engineering-org.md) — Anthropic (Claude Code team lead)
[^src20]: [Claude Code Routines: 8 Production Prompts, Real Costs and When Things Break](../../raw/web/web-claude-code-routines-8-production-prompts-real-costs-and-whe.md) — Alex Newman
[^src21]: [Claude Code for DevOps: Using the /loop skill](../../raw/web/web-claude-code-for-devops-using-the-loop-skill.md) — DevOps practitioner guide
[^src22]: [Boris Cherny: 14 hidden Claude Code features](../../raw/notes/notes-boris-cherny-14-hidden-claude-code-features.md) — Boris Cherny / X thread, 2026
[^src23]: [Permission modes (Claude Code docs)](../../raw/_inbox/web-choose-a-permission-mode-claude-code-docs.md) — Anthropic
[^src24]: [Automated security reviews in Claude Code](../../raw/_inbox/web-automated-security-reviews-in-claude-code-claude-help-center.md) — Anthropic Help Center
[^src25]: [Push events into a running session with Channels](../../raw/_inbox/web-push-events-into-a-running-session-with-channels-claude-code.md) — Anthropic, Claude Code docs
[^src26]: [Claude Code Artifacts (email announcement)](../../raw/_inbox/email-2026-06-19-anthropic-drops-claude-code-artifacts.md) — Anthropic

---
type: synthesis
domain: ai-engineering
status: draft
sources:
  - path: raw/web/the-code-agent-orchestra-what-makes-multi-agent-coding-work.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/vibe-coding-is-dangerous-agentic-engineering-isn-t-ft-wes-mc.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/agent-experience-is-the-new-developer-experience.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/beyond-the-prompt-claude-code.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-05-28-may-must-reads-vibe-coding-token-economics-and-more.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-05-21-goal-landed-here-s-how-to-use-it.md
    channel: email
    ingested_at: 2026-06-15
aliases:
  - agentic coding
  - agentic engineering
  - coding agents
  - agent orchestration
  - conductor to orchestrator
  - agent experience
  - AX
  - 8 levels of AI-assisted coding
  - /goal
  - goal mode
  - let Claude prompt Claude
tags:
  - corpus/ai-engineering
  - synthesis
created: 2026-06-12
updated: 2026-06-15
---

# Agentic Coding

**TL;DR**: Agentic coding is the discipline of orchestrating one or more coding agents to ship software, as distinct from *vibe coding* (one-prompt-and-ship without reading the code) [^src2]. The shift over 2025–2026 is **from conductor (one agent, synchronous, your context window as ceiling) to orchestrator (many agents, asynchronous, the codebase as canvas)** [^src1]. The bottleneck moves from *generation* to *verification* [^src1], and the new leverage is your *spec* and your *taste* [^src1] [^src2]. This page is the sub-hub for coding-agent pages: see [[ai-engineering/agent-harness|Agent Harness]], [[ai-engineering/agent-skills|Agent Skills]], and [[ai-engineering/multi-agent-systems|Multi-Agent Systems]].

## Vibe coding vs agentic engineering

Wes McKinney (creator of Pandas, Apache Arrow) draws a hard line: *vibe coding* means "you just one-prompt it, don't look at the code, and ship it" — which he calls "very dangerous and irresponsible" [^src2]. *Agentic engineering* is the opposite: heavy up-front specification, architecture, and review [^src2]. **"We can't disengage from planning and writing specs. We can move much faster, but don't vibe code"** [^src2]. He spends hours in the spec phase, refuses to start implementing without knowing clearly how it fits together, and stresses that "automated code review certainly helps, but it isn't a substitute for engineering experience" [^src2]. The broader field framing (Towards Data Science, May 2026): the move "from vibe coding to spec-driven development" as the field enters "the age of agentic engineering" [^src5].

## The 8 levels and the conductor→orchestrator shift

Steve Yegge's framework of **8 levels of AI-assisted coding** maps how developers evolve; most are stuck at Level 3–4, the orchestration tier starts at Level 6, and it requires a fundamentally different skill set than what got you to Level 5 [^src1].

The core mental-model shift [^src1]:

- **Conductor** — one agent, synchronous, sequential; your context window is a hard ceiling. Tools: Claude Code CLI, Cursor agent mode.
- **Orchestrator** — many agents, each with its own context window, working asynchronously while you plan, assign, and check in. Tools: Agent Teams, Conductor, Codex, Copilot Coding Agent.

The skills that matter become clear specs, work decomposition, and output verification — "just like managing a real team" rather than writing code yourself [^src1].

### Why multi-agent

Four compounding (multiplying, not additive) reasons: **parallelism** (3× throughput), **specialization** (each agent only sees the files it owns — an agent that only knows `db.js` writes better DB code than a generalist), **isolation** (git worktrees, no merge conflicts), and **compound learning** (an `AGENTS.md` accumulates patterns across sessions) [^src1]. Detailed orchestration patterns — subagents, hierarchical teams-of-teams, Agent Teams with shared task lists and peer messaging, and the three orchestration tiers — live in [[ai-engineering/multi-agent-systems|Multi-Agent Systems]].

## The bottleneck has shifted: generation → verification

**"The bottleneck is no longer generation. It's verification"** [^src1]. Agents produce impressive output fast; knowing whether it's correct is the hard part. Tests that pass before a change don't guarantee they catch regressions from it; agents write technically-valid tests that miss the cases that matter; and flaky environments become *systemic* blockers when forty agents hit the same flaky test at once [^src1]. Until verification infrastructure catches up, human review isn't optional overhead — it's the safety system [^src1].

### Quality gates: trust but verify

Three gates make agent output trustworthy [^src1]:

- **Plan approval** — require a written plan before coding; it's far cheaper to fix a bad plan than bad code.
- **Hooks** — automated checks on lifecycle events (a `TaskCompleted` hook runs lint/tests before marking done; if it fails the agent keeps working). See the hooks discussion in [[ai-engineering/agent-harness|Agent Harness]].
- **`AGENTS.md` for compound learning** — captures patterns and gotchas; every session reads it and adds to it.

A notable empirical caveat on `AGENTS.md`: research (Gloaguen et al., ETH Zurich) found **LLM-generated `AGENTS.md` files offer no benefit and can marginally reduce success (~3%) while raising inference cost by 20%+, whereas developer-written context files give ~4% improvement** [^src1]. The lead must approve every line; never let an agent write to `AGENTS.md` directly [^src1].

## Agent Experience (AX) is the new Developer Experience

Builder.io frames **agent experience (AX)** as "the discipline of designing the layer between a model and a real codebase: the context, tools, permissions, tests, and review loops that tell the agent what matters, what it can touch, and how it knows it worked" [^src3]. The key premise: agents are "completely stateless tools," not wizards — "a stateless agent will walk directly into the same architectural wall five times in a row unless the system around it provides a better feedback loop" [^src3]. Core tenets [^src3]:

- **Context like good code** — minimal (point back to the code itself), transparent (a reviewer can audit which rule shaped the work), tested. Teams otherwise accumulate "a graveyard of skills, AGENTS.md rules, stale definitions" [^src3].
- **Deterministic environment** — "the environment is literally part of the prompt." A human who hits a missing env var stops and investigates; "an agent will route around the failure, change the wrong file, and ship a guess with a polite commit message" [^src3].
- **Prove the work** — agents should present evidence (tests, screenshots, browser flows, logs) before handoff. **"Spend tokens before spending reviewer attention"** — tokens are cheap and 24/7; senior focus is precious and burns out [^src3].
- **Structural safety** — "Good DX made dangerous actions hard. Good AX needs to make dangerous actions impossible." Prompts like "don't mess with the database!" are bypassable; safety must be sandboxing, scoped credentials, and human-in-the-loop gates [^src3].
- **Codebase as the source of truth** — a messy codebase makes the agent "synthesize that confusion into elegant-looking garbage"; deep modules with thin interfaces are "progressive disclosure for machines" [^src3]. (Echoes [[ai-engineering/agent-skills|Agent Skills]] progressive disclosure.)

The organizing line: **"LLMs should do the glue work. People should do the interesting work"** [^src3].

## Claude Code as the reference harness for agentic coding

A practitioner deep-dive on running Claude Code "as a programmable agent, not dressed-up autocomplete" surfaces the day-to-day mechanics [^src4]. The single highest-leverage move, per Boris Cherny: **give the agent a way to verify its own work** — Boris pegs this at a 2–3× quality bump [^src4]. Other load-bearing patterns:

- **Explore → plan → code** — plan mode is read-only; treat the plan like a design doc and have a *second* fresh Claude review it as a staff engineer [^src4].
- **Delegate, don't pair-program** — Cat Wu: "The model performs best if you treat it like an engineer you're delegating to, not a pair programmer you're guiding line by line" [^src4].
- **Compounding `CLAUDE.md`** — "Update CLAUDE.md so you don't repeat this" after every mistake; Boris calls Claude "eerily good at writing rules for itself," and frames every PR review becoming a rule as **"Compounding Engineering"** [^src4]. The team's own `CLAUDE.md` is edited multiple times a week and is "a curated list of every gotcha," with no style preferences or codebase tours [^src4].
- **The `.claude/` directory** is a layered config system — project scope (`.claude/`, committed) vs global (`~/.claude/`); files describe either the project or you; `CLAUDE.md` cascades in monorepos and `rules/*.md` is path-gated [^src4].
- **Parallel sessions** across 3–5 git worktrees are called "the single biggest productivity unlock," with the agent view as a control plane [^src4].
- **`/goal` = the Ralph Loop built in** — sets a verifiable completion condition and grinds until it holds; "Pick something verifiable and deterministic... Write 'the code is good' and you've already lost" [^src4]. See the Ralph Loop in [[ai-engineering/agent-harness|Agent Harness]].

This source also grounds [[ai-engineering/agent-skills|Agent Skills]] (skills as "the unit of reusable expertise"), subagents, plugins, and [[ai-engineering/mcp|MCP]] as the layers above the prompt.

## Delegate the tasks, not the judgment

The unifying discipline across sources: let agents handle scoped tasks with tight pass/fail criteria (boilerplate, migrations, test scaffolding), and keep for yourself architecture, "deciding what NOT to build," and review with full system context [^src1]. McKinney's version: **"When code is free, saying no is our last defense"** — every feature is cheap to create but expensive to maintain [^src2]. What differentiates output between two people using the same model is *taste* — "100s or 1000s of small decisions, essentially manifesting one's taste" [^src2]. And because vague thinking *multiplies* across a parallel fleet, "strong software engineers get more leverage from these tools than weak ones" — the spec is "product thinking made explicit" [^src1].

> **Cost-per-token / token economics**: McKinney runs ~$20,000/month at API rates and argues paying the *true* cost of tokens (usage-based, not subsidized subscriptions) is healthy because it makes "AI slop and low-value projects go away" [^src2]. He built AgentsView partly to measure token spend vs value generated — potentially a performance-review signal [^src2]. The May 2026 field roundup similarly flags token economics and token-saving techniques (caching, lazy-loading, routing, compaction) as a headline theme [^src5].

## `/goal` and the "let Claude prompt Claude" default

The clearest sign of the conductor→orchestrator shift is goal-mode execution. Anthropic shipped **`/goal`** (Claude Code v2.1.139): you give a *done-condition* and Claude runs turns until it thinks it's met, showing elapsed time, turn count, and tokens [^src6]. Boris Cherny's framing at Code with Claude: **"The default is no longer 'I prompt Claude Code.' The default now is 'I let Claude prompt Claude Code.'"** [^src6]. It is the same idea as the **Ralph Loop** (see [[ai-engineering/multi-agent-systems|Multi-Agent Systems]]) and Codex's months-old equivalent; Cherny's prior tool of choice was `/loop` — "point Claude at a cron, walk away... loops are the future" [^src6].

The discipline that makes goals work is **writing the goal so it can't be gamed** [^src6]:
- **Name the task, list the loopholes, name the check.** A weak goal ("fix the type error so it works on Node 24") got "fixed" with a `// @ts-expect-error` — error gone, code unchanged. The rewrite spells out forbidden moves ("must not use ts-expect-error, ts-ignore, or any type assertion") and the verification ("run pnpm typecheck and confirm zero errors before declaring done") [^src6].
- **"If a goal has a loophole, Claude will use it."** "Make the test pass" is permission to delete the test; pair every condition with a constraint ("without disabling, skipping, or weakening any test") or run on a worktree [^src6].

Three things to watch: **token spend** (a multi-hour Opus loop isn't free; set a soft budget like `--tokens 250K` — sharper after programmatic Claude Code moved to API rates on 2026-06-15), the **review queue** (overnight `/goal` runs produce PRs nobody scoped — write a machine-authored-PR policy first), and **blast radius** [^src6]. Robobun (an agent with more Bun commits than Bun's creator) and the two-reviewers-on-one-PR setup (CodeRabbit for style + Claude for cross-file reasoning) are the production exemplars [^src6]. This is the structural sibling of the **reconcile** self-improvement move in [[ai-engineering/learning-ai-engineering|Learning AI Engineering]] and the verification loop in [[ai-engineering/agent-testing|Agent Testing]].

## How developers still learn

An open tension McKinney raises: if seniors no longer write much code (he reviews, guides, adds taste), how do we *develop* seniors? His answer — "the hard labour goes away, which is where we usually learn" (learning by osmosis) — so the focus must shift to design patterns and architecture, to have "the technical vocabulary to guide or understand the agents" [^src2].

## See also

- [[ai-engineering/agent-harness|Agent Harness]] — the scaffolding (hooks, loops, context policies) every coding agent runs inside
- [[ai-engineering/agent-skills|Agent Skills]] — reusable expertise units; progressive disclosure
- [[ai-engineering/multi-agent-systems|Multi-Agent Systems]] — subagents, Agent Teams, orchestration tiers, Ralph Loop
- [[ai-engineering/context-engineering|Context Engineering]] — supply unique workflow, not general knowledge
- [[ai-engineering/mcp|MCP]] — connecting agents to external systems
- [[ai-engineering/ai-agent|AI Agent]] — the ReAct loop and agent fundamentals
- [[software-engineering/ai-assisted-development|AI-Assisted Development]] (software-engineering) — the software-craft counterpart: fundamentals, the write→review shift, deterministic guardrails
- [[ai-engineering/README|AI Engineering hub]]

---

[^src1]: [The Code Agent Orchestra — what makes multi-agent coding work](../../raw/web/the-code-agent-orchestra-what-makes-multi-agent-coding-work.md) — Addy Osmani (O'Reilly AI CodeCon talk)
[^src2]: [Vibe Coding is Dangerous, Agentic Engineering Isn't (ft. Wes McKinney)](../../raw/web/vibe-coding-is-dangerous-agentic-engineering-isn-t-ft-wes-mc.md) — MotherDuck interview
[^src3]: [Agent Experience Is the New Developer Experience](../../raw/web/agent-experience-is-the-new-developer-experience.md) — Builder.io
[^src4]: [Beyond the Prompt: Claude Code Mastery](../../raw/web/beyond-the-prompt-claude-code.md) — arps18 (synthesizing Boris Cherny, Cat Wu, Anthropic team)
[^src5]: [May Must-Reads: Vibe Coding, Token Economics, and More](../../raw/email/email-2026-05-28-may-must-reads-vibe-coding-token-economics-and-more.md) — Towards Data Science newsletter
[^src6]: [/goal landed. Here's how to use it](../../raw/email/email-2026-05-21-goal-landed-here-s-how-to-use-it.md) — Abhishek, Claude Code Camp (on Code with Claude, Boris Cherny, `/goal`)

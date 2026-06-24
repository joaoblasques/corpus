---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/web/long-running-agents.md
    channel: web
    ingested_at: 2026-06-16
  - path: raw/notes/notes-10-autonomous-background-coding-agents.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/_inbox/web-rakuten-claude-managed-agents-case-study-claude-by-anthropic.md
    channel: web
    ingested_at: 2026-06-24
  - path: raw/_inbox/web-assign-tasks-from-anywhere-in-claude-cowork-claude-help-cent.md
    channel: web
    ingested_at: 2026-06-24
aliases:
  - long-running agent
  - long-running agents
  - long-running execution
  - persistent agency
  - long-horizon reasoning
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-16
updated: 2026-06-24
---

# Long-Running Agents

**TL;DR.** A long-running agent "can keep making progress over hours, days, or weeks... across many context windows and sandboxes, recover from failure, leave structured artifacts behind, and resume where it left off." [^src1] It supersedes the chat-window-with-a-loop paradigm, which has a ceiling: the model forgets, declares tasks complete prematurely, and reintroduces fixed bugs [^src1]. The engineering centers on a state layer living *outside* the model's context window plus designed session-to-session handoffs [^src1]. Google, Anthropic, and Cursor have converged on the same shape: separate the model loop from the execution sandbox from the durable session log [^src1].

## Three meanings of "long-running"

The term blurs three distinct things [^src1]:

- **Long-horizon reasoning** — planning/executing over many dependent steps; mostly a model-quality story. METR's time-horizon metric (length of task a model completes at 50% reliability) has doubled roughly every seven months since 2019; on that curve frontier agents hit day-scale tasks by 2028 and year-scale by 2034 [^src1].
- **Long-running execution** — the process runs for hours or days, with the model invoked thousands of times; mostly a [[ai-engineering/agent-harness|harness]] story [^src1].
- **Persistent agency** — an identity that outlives any single task, accumulating memory and preferences; the "Memory Bank" flavor [^src1].

Production agents blend all three, but the engineering problems and the products that solve them differ [^src1].

## Why it matters

- **Economic phase change.** A ten-minute agent answers a question; a ten-hour agent can own a feature or a six-quarter-backlog migration [^src1]. Anthropic reported 30+ hours of autonomous coding in internal tests, including one run producing an 11,000-line Slack-style app [^src1].
- **Persistence changes what the agent is.** A stateless agent answers and disappears; a long-running one accumulates context across weeks [^src1]. Anthropic's Project Vend ran a Claude instance as an actual vending business for a month, surfacing the "weird coherence problems" of maintaining identity across weeks rather than turns [^src1].

## The three walls

Long-running designs are mostly answers to three recurring problems [^src1]:

1. **Finite context.** Even a 1M-token window fills, and [[ai-engineering/context-window-management|context rot]] degrades performance well before the hard limit; a 24-hour run will not fit any window on the roadmap [^src1].
2. **No persistent state.** A new session starts blank — "imagine a software project staffed by engineers working in shifts, where each new engineer arrives with no memory of what happened on the previous shift." [^src1]
3. **No self-verification.** Models skew positive grading their own work, so without a separate signal you get "the agent that ships at 30% complete with full confidence" [^src1].

## Architectural patterns

- **The [[ai-engineering/ralph-loop|Ralph loop]].** The simplest practitioner version — a Bash loop where `prd.json` is the plan and `progress.txt` is the lab notes, state on disk [^src1]. See its own page.
- **Anthropic — harness, then brain/hands/session.** An initializer agent sets up the environment and writes a `feature-list.json` + `init.sh`; a coding agent is woken repeatedly to make incremental progress, run tests, leave a `claude-progress.txt`, and commit, with a "test ratchet" forbidding editing/removing tests [^src1]. The "Decoupling the brain from the hands" architecture splits the **Brain** (model + harness loop), **Hands** (sandboxed ephemeral execution), and **Session** (append-only event log); a fresh container calls `wake(sessionId)` to reconstitute state, and decoupling dropped time-to-first-token ~60% at p50 and over 90% at p95 [^src1]. "Every component in a harness encodes an assumption about what the model can't do on its own." [^src1]
- **Cursor — planners, workers, judges.** After a flat lock-based model bottlenecked and an optimistic-concurrency version didn't fix coordination, Cursor's production design uses **planners** (explore the codebase, emit tasks, recursively spawn sub-planners), **workers** (focused executors that don't coordinate), and **judges** (decide when an iteration finishes/restarts) [^src1]. Notable findings: "a surprising amount of the system's behavior comes down to how we prompt the agents," and different models slot into different roles — a GPT model beat Opus for extended autonomous work because Opus "tended to stop early and take shortcuts" [^src1].
- **Google — Agent Platform.** Cloud Next '26 folded Vertex AI into the Gemini Enterprise Agent Platform, productizing long-running agents with SLAs: Agent Runtime (runs "for days at a time," sub-second cold starts), Agent Sessions (pinnable to custom session IDs), Agent Memory Bank (persistent curated long-term memory with a search API), Agent Sandbox, plus orchestration/registry/identity/gateway/observability services [^src1]. Architecturally "the same brain/hands/session split... just productized at platform scale." [^src1]

The session-as-event-log is the underappreciated part: it is what makes a run recoverable, debuggable, and auditable [^src1].

## Five production patterns

Osmani and Shubham Saboo distill five patterns separating working long-running agents from demos [^src1]:

1. **Checkpoint-and-resume** — write intermediate state to disk and checkpoint every N units; the common multi-day failure is context loss (error on document 201 of 200, restart from scratch) [^src1].
2. **Delegated approval (human-in-the-loop)** — let the agent pause in place with full execution state intact, consume zero compute while a human takes hours, then resume with sub-second latency [^src1].
3. **Memory-layered context** — long-term memory plus low-latency lookups; the production failure mode is *memory drift* (learning a shortcut from atypical interactions and over-applying it), so "govern memory like you govern microservices" [^src1].
4. **Ambient processing** — event-driven agents on a stream/table; don't hardcode policy into the agent, define it in a gateway so a fleet picks up changes without redeploys [^src1].
5. **Fleet orchestration** — a coordinator delegating to specialists, each with its own identity/policy/registry entry — the classic coordinator/worker shape, now handled declaratively [^src1].

## How to build one today

By use case [^src1]:

- **Coding on your own repo** — just use [[ai-engineering/claude-code|Claude Code]] (or Antigravity/Cursor/Codex); treat `AGENTS.md` "like a pilot's checklist," add typecheck/lint hooks, write a plan file, use the Ralph loop when you don't believe "done," and run in a worktree so a closed laptop doesn't kill the run [^src1].
- **Hosted agent product** — "Don't build the runtime. Pick a managed one" (Google Agent Platform, Claude Managed Agents, or self-host on ADK / Claude Agent SDK / Codex SDK) [^src1].
- **Autonomous/operational (monitoring, research, ops)** — Memory-Bank-style persistence (ADK + Memory Bank + Cloud Run + Cloud Scheduler) [^src1].

Cross-cutting moves: write the done-condition before the agent starts ("the single highest-leverage move"); separate the evaluator from the generator; invest in the session log, not just the prompt; and treat compaction and full context resets as first-class — Anthropic found summarization-as-compaction insufficient for very long jobs and used full context resets rebuilt from a structured handoff file [^src1].

## Autonomous background agents (copilot→autopilot shift)

Ch10 of *Beyond Vibe Coding* offers the practitioner framing of the same architecture from the user's perspective. The key distinction: traditional AI coding assistants are *supervised coding agents* — interactive, synchronous, bounded by the current file or function. Autonomous background coding agents are *asynchronous* — you give them a high-level task, they work independently in an isolated sandbox (cloud VM or container), and deliver a PR [^src2].

The **plan → execute → verify → report** cycle [^src2]:
1. **Plan** — agent parses the task, breaks it into substeps, sometimes shows you the plan for approval (Jules, notably). The planning phase is "the AI's way of reasoning about how to accomplish your goal before diving in."
2. **Execute** — reads and modifies code across multiple files. Agents often use brute-force text search (grep) to find relevant parts of the codebase — surprisingly effective despite more sophisticated options existing.
3. **Verify** — runs the test suite iteratively until tests pass, or reports environment failures. This closes the generate→debug→validate loop without a human in the loop.
4. **Report** — delivers a PR; human reviews and may request another iteration.

**Tool landscape in 2025** [^src2]:
- *OpenAI Codex* — cloud CLI, RL-trained on real coding tasks; runs CI-like sandboxes; optional internet access for package/doc fetches.
- *Google Jules* — GitHub-integrated; presents plan before executing; runs on Google Cloud VMs; "plan, then execute" philosophy.
- *Cursor background agents* — IDE-integrated hybrid; remote Ubuntu with internet access; developer can "enter the machine" midtask.
- *Devin (Cognition Labs)* — Slack+GitHub+Jira "AI teammate"; parallel execution of maintenance tasks; automatic preview deployments.

**The generator vs. reviewer asymmetry** [^src2]: using background agents shifts human effort from *writing code* to *writing a good task description* and then *reviewing the output*. Generating a solution from scratch is hard; reviewing and refining it is easier. This is a productivity lever, but it means **code review skills appreciate in value**.

**New challenge: compounding errors** [^src2]: unlike interactive AI assistance where humans intervene at each step, autonomous agents make chains of decisions that can compound. An agent that misinterprets the initial requirements doesn't just generate one flawed function — it builds an "entire implementation architecture" on that misunderstanding, creating "coherent incorrectness": internally consistent code that is fundamentally misaligned with actual needs.

**Best practice: strategic task selection** [^src2]. Agents excel at well-bounded, measurable work: comprehensive test coverage improvements, systematic dependency updates, bulk refactoring, standardized feature implementations across multiple components. Tasks requiring significant architectural decisions, complex stakeholder interpretation, or novel algorithm design remain better suited to human-led development.

## Organizational challenges specific to autonomous agents

Ch10 surfaces challenges that don't arise with interactive AI tools [^src2]:

- **Review bottleneck amplification** — agent PRs arrive as complete implementations (not incremental suggestions), often multiple PRs simultaneously after overnight runs. Reviewing requires reconstructing the agent's "reasoning" from the code, not from a colleague's thought process.
- **Async coordination paradox** — running more agents in parallel to increase productivity makes integrating them more complex. Agents lack the implicit communication channels humans use ("Are you touching the auth module?"). Agent A refactors a utility; Agent B adds calls to the old version; neither knows.
- **Environmental brittleness** — five concurrent agents may have slightly different Node versions, missing system libraries, or different timezone settings in their sandboxes. These variations surface as subtle bugs only during integration ("environmental drift").
- **Trust model shift** — delegating to an agent with write access and execution capabilities is different from accepting a suggestion. A compromised or misdirected agent doesn't just *suggest* bad code — it *commits* it, and potentially *deploys* it.

## Limitations

Still genuinely unsolved [^src1]: **cost** (a 24-hour frontier run can "quietly burn through a week's API budget in an afternoon" without budgets/circuit breakers — see [[ai-engineering/agent-cost-management|Agent Cost Management]]); **security** (a larger attack surface; the brain/hands split keeps credentials unreachable from the sandbox); **alignment drift** (goals lose fidelity across re-summarization); **verification** (auditing 24 hours of activity is a human-time problem); and **the human role** — "the skill that's appreciating in value isn't writing code. It's writing specs that survive contact with an autonomous executor." [^src1]

## Goal-based delegation for long-running agents (Rakuten)

Rakuten's deployment highlights the most important mindset shift for getting value from long-running agents: **delegate goals, not tasks** [^src3]. Yusuke Kaji (GM AI for Business): previous AI deployments were task-based ("do this specific action") — that led to brittle, micro-managed agent loops. Goal-based delegation ("here's what success looks like for this business function") lets agents decide the intermediate steps, adapt when blocked, and learn across sessions.

The result: agents that accumulate organizational knowledge via memory. "Individual learning becomes organizational learning instantly" — when one agent learns that a specific format fails with a specific vendor's system, that learning persists in the memory store and every subsequent agent for that customer benefits [^src3].

Specialist agents (engineering/product/sales/marketing/finance) were deployed within one week each; each learns from every session via built-in memory; 97% drop in first-pass critical errors across the fleet [^src3].

## Phone-to-desktop persistent sessions (Cowork Dispatch)

**Dispatch** (Pro/Max beta) extends the long-running agent pattern to cross-device persistence: a single conversation thread lives across mobile and desktop, so delegating a task from your phone to a Claude Code or Cowork session on your desktop isn't a separate handoff — it's the same persistent context [^src4]. This operationalizes the `wake(sessionId)` pattern from [[ai-engineering/claude-managed-agents|Claude Managed Agents]] Brain-Hands-Session architecture: the phone is the human-in-the-loop checkpoint, and the desktop is the execution environment. Push notifications handle the async completion loop.

## See also

- [[ai-engineering/agentic-coding|Agentic Coding]] — the conductor→orchestrator shift that autonomous agents represent
- [[ai-engineering/agent-testing|Agent Testing]] — verification loops become more important, not less, with autonomous agents
- [[ai-engineering/agent-security|Agent Security]] — trust model implications; autonomous agents as a larger attack surface
- [[ai-engineering/sources/beyond-vibe-coding-book|Beyond Vibe Coding (Book)]] — ch10 as primary source for the copilot→autopilot framing

[^src1]: [Long-running Agents](../../raw/web/long-running-agents.md)
[^src2]: [Ch10 — Autonomous Background Coding Agents](../../raw/notes/notes-10-autonomous-background-coding-agents.md)
[^src3]: [Rakuten — Claude Managed Agents case study](../../raw/_inbox/web-rakuten-claude-managed-agents-case-study-claude-by-anthropic.md) — Yusuke Kaji, Rakuten
[^src4]: [Assign tasks from anywhere in Claude Cowork (Dispatch)](../../raw/_inbox/web-assign-tasks-from-anywhere-in-claude-cowork-claude-help-cent.md) — Anthropic Help Center
</content>

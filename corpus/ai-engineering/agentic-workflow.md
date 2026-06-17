---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/youtube/youtube-tDGiWn0flK8-from-zero-to-your-first-agentic-ai-workflow-in-26-minutes-cl.md
    channel: youtube
    ingested_at: 2026-06-15
  - path: raw/web/the-mother-of-ai-project.md
    channel: web
    ingested_at: 2026-06-15
  - path: raw/web/github-nirdiamant-genai-agents-50-tutorials-and-implementati.md
    channel: web
    ingested_at: 2026-06-15
  - path: raw/notes/notes-clippings-a-harness-for-every-task-dynamic-workflows-in-claude-code.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-10-autonomous-background-coding-agents.md
    channel: notes
    ingested_at: 2026-06-17
aliases:
  - agentic workflow
  - agentic workflows
  - agentic AI workflow
  - WAT framework
  - deterministic vs non-deterministic
  - AI automation
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-15
updated: 2026-06-17
---

# Agentic Workflows

**TL;DR**: An agentic workflow flips traditional automation: instead of specifying *how* to do a task step-by-step (drag nodes, wire them, debug), you describe *what* you want and the agent figures out the sequence, calls tools, handles errors, and self-corrects [^src1]. The skill is structuring the agent so it stays organized and improvable over time, not building the pipeline by hand [^src1].

## Deterministic vs non-deterministic

Traditional automation (n8n, Make) is **deterministic** — "boring is beautiful" because you know exactly what happens each run; ideal for repetitive, predictable tasks [^src1]. AI is **non-deterministic** — variability, judgment, different outputs from the same input [^src1]. The builder's job is "to make a non-deterministic process as deterministic as possible," because business processes are largely deterministic [^src1]. Agentic workflows shine on the messy, judgment-heavy tasks traditional automation can't handle (research, content, support, lead-gen) and improve over time instead of being set-and-forget [^src1].

> Analogy: traditional automation is a paper map and compass (you pick every street); an agentic workflow is GPS (you state the destination, it routes and recalculates when you go off-path) [^src1].

## The WAT framework (Workflows / Agent / Tools)

A structure for keeping a coding-agent harness organized [^src1]:

- **Workflows** — markdown instruction files (SOPs / job descriptions). They tell the agent *what to do* as a sequence of guidelines; the agent figures out *how*. The agent updates the workflow file from feedback so it does better next time [^src1].
- **Agent** — the coordinator/brain (e.g. Claude Code itself). Reads workflows, sees available tools, decides which to call and when, handles errors, adapts. "Think of it as a project manager that delegates tasks to tools" [^src1].
- **Tools** — Python scripts, each doing one specific job (scrape a site, generate a PDF). Modular and reusable; auto-built and auto-fixed by the agent when they fail [^src1].

A `CLAUDE.md` onboarding file explains the framework and a self-improvement loop: "first look in your existing tools, then learn and adapt when things fail... update the workflow so that error never happens again" [^src1] — the same ratchet pattern as [[ai-engineering/agent-harness|Agent Harness]] and [[ai-engineering/claude-md-conventions|CLAUDE.md Conventions]].

## Build loop in practice

The recommended flow: **plan mode** (let the agent ask clarifying questions and produce a comprehensive plan) → review → enable **bypass-permissions** to execute → run, hit errors, let it self-fix, iterate [^src1]. A worked competitor-analysis workflow produced a `business-profile.json`, per-competitor files, caching for cheap subsequent runs, and a branded PDF — the agent self-fixed a Unicode encoding bug and a white-logo rendering issue across runs [^src1]. The lesson: "you have to run the workflow a few times to discover the holes... then you get a battle-tested workflow" [^src1]. Note the **context-rot** caution: clear the conversation when context drops (the demo cleared at ~60% remaining) [^src1] — see [[ai-engineering/context-window-management|Context Window Management]].

## Production-grade vs demo agents

Real agentic systems go far beyond a single workflow. The "Mother of AI" roadmap stages production builds: RAG systems → agents with memory/planning/tool use → recommenders → MLOps/LLMOps → full app + cloud deployment → monitoring, using tools teams actually run (Docker, FastAPI, Airflow, Ollama, LangGraph, OpenSearch, Langfuse) [^src2]. The NirDiamant GenAI-Agents collection catalogs 50+ patterns — most orchestrated with **LangGraph** as stateful graphs with TypedDict/Pydantic state, human-in-the-loop validation, and self-improvement loops [^src3]. See [[ai-engineering/langgraph|LangGraph]], [[ai-engineering/multi-agent-systems|Multi-Agent Systems]], [[ai-engineering/rag|RAG]].

## Autonomous agent task cycle (background agents)

Background agents follow the same workflow discipline as interactive agents but execute it *asynchronously* across the full lifecycle of a coding task [^src5]. The pattern — **plan → execute → verify → report** — is the autonomous version of the WAT workflow:

- **Plan**: the agent reads the task, formulates substeps (some tools, like Jules, surface this for human review before proceeding). This is the WAT "Workflows" step done autonomously.
- **Execute**: reads/modifies code across the full repo using full-text search (grep is the dominant approach, surprisingly effective). This is the WAT "Tools" step.
- **Verify**: runs the test suite iteratively until tests pass; self-corrects before delivering. This closes the loop that interactive agents leave to the human.
- **Report**: delivers a PR with diffs and explanation; human reviews and may feed back for another iteration.

The key organizational insight from ch10: the human role shifts from **writing code** to **writing a good task description** and **reviewing the output**. The generator vs. reviewer asymmetry — generation is hard, review is faster — is the productivity lever background agents exploit [^src5].

## Dynamic workflow orchestration patterns (Claude Code)

When the default single-context-window execution breaks down on complex tasks, Claude Code's **dynamic workflows** offer a catalog of composable orchestration patterns [^src4]. Each addresses a class of task structure:

| Pattern | When to use |
|---|---|
| **Classify-and-act** | Use a classifier agent to route to different sub-workflows based on task type; or classify at the end to select output |
| **Fan-out-and-synthesize** | Split into many parallel subtasks (each with a clean context window), then a barrier synthesizer merges structured outputs |
| **Adversarial verification** | For each spawned agent's output, run a separate verifier agent that challenges the output against a rubric |
| **Generate-and-filter** | Produce many candidates, filter by a rubric, dedupe, and return only the highest-quality results |
| **Tournament** | Spawn N agents each attempting the same task with different approaches; a judging agent pairwise-compares until a winner emerges |
| **Loop until done** | Spawn agents iteratively until a stop condition is met (no new findings, no more errors) rather than a fixed N passes |

The unifying insight: **a workflow separates planning + orchestration (the JavaScript harness layer) from execution (the subagent context windows)** [^src4]. This prevents the single-context failure modes — agentic laziness, self-preferential bias, and goal drift — by ensuring each agent has a focused, bounded task. The synthesizer step in fan-out-and-synthesize is the harness-level equivalent of the planner/executor split in [[ai-engineering/agent-harness|Agent Harness]].

**Use sparingly**: dynamic workflows often use significantly more tokens. Best suited for complex, high-value tasks where quality improvements justify the cost [^src4]. Combine with `/loop` for recurring execution and `/goal` for hard completion conditions. See [[ai-engineering/claude-code|Claude Code]] for the full dynamic workflow mechanics.

## See also

- [[ai-engineering/ai-agent|AI Agent]] — the loop an agentic workflow wraps
- [[ai-engineering/agent-harness|Agent Harness]] — WAT is a harness pattern; the self-improvement ratchet
- [[ai-engineering/agentic-coding|Agentic Coding]] — coding-agent orchestration
- [[ai-engineering/multi-agent-systems|Multi-Agent Systems]] · [[ai-engineering/langgraph|LangGraph]] — multi-agent orchestration
- [[ai-engineering/vibe-coding|Vibe Coding]] — the lighter-weight "describe it and go" sibling
- [[ai-engineering/README|AI Engineering hub]]

---

[^src1]: [From Zero to Your First Agentic AI Workflow in 26 Minutes (Claude Code)](../../raw/youtube/youtube-tDGiWn0flK8-from-zero-to-your-first-agentic-ai-workflow-in-26-minutes-cl.md) — Nate Herk
[^src2]: [The Mother of AI Project](../../raw/web/the-mother-of-ai-project.md) — Jam with AI
[^src3]: [NirDiamant/GenAI_Agents (50+ tutorials)](../../raw/web/github-nirdiamant-genai-agents-50-tutorials-and-implementati.md) — Nir Diamant
[^src4]: [A harness for every task: dynamic workflows in Claude Code](../../raw/notes/notes-clippings-a-harness-for-every-task-dynamic-workflows-in-claude-code.md) — Thariq Shihipar & Sid Bidasaria, Anthropic
[^src5]: [Ch10 — Autonomous Background Coding Agents](../../raw/notes/notes-10-autonomous-background-coding-agents.md)

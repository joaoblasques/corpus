---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/web/agent-harness-engineering.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/is-grep-all-you-need-the-harness-matters-more-than-the-searc.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/github-affaan-m-ecc-the-agent-harness-performance-optimizati.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-03-31-affaan-m-everything-claude-code-the-agent-harness-performanc.md
    channel: email
    ingested_at: 2026-06-12
aliases:
  - harness
  - agent harness
  - harness engineering
  - coding agent harness
  - Harness-as-a-Service
  - HaaS
  - skill issue
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-12
updated: 2026-06-12
---

# Agent Harness

**TL;DR**: The *harness* is everything around the model that turns a raw LLM into a working agent — prompts, tools, context policies, hooks, sandboxes, subagents, feedback loops, recovery paths [^src1]. The defining equation: **"Agent = Model + Harness. If you're not the model, you're the harness"** [^src1]. The practical thesis: **a decent model with a great harness beats a great model with a bad harness** [^src1], and most of the leverage in agentic systems sits on the harness side, which is *your* surface area, not the model provider's [^src1].

## What a harness is

A raw model is not an agent. It becomes one once a harness gives it state, tool execution, feedback loops, and enforceable constraints [^src1]. The term *harness engineering* was coined by Viv Trivedy; Addy Osmani's synthesis pulls together work from Trivedy, Dex Horthy/HumanLayer, Anthropic's engineering team, and Birgitta Böckeler [^src1].

Concretely, a harness includes [^src1]:

- System prompts, `CLAUDE.md`/`AGENTS.md`, skill files, subagent prompts
- Tools, skills, MCP servers, and their descriptions
- Bundled infrastructure (filesystem, sandbox, browser)
- Orchestration logic (subagent spawning, handoffs, model routing)
- Hooks and middleware for deterministic execution (compaction, continuation, lint checks)
- Observability (logs, traces, cost and latency metering)

Claude Code, Cursor, Codex, Aider, Cline are all harnesses; the model underneath is sometimes the same, but the behavior you experience is dominated by what the harness does [^src1]. Simon Willison's reduction of the core loop: an agent "runs tools in a loop to achieve a goal" — the skill is in the design of both the tools and the loop [^src1].

## The harness beats the model (evidence)

The harness is the *hidden variable* in agent performance. Two independent benchmarks make this concrete:

- **Terminal Bench 2.0**: the same model (Claude Opus 4.6) scores far lower inside Claude Code than inside a custom harness; Trivedy's team moved a coding agent from Top 30 to Top 5 by changing *only the harness* [^src1].
- **PwC LongMemEval study** ("Is Grep All You Need?"): across 4 harnesses × 5 models × 2 retrieval methods, holding model and corpus fixed and swapping only the harness moved accuracy by double digits — Claude Opus 4.6 scored 93.1% on the Chronos harness vs 76.7% on Claude Code, a 16-point gap from the wrapper alone [^src2].

A key sub-finding: **result-delivery mode** (a harness decision) can invert retrieval results. Switching from inline delivery (results dumped into context) to file-based delivery (results written to disk, fetched via tool calls) erased or reversed grep's lead with no change to the data; Codex CLI with GPT-5.4 dropped from 93.1% inline to 55.2% file-based [^src2]. The harness controls prompting, tool framing, and how much of the window retrieved results consume — decisions that rival the retrieval method itself [^src2]. See [[ai-engineering/rag|RAG]] and [[ai-engineering/context-window-management|Context Window Management]].

> Models get post-training coupled to the harness they were trained against; moving them into a different harness with better tools, a tighter prompt, and sharper back-pressure "can unlock capability the original harness was leaving on the floor" [^src1].

## The "skill issue" reframe

The harness-engineering mindset rejects "blame the model, wait for the next version." Most agent failures are legible configuration problems, not model problems — HumanLayer: **"it's not a model problem. It's a configuration problem"** [^src1]. The agent didn't know a convention → add it to `AGENTS.md`; ran a destructive command → add a blocking hook; got lost in a 40-step task → split into planner and executor [^src1].

## The ratchet: every mistake becomes a rule

The most important habit: treat agent mistakes as permanent signals, not one-off bad runs [^src1]. You add a constraint only when you've seen a real failure, and remove it only when a capable model has made it redundant. **"Every line in a good AGENTS.md should be traceable back to a specific thing that went wrong"** [^src1]. This is why a harness is a *discipline shaped by your failure history*, not a downloadable framework [^src1]. (Note the resonance with the [[ai-engineering/agent-skills|Agent Skills]] recursive-building loop and the "let Claude write rules for itself" pattern in [[ai-engineering/agentic-coding|Agentic Coding]].)

## Harness building blocks (working backwards from behavior)

The design heuristic: start from the *behavior you want* and derive the harness piece that delivers it; if you can't name the behavior a component exists to deliver, it shouldn't be there [^src1]. Core primitives [^src1]:

- **Filesystem + Git** — durable state, a workspace to offload intermediate work, a coordination surface; Git adds versioning, rollback, branching for free.
- **Bash + code execution** — the general-purpose tool. Rather than pre-building a tool for every action, give the agent bash and let it build tools on the fly: "the difference between teaching someone to use a single kitchen gadget and handing them a kitchen."
- **Sandboxes** — isolated execution with allow-listed commands, network isolation, good defaults (runtimes, Git, test CLIs, headless browser) so the agent can observe and self-verify.
- **Memory + search** — `AGENTS.md`-style files injected each start (crude continual learning); web search and MCP tools like Context7 bridge the training cutoff.
- **Hooks** — the enforcement layer (see below).

### Battling context rot

The harness is largely a delivery mechanism for good [[ai-engineering/context-engineering|context engineering]]. Three recurring techniques against *context rot* (models degrade as the window fills) [^src1]:

1. **Compaction** — summarize/offload older context near the window limit.
2. **Tool-call offloading** — keep head/tail of large outputs in context, offload the full output to the filesystem for on-demand reading.
3. **Skills with progressive disclosure** — reveal instructions/tools only when the task calls for them (see [[ai-engineering/agent-skills|Agent Skills]]).

Anthropic adds **full context resets** for long jobs: tear the session down and rebuild from a compact hand-off file — compaction alone was insufficient for long tasks [^src1].

### Long-horizon execution

Today's models suffer early stopping, poor decomposition, and incoherence across windows [^src1]. Harness patterns:

- **Ralph Loop** — a hook intercepts the model's attempt to exit and re-injects the original prompt into a fresh context window, forcing continuation against a completion goal; each iteration starts clean but reads prior state from the filesystem [^src1].
- **Planner / generator / evaluator splits** — separating generation from evaluation into distinct agents outperforms self-evaluation because agents skew positive grading their own work ("GANs for prose"); the related *sprint contract* negotiates the done-condition before code is written [^src1].

### Hooks: the enforcement layer

Hooks separate "I told the agent to do X" from "the system enforces X" — scripts that run at lifecycle points (before tool call, after edit, before commit, on session start) [^src1]. Run typecheck/lint/tests after edits; block destructive bash (`rm -rf`, `git push --force`, `DROP TABLE`); require approval before opening a PR. Operating principle: **success is silent, failures are verbose** — if a check passes the agent hears nothing; if it fails, the error text is injected into the loop and the agent self-corrects, making feedback almost free in the common case [^src1].

### AGENTS.md and tool choice

The root markdown rulebook lands in the system prompt every turn — the highest-leverage configuration point [^src1]. Two hard-won lessons: **keep it short** (HumanLayer keeps theirs under 60 lines — "pilot's checklist, not style guide") and **earn each line** (trace to a past failure or hard constraint) [^src1]. Same discipline for tools: each tool's name/description/schema is stamped into the prompt every request, so ten focused tools outperform fifty overlapping ones [^src1]. Security note: tool descriptions are *trusted text the model reads*, so a sloppy or malicious MCP can prompt-inject your agent before you type anything [^src1]. See [[ai-engineering/mcp|MCP]].

## Harnesses don't shrink, they move

As models improve, the space of interesting harness combinations doesn't shrink — it moves [^src1]. Opus 4.6 largely killed the context-anxiety failure mode (Sonnet 4.5 used to stop prematurely near its perceived context limit), retiring a whole class of scaffolding [^src1]. But the ceiling moved with the model: anxiety scaffolding goes away and is replaced by multi-day memory policies, three-agent coordination, or evaluators for generated-UI quality. Anthropic: **"every component in a harness encodes an assumption about what the model can't do on its own"** — when the model improves at something, that component becomes load-bearing for nothing and should be removed [^src1].

A related feedback loop: today's agent products are post-trained *with harnesses in the loop*, so the model gets specifically better at filesystem ops, bash, planning, and subagent dispatch — which is why the same model feels different across harnesses, and why changing a tool's logic (`apply_patch` vs `str_replace`) can cause regressions [^src1].

## Harness-as-a-Service (HaaS)

Trivedy's framing: the industry is moving from building on **LLM APIs** (which return a completion) to building on **harness APIs** (which return a runtime) — the Claude Agent SDK, Codex SDK, and OpenAI Agents SDK all point the same way, shipping the loop, tools, context management, hooks, and sandbox primitives out of the box [^src1]. The default path shifts from "build your own loop and tool-calling" to "pick a harness framework, configure the four pillars (system prompt, tools, context, subagents), and put effort into domain-specific design" [^src1]. Trivedy's argument for starting messy: "good agent building is an exercise in iteration. You can't do iterations if you don't have a v0.1" [^src1].

## Harness as a product: ECC (everything-claude-code)

A concrete, shipping harness system is **ECC (everything-claude-code)** by Affaan M — explicitly framed as "the agent harness performance optimization system," not just a config pack [^src3] [^src4]. It packages agents, skills, hooks, rules, and MCP configs evolved over 10+ months of daily use, and runs cross-harness across Codex, Claude Code, Cursor, OpenCode, Gemini, Zed, and GitHub Copilot [^src3]. Notable surface as of v2.0: 64 subagents, 262 skills, 84 legacy command shims [^src3]. It operationalizes most of the patterns above as named components:

- **Memory persistence hooks** — `SessionStart`/`Stop` hooks save/load context across sessions automatically [^src3].
- **Continuous learning v2 (instincts)** — auto-extract patterns from sessions into reusable skills with confidence scoring, import/export, and `/evolve` to cluster instincts into skills [^src3] (an automated version of the ratchet).
- **Context discipline as a documented failure mode** — "Too many MCP servers eat your context. Each MCP tool description consumes tokens... potentially reducing it to ~70k"; ECC's guidance is to keep under 10 MCPs and under 80 tools active [^src3]. Mirrors the tool-choice lesson above and [[ai-engineering/context-window-management|Context Window Management]].
- **AgentShield** — a security scanner for the harness config itself (CLAUDE.md, settings.json, MCP configs, hooks, agents, skills); the `--opus` mode runs red-team/blue-team/auditor Opus agents adversarially rather than pattern-matching [^src3].

## See also

- [[ai-engineering/agentic-coding|Agentic Coding]] — orchestration patterns built on top of the harness
- [[ai-engineering/agent-skills|Agent Skills]] — progressive disclosure as a harness context technique
- [[ai-engineering/context-engineering|Context Engineering]] — the harness is a delivery mechanism for good context
- [[ai-engineering/context-window-management|Context Window Management]] — compaction, offloading, context rot
- [[ai-engineering/mcp|MCP]] — tools and the prompt-injection surface they add
- [[ai-engineering/multi-agent-systems|Multi-Agent Systems]] — subagent orchestration, planner/evaluator splits
- [[ai-engineering/rag|RAG]] — grep-vs-vector and how delivery mode reshapes retrieval
- [[ai-engineering/ai-agent|AI Agent]] — the ReAct loop the harness wraps
- [[ai-engineering/README|AI Engineering hub]]

---

[^src1]: [Agent Harness Engineering](../../raw/web/agent-harness-engineering.md) — Addy Osmani, synthesizing Viv Trivedy, HumanLayer/Dex Horthy, Anthropic, Birgitta Böckeler
[^src2]: [Is Grep All You Need? The Harness Matters More Than the Search](../../raw/web/is-grep-all-you-need-the-harness-matters-more-than-the-searc.md) — StackSweep, on a PwC LongMemEval study
[^src3]: [everything-claude-code (ECC): the agent harness performance optimization system](../../raw/web/github-affaan-m-ecc-the-agent-harness-performance-optimizati.md) — affaan-m/ECC, GitHub
[^src4]: [affaan-m/everything-claude-code (email pointer)](../../raw/email/email-2026-03-31-affaan-m-everything-claude-code-the-agent-harness-performanc.md) — email, Gmail

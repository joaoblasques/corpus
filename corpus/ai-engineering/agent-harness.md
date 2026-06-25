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
  - path: raw/web/how-claude-code-works-in-large-codebases-best-practices-and.md
    channel: web
    ingested_at: 2026-06-15
  - path: raw/email/email-2026-05-28-the-harness-matters-more-than-the-model.md
    channel: email
    ingested_at: 2026-06-15
  - path: raw/web/antirez.md
    channel: web
    ingested_at: 2026-06-15
  - path: raw/email/email-2026-05-28-launching-boring-ui.md
    channel: email
    ingested_at: 2026-06-16
  - path: raw/notes/notes-clippings-a-harness-for-every-task-dynamic-workflows-in-claude-code.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-clippings-harnessing-claude-s-intelligence-3-key-patterns-for-building.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/web/web-harness-design-for-long-running-application-development.md
    channel: web
    ingested_at: 2026-06-23
  - path: raw/web/web-agent-harness-engineering.md
    channel: web
    ingested_at: 2026-06-23
  - path: raw/github/affaan-m-ecc.md
    channel: github
    ingested_at: 2026-06-25
  - path: raw/web/web-handle-approvals-and-user-input-claude-code-docs.md
    channel: web
    ingested_at: 2026-06-25
  - path: raw/web/web-text-editor-tool.md
    channel: web
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-03CfGf9iw_U-completely-understand-hooks-in-less-than-20-minutes.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/web/web-hooks-reference-claude-code-docs.md
    channel: web
    ingested_at: 2026-06-25
  - path: raw/web/web-how-claude-code-works-claude-code-docs.md
    channel: web
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-RzLV8sfFdMM-how-to-build-effective-claude-code-agents-in-2026.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/github/github-googlecloudplatform-agent-starter-pack.md
    channel: github
    ingested_at: 2026-06-25
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
updated: 2026-06-25
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

**Official Anthropic definition**: a harness is "a wrapper around the LLM, the tools and context it has access to" [^src16]. Claude Code itself is a harness — one specifically designed around software engineering workflows. The **AI layer** (the harness layer you control) consists of: `CLAUDE.md` / `AGENTS.md` (standing instructions), skills (reusable procedures), hooks (lifecycle enforcement), and MCPs (external tools) [^src17].

**Pi** (Mario Zechner) is a notable open-source harness in this class — described as "super lightweight and built to be highly extensible," provider-agnostic, and embeddable via a Node.js SDK [^src7]. It is the runtime Boring UI builds on (Boring UI *uses* Pi as its agent harness and extends Pi's plugin model), a concrete case of a product picking an existing harness rather than rolling its own loop [^src7]. See [[ai-engineering/agent-ui|Agent UI]].

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
- **Planner / generator / evaluator splits** — separating generation from evaluation into distinct agents outperforms self-evaluation because agents skew positive grading their own work ("GANs for prose"); the related *sprint contract* negotiates the done-condition before code is written [^src1][^src10].

### The 3-agent GAN harness (Anthropic engineering)

Anthropic's engineering blog documents a concrete planner/generator/evaluator harness built for production application development [^src10]:

- **Planner** — writes a detailed implementation plan including scope, dependencies, and the done-condition. The sprint contract (planner output) must be negotiated *before* the generator starts; retroactively changing scope once generation is underway is the primary source of rework [^src10].
- **Generator** — executes the plan. Constrained to write only to a specified scope; feeds completed work to the evaluator [^src10].
- **Evaluator** — runs in a separate context window with no access to the generator's chain-of-thought. This isolation is the key: "a generator can't reliably grade itself" — the same cognitive bias that makes self-consistent wrong reasoning in humans appears in LLM generators [^src10].

GAN-inspired framing: the evaluator is the discriminator; the generator is trained (via prompting) to produce output the evaluator can't distinguish from the desired spec. Each evaluator rejection is a learning signal that updates the generator's approach [^src10].

**Cost vs. quality tradeoff** observed empirically [^src10]:
- Solo session: 20 minutes, $9. Single agent, no evaluator. Works for well-scoped tasks, but quality is inconsistent on ambiguous scope.
- 3-agent harness: 6 hours, $200. Planner + generator + evaluator loop. Works for tasks with complex done-conditions; quality dramatically higher, consistent across runs.
- DAW (digital audio workstation) example: 4 hours, $124. The harness produced a working feature the solo session couldn't complete reliably.

**Context anxiety** (Sonnet 4.5): in early versions, generators would stop prematurely near their perceived context limit. The harness added explicit context-reset logic. With Opus 4.5 this behavior was gone — "the context resets we built to compensate had become dead weight in the agent harness" [^src9][^src10]. Context reset scaffolding is a canonical example of harness components becoming obsolete as models improve.

### Hooks: the enforcement layer

Hooks separate "I told the agent to do X" from "the system enforces X" — scripts that run at lifecycle points (before tool call, after edit, before commit, on session start) [^src1]. Run typecheck/lint/tests after edits; block destructive bash (`rm -rf`, `git push --force`, `DROP TABLE`); require approval before opening a PR. Operating principle: **success is silent, failures are verbose** — if a check passes the agent hears nothing; if it fails, the error text is injected into the loop and the agent self-corrects, making feedback almost free in the common case [^src1].

### AGENTS.md and tool choice

The root markdown rulebook lands in the system prompt every turn — the highest-leverage configuration point [^src1]. Two hard-won lessons: **keep it short** (HumanLayer keeps theirs under 60 lines — "pilot's checklist, not style guide") and **earn each line** (trace to a past failure or hard constraint) [^src1]. Same discipline for tools: each tool's name/description/schema is stamped into the prompt every request, so ten focused tools outperform fifty overlapping ones [^src1]. Security note: tool descriptions are *trusted text the model reads*, so a sloppy or malicious MCP can prompt-inject your agent before you type anything [^src1]. See [[ai-engineering/mcp|MCP]].

## Harnesses don't shrink, they move

As models improve, the space of interesting harness combinations doesn't shrink — it moves [^src1]. Opus 4.6 largely killed the context-anxiety failure mode (Sonnet 4.5 used to stop prematurely near its perceived context limit), retiring a whole class of scaffolding [^src1]. But the ceiling moved with the model: anxiety scaffolding goes away and is replaced by multi-day memory policies, three-agent coordination, or evaluators for generated-UI quality. Anthropic: **"every component in a harness encodes an assumption about what the model can't do on its own"** — when the model improves at something, that component becomes load-bearing for nothing and should be removed [^src1].

A related feedback loop: today's agent products are post-trained *with harnesses in the loop*, so the model gets specifically better at filesystem ops, bash, planning, and subagent dispatch — which is why the same model feels different across harnesses, and why changing a tool's logic (`apply_patch` vs `str_replace`) can cause regressions [^src1].

## Anthropic's "Claude Code at scale" guidance

Anthropic's own large-codebase post makes the harness thesis first-party: **"the ecosystem built around the model — the harness — determines how Claude Code performs more than the model alone"** [^src5]. Two concrete points reinforce earlier sections:

- **No index by design.** Claude Code doesn't embed or upload the codebase; it greps, lists directories, reads files, and follows references the way a developer would. The rationale is staleness: "by the time a developer queries the index, it reflects the codebase as it existed weeks, days, or even hours before. Retrieval returns a function the team renamed two weeks ago" [^src5]. The tradeoff: it works best "when Claude has enough starting context to know where to look," so the burden on a big/unfamiliar repo is on *you* (the harness), not the model [^src5]. See [[ai-engineering/agentic-search|Agentic Search]] for the grep-vs-index debate; codegraph is the week's attempt to bolt a local knowledge graph back on via MCP [^src5].
- **The CLAUDE.md operating rules** [^src5]: keep the root file thin ("pointers and critical gotchas only; everything else drifts into noise"), push local conventions into subdirectory files that load as Claude walks the tree, codify build/test commands so Claude can't guess, tell Claude to "update CLAUDE.md so you don't repeat this" after a mistake, and **re-read it after model upgrades** — an old single-file-refactor rule that helped a weaker model can block a stronger one from cross-file edits it's now good at (Anthropic suggests a review every 3–6 months). The summary: "give Claude a thin map and a way to check its own work, then get out of the way" [^src5]. These overlap with [[ai-engineering/claude-md-conventions|CLAUDE.md Conventions]].

### The QA-agent harness pattern

A specific high-value harness component: a **QA agent layered on top of existing tests** rather than replacing them. Salvatore Sanfilippo's pattern — the LLM agent reads new commits, analyzes the impact, stands up an environment (e.g. replication + persistence), and simulates days of multi-user traffic to surface what looks broken — "tests like a real user" and catches the performance/UX issues rigid scripts miss [^src6]. The setup is a single Markdown file with goals and SSH details, instructing the agent to compare the new branch against the last stable release and flag *relative* regressions (e.g. speed drops) without hardcoded limits [^src6]. This is the harness-side complement to [[ai-engineering/agent-testing|Agent Testing]].

## Harness-as-a-Service (HaaS)

Trivedy's framing: the industry is moving from building on **LLM APIs** (which return a completion) to building on **harness APIs** (which return a runtime) — the Claude Agent SDK, Codex SDK, and OpenAI Agents SDK all point the same way, shipping the loop, tools, context management, hooks, and sandbox primitives out of the box [^src1]. The default path shifts from "build your own loop and tool-calling" to "pick a harness framework, configure the four pillars (system prompt, tools, context, subagents), and put effort into domain-specific design" [^src1]. Trivedy's argument for starting messy: "good agent building is an exercise in iteration. You can't do iterations if you don't have a v0.1" [^src1].

## Harness as a product: ECC (everything-claude-code)

A concrete, shipping harness system is **ECC (everything-claude-code)** by Affaan M — explicitly framed as "the agent harness performance optimization system," not just a config pack [^src3] [^src4]. It packages agents, skills, hooks, rules, and MCP configs evolved over 10+ months of daily use, and runs cross-harness across Codex, Claude Code, Cursor, OpenCode, Gemini, Zed, and GitHub Copilot [^src3]. Notable surface as of v2.0: 64 subagents, 262 skills, 84 legacy command shims [^src3]. It operationalizes most of the patterns above as named components:

- **Memory persistence hooks** — `SessionStart`/`Stop` hooks save/load context across sessions automatically [^src3].
- **Continuous learning v2 (instincts)** — auto-extract patterns from sessions into reusable skills with confidence scoring, import/export, and `/evolve` to cluster instincts into skills [^src3] (an automated version of the ratchet).
- **Context discipline as a documented failure mode** — "Too many MCP servers eat your context. Each MCP tool description consumes tokens... potentially reducing it to ~70k"; ECC's guidance is to keep under 10 MCPs and under 80 tools active [^src3]. Mirrors the tool-choice lesson above and [[ai-engineering/context-window-management|Context Window Management]].
- **AgentShield** — a security scanner for the harness config itself (CLAUDE.md, settings.json, MCP configs, hooks, agents, skills); the `--opus` mode runs red-team/blue-team/auditor Opus agents adversarially rather than pattern-matching [^src3].

## Self-generating harnesses (dynamic workflows)

The default Claude Code harness is built for coding but breaks down on long-running, massively parallel, adversarial, or highly structured tasks because of three specific failure modes that emerge when planning and execution share a single context window [^src8]:

- **Agentic laziness**: the model stops before finishing a complex multi-part task and declares done prematurely (e.g., stops at 35 of 50 security findings).
- **Self-preferential bias**: when asked to verify or judge its own output, the model skews toward self-approval — structurally similar to a GAN's generator grading itself rather than having a separate discriminator.
- **Goal drift**: across many turns and compaction events, fidelity to the original objective erodes; edge-case requirements and "don't do X" constraints get lost in summarization.

**Dynamic workflows** are Anthropic's harness-level response: Claude writes a JavaScript orchestration file on the fly that spawns separate subagents with their own context windows and focused, isolated goals [^src8]. The harness is therefore *task-specific* rather than general-purpose. Claude can choose which model each subagent uses and whether subagents run in isolated worktrees [^src8]. This represents a shift from "configure a static harness" to "the model generates the harness as part of the task." The distinction vs static workflows: "static workflows need to work for all edge cases, so they are usually more generic. With dynamic workflows, Claude is now intelligent enough to write a custom harness tailor-made for your use case" [^src8].

Harness failure modes become harness design criteria: agentic laziness → use separate agents for each work unit; self-preferential bias → use adversarial verifier agents; goal drift → preserve original intent through fresh context windows rather than compaction. See [[ai-engineering/claude-code|Claude Code]] for the full dynamic-workflow pattern catalog.

## Three patterns for building with Claude's evolving intelligence

Anthropic's platform team identifies three meta-patterns for harness design that remain durable as models improve [^src9]:

### 1. Use what Claude already knows

Build around tools Claude is deeply trained on rather than inventing novel tool interfaces. Claude Code's benchmark-leading performance on SWE-bench Verified in late 2024 came from just bash + text editor tools — "tools that Claude *knows* how to use and gets better at using over time" [^src9]. Agent Skills, programmatic tool calling, and the memory tool are all compositions of these two primitives rather than distinct tool implementations [^src9].

### 2. Ask "what can I stop doing?"

Every harness component encodes an assumption about what Claude can't do on its own. As the model improves, those assumptions should be tested and retired [^src9]:

- **Let Claude orchestrate its own actions.** Rather than the harness deciding every tool result flows back as tokens (slow, costly), give Claude a code-execution tool (bash/REPL) so it can write code expressing tool calls *and the logic between them* — only the output reaches context. On BrowseComp, giving Opus 4.6 the ability to filter its own tool outputs lifted accuracy from 45.3% to 61.6% [^src9].
- **Let Claude manage its own context.** The skills pattern (progressive disclosure via YAML frontmatter) lets Claude assemble its own context rather than the harness pre-loading everything [^src9]. Context editing is the inverse: selectively remove stale tool results or thinking blocks.
- **Let Claude persist its own context.** Rather than building retrieval infrastructure around the model, give Claude simple ways to write to a memory folder and read later. Opus 4.6 scored 84% on BrowseComp-Plus using a memory folder (vs Sonnet 4.5 at 60.4%); the quality of what gets written has improved dramatically across model generations [^src9].

> Concrete model evolution example: Sonnet 4.5 stopped prematurely near its perceived context limit ("context anxiety"). Anthropic added context-reset scaffolding. With Opus 4.5, the behavior was gone — "the context resets we built to compensate had become dead weight in the agent harness" [^src9].

### 3. Set boundaries carefully

- **Design for cache hits.** Static content (system prompt, tools) first, dynamic content (new messages, `<system-reminder>`) last. Don't switch models mid-session (caches are model-specific). Adding/removing a tool from the cached prefix invalidates it — use tool search for dynamic discovery [^src9].
- **Promote actions to dedicated tools for security, UX, or observability.** A bash tool gives the harness only a command string — the same shape for every action. A dedicated `edit` tool gives the harness typed arguments it can intercept, gate, render, audit, or present as a user confirmation modal [^src9]. Reversibility is the key criterion: hard-to-reverse actions (external API calls, file deletion) are natural candidates for dedicated tools with explicit user gates [^src9].
- **Re-evaluate continuously.** Auto mode is an example of where a pattern (dedicated tools for security boundaries around bash) may be partially replaced by a smarter classifier, not by adding more tools [^src9].

## Claude Code hooks lifecycle (event-driven harness control)

Claude Code's hook system provides eight lifecycle events that let the harness intercept, gate, enrich, or observe every phase of a session [^src12]:

| Hook | When it fires | Can block? |
|---|---|---|
| `session_start` | Session opens | No |
| `user_prompt_submitted` | User sends a message | No |
| `pre_tool_use` | Before Claude runs a tool | **Yes** |
| `post_tool_use` | After tool result | No |
| `sub_agent_start` | Subagent spawned | No |
| `sub_agent_stop` | Subagent finishes | No |
| `session_end` | Session closes | No |
| `error` | Error occurs | No |

**JSON payload** on each hook [^src12]: `event_name`, `timestamp`, `id`, `transcript_path`, `cwd`. `user_prompt_submitted` additionally receives `prompt`. **Output format**: `{ event_name, additional_context, updated_input }` — hooks can inject context or modify the input.

**Configuration** [^src12]: `.claude/hooks/` JSON files in the project, global `~/.claude/settings.json` `hooksConfig` key, or the Claude Code settings page (VS Code: Output panel for hook output; CLI: reload with `/new`).

**Pre-tool-use ESLint gate (deterministic quality gate)** [^src12]: the canonical use case for a blocking hook. On a Write tool call for a TypeScript file, the hook runs ESLint on the file-to-be-written. If lint fails, the hook returns a deny response listing the violations; Claude is forced to fix the code and retry. "The hook makes lint non-negotiable — Claude cannot ship linting violations." This is an example of using the harness to enforce deterministic constraints the model can't rationalize away.

**Session_start context injection** [^src12]: use session_start to load module-specific or time-specific context into every session automatically — e.g., inject the current sprint goal, load the domain CLAUDE.md, or pre-populate a memory summary.

## canUseTool callback (Agent SDK tool approval)

The Claude Agent SDK provides a `canUseTool` callback for programmatic tool approval before each tool call executes [^src13]. The callback receives the full tool input and returns one of:

| Response type | Meaning |
|---|---|
| `allow` | Proceed as-is |
| `allow-with-changes` | Proceed, but with modified tool input |
| `allow-and-remember` | Allow and don't ask again for this tool/input pattern |
| `deny` | Block this tool call |
| `suggest-alternative` | Block and suggest a different approach |
| `redirect` | Route to a different tool entirely |

**Tool input fields** available for inspection in the callback [^src13]:
- **Bash**: `command`, `description`, `timeout`
- **Write**: `file_path`, `content`
- **Edit**: `file_path`, `old_str`, `new_str`
- **Read**: `file_path`, `offset`, `limit`

**AskUserQuestion tool** [^src13]: allows Claude to present a structured question with 2–4 options to the user mid-task. Questions specify 1–4 question texts and their option lists. **Restriction**: subagents cannot use AskUserQuestion (they cannot reach back to the user directly; only the parent session can).

## str_replace_based_edit_tool (text editor tool)

The `str_replace_based_edit_tool` (type `"text_editor_20250728"`) is an official Anthropic tool for precise file editing without reading entire files [^src14]. The schema is built into the model — no manual schema declaration needed.

**Commands** [^src14]:
| Command | Purpose |
|---|---|
| `view` | Read file or range (`view_range` parameter) |
| `str_replace` | Replace exact string with new string |
| `create` | Create a new file |
| `insert` | Insert text at a specific line |

**Version history** [^src14]: initial version `text_editor_20241022`; Claude 4 version `text_editor_20250429`; current `text_editor_20250728` (adds `max_characters` parameter). Use type `"text_editor_20250728"` for Claude 4 and later. The tool adds ~700 additional input tokens per call.

The `max_characters` parameter (available in `20250728`+) caps how many characters are returned in a `view` response — useful for controlling context size when previewing large files [^src14].

## Claude Code hooks — full event reference

Claude Code hooks let harnesses intercept lifecycle events with shell scripts [^src15]. All hooks configured in `.claude/settings.json` under `hooks`:

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "tool_name",
        "hooks": [{ "type": "command", "command": "bash script.sh" }]
      }
    ]
  }
}
```

**All 29 hook events** (Claude Code, v1.x) [^src15]:

| Event | Timing | Primary use |
|---|---|---|
| `SessionStart` | Before first turn | Boot scripts, env setup |
| `SessionEnd` | After last turn | Cleanup, final logging |
| `Stop` | Model stops voluntarily | Validate work before declaring done |
| `PreToolUse` | Before tool call | Block/mutate tool args |
| `PostToolUse` | After tool result | Post-process output, log |
| `Notification` | UI notification | Route to Slack/webhook |
| `SubagentStart` | Subagent spawn | Inject context to child |
| `SubagentStop` | Subagent done | Collect subagent output |
| `MemoryQuery` | Memory lookup | Augment/override recall |
| `MemoryWrite` | Memory persist | Canonicalize before storing |
| `PermissionRequest` | Permission check | Auto-approve or hard-deny |
| `ToolError` | Tool call fails | Log, retry, escalate |
| `CompactStart` | Before context compaction | Preserve critical context |
| `CompactEnd` | After compaction | Verify nothing lost |
| `FileRead` | File read by model | Shadow/audit reads |
| `FileWrite` | File write by model | Validate content, lint |
| `BashRun` | Bash command before exec | Prevent dangerous commands |
| `BashOutput` | Bash output available | Parse structured output |
| `MCPCallStart` | MCP tool call start | Auth, rate limit |
| `MCPCallEnd` | MCP tool call done | Audit, transform response |
| `ThinkingStart` | Extended thinking begins | Log reasoning |
| `ThinkingEnd` | Extended thinking ends | Audit CoT |
| `ProjectLoad` | CLAUDE.md loaded | Inject dynamic context |
| `ContextInjection` | Context added | Audit injections |
| `ApprovalRequest` | Human-in-loop approval | Auto-approve, route UI |
| `ApprovalResponse` | Approval answered | Audit decisions |
| `UserMessage` | User input received | Sanitize, classify |
| `AssistantMessage` | Model reply ready | Log, post-process |
| `ToolCallComplete` | Any tool call completes | Aggregate stats |

**Handler types** [^src15]:

| Type | Config key | Usage |
|---|---|---|
| Shell command | `type: "command"` | Execute any script; stdout → stdin to model |
| JSON output | `type: "command"` + JSON print | Return structured JSON to modify behavior |
| Webhook | `type: "webhook"` | POST event JSON to HTTP endpoint |
| Queue/buffer | `type: "command"` + exit code 1 | Block the action (PreToolUse) |
| Passthrough | no hooks entry | Default — no interception |

**Exit code semantics** [^src15]:
- **0**: success; stdout fed to model as context.
- **1** (on `PreToolUse`): **blocks** the tool call; stderr shown to model as reason.
- **2**: hook error (logged, execution continues).
- **JSON output** overrides tool args / results when a `PreToolUse` or `PostToolUse` hook returns valid JSON matching the schema.

**`matcher` field** [^src15]: glob pattern on the tool name. `"Bash"` matches all bash; `"mcp__*"` matches all MCP tools. Omit to match all tools for the event.

The Claude Code hooks system is the main harness extension point for adding **audit trails, policy enforcement, automatic testing gates, and notification routing** without modifying the model or prompts [^src15].

## GCP Agent Starter Pack (maintenance mode)

Google Cloud's `agent-starter-pack` (formerly a primary recommendation for GCP agent deployments) has been moved to **maintenance mode** [^src18]. New projects should use the `agents-cli` tool instead:

```
uvx google-agents-cli setup
```

The starter pack provided: Vertex AI + Cloud Run scaffolding, session management, evaluation pipelines, and CI/CD templates. The `agents-cli` successor (`google/agents-cli`) provides the same functionality in a CLI-first, actively maintained form [^src18].

**Key lesson**: agent harnesses have a short half-life in a fast-moving ecosystem. Design harnesses to be replaceable — keep application logic decoupled from the scaffolding layer.

## See also

- [[ai-engineering/agentic-coding|Agentic Coding]] — orchestration patterns built on top of the harness
- [[ai-engineering/agent-skills|Agent Skills]] — progressive disclosure as a harness context technique
- [[ai-engineering/context-engineering|Context Engineering]] — the harness is a delivery mechanism for good context
- [[ai-engineering/context-window-management|Context Window Management]] — compaction, offloading, context rot
- [[ai-engineering/mcp|MCP]] — tools and the prompt-injection surface they add
- [[ai-engineering/multi-agent-systems|Multi-Agent Systems]] — subagent orchestration, planner/evaluator splits
- [[ai-engineering/generator-evaluator-separation|Generator–Evaluator Separation]] — the GAN-harness insight generalized across the week's sources (a generator can't grade itself)
- [[ai-engineering/rag|RAG]] — grep-vs-vector and how delivery mode reshapes retrieval
- [[ai-engineering/ai-agent|AI Agent]] — the ReAct loop the harness wraps
- [[ai-engineering/README|AI Engineering hub]]

---

[^src1]: [Agent Harness Engineering](../../raw/web/agent-harness-engineering.md) — Addy Osmani, synthesizing Viv Trivedy, HumanLayer/Dex Horthy, Anthropic, Birgitta Böckeler
[^src2]: [Is Grep All You Need? The Harness Matters More Than the Search](../../raw/web/is-grep-all-you-need-the-harness-matters-more-than-the-searc.md) — StackSweep, on a PwC LongMemEval study
[^src3]: [everything-claude-code (ECC): the agent harness performance optimization system](../../raw/web/github-affaan-m-ecc-the-agent-harness-performance-optimizati.md) — affaan-m/ECC, GitHub
[^src4]: [affaan-m/everything-claude-code (email pointer)](../../raw/email/email-2026-03-31-affaan-m-everything-claude-code-the-agent-harness-performanc.md) — email, Gmail
[^src5]: [How Claude Code works in large codebases: best practices](../../raw/web/how-claude-code-works-in-large-codebases-best-practices-and.md) — Anthropic, via [The harness matters more than the model](../../raw/email/email-2026-05-28-the-harness-matters-more-than-the-model.md) (Claude Code Camp)
[^src6]: [Coding with LLMs: the QA agent pattern](../../raw/web/antirez.md) — Salvatore Sanfilippo (antirez), via [How OpenAI engineers prompt](../../raw/email/email-2026-06-08-how-openai-engineers-prompt.md)
[^src7]: [Launching Boring UI](../../raw/email/email-2026-05-28-launching-boring-ui.md) — Julien Hurault, on Pi as the harness behind Boring UI
[^src8]: [A harness for every task: dynamic workflows in Claude Code](../../raw/notes/notes-clippings-a-harness-for-every-task-dynamic-workflows-in-claude-code.md) — Thariq Shihipar & Sid Bidasaria, Anthropic
[^src9]: [Harnessing Claude's Intelligence: 3 Key Patterns for Building Apps](../../raw/notes/notes-clippings-harnessing-claude-s-intelligence-3-key-patterns-for-building.md) — Lance Martin, Anthropic Platform team
[^src10]: [Harness Design for Long-Running Application Development](../../raw/web/web-harness-design-for-long-running-application-development.md) — Anthropic engineering blog
[^src11]: [affaan-m/ECC — GitHub (219K★, v2.0.0)](../../raw/github/affaan-m-ecc.md) — affaan-m, GitHub
[^src12]: [Completely Understand Hooks in Less Than 20 Minutes](../../raw/youtube/youtube-03CfGf9iw_U-completely-understand-hooks-in-less-than-20-minutes.md) — Burke Holland, YouTube
[^src13]: [Handle approvals and user input — Claude Code Agent SDK docs](../../raw/web/web-handle-approvals-and-user-input-claude-code-docs.md) — Anthropic
[^src14]: [Text editor tool — Anthropic API docs](../../raw/web/web-text-editor-tool.md) — Anthropic
[^src15]: [Hooks reference — Claude Code docs](../../raw/web/web-hooks-reference-claude-code-docs.md) — Anthropic
[^src16]: [How Claude Code Works — Claude Code docs](../../raw/web/web-how-claude-code-works-claude-code-docs.md) — Anthropic
[^src17]: [How to Build Effective Claude Code Agents in 2026](../../raw/youtube/youtube-RzLV8sfFdMM-how-to-build-effective-claude-code-agents-in-2026.md) — Cole Medin, YouTube
[^src18]: [google/agent-starter-pack — GCP agent harness (maintenance mode)](../../raw/github/github-googlecloudplatform-agent-starter-pack.md) — Google Cloud, GitHub

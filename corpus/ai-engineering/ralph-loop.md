---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/web/ralph-wiggum-as-a-software-engineer.md
    channel: web
    ingested_at: 2026-06-16
  - path: raw/web/long-running-agents.md
    channel: web
    ingested_at: 2026-06-16
  - path: raw/notes/notes-clippings-loop-engineering.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-full-walkthrough-report.md
    channel: notes
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-iJVJwmCKW9o-i-guess-we-re-writing-loops-now.md
    channel: youtube
    ingested_at: 2026-06-25
aliases:
  - Ralph
  - Ralph technique
  - Ralph Wiggum technique
  - Ralph Wiggum
  - Ralph loop
  - while loop agent
  - loop engineering
  - loop design
  - loop of loops
  - loops creating loops
  - PR heartbeat monitor
  - dynamic sub-loops
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-16
updated: 2026-06-25
---

# Ralph Loop

**TL;DR.** The Ralph technique (a.k.a. the Ralph Wiggum technique) is, in its purest form, a Bash loop that repeatedly feeds the same prompt to a coding agent until a project is built [^src1]. State lives on the filesystem — a plan file, a progress file, and a rulebook — so each amnesiac iteration reads enough from disk to keep going [^src2]. Coined by Geoffrey Huntley, it is one of the simplest practitioner versions of a [long-running agent](/ai-engineering/long-running-agents.md) [^src2]. Huntley's framing: "Ralph is a technique. In its purest form, Ralph is a Bash loop." [^src1]

## The loop

The canonical form is a single shell line [^src1]:

```bash
while :; do cat PROMPT.md | claude-code ; done
```

Ralph can run on any tool "that does not cap tool calls and usage" [^src1]. Addy Osmani's reference implementation expands the same idea into discrete steps: pick the next unfinished task from a list (`prd.json` or equivalent), build a prompt with task + context + persistent notes, call the agent, run tests/checks, append the outcome to `progress.txt`, update the task list (done/failed/blocked), and loop [^src2].

The reason it works is that **state lives outside the agent's context window** [^src2]. The agent is amnesiac each iteration; the filesystem is not. In Osmani's mapping, `prd.json` is the plan, `progress.txt` is the lab notes, and `AGENTS.md` is the rolling rulebook [^src2]. This is the same principle behind larger [harnesses](/ai-engineering/agent-harness.md) — externalize the plan, progress, and rules so a fresh session can resume.

## Core operating principles (from CURSED)

Huntley developed the technique building CURSED, "a brand new production-grade esoteric programming language," with Ralph able to program in a language absent from the LLM's training set [^src1].

- **Monolithic, one task per loop.** "Ralph works autonomously in a single repository as a single process that performs one task per loop." [^src1] You must "ask Ralph to do one thing per loop. Only one thing" — and trust the LLM to pick the most important next step; the restriction may relax as the project stabilizes but must be re-narrowed if it goes off the rails [^src1].
- **Deterministic stack allocation.** Allocate the same items to context every loop — the plan (`fix_plan.md`) and the specifications [^src1]. Specs are written out one-per-file after a long up-front requirements conversation with the agent, before any implementation [^src1].
- **Context frugality + subagents.** "You only have approximately 170k of context window to work with" so use as little as possible; more usage means worse outcomes [^src1]. The primary context window should act as a *scheduler*, spawning [subagents](/ai-engineering/multi-agent-systems.md) to do expensive allocation work like summarizing test results [^src1]. Parallelism is tunable — fan out widely for filesystem search/file-writing, but use only a *single* subagent for build/test to avoid "bad form back pressure" [^src1].
- **Don't assume it's not implemented.** A common failure: the LLM runs ripgrep, wrongly concludes code is missing, and re-implements it. Code-search is non-deterministic; the fix is a prompt "sign" telling Ralph to search before assuming and not duplicate work [^src1].

## Generate, then backpressure

Huntley frames the work as two phases [^src1]:

- **Phase one — generate.** "Generating code is now cheap." Wrong output is steered by updating the standard library (for wrong patterns) or the specifications (for building the wrong thing) [^src1].
- **Phase two — backpressure.** Since generation is easy, the hard part is ensuring Ralph "generated the right thing." Type systems give built-in backpressure; anything — security scanners, static analyzers, tests — can be wired in to reject invalid generation, but "the wheel has got to turn fast" [^src1]. Language choice trades correctness against loop speed: Rust gives strong checking but slow compilation, so the LLM needs more attempts [^src1]. For dynamically typed languages, wiring in a type checker is stressed as essential [^src1].

## Defeating the model's biases

- **No cheating / no placeholders.** Claude "has the inherent bias to do minimal and placeholder implementations" because its reward function is compiling code; Huntley counters with an emphatic sign and notes you can run more Ralphs to find placeholders and convert them into TODO items [^src1].
- **Capture intent in the moment.** Because each loop has a fresh context window, Ralph is told to write out *why* a test exists and why the implementation matters, leaving "little notes for future iterations" since future loops won't have the reasoning in context [^src1].
- **Self-improving rulebook.** `AGENT.md` is "the heart of the loop"; when Ralph learns how to run the project it updates `AGENT.md` (briefly) — but status reports must *not* go there [^src1].

## The TODO list and eventual consistency

Building with Ralph "requires a great deal of faith and a belief in eventual consistency" [^src1]. The TODO/`fix_plan.md` is watched "like a hawk" and thrown out often; when discarded, a planning-mode Ralph loop regenerates it from the specs before switching back to building mode [^src1]. You will "wake up to a broken codebase" — the judgment call is whether to `git reset --hard` and restart Ralph or craft new rescue prompts [^src1]. Tuning Ralph is likened to erecting signs (e.g. a "SLIDE DOWN, DON'T JUMP" sign next to a slide) until eventually "all Ralph thinks about is the signs" [^src1].

## Scope, claims, and limits

- **Greenfield only.** "There's no way in heck would I use Ralph in an existing code base"; it is best for "bootstrapping Greenfield, with the expectation you'll get 90% done with it" [^src1].
- **Engineers still required.** "There is no way this is possible without senior expertise guiding Ralph"; claims that a tool does 100% with no engineer are dismissed as "peddling horseshit" [^src1]. Yet the technique is "surprisingly effective enough to displace a large majority of SWEs as they are currently for Greenfield projects" [^src1].
- **Deterministically bad.** Huntley's signature line: "the technique is deterministically bad in an undeterministic world" [^src1]. Its Achilles' heel is the non-determinism of doing multiple implementations at once [^src1].

## Relation to long-running agents

Osmani classes the Ralph loop as a "simpler" practitioner version of [long-running agents](/ai-engineering/long-running-agents.md), popularized by Geoffrey Huntley and Ryan Carson [^src2]. Carson's Compound Product extends it by chaining multiple loops — an analysis loop reading daily reports, a planning loop emitting a PRD, an execution loop writing code — described as roughly the open-source version of the planner/generator/evaluator triad Anthropic landed on independently [^src2]. Anthropic's scientific-computing stack reduces the same idea to a `for` loop "that kicks the agent back into context whenever it claims completion and asks if it's really done" [^src2]. Osmani's summary: "you can build a working long-running agent in an evening with a bash script and a JSON file" [^src2].

## Loop engineering: the generalized concept

Addy Osmani (2026) generalizes the Ralph loop into **loop engineering** — "replacing yourself as the person who prompts the agent; you design the system that does it instead" [^src3]. The shift is from interactive prompting (type, read, type again) to designing a system that finds, distributes, checks, and records work automatically.

The practical driver: "Both products [Claude Code and Codex] have all five [building blocks] now." The same loop design works regardless of tool [^src3].

**Five building blocks of a loop** [^src3]:

| Block | What it is |
|---|---|
| **Automations** | Scheduled heartbeat that does discovery and triage by itself; findings come to you |
| **Worktrees** | Git worktrees so parallel agents don't collide on the same files |
| **Skills** | Encoded project knowledge so the agent doesn't re-derive context every run |
| **Plugins / connectors** | MCP-based integrations so the loop can act in your real tools (open PR, link ticket, ping Slack) |
| **Sub-agents** | Keep the maker away from the checker — one writes, one verifies |

**Plus one memory substrate**: a markdown file, Linear board, or any out-of-context store that holds what's done and what's next. "The agent forgets, the repo doesn't" [^src3].

**Claude Code loop primitives** [^src3]:
- `/loop` — re-runs on a cadence
- `/goal` — keeps going until a verifiable condition holds; a *separate small model* checks whether done after each turn (the checker is never the same as the maker)
- `/schedule` — cron task on Anthropic's cloud
- Hooks — shell commands at lifecycle points
- GitHub Actions — keeps running after you close the laptop

**The canonical one-day loop example** [^src3]: An automation runs every morning on the repo. A triage skill reads CI failures, open issues, and recent commits → writes findings to a markdown/Linear board. For each actionable finding: opens an isolated worktree, sends a subagent to draft the fix, a second subagent reviews against project skills and existing tests. Connectors open the PR and update the ticket. Anything unhandled lands in the triage inbox. The state file is the spine — tomorrow's run picks up where today stopped.

**Three problems that get harder, not easier, with better loops** [^src3]:
1. **Verification** — a loop running unattended is also a loop making mistakes unattended.
2. **Comprehension debt** — the faster the loop ships code you didn't write, the bigger the gap between what exists and what you understand.
3. **Cognitive surrender** — the temptation to stop having an opinion and just take whatever the loop returns. "Designing the loop is the cure when you do it with judgement and the accelerant when you do it to avoid thinking" [^src3].

Cross-reference: Boris Cherny (head of Claude Code): "I don't prompt Claude anymore. I have loops running that prompt Claude... My job is to write loops" [^src3]. See [Claude Code](/ai-engineering/claude-code.md) for routines (the native scheduled-automation primitive) and [Agent Skills](/ai-engineering/agent-skills.md) for the skill-building prerequisite.

## Loops creating loops: Theo's dynamic sub-loop architecture

Theo (t3.gg) documents a concrete application where a single master loop dynamically created multi-step sub-loops per-PR rather than following a fixed workflow structure [^src5].

**The problem**: a large refactor required at least three stacked PRs with sequential dependencies. Manually shepherding each through review, addressing code-review bot comments, and stacking the next PR was friction Theo was still doing himself.

**The solution prompt** — the key message that changed his workflow [^src5]:
> "Would it be possible to make a workflow that: (1) spins up a separate thread to make the PR, (2) spins up another thread to review that PR when it's filed, (3) puts the thread from (1) in a loop reviewing comments until it gets all approvals, and (4) the thread would merge the PR and trigger another one for the next piece."

**The heartbeat monitor pattern** [^src5]: the agent created a "heartbeat" attached to the main orchestration thread that polls every 5–10 minutes. On each wake-up:
1. Read implementation thread status
2. Detect filed PRs and new commits (`sha` check)
3. Spin up a fresh review thread when a new commit is pushed
4. Send actionable review findings back to the implementation thread
5. Re-review after fixes are pushed
6. Pull latest main before creating the next worktree for the next PR

**What happened overnight**: Theo set this off at 2:29 AM and woke up at 6:50 AM with four stacked PRs, reviewed through multiple cycles by code-review bots and an Opus reviewer thread, all merged. "My loops created loops and they did a great job at it" [^src5].

**The key property**: the workflow was *dynamically generated* for the specific problem, not a hardcoded pipeline. "This isn't a hard-coded every time I make a change I spin up one reviewer... This is a dynamic workflow that was created based on the specific needs of this specific problem I was solving" [^src5]. The agent determined what sub-loops the problem required, not the developer.

**Trade-off — cost**: "You will burn many more tokens when you run things in loops like this. And if it's going down the wrong path, it might go down that wrong path for longer... If you're paying API prices, you probably shouldn't be doing loops yet" [^src5]. The pattern is viable on a subscription but expensive on per-token billing.

**Pre-loop advice**: before designing the loop, audit what you currently do between agent turns — run tests, check output, commit, push, file PR, copy review comments back in. "Tell the agent to do that." The discipline: "find where you have to be involved and see what it takes to prompt yourself out of it" [^src5].

**Contrast with the Ralph loop**: Ralph is a static loop — same prompt, same context reload, repeat. Theo's architecture is a *meta-loop* — an orchestrating thread that dynamically instantiates specialized sub-loops shaped by the problem. Neither requires elaborate pre-built agent personas; the agent constructs the work structure dynamically. "The idea of pre-defining personas to go do things in your codebase fundamentally misses the cool part... It's dynamic" [^src5].

See [Claude Code](/ai-engineering/claude-code.md) for native loop primitives (`/loop`, `/goal`, `/schedule`) and worktrees that prevent file collisions across parallel threads.

[^src1]: [Ralph Wiggum as a "software engineer"](../../raw/web/ralph-wiggum-as-a-software-engineer.md)
[^src2]: [Long-running Agents](../../raw/web/long-running-agents.md)
[^src3]: [Loop Engineering](../../raw/notes/notes-clippings-loop-engineering.md) — Addy Osmani
[^src4]: [Full Walkthrough: Workflow for AI Coding — Matt Pocock](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-full-walkthrough-report.md) — Matt Pocock, AI Hero (conference talk); introduces the four-pattern escalating-autonomy spectrum (single task → HITL → AFK → Ralph) and the `/grill-me` skill for pre-build interview
[^src5]: [I guess we're writing loops now? — Theo (t3.gg)](../../raw/youtube/youtube-iJVJwmCKW9o-i-guess-we-re-writing-loops-now.md) — Theo, YouTube
</content>
</invoke>

<!-- RELATED:START (generated by bin/corpus_heal.py related — do not edit inside) -->

## Related across domains

- [AI-Augmented Knowledge Work](/productivity/ai-augmented-knowledge-work.md) · _productivity_

<!-- RELATED:END -->

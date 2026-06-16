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
aliases:
  - Ralph
  - Ralph technique
  - Ralph Wiggum technique
  - Ralph Wiggum
  - Ralph loop
  - while loop agent
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-16
updated: 2026-06-16
---

# Ralph Loop

**TL;DR.** The Ralph technique (a.k.a. the Ralph Wiggum technique) is, in its purest form, a Bash loop that repeatedly feeds the same prompt to a coding agent until a project is built [^src1]. State lives on the filesystem — a plan file, a progress file, and a rulebook — so each amnesiac iteration reads enough from disk to keep going [^src2]. Coined by Geoffrey Huntley, it is one of the simplest practitioner versions of a [[ai-engineering/long-running-agents|long-running agent]] [^src2]. Huntley's framing: "Ralph is a technique. In its purest form, Ralph is a Bash loop." [^src1]

## The loop

The canonical form is a single shell line [^src1]:

```bash
while :; do cat PROMPT.md | claude-code ; done
```

Ralph can run on any tool "that does not cap tool calls and usage" [^src1]. Addy Osmani's reference implementation expands the same idea into discrete steps: pick the next unfinished task from a list (`prd.json` or equivalent), build a prompt with task + context + persistent notes, call the agent, run tests/checks, append the outcome to `progress.txt`, update the task list (done/failed/blocked), and loop [^src2].

The reason it works is that **state lives outside the agent's context window** [^src2]. The agent is amnesiac each iteration; the filesystem is not. In Osmani's mapping, `prd.json` is the plan, `progress.txt` is the lab notes, and `AGENTS.md` is the rolling rulebook [^src2]. This is the same principle behind larger [[ai-engineering/agent-harness|harnesses]] — externalize the plan, progress, and rules so a fresh session can resume.

## Core operating principles (from CURSED)

Huntley developed the technique building CURSED, "a brand new production-grade esoteric programming language," with Ralph able to program in a language absent from the LLM's training set [^src1].

- **Monolithic, one task per loop.** "Ralph works autonomously in a single repository as a single process that performs one task per loop." [^src1] You must "ask Ralph to do one thing per loop. Only one thing" — and trust the LLM to pick the most important next step; the restriction may relax as the project stabilizes but must be re-narrowed if it goes off the rails [^src1].
- **Deterministic stack allocation.** Allocate the same items to context every loop — the plan (`fix_plan.md`) and the specifications [^src1]. Specs are written out one-per-file after a long up-front requirements conversation with the agent, before any implementation [^src1].
- **Context frugality + subagents.** "You only have approximately 170k of context window to work with" so use as little as possible; more usage means worse outcomes [^src1]. The primary context window should act as a *scheduler*, spawning [[ai-engineering/multi-agent-systems|subagents]] to do expensive allocation work like summarizing test results [^src1]. Parallelism is tunable — fan out widely for filesystem search/file-writing, but use only a *single* subagent for build/test to avoid "bad form back pressure" [^src1].
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

Osmani classes the Ralph loop as a "simpler" practitioner version of [[ai-engineering/long-running-agents|long-running agents]], popularized by Geoffrey Huntley and Ryan Carson [^src2]. Carson's Compound Product extends it by chaining multiple loops — an analysis loop reading daily reports, a planning loop emitting a PRD, an execution loop writing code — described as roughly the open-source version of the planner/generator/evaluator triad Anthropic landed on independently [^src2]. Anthropic's scientific-computing stack reduces the same idea to a `for` loop "that kicks the agent back into context whenever it claims completion and asks if it's really done" [^src2]. Osmani's summary: "you can build a working long-running agent in an evening with a bash script and a JSON file" [^src2].

[^src1]: [Ralph Wiggum as a "software engineer"](../../raw/web/ralph-wiggum-as-a-software-engineer.md)
[^src2]: [Long-running Agents](../../raw/web/long-running-agents.md)
</content>
</invoke>

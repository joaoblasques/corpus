---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/youtube/How AI agents & Claude skills work (Clearly Explained).md
    channel: youtube
    ingested_at: 2026-06-09
aliases:
  - agent skills
  - Claude skills
  - skills
  - progressive disclosure
  - skill.md
  - recursive skill building
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-09
updated: 2026-06-09
---

# Agent Skills

**TL;DR**: A *skill* is a modular capability file (`skill.md`) with a name, a description, and a body of instructions. Its key property is **progressive disclosure**: only the name and description sit in the context window; the full body loads on-demand when the agent decides the skill is relevant. This makes skills far cheaper than `AGENTS.md`/`CLAUDE.md` files, which are re-injected into context on every turn [^src1].

## Progressive disclosure — the core mechanic

A skill file has three parts: name, description, and body ("a bunch of info") [^src1]. When the file exists, only the name + description enter the context window. When the agent recognizes — from the description — that it needs the skill, it then reads the rest [^src1].

Concrete token contrast from the source: one 116-line "code structure" skill measured **944 tokens**. As an `AGENTS.md` file that 944 tokens is added *every single turn*; as a skill, only the name + description load up front — **53 tokens** — until the skill is actually invoked [^src1] [3:39](<../../raw/youtube/How AI agents & Claude skills work (Clearly Explained).md#t=3:39>).

## Skills vs AGENTS.md / CLAUDE.md

The source argues most always-on context files are unnecessary: **"95% of people don't need this"** [^src1]. The reasoning:

- Models are already good and the **codebase itself is context** — telling the agent "this code base uses React" is redundant because it can read the code [^src1].
- An `AGENTS.md`/`CLAUDE.md` file is re-added to context on *every* turn, spending its full token cost repeatedly (e.g. a 1,000-line file ≈ 7,000 tokens per run) [^src1].
- The legitimate ~5% case: **proprietary information or a personal methodology** that genuinely must be referenced on every turn [^src1].

> Note: this is one practitioner's opinionated stance (Ras Mic). It concerns *what to put in always-on context*, not a claim that project-level instruction files have no use. Contrast with [[ai-engineering/context-engineering|Context Engineering]] sources that treat CLAUDE.md as valuable long-term memory.

## Recursively building skills (the recommended method)

The anti-pattern: identify a workflow, then immediately hand-write the skill. The source calls this "the worst thing you can do" because the skill captures no experience of a *successful run* [^src1].

The recommended loop [^src1] [9:34](<../../raw/youtube/How AI agents & Claude skills work (Clearly Explained).md#t=9:34>):

1. **Identify the workflow.**
2. **Walk the agent through it step-by-step** — like mentoring a new employee; let it act, correct it, build a successful run *in context*.
3. **After a successful run, tell the agent to review what it did and write the skill** — now it has the context of what success looks like.
4. **It will still fail at gaps.** When it does, ask it *why it failed* (it reports the error descriptively), pass the failure back, have it fix the cause.
5. **After the fix works, tell it: "update the skill so this doesn't happen again."**
6. **Repeat.** The source's eight-source report generator took ~5 iterations of this loop to become reliable.

Mental model behind the method: LLMs **don't think — they predict tokens**, mapping input onto a vector space and returning the closest resemblance [^src1]. So an agent "will mimic you perfectly, but you've given it nothing to mimic" unless you supply a worked example. Treat agents like new employees, not magic boxes. See [[ai-engineering/ai-agent|AI Agent]].

## Don't download other people's skills

Two reasons [^src1] [12:34](<../../raw/youtube/How AI agents & Claude skills work (Clearly Explained).md#t=12:34>):

- **Security**: a downloaded skill is an easy attack vector.
- **Context**: a third-party skill lacks *your* successful-run context — the thing that makes a skill work. Reviewing others' skills to learn from them is fine; installing them wholesale is not.

## Relationship to context efficiency

Skills are fundamentally a [[ai-engineering/context-window-management|context window management]] technique: progressive disclosure keeps the window lean, and a leaner window is both cheaper and more performant (the model degrades as the window fills). See [[ai-engineering/context-window-management|Context Window Management]] and [[ai-engineering/context-engineering|Context Engineering]].

## See also

- [[ai-engineering/context-window-management|Context Window Management]] — why a lean window matters; sub-agents
- [[ai-engineering/context-engineering|Context Engineering]] — "less is more"; supply unique workflow, not general knowledge
- [[ai-engineering/ai-agent|AI Agent]] — token-predictor mental model; agents as new employees
- [[ai-engineering/multi-agent-systems|Multi-Agent Systems]] — scaling from one agent to sub-agents *for productivity*
- [[ai-engineering/sources/how-ai-agents-and-skills-work|Source: How AI agents & Claude skills work]]
- [[ai-engineering/README|AI Engineering hub]]

---

[^src1]: [How AI agents & Claude skills work (Clearly Explained)](<../../raw/youtube/How AI agents & Claude skills work (Clearly Explained).md>) — Greg Isenberg × Ras Mic, YouTube

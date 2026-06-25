---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-compound-engineering-how-every-codes-with-agents.md
    channel: web
    ingested_at: 2026-06-23
  - path: raw/web/github-everyinc-compound-engineering-plugin-official-compoun.md
    channel: web
    ingested_at: 2026-06-24
  - path: raw/_inbox/web-the-agent-that-saved-my-brain.md
    channel: web
    ingested_at: 2026-06-24
  - path: raw/web/web-my-ai-had-already-fixed-the-code-before-i-saw-it.md
    channel: web
    ingested_at: 2026-06-25
aliases:
  - compound engineering
  - compound knowledge
  - compound loop
  - plan-work-review-compound
  - compounding engineering
  - self-improving development systems
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-23
updated: 2026-06-25
---

# Compound Engineering

**TL;DR**: Compound engineering is a software development methodology where each coding session's learnings are captured back into `AGENTS.md`, making the agent progressively more effective with the same team and codebase. The loop: **plan → work → review → compound** [^src1]. The result: a single developer can manage 5 software products — and over time, the AI becomes "not just a tool but a compounding investment" [^src1].

## The four-stage loop

1. **Plan** — spend time on a spec, task breakdown, and context-setting before touching the model. "High-quality planning is the only way to reliably go from 0 to 1 with an agent" [^src1].
2. **Work** — execute with the model; maintain review checkpoints. "Once you've got the model doing work, your job is quality control and course-correction" [^src1].
3. **Review** — read the code. Even in agentic workflows, the engineer must understand output to catch regressions and steer quality [^src1].
4. **Compound** — write learnings back. Patterns the model got wrong, conventions the team uses, edge cases that emerged — these go into `AGENTS.md` so the next session starts smarter [^src1].

"The fourth step is where leverage lives" — most teams skip it and end up in a permanent catch-up loop [^src1].

## What compounds into AGENTS.md

After each work session, write to `AGENTS.md` [^src1]:
- **Mistakes the model made** → rules preventing them (e.g. "never modify `auth.ts` without adding a test")
- **Patterns the model used well** → templates to standardize
- **Team preferences** → explicit style rules the model has to re-learn without them
- **Edge cases encountered** → explicit guardrails

The test: any time the model makes a mistake, you should be able to add exactly one rule to `AGENTS.md` that would have prevented it [^src1].

This is the same mechanism as the [[ai-engineering/agent-harness|ratchet principle]] — "every line in a good AGENTS.md should be traceable back to a specific thing that went wrong."

## Scale: 5 products, 1 person

Every.to applies compound engineering across their software business: 5 products each managed by a single developer, with the compound step keeping the model aligned to each codebase's conventions [^src1]. The claim: compound engineering makes a single developer as productive as a team of 5 [^src1].

"The gap between engineers who get 10x productivity from AI and those who get 2x isn't model choice or prompt quality — it's whether they compound" [^src1].

## Time allocation model

Every.to's reported split: **80% planning and review, 20% execution** [^src1]. More time spent NOT coding (spec work, review, `AGENTS.md` updates) produces more output because the model executes the implementation.

This mirrors [[ai-engineering/spec-driven-development|Spec-Driven Development]] — the engineer moves up the abstraction ladder. Compound engineering *extends* spec-driven development with a fourth, learning-capture step (the spec front-loads intent; the compound step writes back what the run taught).

## The compound engineering plugin

The full compound engineering workflow is packaged as an open-source Claude Code plugin installable via the marketplace [^src2]:

```
/plugin marketplace add EveryInc/compound-engineering-plugin
```

The plugin ships **37 skills and 51 agents**, and works across Claude Code, Cursor, Codex, GitHub Copilot, Factory Droid, Qwen Code, and more [^src2].

**Full skill inventory** [^src2]:

| Skill | Purpose |
|---|---|
| `/ce-strategy` | Creates and maintains `STRATEGY.md` — product target problem, approach, persona, key metrics |
| `/ce-ideate` | Divergent ideation against strategy |
| `/ce-brainstorm` | Interactive Q&A; produces right-sized requirements doc |
| `/ce-plan` | Turns requirements into detailed implementation plan (searches past learnings) |
| `/ce-work` | Executes plan with worktrees and task tracking |
| `/ce-debug` | Multi-agent debugging pass |
| `/ce-code-review` | Multi-agent code review before merging |
| `/ce-compound` | Extracts 1–3 learnings; checks for stale knowledge; saves to `docs/` with YAML frontmatter |
| `/ce-product-pulse` | Time-windowed report on what users actually experienced (saved to `docs/pulse-reports/`) |

The **`/ce-compound` step** is what converts individual sessions into organizational knowledge: each brainstorm or plan step automatically searches `docs/` files from past compound steps, so past insights surface next time [^src2]. "80% is in planning and review, 20% is in execution" [^src2].

## Compound engineering in non-technical roles (Montaigne)

Austin Tedesco, Every's head of growth ("the first to tell you he doesn't have a technical background"), built **Montaigne** — a personal agent powered by the compound knowledge system [^src3]. Tools connected: Stripe, PostHog, Slack, Notion, Figma, email, calendar, and the full Every product suite. The agent lives in Claude Code terminal and as an OpenClaw bot on Slack.

Pattern: knowledge layers (MEMORY.md, domain context) + skills for repeat workflows → an agent that handles execution of recurring growth tasks so Tedesco can "have energy for the hard and fulfilling parts of my job" [^src3]. Setup took 3 weeks of exploration before building. The compound knowledge plugin is open-sourced for others to adapt.

## Compounding engineering in practice (Every.to)

Every.to's Cora (AI-enabled email assistant) team practices this as a first principle [^src4]. A concrete example: Claude Code reviewed prior PRs and pre-applied lessons — "Changed variable naming to match pattern from PR #234, removed excessive test coverage per feedback on PR #219, added error handling similar to approved approach in PR #241" — without being explicitly asked [^src4]. The key disciplines:

- Every PR that fixes something *teaches* the system — a bug fix is half-done if it doesn't prevent its entire category
- Every code review should yield extractable lessons written back to `CLAUDE.md`
- The workflow for new features: write a failing test *first*, have Claude iterate the detection logic until the test passes 10/10 runs, then codify the whole pattern in `CLAUDE.md` as a reusable workflow [^src4]

"Typical AI engineering is about short-term gains. You prompt, it codes, you ship. Then you start over. Compounding engineering is about building systems with memory, where every pull request teaches the system, every bug becomes a permanent lesson, and every code review updates the defaults." [^src4]

## See also

- [[ai-engineering/agentic-coding|Agentic Coding]] — the broader orchestration discipline; compound engineering is its learning-loop layer
- [[ai-engineering/spec-driven-development|Spec-Driven Development]] — the plan stage formalized; compound engineering adds the learning-capture step that spec-driven omits
- [[ai-engineering/generator-evaluator-separation|Generator–Evaluator Separation]] — the review stage as a structural pattern (separate grader)
- [[ai-engineering/agent-harness|Agent Harness]] — the ratchet principle (same mechanism)
- [[ai-engineering/claude-md-conventions|CLAUDE.md Conventions]] — where `AGENTS.md`/`CLAUDE.md` fit in the context stack
- [[ai-engineering/agent-skills|Agent Skills]] — skill files as an alternative to always-loaded AGENTS.md

---

[^src1]: [Compound Engineering: How Every.to Codes with Agents](../../raw/web/web-compound-engineering-how-every-codes-with-agents.md) — Every.to
[^src2]: [EveryInc/compound-engineering-plugin (GitHub)](../../raw/web/github-everyinc-compound-engineering-plugin-official-compoun.md) — EveryInc
[^src3]: [The Agent That Saved My Brain](../../raw/_inbox/web-the-agent-that-saved-my-brain.md) — Austin Tedesco, Every
[^src4]: [My AI Had Already Fixed the Code Before I Saw It](../../raw/web/web-my-ai-had-already-fixed-the-code-before-i-saw-it.md) — Every.to

---
type: synthesis
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-harness-design-for-long-running-application-development.md
    channel: web
    ingested_at: 2026-06-23
  - path: raw/notes/notes-clippings-new-in-claude-managed-agents-dreaming-outcomes-and-multiagen.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-clippings-a-harness-for-every-task-dynamic-workflows-in-claude-code.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/email/email-2026-06-12-two-weeks-with-claude-fable-5.md
    channel: email
    ingested_at: 2026-06-20
  - path: raw/web/web-compound-engineering-how-every-codes-with-agents.md
    channel: web
    ingested_at: 2026-06-23
  - path: raw/notes/notes-clippings-best-practices-for-computer-and-browser-use-with-claude.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/youtube/youtube-vtyx7ex-0ba.md
    channel: youtube
    ingested_at: 2026-06-17
aliases:
  - generator-evaluator separation
  - generator evaluator
  - separate grader
  - self-preferential bias
  - self-evaluation bias
  - evaluator pattern
  - separate the grader
tags:
  - corpus/ai-engineering
  - synthesis
created: 2026-06-23
updated: 2026-06-23
---

# Generator–Evaluator Separation

**TL;DR.** A recurring finding across this week's Anthropic-engineering and practitioner sources: **a model cannot reliably grade its own output.** When asked to verify or judge work it just produced, an LLM skews toward self-approval [^dyn] — the same self-consistency bias humans show. The durable response, converging independently across coding harnesses, managed-agent platforms, computer-use, and human-in-the-loop discipline, is to **move evaluation out of the generator's context** into a separate agent, model, rubric-grader, or human. This page names that convergence; the per-source detail lives on the linked pages.

## The core claim

In Anthropic's 3-agent GAN harness for long-running development, the evaluator runs "in a separate context window with no access to the generator's chain-of-thought" because **"a generator can't reliably grade itself"** [^gan]. The dynamic-workflows post names the failure mode directly: **self-preferential bias** — "when asked to verify or judge its own output, the model skews toward self-approval" — structurally identical to a GAN generator grading itself instead of facing a separate discriminator [^dyn]. See [Agent Harness](/ai-engineering/agent-harness.md).

The fix is architectural, not a better prompt: isolate the grader so its judgment is not contaminated by the reasoning that produced the work.

## Where the pattern shows up (this week's sources)

| Instance | What is separated | Mechanism | Source |
|---|---|---|---|
| **3-agent GAN harness** | Generator vs. evaluator | Evaluator in its own context window, blind to the generator's chain-of-thought; each rejection is a learning signal | [Agent Harness](/ai-engineering/agent-harness.md) [^gan] |
| **Managed Agents — Outcomes** | Agent vs. rubric grader | A separate grader "evaluates the output against your criteria in its own context window, so it isn't influenced by the agent's reasoning"; output that falls short is sent back for another pass | [Claude Managed Agents](/ai-engineering/claude-managed-agents.md) [^outcomes] |
| **Computer-use advisor tool** | Executor vs. advisor | A higher-intelligence advisor model (e.g. Opus advising a Sonnet executor) is called mid-task for planning and course-correction | [Computer Use](/ai-engineering/computer-use.md) [^cu] |
| **Compound engineering** | Build vs. review | The human read-the-code review step is a non-negotiable stage even in agentic workflows; ~80% of time is planning + review | [Compound Engineering](/ai-engineering/compound-engineering.md) [^compound] |
| **Fable 5 loop engineering** | Doing vs. verifying-the-right-work | "Verify the right work, not that the work is right" — the model self-checks each step; the human verifies the *task* was worth doing | [Claude Model Lineup](/ai-engineering/claude-models.md) [^fable] |
| **Cognitive surrender (anti-pattern)** | (collapse of separation) | When the human stops evaluating and blindly accepts model output, the separation disappears and a fragile "house of cards" accrues | [Cognitive Debt](/software-engineering/cognitive-debt.md) [^cog] |

## Why it works: bias, not capability

The evaluator does not need to be *smarter* than the generator (though in the advisor pattern it often is). It needs to be **uncontaminated**: judging in a context that never saw the generator's justifications removes the pull toward self-approval [^gan][^outcomes]. This is the LLM analogue of code review by a second engineer, or of separating the person who writes a test from the person who writes the code.

Two design corollaries from the sources:

- **Diversity of lens beats redundancy.** The advisor pattern uses a *different, stronger* model for the hard judgment calls rather than a second copy of the executor [^cu]; the GAN framing treats the evaluator as a discriminator the generator is trained (via prompting) to satisfy [^gan].
- **The done-condition must precede generation.** Anthropic's harness negotiates the "sprint contract" (scope + done-condition) *before* the generator starts; retroactively changing the bar once generation is underway is "the primary source of rework" [^gan]. This is why [Spec-Driven Development](/ai-engineering/spec-driven-development.md)'s constitution/spec and compound engineering's plan stage are the front half of the same loop the evaluator closes.

## The human's job moves up a level

As the model self-checks individual steps reliably, the human's evaluation does not disappear — it **relocates to the task level**. Fable 5's loop-engineering reframe is the cleanest statement: stop verifying that each step was executed correctly (the model does that) and start verifying that the *loop is producing the right outputs for the right problems* [^fable]. Compound engineering operationalizes the same shift by spending the majority of time on planning and review rather than execution [^compound].

The failure mode is **cognitive surrender**: abandoning the evaluator role entirely and merging whatever the model emits, which leaves a system the human can no longer debug [^cog]. Generator–evaluator separation is the structural defense; staying in the loop at the right altitude is the human discipline that keeps it intact.

## Relation to evaluation-as-testing

This pattern is the *in-the-loop* sibling of offline evaluation. [Agent Evaluation](/ai-engineering/agent-evaluation.md) covers golden datasets, online/offline evals, and LLM-as-judge as a *measurement* discipline; the separation here is the *runtime* version — a grader embedded in the production loop that gates each pass rather than scoring a batch after the fact. Both rest on the same premise that judgment must come from outside the thing being judged. See also [Agent Testing](/ai-engineering/agent-testing.md) for the verification-loop view and [Multi-Agent Systems](/ai-engineering/multi-agent-systems.md) for planner/generator/evaluator as a coordination topology.

## See also

- [Agent Harness](/ai-engineering/agent-harness.md) — the 3-agent GAN harness; self-preferential bias as a harness design criterion
- [Claude Managed Agents](/ai-engineering/claude-managed-agents.md) — Outcomes (rubric-driven self-correction)
- [Compound Engineering](/ai-engineering/compound-engineering.md) — review as a first-class stage
- [Claude Model Lineup](/ai-engineering/claude-models.md) — Fable 5 loop engineering ("verify the right work")
- [Computer Use](/ai-engineering/computer-use.md) — the executor/advisor split
- [Agent Evaluation](/ai-engineering/agent-evaluation.md) — the offline/measurement sibling
- [Cognitive Debt](/software-engineering/cognitive-debt.md) — what happens when the human drops the evaluator role
- [AI Engineering hub](/ai-engineering/README.md)

---

[^gan]: [Harness Design for Long-Running Application Development](../../raw/web/web-harness-design-for-long-running-application-development.md) — Anthropic engineering blog
[^outcomes]: [New in Claude Managed Agents: dreaming, outcomes, and multiagent orchestration](../../raw/notes/notes-clippings-new-in-claude-managed-agents-dreaming-outcomes-and-multiagen.md) — Anthropic announcement
[^dyn]: [A harness for every task: dynamic workflows in Claude Code](../../raw/notes/notes-clippings-a-harness-for-every-task-dynamic-workflows-in-claude-code.md) — Thariq Shihipar & Sid Bidasaria, Anthropic
[^fable]: [Two Weeks with Claude Fable 5 — Loop Engineering](../../raw/email/email-2026-06-12-two-weeks-with-claude-fable-5.md)
[^compound]: [Compound Engineering: How Every.to Codes with Agents](../../raw/web/web-compound-engineering-how-every-codes-with-agents.md) — Every.to
[^cu]: [Best practices for computer and browser use with Claude](../../raw/notes/notes-clippings-best-practices-for-computer-and-browser-use-with-claude.md) — Lucas Gonzalez & Luca Weihs, Anthropic
[^cog]: [What Modern Software Engineering Means (Google Cloud podcast — Seroter, Hammerly, Jaspan, Osmani)](../../raw/youtube/youtube-vtyx7ex-0ba.md)

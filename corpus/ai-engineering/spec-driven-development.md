---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/email/email-2026-06-16-claude-max-plan-is-not-what-you-think.md
    channel: email
    ingested_at: 2026-06-20
aliases:
  - spec-driven development
  - spec-first
  - spec-kit
  - SDD
  - specification-driven development
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-20
updated: 2026-06-20
---

# Spec-Driven Development

**TL;DR**: Instead of prompting agents with vague tasks, align on a written specification first — covering what to build, constraints, and success criteria — and let the AI work against that spec. The code becomes the output; the spec becomes the document you maintain [^src1].

## The problem: agents guess

When agent output isn't right, the instinct is to write a longer prompt. That's a trap. The core issue is that the bigger the codebase, the more context lives outside any prompt. One analysis found 31% more PRs now merge without review — the main issue being that no one wrote down what the code was actually supposed to do [^src1].

## The solution: spec before code

**Apoorv Gupta (Principal Software Engineer, Microsoft)** identifies the fix: align on goals first, then let AI work against a clear spec. One solid resource covering what to build, the constraints, and the success criteria — at which point code is just the output [^src1].

Key principle: **"The spec becomes the actual document you maintain."** Specs accumulate institutional knowledge in a way that prompts don't.

## GitHub Spec Kit workflow

GitHub's `spec-kit` (github/spec-kit) implements a six-step loop [^src1]:

| Step | Action |
|---|---|
| **Constitution** | Write the mission, stack, and guardrails the agent loads on each session |
| **Specify** | Define what to build |
| **Plan** | Break it into tasks |
| **Tasks** | Assign and sequence |
| **Implement** | Agent executes against the spec |
| **Validate** | Check against success criteria |

The **constitution** is the most load-bearing piece: "write the constitution first so the agent loads the same rules each session" [^src1]. It is effectively a persistent CLAUDE.md / AGENTS.md for a project.

For legacy code: draft the spec from existing docs and cover only what's changing. JetBrains offers a deeplearning.ai course on running spec-driven development on a real repo [^src1].

## When NOT to spec

"Running the full lifecycle for small tasks is just too much." Birgitta Böckeler documented a spec tool turning a simple bug fix into four user stories and sixteen criteria. Save spec-driven development for work that [^src1]:
- Needs to last in the codebase
- Involves other team members
- Has non-obvious requirements or constraints

For a quick fix with a clear test, just prompt and move on.

## Related patterns

- **Factory 2.0** (Factory AI, used by NVIDIA/Adobe/EY): extends the spec-driven idea into a "software factory" where Droids handle everything from bug-triage to shipping in a single loop; a Router picks the most efficient model per job. Engineers shift from writing code to building the systems that write it [^src1].
- **Spec-driven development vs vibe-coding**: see [[ai-engineering/vibe-coding|Vibe Coding]] for the contrast; spec-driven development is the discipline vibe-coding opts out of.

## See also

- [[ai-engineering/agentic-coding|Agentic Coding]] — the coding-agent context this sits in
- [[ai-engineering/claude-md-conventions|CLAUDE.md Conventions]] — the constitution as a CLAUDE.md file
- [[ai-engineering/agent-evaluation|Agent Evaluation]] — validation step in the spec loop
- [[ai-engineering/vibe-coding|Vibe Coding]] — the counter-pattern
- [[ai-engineering/README|AI Engineering hub]]

---

[^src1]: [Claude Max Plan Is Not What You Think (The Code newsletter)](../../raw/email/email-2026-06-16-claude-max-plan-is-not-what-you-think.md) — referencing Apoorv Gupta/Microsoft spec-driven development post, GitHub spec-kit, Böckeler/martinfowler.com

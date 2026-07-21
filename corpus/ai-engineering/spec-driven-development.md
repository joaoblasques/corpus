---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/email/email-2026-06-16-claude-max-plan-is-not-what-you-think.md
    channel: email
    ingested_at: 2026-06-20
  - path: raw/email/email-2026-06-14-claude-code-built-my-website-9-steps.md
    channel: email
    ingested_at: 2026-06-24
  - path: raw/youtube/youtube-14RP8liACqo-how-senior-engineers-actually-build-with-ai-in-2026-build-a.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-9dKA2hq4vf0-how-senior-engineers-actually-build-with-ai-in-2026-build-a.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-full-walkthrough-report.md
    channel: notes
    ingested_at: 2026-06-25
aliases:
  - spec-driven development
  - spec-first
  - spec-kit
  - SDD
  - specification-driven development
  - six-file context system
  - nine context files
  - PRD-driven workflow
  - Smart Zone Dumb Zone
  - grill-me
  - /grill-me
  - write-a-prd
  - prd-to-issues
  - Ralph loop
  - AFK multi-phase
  - HITL multi-phase
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-20
updated: 2026-06-24
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
- **Spec-driven development vs vibe-coding**: see [Vibe Coding](/ai-engineering/vibe-coding.md) for the contrast; spec-driven development is the discipline vibe-coding opts out of.

## Website building as a spec-driven workflow (Charlie Hills 9-step)

Charlie Hills documented a spec-first website build process that applies the "spec before code" discipline to non-technical contexts [^src2]:

1. **CONTEXT.md** — Claude Chat interviews you (questions about audience, goals, tone) and produces a structured facts file
2. **Claude Code interview** — Claude Code asks clarifying questions one at a time using the facts file
3. **COPY.md** — approve headlines, SEO keyword map, and meta descriptions *before any code is written*
4. **DESIGN.md** — provide 5 visual references + brand kit (fonts, colors, logo); Claude merges them into design direction
5-9. Build and iterate

The key discipline: all spec artifacts (copy, design direction) must be approved before implementation begins. This prevents the most common vibe-coding failure mode: generating a visually mediocre site because design input came after code [^src2]. Quote: "Claude Code is brilliant at building things that work and terrible at making them look good" — the design spec step is the fix.

This extends the GitHub Spec Kit Constitution→Specify→Plan→Tasks→Implement→Validate loop (§ above) to the content and design layer, making spec-driven development accessible to non-engineers building their own sites.

## Six-file context system (JavaScript Mastery)

A pre-build documentation set that the agent reads before writing any code, giving it "complete knowledge of what you're building" [^src3]. The six files live in a `context/` folder at project root:

| File | Purpose |
|---|---|
| **Project overview** | What the product is, who it's for, core flows, what's out of scope |
| **Architecture** | Tech stack, layer boundaries, invariants the codebase must never break |
| **Code standards** | TypeScript/framework conventions; keeps output consistent across the build |
| **AI workflow rules** | How to scope work, what to do when a decision is needed |
| **UI context** | Design tokens, component conventions; keeps UI coherent across sessions |
| **Progress tracker** | Current phase, what's in progress, what's complete, architectural decisions — the only file that updates constantly |

The progress tracker is what most developers skip and most need: at the start of any new session, the agent reads it and knows exactly where the build left off, "no re-explaining needed" [^src3].

Key distinction [^src3]: "vibe coding focuses on the outcome — you describe what you want, let the agent run, and react to whatever comes out. Spec-driven keeps the thinking with you and gives the agent a system to execute against. You stay the architect; the agent becomes the implementation engine."

The six-file system generates output from a planning conversation with a general-purpose AI (ChatGPT/Claude/Gemini), not from a blank page.

## Nine-file extended system (JavaScript Mastery v2)

An expanded context system for larger builds [^src4]:

1. Product overview (what/who/flows/out-of-scope)
2. Architecture
3. Folder structure
4. Code standards
5. UI rules
6. Design tokens
7. Library-specific patterns (with MCP-fetched examples)
8. Build plan
9. Living progress tracker

The `AGENTS.md` file ties these together: it loads context routing rules at session start, pointing the agent to each file and explaining when to consult it [^src4].

## PRD-driven workflow and context hygiene (Matt Pocock)

A full end-to-end spec-to-agent pipeline [^src5]:

1. **`/grill-me`** — relentless one-question-at-a-time interview that resolves every branch of a plan's decision tree before any code is written. "Interview the user until reaching shared understanding." The skill provides a recommended answer per question and explores the codebase itself when it can.
2. **`/write-a-prd`** — produce a PRD from the interview output
3. **`/prd-to-issues`** — convert the PRD into a Kanban board (one card per scoped unit)
4. **AFK agent** — run the issue board unattended

**Context hygiene**: the key ongoing discipline is keeping every task in the model's **Smart Zone** — the context window portion before the model begins to degrade. The tipping point is approximately 40% used / ~100K tokens [^src5]. Two tools:
- **Clearing context**: reset to empty (lossy, but every phase runs fresh and smart)
- **Compacting context**: summarize and continue (retains gist, costs fidelity)

**Four escalating autonomy patterns** [^src5]:
1. Single task in Smart Zone
2. **HITL multi-phase**: human kicks off each phase manually, clearing context between
3. **AFK multi-phase**: phases run in a loop without human kicks
4. **Ralph**: agent improvises the plan and runs continuously — "if you let the agent improvise, you end up with Ralph"

## See also

- [Agentic Coding](/ai-engineering/agentic-coding.md) — the coding-agent context this sits in
- [Compound Engineering](/ai-engineering/compound-engineering.md) — extends the spec-first plan stage with a learning-capture (compound) step that writes run learnings back to `AGENTS.md`
- [CLAUDE.md Conventions](/ai-engineering/claude-md-conventions.md) — the constitution as a CLAUDE.md file
- [Agent Evaluation](/ai-engineering/agent-evaluation.md) — validation step in the spec loop
- [Vibe Coding](/ai-engineering/vibe-coding.md) — the counter-pattern
- [How spec-driven development improves AI coding quality (Red Hat)](/ai-engineering/sources/how-spec-driven-development-improves-ai-coding-quality-red-h-a.md) — independent source corroborating the spec-first quality claim
- [Diving Into Spec-Driven Development With GitHub Spec Kit (Microsoft)](/ai-engineering/sources/diving-into-spec-driven-development-with-github-spec-kit-mic-doc.md) — second account of the spec-kit loop described above
- [AI Engineering hub](/ai-engineering/README.md)

---

## Further sources (not yet expanded)

- [How to Write a Good Spec for AI Agents: Five Principles](/ai-engineering/sources/how-to-write-a-good-spec-for-ai-agents-five-principles-ce.md) — quick-intake stub; five spec-writing principles balancing context limits against precision loss
- [Superpowers — Agentic Skills Framework for TDD-First Software Development](/ai-engineering/sources/superpowers-agentic-skills-framework-for-tdd-first-software--f.md) — quick-intake stub; a skills framework encoding YAGNI/DRY/red-green TDD as agent workflow

[^src1]: [Claude Max Plan Is Not What You Think (The Code newsletter)](../../raw/email/email-2026-06-16-claude-max-plan-is-not-what-you-think.md) — referencing Apoorv Gupta/Microsoft spec-driven development post, GitHub spec-kit, Böckeler/martinfowler.com
[^src2]: [Claude Code built my website (9 steps)](../../raw/email/email-2026-06-14-claude-code-built-my-website-9-steps.md) — Charlie Hills
[^src3]: [How Senior Engineers Actually Build With AI (Ghost AI build — six-file system)](../../raw/youtube/youtube-14RP8liACqo-how-senior-engineers-actually-build-with-ai-in-2026-build-a.md) — JavaScript Mastery, YouTube
[^src4]: [How Senior Engineers Actually Build With AI (Job Pilot build — nine files + five skills)](../../raw/youtube/youtube-9dKA2hq4vf0-how-senior-engineers-actually-build-with-ai-in-2026-build-a.md) — JavaScript Mastery, YouTube
[^src5]: [Full Walkthrough: Workflow for AI Coding — Matt Pocock](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-full-walkthrough-report.md) — Matt Pocock, AI Hero (conference talk notes report)

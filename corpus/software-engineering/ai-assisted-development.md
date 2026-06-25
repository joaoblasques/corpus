---
type: synthesis
domain: software-engineering
status: draft
sources:
  - path: raw/_inbox/email-2026-05-24-software-fundamentals-matter-more-than-ever.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/_inbox/email-2026-06-08-automated-doubt-open-code-review-how-llms-really-work.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/_inbox/email-2026-06-10-fake-rockstar-devs-apples-cheaper-ai-gits-weird-variable.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/_inbox/email-2026-05-21-how-do-junior-devs-break-in-now.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/web/github-alibaba-open-code-review-open-source-free-battle-test.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/web-youtube-30iqsttzbps.md
    channel: web
    ingested_at: 2026-06-25
aliases:
  - AI-assisted development
  - AI coding
  - coding with AI
  - agentic coding
  - AI code review
  - automated doubt
tags:
  - corpus/software-engineering
  - synthesis
created: 2026-06-12
updated: 2026-06-16
---

# AI-Assisted Development

**TL;DR**: AI can write code fast, but "it can also help you create a bigger mess faster if you do not understand the system you are building" [^src1]. The recurring theme across sources: AI makes software fundamentals *more* important, shifts the engineer's job from writing to reviewing, and demands deterministic guardrails around probabilistic output [^src1][^src2][^src3].

## Fundamentals matter more, not less

Tech With Tim's five fundamentals for coding with AI [^src1]:

1. **Reach a shared understanding first** — a common AI failure is building the wrong thing; make the AI ask questions and clarify edge cases before generating, since "no one knows exactly what they want at the beginning" [^src1].
2. **Create a shared language** — terms in plan, code, modules, and prompts must line up; undefined domain terms make the AI guess, producing wrong abstractions and naming [^src1].
3. **Use feedback loops** — types, tests, and automated checks let the AI see when code is wrong. "The rate of feedback is your speed limit"; TDD fits AI coding because it forces small steps [^src1].
4. **Make the codebase easy to test** — testable code needs clear boundaries; **deep modules** (meaningful functionality behind a simple interface) beat shallow scattered ones. "AI can create shallow, scattered code very easily" — lots of small files that look modular but are hard to review and change [^src1].
5. **Design the interface, then delegate the implementation** — own the system design and boundaries; let AI fill in lower-risk internals [^src1].

> "AI did not make software fundamentals optional. It made them more important." [^src1]

## The shift from writing to reviewing

Software engineering "has shifted from writing code to reviewing it" — the Pragmatic Engineer's 2026 survey describes developers as "overwhelmed and derailed" by the volume of AI-generated code they must audit [^src4]. The intuition that came from building line-by-line is being replaced by surface-level reading of agent output, thinning technical depth [^src4]. A related risk: dissent depends on depth — when engineers no longer understand systems deeply, objections lose their edge and architectural concerns go unvoiced [^src4]. Structural fixes (blameless postmortems, a mandatory "risks and unresolved concerns" section in design docs) beat asking engineers to "be braver" [^src4].

## AI rockstars and the maintainability cost

"Rockstar" developers leave behind overly complex, idiosyncratic codebases that prioritize individual cleverness over team maintainability — and "AI tools usually make this problematic pattern worse by rapidly producing massive amounts of fragmented code" without a cohesive architectural vision [^src3]. The counter-discipline is the same simplicity principle from [[software-engineering/software-design-principles|software design principles]]: not building unnecessary features avoids tech debt, a risk amplified now that AI makes code so cheap to generate [^src2].

## Deterministic guardrails around probabilistic agents

The most reliable AI-tooling pattern across sources is **pairing a probabilistic model with deterministic engineering**:

- **Automated doubt** — specialized subagents critique artifacts from multiple perspectives, front-loading scrutiny at the design stage and auditing for security, type safety, and logic errors post-implementation [^src2].
- **Open Code Review** (Alibaba, open-sourced after two years of internal use serving tens of thousands of developers) — a CLI that reads Git diffs and produces line-level review comments. Its core philosophy: "combine deterministic engineering with an agent, each handling what it does best" [^src5]. Deterministic logic handles file selection, bundling related files, and rule matching (the steps that must not go wrong); the agent handles dynamic decisions and context retrieval [^src5].
- General-purpose review agents (e.g. Claude Code with Skills) suffer **incomplete coverage** (cutting corners on large changesets), **position drift** (line numbers off target), and **unstable quality** — "a purely language-driven architecture lacks hard constraints on the review process" [^src5].

This mirrors the architectural argument that AI risk is bounded by the system, not the model — see [[software-engineering/ai-risk-architecture|AI Risk Architecture]].

## AI Studio + Firebase: vibe coding and loss of control

A live walkthrough of Google AI Studio + Firebase integration reveals structural risks of delegating to AI-driven platforms [^src6]:

**What worked**: fast data modeling (Firestore schema with `users`, `stories`, `connections` collections); automatic Firebase Auth + Google sign-in; parallel file editing by the AI ("it has the ability to edit these files in parallel, which is extremely cool"); budget cap UI for Gemini API key [^src6].

**What broke / gotchas**:

1. **Vendor lock-in on deployment**: AI Studio generates code that embeds the Gemini API key in the JS bundle — "visible to anyone who inspects your site source" — forcing Cloud Functions as a workaround to keep the key server-side [^src6].
2. **Existing project collision**: enabling Firebase integration connected to an existing project and started writing to that database. "You have an existing application in Firestore, so you're working on other stuff. You've just given AI Studio the ability to potentially connect to those and start writing to those databases. That should be terrifying to you." [^src6]
3. **Prompt injection**: AI-generated cloud function injected raw user story text directly into a system prompt — "if the user tries a prompt injection, they can just try to prompt inject my app right here" [^src6].
4. **Loss of control framing**: "when we're starting to use these AI tools, it's more like it we lose a bit of control. It's kind of like hiring an employee to write code for you. You don't get control over the code." [^src6]

Mitigation path applied: move AI matching logic to Firebase Cloud Functions (serverless, secrets safe), clone from GitHub, deploy independently of AI Studio [^src6]. Related: [[software-engineering/ai-risk-architecture|AI Risk Architecture]] — output risk vs. data risk vs. action risk.

## See also

- [[ai-engineering/agentic-coding|Agentic Coding]] (ai-engineering) — the agent-orchestration counterpart: coding-agent harness, skills, and workflow mechanics
- [[software-engineering/ai-risk-architecture|AI Risk Architecture]] — pairing probabilistic components with deterministic checks at the system level
- [[software-engineering/software-design-principles|Software Design Principles]] — deep modules, simplicity, and testability that AI coding stresses
- [[software-engineering/engineering-craft|Engineering Craft]] — the durable human skills (resourcefulness, persistence) under AI
- [[software-engineering/insforge|InsForge]] — agent-operated backend platform (DB/auth/storage/compute via MCP or CLI)
- [[software-engineering/README|Software Engineering hub]]

---

[^src1]: [Software fundamentals matter more than ever](../../raw/email/email-2026-05-24-software-fundamentals-matter-more-than-ever.md)
[^src2]: [Automated doubt, open code review, how LLMs really work](../../raw/email/email-2026-06-08-automated-doubt-open-code-review-how-llms-really-work.md)
[^src3]: [Fake rockstar devs, Apple's cheaper AI, Git's weird variable](../../raw/email/email-2026-06-10-fake-rockstar-devs-apples-cheaper-ai-gits-weird-variable.md)
[^src4]: [How do junior devs break in now](../../raw/email/email-2026-05-21-how-do-junior-devs-break-in-now.md)
[^src5]: [Open Code Review (Alibaba)](../../raw/web/github-alibaba-open-code-review-open-source-free-battle-test.md)
[^src6]: [Building with Google AI Studio + Firebase (YouTube 30iQsttzBps)](../../raw/web/web-youtube-30iqsttzbps.md)

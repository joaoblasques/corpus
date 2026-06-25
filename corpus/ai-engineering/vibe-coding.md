---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/email/email-2026-04-15-vibe-coding-isn-t-enough-here-s-a-better-approach.md
    channel: email
    ingested_at: 2026-06-15
  - path: raw/web/https-newsletter-towardsdatascience-com-e3t-ctc-l2-113-d5qls-3124b6d4.md
    channel: web
    ingested_at: 2026-06-15
  - path: raw/email/email-2026-06-07-being-good-at-ai-is-stupidly-simple.md
    channel: email
    ingested_at: 2026-06-15
  - path: raw/youtube/youtube-IiZ5HRaeX4s-stop-watching-tutorials-build-these-4-claude-projects-to-10x.md
    channel: youtube
    ingested_at: 2026-06-15
  - path: raw/youtube/youtube-we7bzvkbcvw.md
    channel: youtube
    ingested_at: 2026-06-17
  - path: raw/notes/notes-01-introduction-what-is-vibe-coding.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-03-the-70-percent-problem-ai-assisted-workflows-that-actuall.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-04-beyond-the-70-percent-maximizing-human-contribution.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-06-ai-driven-prototyping-tools-and-techniques.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/_inbox/email-2026-06-14-claude-code-built-my-website-9-steps.md
    channel: email
    ingested_at: 2026-06-24
  - path: raw/_inbox/web-how-anthropic-uses-claude-in-marketing-claude.md
    channel: web
    ingested_at: 2026-06-24
  - path: raw/_inbox/web-vibecode-claude-platform-api-case-study-claude-by-anthropic.md
    channel: web
    ingested_at: 2026-06-24
  - path: raw/web/web-ai-writes-code-faster-your-job-is-still-to-prove-it-works.md
    channel: web
    ingested_at: 2026-06-25
  - path: raw/notes/notes-local-ai-coding-report.md
    channel: notes
    ingested_at: 2026-06-25
aliases:
  - vibe coding
  - vibe-coding
  - spec-driven development
  - SDD
  - spec-driven
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-15
updated: 2026-06-24
confidence: 0.8
last_confirmed: 2026-06-17
---

# Vibe Coding (and why Spec-Driven Development supersedes it)

**TL;DR**: *Vibe coding* is building software by describing intent in natural language and letting a coding agent produce it — fast and accessible, but it "often produces code that doesn't match what you asked for" [^src1]. **Spec-Driven Development (SDD)** is the maturity step: write a clear spec first, then implement from it, so humans and agents align on the non-negotiables before any code is written [^src1][^src2].

## What vibe coding is

The everyday on-ramp: open Claude, pick a strong model, turn on thinking, and the single most useful trick for non-technical users is **"ask me questions first"** — Claude's `AskUserQuestion` tool flips the interaction so the model interviews *you* (3–5 questions) instead of you prompting it badly [^src3]. From there you can "build a real website or app tonight, yourself, using English," turning on bypass-permissions and iterating by pasting errors back in [^src3]. The same "let Claude interview you, then build the MVP, then iterate" loop drives the "4 Claude projects" approach — plan before building anything complex, then add features as you need them [^src4].

Two practitioner archetypes emerged early [^src6]: **bootstrappers** use AI to go from zero to a working MVP — the primary appeal is speed and low barrier to entry. **Iterators** integrate AI into their daily workflow for incremental improvements — the appeal is sustained productivity. The defining habit in either case is **"programming with intent"**: expressing the desired outcome in natural language rather than specifying step-by-step implementation [^src6].

## The 70% problem

AI reliably handles *accidental complexity* (Fred Brooks' term) — boilerplate, patterned code, mechanical transformations. The 30% it doesn't handle is *essential complexity*: architectural decisions, edge cases, security, long-term maintainability, and integration judgment [^src7]. Peter Yang named this the "70% phenomenon": AI goes 70% of the way, then performance falls sharply [^src7]. The "two steps back" antipattern captures the failure mode: fixing one bug introduces two new ones, producing a whack-a-mole cycle; the "demo-quality trap" is the corollary — impressive prototypes that fail under real-world conditions [^src7].

### Twelve Golden Rules of Vibe Coding

The discipline that keeps the 70% from becoming 50% [^src7]:

1. Start with a clear vision and a written plan
2. Break complex tasks into smaller prompts
3. **Don't merge code you don't understand**
4. **Treat AI as a junior developer (with supervision)**
5. **Isolate AI changes in Git by doing separate commits**
6. Don't blindly trust generated tests — validate they actually catch failures
7. Review with security in mind
8. Test at the integration level, not just unit tests
9. Keep context focused — don't let the session accumulate unrelated state
10. Document AI-generated decisions as you would human ones
11. Maintain a "humans review" gate before shipping
12. Update your system prompt / CLAUDE.md when you discover a mistake

## Human 30%: durable skills by seniority

The skills AI cannot substitute for, organized by career stage [^src8]:

**Senior**: architect-and-editor role (the human frames the architecture, the agent fills it in); Chat-Oriented Programming (CHOP — Steve Yegge's term for prompt-refinement-as-coding); mentoring and domain mastery; leadership and system-level judgment.

**Mid-level**: systems integration across services; specialization in a domain the agent can't fully model; DevOps ownership; code review with full organizational context.

**Junior**: fundamentals that let you recognize bad AI output; debugging without AI as a fallback; writing tests that actually fail; reading for maintainability.

Tim O'Reilly on the shift: "the end of programming as we know it today" — not the end of programming [^src8]. Simon Willison: AI makes strong programming skills *more* valuable, not less, because skill is what separates someone who uses AI well from someone who ships broken output [^src8].

## Prototyping with AI: the 80% prototype concept

AI can scaffold ~80% of an interface quickly, producing a working prototype in minutes [^src9]. The tradeoff is fidelity vs. control: higher-fidelity AI tools (Vercel v0, Lovable, Bolt.new, screenshot-to-code) move faster but offer less fine-grained control than AI-augmented IDEs. The scope-creep risk is highest in the prototyping phase — each iteration can pull the prototype further from the production goal. A prototype-to-production transition checklist should cover: security hardening, proper error handling, comprehensive testing, and performance under real load [^src9].

## Why vibe coding isn't enough

Vibe coding is fast but loses intent across agent sessions and invites scope drift [^src1]. The failure mode generalizes the [[ai-engineering/agent-harness|harness]] lesson: without written constraints, the agent picks interpretations silently and runs with them.

## Spec-Driven Development (the better approach)

SDD introduces a **plan → implement → verify** workflow [^src1]:

- Write **project constitutions** and **feature specs** that preserve context across agent sessions [^src1].
- Apply plan-implement-verify to guide the agent step by step, reducing cognitive overhead and keeping output aligned with intent [^src1].
- Use the same workflow in new *and* existing codebases; package it into reusable [[ai-engineering/agent-skills|agent skills]] [^src1].

The deeper case: SDD "aligns both humans and agents around the project's main non-negotiables" and addresses the core issues of vibe coding [^src2]. This is the same discipline as the [[ai-engineering/ai-product-management|PRD-before-agents]] practice (clear Definition of Done + Non-Goals) and Karpathy's **Goal-Driven Execution** ("don't tell it what to do; give it success criteria and watch it go") in [[ai-engineering/claude-md-conventions|CLAUDE.md Conventions]].

## "Coding is describing, not writing"

At the frontier of full-agentic work the *definition of coding itself* shifts: Boris Cherny (head of Claude Code), who hasn't hand-edited a line since November, describes his day as still "coding" even though it is "just talking to Claude code to code for you" — **"coding now is describing what you want, not writing actual code"** [^src5]. This is the endpoint of the vibe-coding on-ramp, but distinct from naive vibe coding because the discipline (plan mode, reading the output, human review, verifiable specs) is retained — the SDD discipline below scales *up* to this level rather than being discarded. See [[ai-engineering/sources/boris-cherny-100-percent-claude-code|Boris Cherny — 100% Claude Code]].

## Relationship to other operating modes

| Mode | Specification effort | Best for |
|---|---|---|
| **Vibe coding** | Minimal — describe intent | Prototypes, personal tools, learning |
| **Spec-Driven Development** | Up-front spec + verify loop | Production, multi-session, existing codebases |
| **[[ai-engineering/agentic-workflow|Agentic workflow]]** | Structured workflow files (WAT) | Repeatable multi-step automations |

## Non-technical practitioners building real workflows

The gap between "I wish this existed" and "I can build it myself" is now smaller than people realize — documented by practitioners without coding backgrounds:

**Austin Lau (Anthropic growth marketer)** — never opened a terminal before Claude Code launched; built two production workflows within a week [^src10]:
- A **Figma plugin** generating ad creative variations with a single click (45 min to build; saves ~30 min every time he updates a large batch of creatives across multiple aspect ratios). Process before: open Figma, copy frames, switch to Google Docs, paste copy, repeat across 10+ aspect ratios. Process after: specify frame, paste all variations, click a button.
- A **Google Ads copy workflow** (`/rsa` slash command) that cross-references brand voice skills, product accuracy rules, and RSA best practices, then exports upload-ready CSV files. What used to take 30 minutes per ad now takes 30 seconds.

Key practice patterns [^src10]: start with a tiny experiment (first project: a simple calculator app); let Claude read the existing API docs and prototype; describe the problem as you would to a colleague, not as a spec; treat Claude as a brainstorming partner who gets better with refinement. "All I would have to do is specify the frame of the creative… and with the click of a button, the Figma plugin will create all the different permutations."

**Vibecode** — a mobile-first app builder where users speak or type in natural language from their phone; Claude Code programmatically does the React Native/Expo generation, backend creation, and multi-file orchestration [^src11]. Real examples users built: a marketplace app for land sales in Australia; a virtual sensory board for children with autism. Company grew 3x to $10M ARR using this natural-conversation interface. "Coding is describing what you want, not writing actual code" — matches [[ai-engineering/vibe-coding#coding-is-describing-not-writing|"Coding is describing"]] above.

## Website building as a structured 9-step workflow

Charlie Hills documented a structured pre-build process that uses Claude's questioning ability before generating any code [^src12]:

1. **CONTEXT.md**: a Claude Chat interview where you answer questions about yourself, your audience, and your goals — produces a structured facts file
2. **Claude Code interview**: Claude Code asks one clarifying question at a time using that facts file as input
3. **COPY.md**: approve the full site copy (headlines, SEO keyword map, meta descriptions) *before any code is written*
4. **DESIGN.md**: 5 visual references + brand kit (fonts, colors, logo) merged by Claude into design direction
5–9. Build, iterate, and refine

Key constraint: "Claude Code is brilliant at building things that work and terrible at making them look good" — so the design references are mandatory input before code starts. Getting human sign-off on copy and design direction before implementation prevents the most common "vibe coding" failure mode [^src12].

## The cost of shipping without proof

Addy Osmani's 2026 survey quantifies what vibe-coding-without-review costs in production [^src13]:

- **45% of AI-generated code** has security flaws at merge time
- **XSS vulnerabilities at 2.74× the human rate** in AI-assisted codebases
- PRs are **18% larger** — developers accept bigger AI output batches with proportionally less scrutiny
- **Incidents up 24%**, change failure rates up 30%

The key rule: **"if you haven't seen the code do the right thing yourself, it doesn't work."** AI-generated proof ("the tests pass in my head") is not evidence. This is the spec-driven development principle applied to code review: the PR Contract (what, why, proof, risk, review focus) is the exit criteria, not a nice-to-have [^src13].

## Local vibe coding: compliance and performance trade-offs

For regulated industries (ITAR, HIPAA, finance), vibe coding with cloud models is prohibited — all code must stay on-premises [^src14]. Local model performance is approximately 5× slower than frontier cloud models and quality is "a model from 1–2 years ago" — still useful for non-critical tasks, but requires more review cycles.

The practical implication for the vibe-coding workflow: the permissive "just build it" loop requires more checkpoints with local models because the probability of subtle errors is higher. The spec-driven discipline (spec first, validate at each stage) becomes more critical, not less, when using local models [^src14].

## See also

- [[ai-engineering/agentic-coding|Agentic Coding]] — the broader coding-agent practice
- [[ai-engineering/agent-harness|Agent Harness]] — written constraints are what vibe coding lacks
- [[ai-engineering/ai-product-management|AI Product Management]] — PRD / Definition of Done / Non-Goals
- [[ai-engineering/prompt-engineering|Prompt Engineering]] — the "ask me questions first" pattern
- [[ai-engineering/agent-security|Agent Security]] — security risks specific to AI-generated code
- [[ai-engineering/agent-testing|Agent Testing]] — verification loops that catch what vibe coding misses
- [[ai-engineering/learning-ai-engineering|Learning AI Engineering]] — where vibe coding fits a beginner path
- [[ai-engineering/sources/beyond-vibe-coding-book|Beyond Vibe Coding (Book)]] — full source treatment
- [[ai-engineering/README|AI Engineering hub]]

---

[^src1]: [Vibe coding isn't enough. Here's a better approach (Spec-Driven Development)](../../raw/email/email-2026-04-15-vibe-coding-isn-t-enough-here-s-a-better-approach.md) — DeepLearning.AI / JetBrains course announcement
[^src2]: [From Vibe Coding to Spec-Driven Development](../../raw/web/https-newsletter-towardsdatascience-com-e3t-ctc-l2-113-d5qls-3124b6d4.md) — Mariya Mansurova, Towards Data Science
[^src3]: [Being good at AI is (stupidly) simple](../../raw/email/email-2026-06-07-being-good-at-ai-is-stupidly-simple.md) — Ruben Hassid
[^src4]: [Stop Watching Tutorials — Build These 4 Claude Projects](../../raw/youtube/youtube-IiZ5HRaeX4s-stop-watching-tutorials-build-these-4-claude-projects-to-10x.md) — Austin Marchese
[^src5]: [100% of my code is written by Claude — Boris Cherny (Lenny's Podcast)](../../raw/youtube/youtube-we7bzvkbcvw.md)
[^src6]: [Ch1 — Introduction: What Is Vibe Coding?](../../raw/notes/notes-01-introduction-what-is-vibe-coding.md)
[^src7]: [Ch3 — The 70% Problem](../../raw/notes/notes-03-the-70-percent-problem-ai-assisted-workflows-that-actuall.md)
[^src8]: [Ch4 — Beyond the 70%: Maximizing Human Contribution](../../raw/notes/notes-04-beyond-the-70-percent-maximizing-human-contribution.md)
[^src9]: [Ch6 — AI-Driven Prototyping: Tools and Techniques](../../raw/notes/notes-06-ai-driven-prototyping-tools-and-techniques.md)
[^src10]: [How Anthropic uses Claude in Marketing](../../raw/_inbox/web-how-anthropic-uses-claude-in-marketing-claude.md) — Austin Lau, Anthropic
[^src11]: [Vibecode — Claude Platform API case study](../../raw/_inbox/web-vibecode-claude-platform-api-case-study-claude-by-anthropic.md) — Vibecode
[^src12]: [Claude Code built my website (9 steps)](../../raw/_inbox/email-2026-06-14-claude-code-built-my-website-9-steps.md) — Charlie Hills
[^src13]: [AI Writes Code Faster. Your Job Is Still to Prove It Works.](../../raw/web/web-ai-writes-code-faster-your-job-is-still-to-prove-it-works.md) — Addy Osmani, addyosmani.com
[^src14]: [Local AI coding: compliance and performance report](../../raw/notes/notes-local-ai-coding-report.md) — notes report

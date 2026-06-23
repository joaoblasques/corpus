---
type: concept
domain: ai-business
status: draft
sources:
  - path: raw/email/email-2026-05-22-still-not-getting-interviews.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-05-14-3-things-you-have-to-do-in-your-interview.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/web/how-ruthless-prioritization-got-me-a-40-raise-and-a-head-of.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/web-the-top-5-skills-for-ai-engineering-taste.md
    channel: web
    ingested_at: 2026-06-17
  - path: raw/web/web-stop-feeding-me-ai-slop.md
    channel: web
    ingested_at: 2026-06-17
  - path: raw/web/web-the-top-5-skills-for-ai-engineering-clarity-of-communication.md
    channel: web
    ingested_at: 2026-06-17
  - path: raw/web/web-exactly-why-and-how-ai-will-replace-knowledge-work.md
    channel: web
    ingested_at: 2026-06-17
  - path: raw/email/email-2026-06-16-9-software-engineering-skills-a-de-should-have-and-how-to-le.md
    channel: email
    ingested_at: 2026-06-20
  - path: raw/notes/notes-how-to-compete-with-ai.md
    channel: notes
    ingested_at: 2026-06-17
aliases:
  - getting noticed
  - coding interview tips
  - developer portfolio
  - career growth for engineers
  - getting promoted
  - AI engineering skills
  - skills for AI engineers
  - competing with AI
  - expertise as files
  - Jevons paradox intelligence
  - stop selling hours
tags:
  - corpus/ai-business
  - concept
created: 2026-06-12
updated: 2026-06-23

---

# Navigating a Technical Career

**TL;DR.** Advancing as an engineer splits into three levers: (1) a **portfolio** that signals fit fast, (2) **interview behavior** that surfaces reasoning and collaboration, and (3) on-the-job **leverage** — controlling *what* you work on rather than absorbing all incoming chaos. The recurring theme across sources: visible, intentional, role-targeted work beats raw effort. Being "helpful" and busy does not get you noticed; being legible and essential does.

## Portfolio: signal fit in seconds

Recruiters skim and look for quick signals; a portfolio must make obvious what kind of developer you are and why someone should talk to you [^src1]. Four common failure modes [^src1]:

- **No wow factor.** Generic projects (to-do, weather, algorithm visualizer) are ignored. Add a twist: an AI-powered meal planner instead of a CRUD to-do app, or a stock tracker using news sentiment analysis. Functionality can stay simple; the angle makes it stand out [^src1].
- **Ambiguous names/descriptions.** "React Dashboard" is vague; "E-commerce sales dashboard for real-time order tracking" reads instantly. Keep descriptions to 1–2 sentences covering *what it does, the stack, and the outcome* [^src1].
- **No role targeting.** A grab-bag (ML model + WordPress blog + Python game + React app) looks unfocused, not versatile. Pick 2–3 projects aligned to the target role [^src1].
- **Amateur presentation.** With AI design help there is "no real excuse for having a poor-looking portfolio" — use complementary colors, modern fonts, consistent spacing, mobile-friendly layout [^src1].

A solved real business problem makes a stronger portfolio piece than a side project nobody asked for — see [[ai-business/monetizing-code|Monetizing Code]]. The mechanics of turning these signals into applications — persistent career-strategist context, per-job tailoring, remote-trust proxies — are **applied in** [[ai-business/ai-job-search|Finding a Job Using AI]].

## Interview behavior: communication is the majority of the score

The coding interview judges what you *say* as much as what you build. Three rules [^src2]:

1. **Stream your consciousness.** "More than half of the interview is just purely communication" [^src2]. Silent thinking leaves the interviewer blind to your approach; verbalizing reasoning and tradeoffs keeps you in contention even after mistakes.
2. **Code fluidly.** Over-reliance on autocomplete and IDE help leaves candidates unable to write basic syntax from memory — a bad signal regardless of underlying skill. Practice DSA prep *without autocomplete* [^src2].
3. **Treat the interviewer as a teammate.** They are asking "do I want to work with this person?" Collaboration earns hints and goodwill; most interviewers want you to succeed [^src2].

> [unsourced — note] Rule 2 (atrophied fundamentals from AI tooling) connects to the broader "shallow understanding" trend covered in [[ai-business/ai-and-the-job-market|AI and the Job Market]] and [[software-engineering/README|Software Engineering]].

## On-the-job leverage: control what you work on

A data engineer reports going from "drowning in work and still not getting noticed" to a 40% raise and Head of Data title — *without applying for it* — by changing how he prioritized, not by working harder [^src3]. Key claims:

- **Being helpful keeps you stuck.** "The more you say yes, the more you teach people to treat your time like it's free" [^src3]. Impact scattered across ten half-finished tasks is invisible; you become the go-to fixer, and "fixers don't get promoted. Builders of leverage do" [^src3].
- **Build a prioritization system.** Score every request by business value, real urgency, and who's asking/why. Bring leadership a plan (top 3), not a complaint — this earns "air cover" [^src3].
- **Make priorities public and boring.** A weekly Slack update (done / in progress / next) makes work undeniable; redirect "urgent" interrupters to the VP, and "nine out of ten times, they backed off" [^src3].
- **Proximity to the business beats tool mastery.** "Your proximity to the business is what makes you irreplaceable, not just your skill with SQL or Airflow" [^src3]. The unlock is moving from the *execution* layer to the *decision-making* layer — choosing what to build.

This dovetails with the gen-AI career advice that good work alone is insufficient: you must "let everyone know how impactful your work is" — see [[ai-business/ai-and-the-job-market|AI and the Job Market]]. Prioritization as a discipline overlaps with [[productivity/README|Productivity]].

## AI engineering skills: the human capabilities that compound

Several sources converge on a cluster of human skills that AI amplifies rather than replaces. These are the capabilities that matter *most* when working alongside AI agents.

### Taste: judgment about what good looks like

"Taste" is the ability to make thoughtful, correct decisions throughout the SDLC that lead to the outcomes you want and avoid the ones you don't [^src4]. It manifests in how an engineer steers an AI agent: keeping it in scope, specifying what to optimize for, providing clean schema designs — "fully articulating their decades of deep software engineering experience, but instead of writing the for loops, letting the agent do it" [^src4].

How to cultivate taste [^src4]:
- **Be deeply critical.** Ask Claude to perform adversarial reviews: "Look for the specific tradeoffs I made and help me consider the consequences of those tradeoffs."
- **Be hypothesis-driven.** Frame ideas as testable bets; split-test 2–3 approaches using parallel agents. "With AI, you can share a hypothesis and ask it to spin up N agents to test or validate your hypothesis" [^src4].
- **Be explicit about choices.** Name what you are trading off; knowing what *not* to do and anticipating failure conditions up front saves costly correction later.
- **Learn by observing others.** Pair programming, design reviews, watching great engineers — taste "sort of happens organically if you are paying attention and intentional" [^src4].

The failure mode: if you lack taste, the agent just optimizes to complete the task, producing the 5,500-line `main.py` spaghetti pile [^src4].

### Clarity of communication and vision

Clear communicators unlock tighter feedback loops with AI: less time wasted, less context spiral, more confidence to run longer unsupervised sessions [^src5]. The analogy used: a musician who deepens their theory knowledge gains more "musical vocabulary" to reach listeners — the same progression applies to prompting AI [^src5].

Practical practices for working with AI agents [^src5]:
- **Provide a concrete end-state**, not just a vague PRD — include mocks/screenshots, schema, and user stories the agent can reason about. Add a rule to CLAUDE.md so the agent doesn't drift from the vision.
- **Treat the AI like a co-worker.** "You would never say to a co-worker 'go build me a secure API for this shopping cart app' full stop." Be specific; list what's out of scope, what to do when stuck, and relevant best practices.
- **Communicate in verifiable criteria.** Feature checklists should be deterministically checkable — a Python script that hits live code paths, not just unit tests. "Do not use [LLM-as-judge] in the same context window as the agent that built the model (biases will creep in)" [^src5].
- **Don't overload.** Structure communications sequentially, in bite-sized chunks. If you must interrupt, consider revisiting the original plan rather than piling on corrections.
- **Spin up adversarial critics.** "Asking N agents to rip apart your design doc or architecture will lead to better designs" — 3 agents with slightly different focus areas, findings synchronized by an orchestrator [^src5].

### The thinking-first principle (anti-AI-slop)

AI amplifies your output; it does not generate thinking you haven't done. The failure mode is using AI "to simulate the appearance of having done [thinking]" — producing verbose, confident-sounding content that is "content-free" when interrogated [^src6]. The tell: when pushed back on, the author goes quiet, sends more AI output, or admits they haven't read what they sent.

"The value of human communication is distillation. I am relying on you because you've allegedly been thinking about this problem for a week… When you outsource the thinking and writing, I get homework instead of assistance" [^src6].

A 2x engineer with AI becomes 5–10x; an engineer with negative judgment also gets amplified — "bad decisions get made faster, but look more polished" [^src6]. The risk compounds when code gets merged that nobody understands: on-call engineers debug with generated runbooks for code nobody authored.

Correct use: think first, sketch key decisions, then use AI to help with prose. "The thinking is mine. The language is assisted" [^src6].

### The articulation gap: where human expertise meets AI capability

The real barrier between human expertise and AI isn't capability — it's *capture*. Experts have 20 years of pattern recognition locked in their heads that they've never written down. Once that knowledge is articulated into skills, SOPs, context files, and documented processes, AI can use it instantly and across all instances simultaneously [^src7].

This is a one-way ratchet: "Once expertise gets captured — into a skill, an open source project, a documented SOP, a published process — it never comes back out" [^src7]. The implication for engineers: your competitive edge is not keeping knowledge in your head; it's being the person who builds the scaffolding that captures and operationalizes it.

This connects directly to [[ai-business/ai-and-the-job-market|AI and the Job Market]]: the "utility" framing and the articulation gap are the same observation from different angles — AI capability exists, but human-structured context is what makes it deploy reliably.

## Competing with AI: 10 principles for hard-to-commoditize value

A condensed, practitioner-level distillation of the positioning problem — structured as 10 ordered moves [^src8]. Captures the distinct angles not already covered above.

**The macro context: Jevons Paradox for intelligence.** Token costs have fallen ~7,000x from 2022 to 2026 ($20 → $0.0028 per 1M tokens). "When first attempts become nearly free, the number of attempts explodes. Jevons Paradox: cheaper intelligence means more drafts, more tests, more analysis, and more competition" [^src8]. The threat is not AI becoming perfect — it is AI becoming cheap enough to replace *good enough*.

### The 10 moves

1. **Stop competing on what AI does better.** Research, summarization, first drafts, data analysis, coding — if your value is "I can do this faster with more information," AI will beat you. "Move above the output layer" [^src8].

2. **Move up the value chain.** Add value earlier in the process — strategy, framing, problem definition, decision-making. The higher you operate, the harder you are to commoditize.

3. **Judgment is the new work.** "Everyone can generate options. Few people can pick" [^src8]. Taste (covered above under AI engineering skills) is trained by reps, failures, and real consequences — not by reading about taste.

4. **Your expertise must become files.** "AI is only as good as the context it has. Your unique context is your moat" [^src8]. Concretely: `about-me.md`, `examples-i-love.md`, `examples-i-hate.md`, `mistakes-i-won't-repeat.md`, `audience.md`, `templates/`. Turn prompts into reusable memory; feed AI your taste, scars, standards, and constraints. This is the tactical implementation of what Miessler calls the "articulation gap" — make your expertise externalizable so you, not only AI, can reuse it.

5. **Stop selling hours.** Time spent is irrelevant when AI can replicate output faster. Better pitches: "I understood the real problem / I knew what to ignore / I found the missing risk / I made the decision easier" [^src8]. Sell taste, judgment, and outcomes. Relates to the [[ai-business/monetizing-code|Monetizing Code]] framing (sell a result, not code).

6. **Use AI where you already have taste.** Use AI to multiply strengths, not hide weaknesses. "Your skill is the steering wheel. AI is the engine" [^src8]. Keep one manual skill alive to avoid capability atrophy.

7. **Build systems, not one-off answers.** "The answer person gets replaced first. The system person compounds" [^src8]. Templates, checklists, workflows, reusable prompts — a task disappears after you do it; a system keeps working. Mirrors the leverage argument in §On-the-job leverage above.

8. **Stay close to reality.** "AI is trained on text. Reality is uglier — and more valuable" [^src8]. Talk to customers, read support tickets, inspect raw data, test prototypes. As the internet gets more synthetic, direct contact with real-world signal becomes scarcer and more premium.

9. **Kill additive work.** "For every new AI workflow you add, kill 3 tasks" [^src8]. Cheap intelligence creates infinite appetite. Taste is saying no before the machine starts cooking — a counter to the tendency to pile automation on automation without clearing the backlog of tasks.

10. **Play the long game.** Not about learning "AI tools." About upgrading yourself: continuous adaptation, better judgment, stronger relationships, sharper POV, more accountability. The formula: `human judgment + unique context + taste + trust + adaptability + continuous compounding = hard-to-commoditize value` [^src8].

**Overlap note.** Principles 3 (judgment/taste) and 4 (articulation gap via files) reinforce the sections above — they are included here for the framing clarity the 10-principle structure provides. Principles 1–2, 5, 8–9 add angles not covered elsewhere in this page.

## Software engineering skills: the DE lane

Data engineers sometimes under-invest in software engineering fundamentals, focusing on tools (Spark, Airflow, dbt) without the craft skills that make those tools productive at scale. Alejandro Aboy's 9 SE skills for DEs (2026) identifies the transferable skills with the most leverage [^src9]:

- **Pick one lane and go deep** — employer signal: depth is more credible than breadth across 20 tools.
- **Write understandable code** — code is read at 3am during incidents; clarity is a production concern, not just aesthetics.
- **Know one design pattern** — Repository, Factory, Observer — enough to make pipelines extensible without rewriting from scratch.
- **Participate in code review** — both as author and reviewer; the review habit compresses years of learning into months.
- **Contribute to open-source** — the strongest DE portfolio signal: initiative, collaboration, real-world craft.

> "The difference between a senior DE and a junior DE that knows a lot of tools is often just these software engineering fundamentals." [^src9]

This complements the on-the-job leverage section: being legible (clear code, review participation, OSS record) makes your work undeniable without extra status-maintenance overhead.

## Gotchas

- Portfolio "wow factor" advice is from a creator who sells courses (Tech With Tim); the guidance is generic-sound but vendor-adjacent [^src1][^src2].
- The 40% raise story promotes a paid "Workload Prioritization Playbook"; the full rubric is paywalled, so the framework here is the free-tier summary [^src3].
- The "top 5 skills" series (taste, clarity/vision) is from a Substack newsletter (The Engineer's Etlist); claims about outcomes are anecdotal, not empirical [^src4][^src5].
- The "Exactly why and how AI will replace knowledge work" piece is a long-form opinion from a security consultant (Daniel Miessler); the capability-stack model and "articulation gap" framing are his own synthesis, not peer-reviewed [^src7].
- The "How to Compete with AI" source (10 principles) is a visual/slide-format note (possibly a social-media infographic or presentation deck) clipped from the user's Obsidian inbox; author unidentified in the raw file. The token-price table is empirically grounded (cites DeepSeek V4 Flash cache pricing for 2026); the 10 principles are framework advice, not research [^src8].

[^src1]: [still not getting interviews?](../../raw/email/email-2026-05-22-still-not-getting-interviews.md)
[^src2]: [3 things you have to do in your interview](../../raw/email/email-2026-05-14-3-things-you-have-to-do-in-your-interview.md)
[^src3]: [How ruthless prioritization got me a 40% raise and a head of data title I didn't even want](../../raw/web/how-ruthless-prioritization-got-me-a-40-raise-and-a-head-of.md)
[^src4]: [The Top 5 Skills for AI Engineering: Taste](../../raw/web/web-the-top-5-skills-for-ai-engineering-taste.md)
[^src5]: [The Top 5 Skills for AI Engineering: Clarity of Communication and Vision](../../raw/web/web-the-top-5-skills-for-ai-engineering-clarity-of-communication.md)
[^src6]: [Stop Feeding Me AI Slop](../../raw/web/web-stop-feeding-me-ai-slop.md)
[^src7]: [Exactly Why and How AI Will Replace Knowledge Work](../../raw/web/web-exactly-why-and-how-ai-will-replace-knowledge-work.md)
[^src8]: [How to Compete with AI (10 principles)](../../raw/notes/notes-how-to-compete-with-ai.md)
[^src9]: [9 Software Engineering Skills a DE Should Have (Alejandro Aboy)](../../raw/email/email-2026-06-16-9-software-engineering-skills-a-de-should-have-and-how-to-le.md)

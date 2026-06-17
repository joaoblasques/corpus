---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/youtube/youtube-we7bzvkbcvw.md
    channel: youtube
    ingested_at: 2026-06-17
aliases:
  - Boris Cherny interview
  - 100% of my code is written by Claude
  - head of Claude Code interview
  - Lenny Boris Cherny
tags:
  - corpus/ai-engineering
  - source
created: 2026-06-17
updated: 2026-06-17
---

# Boris Cherny — "100% of my code is written by Claude" (Lenny's Podcast)

**TL;DR.** Boris Cherny, head of Claude Code at Anthropic, has not hand-edited a line of code since November and ships "10, 20, 30 pull requests" a day, all written by Claude Code, with "like five agents running" at once [^src1]. The interview is the practitioner source for *full-agentic coding* as a lived workflow rather than a theory: coding is now "describing what you want, not writing actual code" [^src1], and the leverage shifts entirely to specs, taste, product judgment, and parallel-agent orchestration. This page captures the workflow, the product/management principles, and the build-for-AI advice; concepts are cross-linked to their canonical pages.

## The full-agentic workflow

- **100% AI-written, since November.** "100% of my code is written by Claude code. I have not edited a single line by hand since November" — while still "one of the top few most productive engineers" at Anthropic [^src1]. He still *reads* the code and keeps a human review checkpoint; Claude reviews 100% of Anthropic's PRs with a human layer after [^src1].
- **~5 parallel agents, all the time.** "At the moment I have like five agents running" during the recording; "I always have a bunch of agents running" [^src1]. Anthropic calls running many sessions at once **"multi-clouding"** [^src1]. Surface split: roughly a third terminal, a third desktop app, a third the iOS app — "a third of my code... is the iOS app, which is just so surprising" [^src1]. See [[ai-engineering/claude-code|Claude Code]], [[ai-engineering/multi-agent-systems|Multi-Agent Systems]].
- **Plan mode first.** "I start almost all of my tasks in plan mode, maybe like 80%." Plan mode is "actually really simple... we inject one sentence into the model's prompt to say, 'Please don't write any code yet.'" After a good plan he auto-accepts edits: "if the plan works good, it's just going to one-shot it" [^src1]. Echoes the explore→plan→code pattern in [[ai-engineering/agentic-coding|Agentic Coding]].
- **Use the most capable model.** Tip #1: "use the most capable model... I have maximum effort enabled always." Counterintuitively a cheaper model can cost *more*: "because it's less intelligent, it actually takes more tokens in the end to do the same task" [^src1]. Connects to [[ai-engineering/agent-cost-management|Agent Cost Management]].
- **Run times are growing.** Sonnet 3.5 a year ago "could run for maybe 15 or 30 seconds before... going off the rails"; Opus 4.6 runs "10, 30, 20, 30 minutes unattended," with examples running "hours or even days" and "some examples where they ran for many weeks" [^src1]. See [[ai-engineering/long-running-agents|Long-Running Agents]].

## "Claudify": under-resource, then go faster

Two team principles that *force* delegation to the agent [^src1]:
- **Under-resource everything a little.** "When you under-fund everything a little bit... people are kind of forced to Claudify." A single engineer on a project ships fast because the only way to is to automate with Claude [^src1].
- **Encourage speed.** "If you can do something today, you should just do it today" — early on "our only advantage was speed" [^src1].
- **Be loose with tokens.** Advice to CTOs: "don't try to cost cut at the beginning. Start by just giving engineers as many tokens as possible"; optimize (Haiku/Sonnet, scaling) only once an idea proves out [^src1]. Anthropic is "starting to see some engineers that are spending... hundreds of thousands a month in tokens" [^src1]. The lived form of [[ai-engineering/agent-cost-management|Agent Cost Management]]'s "spend before optimizing."
- **Productivity per engineer up ~200%** in PRs since Claude Code; the team "probably 4x'd" while per-engineer output more than tripled — versus the "few percentage points" a year of code-quality work used to buy at Meta [^src1].

## Building for / on the model (advice for AI builders)

- **Don't box the model in.** "Almost always you get better results if you just give the model tools, you give it a goal, and you let it figure it out. I think a year ago you actually needed a lot of the scaffolding, but nowadays you don't really need it" [^src1]. "Don't try to give it a bunch of context up front. Give it a tool so that it can get the context it needs" — the [[ai-engineering/context-engineering|context-engineering]] inversion. *(Contrast note: this is a strong "minimal-scaffolding" stance; see Contradictions below.)*
- **The bitter lesson.** Cite Sutton: "the more general model will always outperform the more specific model." Practical corollary: "always bet on the more general model... don't try to use tiny models for stuff, don't try to fine-tune." Scaffolding may add "maybe 10 20%" but "often these gains just get wiped out with the next model" [^src1].
- **Build for the model 6 months out, not today.** Claude Code "bet on building for the model 6 months from now." The cost: "your product market fit won't be very good for the first 6 months," but when the model lands "the product is going to click." The inflection came with Opus 4 / Sonnet 4 (first ASL-3-class model) [^src1].
- **The product is the model.** For Claude Code "we inverted that. We said the product is the model... put the minimal scaffolding around it, give it the minimal set of tools." In research terms this is keeping the model **"on distribution"** — building for what the model is trying to do [^src1].
- **Latent demand (and its modern form).** The traditional version: ship where people already (mis)use a product — Facebook Marketplace came from "40% of posts in Facebook groups are buying and selling," and Claude Cowork came from people using Claude Code non-technically (recovering wedding photos from a corrupted drive, analyzing an MRI, a genome, growing tomato plants) [^src1]. The modern version: "look at what the model is trying to do and make that a little bit easier" [^src1]. See [[ai-engineering/ai-product-management|AI Product Management]].

## Where the work is going

- **Coding is "virtually solved."** "At least for the kinds of programming that I do, it's just a solved problem because Claude can do it"; the frontier is moving to *Claude proposing what to build* — reading feedback channels, bug reports, telemetry and putting up PRs unprompted ("a little more like a co-worker") — and to non-coding general tasks via Cowork (paying a parking ticket, project management, syncing spreadsheets, Slack/email) [^src1].
- **The role shift.** "The title software engineer is going to start to go away... replaced by builder," or "everyone's going to be a product manager and everyone codes." On the Claude Code team "everyone codes" — PM, EM, designer, finance, data scientist; roles have "maybe a 50% overlap" [^src1]. The most-rewarded people will be "curious... generalists [who] cross over multiple disciplines" [^src1]. Career framing lives in [[ai-business/ai-and-the-job-market|AI and the Job Market]].
- **Printing-press analogy.** Cherny's historical anchor: literacy was sub-1% (scribes) before Gutenberg; printed volume and cost shifted ~100×, literacy reached ~70% over 200 years. The transition was "inherently democratizing" but "very disruptive and... painful for a lot of people" [^src1].

## Safety as a product driver

Anthropic's product ladder is "coding, then tool use, then computer use" — chosen because each step is how they study safety in three layers: **mechanistic interpretability** (Chris Olah; monitoring neurons, superposition), **evals** (the model "in a petri dish"), and **behavior in the wild** [^src1]. Claude Code was used internally ~4–5 months before release to study safety, shipped as a "research preview"; the **open-source sandbox** ("works with any agent, not just Claude Code") is Anthropic's "race to the top" lever [^src1]. See [[ai-engineering/agent-security|Agent Security]].

## Contradictions / tensions to track

- **Scaffolding stance vs. the corpus's harness emphasis.** Cherny argues "you don't really need" the scaffolding now — "don't box the model in," bet on the general model, expect the next model to wipe out a 10–20% scaffolding gain [^src1]. The corpus's [[ai-engineering/agent-harness|Agent Harness]] / [[ai-engineering/agentic-coding|Agentic Coding]] pages (Builder.io AX, Osmani) hold that the *harness* — context, hooks, tests, review loops — matters as much as the model. These are not flatly opposed (Cherny still relies on plan mode, sandboxing, CLAUDE.md, `/goal`, and human review), but they weight model-vs-scaffolding differently; the reconciliation is *minimal but well-designed* scaffolding around a strong general model, not zero scaffolding.

## See also

- [[ai-engineering/claude-code|Claude Code]] — the tool; parallel sessions, plan mode, model config
- [[ai-engineering/agentic-coding|Agentic Coding]] — orchestration theory this interview instantiates
- [[ai-engineering/vibe-coding|Vibe Coding]] — "coding is describing, not writing"
- [[ai-engineering/long-running-agents|Long-Running Agents]] — multi-hour/day runs
- [[ai-engineering/ai-product-management|AI Product Management]] — latent demand, "everyone's a PM"
- [[ai-engineering/agent-cost-management|Agent Cost Management]] — loose-with-tokens, best-model economics
- [[ai-engineering/README|AI Engineering hub]]

---

[^src1]: [100% of my code is written by Claude — Boris Cherny (Lenny's Podcast)](../../../raw/youtube/youtube-we7bzvkbcvw.md)

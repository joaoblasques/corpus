---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/youtube/How AI agents & Claude skills work (Clearly Explained).md
    channel: youtube
    ingested_at: 2026-06-09
  - path: raw/web/what-s-the-real-deal-about-skills-this-is-not-a-mcp-is-dead.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/github-zazencodes-agent-skills-a-central-version-controlled.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/github-zazencodes-agent-skills-a-central-version-controlled-dac91b4a.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/github-luongnv89-asm-the-universal-skill-manager-for-ai-codi.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/agent-skills.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/notes/notes-clippings-how-anthropic-enables-self-service-data-analytics-with-claud.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-clippings-everyinccompound-knowledge-plugin-ai-powered-workflows-for-k.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-clippings-everyincclaude-commands-our-favorite-claude-code-commands.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-clippings-everyinccharlie-cfo-skill-claude-code-skill-for-bootstrapped.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-clippings-lessons-from-building-claude-code-how-we-use-skills.md
    channel: notes
    ingested_at: 2026-06-17
aliases:
  - agent skills
  - Claude skills
  - skills
  - progressive disclosure
  - skill.md
  - recursive skill building
  - skill manager
  - SKILL.md
  - skills-as-SDLC
  - anti-rationalization tables
  - process over prose
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-09
updated: 2026-06-17
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

## Skills as the cure for context rot

A second source frames skills primarily as the remedy for **context rot** — the failure mode where, after "70 tools, 5 MCP connections... RAG capabilities for 5K documents and 7 pages system prompts," the agent "starts not giving a f*** about the instructions" [^src2]. Skills fix this because they are "reusable prompts that Agents can load ON DEMAND" rather than at startup [^src2]. The reframing of system-prompt architecture: **"Your system prompt now becomes the identity and sitemap of what your Agents can do, and SKILLs are guidance to execute certain actions"** [^src2].

The most-emphasized point in this source: skills don't just store reusable prompts — **they tell the agent *how* and *when* to use its tools**. "You can configure a tool and specify what the tool does, but a skill can tell the agent how and when to use" it [^src2]. This makes skills complementary to, not a replacement for, [[ai-engineering/mcp|MCP]] and [[ai-engineering/rag|RAG]]: combine them to keep the system prompt lean while giving the agent deep capabilities on demand [^src2]. The named hard part is the same as in the YouTube source — writing the *description* well enough that the agent invokes the skill in the right situation [^src2].

## Anatomy and the anti-rationalization (description) problem

Across sources the file shape is consistent: a directory whose name matches the skill, containing `SKILL.md` with YAML frontmatter (`name`, `description`, optionally `version`, `license`, `allowed-tools`, `effort`) followed by markdown instructions; optional `references/` (extra markdown) and `scripts/` (executable code in any language) sit alongside [^src2] [^src4]. The load order is the disclosure mechanism: only the frontmatter `description` enters context first; the body and helper files load when the skill fires [^src2].

The recurring failure mode is **rationalizing a bad description** — a skill that is well-written but never gets picked up (or fires at the wrong time) because its description doesn't clearly state *when* to use it. "Failing to explain that properly will take all the advantages from these assets" [^src2]. This is the skills-side analogue of the SDLC discipline below: the description is the contract.

## Skills-as-SDLC and skill managers

As teams accumulate skills across multiple agents, skill management becomes its own software-development-lifecycle problem (create → develop → audit → test → publish), and tooling has emerged to handle it.

**Central version control (zazencodes/agent-skills)**: keep all skills for different tools in one Git repo and symlink them into each agent's skill folder, so "either way, you're changing the same files" [^src3]. The canonical folder is `agents/` (→ `~/.agents/skills`), with `claude/` as a required mirror (→ `~/.claude/skills`) "because Claude Code doesn't read `~/.agents/skills`"; other agents (codex, copilot, cursor, gemini) are opt-in [^src3]. A `setup_symlinks.py` script backs up existing system skills, copies them into the repo, and replaces each system directory with a symlink back [^src3].

**Universal skill manager (luongnv89/asm)**: a TUI+CLI to "install, search, audit, and organize all your agent skills — everywhere," across 19 providers (Claude Code, Codex, OpenClaw, Cursor, Windsurf, Cline, Gemini CLI, Antigravity, etc.) [^src4]. It addresses skills "scattered everywhere... installed three times" with no visibility and risky manual installs [^src4]. The full lifecycle: `asm init` (scaffold), `asm link` (symlink for live-editing iteration), `asm audit security` / `asm eval` (score), `asm install github:user/repo`, and `asm publish` (security audit → signed manifest → PR to the registry) [^src4].

**Security and verification are first-class.** Both managers treat installing third-party skills as an attack surface (consistent with the YouTube source's "don't download other people's skills" security point). asm's scanner flags shell execution, network access, credential exposure, and obfuscation *before* install [^src4]. Its automated **verification** requires four criteria for a verified badge: valid frontmatter (`name`+`description`), ≥20 characters of body instruction, no malicious patterns (`atob()`, suspicious base64, hex escapes, hardcoded `API_KEY`/`SECRET_KEY`/`PASSWORD`), and proper directory structure [^src4]. The ecosystem is large: asm's catalog indexes 2,800+ skills, including Anthropic's official skills (95,957★), superpowers (89,816★), and everything-claude-code (81,392★) [^src4]. (everything-claude-code is the harness system covered in [[ai-engineering/agent-harness|Agent Harness]].)

**Where to find/learn skills**: the official Anthropic marketplace via `/plugin marketplace add anthropics/skills` (pre-installed in claude.ai), plus `skill-creator` — "a skill... that creates skills" following Anthropic's formatting/packaging best practices [^src2]. The recommended single learning resource is Anthropic's "Agent Skills" Deep Learning course [^src2].

## What a skill *is* — workflow, not reference (Process over prose)

A fifth source (Addy Osmani's `agent-skills`, 27K★) sharpens the definition: a skill is **"a markdown file with frontmatter that gets injected into the agent's context when the situation calls for it"** — "somewhere between a system-prompt fragment and a runbook" [^src5]. The load-bearing distinction is **workflow vs reference**: a skill is *not* "everything you should know about testing"; it is "a sequence of steps the agent follows, with checkpoints that produce evidence, ending in a defined exit criterion" [^src5].

> "If you put a 2,000-word essay on testing best practices into the agent's context, the agent reads it, generates plausible-looking text, and skips the actual testing. If you put a workflow there... the agent has something to do, and you have something to verify." [^src5]

This is the same failure that makes "AI rules" repos do nothing in practice: **the rules are essays** [^src5]. Process over prose, workflows over reference, steps-with-exit-criteria over essays-without-them [^src5].

## Skills as encoded SDLC

Osmani's library organizes ~20 skills around six lifecycle phases with slash-command entry points — Define (`/spec`), Plan (`/plan`), Build (`/build`), Verify (`/test`), Review (`/review`), Ship (`/ship`), plus `/code-simplify` across the bottom [^src5]. The claim: this is the **same SDLC every functioning org runs** (Google's design-doc → review → implementation → readability-review → launch-checklist; Amazon's working-backwards memo and bar raiser) — and the thing agents skip by default [^src5]. The router (`using-agent-skills`) activates only the skills the task's actual scope needs: ~3 for a bug fix, ~11 for a complex feature [^src5].

### The five load-bearing principles [^src5]

1. **Process over prose** — workflows are agent-actionable; essays are not.
2. **Anti-rationalization tables** (the most distinctive decision) — each skill ships a table of excuses paired with pre-written rebuttals, because *"LLMs are excellent at rationalisation"* and will produce a plausible paragraph explaining why this task doesn't need a spec/test/review. E.g. "I'll write tests later." → "Later is the load-bearing word. There is no later." The pattern works for human teams too: "Anti-rationalization tables are pre-written rebuttals to lies the agent hasn't yet told" [^src5].
3. **Verification is non-negotiable** — every skill terminates in concrete evidence (tests pass, clean build, runtime trace, reviewer sign-off); "seems right" never closes the loop. Same principle as [[ai-engineering/agent-testing|Agent Testing]].
4. **Progressive disclosure** — don't load all 20 skills at start; the router loads what's relevant ("a twenty-skill library into a 5K-token slot without poisoning the well") [^src5].
5. **Scope discipline** — *"touch only what you're asked to touch."* Named "the single biggest determinant of whether an agent's PR is mergeable" [^src5].

The "Google DNA": individual skills encode published practices — Hyrum's Law (api-and-interface-design), the test pyramid + Beyoncé Rule + DAMP-over-DRY (TDD), ~100-line PR sizing with Critical/Nit/Optional/FYI labels (code review), Chesterton's Fence (simplification), trunk-based development, Shift Left + feature flags [^src5]. The point: "a frontier model has read the phrase 'Hyrum's Law'... but it does not apply Hyrum's Law when it's designing your API at 3am" [^src5]. Skills matter **more for long-running agents** — a skipped test in a 30-hour run becomes "a debugging archaeology project at the end" [^src5]. The portable `SKILL.md` format is the payoff: write the workflow once, any harness (Claude Code, Cursor rules, Gemini CLI, Codex) enforces it [^src5].

## Pairwise skills: knowledge + unbook (analytics pattern)

Anthropic's internal analytics stack demonstrates a pattern applicable to any domain-intensive skill design: two complementary skills per domain rather than one monolithic skill [^src6]:

- **Knowledge skill** — a thin router that loads domain-specific reference files (tables, columns, joins, gotchas) on demand. It "narrows the space to a few dozen curated files before a query is ever written" rather than exposing the full search space [^src6]. Without this router, Claude Code analytics accuracy was below 21%; with pairwise skills it consistently exceeded 95% in aggregate [^src6].
- **Unbook skill** — encodes the *procedure* a senior analyst would follow: clarify the question → find sources via the knowledge skill → execute → loop results through adversarial review sub-agents. It bundles reusable analysis patterns (retention curves, rate decomposition, funnel analysis) so common requests don't get reinvented [^src6].

The distinction is *declarative knowledge* (what a metric means) vs *procedural knowledge* (which sources to consult in what order, how to navigate ambiguity, what a finished analysis looks like) [^src6]. Reference docs within the knowledge skill should describe tables (grain, scope, exclusions), mechanics of gotchas, and explicit routing triggers ("IF the question is about experiment lift… DO NOT use for raw event counts") — without prescriptive recipes that go stale [^src6].

**Skill maintenance is an engineering problem.** Anthropic watched offline analytics accuracy drift from ~95% at launch to ~65% over a month before colocating skill markdown files in the same repo as transformation models — so the PR that changes a model also updates the skill describing it. A code-review hook flags any reporting-model change that doesn't touch a skill file; ~90% of data-model PRs now include a skill change in the same diff [^src6].

## Skills as compounding knowledge (the compound loop)

The **Compound Knowledge** pattern (EveryInc) treats skills as a vehicle for knowledge that accumulates across sessions rather than being rediscovered each time [^src7]:

```
/kw:brainstorm   →  Brain dump, pull references, find the shape
/kw:plan         →  Structure into actionable plan (searches past learnings)
/kw:confidence   →  Gut-check what you know vs. don't
/kw:review       →  Two parallel reviewers: strategic alignment + data accuracy
/kw:work         →  Execute plan, log what was done
/kw:compound     →  Save 1–3 learnings; check for stale knowledge it contradicts
```

`/kw:compound` saves learnings to `docs/knowledge/` as plain markdown with YAML frontmatter (type, tags, confidence, created, source). `/kw:plan` searches that directory automatically — past insights surface next time [^src7]. The feedback loop: each cycle makes the next faster because the plan starts with accumulated context. Knowledge files are git-tracked and greppable [^src7].

The `/kw:review` skill runs two reviewers **in parallel**: one checks strategic alignment (Is the goal clear? Is the hypothesis falsifiable?), one checks data accuracy (Are numbers sourced? Are baselines explicit? Is data fresh?). Findings are merged and grouped by priority (P1 blocks shipping / P2 should fix / P3 nice to have) [^src7].

## Skills as structured prompt templates (command libraries)

A simpler pattern than the full skill SDLC: a library of prompt templates stored in `.claude/commands/` that Claude uses as slash commands or copied directly [^src8]. EveryInc's `claude_commands` demonstrates five templates covering the most common software engineering workflows [^src8]:

| Command | Purpose |
|---|---|
| Experiment-driven development | Learn-from-failure loop; tracks attempts with success/failure logs |
| Generate codebase context | Creates `llms.txt`-style docs with file purposes, function signatures, architecture diagrams |
| Analyze GitHub issue | Reviews issue → examines codebase → creates implementation plan before coding |
| Create GitHub issue | Generates structured issues with MINIMAL / MORE / A LOT detail levels based on complexity |
| Address PR feedback | Parallel processing of independent changes; priority classification; resolution tracking |

Templates include clear objectives, step-by-step processes, decision criteria, and output formats [^src8]. The project-specific versions live in `.claude/commands/`; generic versions can be shared across teams [^src8].

## Nine skill categories (Anthropic internal catalog)

After cataloguing hundreds of internal skills at Anthropic, the Claude Code team found they cluster into nine categories. "The best skills fit cleanly into one; the ones that try to do too much straddle several and confuse the agent" [^src10].

| Category | What it does | Examples |
|---|---|---|
| **1. Library & API reference** | How to correctly use internal/external libraries; edge cases, footguns | `billing-lib`, `internal-platform-cli`, `sandbox-proxy` |
| **2. Product verification** | Test/verify code is working; often uses Playwright, tmux, programmatic assertions | `signup-flow-driver`, `checkout-verifier`, `tmux-cli-driver` |
| **3. Data fetching & analysis** | Connect to data/monitoring stacks; credentials, dashboard IDs, common query patterns | `funnel-query`, `cohort-compare`, `grafana`, `datadog` |
| **4. Business process & team automation** | Automate repetitive workflows into one command; log previous results for consistency | `standup-post`, `create-<ticket>-ticket`, `weekly-recap` |
| **5. Code scaffolding & templates** | Generate framework boilerplates; especially useful when scaffolding has NL requirements | `new-<framework>-workflow`, `new-migration`, `create-app` |
| **6. Code quality & review** | Enforce quality/review standards; run deterministically via hooks or GitHub Actions | `adversarial-review`, `code-style`, `testing-practices` |
| **7. CI/CD & deployment** | Fetch, push, deploy code; often references other skills | `babysit-pr`, `deploy-<service>`, `cherry-pick-prod` |
| **8. Runbooks** | Symptom-driven investigation → structured report; maps symptoms to tools to query patterns | `<service>-debugging`, `oncall-runner`, `log-correlator` |
| **9. Infrastructure operations** | Routine maintenance/operational procedures with guardrails for destructive actions | `<resource>-orphans`, `dependency-management`, `cost-investigation` |

> **Verification skills have had the most measurable impact on Claude's output quality internally.** "It can be worth having an engineer spend a week just making your verification skills excellent" [^src10]. Techniques: have Claude record a video of its output, enforce programmatic assertions on state at each step.

## Best practices for writing skills (Anthropic lessons)

**Don't state the obvious.** Claude already knows how to code and can read your codebase. A skill that restates what Claude would do by default "adds context without adding value." Focus on information that pushes Claude out of its normal way of thinking [^src10].

**Build a gotchas section.** "The highest-signal content in any skill is the Gotchas section." Build it from common failure points over time [^src10]:
> "The `subscriptions` table is append-only. The row you want is the one with the highest version, not the most recent `created_at`." "This field is called `@request_id` in the API gateway and `trace_id` in the billing service. They're the same value."

**Use the file system and progressive disclosure.** A skill is a folder, not just a markdown file: split detailed content into `references/api.md`, store template files in `assets/`, add scripts in `scripts/`. Tell Claude what files exist and it will read them at appropriate times [^src10].

**Avoid railroading.** Give Claude the information it needs with flexibility to adapt to the situation — skills are highly reusable, so overly specific instructions create brittleness [^src10].

**Think through setup.** If a skill needs user-configured parameters (e.g. a Slack channel), store configuration in `config.json` in the skill directory. If the config isn't set up, the agent asks the user. Use the `AskUserQuestion` tool for structured multiple-choice questions [^src10].

**Write descriptions for the model, not for humans.** When Claude Code starts a session, it scans a listing of skills with their descriptions to decide when to invoke one. The `description` field is "not a summary, it's a description of *when* to trigger this skill." Include triggers [^src10].

**Help Claude remember.** Some skills can include memory by storing data within them — an append-only text log, JSON files, or SQLite. Example: a `standup-post` skill that keeps `standups.log` with every past post it's written [^src10].

**Store scripts and generate code.** Giving Claude scripts and libraries lets it spend turns on composition (what to do next) rather than reconstructing boilerplate. A `data-science` skill with a library of fetch-data helper functions lets Claude compose advanced analysis on the fly [^src10].

**Use on-demand hooks.** Skills can include hooks that only activate when the skill is called and last for the duration of the session. Examples: `/careful` blocks destructive commands when touching prod; `/freeze` blocks edits outside a specific directory during debugging [^src10].

## Skill distribution: repos vs plugin marketplace

Two distribution paths [^src10]:
- **Check into repo** (`./.claude/skills`): works well for smaller teams with few repos; every checked-in skill adds to the model's context.
- **Plugin marketplace**: as the team scales, a marketplace lets engineers choose which skills to install and includes a setup flow. Anthropic's internal approach: anyone with a skill that gains traction can PR it into the marketplace — no centralized gatekeeping, organic curation [^src10].

Skills compose without native dependency management: reference another skill by name and the model invokes it if installed [^src10]. Measure skill usage with a `PreToolUse` hook that logs invocations, to find popular skills or ones that are under-triggering [^src10].

## Domain skill example: Charlie CFO

`charlie-cfo-skill` (EveryInc) is a concrete example of a domain-specific skill that activates on financial questions for bootstrapped startups [^src9]. It provides financial frameworks — cash management, unit economics, capital allocation, working capital, forecasting — and names after Charlie Munger's capital discipline principle [^src9]. The skill activates automatically on natural-language financial questions ("Should we make this hire?", "How much runway do we need?") and ships with `references/` docs for metrics benchmarks and case studies (Mailchimp, Zapier, Basecamp) [^src9]. Install: `npx skills add EveryInc/charlie-cfo-skill` [^src9].

This pattern — a domain skill bundling both a system prompt and reference docs, triggered by question type — is the production form of the pairwise knowledge/procedure skill design described above.

## See also

- [[ai-engineering/context-window-management|Context Window Management]] — why a lean window matters; sub-agents
- [[ai-engineering/context-engineering|Context Engineering]] — "less is more"; supply unique workflow, not general knowledge
- [[ai-engineering/ai-agent|AI Agent]] — token-predictor mental model; agents as new employees
- [[ai-engineering/multi-agent-systems|Multi-Agent Systems]] — scaling from one agent to sub-agents *for productivity*
- [[ai-engineering/agent-harness|Agent Harness]] — skills as a harness context technique; everything-claude-code
- [[ai-engineering/agentic-coding|Agentic Coding]] — skills as "the unit of reusable expertise"
- [[ai-engineering/mcp|MCP]] — skills tell the agent *how/when* to use MCP tools
- [[ai-engineering/rag|RAG]] — combine skills with RAG/MCP on demand
- [[ai-engineering/sources/how-ai-agents-and-skills-work|Source: How AI agents & Claude skills work]]
- [[ai-engineering/sources/internal-operating-system-claude-projects|Source: 4 Claude Projects / Internal OS]] — skills as reusable processes (`ask-the-board`, `ingest-resource`, `/improve-system`)
- [[ai-engineering/README|AI Engineering hub]]

---

[^src1]: [How AI agents & Claude skills work (Clearly Explained)](<../../raw/youtube/How AI agents & Claude skills work (Clearly Explained).md>) — Greg Isenberg × Ras Mic, YouTube
[^src2]: [What's the real deal about SKILLs (This is not a 'MCP is dead' post)](../../raw/web/what-s-the-real-deal-about-skills-this-is-not-a-mcp-is-dead.md) — Alejandro Aboy, The Pipe and the Line
[^src3]: [agent-skills: a central, version-controlled home for coding agent skills](../../raw/web/github-zazencodes-agent-skills-a-central-version-controlled.md) — zazencodes/agent-skills, GitHub
[^src4]: [agent-skill-manager (asm): the universal skill manager for AI coding agents](../../raw/web/github-luongnv89-asm-the-universal-skill-manager-for-ai-codi.md) — luongnv89/asm, GitHub
[^src5]: [Agent Skills](../../raw/web/agent-skills.md) — Addy Osmani, addyosmani.com (github.com/addyosmani/agent-skills)
[^src6]: [How Anthropic enables self-service data analytics with Claude](../../raw/notes/notes-clippings-how-anthropic-enables-self-service-data-analytics-with-claud.md) — Anthropic Data Science & Data Engineering team
[^src7]: [EveryInc/compound-knowledge-plugin — AI-powered workflows for knowledge work](../../raw/notes/notes-clippings-everyinccompound-knowledge-plugin-ai-powered-workflows-for-k.md) — EveryInc, GitHub
[^src8]: [EveryInc/claude_commands — Our favorite Claude Code commands](../../raw/notes/notes-clippings-everyincclaude-commands-our-favorite-claude-code-commands.md) — EveryInc, GitHub
[^src9]: [EveryInc/charlie-cfo-skill — Claude Code skill for bootstrapped CFO financial management](../../raw/notes/notes-clippings-everyinccharlie-cfo-skill-claude-code-skill-for-bootstrapped.md) — EveryInc, GitHub
[^src10]: [Lessons from building Claude Code: How we use skills](../../raw/notes/notes-clippings-lessons-from-building-claude-code-how-we-use-skills.md) — Thariq Shihipar, Anthropic

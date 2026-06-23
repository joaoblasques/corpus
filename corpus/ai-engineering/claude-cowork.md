---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/web/cowork.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/cowork-0dd4601a.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-04-10-cowork.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/web/the-claude-cowork-stack-marketing-against-the-grain.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-05-19-top-5-claude-cowork-tips-i-wish-i-knew-from-day-one.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-06-10-stop-using-your-own-claude-at-work.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/web/cowork-toolkit-the-essential-starter-kit-for-claude-cowork.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-04-30-day-1-welcome-to-the-cowork-toolkit-lets-dive-in.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-05-01-day-2-teach-cowork-how-you-actually-write.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-05-02-day-3-build-your-first-cowork-workstation.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-05-05-day-6-how-to-scale-your-cowork-to-run-your-entire-life.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/web/shared-cowork-toolkit-templates-d1.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/shared-cowork-toolkit-templates-d2.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/shared-cowork-toolkit-templates-d6.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-06-09-post-call-admin-done-in-one-click.md
    channel: email
    ingested_at: 2026-06-15
  - path: raw/email/email-2026-05-06-day-7-you-built-the-foundation-here-s-the-shortcut-to-the-re.md
    channel: email
    ingested_at: 2026-06-17
  - path: raw/notes/notes-clippings-best-practices-for-getting-started-with-claude-cowork.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-clippings-deploying-claude-across-the-enterprise-with-claude-cowork.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-clippings-deploying-claude-across-the-enterprise-with-claude-cowork-1.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-clippings-collaborate-with-claude-across-excel-powerpoint-word-and-out.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-clippings-claude-for-the-legal-industry.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-clippings-building-ai-agents-for-the-enterprise.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-clippings-get-started-with-claude-cowork.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/web/web-claude-cowork-anthropics-agentic-ai-for-knowledge-work.md
    channel: web
    ingested_at: 2026-06-23
  - path: raw/youtube/youtube-IevmGCVo9Pw-create-your-own-personal-claude-ai-system-that-makes-your-wo.md
    channel: youtube
    ingested_at: 2026-06-23
aliases:
  - Claude Cowork
  - Cowork
  - claude-cowork
  - Cowork OS
tags:
  - corpus/ai-engineering
  - entity
created: 2026-06-12
updated: 2026-06-17
---

# Claude Cowork

**TL;DR.** Claude Cowork is the desktop-app product for non-developers — described as "the non-developer version of Claude Code" [^src8]. New Anthropic capabilities land in [[ai-engineering/claude-code|Claude Code]] first and the best ones trickle down to Cowork over time [^src8]. It works against a **workspace folder** on your computer: each session starts by reading instruction and memory files (`CLAUDE.md`, `MEMORY.md`) plus an ABOUT-ME profile, so you never re-explain who you are [^src1][^src8]. The discipline that makes it powerful is **context economy** — keeping the always-loaded files lean so the context window is spent on the task, not the profile [^src1].

Access: download the desktop app at claude.com/download, open the **Cowork** tab (between Chat and Code), and select a folder as your workspace [^src1]. Three modes of Claude: **Chat** (ask/answer, won't read local files or take unrequested actions), **Code** (developers), **Cowork** (non-developers, file-aware, takes actions) [^src8].

## Workspace folder setup

Two competing folder conventions appear in the sources; both rest on the same principle (a lean, always-read profile + on-demand reference files).

**Ruben Hassid's ABOUT-ME pattern** [^src1]. A `Claude Cowork` folder with three subfolders:
- **ABOUT ME/** — the only folder Cowork reads automatically. Three core files: `about-me` (who you are, how you think, how you want Claude to write), `anti-ai-writing-style` (the words/patterns you hate, as rules), `my-company` (goals, strategy, what you're saying no to) [^src1].
- **OUTPUTS/** — one subfolder per project; Cowork never reads it on its own, saving tokens [^src1].
- **TEMPLATES/** — Cowork saves the skeleton of work you liked ("keeps the structure, strips the content") to reuse later [^src1].

**Global Instructions** (Settings → Cowork) tell Cowork to read every ABOUT ME/ file before every task and never touch OUTPUTS/ or TEMPLATES/ unless pointed at a file [^src1]. The key constraint: if ABOUT ME files stay small (under ~6,000 tokens total) Cowork reads them completely every session; if too big, it "starts summarizing them loosely instead of reading them carefully" [^src1].

**Jeff Su's "Cowork OS" pattern** (used by the Toolkit below) [^src9]. A flat workspace folder with `CLAUDE.md` + `MEMORY.md` at the root and a `00_Resources/` folder for reference files [^src9][^src10]. Critical detail: the root file **must** be named exactly `CLAUDE.md` (case-sensitive) or Cowork won't recognize it [^src9].

## CLAUDE.md vs MEMORY.md — the core distinction

Both files load every session and both are plain-text markdown [^src9]:

- **CLAUDE.md is prescriptive — what to DO.** Rules and standing instructions: "always X", "never Y", "when I ask about Z, do it this way" [^src9].
- **MEMORY.md is descriptive — what to KNOW.** Accumulated facts: active projects, decisions, contacts, preferences [^src9].

The test for where an entry belongs: if it contains "always"/"never" it's a CLAUDE.md rule; if it states a fact that could change tomorrow it goes in MEMORY.md [^src11]. Misfiling degrades output quality [^src11]. Over time this accumulation is "the difference between a tool that does what you say and an assistant that knows what you mean" — after 90 sessions you have 90 contextual facts applied automatically [^src11].

## The voice problem and reference files

To stop Cowork sounding like AI, create a `voice-principles.md` in `00_Resources/` capturing tone, sentence style, and words to avoid, and add a CLAUDE.md pointer: "Before producing any written content, read voice-principles.md" [^src12]. A **voice-extraction prompt** has Cowork analyze your last 30 sent emails (or pasted samples) and rewrite the file in your patterns [^src12].

This is the **reference-file pattern**: instead of putting everything in CLAUDE.md, create a separate file and point to it. Three reasons — size (keep CLAUDE.md under ~300 lines), modularity (different contexts load different files), maintainability (edit once, propagates) [^src12]. Rule of thumb: a long CLAUDE.md is a signal to pull content into a reference file and replace it with a one-line pointer [^src12].

## Token / credit economy

Cowork bills tokens, not messages, and re-reads the full conversation history on every turn — so "Message 30 costs 31x more tokens than message 1" [^src1]. Hacks [^src1]:
1. **Restart the conversation from an earlier message** rather than sending a follow-up.
2. **Start a fresh session every ~20 messages**; one developer found 98.5% of tokens went to re-reading history, only 1.5% to output [^src1].
3. **Batch tasks into one message** (one context reload, not three).
4. **Use Sonnet/Haiku for quick tasks**, reserve Opus + extended thinking for deep work [^src1].
5. **Keep ABOUT ME files small** [^src1].

Trimming the root CLAUDE.md from 600+ lines to ~250 dropped one user's token usage by roughly 25% [^src11]. See [[ai-engineering/context-window-management|Context Window Management]].

## Using personal Claude safely at work

Workers at 90%+ of companies use personal chatbots for work, often without telling IT; 57% have typed sensitive info at least once [^src6]. On personal plans, Anthropic may train on chats by default (consumer-terms change of August 2025), retained up to 5 years unless turned off — the opt-out applies going forward only [^src6]. Guidance: turn off training; never paste source code, customer/patient data, unreleased plans, financials, or credentials; anonymize before pasting; use a temporary chat for work tasks; and treat **connectors** as the most dangerous setting — a connected AI can be hijacked by content it reads (the "lethal trifecta": private-data access + untrusted content + outbound channel) [^src6]. Never connect work accounts to a personal AI; the clean answer for regulated data is a company-paid tool [^src6].

---

# Cowork Toolkit

A free email-course starter kit (Jeff Su / Cowork Academy) that builds a self-improving workspace [^src7]. It ships two pre-filled starter files (`CLAUDE.md`, `MEMORY.md`), a voice profile + extraction prompt, populate prompts for two workstations (Email HQ, Personal Finances), a first-project prompt, and a session-audit skill — tied together by routing logic and three-level inheritance [^src7]. (The shared Google-Drive template folders confirm the artifacts: `CLAUDE.md`/`MEMORY.md` [^src13], `voice-principles.md`/`voice-extraction-prompt.md` [^src14], `starter-session-audit.skill` [^src15].)

The course runs as a 7-day arc — Day 1 foundation files (`CLAUDE.md`/`MEMORY.md`), Day 2 voice principles, Day 3 Email HQ, Day 4 Personal Finances + routing, Day 5 first scoped project, Day 6 session audits — closing on Day 7 with a recap and the scaling vision: 15+ workstations (health, housing, product marketing, content) each accruing months of memory [^src17]. The framing is that after the toolkit "the gap isn't knowledge, it's time" — every structural concept is in place, what remains is accumulation [^src17].

## Workstations

**Workstations** are domain folders inside the workspace, one per area of work; each has its own CLAUDE.md (domain rules) and MEMORY.md (domain context) [^src10]. Root rules cascade down automatically, so voice principles and preferences flow into every workstation without repetition [^src10]. Two types: **universal** (cut across everything — email, brand identity) and **dedicated** (own one area — personal finances, health) [^src10].

A **populate prompt** creates the workstation and fills it from your real data. Example (Email HQ): connect Gmail, scan the last 4 weeks of sent mail, extract editorial rules (greeting, sign-off, formality by recipient), build a contacts CRM of the top 10 recipients, and add a routing entry — showing everything before saving [^src10]. The Gmail connector reads but does not send; you always review and hit send [^src10].

## The three scaling mechanisms

A 3-month-old workspace beats a 3-day-old one through three mechanisms [^src11]:
1. **Accumulating memory** — each correction (a sign-off, a banned phrase) gets written to the right MEMORY.md and never needs repeating.
2. **Routing** — a routing table in the root CLAUDE.md (one sentence per row) loads only the workstation needed for the task, so adding workstations doesn't slow every session. Resolving conflicts is part of building the table: the canonical edge case is whether a landlord email routes to Email HQ or to a Housing workstation [^src17].
3. **Session audits** — saying "audit this session" has Cowork scan for uncaptured learnings and propose where to save each (which file, which section, exact wording), with your approval. "Two actions… are what make the workspace self-improving instead of static" [^src11].

Memory discipline: 1–2 sentences per entry; a 150-line ceiling on root MEMORY.md (fix by compression/archiving, never raising the ceiling); and an `ARCHIVE.md` that is *not* read every session, so it has no size cost — the "filing cabinet" to MEMORY.md's "whiteboard" [^src11].

## Skills vs workstations

If the process requires your judgment along the way, it's a **workstation**; if you already know exactly what the output should be and just need execution, it's a **skill** [^src11]. See [[ai-engineering/agent-skills|Agent Skills]].

### Worked example: a post-call wrap-up skill

A concrete end-to-end skill build (≈30–45 min) shows the skill + connector pattern in practice [^src16]. The skill, `post-call-wrapup`, takes a meeting transcript and outputs four things: top-3 takeaways, action items with owner + due date, a client-facing follow-up email draft, and a standardized file name (`ClientName-YYYY-MM-DD`) [^src16]. It uses three built-in connectors — Google Drive (file the transcript), Notion (append takeaways/action items to the client's page under a dated heading), and Gmail (save the follow-up as a draft) [^src16].

Two patterns reinforce the rest of this page: the guardrail **"Never send. Always draft."** mirrors the Gmail-connector discipline (the connector reads and drafts but you hit send) [^src16][^src10], and **calibration-by-correction** — "whatever it got wrong, tell it once; by the second call it is calibrated to how you actually write" — is the same accumulating-memory mechanism that makes a workspace improve over time [^src16][^src11]. (An operator note in the same source records that **Claude Opus 4.8 became the default across Max, Team, and the API**, enabling scheduled multi-step agent workflows that run sub-agents hands-off [^src16].)

## Enterprise deployment (Anthropic's deployment guide)

Anthropic released a guide for deploying Cowork across a business function, with patterns drawn from Anthropic's own teams and customers including Thomson Reuters, Zapier, Jamf, L'Oréal, Lyft, and Rakuten [^src19][^src21].

**Five-level adoption maturity model** [^src19]:
1. Chat Q&A — individual, ad-hoc question-answering.
2. File-aware tasks — Cowork reads local files and connected apps to produce outputs.
3. Pilot use cases — structured pilots with a champion team; single-function deployments.
4. Department-wide workflows — recurring tasks, scheduled automation, shared workspace conventions.
5. Department-wide plugins — custom plugins encoding institutional knowledge, connecting proprietary systems.

**Six-month deployment framework** [^src19][^src21]:
- Months 1–2: identify champion teams and first use cases; run structured pilot evaluation.
- Months 3–4: expand to a second function; build shared CLAUDE.md / plugin templates.
- Months 5–6: org-wide rollout; plugin marketplace; embed into official processes.

**The "agentic thinking divide"** [^src21]: the enterprises pulling ahead are embedding agentic AI into how employees work, encoding institutional knowledge into systems that compound over time. The contrast: AI deployments that produce incremental gains that plateau vs. those that compound — the difference is whether you're building toward autonomous workflows or staying in a chat-prompt loop.

**Claude Cowork as the non-developer deployment vehicle:** the guide explicitly frames Cowork as the path for taking capabilities that previously required a custom build (long-running agents, multi-agent pipelines, MCP connectors) and making them available to "every team in your organization, without requiring a custom build for each one" [^src21].

## Claude for Microsoft 365

Claude integrates natively with Excel, PowerPoint, Word, and Outlook as add-ins deployed from Microsoft AppSource [^src20]:

- **Excel, PowerPoint, Word**: generally available to all paid plans (Mac and Windows). One AppSource listing covers all three.
- **Outlook**: public beta on all paid plans. Triages inbox (sorts by: needs response, can draft, noise), writes replies as drafts with recipients/subject/body filled in, checks attendee availability for calendar invites. Opens attachments in Word or Excel with full prior context carried over.
- **Cross-app context**: Claude moves between apps without re-explanation — triage an email in Outlook, open the attachment in Word, build the analysis in Excel, turn it into a deck in PowerPoint [^src20].

**Enterprise controls** [^src20]:
- **OpenTelemetry export** — configure a custom OTel collector to stream all prompts, tool calls, and document references to your security team's own infrastructure.
- **Analytics API** — breaks out activity per user, per app, per day.
- LLM gateway routing: traffic can route through an existing gateway to Claude models on Amazon Bedrock, Google Cloud Vertex AI, or Microsoft Foundry.
- Microsoft 365 Copilot customers can also access Claude models directly in Excel and PowerPoint.

## Legal vertical: Claude for the legal industry

Legal professionals became the most engaged Claude Cowork users of any knowledge-work function after Anthropic's first legal plugin release [^src22]. The legal stack uses:
- **20+ MCP connectors** to legal systems: contract lifecycle (Docusign, Ironclad, Definely), deal rooms (Box, Datasite), document management (iManage, NetDocuments), e-discovery (Consilio, Everlaw, Relativity), legal research (Thomson Reuters CoCounsel, Harvey, Midpage, Trellis), IP (Solve Intelligence) [^src22].
- **12 practice-area plugins** — each runs a setup interview that learns the team's playbook, escalation chain, and house style. Plugins include: Commercial Legal, Corporate Legal, Employment Legal, Privacy Legal, Product Legal, Regulatory Legal, AI Governance Legal, IP Legal, Litigation Legal, Law Student, Legal Clinic, Legal Builder Hub [^src22].
- **Claude Works in Microsoft apps**: context flows from Word redlines to Outlook cover notes to Excel checklists to PowerPoint board summaries without re-explanation [^src22].

A subset of practice-area plugins (Commercial Legal, Corporate Legal, Litigation Legal, Product Legal) are also available as cookbooks for deployment as [[ai-engineering/claude-managed-agents|Managed Agents]] via the Claude Platform [^src22].

## Official Cowork: architecture, Projects, and safety (Anthropic guide)

**Architecture.** Cowork uses the same agentic engine as Claude Code, running code and shell commands inside an isolated virtual machine (VM) on your computer; only files you explicitly connect are accessible; code execution is sandboxed [^src23]. When a task starts, Claude: (1) analyzes the request and creates a plan, (2) breaks complex work into subtasks, (3) runs code/shell commands in the isolated VM, (4) coordinates parallel workstreams when appropriate, (5) delivers outputs to your file system [^src23]. **Deletion protection**: Claude requires explicit permission before permanently deleting any files [^src23].

**Permission modes** [^src23]:
- **Ask before acting** — Claude pauses for approval of each action. Recommended when working with new tools, unfamiliar files, or anything you want to watch closely.
- **Act without asking** — Claude works without pausing. Faster but riskier; use only when actively supervising with trusted files and sites.

Both modes still prompt before permanent file deletion.

**Projects.** Group related tasks into persistent, self-contained workspaces with their own files, links, instructions, and memory [^src23]. Memory within Cowork is supported inside Projects but not retained across standalone sessions [^src23]. Projects make Cowork significantly more powerful for recurring or long-running work by preserving context between sessions.

**Scheduled tasks.** Type `/schedule` in any task to create recurring or on-demand automation. Scheduled tasks only run while the desktop app is open and the computer is awake [^src23]. (The Claude Code `claude --schedule` cron runs on Anthropic's cloud and does not require the local machine to be active — a key distinction.)

**Mobile access.** Pro and Max plan users can message Claude from their phone while the desktop app runs on their computer; Claude works using local files and connectors on the desktop, and the phone receives results in the same conversation [^src23]. Team/Enterprise require the desktop app on desktop.

**Network / compliance notes** [^src23]:
- Web search and web fetch run server-side and are not affected by network egress settings; admins can disable web search in Organization settings.
- Cowork activity is not captured in the Compliance API (as of 2026-06-17); Team/Enterprise admins can use OpenTelemetry (OTel) to monitor activity.

## Other guides

`claude101.com` collects free Cowork-adjacent guides (Cowork setup, Cowork + Projects, slides, skills, sounding like you, avoiding usage limits) [^src8].

## Anthropic's getting-started guidance

Austin Lau (Anthropic growth team) offers a first-party framework for when to reach for Cowork vs chat [^src18]:

**The core distinction**: "Claude Cowork is for when the output is something you'll hand to someone else" — a file someone opens, presents, or sends. Chat is for when the output is "a thought in your head" [^src18].

**Five ingredients of a Claude Cowork-shaped task** (you don't need all five, but good candidates hit a few) [^src18]:
1. More than one thing goes in — multiple files, a folder, a file plus connectors.
2. A file comes out — a doc, deck, spreadsheet, or CSV.
3. You'll do it again — recurring tasks are the sweet spot; one-offs are fine but repeatable work is where scheduling pays off.
4. You already know what good looks like — you can tell in 15 seconds whether the output is right, wrong, or 70% there.
5. The middle is the boring part — the thinking lives at the start and end; extract/compile/reconcile/reformat is what you hand off.

**First-session best practices** [^src18]:
1. Open the desktop app, switch to the Cowork tab.
2. Give Claude rich context — drop files, point at a folder, or connect an app. "The difference between a mediocre output and a great one is almost never your prompt, but whether you're providing enough rich context."
3. Describe the deliverable (outcome, not process).
4. Start with a real task you know well so you can immediately judge quality.
5. **Make Claude ask clarifying questions before starting**: include "Before we begin, repeat my ask back to me so we're aligned, then ask me as many clarifying questions as you have." This surfaces gaps upfront rather than mid-task; "answering five questions up front costs you 30 seconds. Finding those same gaps afterwards costs you time and tokens."

**Worked examples from practice** [^src18]: daily briefing on Slack + Gmail → short triage report (6 am cron); budget pacing dashboard pulling Google Ads + Meta Ads spend into a live HTML artifact; weekly Search Console reporting reconciled into a single sheet with templated callouts. All reduce the work to the judgment-only slices.

> "Many people don't know that Claude Cowork and Claude Code run on the same engine under the hood." [^src18] Cowork is Claude Code's harness adapted for non-technical knowledge work.

## See also

- [[ai-engineering/claude-code|Claude Code]] — the developer counterpart; capabilities land here first
- [[ai-engineering/anthropic|Anthropic]] — provider and model lineup
- [[ai-engineering/claude-managed-agents|Claude Managed Agents]] — some legal practice-area plugins deploy as Managed Agents
- [[ai-engineering/mcp|MCP]] — the protocol underlying Cowork's 20+ legal connectors and all external app integrations
- [[ai-engineering/context-window-management|Context Window Management]], [[ai-engineering/agent-skills|Agent Skills]]

[^src1]: [Cowork (Ruben Hassid)](../../raw/web/cowork.md)
[^src2]: [Cowork 2.0 (Ruben Hassid, dup)](../../raw/web/cowork-0dd4601a.md)
[^src3]: [Cowork (email pointer)](../../raw/email/email-2026-04-10-cowork.md)
[^src4]: [The Claude Cowork Stack — marketing against the grain](../../raw/web/the-claude-cowork-stack-marketing-against-the-grain.md)
[^src5]: [Top 5 Claude Cowork Tips I Wish I Knew from Day One](../../raw/email/email-2026-05-19-top-5-claude-cowork-tips-i-wish-i-knew-from-day-one.md)
[^src6]: [Stop using your own Claude at work](../../raw/email/email-2026-06-10-stop-using-your-own-claude-at-work.md)
[^src7]: [Cowork Toolkit — the essential starter kit](../../raw/web/cowork-toolkit-the-essential-starter-kit-for-claude-cowork.md)
[^src8]: [Claude 101](../../raw/web/claude-101.md)
[^src9]: [Day 1: Welcome to the Cowork Toolkit](../../raw/email/email-2026-04-30-day-1-welcome-to-the-cowork-toolkit-lets-dive-in.md)
[^src10]: [Day 3: Build your first Cowork workstation](../../raw/email/email-2026-05-02-day-3-build-your-first-cowork-workstation.md)
[^src11]: [Day 6: How to scale your Cowork to run your entire life](../../raw/email/email-2026-05-05-day-6-how-to-scale-your-cowork-to-run-your-entire-life.md)
[^src12]: [Day 2: Teach Cowork how you actually write](../../raw/email/email-2026-05-01-day-2-teach-cowork-how-you-actually-write.md)
[^src13]: [Cowork Toolkit templates — Day 1](../../raw/web/shared-cowork-toolkit-templates-d1.md)
[^src14]: [Cowork Toolkit templates — Day 2](../../raw/web/shared-cowork-toolkit-templates-d2.md)
[^src15]: [Cowork Toolkit templates — Day 6](../../raw/web/shared-cowork-toolkit-templates-d6.md)
[^src16]: [Post-call admin, done in one click (Return My Time)](../../raw/email/email-2026-06-09-post-call-admin-done-in-one-click.md)
[^src17]: [Day 7: You built the foundation. Here's the shortcut to the rest.](../../raw/email/email-2026-05-06-day-7-you-built-the-foundation-here-s-the-shortcut-to-the-re.md)
[^src18]: [Best practices for getting started with Claude Cowork](../../raw/notes/notes-clippings-best-practices-for-getting-started-with-claude-cowork.md) — Austin Lau, Anthropic growth team
[^src19]: [Deploying Claude across the enterprise with Claude Cowork](../../raw/notes/notes-clippings-deploying-claude-across-the-enterprise-with-claude-cowork.md) — Anthropic (guide announcement)
[^src20]: [Collaborate with Claude across Excel, PowerPoint, Word and Outlook](../../raw/notes/notes-clippings-collaborate-with-claude-across-excel-powerpoint-word-and-out.md) — Anthropic
[^src21]: [Building AI agents for the enterprise](../../raw/notes/notes-clippings-building-ai-agents-for-the-enterprise.md) — Anthropic (enterprise guide; same guide also at [^src19b]: [Deploying Claude across the enterprise with Claude Cowork (duplicate)](../../raw/notes/notes-clippings-deploying-claude-across-the-enterprise-with-claude-cowork-1.md))
[^src22]: [Claude for the legal industry](../../raw/notes/notes-clippings-claude-for-the-legal-industry.md) — Anthropic
[^src23]: [Get started with Claude Cowork](../../raw/notes/notes-clippings-get-started-with-claude-cowork.md) — Anthropic official guide

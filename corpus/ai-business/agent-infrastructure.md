---
type: concept
domain: ai-business
status: draft
sources:
  - path: raw/web/web-the-agent-stack-bet.md
    channel: web
    ingested_at: 2026-06-17
  - path: raw/web/web-we-need-to-talk-about-agents.md
    channel: web
    ingested_at: 2026-06-17
  - path: raw/web/web-clay-go-to-market-with-unique-dataand-the-ability-to-act-on.md
    channel: web
    ingested_at: 2026-06-25
aliases:
  - agent stack
  - production agents
  - agentic systems
  - agent identity
  - agent governance
  - enterprise agents
tags:
  - corpus/ai-business
  - concept
created: 2026-06-17
updated: 2026-06-25
---

# Agent Infrastructure

**TL;DR.** Two 2025–2026 sources converge on a shared diagnosis: most production agents are fragile (shared credentials, no persistent state, custom plumbing drowning engineering bandwidth), and the industry needs a principled stack: per-agent identity, universal context access, durable execution across sessions, and open platform primitives. A parallel VC essay warns that framing agents as "digital co-workers" is the wrong adoption metaphor — the real opportunity is re-architecting workflows to exploit new capabilities, not substituting agents for headcount.

## The current state: governance debt

"Peek under the hood of most 'production agents' shipping today and you won't find intelligence. You'll find custom plumbing, fragile session logic, shared service accounts, and a security model held together by hope" [^src1].

The core problem is **excessive agency**: autonomous systems given broad permissions operating at runtime without observability. They mark tasks "complete" while leaving corrupted state. The humans find out on Monday [^src1]. This is called **governance debt** — silent accumulation of security and audit risk that forces a full rewrite after the first incident.

## The four architectural bets

### 1. Agent identity at the platform layer

Today: agents borrow a service account or inherit a human's OAuth token and "promise" — in application code, in a prompt — to stay within bounds. "In a real enterprise environment, a promise in a prompt is not a policy" [^src1].

The bet: move agent identity from the application layer down into the platform. **Embedded** (not bolted-on) security means the agent has an unforgeable identity recognized at the network and platform level; policy is enforced at the source. "If the agent reaches for a database it isn't cleared for, the connection never opens" [^src1].

Done right, this turns "a fleet of liabilities into something that looks a lot more like a managed workforce: every action attributable, every permission auditable, every agent revocable with one call" [^src1].

### 2. Universal context, not scraped windows

Current state: teams burn large shares of engineering hours on custom serialization, bespoke session stores, and hand-rolled memory layers. The context agents can access is siloed — a browser agent sees the open tab; a desktop wrapper sees dragged-in files. Neither can reason across CRM, ERP, data warehouse, ticketing systems, and transcripts simultaneously [^src1].

The bet: platform-level context integration. Without it, "the ceiling of agentic AI is 'slightly better spreadsheet autocomplete'" [^src1].

### 3. Persistence beyond the session

"A session that survives a dropped WebSocket is table stakes. A mission that survives a quarter is the bar enterprises actually need" [^src1].

Real enterprise work doesn't fit in a session: a procurement workflow spans weeks, a compliance audit runs a month, an incident investigation outlives three on-call rotations. Most agents today hit a time or token ceiling — the mission fails, and a human reconstructs the thread from wherever the transcript ended [^src1].

Requirements for enterprise-grade persistence:
- State and checkpointing that survives restarts, disconnects, redeploys, and model version changes **by default**.
- Context that outlives the token window: long-horizon memory, summarization, and handoff between agent instances.
- Missions that outlive sessions: agents that stay on the job across days, credential rotations, with an auditable trail.
- First-class human-in-the-loop primitives: pause-and-ask instead of silently claiming authority [^src1].

### 4. Platforms, not bespoke plumbing

"The pattern I see most often in strong teams is the saddest one: brilliant engineers draining their bandwidth into stack problems that do not differentiate their product. Custom memory. Bespoke eval harnesses. Homegrown observability. Handwritten retry logic" [^src1].

The bet: open-primitive platforms (comparable to the cloud compute → containers → CI/CD maturation pattern). Teams prototype locally on open primitives and graduate to a managed platform without a rewrite. Engineering hours go to domain reasoning and business logic — the only part users actually pay for [^src1].

## The "agent" framing problem

Euclid VC argues that the term "agent" is actively harmful to adoption in vertical markets [^src2].

**The GM/Toyota analogy.** GM spent $40–45B in the 1980s on factory robots, placing them exactly where human workers had been. "Job roles stayed the same. The pace and sequence of the assembly line were unchanged." Result: robots sometimes painted each other, manufacturing costs increased. Toyota, with the same technology, asked "what becomes possible?" — redesigned plant layouts, reorganized work cells, moved humans to system oversight. By 1990 Toyota's profit per vehicle was 3× GM's [^src2].

**Why "agent" replicates GM's mistake.** When AI is cast as a co-worker, the unit of adoption becomes the *role* ("can we replace Sarah?"), not the *workflow* ("what can now happen that couldn't before?"). This produces local gains (headcount cuts) while leaving underlying structure untouched — the same failure mode as bolting a robot where a person stood [^src2].

**The "work not done" opportunity.** The more compelling frame for vertical AI: capturing work that *wasn't being done*: bids not submitted, calls not answered after hours, patients not seen. This is revenue expansion, not cost reduction — and it doesn't appear in headcount models [^src2].

Examples of correct framing:
- Abridge (healthcare): redesigned the documentation workflow so a patient conversation auto-becomes a structured clinical note. Physicians review/sign off. "86% less effort on documentation and 60% less after-hours work" [^src2].
- EvenUp (legal): automates demand drafting and medical chronology. "Drafting output tripled and average settlement timelines cut by a month, all without adding headcount" [^src2].
- BuildVision (construction): frees sales reps from PDF/phone-call back-and-forth to take on more complex, higher-margin jobs [^src2].

None of these lead with "agent." They lead with the workflow and the results.

**The moving boundary.** As AI handles reliable execution, human roles migrate to the frontier — where empathy overrides policy, where competing visions must be mediated, where the agent hits reliability limits. "Workers no longer define the workflow; they occupy the segments where agentic capabilities fail, get bottlenecked, or hit their limits" [^src2].

## Contradictions and tensions

**Tension:** The agent-stack piece frames better agent infrastructure as the path to unlocking agent potential [^src1]. The VC piece warns that selling "agents" at all is the wrong frame for enterprise buyers [^src2]. These are compatible: the infrastructure bets are a builder/platform concern; the framing critique is a go-to-market concern. Both agree the current state is brittle and that the right question is workflow re-architecture, not headcount substitution.

## Gotchas

- The agent-stack piece (Addy Osmani) appears to be associated with a platform or product in the agent orchestration space; the recommendations may be colored by commercial interest [^src1].
- Euclid VC is a venture investor backing Vertical AI founders; the "capabilities not agents" framing is also their investment thesis [^src2].

## Clay — GTM data + agent workflows

Clay (clay.com) is a go-to-market platform that exemplifies how AI agents integrate into commercial workflows [^src3]:

- Aggregates data from 150+ providers (lead enrichment, account scoring, intent signals, contact data).
- **Claygent** — an AI agent that can search public databases, navigate gated forms, and find unique data points; agents are versionable and reusable across workflows.
- **MCP integration**: Claygent connects to any MCP server (Salesforce, Gong, Google Docs) for deeper business context — a live example of the MCP-as-front-door architecture described in [Selling to AI Agents](/ai-business/selling-to-ai-agents.md).
- Sculptor: an AI chat interface for GTM idea generation, analysis, and table building.
- Anthropic uses Clay internally: "Clay has helped Anthropic significantly improve our lead enrichment and sales data pipelines. We've been able to consolidate our tech stack to core essentials, like our CRM, Clay, and email tool." [^src3]

Clay represents the "orchestrate and act on data at scale" layer — connecting enrichment, intent signals, and CRM data, then triggering outreach or CRM updates automatically. It is an example of the kind of "picks-and-shovels" infrastructure for AI-assisted GTM workflows that complements the solo-founder plays in this domain.

## Related

- [AI and the Job Market](/ai-business/ai-and-the-job-market.md) — the broader narrative on AI's economic impact; the Toyota/GM analogy is covered in depth there too.
- [Monetizing Code](/ai-business/monetizing-code.md) — building AI workflows as the monetization opportunity.
- [Navigating a Technical Career](/ai-business/technical-career.md) — human skills that compound alongside agents.
- [Selling to AI Agents](/ai-business/selling-to-ai-agents.md) — the commercial layer: how to build products that *sell to* AI agents, not just how to build them.

[^src1]: [The Agent Stack Bet](../../raw/web/web-the-agent-stack-bet.md)
[^src2]: [We Need to Talk About Agents](../../raw/web/web-we-need-to-talk-about-agents.md)
[^src3]: [Clay | Go to market with unique data](../../raw/web/web-clay-go-to-market-with-unique-dataand-the-ability-to-act-on.md)

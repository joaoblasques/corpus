---
type: concept
domain: ai-business
status: draft
sources:
  - path: raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-sell-your-api-to-report.md
    channel: notes
    ingested_at: 2026-06-25
aliases:
  - sell to AI agents
  - agentic commerce
  - agent economy
  - MCP front door
  - x402 micropayments
  - AEO answer engine optimization
  - word of machine
  - agent buying loop
  - API monetization agents
tags:
  - corpus/ai-business
  - concept
created: 2026-06-25
updated: 2026-06-25
---

# Selling to AI Agents

**TL;DR.** A new customer class is arriving — autonomous AI agents with wallets — and almost no one is building for them. Agents don't want persuasion, demos, or landing pages: they want clear capability, permission to use it, and trust signals. The infrastructure already exists (payments via ACP/AP2/x402, identity, tools via MCP); a solo founder's job is to assemble, not invent. The strategic plays are: (1) make your existing product agent-buyable, or (2) build picks-and-shovels for the agent economy. Price per call, not per seat. Win distribution via AEO (Answer Engine Optimization), not SEO [^src1].

## The new customer

"For the entire history of the internet, your customer was a human." Now an agent shows up with a wallet — "billions of customers, millions of wallets" — and "almost nobody is actually building to sell to AI agents just yet" [^src1].

People already have AI assistants that book dinners, compare vendors, file support tickets, and buy software. Businesses are spinning up agents for procurement, research, and sales. "The people thinking clearly about this believe that agent traffic will outnumber human traffic before long" [^src1].

Agents don't want persuasion, demos, social proof: "An agent just wants three things: clear capability of what you've built, permission to use it, and then enough trust signals to know it will not get burnt." They don't read your story, watch your videos, or browse. They read structure and call your endpoint. "If an agent can't understand what you do and act on it through code, you are invisible" [^src1].

## The agent buying loop

Five-step path: **Find** (reads documents and pricing, doesn't browse) → **Evaluate** (checks capabilities, limits, policies) → **Trust** (checks identity proof, compliance, safety) → **Transact** (pays, books, subscribes) → **Recommend** (tells other agents what worked) [^src1].

The "word of machine" loop: "It tells other agents what worked, and that word of machine loop will decide who wins" [^src1]. This agent-to-agent recommendation replaces human word-of-mouth as the decisive distribution channel.

## The three rails (assemble, don't invent)

The infrastructure exists. A solo founder's job is assembly [^src1]:

### Rail 1 — Payments
- **ACP (Agentic Commerce Protocol)** — OpenAI + Stripe; powers instant checkout inside ChatGPT. Etsy has it live; a million Shopify merchants are coming on. OpenAI takes ~4%.
- **AP2 (Agent Payments Protocol)** — Google + Coinbase; agents pay on behalf of a user with strict spending mandates.
- **x402 (Coinbase)** — the one to watch for solo founders: any API endpoint can charge a tiny fee in stablecoins, no login, no card required. An agent can hand you money in fractions of a cent, millions of times a day [^src1].

### Rail 2 — Identity / inboxes
Agents need their own inboxes to handle email-based workflows. AgentMail gives each agent its own inbox that sends, receives, creates threads, reads emails, and can sign up for services and pull verification codes — without a human clicking buttons [^src1]. (AgentMail is itself an example of selling to agents: Claude recommended it without any human research.)

### Rail 3 — Tools (MCP is the new front door)
"Instead of an agent trying to click around your website like a confused human, you expose an MCP server" — a clean menu of actions your software offers (search customers, create invoice, issue refund, update ticket). The agent reads the menu, picks the action, and calls it. "That menu is becoming the real front door of your business" [^src1]. Companies already doing this: Zerneo, Posties, Lead Magic.

## Two plays

### Play 1 — Make your existing product agent-buyable (defensive)

Three moves this week [^src1]:
1. **Expose an MCP server** — let agents do business with you through actions instead of your UI.
2. **Add discovery files** — create an `llms.txt` at your domain root: a short plain-text file telling AI systems what you do, your pricing, and your policies. Agent-readable by design. "A non-technical founder can write a good one in an hour with help from Claude or ChatGPT" [^src1].
3. **Plug into a checkout protocol** — ACP, x402, or AP2, depending on your model. An agent can now pay you without a human in the loop.

### Play 2 — Build picks-and-shovels for the agent economy (offensive)

**Idea 1 — Agent-ready-in-a-box for small businesses**: most local/small businesses have no idea agents are about to become shoppers. Take their website, generate the discovery file, the agent-readable pricing and policy page, and a simple MCP server exposing their core actions. Math: setup fee + $39–$99/month to keep current as agent standards evolve. Pitch: "Do not become invisible when agents start buying stuff" [^src1].

**Idea 2 — Single-capability paid tool** (purest form): pick one narrow, high-frequency capability — a verification check, niche data lookup, formatting job, YouTube transcription, background removal, research call — "anything an agent needs mid-task and would happily pay a fraction of a cent for rather than figuring it out itself." Wrap it, charge per call via x402. "You are not chasing 100 human subscribers. You're chasing one [agent] serving one capability that hits it thousands of times a day" [^src1].

Example: a YouTube transcription API — if an agent is building something that needs transcription, it searches the internet, finds your MCP/API, and uses it rather than trying to build its own tool. Agents find the fastest and cheapest way; your job is to be findable and cheap-per-call [^src1].

**Idea 3 — Agent support / procurement desk**: when an agent has a problem, where does it go? When a business agent needs to buy software, it needs clean vendor comparisons against policies. Either gap is a product: an agent support desk (AgentMail + checkout protocol) or a vendor comparison tool. Side benefit: affiliate steering — build directories that push agents toward certain tools and earn affiliate commissions [^src1].

## Pricing for a machine, not a person

"Humans buy seats and monthly plans. An agent does not want a seat." Agents make huge numbers of tiny calls and want to pay for exactly what they use [^src1].

- **Price per call, usage-based billing.**
- **Keep a generous free tier** — it matters more for agents than humans because it's how an agent discovers and trusts you first. The free tier is your discovery layer before the agent scales up usage [^src1].
- The math: "if a call costs you a fraction of a cent and you charge a small multiple, every call is margin. Machines generate calls at a scale humans never could" [^src1].

Example: one agent using a transcription API 50 times/day started on a free tier, scaled to paid as needs grew — with no human in the decision loop [^src1].

## AEO — Answer Engine Optimization (the new SEO)

"You can build the best agent tool in the world, but if no agent can find it, you have nothing" [^src1].

Old game: ranking on Google for human eyeballs. New game: getting cited, trusted, and recommended by AI systems [^src1].

Steps:
1. **Unblock AI crawlers** — many sites (especially those behind Cloudflare) block AI crawlers by default. Check that major AI crawlers can access your site.
2. **Add `llms.txt`** — see Play 1 above.
3. **Structure content for AI reading** — "Lead with a 50-word factual answer. That is the chunk an AI grabs and quotes." Write in clear factual statements; agents extract facts, not vibes and opinions. Add structured data labels (prices, policies, offerings) [^src1].
4. **Get listed where agents look** — public MCP registries, directories, and marketplaces "are being searched right this second by agents." The end game: "be the tool that agents recommend to other agents. It just snowballs" [^src1].

## The bigger picture

"The internet is splitting in two. There is the human internet we all grew up with, and now there is a new agentic internet being wired up right now." Agents are getting access to payments, identity, inboxes, and tools. "Almost no one is building for the second one yet" [^src1].

The opportunity framing: "You resist the urge to spend three months on a beautiful interface because your customer does not have eyes" [^src1].

## Relationship to other pages

- **[[ai-business/agent-infrastructure|Agent Infrastructure]]** — technical architecture of production agents (identity, context, persistence, platforms); this page is the *commercial* layer — how to sell to agents, not how to build them.
- **[[ai-business/monetizing-code|Monetizing Code]]** — the "picks-and-shovels" single-capability tool play is a direct extension of "sell a result, not code," applied to an agent customer instead of a human.
- **[[ai-business/boring-expert-businesses|Boring Expert Businesses]]** — the "make yourself agent-buyable" defensive play applies to any expert service business wanting to capture agent traffic.

[^src1]: [Sell Your API to AI Agents & Make SERIOUS Money in 2026](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-sell-your-api-to-report.md) — Oliver (Rosewell.dev / ex-Response AI); solo-founder framing, genuine operator context; video report from Obsidian vault

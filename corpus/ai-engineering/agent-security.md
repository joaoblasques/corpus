---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/email/email-2026-05-28-building-secure-ai-agents-from-prompt-injection-to-productio.md
    channel: inbox
    ingested_at: 2026-06-12
  - path: raw/web/secure-llms-how-to-prevent-prompt-injection.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/auth-md-open-protocol-for-agent-registration.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/i-built-a-vulnerable-app-and-spent-1-500-seeing-if-llms-coul.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/catch-security-issues-as-claude-writes-code-claude-code-docs.md
    channel: web
    ingested_at: 2026-06-15
  - path: raw/email/email-2026-06-08-how-openai-engineers-prompt.md
    channel: email
    ingested_at: 2026-06-15
  - path: raw/notes/notes-clippings-claude-security-is-now-in-public-beta.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-08-security-maintainability-and-reliability.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/web/web-mitigating-the-risk-of-prompt-injections-in-browser-use.md
    channel: web
    ingested_at: 2026-06-21
  - path: raw/web/web-project-glasswing-securing-critical-software-for-the-ai-era.md
    channel: web
    ingested_at: 2026-06-23
  - path: raw/web/web-trendaitm-and-anthropic-advance-ai-powered-vulnerability-det.md
    channel: web
    ingested_at: 2026-06-23
  - path: raw/web/web-sentinelone-unveils-wayfinder-frontier-ai-services-to-proact.md
    channel: web
    ingested_at: 2026-06-23
  - path: raw/web/web-crowdstrike-puts-claude-opus-4-7-to-work-across-falcon-and-q.md
    channel: web
    ingested_at: 2026-06-23
  - path: raw/web/web-enhancing-ai-driven-defense-with-anthropics-claude-opus-4-7.md
    channel: web
    ingested_at: 2026-06-24
  - path: raw/web/web-red-agent-and-claude-opus-securing-production-targets-at-sca.md
    channel: web
    ingested_at: 2026-06-24
  - path: raw/web/web-use-claude-cowork-safely-claude-help-center.md
    channel: web
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-P4rv9RSM1IE-claude-skills-everything-you-need-to-know-about-claude-skill.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-full-guide-build-report.md
    channel: notes
    ingested_at: 2026-06-25
  - path: raw/web/web-self-hosted-sandboxes.md
    channel: web
    ingested_at: 2026-06-25
  - path: raw/web/web-build-a-claude-managed-agent-with-vercel-sandbox-vercel-know.md
    channel: web
    ingested_at: 2026-06-25
  - path: raw/web/web-set-up-claude-managed-agents-cloudflare-sandbox-sdk-docs.md
    channel: web
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-M-NTwkM3VwM-local-ai-agents-in-26-minutes.md
    channel: youtube
    ingested_at: 2026-06-26
aliases:
  - prompt injection
  - LLM security
  - AI guardrails
  - agent hardening
  - auth.md
  - lockdown mode
  - security-guidance plugin
  - AI-generated code vulnerabilities
  - hard-coded secrets
  - dependency hallucination
  - package hallucination
  - overconfidence effect
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-12
updated: 2026-06-24
---

# Agent Security

**TL;DR**: Hardening LLM agents for production rests on defense in depth — no single control is reliable. Layer input validation (prompt-injection classifiers, sanitization, human-in-the-loop), guardrails (LLM-as-judge, PII masking, moderation), output control ([structured outputs](/ai-engineering/structured-outputs.md)), and architecture (least privilege, scoped tools, auth inheritance, observability) [^src1]. "Security is just good engineering applied to AI" [^src1]. Emerging protocols like auth.md extend this to agent identity and registration [^src3].

## Prompt injection

The "LLM equivalent of code injection" — the user manipulates the model into doing something it shouldn't; "think of it as SQL injection, but for natural language" [^src2]. Two forms [^src2]:
- **Direct injection** — the user writes text to override instructions, e.g. "Forget all your previous instructions."
- **Indirect injection** — malicious content hidden in external files, URLs, or images that a multimodal model processes (e.g. asking the model to read a file that contains the injection).

Root cause is structural: LLMs are trained to be helpful, and "at some point, ignoring their instructions is a way of being helpful" [^src2]. Real incidents cited: a Spanish supermarket (Alcampo) chatbot giving Python tutorials, and company bots revealing internal instructions [^src1][^src2].

### Prevention techniques

All are preventive — a gatekeeping layer before the LLM receives the request [^src2]:
- **Text classifiers** — a model labels the prompt INJECTION/safe with a 0–1 score (e.g. Hugging Face `deberta-v3-base-prompt-injection`); reject above a chosen tolerance and never forward to the LLM [^src2].
- **Guardrails (LLM-as-judge)** — one LLM in front of another decides if a request is in-scope, on-topic, and appropriate, outputting `allowed`/`not_allowed` [^src2].
- **Input sanitization** — strip malicious encoded characters, usually within XML or Markdown syntax, before the query reaches the LLM [^src2].
- **Few-shot prompting** — give the model examples of what attacks look like so it can recognize them [^src2].

## Defense in depth (four layers)

A production-ready agent should layer all four [^src1]:
1. **Input validation** — injection classifiers, input sanitization, custom pattern matching, human-in-the-loop.
2. **Guardrails** — topical scope guardrails, PII detection/masking, content moderation, LLM-as-judge appropriateness checks.
3. **Output control** — [structured outputs](/ai-engineering/structured-outputs.md) with Pydantic schemas, response-format enforcement, the Instructor library for automatic retries, output validation before downstream use.
4. **Architecture** — least-privilege database access, scoped tool permissions, authentication inheritance for multi-tenant apps, comprehensive logging/monitoring/observability, cloud content filtering.

The recommended learning sequence is reliability first (structured outputs) → understand the threat (injection) → secure design → hands-on guardrails → observability [^src1].

### Human-in-the-loop (HITL)

A code-driven guardrail that blocks execution if the user rejects an action, breaking the agent loop. Two types: **user permission** and **user input** [^src1]. Strongly recommended where destructive operations carry high impact — in testing, agents asked before destructive operations (e.g. DELETE endpoints) only "most of the time," frequently proceeding without asking [^src1]. (See [agent harness](/ai-engineering/agent-harness.md) guidance on confirming irreversible actions.)

### Key principles

- **Guardrails are not deterministic** — "They can fail to block something. This is part of real-world LLM security. Layer your defenses" [^src1].
- **Least privilege as a hard backstop** — "An agent can't drop your production table if it doesn't have DROP permissions" [^src1].
- **Log everything** — "You cannot debug what you didn't log"; the biggest challenge in AI projects is silent errors — agents attempting things they shouldn't, or hallucinating that an action succeeded [^src1].

## Production hardening at the harness level

Coding-agent harnesses add their own real-time security passes. Anthropic's `security-guidance` plugin reviews Claude's edits as they happen and sends vulnerabilities back for immediate fix: every file write triggers a scan, a model double-checks diffs at turn end, high-severity issues are fed back for fixing, and on git commit an agentic reviewer traces data flow to catch cross-file bugs like IDOR or cross-file SSRF [^src5]. (See [Claude Code](/ai-engineering/claude-code.md).) On the exfiltration side, ChatGPT's **Lockdown Mode** can't stop an injection from landing but "seals the exits," cutting the outbound requests attackers use to siphon data — at the cost of disabling agent mode, deep research, and downloads [^src6].

## Offensive use: agents as AppSec testers

The same agent capabilities that need hardening can be turned outward — pointing a coding agent at an app to *find* the vulnerabilities. One security researcher built a deliberately vulnerable book-review app (FastAPI backend, React Native/Expo Hermes-exported Android app) with a flag hidden in private reviews, then spent ~$1,500 running multiple LLMs as autonomous attackers to see if they could reproduce a real-world exploit class [^src4].

The planted bug: the API itself was hardened, but the app shipped a `google-services.json` exposing Firebase config, letting an attacker sign up directly against Firebase and read the Firestore DB — **Broken Access Control / Missing Object-Level Authorization**, which the author reports seeing "in the wild" on Firebase and Supabase apps with a hardened API but wide-open data layer [^src4].

### What it tells us about agents-as-attackers

- **It works, unevenly.** Of ten models given ten runs each, GPT-5.5 solved 7/10; Claude Sonnet 4.6 and Claude Opus 4.8 each 2/10; several models (Gemini, MiniMax, DeepSeek Flash) solved 0/10 [^src4]. Not a scientific eval, but a useful signal that capability varies widely.
- **The hard part is approach, not skill.** Failing runs typically fixated on the API/app surface and never pivoted to the real attack vector (Firebase) — or found Firebase but tried to use its credentials *against the API* instead of directly [^src4]. The author had to use harness extensions to "force models to keep trying" rather than report "API seems secure" [^src4].
- **Safety guardrails interfere with legitimate testing.** Some models gave immediate refusals (Gemini 3.1 Pro: ~9k median tokens/run vs 100k+ for engaged runs) [^src4]. Others showed "late refusals" — Claude Opus "got so close... but security guardrails ended the session early" [^src4]. An OpenAI account "already approved for security research" avoided refusals [^src4]. The same models also hesitated to act against a live DB: most "had momentary blips of 'This would affect the live database so I'm not going to do that'" [^src4].

**Defensive takeaway for builders**: a hardened API is not enough if the data layer (Firebase/Supabase) is directly reachable — the least-privilege and scoped-access principles above apply to the *backend-as-a-service* layer, not just your own endpoints. Assume an attacker can run a capable agent against your shipped client and any config it bundles.

## Vulnerability categories in AI-generated code

Ch8 catalogs the specific vulnerability classes AI coding assistants introduce most frequently [^src8]:

| Vulnerability | Mechanism in AI code |
|---|---|
| **Hard-coded secrets** | API keys, passwords, tokens embedded in source code; AI replicates patterns from training data where secrets were inline |
| **SQL injection** | String concatenation for queries rather than parameterized queries, especially when the AI is building CRUD scaffolding quickly |
| **Cross-site scripting (XSS)** | Inadequate output encoding in frontend code; AI produces working HTML but not necessarily safe HTML |
| **Improper authentication** | Missing auth checks on routes, especially in scaffolded backends; AI may not know which endpoints are sensitive |
| **Insecure defaults** | Debug mode left on, permissive CORS, missing rate limiting — "working" defaults that are not "secure" defaults |
| **Error-handling leakage** | Stack traces, file paths, internal state in error responses; AI error handling often exposes too much |
| **Dependency hallucination** | References to packages that don't exist or are typosquatted; malicious actors register hallucinated package names |
| **Package hallucination** | A distinct variant: AI invents plausible-sounding imports; if a malicious package of that name exists in the registry, it gets installed |

**Empirical scale**: 25–33% of GitHub Copilot-generated code has security weaknesses (2023 analysis); 40% of AI-generated code had potential vulnerabilities in a 2021 study [^src8]. These rates are higher than typical human-written code because AI optimizes for functional correctness, not security correctness.

The Snyk taint analysis hybrid approach addresses this: static taint tracking traces untrusted input through the codebase to sensitive sinks, then an AI layer interprets the taint paths to filter false positives [^src8].

## The overconfidence effect

A 2022 study found developers using AI coding assistants were *more* confident in their code's security even when it was objectively less secure than code written without AI [^src8]. The effect is compounding: AI-generated code may contain more vulnerabilities *and* the developer is less likely to subject it to security review. "Trust but verify" (Russian proverb invoked in ch8) is the corrective stance: trust the output enough to use it as a starting point, but verify before it ships [^src8]. See [Agent Testing](/ai-engineering/agent-testing.md) for the testing-side complement.

## Prompt injection in browser use

Every webpage a browser-use agent visits is "a potential vector for attack" [^src9]. Attack vectors include hidden text, manipulated images, and deceptive UI elements — all of which can carry payloads invisible to a human user but visible to a multimodal model examining a screenshot.

Anthropic's documented defense layers for browser agents [^src9]:

1. **RL training** — fine-tuning specifically on prompt-injection resistance; teaches the model to recognize and ignore injection attempts embedded in page content.
2. **Classifiers scanning untrusted content** — a separate classifier layer that labels external web content as untrusted before it enters the main model's context; injections in classified untrusted blocks are weighted accordingly.
3. **Red teaming** — continuous adversarial evaluation to find new injection patterns and update defenses.

The result: **Claude Opus 4.5 achieved ~1% attack success rate** in Anthropic's browser-use evaluations, "setting a new standard in robustness to prompt injections" [^src9]. This is a major reduction vs. undefended models.

**Claude for Chrome** expanded from research preview to general beta (Max plan) alongside these improvements [^src9] — the security work was a prerequisite for broader browser-agent deployment. The browser extension lets Claude operate real Chrome tabs as a computer-use agent with the above defenses active.

**Practical guidance for builders**: defensive architecture cannot rely solely on model training. Layer model-level defenses with:
- **Scope constraints in system prompts**: explicitly forbid the agent from following instructions sourced from external content.
- **HITL gates for sensitive actions**: require human confirmation before any action triggered by information from external web pages.
- **Least-privilege tool design**: the agent should not be able to exfiltrate data even if successfully injected.

See [Computer Use](/ai-engineering/computer-use.md) for implementation detail on browser-use configuration with Sonnet 4.6 (most robust for clicking tasks).

## Claude Security (enterprise vulnerability scanning product)

Claude Security (previously Claude Code Security) is Anthropic's enterprise-grade vulnerability-scanning product, available in public beta to Claude Enterprise customers as of mid-2026 [^src7]. It uses **Opus 4.7** to scan codebases the way a security researcher would — tracing data flows across files and modules, understanding component interactions — rather than searching for known patterns [^src7].

**Workflow** [^src7]:
1. Select a repository (or scope to a directory or branch) from the Claude.ai sidebar, then start a scan.
2. Claude produces findings with: confidence rating, severity, likely impact, reproduction steps, and instructions for a targeted patch.
3. Open the finding in Claude Code on the web to apply the fix in context.

**What enterprise users learned in preview** [^src7]:
- "Detection quality is paramount" — high-confidence findings are what accelerates security work; Claude Security's multi-stage validation pipeline reduces false positives before a finding reaches an analyst.
- "Time from scan to fix is the metric that matters" — several teams went from scan to applied patch in a single sitting instead of days of back-and-forth.
- Teams want ongoing coverage, not one-off audits → the product added **scheduled scans**.

**Additional features added at GA** [^src7]: target a scan at a specific directory; dismiss findings with documented reasons (so future reviewers trust prior triage); export findings as CSV or Markdown; send results to Slack, Jira, or other tools via webhooks.

**The broader supply-chain.** Technology partners embedding Opus 4.7 into their existing platforms: CrowdStrike, Microsoft Security, Palo Alto Networks, SentinelOne, TrendAI, and Wiz [^src7]. Services partners deploying Claude-integrated security solutions: Accenture, BCG, Deloitte, Infosys, PwC.

> "AI is compressing the timeline between vulnerability discovery and exploitation. We believe the right response is to make sure defenders have access to frontier capabilities." [^src7]

## Project Glasswing and security research partners (2026)

**Project Glasswing** (announced April 7 2026) is Anthropic's initiative to turn frontier AI into a tool for defenders. Using Mythos Preview in autonomous mode against real codebases, Anthropic found "thousands of 0-days" in widely-deployed critical software [^src10]. Key components [^src10]:
- **$100M in credits** — disbursed to the security research community for defensive use of frontier Claude models.
- **Cyber Verification Program** — vetting process that grants security researchers and companies expanded access to Claude for legitimate offensive security and vulnerability research.
- **Major tech coalition** — participating organizations across software, hardware, and cloud.

**TrendAI AESIR** — TrendAI's platform pairs Claude Opus 4.7 with their Vision One security platform to provide "Autonomous Enemy Simulation and Intelligence Response." AESIR uses Claude to research exploits at the depth of a human threat actor, providing prioritization and investigation alongside TrendAI's broader threat intelligence ecosystem [^src11].

**SentinelOne Wayfinder** — Frontier AI Services product integrating Claude Opus 4.7. "No single model will ever be the answer" — Wayfinder is designed as a multi-model foundation (best model for each specific task), combining Claude's reasoning with SentinelOne's threat data [^src12].

**CrowdStrike Falcon + Project QuiltWorks** — CrowdStrike embedded Opus 4.7 in two systems: Charlotte (Agentic SOAR with AgentWorks for multi-agent security workflows) and Project QuiltWorks (long-form code analysis and supply chain security) [^src13]. AgentWorks allows security teams to compose custom workflows using pre-built and custom security agents without writing code [^src13].

All three organizations joined the Cyber Verification Program for expanded model access tied to documented security research use cases [^src11][^src12][^src13].

### Palo Alto Networks Unit 42 / Frontier AI Defense

Palo Alto Networks' Unit 42 threat research group runs an AI-assisted defense platform under the **Frontier AI Defense** umbrella, powered by Claude Opus 4.7 [^src14]. Three core capabilities [^src14]:

- **AI-Driven Exposure Analysis**: traces complex exploit chains across multi-component environments that traditional scanning misses; maps attack paths from exposure to impact.
- **Scalable Application Analysis**: deep-stack code review — "reviews code at the level of understanding that a security engineer would", connecting architectural decisions to vulnerabilities.
- **Agentic Defense**: autonomous detection and remediation with human oversight; agents run threat response workflows with humans approving high-consequence actions.

Palo Alto Networks joined the Cyber Verification Program for expanded access to frontier Claude models tied to documented security research use cases [^src14].

### Wiz Red Agent

Wiz's **Red Agent** is an autonomous security agent scanning production environments at scale [^src15]. Operational metrics [^src15]:
- **150,000+ production web applications and APIs** scanned weekly
- **115 billion tokens** processed per week
- **3,000+ high and critical exploitable risks** found per week
- **0 false positives** — findings are confirmed as exploitable before surfacing

Red Agent uses **Claude Opus 4.6 and 4.7** as its reasoning engine, combined with the Wiz Security Graph for comprehensive context. "Logic flaws that traditional scanning structurally cannot see" — authentication bypasses, privilege escalation chains, multi-step business logic vulnerabilities — require frontier AI reasoning, not pattern-matching [^src15]. Available to Wiz ASM Advanced customers.

## Agent identity and registration (auth.md)

As agents act on behalf of users, identity becomes a security surface. **auth.md** is an open protocol (authored by WorkOS, not tied to its infrastructure) for agent registration without a sign-up form [^src3]. An app hosts a Markdown file at `https://yourapp.com/auth.md` declaring supported flows, scopes, and how to register [^src3]. Two flows [^src3]:
- **Agent verified** — agent-attested; the agent's identity provider vouches for the user, no human in the loop.
- **User claimed** — needs no provider; the agent shows the user a code, they sign in and confirm it.

It issues a scoped, short-lived, revocable access token over standard OAuth, composing existing standards (Protected Resource Metadata, ID-JAG identity assertions) so existing API auth is reused [^src3].

## Prompt injection risk model for agentic desktop apps

From Anthropic's official Cowork safety guide, the clearest practitioner framing of injection risk [^src16]:

**Two-condition requirement**: prompt injection requires *both* (1) Claude reads content from outside the user's trust boundary AND (2) Claude has write-capable tools available. Neither condition alone enables injection:

- Read-only sessions can't be exploited (no action capability)
- Sessions that never touch external content can't be injected (no attack surface)

**Tool risk classification** [^src16]:
- **Read tools** (Browse, Read File, Search): low risk — information exposure only; the injection must also gain write access to matter
- **Write tools** (Edit File, Bash, Send Email, Call API, Move to Trash): high risk — actions are often irreversible

**Safety hierarchy for agentic desktop use** [^src16]:
1. Use a dedicated working folder, not root or home directory
2. "Act without asking" mode is the highest-risk configuration — never enable for untrusted content sessions
3. Computer use sessions have no sandbox — treat them like granting full desktop control to a remote user
4. Scheduled/automated tasks have no human oversight — permission scope must be deliberately narrow

This framing generalizes beyond Cowork: any agentic system reading external content while holding broad write permissions follows the same two-condition injection model. The mitigation is to minimize the overlap: either scope reads to trusted sources or restrict write permissions — eliminating one condition eliminates the threat [^src16].

## Third-party skill security risk

**More than one in three public skills contain security flaws** [^src17]. The skills ecosystem shares the same supply-chain risk as npm/PyPI: anyone can publish a skill, installation is one click, and the security review burden is on the user.

Specific documented risk vectors [^src17]:
- **Prompt injection via skill instructions** — a skill's `SKILL.md` can contain adversarial text that alters the agent's behavior when the skill activates.
- **Excessive tool scope** — skills requesting broad filesystem or network access beyond their stated purpose.
- **Data exfiltration via skill callbacks** — skills that POST captured context to external endpoints.
- **Dependency confusion** — skills referencing external resources (images, scripts) from attacker-controlled domains.

**Mitigations** [^src17]:
1. Prefer Anthropic's official skill directory over community repositories.
2. Build critical workflow skills yourself — the 4th skill build method ("from conversation") makes this fast.
3. Read the full skill file before installing; look for unexplained network calls or broadly-scoped tool definitions.
4. Use sandboxed environments (separate Claude account / project) for evaluating unknown skills.

This connects to the MCP security surface (see [MCP](/ai-engineering/mcp.md)): both skill files and MCP server instructions can carry injections, and the same defensive instinct applies — read what you're loading before you load it.

## The lethal trifecta (AI second brain risk model)

Cole Medin's AI second brain guide introduces the **lethal trifecta** as the highest-risk configuration in agentic systems [^src17]:

> **Lethal trifecta** = private data access + untrusted content + exfiltration vector

When all three are present simultaneously — e.g. an agent with access to private emails/documents that also reads untrusted web content and has outbound HTTP tools — the risk of successful prompt injection leading to data exfiltration is at its maximum [^src17].

Mitigation pattern: never grant all three simultaneously. Strategies:
1. Separate agents by trust domain — a "reader" agent with private-data access has no web tools; a "searcher" agent has web access but no private-data access
2. Use the **zero-trust API model**: all external data is treated as untrusted; no untrusted content can instruct the agent to use output tools
3. Heartbeat monitoring: a separate supervisor agent periodically checks the primary agent's behavior for anomalies [^src17]

The lethal trifecta is a useful heuristic during design: sketch the agent's tool graph and ask whether any configuration simultaneously achieves all three elements. If yes, restructure.

## Self-hosted sandboxes (Managed Agents)

Anthropic's Managed Agents platform supports **self-hosted sandboxes** — running tool execution on the customer's own infrastructure rather than Anthropic's [^src18]. This directly addresses the lethal-trifecta problem: when private data never leaves the customer environment, the exfiltration surface shrinks dramatically.

Architecture [^src18]:
- **EnvironmentWorker** — the customer-side worker process that receives tool call requests via a polling connection and executes them locally
- **AgentToolContext** — the context object passed to each tool execution, carrying request metadata and session state
- **MCP tunnels** — an alternative path: instead of the polling model, expose the tool surface as an MCP server and connect it to the Managed Agent via a secure tunnel; the agent calls tools via standard MCP protocol

The self-hosted model means: the model (at Anthropic) decides what to do; the execution (tools, file writes, API calls) happens on the customer's infrastructure. Private data is accessed only from within the customer's trust boundary [^src18].

## Credential brokering at the firewall level

When agents handle per-customer credentials (API keys, OAuth tokens), passing them as environment variables inside the sandbox is insecure: any code in the sandbox can read them via `process.env`. Two documented patterns eliminate this attack surface [^src19][^src20]:

**Vercel Sandbox network policy** [^src19]:
- The credential is never set in the sandbox environment.
- A network policy on the sandbox intercepts outbound HTTP requests matching specific URL patterns (`/v1/sessions/<sessionId>/...`) and injects the `Authorization: Bearer <key>` header at the network layer.
- `console.log(process.env)` inside the sandbox shows no credential.
- Requests to non-matching URLs are rejected by default (deny-all firewall).

**Cloudflare egress policy** [^src20]:
- Per-session egress proxy injects credentials into outbound requests without the agent code ever receiving them.
- Custom proxy middleware can apply domain allowlists, log outbound calls, and block exfiltration paths.
- The control plane (Workers) configures the policy per session at the webhook stage.

**Why this matters for security**: the credential brokering pattern eliminates one limb of the lethal trifecta (§ above) — even if the agent is successfully prompt-injected and executes malicious code, the injected code cannot extract credentials by reading environment variables or process state. The credentials only exist on the network wire, scoped to specific endpoints.

## Local AI agent isolation model

For [local AI agents](/ai-engineering/local-ai-agents.md) — which run on your own machine and may touch your files, email, and the screen — safety is "the primary concern," because you are "giving this very intelligent agent access to your computer and hoping that it's not going to just go bananas" [^src21] [11:39](../../raw/youtube/youtube-M-NTwkM3VwM-local-ai-agents-in-26-minutes.md#t=11:39). Documented incidents include agents deleting a user's emails or carrying viruses introduced via shared skills [^src21]. The practitioner isolation model [^src21] [12:05](../../raw/youtube/youtube-M-NTwkM3VwM-local-ai-agents-in-26-minutes.md#t=12:05):

1. **Isolate the machine** — run local agents on a dedicated/wiped machine, never on the primary machine holding sensitive data.
2. **Scope access narrowly** — give it a *separate* email for screening, not the personal inbox with sensitive mail; grant only what each task needs.
3. **Don't trust foreign skills** — others' workflow/skill files can hide malicious instructions; avoid skills except from trusted developers, and when you do want one, "give the skill to Claude and tell it to scan the skill and then rewrite it itself" before installing. This is the local-agent version of the [don't-download-skills](/ai-engineering/agent-skills.md) rule.
4. **Scheduled security audits** — use the agent's own heartbeat to run a security audit hourly (or at minimum daily); frameworks like [OpenClaw](/ai-engineering/openclaw.md) expose dedicated security checks, and no-code [Claude Cowork](/ai-engineering/claude-cowork.md) pre-bakes many of these protections.

General rule of thumb from the source: "be as paranoid as possible" [^src21]. This is the personal-machine analogue of the [Managed Agents](/ai-engineering/claude-managed-agents.md) self-hosted-sandbox and credential-brokering patterns above — shrink the blast radius before granting write/action tools.

## See also

- [Structured Outputs](/ai-engineering/structured-outputs.md) — output-control layer; reliability prerequisite for security
- [Prompt Engineering](/ai-engineering/prompt-engineering.md) — injection is the adversarial inverse; few-shot defenses
- [Agent Harness](/ai-engineering/agent-harness.md) — where HITL and confirmation gates live
- [Claude Code](/ai-engineering/claude-code.md) — real-time security plugin reviewing agent edits
- [MCP](/ai-engineering/mcp.md) — tool-exposure surface; scoped permissions and OAuth apply
- [Claude Model Lineup](/ai-engineering/claude-models.md) — Opus 4.7 powers Claude Security's model-backed scans
- [Agent Testing](/ai-engineering/agent-testing.md) — the testing-side complement to security; overconfidence effect
- [Vibe Coding](/ai-engineering/vibe-coding.md) — the 70% problem; why AI code needs more security review, not less
- [Beyond Vibe Coding (Book)](/ai-engineering/sources/beyond-vibe-coding-book.md) — ch8 as primary source for vulnerability taxonomy

---

[^src1]: [Building Secure AI Agents: From Prompt Injection to Production Guardrails (email)](../../raw/email/email-2026-05-28-building-secure-ai-agents-from-prompt-injection-to-productio.md)
[^src2]: [Secure LLMs for Data Engineers: How to prevent Prompt Injection](../../raw/web/secure-llms-how-to-prevent-prompt-injection.md)
[^src3]: [auth.md — open protocol for agent registration](../../raw/web/auth-md-open-protocol-for-agent-registration.md)
[^src4]: [I built a vulnerable app and spent $1,500 seeing if LLMs could hack it](../../raw/web/i-built-a-vulnerable-app-and-spent-1-500-seeing-if-llms-coul.md) — Kasra
[^src5]: [Catch security issues as Claude writes code (Claude Code docs)](../../raw/web/catch-security-issues-as-claude-writes-code-claude-code-docs.md) — Anthropic, via [How OpenAI engineers prompt](../../raw/email/email-2026-06-08-how-openai-engineers-prompt.md)
[^src6]: [How OpenAI engineers prompt](../../raw/email/email-2026-06-08-how-openai-engineers-prompt.md) — The Code (on ChatGPT Lockdown Mode)
[^src7]: [Claude Security is now in public beta](../../raw/notes/notes-clippings-claude-security-is-now-in-public-beta.md) — Anthropic
[^src8]: [Ch8 — Security, Maintainability, and Reliability](../../raw/notes/notes-08-security-maintainability-and-reliability.md)
[^src9]: [Mitigating the Risk of Prompt Injections in Browser Use](../../raw/web/web-mitigating-the-risk-of-prompt-injections-in-browser-use.md) — Anthropic
[^src10]: [Project Glasswing: Securing Critical Software for the AI Era](../../raw/web/web-project-glasswing-securing-critical-software-for-the-ai-era.md) — Anthropic
[^src11]: [TrendAI and Anthropic Advance AI-Powered Vulnerability Detection](../../raw/web/web-trendaitm-and-anthropic-advance-ai-powered-vulnerability-det.md) — TrendAI
[^src12]: [SentinelOne Unveils Wayfinder Frontier AI Services](../../raw/web/web-sentinelone-unveils-wayfinder-frontier-ai-services-to-proact.md) — SentinelOne
[^src13]: [CrowdStrike Puts Claude Opus 4.7 to Work Across Falcon and QuiltWorks](../../raw/web/web-crowdstrike-puts-claude-opus-4-7-to-work-across-falcon-and-q.md) — CrowdStrike
[^src14]: [Enhancing AI-Driven Defense with Anthropic's Claude Opus 4.7](../../raw/web/web-enhancing-ai-driven-defense-with-anthropics-claude-opus-4-7.md) — Palo Alto Networks
[^src15]: [Wiz Red Agent and Claude Opus: Securing Production Targets at Scale](../../raw/web/web-red-agent-and-claude-opus-securing-production-targets-at-sca.md) — Wiz
[^src16]: [Use Claude Cowork safely — Claude Help Center](../../raw/web/web-use-claude-cowork-safely-claude-help-center.md) — Anthropic
[^src17]: [Full Guide: Build an AI Second Brain (Cole Medin)](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-full-guide-build-report.md) — Cole Medin, YouTube (processed report)
[^src18]: [Self-hosted sandboxes for Managed Agents](../../raw/web/web-self-hosted-sandboxes.md) — Anthropic
[^src19]: [Build a Claude Managed Agent with Vercel Sandbox](../../raw/web/web-build-a-claude-managed-agent-with-vercel-sandbox-vercel-know.md) — Vercel Knowledge Base
[^src20]: [Set up Claude Managed Agents · Cloudflare Sandbox SDK docs](../../raw/web/web-set-up-claude-managed-agents-cloudflare-sandbox-sdk-docs.md) — Cloudflare
[^src21]: [Local AI Agents In 26 Minutes](../../raw/youtube/youtube-M-NTwkM3VwM-local-ai-agents-in-26-minutes.md) — Tina Huang, YouTube

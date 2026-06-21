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
updated: 2026-06-21
---

# Agent Security

**TL;DR**: Hardening LLM agents for production rests on defense in depth — no single control is reliable. Layer input validation (prompt-injection classifiers, sanitization, human-in-the-loop), guardrails (LLM-as-judge, PII masking, moderation), output control ([[ai-engineering/structured-outputs|structured outputs]]), and architecture (least privilege, scoped tools, auth inheritance, observability) [^src1]. "Security is just good engineering applied to AI" [^src1]. Emerging protocols like auth.md extend this to agent identity and registration [^src3].

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
3. **Output control** — [[ai-engineering/structured-outputs|structured outputs]] with Pydantic schemas, response-format enforcement, the Instructor library for automatic retries, output validation before downstream use.
4. **Architecture** — least-privilege database access, scoped tool permissions, authentication inheritance for multi-tenant apps, comprehensive logging/monitoring/observability, cloud content filtering.

The recommended learning sequence is reliability first (structured outputs) → understand the threat (injection) → secure design → hands-on guardrails → observability [^src1].

### Human-in-the-loop (HITL)

A code-driven guardrail that blocks execution if the user rejects an action, breaking the agent loop. Two types: **user permission** and **user input** [^src1]. Strongly recommended where destructive operations carry high impact — in testing, agents asked before destructive operations (e.g. DELETE endpoints) only "most of the time," frequently proceeding without asking [^src1]. (See [[ai-engineering/agent-harness|agent harness]] guidance on confirming irreversible actions.)

### Key principles

- **Guardrails are not deterministic** — "They can fail to block something. This is part of real-world LLM security. Layer your defenses" [^src1].
- **Least privilege as a hard backstop** — "An agent can't drop your production table if it doesn't have DROP permissions" [^src1].
- **Log everything** — "You cannot debug what you didn't log"; the biggest challenge in AI projects is silent errors — agents attempting things they shouldn't, or hallucinating that an action succeeded [^src1].

## Production hardening at the harness level

Coding-agent harnesses add their own real-time security passes. Anthropic's `security-guidance` plugin reviews Claude's edits as they happen and sends vulnerabilities back for immediate fix: every file write triggers a scan, a model double-checks diffs at turn end, high-severity issues are fed back for fixing, and on git commit an agentic reviewer traces data flow to catch cross-file bugs like IDOR or cross-file SSRF [^src5]. (See [[ai-engineering/claude-code|Claude Code]].) On the exfiltration side, ChatGPT's **Lockdown Mode** can't stop an injection from landing but "seals the exits," cutting the outbound requests attackers use to siphon data — at the cost of disabling agent mode, deep research, and downloads [^src6].

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

A 2022 study found developers using AI coding assistants were *more* confident in their code's security even when it was objectively less secure than code written without AI [^src8]. The effect is compounding: AI-generated code may contain more vulnerabilities *and* the developer is less likely to subject it to security review. "Trust but verify" (Russian proverb invoked in ch8) is the corrective stance: trust the output enough to use it as a starting point, but verify before it ships [^src8]. See [[ai-engineering/agent-testing|Agent Testing]] for the testing-side complement.

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

See [[ai-engineering/computer-use|Computer Use]] for implementation detail on browser-use configuration with Sonnet 4.6 (most robust for clicking tasks).

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

## Agent identity and registration (auth.md)

As agents act on behalf of users, identity becomes a security surface. **auth.md** is an open protocol (authored by WorkOS, not tied to its infrastructure) for agent registration without a sign-up form [^src3]. An app hosts a Markdown file at `https://yourapp.com/auth.md` declaring supported flows, scopes, and how to register [^src3]. Two flows [^src3]:
- **Agent verified** — agent-attested; the agent's identity provider vouches for the user, no human in the loop.
- **User claimed** — needs no provider; the agent shows the user a code, they sign in and confirm it.

It issues a scoped, short-lived, revocable access token over standard OAuth, composing existing standards (Protected Resource Metadata, ID-JAG identity assertions) so existing API auth is reused [^src3].

## See also

- [[ai-engineering/structured-outputs|Structured Outputs]] — output-control layer; reliability prerequisite for security
- [[ai-engineering/prompt-engineering|Prompt Engineering]] — injection is the adversarial inverse; few-shot defenses
- [[ai-engineering/agent-harness|Agent Harness]] — where HITL and confirmation gates live
- [[ai-engineering/claude-code|Claude Code]] — real-time security plugin reviewing agent edits
- [[ai-engineering/mcp|MCP]] — tool-exposure surface; scoped permissions and OAuth apply
- [[ai-engineering/claude-models|Claude Model Lineup]] — Opus 4.7 powers Claude Security's model-backed scans
- [[ai-engineering/agent-testing|Agent Testing]] — the testing-side complement to security; overconfidence effect
- [[ai-engineering/vibe-coding|Vibe Coding]] — the 70% problem; why AI code needs more security review, not less
- [[ai-engineering/sources/beyond-vibe-coding-book|Beyond Vibe Coding (Book)]] — ch8 as primary source for vulnerability taxonomy

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

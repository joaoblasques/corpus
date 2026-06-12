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
aliases:
  - prompt injection
  - LLM security
  - AI guardrails
  - agent hardening
  - auth.md
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-12
updated: 2026-06-12
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

Coding-agent harnesses add their own real-time security passes. Anthropic's security plugin reviews Claude's edits as they happen and sends vulnerabilities back for immediate fix: every file write triggers a scan, a model double-checks diffs at turn end, high-severity issues are fed back for fixing, and on git commit an agentic reviewer traces data flow to catch cross-file bugs like IDOR or SSRF [^src1]. (See [[ai-engineering/claude-code|Claude Code]].) On the exfiltration side, ChatGPT's "Lockdown Mode" can't stop an injection from landing but "seals the exits," cutting the outbound requests attackers use to siphon data — at the cost of disabling agent mode, deep research, and downloads [^src1].

## Offensive use: agents as AppSec testers

The same agent capabilities that need hardening can be turned outward — pointing a coding agent at an app to *find* the vulnerabilities. One security researcher built a deliberately vulnerable book-review app (FastAPI backend, React Native/Expo Hermes-exported Android app) with a flag hidden in private reviews, then spent ~$1,500 running multiple LLMs as autonomous attackers to see if they could reproduce a real-world exploit class [^src4].

The planted bug: the API itself was hardened, but the app shipped a `google-services.json` exposing Firebase config, letting an attacker sign up directly against Firebase and read the Firestore DB — **Broken Access Control / Missing Object-Level Authorization**, which the author reports seeing "in the wild" on Firebase and Supabase apps with a hardened API but wide-open data layer [^src4].

### What it tells us about agents-as-attackers

- **It works, unevenly.** Of ten models given ten runs each, GPT-5.5 solved 7/10; Claude Sonnet 4.6 and Claude Opus 4.8 each 2/10; several models (Gemini, MiniMax, DeepSeek Flash) solved 0/10 [^src4]. Not a scientific eval, but a useful signal that capability varies widely.
- **The hard part is approach, not skill.** Failing runs typically fixated on the API/app surface and never pivoted to the real attack vector (Firebase) — or found Firebase but tried to use its credentials *against the API* instead of directly [^src4]. The author had to use harness extensions to "force models to keep trying" rather than report "API seems secure" [^src4].
- **Safety guardrails interfere with legitimate testing.** Some models gave immediate refusals (Gemini 3.1 Pro: ~9k median tokens/run vs 100k+ for engaged runs) [^src4]. Others showed "late refusals" — Claude Opus "got so close... but security guardrails ended the session early" [^src4]. An OpenAI account "already approved for security research" avoided refusals [^src4]. The same models also hesitated to act against a live DB: most "had momentary blips of 'This would affect the live database so I'm not going to do that'" [^src4].

**Defensive takeaway for builders**: a hardened API is not enough if the data layer (Firebase/Supabase) is directly reachable — the least-privilege and scoped-access principles above apply to the *backend-as-a-service* layer, not just your own endpoints. Assume an attacker can run a capable agent against your shipped client and any config it bundles.

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

---

[^src1]: [Building Secure AI Agents: From Prompt Injection to Production Guardrails (email)](../../raw/email/email-2026-05-28-building-secure-ai-agents-from-prompt-injection-to-productio.md)
[^src2]: [Secure LLMs for Data Engineers: How to prevent Prompt Injection](../../raw/web/secure-llms-how-to-prevent-prompt-injection.md)
[^src3]: [auth.md — open protocol for agent registration](../../raw/web/auth-md-open-protocol-for-agent-registration.md)
[^src4]: [I built a vulnerable app and spent $1,500 seeing if LLMs could hack it](../../raw/web/i-built-a-vulnerable-app-and-spent-1-500-seeing-if-llms-coul.md) — Kasra

---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/web/automated-agent-testing-with-playwright.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/automated-agent-testing-with-playwright-b6d5ac15.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-06-09-keep-your-ai-coding-agents-honest-by-testing-them.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/web/did-claude-increase-bugs-in-rsync.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/notes/notes-03-the-70-percent-problem-ai-assisted-workflows-that-actuall.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-05-understanding-generated-code-review-refine-own.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-07-building-web-applications-with-ai.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-08-security-maintainability-and-reliability.md
    channel: notes
    ingested_at: 2026-06-17
aliases:
  - agent testing
  - testing coding agents
  - agent honesty
  - verification loops
  - keeping agents honest
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-12
updated: 2026-06-17
---

# Agent Testing

**TL;DR**: Coding agents claim work is done before it actually is. Tests are the external reality check: an agent can assert a feature works, but a passing end-to-end test is proof [^src1]. The discipline is building verification loops — tests, hooks, traces — that feed agents real feedback and refuse to let them call something finished prematurely [^src2].

## Why agents need an external loop

LLMs "like to call something done before it really is" [^src2]. Left to self-report, an agent's claim that a feature works is unverified. A test that drives the real application the way a user would — clicking, typing, waiting for loads, then asserting the app behaved correctly — converts a claim into evidence [^src1].

Reinforcement tools (tests, linters) are the **external loop** that keeps an agent from prematurely declaring success [^src2]. The framing inverts the engineer's job: the real work "was never typing code" but architecting systems you can be confident in [^src2]. See [[ai-engineering/context-engineering|Context Engineering]] — agents need the right information at the right time, and a failing test with rich context is exactly that.

## Playwright as the reality check

Playwright drives a real browser end-to-end, making it a strong verification harness for agentic coding [^src1]. Patterns that make agent-facing tests reliable [^src2]:

| Technique | Purpose |
|---|---|
| **Accessibility-tree locators** | Stay high in the DOM hierarchy; reduces flakiness vs brittle selectors |
| **Semantic HTML** | Keeps tests accurate and stable as the UI changes |
| **Storage-state auth** | Serialize and reuse login once instead of logging in per test (fast, stable) |
| **HAR / route mocking** | Deterministic network responses; test edge cases (404s, errors) and run offline |
| **Visual regression** | Image-diff thresholds catch unexpected UI changes during refactors |
| **Traces** | Give agents detailed failure context (screenshots, video, file paths) so they guess less |

### Feedback that makes autonomous debugging work

The pattern: set up commit hooks, hand the agent a **failing test plus well-defined success criteria**, and let it resolve the bug on its own [^src2]. Clear success conditions are what make autonomous debugging actually work — vague criteria ("make it work") stall the loop [^src2]. Traces matter because "having all that information upfront cuts down on the guesswork an agent has to do when a test fails" [^src2].

### Git hooks enforce quality before the repo

Pre-commit and pre-push hooks (Husky, lint-staged, Lefthook) run formatting, tests, and checks for leaked API keys before code reaches the repository [^src2]. This is the deterministic enforcement layer beneath the advisory test loop.

### Playwright agent tooling

Playwright's `init agents` command scaffolds three sub-agents — **Generator, Healer, and Planner** — that drop into an agentic workflow; the Playwright MCP and Playwright CLI are distinct integration surfaces with different tradeoffs [^src2].

## Review-debug-refactor: the ownership cycle for AI-generated code

AI output requires a structured ownership cycle before it can be trusted [^src4]:

**Review:** The "majority solution" effect means AI tends to produce the most common/generic solution, which may not be appropriate for the specific context. Treat AI code as if an intern wrote it — assume good intent and basic competence but verify everything before merging. Copyright/licensing risk also enters at the review stage: training data provenance is opaque, and code that looks original may reproduce licensed patterns [^src4].

**Debug:** A 6-step debugging process for AI-generated code: (1) isolate the failure to the smallest reproducible case, (2) read the code literally, not charitably — the model's intent doesn't matter, only what the code actually does, (3) check the AI's own explanation against the code, (4) look for the "majority solution" substituting a generic approach for the specific one needed, (5) add instrumentation, (6) ask the AI to explain its own code in detail — mismatches between explanation and code often reveal the bug [^src4].

**Refactor:** After verifying correctness, pass AI-generated code through the same refactoring discipline as human code: extract duplication, simplify conditionals, add types/contracts, and ensure error paths are explicit. AI-generated code frequently passes happy-path tests while leaving error handling shallow or absent [^src8].

## Testing frameworks for AI-generated code

Ch8 catalogs testing types that complement the Playwright/E2E focus above [^src8]:

| Test type | Purpose for AI code |
|---|---|
| **Unit** | Verify individual functions; catch the "majority solution" effect at the smallest scope |
| **Integration** | Catch cross-component assumptions the AI made that human review missed |
| **End-to-end** | Simulate real user flows; the strongest signal that the AI's output actually works |
| **Property-based** | Generate random inputs to find edge cases the AI's training distribution didn't cover |
| **Load/performance** | AI-generated code often passes functional tests but fails under realistic traffic |
| **Error-handling** | AI reliably generates happy-path code; error paths must be explicitly tested |
| **Monitoring** | Production observability for nondeterministic failures (AI inference differs from code generation — runtime AI is nondeterministic even when the committed code is deterministic) |

Key nondeterminism distinction: AI *code generation* is deterministic once committed to version control. Runtime AI *inference* (if the code calls an LLM) is nondeterministic. Tests must treat these differently [^src8].

## The overconfidence effect

A 2022 study found that developers using AI coding assistants were *more* confident in their code's security even when the code was objectively less secure than code written without AI [^src7]. This is the testing-specific instance of the [[ai-engineering/vibe-coding|70% problem]]: the developer's trust in the AI's output substitutes for the verification loop the AI cannot perform on itself. The implication for testing discipline: AI-assisted code needs *more* scrutiny for security, not less, precisely because the confidence signal is inverted.

Supporting data: 25–33% of GitHub Copilot-generated code has security weaknesses (2023 analysis); 40% of AI-generated code had potential vulnerabilities in a 2021 study [^src7]. See [[ai-engineering/agent-security|Agent Security]] for the full vulnerability taxonomy.

## Bug-regression evidence: did agents make things worse?

A natural fear is that agent-assisted commits ship more bugs. The rsync case study is a rare empirical test of that claim [^src3].

**Context**: In May 2026 a spurious Mastodon post correlated an rsync regression with the release containing Claude commits; the outrage spread to Hacker News and a GitHub issue with 350+ comments, much of it harassment with "no bug report, no technical content" [^src3].

**Method**: Every commit was ordered by date and grouped into releases; bugs (from GitHub, Bugzilla, mailing list) were attributed to releases and scored 0–100 for severity by a small open-weight model at temperature 0. The metric was **severity-weighted bugs per 10 commits (sev/10c)** [^src3].

**Findings** [^src3]:

| Test | Result |
|---|---|
| Permutation test | Claude group's bug rate ≈ a coin flip vs random release pairs — nothing unusual |
| Distribution | The two Claude releases *bracket* the historical interquartile range in opposite directions; neither is an outlier |
| Lines changed | Claude releases changed far more lines but had no more bugs — "More code, same bugs" |
| Regime check | Within the v3.x era, Claude releases sit mid-pack or better; the higher-bug regime predates Claude |

The single worst release in rsync history (v3.4.1, 97th percentile) was **entirely pre-Claude** — "and yet nobody noticed" because there was no enemy to blame [^src3].

**Root cause of the real regressions**: not Claude, but a flood of AI-generated CVE reports forcing rapid, extensive changes to rsync's attack surface — "LLMs → more known security issues → more changes needed → more regressions" [^src3]. Maintainer Andrew Tridgell: the model being useful "does mean you have to be cautious, but I am being cautious" [^src3].

**Takeaway for agent testing**: attributing a regression to "the agent" requires a baseline. Severity-weighting and release-level grouping are the honest framing; absent that, anti-AI sentiment fills the gap with vibes. The defensive posture is the same one this page argues for — verification loops and evidence, not self-report or outrage.

## Related

- [[ai-engineering/ai-agent|AI Agent]] — agents claim completion; tests verify it
- [[ai-engineering/agent-evaluation|Agent Evaluation]] — offline/online eval is the systematic version of this loop
- [[ai-engineering/context-engineering|Context Engineering]] — traces and failing tests as just-in-time context
- [[ai-engineering/agent-security|Agent Security]] — vulnerability taxonomy; the overconfidence effect connects security + testing
- [[ai-engineering/vibe-coding|Vibe Coding]] — the 70% problem; why testing discipline is mandatory, not optional
- [[ai-engineering/sources/beyond-vibe-coding-book|Beyond Vibe Coding (Book)]] — ch5, ch7, ch8 as primary sources

---

[^src1]: [Keep your AI coding agents honest by testing them](../../raw/email/email-2026-06-09-keep-your-ai-coding-agents-honest-by-testing-them.md)
[^src2]: [Playwright: Automated Testing & AI Workflows](../../raw/web/automated-agent-testing-with-playwright.md)
[^src3]: [Did Claude increase bugs in rsync?](../../raw/web/did-claude-increase-bugs-in-rsync.md)
[^src4]: [Ch5 — Understanding Generated Code: Review, Refine, Own](../../raw/notes/notes-05-understanding-generated-code-review-refine-own.md)
[^src7]: [Ch7 — Building Web Applications with AI](../../raw/notes/notes-07-building-web-applications-with-ai.md)
[^src8]: [Ch8 — Security, Maintainability, and Reliability](../../raw/notes/notes-08-security-maintainability-and-reliability.md)

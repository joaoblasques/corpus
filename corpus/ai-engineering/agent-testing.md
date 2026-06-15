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
updated: 2026-06-12
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

---

[^src1]: [Keep your AI coding agents honest by testing them](../../raw/email/email-2026-06-09-keep-your-ai-coding-agents-honest-by-testing-them.md)
[^src2]: [Playwright: Automated Testing & AI Workflows](../../raw/web/automated-agent-testing-with-playwright.md)
[^src3]: [Did Claude increase bugs in rsync?](../../raw/web/did-claude-increase-bugs-in-rsync.md)

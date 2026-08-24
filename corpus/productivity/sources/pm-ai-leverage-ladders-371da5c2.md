---
type: source
domain: productivity
status: draft
sources:
  - path: raw/_inbox/web-how-top-pms-increase-their-leverage-with-ai-371da5c2.md
    channel: web
    ingested_at: 2026-08-24
aliases:
  - PM AI leverage
  - three ladders of PM AI leverage
  - AI-native builder
  - personal leverage ladder
  - product leverage ladder
  - systems leverage ladder
tags:
  - corpus/productivity
  - source
  - ai-tools
  - product-management
  - leverage
created: 2026-08-24
updated: 2026-08-24
---

# How Top PMs Increase Their Leverage with AI: The Three-Ladder Framework

**TL;DR.** A forward-looking framework from Colin Matthews (published via Lenny's Newsletter, mid-2026) for PM AI leverage organized into three ladders — personal, product, and systems — each with three rungs. Domain expertise multiplies results on all rungs. The framework comes from training 30,000+ PMs. [^pm]

## The three ladders

| Ladder | What it gives | Top-rung capability |
|---|---|---|
| Personal | Check items off your own to-do list faster | AI completes multi-step tasks and checks its own results |
| Product | Ship the right things more quickly | Agent ships code changes to production as pull requests |
| Systems | Build repeatable, consistently outsourced workflows | Automated pipelines that run without manual intervention between steps |

"As you ascend each ladder rung, you get an order of magnitude more leverage." [^pm]

## Personal leverage ladder

Three rungs [^pm]:

- **Rung 1 — Write text**: use AI for PRDs, tickets, emails; copy-paste results to other tools
- **Rung 2 — Create artifacts**: slides, basic Excel models, small prototypes; AI generates the artifact itself
- **Rung 3 — Delegate complete to-do items**: connect LLM to Amplitude, Google Drive, Notion, PostHog via MCP; the LLM pulls and pushes data to complete tasks end-to-end (e.g. retention analysis running to an HTML output with citations)

Key enabler for rung 3: MCP connections to the products you use frequently. "Simply navigate to your product's connectors marketplace and add your tools." [^pm]

Workflow-to-skill pattern: once AI completes a task well in a chat session, lock in the workflow by asking the LLM to create a skill (repeatable prompt/workflow) in the same session [^pm].

## Product leverage ladder

Three rungs [^pm]:

- **Rung 1 — Web-based prototypes**: Lovable, Replit, Magic Patterns; communicates ideas but code is disconnected from real codebase
- **Rung 2 — Code-based prototypes**: Claude Code or Codex accesses your real codebase; uses real components, design patterns, follows existing conventions
- **Rung 3 — Agent ships to production**: agent creates a pull request; engineer reviews and merges. Appropriate for copy changes, small UI/UX tweaks, changes to views using existing backend code

For rung 2, the recommended setup: ask an engineer to create a "UI-only" repo — all base UI elements, styles, routes, pages, components, plus a mock data store mimicking the API — that runs without environment variables or backend services. PMs can then use Claude Code against this repo without accidentally breaking production [^pm].

"As a PM, it does not make sense to spend time being a worse engineer than the rest of your team. Knowing when you should write a doc, ship a prototype, or create a PR is as important as the technical ability." [^pm]

## Systems leverage ladder (implied)

The framework defines systems leverage as building repeatable automated workflows — skills and multi-step chains — so that AI completes recurring work consistently at high quality. This is the layer above one-off task delegation: the work runs without the PM initiating it each time [^pm].

## Domain expertise as multiplier

The framework is explicit that AI leverage does not replace domain expertise — it multiplies it. A PM who understands their data model, product architecture, and customer problems will extract far more value from rung-3 workflows than someone who doesn't [^pm].

## Related corpus pages

- [AI-Augmented Knowledge Work](/productivity/ai-augmented-knowledge-work.md) — broader treatment of AI in knowledge work
- [Tokenmaxxing and AI Fake Productivity](/productivity/tokenmaxxing.md) — the failure mode (mistaking activity for leverage)

---

[^pm]: Colin Matthews, "How top PMs increase their leverage with AI," Lenny's Newsletter, 2026 (mid-year). `raw/_inbox/web-how-top-pms-increase-their-leverage-with-ai-371da5c2.md`

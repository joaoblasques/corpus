---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/web-how-strongdms-ai-team-build-serious-software-without-even-lo.md
    channel: web
    ingested_at: 2026-08-19
  - path: raw/_inbox/web-the-strongdm-software-factory-building-software-with-ai.md
    channel: web
    ingested_at: 2026-08-19
aliases:
  - software factory
  - dark factory
  - non-interactive development
  - agentic software factory
  - software factory model
confidence: 0.85
last_confirmed: 2026-08-19
tags:
  - ai-engineering
  - agentic-coding
  - software-factory
  - coding-agents
created: 2026-08-19
updated: 2026-08-19
---

# Software Factory

**TL;DR**: A "Software Factory" is a non-interactive development model where human engineers define intent (specs + scenarios) and coding agents write, validate, and iterate on code without human code review. Pioneered by StrongDM's AI Lab in 2025; sometimes called the "Dark Factory" level of AI adoption.

## Core model

Humans define intent: what the system should do, the scenarios it must handle, the constraints that matter. After that, agents take over — they generate code, validate it against real-world behavior, and iterate until convergence, without hand-tuning or human review.[^strongdm-blog]

The guiding mantra at StrongDM:[^simonw]
- **Why am I doing this?** (implied: the model should be doing this instead)
- Code must not be written by humans
- Code must not be reviewed by humans
- If you haven't spent at least $1,000 on tokens per human engineer per day, your software factory has room for improvement

## Key techniques

### Scenario-based validation
StrongDM repurposed "scenario" to mean an end-to-end user story stored outside the codebase (like a holdout set in ML), which agents can understand and validate against. This replaces boolean test suites ("tests are green") with a probabilistic measure: "of all observed trajectories through all scenarios, what fraction likely satisfy the user?"[^simonw]

Scenarios are holdout sets — kept invisible to coding agents to prevent agents from "cheating" by asserting true on tests they wrote themselves.

### Digital Twin Universe (DTU)
A set of behavioral clones of third-party services the software depends on (Okta, Jira, Slack, Google Docs, Sheets). Agents build these twins from public SDK and API docs, targeting 100% compatibility with reference client libraries. Advantages over testing against live services:[^simonw]
- Validate at volumes and rates far exceeding production limits
- Test failure modes dangerous or impossible against live services
- Run thousands of scenarios/hour with no rate limits, abuse detection, or API costs

### Other named techniques
- **Gene Transfusion** — extracting patterns from existing systems and applying them elsewhere
- **Semports** — directly porting code from one language to another via agents
- **Pyramid Summaries** — providing multiple levels of summary so an agent can enumerate short ones quickly and zoom in on detail as needed

## Historical context

The catalyst for StrongDM's approach was the October 2024 revision of Claude 3.5 Sonnet, after which long-horizon agentic coding workflows began "compounding correctness rather than error." StrongDM's AI Lab team (3 people) formed in July 2025.[^simonw]

Simon Willison identifies a broader November 2025 inflection point (Claude Opus 4.5, GPT 5.2) where reliable agentic coding at scale became mainstream.

## Open source output

- **Attractor** (`github.com/strongdm/attractor`): StrongDM's non-interactive coding agent. Notably, the repo contains no code — only markdown spec files and a note to feed them to a coding agent. [unsourced — cannot verify current repo state]
- **cxdb** (`github.com/strongdm/cxdb`): AI Context Store — immutable DAG for conversation histories and tool outputs (~16k Rust + 9.5k Go + 6.7k TypeScript).[^simonw]

## Cost considerations

The "$1,000/day per engineer" benchmark raises real business model questions: if software factory patterns cost $20k/month per engineer in token costs, it becomes a profitability calculation rather than a pure productivity gain. Willison notes that the $200/month Claude Max plan is sufficient for individual exploration without 24/7 agent swarms.[^simonw]

## Related concepts

- [/ai-engineering/agentic-coding.md](/ai-engineering/agentic-coding.md) — the broader practice
- [/ai-engineering/spec-driven-development.md](/ai-engineering/spec-driven-development.md) — spec-first methodology that software factories depend on
- [/ai-engineering/agent-harness.md](/ai-engineering/agent-harness.md) — harness infrastructure software factories run on
- [/ai-engineering/strongdm.md](/ai-engineering/strongdm.md) — the entity that pioneered this model

[^simonw]: Simon Willison, "How StrongDM's AI team build serious software without even looking at the code," simonwillison.net, 2026-02-07. `raw/_inbox/web-how-strongdms-ai-team-build-serious-software-without-even-lo.md`
[^strongdm-blog]: StrongDM Team, "The StrongDM Software Factory: Building Software with AI," strongdm.com, 2026-02-19. `raw/_inbox/web-the-strongdm-software-factory-building-software-with-ai.md`

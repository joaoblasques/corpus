---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/web-how-to-use-the-goal-command-in-claude-code-for-fully-autonom-6a7b32b1.md
    channel: web
    ingested_at: 2026-08-21
aliases:
  - Claude Code /goal command
  - goal command autonomous workflows
tags:
  - corpus/ai-engineering
  - source
created: 2026-08-21
updated: 2026-08-21
---

# How to Use the /goal Command in Claude Code for Fully Autonomous Workflows

**TL;DR.** `/goal` shifts Claude Code from reactive (answer one prompt, stop) to outcome-driven (keep reasoning and executing until measurable exit criteria are met). Effective goals state verifiable conditions, explicit scope, and a failure path; sub-agents can parallelize complex goals across modules. [^src1]

## Key concepts

**Prompt vs. goal.** A prompt is task-scoped ("refactor this function"). A goal is outcome-scoped ("all unit tests pass, TypeScript compilation succeeds, CI pipeline green"). Claude Code continues iterating — fixing errors, re-running tests, adjusting code — until the condition is met or it can't proceed. [^src1]

**When to use /goal:**
- Task requires multiple dependent rounds of execution and error correction
- Success condition is measurable and verifiable
- Unattended operation while working on something else
- Running in headless / automated mode (CI/CD) [^src1]

**Writing effective goals — principles:**
- Verifiable conditions (test exit codes, file existence, API responses, compilation status)
- No subjective language ("better", "cleaner")
- Explicit scope (which files/directories are in scope)
- Negative constraints ("without modifying /config files")
- Failure path ("if any test fails after three retry attempts, stop and report") — prevents infinite loops [^src1]

**Exit criteria types:**
- Command exit codes: `` `npm test` exits with code 0 and all 47 tests pass ``
- File state: "CHANGELOG.md exists with entries for all commits since last tag"
- API response: "GET /health returns `{"status": "ok"}` with 200"
- Composite: combine multiple conditions in one goal [^src1]

**Headless mode.** `claude-code --headless --goal "..."` runs fully non-interactively; exit code usable by CI systems. Always capture logs for audit. Common CI pattern: tests fail → trigger Claude Code with goal to fix them → CI re-runs original test step. [^src1]

**Sub-agents.** Claude Code can spawn parallel sub-agents for complex goals: a primary agent decomposes the goal, spawns sub-agents with their own sub-goals (e.g. one per module in a multi-module refactor), collects results, and verifies top-level exit criteria. [^src1]

**Common mistakes:**
- Underspecifying scope → unintended changes
- Unmeasurable exit criteria → model loops
- No failure path → infinite retries on irresolvable problems
- Overloading a single goal (too broad) → break into sequential sub-goals [^src1]

**Real-world use cases:** automated test repair after dependency updates; JSDoc documentation generation with coverage verification; dependency migration (replacing deprecated API patterns across a codebase); pre-release checklist automation (multi-condition composite goal). [^src1]

## Related pages

- [Agentic Coding](/ai-engineering/agentic-coding.md)
- [Agent Harness](/ai-engineering/agent-harness.md)
- [Claude Managed Agents](/ai-engineering/claude-managed-agents.md)

[^src1]: raw/_inbox/web-how-to-use-the-goal-command-in-claude-code-for-fully-autonom-6a7b32b1.md (MindStudio, channel: web, 2026-06-30)

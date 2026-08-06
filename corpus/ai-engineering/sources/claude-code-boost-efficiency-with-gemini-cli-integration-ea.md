---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/notes/notes-03-resources-study-notes-claude-code-boost-efficiency-with-gemini-cli-integration.md
    channel: notes
    ingested_at: 2026-07-06
aliases: []
tags:
  - corpus/ai-engineering
  - source
  - doc-quick-intake
created: 2026-07-06
updated: 2026-08-06
provisional: false
url: 
origin: obsidian
consolidated_into: ai-engineering/gemini-cli.md
---

# Claude Code - Boost Efficiency with Gemini CLI Integration

**TL;DR:** Use Gemini CLI as a sub-contractor for Claude Code when tasks exceed Claude's context window — particularly for large codebase analysis where files total >100KB.

---

## Core Pattern

The central technique is delegating large-context tasks from Claude Code to Gemini CLI.[^1] Gemini CLI handles entire codebases due to its massive context window, while Claude Code orchestrates the workflow.

[^1]: raw/notes/notes-03-resources-study-notes-claude-code-boost-efficiency-with-gemini-cli-integration.md

**When to delegate to Gemini CLI:**[^1]
- Files totaling >100KB
- Entire codebase architecture analysis
- Comparing multiple large files
- Understanding project-wide patterns

## Gemini CLI Advantages

- Free tier: 100 requests/day with Gemini 2.5 Pro[^1]
- Massive context window capable of ingesting entire codebases[^1]

## CLAUDE.md Setup

Add a dedicated section to `CLAUDE.md` instructing Claude to invoke Gemini CLI for large analysis tasks:[^1]

```markdown
## Large Codebase Analysis
Use Gemini CLI when analyzing entire codebases or multiple large files.
- gemini -p "analyze this: $(cat file.py)"
- gemini --all-files -p "..."
```

## Prefix Commands

Even with the CLAUDE.md section in place, prefix individual requests explicitly to ensure delegation occurs.[^1] Example prompt pattern:

> "Use Gemini to analyze the current architecture and plan how to implement X. Put the plan in a markdown file and pause for my feedback."[^1]

The pause-for-feedback step is deliberate — review the plan before Claude begins coding.[^1]

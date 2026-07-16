---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/notes/notes-03-resources-articles-diving-into-spec-driven-development-with-github-spec-kit.md
    channel: notes
    ingested_at: 2026-07-14
aliases: []
tags:
  - corpus/ai-engineering
  - source
  - doc-quick-intake
created: 2026-07-14
updated: 2026-07-16
provisional: false
url: https://developer.microsoft.com/blog/spec-driven-development-spec-kit
origin: obsidian
---

# Diving Into Spec-Driven Development With GitHub Spec Kit - Microsoft for Developers

**Source:** Den Delimarsky, Microsoft for Developers blog — [developer.microsoft.com](https://developer.microsoft.com/blog/spec-driven-development-spec-kit)

## TL;DR

Spec-Driven Development (SDD) is a methodology that treats specifications as living documents capturing the "why" behind technical decisions; GitHub Spec Kit is a toolkit (Specify CLI + templates + slash commands) that operationalizes this for AI-driven projects by structuring work into a Constitution→Specify→Plan→Tasks→Implement→Validate loop.[^1]

## Core Concepts

**Spec-Driven Development (SDD).** SDD makes technical decisions "explicit, reviewable, and adaptable by capturing the 'why' behind choices in a format that evolves with the project."[^1] The emphasis is on shared context: AI coding agents and human team members alike work from the same specification artifact, reducing misalignment.[^1]

**GitHub Spec Kit.** A toolkit composed of the Specify CLI, foundational templates for specs/plans/tasks, and scripts. It bootstraps a structured SDD environment within a repository.[^1]

**Specify CLI.** Installed via `uvx`; supports multiple coding agents and bootstraps new projects with the template scaffolding needed to begin SDD.[^1]

**Slash commands.** Three sequential commands drive the workflow: `/specify` (write the spec), `/plan` (produce the technical plan), `/tasks` (break into implementable tasks).[^1] This maps directly to the Implement→Validate steps that follow.

**Living specifications.** Specs are version-controlled documents updated continuously as requirements change; version control provides traceability.[^1]

## Workflow

1. Bootstrap with `uvx specify init` (Specify CLI).
2. Run `/specify` — author the specification with detailed functional requirements; avoid prescribing technical solutions at this stage.[^1]
3. Run `/plan` — produce the technical plan from the spec.
4. Run `/tasks` — decompose the plan into implementable task units.
5. Implement and validate against the spec.

## Best Practices

- **Detailed initial prompts:** include functional requirements and motivations; "avoid specifying technical solutions too early in the process."[^1]
- **Regular spec reviews:** incorporate review cycles into the workflow to keep specs aligned with current objectives.[^1]
- **Version control for specs:** ensures accountability and traceability of specification changes.[^1]

## Common Pitfalls

- **Incomplete specifications** → misinterpretation and revision cycles; mitigated by team-wide spec review.[^1]
- **Ignoring specification updates** → specs diverge from actual project state; mitigated by scheduled review cadences.[^1]

## Relation to Corpus Pages

- [Spec-Driven Development](/ai-engineering/spec-driven-development.md) — this Microsoft source documents the same GitHub Spec Kit tooling the concept page describes as the Constitution→Specify→Plan→Tasks→Implement→Validate loop; it is a second, independent account of that workflow.
- [Agentic Coding](/ai-engineering/agentic-coding.md) — the surrounding coding-agent practice that SDD is designed to support.
- [AI Engineering hub](/ai-engineering/README.md)

[^1]: raw/notes/notes-03-resources-articles-diving-into-spec-driven-development-with-github-spec-kit.md

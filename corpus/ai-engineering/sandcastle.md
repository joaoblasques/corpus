---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/web/github-mattpocock-sandcastle-orchestrate-sandboxed-coding-ag.md
    channel: web
    ingested_at: 2026-06-16
aliases:
  - Sandcastle
  - "@ai-hero/sandcastle"
  - ai-hero sandcastle
tags:
  - corpus/ai-engineering
  - entity
created: 2026-06-16
updated: 2026-06-16
---

# Sandcastle

**TL;DR.** Sandcastle is a TypeScript library for orchestrating AI coding agents in isolated sandboxes: a single `sandcastle.run()` invokes an agent, the library sandboxes it under a configurable branch strategy, and the agent's commits get merged back [^src1]. It is provider-agnostic — shipping built-in providers for Docker, Podman, and Vercel, with the ability to create custom ones — and is aimed at parallelizing AFK ("away from keyboard") agents, building review pipelines, or orchestrating one's own agents [^src1].

## What it is

A programmatic harness for [AFK/long-running coding agents](/ai-engineering/long-running-agents.md). You invoke `run()` (one-shot), `createSandbox()` (multiple runs in one container), `createWorktree()` (worktree as a first-class concept), or `interactive()`, passing an **agent provider** and a **sandbox provider** [^src1]. The package is installed via `npm install --save-dev @ai-hero/sandcastle`, with `npx @ai-hero/sandcastle init` scaffolding a `.sandcastle/` config directory [^src1].

```ts
import { run, claudeCode } from "@ai-hero/sandcastle";
import { docker } from "@ai-hero/sandcastle/sandboxes/docker";
await run({
  agent: claudeCode("claude-opus-4-7"),
  sandbox: docker(), // or podman(), vercel(), or your own provider
  promptFile: ".sandcastle/prompt.md",
});
```

## Sandbox providers

A `SandboxProvider` tells Sandcastle how to execute commands in an isolated environment [^src1]. There are two kinds: **bind-mount** (mounts a host directory, e.g. Docker/Podman — no file sync needed) and **isolated** (own filesystem, e.g. a cloud VM — syncs code in/out) [^src1]. Built-in providers: Docker (bind-mount), Podman (bind-mount, rootless), Vercel (isolated — Firecracker microVMs via `@vercel/sandbox`), and `noSandbox()` (runs the agent directly on the host, no container isolation) [^src1]. Custom providers are built with `createBindMountSandboxProvider` or `createIsolatedSandboxProvider` [^src1].

## Branch strategies

Sandcastle controls where the agent's commits land via a branch strategy on `run()` [^src1]:

- **head** — agent writes directly to the host working directory; no worktree or branch indirection. Default for bind-mount providers; only works with bind-mount [^src1].
- **merge-to-head** — a temp branch in a git worktree; changes merge back to HEAD when done. Default for isolated providers; the "safe default for automation" [^src1].
- **branch** — commits land on an explicitly named branch; re-running with the same branch reuses the worktree [^src1].

## Agent providers

The harness is multi-agent-provider: `claudeCode`, `pi`, `codex`, `cursor`, `opencode`, and `copilot` are all supported, each with provider-specific options (e.g. `claudeCode("claude-opus-4-7", { effort: "high" })` where `effort` maps to Claude Code reasoning level, `max` being Opus-only) [^src1]. Provider factories also accept `env`, `captureSessions`, and `permissionMode` [^src1].

## Notable features

- **Iteration loop with completion signal.** The agent emits a configurable signal (default `<promise>COMPLETE</promise>`) to end the loop early; `maxIterations` caps it [^src1]. A separate `completionTimeoutSeconds` grace window handles "hanging processes" — a spawned `gh`/git child or MCP server keeping stdout open — so the run resolves successfully with the commits already made instead of failing on idle timeout [^src1].
- **Session capture, resume, and fork.** For resumable providers (Claude Code, Codex, Pi), Sandcastle captures the agent's session JSONL to the host so `--resume` works; `.fork()` continues from a captured session under a new session id, enabling fan-out workflows [^src1]. Safe concurrent fan-out requires each child get a distinct branch [^src1].
- **Structured output.** `Output.object()` / `Output.string()` extract a typed, schema-validated payload from the agent's stdout (any Standard Schema validator — Zod, Valibot, ArkType); requires `maxIterations === 1` [^src1].
- **Prompt system.** `promptFile` supports `{{KEY}}` substitution via `promptArgs` and `` !`command` `` shell expansion (run inside the sandbox); inline `prompt` strings are passed literally with no substitution [^src1].
- **Templates.** `init` scaffolds one of five workflow templates: `blank`, `simple-loop`, `sequential-reviewer`, `parallel-planner`, and `parallel-planner-with-review` — the planner templates plan parallelizable issues, execute on separate branches, then merge [^src1].

## Relationships

- A concrete harness for running [long-running / AFK agents](/ai-engineering/long-running-agents.md); the `sequential-reviewer` and `parallel-planner-with-review` templates implement [multi-agent](/ai-engineering/multi-agent-systems.md) reviewer patterns.
- Built to orchestrate [Claude Code](/ai-engineering/claude-code.md) (its default agent provider) among other coding agents.
- Authored by Matt Pocock, shipped under the `@ai-hero/` npm scope; MIT-licensed [^src1].

[^src1]: [mattpocock/sandcastle — orchestrate sandboxed coding agents](../../raw/web/github-mattpocock-sandcastle-orchestrate-sandboxed-coding-ag.md)

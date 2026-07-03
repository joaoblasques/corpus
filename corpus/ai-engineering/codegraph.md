---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/web/github-colbymchenry-codegraph-pre-indexed-code-knowledge-gra.md
    channel: web
    ingested_at: 2026-06-16
aliases:
  - CodeGraph
  - "@colbymchenry/codegraph"
  - codegraph
tags:
  - corpus/ai-engineering
  - entity
created: 2026-06-16
updated: 2026-06-16
---

# CodeGraph

**TL;DR.** CodeGraph is a 100%-local tool that gives AI coding agents a pre-indexed knowledge graph of a codebase — symbol relationships, call graphs, and code structure — so agents query the graph instantly instead of scanning files with grep/glob/Read [^src1]. It is delivered as an [MCP](/ai-engineering/mcp.md) server that auto-configures Claude Code, Cursor, Codex, opencode, Hermes Agent, Gemini, Antigravity, and Kiro [^src1]. Benchmarked across 7 repos/7 languages, it reported on average "16% cheaper · 47% fewer tokens · 22% faster · 58% fewer tool calls" [^src1].

## What it does

When an agent explores a codebase, it spawns Explore agents that scan files with grep, glob, and Read — consuming tokens on every tool call; CodeGraph replaces that discovery loop with graph queries against a pre-built index [^src1]. The mechanism: tree-sitter parses source into ASTs, language-specific queries extract nodes (functions, classes, methods) and edges (calls, imports, extends, implements), everything is stored in a local SQLite database (`.codegraph/codegraph.db`) with FTS5 full-text search, and references are resolved post-extraction [^src1]. This is a concrete instance of [agentic search](/ai-engineering/agentic-search.md) — pre-indexed structural retrieval rather than a grep/read sweep — and an [agent-cost](/ai-engineering/agent-cost-management.md) play (fewer tool calls, fewer tokens).

## Setup

Install via a one-line OS-detecting shell/PowerShell installer or `npm i -g @colbymchenry/codegraph`; CodeGraph bundles its own runtime so there is nothing to compile [^src1]. `codegraph install` auto-detects and wires the MCP server into each agent; `codegraph init -i` creates the per-project `.codegraph/` index directory and builds the initial graph [^src1]. Configuration is zero-config — there is no config file; language support is automatic from file extension, and it skips dependency/build/cache directories, `.gitignore`d paths, and files over 1 MB by default [^src1].

## MCP tools

When running as an MCP server (`codegraph serve --mcp`) it exposes [^src1]:

- **`codegraph_explore`** — *primary*. Answers almost any question in one call ("how does X work", a flow "how does X reach Y", surveying an area), returning the relevant symbols' verbatim source grouped by file plus a relationship map and blast radius; surfaces dynamic-dispatch hops (callbacks, interface→impl) grep can't follow [^src1].
- **`codegraph_search`** — find symbols by name.
- **`codegraph_callers` / `codegraph_callees`** — walk the call graph.
- **`codegraph_impact`** — analyze what code is affected by changing a symbol.
- **`codegraph_node`** — one symbol's full source (every overload for ambiguous names).
- **`codegraph_files` / `codegraph_status`** — indexed file structure; index health.

A `codegraph affected` CLI command traces import dependencies transitively to find which test files are affected by changed source files, usable in CI/git hooks [^src1].

## Staying fresh

Three layers keep the index in step with the code [^src1]: a **file watcher** using native OS events (FSEvents/inotify/ReadDirectoryChangesW) with debounced auto-sync (default 2000ms); a **per-file staleness banner** that, during the debounce window, prepends a ⚠️ banner telling the agent to Read a still-pending file directly; and **connect-time catch-up** reconciliation when the MCP server (re)connects.

> "the agent never gets a silent wrong answer in the brief window between an edit and the next sync" [^src1]

## Coverage

20+ languages have full or partial extraction support [^src1]. **Framework-aware routes** link URL patterns to handlers across 16 frameworks (Django, Flask, FastAPI, Express, NestJS, Laravel, Rails, Spring, Gin, Axum, ASP.NET, and more) [^src1]. A distinguishing feature is **mixed iOS / React Native / Expo** bridging — closing cross-language flows (Swift ↔ ObjC, React Native legacy bridge + TurboModules + Fabric, native → JS event emitters, Expo Modules) that static tree-sitter extraction stops at [^src1]. Impact-coverage is measured per language on real benchmark repos rather than asserted, with residuals attributed to genuine static-analysis frontiers (runtime dynamic dispatch, reflection/DI, framework-convention entry points) [^src1].

## Benchmark caveat

The benchmark compares a headless Claude Code (Opus 4.8) answering one architecture question per repo with vs. without CodeGraph, median of 4 runs [^src1]. On the most response-heavy repos (Excalidraw, Tokio) cost is roughly break-even; the largest cost wins are on small repos (Alamofire 40% cheaper, OkHttp 25%) [^src1]. The current numbers are *lower* than the prior Opus 4.7 validation — attributed to a stronger native baseline (Opus 4.8 greps/reads efficiently on the main thread instead of fanning out into Explore-subagent sweeps), not a CodeGraph regression [^src1].

## Relationships

- Delivered as an [MCP](/ai-engineering/mcp.md) server; usage guidance ships in the MCP `initialize` response, so nothing is written to CLAUDE.md/AGENTS.md [^src1].
- Targets [Claude Code](/ai-engineering/claude-code.md) and other coding agents including [Hermes](/ai-engineering/hermes.md).
- A hosted product (getcodegraph.com) is in beta; the CLI/MCP server is MIT-licensed [^src1].

[^src1]: [colbymchenry/codegraph — pre-indexed code knowledge graph](../../raw/web/github-colbymchenry-codegraph-pre-indexed-code-knowledge-gra.md)

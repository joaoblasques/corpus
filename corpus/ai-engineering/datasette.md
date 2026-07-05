---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-release-datasette-1-0a35-29b0393a.md
    channel: web
    ingested_at: 2026-07-05
  - path: raw/web/web-release-datasette-1-0a34-47242b80.md
    channel: web
    ingested_at: 2026-07-05
  - path: raw/web/web-datasette-apps-host-custom-html-applications-inside-datasett-5f725425.md
    channel: web
    ingested_at: 2026-07-05
  - path: raw/web/web-release-datasette-acl-0-6a0-b6fb1ed2.md
    channel: web
    ingested_at: 2026-07-05
  - path: raw/web/web-release-datasette-export-database-0-3a2-bb77945c.md
    channel: web
    ingested_at: 2026-07-05
  - path: raw/web/web-simonw-browser-compat-db-ff39842e.md
    channel: web
    ingested_at: 2026-07-05
aliases:
  - Datasette
  - datasette-lite
  - Datasette Lite
  - datasette-apps
  - datasette-acl
  - datasette-export-database
tags:
  - corpus/ai-engineering
  - entity
created: 2026-07-05
updated: 2026-07-05
---

# Datasette

**TL;DR**: Datasette is an open-source Python tool for exploring, publishing, and sharing SQLite databases as interactive web applications, developed and maintained by Simon Willison [^src1]. As of 2026, it is in a long-running alpha series (1.0a34+) with a focus on full read-write editing, an extensible plugin ecosystem, and a browser-hosted variant (Datasette Lite) using Pyodide + WebAssembly [^src1][^src2].

## Core capabilities

Datasette exposes SQLite databases through a web UI and JSON API, allowing faceted search, SQL querying, and data export. It is designed as a "publish data" tool — deploy a `.db` file as a discoverable, queryable, shareable application.

**Read-write editing (1.0a34+).** The 1.0a34 release added row insert, edit, and delete tools directly in the Datasette UI — features that were "long overdue" according to Willison, and were directly inspired by Datasette Agent's SQL write support being added first [^src2].

**Create/alter table UI (1.0a35+).** The 1.0a35 release added two major interfaces backed by JSON APIs [^src1]:
- **Create table**: define columns, primary keys, custom column types, NOT NULL constraints, literal and expression defaults, single-column foreign keys. Backed by `/<database>/-/create`.
- **Alter table**: add, rename, reorder and drop columns; change column types, defaults, NOT NULL constraints, primary keys and foreign keys; rename or drop entire tables. Backed by `/<database>/<table>/-/alter`.

## Datasette Apps

`datasette-apps` (v0.1a3+) hosts sandboxed HTML+JavaScript applications inside Datasette iframes [^src3]:
- Apps live inside `<iframe sandbox="allow-scripts allow-forms">` + CSP meta tag, preventing XSS and data exfiltration.
- Apps communicate via `postMessage`/`MessageChannel` to issue SQL queries against the database.
- A "prompt-copy" feature lets users paste the schema into any LLM to build apps.
- Security vulnerability found by Claude Fable 5 during development: a less-privileged user could trick an admin into running their app and exfiltrate private data — fixed by restricting CSP allow-listing to users with the `apps-set-csp` permission [^src3].
- Built using Claude Opus 4.6 (initial prototype), GPT-5.5 xhigh / Codex Desktop (main build), and Claude Fable 5 (security review) [^src3].

## Datasette ACL

`datasette-acl` provides fine-grained access control for multi-user Datasette instances. The 0.6a0 release (2026-06-18) expanded scope from table-only permissions toward a general resource-sharing system [^src4].

## Plugin ecosystem

Key plugins as of mid-2026:
- `datasette-apps` — sandboxed HTML applications inside Datasette
- `datasette-acl` — multi-user fine-grained access control
- `datasette-export-database` — export full database; 0.3a2 fixed a `pyproject.toml` version pin that had locked the plugin to `datasette==1.0a27` [^src5]

## Datasette Lite

Datasette Lite runs the full Datasette Python application inside a browser using Pyodide and WebAssembly — no server required. Willison has been exploring whether OPFS (Origin Private File System) can enable Datasette Lite to edit persistent SQLite files directly in the browser [^src6].

A `simonw/browser-compat-db` project demonstrates the pattern: Mozilla's `mdn/browser-compat-data` converted to a ~66 MB SQLite database, hosted on a GitHub orphan branch (open CORS headers), explorable via Datasette Lite [^src7].

## AI-assisted development

Willison actively uses AI coding tools to build Datasette features:
- Claude Code (Opus 4.8) for scripts and web UI experiments
- GPT-5.5 xhigh via Codex Desktop for major build tasks
- Claude Fable 5 for security review

## See also

- [Simon Willison](/ai-engineering/simon-willison.md) — creator and maintainer
- [Agent Security](/ai-engineering/agent-security.md) — datasette-apps security model illustrates sandboxed-iframe injection defense
- [sqlite-utils](/ai-engineering/sqlite-utils.md) — companion CLI/library for manipulating SQLite databases

---

[^src1]: [Release: datasette 1.0a35](../../raw/web/web-release-datasette-1-0a35-29b0393a.md) — Simon Willison, 2026-06-23
[^src2]: [Release: datasette 1.0a34](../../raw/web/web-release-datasette-1-0a34-47242b80.md) — Simon Willison, 2026-06-16
[^src3]: [Datasette Apps: Host custom HTML applications inside Datasette](../../raw/web/web-datasette-apps-host-custom-html-applications-inside-datasett-5f725425.md) — Simon Willison, 2026-06-18
[^src4]: [Release: datasette-acl 0.6a0](../../raw/web/web-release-datasette-acl-0-6a0-b6fb1ed2.md) — Simon Willison, 2026-06-18
[^src5]: [Release: datasette-export-database 0.3a2](../../raw/web/web-release-datasette-export-database-0-3a2-bb77945c.md) — Simon Willison, 2026-06-25
[^src6]: [Tool: OPFS + Pyodide test harness](../../raw/web/web-tool-opfs-pyodide-test-harness-d88aa482.md) — Simon Willison, 2026-06-23
[^src7]: [simonw/browser-compat-db](../../raw/web/web-simonw-browser-compat-db-ff39842e.md) — Simon Willison, 2026-06-24

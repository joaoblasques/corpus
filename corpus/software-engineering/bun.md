---
type: entity
domain: software-engineering
status: draft
sources:
  - path: raw/web/web-bun-is-a-fast-javascriptall-in-one-toolkit.md
    channel: web
    ingested_at: 2026-06-25
aliases:
  - Bun
  - bun runtime
  - bun install
  - bun test
  - bun bundler
  - JavaScript runtime
  - all-in-one JavaScript toolkit
tags:
  - corpus/software-engineering
  - entity
created: 2026-06-25
updated: 2026-07-11
---

# Bun

**TL;DR**: Bun is a fast, incrementally adoptable all-in-one JavaScript/TypeScript/JSX toolkit. It replaces multiple separate tools (Node.js runtime + npm + webpack/esbuild + Jest) with a single binary. Aims for 100% Node.js compatibility so it can be adopted piece-by-piece in existing projects [^src1].

## What Bun includes

| Tool | Bun equivalent |
|---|---|
| Runtime | `bun <script.js>` — replaces Node.js |
| Package manager | `bun install` — replaces npm/yarn/pnpm |
| Test runner | `bun test` — replaces Jest/Vitest |
| Bundler | `bun build` — replaces webpack/esbuild/rollup |

## Key characteristics

- **Fast**: designed from the ground up for speed (written in Zig, uses JavaScriptCore engine instead of V8)
- **Incrementally adoptable**: individual tools like `bun install` can be used in existing Node.js projects without switching the runtime [^src1]
- **Node.js compatible**: aims for 100% compatibility so existing npm packages and Node.js APIs work [^src1]
- **TypeScript and JSX**: native support without additional configuration

## Positioning vs Node.js

Bun positions itself as a drop-in speed upgrade. Running `bun install` instead of `npm install` in a Node.js project requires no other changes. Full adoption (runtime, test, bundler) is optional and progressive [^src1].

## See also

- [JavaScript Fundamentals](/software-engineering/javascript-fundamentals.md) — Bun replaces several Node.js-ecosystem tools
- [FastAPI](/software-engineering/fastapi.md) — Python counterpart for fast API development

---

[^src1]: [Bun — fast JavaScript all-in-one toolkit](../../raw/web/web-bun-is-a-fast-javascriptall-in-one-toolkit.md)

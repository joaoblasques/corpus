---
type: concept
domain: software-engineering
status: stub
sources:
  - path: raw/_inbox/web-i-ported-return-to-castle-wolfenstein-to-the-web-with-multip-15912e08.md
    channel: web
    ingested_at: 2026-08-23
aliases:
  - WASM
  - WebAssembly
  - wasm
tags:
  - corpus/software-engineering
  - concept
  - webassembly
  - emscripten
created: 2026-08-23
updated: 2026-08-23
---

# WebAssembly (WASM)

**TL;DR**: WebAssembly is a binary instruction format and portable compilation target for the web, enabling near-native performance for languages like C, C++, and Rust in browser environments.

## Key toolchain: emscripten

**emscripten** is the primary compiler toolchain for targeting WebAssembly from C/C++ code. It provides:
- Compilation of C/C++ → WASM + JS glue
- Virtual filesystem abstraction (IDBFS for IndexedDB persistence, MEMFS for in-memory)
- OpenGL → WebGL translation (via GL4ES or built-in)
- POSIX compatibility shims (sockets, file I/O)

## Graphics: GL4ES

**GL4ES** translates OpenGL 1.x/2.x calls to WebGL2, enabling legacy OpenGL codebases to run in-browser without full renderer rewrites. Used in game porting where the engine predates WebGL.

## Browser persistence

emscripten provides two main virtual filesystem backends for persistent storage:
- **IDBFS** — IndexedDB-backed; survives page reloads; suitable for large asset packs (~hundreds of MB)
- **MEMFS** — in-memory only; reset on reload

## Game porting pattern

A documented porting pattern for GPL game engines (ioquake3-based):
1. Start from existing WASM single-player port (e.g., Wwasm)
2. Diff the WASM port vs the clean source to isolate emscripten-specific patches
3. Re-graft those patches onto the multiplayer codebase
4. Handle asset extraction separately (offzip for ISO carving when Wine fails)

See: [RTCW Web Port (Pieter Levels, 2026)](/software-engineering/sources/rtcw-web-port-15912e08.md) — concrete case study using this pattern.

## See also

- [AI-Assisted Development](/software-engineering/ai-assisted-development.md) — Pieter Levels used Claude Fable to port RTCW in ~3 hours

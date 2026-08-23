---
type: source
domain: software-engineering
status: draft
sources:
  - path: raw/_inbox/web-i-ported-return-to-castle-wolfenstein-to-the-web-with-multip-15912e08.md
    channel: web
    ingested_at: 2026-08-23
aliases: []
tags:
  - corpus/software-engineering
  - source
  - webassembly
  - emscripten
  - game-porting
  - pieter-levels
created: 2026-08-23
updated: 2026-08-23
---

# Porting Return to Castle Wolfenstein to the Web with Multiplayer (Pieter Levels, 2026)

**TL;DR**: Pieter Levels (levelsio) ported the 2001 game Return to Castle Wolfenstein to the browser with multiplayer in approximately 3 hours total, using Claude Fable as the primary AI pair-programmer. Result: rtcw.pieter.com.

## Technical approach

### Starting point
- Base: **iortcw** — the GPL source port of RTCW (ioquake3-based engine)
- Reference: **Wwasm** — an existing single-player-only WebAssembly port of RTCW
- Strategy: diff Wwasm vs clean iortcw SP to identify EMSCRIPTEN-specific patches, then re-graft those patches into the MP (multiplayer) codebase

### Compilation pipeline
- **emscripten** — compiled the MP engine to WebAssembly
- **GL4ES** — OpenGL 1.x → WebGL2 translation layer
- Fixed GL4ES initialization for the MP renderer (different entry point than the SP renderer)

### Networking
- Re-enabled the multiplayer networking layer (disabled in Wwasm's SP-only port)
- Patched out the 1.41 point-release version check to allow modern builds to connect
- Built a native `iowolfded` dedicated server for the multiplayer backend

### Game asset extraction
- Source: retail CD ISO
- Wine approach failed (i386 dependency hell on modern Linux)
- Solution: **offzip** — carved raw deflate streams from the ISO to extract `pak0.pk3` and `mp_pak0.pk3`

### Client-side asset delivery
- Client fetches pak files over HTTPS into the emscripten virtual filesystem (IndexedDB / IDBFS)
- Total pak size: ~380 MB; downloads once and persists in the browser

## Key techniques documented

| Problem | Solution |
|---|---|
| SP WASM patches → MP codebase | diff Wwasm vs clean SP, re-graft EMSCRIPTEN blocks into MP |
| OpenGL on WebAssembly | GL4ES (OpenGL 1.x → WebGL2) |
| ISO asset extraction without Wine | offzip (deflate stream carving) |
| Browser file persistence | emscripten IDBFS (IndexedDB) |
| Version mismatch | patch out point-release check |

## See also

- [WebAssembly](/software-engineering/webassembly.md) — core compilation target (emscripten → WASM)
- [AI-Assisted Development](/software-engineering/ai-assisted-development.md) — Levels used Claude Fable throughout; ~1 hour of productive coding time

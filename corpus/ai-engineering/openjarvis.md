---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-openjarvis-a-local-first-personal-ai-is-now-available-to-run-559ec7e6.md
    channel: web
    ingested_at: 2026-07-02
aliases:
  - OpenJarvis
  - open-jarvis
  - jarvis (CLI)
tags:
  - corpus/ai-engineering
  - entity
created: 2026-07-02
updated: 2026-07-02
---

# OpenJarvis

**TL;DR.** OpenJarvis is an open-source framework, built by Stanford's Hazy Research and Scaling Intelligence labs (part of their "Intelligence Per Watt" research into efficient local AI), for building personal AI agents that run on the user's own hardware. It makes local-first the default — models run locally via [[ai-engineering/ollama|Ollama]], with cloud as optional fallback — and tracks energy, cost, and latency alongside accuracy [^src1].

## Positioning

Most personal-AI tools send every request to the cloud even though local models can already handle most day-to-day chat and reasoning. OpenJarvis inverts that default: local-first, cloud-optional [^src1]. Version 1.0 ships with built-in [[ai-engineering/ollama|Ollama]] support.

## Setup

```bash
curl -fsSL https://open-jarvis.github.io/OpenJarvis/install.sh | bash   # macOS/Linux
jarvis                                                                   # start
```
Windows: run the install script inside WSL2, or use the desktop app. The install script auto-detects an existing Ollama installation and sets up a starter model.

## Model configuration

```bash
jarvis model pull qwen3.5:35b
jarvis ask -m qwen3.5:35b "Your prompt"
```
Default model set via `~/.openjarvis/config.toml`:
```toml
[intelligence]
default_model = "qwen3.5:35b"
preferred_engine = "ollama"
```

## Built-in agent presets

Each preset bundles an agent with the engines/tools it needs [^src1]:

| Preset | Purpose | Example |
|---|---|---|
| `morning-digest-mac` | Morning briefing from calendar, email, and news | `jarvis init --preset morning-digest-mac` → `jarvis connect gdrive` → `jarvis digest --fresh` |
| `deep-research` | Web + local-document research with citations | `jarvis init --preset deep-research` → `jarvis memory index ./docs/` → `jarvis ask "..."` |
| `code-assistant` | Local coding agent that writes and runs Python | `jarvis init --preset code-assistant` |

## Related

- [[ai-engineering/ollama|Ollama]] — the local model-serving backend OpenJarvis runs on
- [[ai-engineering/local-ai-agents|Local AI Agents]] — the broader category of always-on, own-hardware agents
- [[ai-engineering/openclaw|OpenClaw]] — a comparable open-source local-agent framework, also Ollama-integrated
- [[ai-engineering/README|AI Engineering hub]]

---

[^src1]: [OpenJarvis: a local-first personal AI is now available to run with Ollama](../../raw/web/web-openjarvis-a-local-first-personal-ai-is-now-available-to-run-559ec7e6.md) — Ollama Blog, 2026-05-28

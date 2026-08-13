---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/notes/notes-03-resources-articles-uv-python-environment-package-manager.md
    channel: notes
    ingested_at: 2026-07-20
aliases: []
tags:
  - corpus/ai-engineering
  - source
  - doc-quick-intake
  - uv
  - python
  - package-management
  - developer-tools
created: 2026-07-20
updated: 2026-08-13
provisional: false
url: https://open.substack.com/pub/marvelousmlops/p/uv-all-the-way-your-go-to-python
origin: obsidian
---

# "UV: The Modern Go-To Python Environment and Package Manager"

**TL;DR**: `uv` consolidates `pip`, `venv`, `pyenv`, and `pip-tools` into a single fast CLI for Python project and environment management. One tool handles Python installation, virtualenv creation, dependency resolution, and lockfile generation.[^src]

[^src]: raw/notes/notes-03-resources-articles-uv-python-environment-package-manager.md

## What uv manages

`uv` owns the full local Python toolchain stack: project-specific virtualenvs (`.venv`) and all dependencies inside them.[^src] It replaces four separate tools that previously had to be composed manually.

| Replaced tool | Role taken over by uv |
|---|---|
| `pip` | Dependency installation |
| `venv` | Virtual environment creation |
| `pyenv` | Python version management |
| `pip-tools` | Dependency locking |

## Installation

- macOS: `brew install uv`
- Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`[^src]

## Core commands

### `uv init`

Scaffolds a new project with: `.git`, `.gitignore`, `.python-version`, `pyproject.toml`, `main.py`, `README.md`.[^src] Accepts `--name`, `--python`, and `--description` flags.

Best practice: create a named package subfolder (e.g., `alice/`) instead of keeping a top-level `main.py` — "prepares for multi-module growth."[^src]

### `uv sync`

"One command does everything — installs Python if needed, creates `.venv`, creates/updates `uv.lock`, installs/syncs dependencies."[^src] Should be run after every `pyproject.toml` change.

### `uv add <package>`

Adds a dependency, updates both `pyproject.toml` and `uv.lock`, and installs immediately.[^src]

### Virtual environment activation

`source .venv/bin/activate` — required in each new terminal session.[^src]

## Key files

**`pyproject.toml`**: The standard Python project config file (not uv-specific); `uv` reads and writes it for all dependency and metadata management.[^src]

**`uv.lock`**: Pins all dependency versions across the full transitive dependency tree — analogous to `package-lock.json` in Node.js.[^src]

## Related corpus pages

- [/ai-engineering/README.md](/ai-engineering/README.md)

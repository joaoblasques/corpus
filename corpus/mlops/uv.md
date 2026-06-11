---
type: entity
domain: mlops
status: stub
sources:
  - path: raw/notes/00-01-dev-environment-kb.md
    channel: notes
    ingested_at: 2026-06-09
aliases:
  - uv
  - uv pip
  - astral uv
tags:
  - corpus/mlops
  - entity
created: 2026-06-09
updated: 2026-06-09
---

# uv

**TL;DR**: A fast Python package manager and virtual-environment tool — the canonical Layer-2 choice in the [[mlops/dev-environment-stack|dev environment stack]] for installing AI/ML libraries into an isolated per-project environment [^src1].

## Role in the stack

uv occupies the **package-manager layer**: it creates virtual environments and installs Layer-4 libraries (PyTorch, NumPy, transformers) into them, replacing `pip` + `venv` for project dependency management [^src1].

## Gotchas

- **Don't mix `uv pip install` and `pip install` in the same venv** — mostly harmless but can produce surprising resolution differences. Pick one (uv) per project [^src1].
- **uv does not exempt you from venv activation** — `import` failures after a successful `uv pip install` are almost always an inactive/wrong venv (`which python` to confirm) [^src1].

> [unsourced — please verify] Broader uv capabilities (project/lockfile management via `uv.lock`, Python version management, tool installation) are not covered by the current source; this page reflects only its role as the course's package manager. Expand when a uv-primary source is ingested.

## See also

- [[mlops/dev-environment-stack|Dev Environment Stack]]
- [[mlops/README|MLOps hub]]

---

[^src1]: [AI Engineering from Scratch — Phase 00 / 01 Dev Environment](../../raw/notes/00-01-dev-environment-kb.md)

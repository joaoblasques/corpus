---
type: entity
domain: mlops
status: stub
sources:
  - path: raw/notes/00-01-dev-environment-kb.md
    channel: notes
    ingested_at: 2026-06-09
  - path: raw/email/email-2025-07-29-developing-on-databricks.md
    channel: email
    ingested_at: 2026-06-19
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

## In practice (Databricks MLOps course)

The Marvelous MLOps Databricks course uses uv for Python project management: dependencies are declared in `pyproject.toml` and the environment is built with `uv sync --extra dev`, which creates a `.venv` in the project folder [^src2]. It pins **exact versions** for all packages — intentional because the package is meant to be a *self-contained app*, not a reusable library (for reusable packages, locking too strictly causes resolution issues); the exact pins let the package override existing versions when installed inside a Databricks environment [^src2]. See [[mlops/databricks-development|Databricks Development]].

> [unsourced — please verify] Broader uv capabilities (project/lockfile management via `uv.lock`, Python version management, tool installation) are not covered by the current source; this page reflects only its role as the course's package manager. Expand when a uv-primary source is ingested.

## See also

- [[mlops/dev-environment-stack|Dev Environment Stack]]
- [[mlops/README|MLOps hub]]

---

[^src1]: [AI Engineering from Scratch — Phase 00 / 01 Dev Environment](../../raw/notes/00-01-dev-environment-kb.md)
[^src2]: [Developing on Databricks (Marvelous MLOps, Lecture 2)](../../raw/email/email-2025-07-29-developing-on-databricks.md)

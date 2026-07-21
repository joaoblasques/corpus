---
type: entity
domain: mlops
status: draft
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
updated: 2026-06-21
---

# uv

**TL;DR**: A fast Python package manager and virtual-environment tool — the canonical Layer-2 choice in the [four-layer dev environment stack](/mlops/dev-environment-stack.md) for installing AI/ML libraries into an isolated per-project environment [^src1]. It also drives Python project management in the Marvelous MLOps Databricks course, where dependencies live in `pyproject.toml` and the `.venv` is built with `uv sync` [^src2].

## Role in the stack

uv occupies the **package-manager layer** (Layer 2) of the dev-environment stack — alongside `pnpm` (Node) and `cargo` (Rust) — sitting above the system foundation and below the language runtimes and AI/ML libraries [^src1]. Its job is to create virtual environments and install Layer-4 libraries (PyTorch, NumPy, transformers) into them, replacing `pip` + `venv` for project dependency management [^src1].

Because the stack installs bottom-up — each layer depends on the one below it — and a virtual environment isolates Layer-4 libraries per project, uv is the tool that keeps project version conflicts contained instead of accumulating in a system-wide install [^src1].

## Usage

- **`uv pip install <pkg>`** — install a package into the active venv; later course lessons assume this command and the venv set up in Lesson 01 [^src1].
- **`uv sync --extra dev`** — build the project virtual environment (stored in `.venv` inside the project folder) from `pyproject.toml`, including the `dev` optional-dependency group [^src2].
- **`uv build`** — build the package locally into a wheel file; if the wheel is not ignored by `.gitignore`, it can be synced to the workspace and installed directly inside a Databricks notebook [^src2].

## Gotchas

- **Prefer `uv` + venv over `sudo pip`.** `sudo pip install` pollutes the system Python and can break OS-level tools — the source's guidance is blunt: *"Use `uv` with a virtual environment instead. Never `sudo pip`."* [^src1]
- **uv does not exempt you from venv activation.** An `import` failure after a successful `uv pip install` is almost always an inactive or wrong venv: the package installed into one venv while the shell uses another (or system Python). Run `which python` to confirm — when a venv is active it resolves to `.venv/bin/python` [^src1].
- **Don't mix `uv pip install` and `pip install` in the same venv.** Mostly harmless, but it can produce surprising resolution differences. Pick one (uv) per project [^src1].
- **A generic toolchain check may not cover uv.** The course's `verify.py` (at the documented commit) does not check for `uv` or `pnpm`, so a passing script means "some toolchain exists," not that uv specifically is installed [^src1].

## In practice — Databricks MLOps course

The Marvelous MLOps Databricks course (Lecture 2) standardizes on uv: *"we use uv for Python project management, and we highly recommend trying it out if you haven't already"* [^src2]. The Python version and project dependencies are declared in `pyproject.toml`, and `uv sync --extra dev` builds a `.venv` inside the project folder [^src2].

**Exact version pins, on purpose.** The `marvel-characters` `pyproject.toml` specifies exact versions for all packages (e.g. `mlflow==3.1.1`, `numpy==1.26.4`, `scikit-learn==1.7.0`) [^src2]. This is intentional *because the package is a self-contained app, not a reusable library* — for reusable packages, locking too strictly can cause dependency-resolution issues, but here the exact pins let the package override existing versions when installed inside a Databricks environment [^src2]. Optional-dependency groups separate concerns: `dev` (databricks-connect, ipykernel, pre-commit) and `ci` (pre-commit) [^src2].

**Version must match the runtime.** The project's Python version must match the target Databricks serverless environment: the course uses Python 3.12 (`requires-python = ">=3.12, <3.13"`), which matches serverless environment version 3 (Python 3.12.3) [^src2]. Notably the project overrides the environment's pre-installed package versions — e.g. MLflow 3.1.1 instead of the environment's 2.21.3 — which is exactly what the exact pins above enable [^src2].

See [Databricks Development](/mlops/databricks-development.md) for the surrounding local-development workflow (CLI, VS Code extension, serverless compute).

> [unsourced — scope note] Broader uv features not exercised by these two sources (lockfile management via `uv.lock`, standalone Python-version management, `uv tool` installs) are out of scope for this page. Expand when a uv-primary source is ingested.

## See also

- [Dev Environment Stack](/mlops/dev-environment-stack.md)
- [Databricks Development](/mlops/databricks-development.md)
- [MLOps hub](/mlops/README.md)

---

## Further sources (not yet expanded)

- [UV: The Modern Go-To Python Environment and Package Manager](/ai-engineering/sources/uv-the-modern-go-to-python-environment-and-package-manager-aae.md) — quick-intake stub; tutorial framing of uv as a replacement for pip, venv, pyenv, and pip-tools

[^src1]: [AI Engineering from Scratch — Phase 00 / 01 Dev Environment](../../raw/notes/00-01-dev-environment-kb.md)
[^src2]: [Developing on Databricks (Marvelous MLOps, Lecture 2)](../../raw/email/email-2025-07-29-developing-on-databricks.md)

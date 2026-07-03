---
type: concept
domain: mlops
status: draft
sources:
  - path: raw/notes/00-01-dev-environment-kb.md
    channel: notes
    ingested_at: 2026-06-09
aliases:
  - dev environment
  - development environment
  - four-layer stack
  - toolchain setup
tags:
  - corpus/mlops
  - concept
created: 2026-06-09
updated: 2026-06-09
---

# Dev Environment Stack

**TL;DR**: An AI/ML engineering environment is a **four-layer dependency stack** — System Foundation → Package Managers → Language Runtimes → AI/ML Libraries — installed **bottom-up** because each layer depends on the one below it. A virtual environment isolates the top layer per project so version conflicts stay contained instead of accumulating system-wide [^src1].

## The four layers

| Layer | Contents | Examples |
|---|---|---|
| 1 — System Foundation | OS, shell, git, GPU drivers | macOS/Linux, zsh, `git`, CUDA drivers |
| 2 — Package Managers | move dependencies around | [uv](/mlops/uv.md), pnpm, cargo |
| 3 — Language Runtimes | hold the structure | Python, Node, Rust, Julia |
| 4 — AI/ML Libraries | what you actually use | PyTorch, NumPy, transformers |

The building analogy from the source: foundation (OS + drivers), plumbing (package managers), framing (runtimes), interior (AI libraries) — you don't install the wallpaper before the drywall is up [^src1].

## Invariants

- **Stack ordering**: `Layer N` cannot function without `Layer N-1`. AI libs need a runtime; runtimes need a package manager; package managers need a working OS [^src1].
- **Venv invariant**: when a virtual environment is active, `which python` resolves to `.venv/bin/python`, not system Python. If it doesn't, the venv isn't active — that's the diagnostic [^src1].
- **GPU is optional**: `torch.cuda.is_available()` / `torch.backends.mps.is_available()` returning `False` is non-fatal for CPU-friendly work. GPU is a force multiplier, not a prerequisite [^src1]. See [GPU & VRAM](/mlops/gpu-and-vram.md).

## Verification pattern

The source's recommended pattern is **checks-as-data**: a list of `(name, check_fn, detail)` tuples driven by one dispatcher that prints PASS/FAIL and returns a bool, exiting non-zero if any required check fails [^src1]. Design choices worth carrying forward: checks-as-data makes the script extensible without touching the dispatcher; `__import__("foo")` tests library presence; optional checks live in a separate list so they don't gate the exit code [^src1].

## Common pitfalls

- **`sudo pip install`** pollutes system Python and can break OS-level tools → use [uv](/mlops/uv.md) with a virtual environment; never `sudo pip` [^src1].
- **"Install worked but `import` fails"** → almost always the venv isn't active (package went to venv A, shell uses venv B or system Python). Confirm with `which python` [^src1].
- **`python` vs `python3` on macOS** → modern macOS ships no `python` symlink; standardize on activating the venv (which provides `python`) [^src1].
- **Wrong CUDA index URL for PyTorch** → pip silently installs a CPU-only wheel despite a present GPU. Specify `--index-url https://download.pytorch.org/whl/cu124` (matching your CUDA) and verify with `torch.cuda.is_available()` immediately [^src1].

## Contrast

Managed environments (Colab, Lightning Studios, HF Spaces) skip Layers 1–3 by providing them; this stack is the "build it yourself locally" path, chosen for full control, reproducibility, and layer-by-layer debuggability [^src1]. See [Cloud GPU Providers](/mlops/cloud-gpu-providers.md) for the managed-compute side.

## See also

- [MLOps hub](/mlops/README.md)
- [Git](/mlops/git.md) — Layer 1 tooling; version control for the work built on this stack

---

[^src1]: [AI Engineering from Scratch — Phase 00 / 01 Dev Environment](../../raw/notes/00-01-dev-environment-kb.md)

---
type: hub
domain: mlops
status: draft
tags:
  - corpus/mlops
  - hub
created: 2026-06-09
updated: 2026-06-09
provisional: true
---

# MLOps

The engineering substrate for building ML and software systems: how the development environment is set up, how work is versioned, how compute is provisioned, and how infrastructure is declared and managed. Distinct from the content domains — `ai-engineering` (LLM internals, agents), `data-engineering` (ETL, modeling), and `software-engineering` (code design, application architecture) — this domain covers the layer *underneath* all of them: the tooling and infrastructure that the engineering work runs on.

> **Provisional domain** (created 2026-06-09). Seeded by the "AI Engineering from Scratch" course (Phase 00, setup-and-tooling) plus an IaC article. Expected to grow as later course phases (fine-tuning, data management, deployment) are ingested. 30-day review: 2026-07-09.

## Pages

### Entities
- [[mlops/uv|uv]] — entity · stub · fast Python package manager + virtual-environment tool; the canonical Layer-2 tool in the dev stack
- [[mlops/git|Git]] — entity · draft · content-addressed snapshot store; branch-per-task workflow, ML-aware `.gitignore`
- [[mlops/terraform|Terraform]] — entity · draft · HCL-based IaC tool; providers/resources, `.tfstate`, `.tfvars`, remote backends

### Concepts
- [[mlops/dev-environment-stack|Dev Environment Stack]] — concept · draft · four-layer dependency stack (OS → package managers → runtimes → AI libs); venv isolation; bottom-up install
- [[mlops/gpu-and-vram|GPU & VRAM]] — concept · draft · why GPUs win for ML, VRAM as the hard ceiling, fp16 rule of thumb, training ≈ 6× inference, LoRA
- [[mlops/cloud-gpu-providers|Cloud GPU Providers]] — concept · draft · Colab / RunPod / Lambda / Vast.ai comparison; when to use each
- [[mlops/infrastructure-as-code|Infrastructure as Code]] — concept · draft · declarative infra management; desired-state vs current-state reconciliation; "git for infrastructure"

## Sources ingested
- [AI Engineering from Scratch — Phase 00 / 01 Dev Environment](../../raw/notes/00-01-dev-environment-kb.md) — first-party course note, 2026-05-25
- [AI Engineering from Scratch — Phase 00 / 02 Git & Collaboration](../../raw/notes/00-02-git-and-collaboration-kb.md) — first-party course note, 2026-05-27
- [AI Engineering from Scratch — Phase 00 / 03 GPU Setup & Cloud](../../raw/notes/00-03-gpu-setup-and-cloud-kb.md) — first-party course note, 2026-05-27
- [IaC fundamentals for data engineers](<../../raw/web/IaC (Infrastructure-as-Code) fundamentals for data engineers.md>) — startdataengineering.com (Joseph Machado), 2026-05-27

## See also

- [[software-engineering/README|Software Engineering]] — code design, distributed systems, container orchestration (Kubernetes); the application layer above this substrate
- [[ai-engineering/README|AI Engineering]] — the ML/LLM work the GPU and environment tooling here exists to support
- [[data-engineering/README|Data Engineering]] — IaC here provisions the cloud data infrastructure (S3, EC2/EMR) those pipelines run on

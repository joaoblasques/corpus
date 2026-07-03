---
type: hub
domain: mlops
status: draft
tags:
  - corpus/mlops
  - hub
created: 2026-06-09
updated: 2026-06-25
provisional: true

---

# MLOps

The engineering substrate for building ML and software systems: how the development environment is set up, how work is versioned, how compute is provisioned, and how infrastructure is declared and managed. Distinct from the content domains — `ai-engineering` (LLM internals, agents), `data-engineering` (ETL, modeling), and `software-engineering` (code design, application architecture) — this domain covers the layer *underneath* all of them: the tooling and infrastructure that the engineering work runs on.

> **Provisional domain** (created 2026-06-09). Seeded by the "AI Engineering from Scratch" course (Phase 00, setup-and-tooling) plus an IaC article. Expected to grow as later course phases (fine-tuning, data management, deployment) are ingested. 30-day review: 2026-07-09.

## Pages

### Entities
- [uv](/mlops/uv.md) — entity · stub · fast Python package manager + virtual-environment tool; the canonical Layer-2 tool in the dev stack
- [Git](/mlops/git.md) — entity · draft · content-addressed snapshot store; branch-per-task workflow, ML-aware `.gitignore`; branching strategies (GitHub Flow, Git Flow); perfect commit; GitHub concepts (fork/star/PR/SSH key)
- [Terraform](/mlops/terraform.md) — entity · draft · HCL-based IaC tool; providers/resources, `.tfstate`, `.tfvars`, remote backends
- [VS Code](/mlops/vs-code.md) — entity · draft · Microsoft code editor; folder-as-project, panels, integrated terminal, command palette, extensions
- [MLflow](/mlops/mlflow.md) — entity · draft · experiment tracking + model registry; runs/experiments, MLflow 3 LoggedModel, flavors/signature, UC registration, pyfunc wrapper
- [AWS](/mlops/aws.md) — entity · draft · largest cloud provider; core service map + Cloud Practitioner/Solutions Architect learning path
- [Azure](/mlops/azure.md) — entity · draft · 2nd cloud provider; service map, resource hierarchy, AZ-900 fundamentals
- [GCP](/mlops/gcp.md) — entity · draft · Google cloud; Compute Engine/GKE/BigQuery, org→folder→project hierarchy
- [Terax](/mlops/terax.md) — entity · stub · open-source AI-native terminal (Tauri 2 + Rust); 7 MB, <300 ms start, built-in agent with reviewable diffs
- [Herder](/mlops/herder.md) — entity · draft · modern tmux-style multiplexer; session-vs-process-state snapshots, built-in agent-awareness (working/idle/blocked/done), thin-client remote mode, Herda Plus plugin
- [Made With ML](/mlops/made-with-ml.md) — entity · stub · GokuMohandas/Made-With-ML; 48k-star production ML course (design → deploy → iterate); PyTorch + Ray
- [Hands-On ML (3rd Edition)](/mlops/handson-ml3.md) — entity · stub · Aurélien Géron / ageron/handson-ml3; 13k-star companion to O'Reilly book; Scikit-Learn + Keras + TF2
- [100 Days of ML Code](/mlops/100-days-of-ml-code.md) — entity · stub · Avik-Jain; 51k-star infographic ML algorithm challenge; data-preprocessing through SVM + deep learning
- [Ampernetacle](/mlops/ampernetacle.md) — entity · stub · Terraform config for 4-node ARM Kubernetes cluster on OCI free tier; jpetazzo
- [Tilt](/mlops/tilt.md) — entity · stub · dev-loop automation for Kubernetes microservices; `tilt up` replaces manual `docker build && kubectl apply`
- [Designing Machine Learning Systems](/mlops/designing-ml-systems.md) — entity · draft · Chip Huyen's O'Reilly book (2022); holistic ML systems design: data, training, deployment, monitoring, infrastructure (Ch 1–11)

### Concepts
- [MLOps Principles](/mlops/mlops-principles.md) — concept · draft · what MLOps is (reliable+efficient production); traceability/reproducibility core principle, tooling-by-category, MLOps vs DevOps (the data difference), DevOps loop, concepts-over-tools principle
- [Dev Environment Stack](/mlops/dev-environment-stack.md) — concept · draft · four-layer dependency stack (OS → package managers → runtimes → AI libs); venv isolation; bottom-up install
- [GPU & VRAM](/mlops/gpu-and-vram.md) — concept · draft · why GPUs win for ML, VRAM as the hard ceiling, fp16 rule of thumb, training ≈ 6× inference, LoRA
- [Cloud GPU Providers](/mlops/cloud-gpu-providers.md) — concept · draft · Colab / RunPod / Lambda / Vast.ai comparison; when to use each
- [Infrastructure as Code](/mlops/infrastructure-as-code.md) — concept · draft · declarative infra management; desired-state vs current-state reconciliation; CloudFormation/CDK/ARM
- [Cloud Computing Fundamentals](/mlops/cloud-computing-fundamentals.md) — concept · draft · provider-agnostic concepts: scaling, load balancing, serverless, IaaS/PaaS/SaaS, availability/durability, EDA
- [CLI Tools](/mlops/cli-tools.md) — concept · draft · modern terminal tools (zoxide, ripgrep, fd, bat, eza, fzf, tmux, jq, gh, pass)
- [Terminal & Shell](/mlops/terminal-and-shell.md) — concept · draft · Alacritty/iTerm2/WezTerm, zsh, Powerlevel10k, nerd fonts, Zinit-based config; zsh plugins; macOS terminal tips; AI-native terminals (Terax, Warp)
- [tmux](/mlops/tmux.md) — concept · draft · terminal multiplexer; sessions/windows/panes; persistent VPS-based agent sessions; multi-agent pane workflows; cron scheduling via codex exec
- [VPS for Agents](/mlops/vps-for-agents.md) — concept · draft · running Codex/Claude Code on an always-on VPS; Hostinger KVM2, device-code auth, phone control via Termius, cron automations; scorched-earth security (Tailscale + Cloudflare Tunnel + UFW)
- [Linux Commands](/mlops/linux-commands.md) — concept · draft · the 20% of Linux commands for 80% of work; navigation, pipes, grep, file permissions, vim
- [Linux Filesystem Structure](/mlops/linux-filesystem.md) — concept · draft · the FHS directory tree (/, /bin, /etc, /var, /proc, /usr); virtual vs real directories; DevOps-relevant config locations
- [Cron Scheduling](/mlops/cron-scheduling.md) — concept · draft · crontab syntax (5-field time spec, env vars, step/range/list notation), cron vs Airflow vs K8s CronJob, Windows Task Scheduler reference
- [Networking Fundamentals](/mlops/networking-fundamentals.md) — concept · draft · containers, 4 DevOps networking layers, Headscale/WireGuard mesh VPN
- [Python](/mlops/python.md) — concept · draft · general-purpose Python language reference: data types, type annotations, functions, classes, dunder methods
- [Python Built-in Functions](/mlops/python-built-in-functions.md) — concept · draft · the `builtins` scope catalog: math, type construction, collections, iterables (map/filter/zip/enumerate), I/O, OOP/introspection
- [Drift Detection](/mlops/drift-detection.md) — concept · draft · model-monitoring: reference vs. analysis samples; univariate drift metrics (JS, Wasserstein, Hellinger, L-Infinity, KS, Chi-2) and their tradeoffs
- [Model Serving](/mlops/model-serving.md) — concept · draft · real-time inference (Flask `/predict` API) vs batch inference (Airflow DAG) vs Databricks Model Serving (serverless REST, 3 architectures, A/B sticky assignment); shared preprocessing + saved pipeline
- [Databricks Development](/mlops/databricks-development.md) — concept · draft · local-first Databricks dev: CLI auth, VS Code extension, Databricks Connect, serverless env versions, uv, pydantic ProjectConfig
- [Databricks Asset Bundles](/mlops/databricks-asset-bundles.md) — concept · draft · declarative YAML packaging of code/jobs/deps (wraps Terraform); databricks.yml, Lakeflow Jobs, task dependencies, bundle CLI
- [CI/CD for ML](/mlops/ci-cd-for-ml.md) — concept · draft · Unity Catalog 3-tier hierarchy + access modes, Service Principals, Git Flow + branch protection, GitHub Actions CI/CD matrix
- [Model Monitoring](/mlops/model-monitoring.md) — concept · draft · why ML monitoring differs; data vs concept drift; Databricks Lakehouse Monitoring (profile/drift tables, inference tables); implementation pipeline
- [Production ML Workflow](/mlops/production-ml-workflow.md) — concept · draft · production-minded training (Practical ML Series Pt 2): holdout set, robust preprocessing, model comparison, business-metric optimization, sklearn pipeline serialization

### Syntheses
- [Environment Promotion (dev → acc → prd)](/mlops/environment-promotion.md) — synthesis · draft · the cross-source deployment discipline (ML CI/CD + data-infra CI/CD + DAB): humans only in dev, env-scoped state, CI-check → human-gated prod apply, machine identity
- [DevOps Learning Roadmap](/mlops/devops-learning-roadmap.md) — synthesis · draft · TWN 10-step canonical path + 26-week schedule; KubeCraft roadmap; 8 common learning mistakes (Nana); concepts-over-tools principle; Linux-first argument

## Sources ingested
- [AI Engineering from Scratch — Phase 00 / 01 Dev Environment](../../raw/notes/00-01-dev-environment-kb.md) — first-party course note, 2026-05-25
- [AI Engineering from Scratch — Phase 00 / 02 Git & Collaboration](../../raw/notes/00-02-git-and-collaboration-kb.md) — first-party course note, 2026-05-27
- [AI Engineering from Scratch — Phase 00 / 03 GPU Setup & Cloud](../../raw/notes/00-03-gpu-setup-and-cloud-kb.md) — first-party course note, 2026-05-27
- [IaC fundamentals for data engineers](<../../raw/web/IaC (Infrastructure-as-Code) fundamentals for data engineers.md>) — startdataengineering.com (Joseph Machado), 2026-05-27
- YouTube cloud-cert cluster (2026-06-15): AWS services + AWS learning roadmap; Azure AZ-900 (×2) + Intellipaat Azure; GCP full course; cloud-computing fundamentals
- YouTube dev-setup cluster (2026-06-15): 3× CLI-tools videos; Alacritty + Mac terminal setup (×2); zsh hacks; VS Code tutorial; Linux commands; Python concepts
- [Introduction to MLOps (Marvelous MLOps)](../../raw/email/email-2025-07-28-introduction-to-mlops.md) — course lecture 1; MLOps principles & tooling categories, 2026-06-19
- GitHub repos cluster (2026-06-25): handson-ml3 (Aurélien Géron), 100-Days-Of-ML-Code (Avik Jain), Made-With-ML (GokuMohandas), Ampernetacle (jpetazzo), Tilt (tilt-dev)
- Notes/PDFs cluster (2026-06-25): Build Anything with Tmux; I Gave Codex a 24/7 Server; Terax AI Terminal; DevOps from Zero to Hero; I Wasted 2 Years Learning DevOps Wrong; TWN DevOps Roadmap PDF; TWN Weekly Learning Schedule PDF; I Lost 2 Years and $300K to the Wrong Roadmap (email)
- YouTube + web cluster (2026-06-25): This Zsh Config (Dreams of Autonomy); 50 macOS Tips (NetworkChuck); Terax YouTube (Better Stack); Git for Professionals (Tobias Günther / freeCodeCamp); Only GitHub Guide (corbin); Secure a VPS in 2026 (Dreams of Code); DevOps Zero to Hero (JavaScript Mastery); I Wasted 2 Years DevOps (Nana/TWN); Linux Filesystem (WhiteboardDoodles); Build Anything with Tmux YouTube (David Ondrej); crontab(5) Linux manual; Windows Task Scheduler docs; Designing Machine Learning Systems (Chip Huyen, O'Reilly PDF)
- [The New Age of Modern Terminal Multiplexer Herder](../../raw/youtube/youtube-27B50lXinWM-the-new-age-of-modern-terminal-multiplexer-herdr.md) — Seth Phaeno, YouTube (Dev setup), 2026-06-26 → new entity [Herder](/mlops/herder.md) + tmux comparison

## See also

- [Software Engineering](/software-engineering/README.md) — code design, distributed systems, container orchestration (Kubernetes); the application layer above this substrate
- [AI Engineering](/ai-engineering/README.md) — the ML/LLM work the GPU and environment tooling here exists to support
- [Data Engineering](/data-engineering/README.md) — IaC here provisions the cloud data infrastructure (S3, EC2/EMR) those pipelines run on

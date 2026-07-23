---
type: hub
domain: mlops
status: draft
tags:
  - corpus/mlops
  - hub
created: 2026-06-09
updated: 2026-07-22
provisional: false

---

# MLOps

The engineering substrate for building ML and software systems: how the development environment is set up, how work is versioned, how compute is provisioned, and how infrastructure is declared and managed. Distinct from the content domains — `ai-engineering` (LLM internals, agents), `data-engineering` (ETL, modeling), and `software-engineering` (code design, application architecture) — this domain covers the layer *underneath* all of them: the tooling and infrastructure that the engineering work runs on.

> Graduated 2026-07-22. Seeded by the "AI Engineering from Scratch" course (Phase 00, setup-and-tooling) plus an IaC article; grown to 41 pages across email/github/notes/pdf/web/youtube channels.

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
- [Practitioners Guide to MLOps (Google, May 2021)](sources/practitioners-guide-to-mlops.md) — Khalid Salama, Jarek Kazmierczak, Donna Schut; 37-page whitepaper defining the MLOps lifecycle (7 phases), 11 core capabilities, and 6 process deep-dives; 2026-07-23
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

<!-- AUTO-INDEX:START (generated by bin/corpus_heal.py hubs — do not edit inside) -->

## Pages in this domain

### Concepts (23)
- [CI/CD for ML (on Databricks)](/mlops/ci-cd-for-ml.md)
- [CLI Tools](/mlops/cli-tools.md)
- [Cloud Computing Fundamentals](/mlops/cloud-computing-fundamentals.md)
- [Cloud GPU Providers](/mlops/cloud-gpu-providers.md)
- [Cron Scheduling](/mlops/cron-scheduling.md)
- [Databricks Asset Bundles (DAB)](/mlops/databricks-asset-bundles.md)
- [Databricks Development (Local-First)](/mlops/databricks-development.md)
- [Dev Environment Stack](/mlops/dev-environment-stack.md)
- [Drift Detection](/mlops/drift-detection.md)
- [GPU & VRAM](/mlops/gpu-and-vram.md)
- [Infrastructure as Code](/mlops/infrastructure-as-code.md)
- [Linux Commands](/mlops/linux-commands.md)
- [Linux Filesystem Structure](/mlops/linux-filesystem.md)
- [MLOps Principles](/mlops/mlops-principles.md)
- [Model Monitoring](/mlops/model-monitoring.md)
- [Model Serving (Real-Time API + Batch Inference)](/mlops/model-serving.md)
- [Networking Fundamentals (for DevOps/MLOps)](/mlops/networking-fundamentals.md)
- [Production-Minded ML Training Workflow](/mlops/production-ml-workflow.md)
- [Python](/mlops/python.md)
- [Python Built-in Functions](/mlops/python-built-in-functions.md)
- [Terminal & Shell](/mlops/terminal-and-shell.md)
- [tmux](/mlops/tmux.md)
- [VPS for Agents](/mlops/vps-for-agents.md)

### Entities (16)
- [100 Days of ML Code](/mlops/100-days-of-ml-code.md)
- [Ampernetacle](/mlops/ampernetacle.md)
- [AWS](/mlops/aws.md)
- [Azure](/mlops/azure.md)
- [Designing Machine Learning Systems](/mlops/designing-ml-systems.md)
- [GCP](/mlops/gcp.md)
- [Git](/mlops/git.md)
- [Hands-On Machine Learning (3rd Edition)](/mlops/handson-ml3.md)
- [Herder](/mlops/herder.md)
- [Made With ML](/mlops/made-with-ml.md)
- [MLflow](/mlops/mlflow.md)
- [Terax](/mlops/terax.md)
- [Terraform](/mlops/terraform.md)
- [Tilt](/mlops/tilt.md)
- [uv](/mlops/uv.md)
- [VS Code](/mlops/vs-code.md)

### Syntheses (2)
- [DevOps Learning Roadmap](/mlops/devops-learning-roadmap.md)
- [Environment Promotion (dev → acc → prd)](/mlops/environment-promotion.md)

<details>
<summary>Source summaries (103)</summary>

- ["29%+ warehouse savings: How the dbt Fusion engine drives cost efficiency | dbt Labs"](/mlops/sources/29-warehouse-savings-how-the-dbt-fusion-engine-drives-cost-e-121b247d.md)
- ["AL 005: 60% Growth in 60 Days? How?!"](/mlops/sources/al-005-60-growth-in-60-days-how-150a587c.md)
- ["Alternative data for hedge funds: from web to signals"](/mlops/sources/alternative-data-for-hedge-funds-from-web-to-signals-3f1968e5.md)
- ["Announcing the Monetization Gateway: charge for any resource behind Cloudflare via x402"](/mlops/sources/announcing-the-monetization-gateway-charge-for-any-resource--88fda6db.md)
- ["Artifacts: versioned storage that speaks Git"](/mlops/sources/artifacts-versioned-storage-that-speaks-git-882e9a38.md)
- ["Ask, build, compose: What our 5th Genie Hackathon taught us about Databricks Genie"](/mlops/sources/ask-build-compose-what-our-5th-genie-hackathon-taught-us-abo-733b3260.md)
- ["Automatic Upgrades: best practice features for your lakehouse tables"](/mlops/sources/automatic-upgrades-best-practice-features-for-your-lakehouse-afb2599c.md)
- ["Automating Cisco Webex Sprint Meetings with Zenflow: Enterprise Integration Guide"](/mlops/sources/automating-cisco-webex-sprint-meetings-with-zenflow-enterpri-3546511b.md)
- ["Automating the impossible: migrating 40,000+ objects to dbt in 9 months | dbt Summit"](/mlops/sources/automating-the-impossible-migrating-40-000-objects-to-dbt-in-b213f86c.md)
- ["Benchmarking Vortex File Format ... vs Parquet, CSV ... vs DuckDB, Polars, Datafusion."](/mlops/sources/benchmarking-vortex-file-format-vs-parquet-csv-vs-duckdb-pol-d8c981f0.md)
- ["Beyond dashboards: Introducing Decision Execution Platforms"](/mlops/sources/beyond-dashboards-introducing-decision-execution-platforms-53e3b67a.md)
- ["Beyond Enterprise Data Lineage: The Case for a Platform-Independent Data Catalog"](/mlops/sources/beyond-enterprise-data-lineage-the-case-for-a-platform-indep-ebac959b.md)
- ["Building in Public: Risks and Strategies for Founders"](/mlops/sources/building-in-public-risks-and-strategies-for-founders-d331a11a.md)
- ["Choosing an ERP for Manufacturing: How AI Is Reshaping the Vendor Landscape"](/mlops/sources/choosing-an-erp-for-manufacturing-how-ai-is-reshaping-the-ve-9e4f1daf.md)
- ["CI/CD Databricks ETLs: Automate Testing in Isolated Environments"](/mlops/sources/ci-cd-databricks-etls-automate-testing-in-isolated-environme-8001aeb0.md)
- ["claude-sonnet-4-6 vs gpt-5.2: Benchmarks, Pricing & Context Window | Requesty"](/mlops/sources/claude-sonnet-4-6-vs-gpt-5-2-benchmarks-pricing-context-wind-b1a3fd7b.md)
- ["Code is the Canvas: Bring the Whole Team to It"](/mlops/sources/code-is-the-canvas-bring-the-whole-team-to-it-4d506fa4.md)
- ["CytoReason: Smarter Data Pipelines with Nextflow & lakeFS"](/mlops/sources/cytoreason-smarter-data-pipelines-with-nextflow-lakefs-a44471df.md)
- ["Data Projects: Managing Data Assets at Netflix Scale"](/mlops/sources/data-projects-managing-data-assets-at-netflix-scale-4da3ecae.md)
- ["Databricks Zerobus: Event Streams + The Lakehouse - Confessions of a Data Guy"](/mlops/sources/databricks-zerobus-event-streams-the-lakehouse-confessions-o-01431550.md)
- ["Metadata Management — Architecture, Patterns, and Operational Playbook"](/mlops/sources/metadata-management-architecture-patterns-and-operational-pl-eace.md)
- ["Stop Thinking in Salaries: Build Systems That Pay You for Life | Best Audiobooks"](/mlops/sources/stop-thinking-in-salaries-build-systems-that-pay-you-for-lif-JAN3fFcDG8Y.md)
- ["The Mom Who Mastered Claude: How To Build An Audience That Buys Using Claude Code (Step by Step!)"](/mlops/sources/the-mom-who-mastered-claude-how-to-build-an-audience-that-bu-DnZ53NQXfuA.md)
- ["Web Scraping 101: A Million Dollar Project Idea"](/mlops/sources/web-scraping-101-a-million-dollar-project-idea-DJnH0jR8y5Q.md)
- [100% REMOTE Boring Businesses (That Almost Never Fail)](/mlops/sources/100-remote-boring-businesses-that-almost-never-fail-EnSJN9zl-yA.md)
- [5 powerful scrapers to add to your SEO tool kit](/mlops/sources/5-powerful-scrapers-to-add-to-your-seo-tool-kit-906d6a15.md)
- [5% ownership is probably the most common final stake for VC funded startup founders — @levelsio (Pieter Levels)](/mlops/sources/5-ownership-is-probably-the-most-common-final-stake-for-vc-f-73fd6897.md)
- [A broken DNSSEC rollover took down .AL. Now 1.1.1.1 tells you when validation is bypassed](/mlops/sources/a-broken-dnssec-rollover-took-down-al-now-1-1-1-1-tells-you--a9e7f215.md)
- [A Catalog Is All You Need](/mlops/sources/a-catalog-is-all-you-need-1015a427.md)
- [A Decision Framework for ETL Migration to Databricks](/mlops/sources/a-decision-framework-for-etl-migration-to-databricks-9db6e9d6.md)
- [a-novel-approach-to-trading-strategy-parameter-optimization](/mlops/sources/a-novel-approach-to-trading-strategy-parameter-optimization-a.md)
- [About MetricFlow | dbt Developer Hub](/mlops/sources/about-metricflow-dbt-developer-hub-b.md)
- [about-dbt-wizard-in-the-dbt-platform-previewstarterenterpris](/mlops/sources/about-dbt-wizard-in-the-dbt-platform-previewstarterenterpris-eeaeee.md)
- [Activities - Kai Waehner](/mlops/sources/activities-kai-waehner-0cf0b10c.md)
- [ADBC?](/mlops/sources/adbc-b0c21ff6.md)
- [Add Git-Like Data Versioning to MATLAB with lakeFS](/mlops/sources/add-git-like-data-versioning-to-matlab-with-lakefs-8ae9afe5.md)
- [Add snapshots to your DAG | dbt Developer Hub](/mlops/sources/add-snapshots-to-your-dag-dbt-developer-hub-b.md)
- [Agent Bricks and the Commoditization of AI Systems - Confessions of a Data Guy](/mlops/sources/agent-bricks-and-the-commoditization-of-ai-systems-confessio-4ec6fbca.md)
- [Agentic Data Engineering Is Here — But Can It Close the Loop?](/mlops/sources/agentic-data-engineering-is-here-but-can-it-close-the-loop-b94b0b55.md)
- [AI agent versioned filesystem with E2B and lakeFS](/mlops/sources/ai-agent-versioned-filesystem-with-e2b-and-lakefs-5b56487a.md)
- [AI Sped Up Coding Faster Than It Sped Up Delivery](/mlops/sources/ai-sped-up-coding-faster-than-it-sped-up-delivery-b8e50c89.md)
- [Apache Iceberg and the catalog layer (w/ Russell Spitzer)](/mlops/sources/apache-iceberg-and-the-catalog-layer-w-russell-spitzer-b1237b12.md)
- [Automating cross-repo documentation with GitHub Agentic Workflows](/mlops/sources/automating-cross-repo-documentation-with-github-agentic-work-7eb481ee.md)
- [Best LinkedIn scrapers for sales and marketing teams](/mlops/sources/best-linkedin-scrapers-for-sales-and-marketing-teams-f3159d29.md)
- [BI’s Second Unbundling](/mlops/sources/bi-s-second-unbundling-2274b40d.md)
- [Book a Demo and See lakeFS in Action](/mlops/sources/book-a-demo-and-see-lakefs-in-action-18b22a81.md)
- [Breaking Down the Obsidian CEO’s Personal Vault System](/mlops/sources/breaking-down-the-obsidian-ceo-s-personal-vault-system-0Wbw1e7wNK0.md)
- [build superfans](/mlops/sources/build-superfans-543df40f.md)
- [Building a data stack for trusted AI | dbt Labs](/mlops/sources/building-a-data-stack-for-trusted-ai-dbt-labs-408a3692.md)
- [Building a multilingual medicine safety Actor on Apify](/mlops/sources/building-a-multilingual-medicine-safety-actor-on-apify-60944a1f.md)
- [Building a We Work Remotely scraper on Apify](/mlops/sources/building-a-we-work-remotely-scraper-on-apify-5a48ae0c.md)
- [Building Without the Handoffs](/mlops/sources/building-without-the-handoffs-5d9dbfe1.md)
- [building-a-modern-clinical-health-data-lake-with-delta-lake](/mlops/sources/building-a-modern-clinical-health-data-lake-with-delta-lake-ae.md)
- [Claude AI Can Automatically Build and Improve Your Trading Systems](/mlops/sources/claude-ai-can-automatically-build-and-improve-your-trading-s-e.md)
- [Claude Code - Building a Profitable Online Directory](/mlops/sources/claude-code-building-a-profitable-online-directory-dec.md)
- [Claude Code - MCP Stack Setup Playwright Docker GitHub](/mlops/sources/claude-code-mcp-stack-setup-playwright-docker-github-b.md)
- [Claude Code built me a $273/Day online directory](/mlops/sources/claude-code-built-me-a-273-day-online-directory-I_wbc5ND79o.md)
- [Claude Code Second Brain — Managing Life in Obsidian](/mlops/sources/claude-code-second-brain-managing-life-in-obsidian-bda.md)
- [Claude Will Change Trading Forever (Here's How To Prepare)](/mlops/sources/claude-will-change-trading-forever-here-s-how-to-prepare-G7zv25c7Z8M.md)
- [ClickHouse + Fusion Preview | dbt Labs](/mlops/sources/clickhouse-fusion-preview-dbt-labs-35ff478a.md)
- [Crypto Trading Bot Masterclass 2026 — Architecture and Risk Guide](/mlops/sources/crypto-trading-bot-masterclass-2026-architecture-and-risk-gu-2026.md)
- [Dashboards and Queries for Apache Kafka](/mlops/sources/dashboards-and-queries-for-apache-kafka-203641b9.md)
- [Databricks positioned highest in execution and furthest in vision for the second consecutive year in Gartner Magic Quadrant](/mlops/sources/databricks-positioned-highest-in-execution-and-furthest-in-v-cca3c0df.md)
- [DevOps - DevSecOps CI Pipeline with GitHub Actions](/mlops/sources/devops-devsecops-ci-pipeline-with-github-actions-ac.md)
- [DevOps - Docker Model Runner for Local LLMs](/mlops/sources/devops-docker-model-runner-for-local-llms-doc.md)
- [DevOps - How AI Is Changing DevOps Careers](/mlops/sources/devops-how-ai-is-changing-devops-careers-caee.md)
- [Easily Make Money Selling Digital Products on Etsy (2023)](/mlops/sources/easily-make-money-selling-digital-products-on-etsy-2023-E0qSPO2kdmg.md)
- [feature-store-the-definitive-guide-mlops-dictionary](/mlops/sources/feature-store-the-definitive-guide-mlops-dictionary-dca.md)
- [Fintech Engineering Handbook](/mlops/sources/fintech-engineering-handbook-adb.md)
- [healthcare-data-standards-explained-snomed-to-cpt](/mlops/sources/healthcare-data-standards-explained-snomed-to-cpt-c.md)
- [helix-retrospective](/mlops/sources/helix-retrospective-eece.md)
- [How Claude Code’s Creator Starts EVERY Project](/mlops/sources/how-claude-code-s-creator-starts-every-project-KWrsLqnB6vA.md)
- [How I Built My Own AI Trading Assistant Using Claude Cowork](/mlops/sources/how-i-built-my-own-ai-trading-assistant-using-claude-cowork-GlkJMO_ufYA.md)
- [How To Actually Use Claude Code for Trading Strategies (Like a Quant)](/mlops/sources/how-to-actually-use-claude-code-for-trading-strategies-like--EUSXhJNwRqI.md)
- [How To Automate TradingView Strategies WITHOUT CODING! (New & Best Method)](/mlops/sources/how-to-automate-tradingview-strategies-without-coding-new-be-UQqt1Sr-FH0.md)
- [How To Create A Personal Zero Human Trading Firm](/mlops/sources/how-to-create-a-personal-zero-human-trading-firm-T6jdfZ317Vw.md)
- [I Built an AI Trading System With Claude + TradingView](/mlops/sources/i-built-an-ai-trading-system-with-claude-tradingview-IqvnryFzZD4.md)
- [I Found Where AI Agents Are Beating Humans on Polymarket (perfect for OpenClaw)](/mlops/sources/i-found-where-ai-agents-are-beating-humans-on-polymarket-per-Kz3kZOTd_tI.md)
- [I Wish Someone Had Explained Cowork Like This Earlier (in under 10 min)](/mlops/sources/i-wish-someone-had-explained-cowork-like-this-earlier-in-und-IBI8DecuFyg.md)
- [Make your AI better at data work with dbt's agent skills](/mlops/sources/make-your-ai-better-at-data-work-with-dbt-s-agent-skills-eca.md)
- [Manage budgets and cost controls for Genie](/mlops/sources/manage-budgets-and-cost-controls-for-genie-ee.md)
- [mbta-on-time-lakehouse-retrospective](/mlops/sources/mbta-on-time-lakehouse-retrospective-eece.md)
- [MetadataOps — How Data Engineers Are Adapting to Serve AI Consumers](/mlops/sources/metadataops-how-data-engineers-are-adapting-to-serve-ai-cons-f.md)
- [Monitoring Lakeflow Jobs Cost and Performance with System Tables](/mlops/sources/monitoring-lakeflow-jobs-cost-and-performance-with-system-ta-abe.md)
- [NotebookLM + Obsidian Integration Workflow](/mlops/sources/notebooklm-obsidian-integration-workflow-f.md)
- [OpenClaw 2.0 is here.](/mlops/sources/openclaw-2-0-is-here-6vPaitNQMGY.md)
- [Practitioners Guide to MLOps (Google, 2021)](/mlops/sources/practitioners-guide-to-mlops.md)
- [Proactive Alignment — How Data Teams Avoid Being Blindsided by Surprise Projects](/mlops/sources/proactive-alignment-how-data-teams-avoid-being-blindsided-by-ec.md)
- [Seedance 2.0 + Claude Code Creates $10k Websites in Minutes](/mlops/sources/seedance-2-0-claude-code-creates-10k-websites-in-minutes-NvxiSG34mPU.md)
- [Sell Your API to AI Agents & Make SERIOUS Money in 2026 (full guide / beginner friendly)](/mlops/sources/sell-your-api-to-ai-agents-make-serious-money-in-2026-full-g-GyijriMIKPA.md)
- [Silent Data Loss Detection — Pipeline Volume Anomaly Monitoring with BigQuery and AI](/mlops/sources/silent-data-loss-detection-pipeline-volume-anomaly-monitorin-be.md)
- [systematic-trend-following-with-adaptive-portfolio-construct](/mlops/sources/systematic-trend-following-with-adaptive-portfolio-construct-cc.md)
- [TerraForm - WPP](/mlops/sources/terraform-wpp-doc.md)
- [Terraform Interview Cheat Sheet](/mlops/sources/terraform-interview-cheat-sheet-ee.md)
- [terraform_cheatsheet](/mlops/sources/terraform-cheatsheet-ceaee.md)
- [The Easiest $3K/Day Business — Photo Magnets](/mlops/sources/the-easiest-3k-day-business-photo-magnets-da.md)
- [The Four Step Process to Loop Engineer ANYTHING (+ Why Prompt Engineering Isn't Dead)](/mlops/sources/the-four-step-process-to-loop-engineer-anything-why-prompt-e-JirDfgJcJFU.md)
- [The Most Passive Online Side Hustle I've Ever Seen](/mlops/sources/the-most-passive-online-side-hustle-i-ve-ever-seen-Wl0NMNbYRDk.md)
- [This Underrated Tool Replaced 3 Homelab Services (and it's open source!)](/mlops/sources/this-underrated-tool-replaced-3-homelab-services-and-it-s-op-3wJ0IQ3rHjA.md)
- [This Will Blow Up Your Etsy Store.. (How To Sell Midjourney Art On Etsy)](/mlops/sources/this-will-blow-up-your-etsy-store-how-to-sell-midjourney-art-IokqNEjKKPY.md)
- [Trading - HMM Regime-Based Strategy with Claude Code](/mlops/sources/trading-hmm-regime-based-strategy-with-claude-code-cde.md)
- [Turn Famous Songs into Cash with Suno AI Remixes LEGALLY!](/mlops/sources/turn-famous-songs-into-cash-with-suno-ai-remixes-legally-M9EgmsugWXk.md)
- [Using OpenClaw for Automated Trading](/mlops/sources/using-openclaw-for-automated-trading-ad.md)

</details>

<!-- AUTO-INDEX:END -->

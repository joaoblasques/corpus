---
type: synthesis
domain: mlops
status: draft
sources:
  - path: raw/pdf/pdf-1-devops-roadmap-by-techworld-with-nana.md
    channel: pdf
    ingested_at: 2026-06-25
  - path: raw/pdf/pdf-2-weekly-learning-schedule-by-techworld-with-nana.md
    channel: pdf
    ingested_at: 2026-06-25
  - path: raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-i-wasted-2-years-report.md
    channel: notes
    ingested_at: 2026-06-25
  - path: raw/email/email-2026-06-17-i-lost-2-years-and-300k-to-the-wrong-roadmap.md
    channel: email
    ingested_at: 2026-06-25
  - path: raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-devops-from-zero-report.md
    channel: notes
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-9FKqsCVOD_Y-i-wasted-2-years-learning-devops-wrong-here-s-what-i-d-do-in.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-H5FAxTBuNM8-devops-from-zero-to-hero-build-and-deploy-a-production-api.md
    channel: youtube
    ingested_at: 2026-06-25
aliases:
  - DevOps roadmap
  - DevOps learning path
  - TechWorld with Nana
  - KubeCraft roadmap
  - DevOps career path
tags:
  - corpus/mlops
  - synthesis
created: 2026-06-25
updated: 2026-06-25
---

# DevOps Learning Roadmap

**TL;DR** — Multiple sources converge on the same ordered path: OS/Linux → Git → Containers (Docker) → CI/CD → One cloud provider → Kubernetes → IaC (Terraform + Ansible) → Monitoring (Prometheus/Grafana) → Scripting (Python). The most important meta-advice from experienced practitioners: **master concepts, not just tools** — the concepts transfer when tools change; and **build real end-to-end projects early**, before you feel "ready" [^src2][^src3].

## Canonical sequence (TWN DevOps Roadmap)

Nana Janashia's (TechWorld with Nana) 10-step roadmap, presented as the order a professional would follow from scratch [^src1]:

| # | Topic | Why first |
|---|---|---|
| 1 | Concepts of software development | Understand what dev teams do; Git workflows, SDLC, build tools, testing |
| 2 | OS & Linux Basics | Most servers run Linux; shell, file permissions, SSH, networking basics |
| 3 | Containerization — Docker | Standard unit of software packaging; Docker is dominant |
| 4 | CI/CD Pipelines | Automate: test → package → build image → push → deploy |
| 5 | Learn **one** cloud provider | Go deep on AWS, Azure, or GCP — IAM, VPC, compute |
| 6 | Container Orchestration — Kubernetes | Manage hundreds of containers across servers |
| 7 | Monitoring & Observability | Prometheus (metrics), Grafana (dashboards), ELK Stack (logs) |
| 8 | Infrastructure as Code | Terraform (provisioning) + Ansible (configuration management) |
| 9 | Scripting language | Python for automation glue |
| 10 | Version Control — Git | (Often taught first; listed 10th as it is assumed throughout) |

Note: The KubeCraft email (Mischa van den Burg) presents a compatible sequence with a similar philosophy: Linux → Containers → Kubernetes + Homelab → One cloud → Networking → One language [^src3].

## TWN 4-level learning schedule (6 months, ~15h/week)

Structured weekly breakdown from TWN's study guide [^src2]:

| Level | Focus | Weeks | Skill grade |
|---|---|---|---|
| **Level 1** — Prerequisites | Linux, Git, Build Tools | 1–3 | Beginner |
| **Level 2** — Fundamentals | Cloud basics, Nexus, Docker | 4–7 | Novice |
| **Level 3** — Core | CI/CD (Jenkins), AWS, Kubernetes, EKS | 8–16 | Intermediate |
| **Level 4** — Advanced | Terraform, Ansible, Python automation, Prometheus | 17–26 | Senior |

Week 1 focus: Linux commands (`pwd`, `ls`, `rm`), shell scripting, Ubuntu VM on VirtualBox.
Week 2: Environment variables, networking (IP, DNS, NAT, firewalls), Git basics.
Weeks 8–10: Jenkins CI/CD pipelines, Jenkinsfile, multibranch pipelines, GitLab integration.
Weeks 17–20: Terraform (providers, resources, state, modules, EKS module), Terraform CI/CD via Jenkins.
Weeks 21–22: Python (OOP, boto3 for AWS automation, EC2/snapshot management, website monitoring).
Weeks 23–24: Ansible (control node, playbooks, variables, dynamic EC2 inventory).
Weeks 25–26: Prometheus (targets, metrics, exporters, alertmanager), Grafana dashboards [^src2].

## 8 mistakes that waste years (Nana's analysis)

From the "I Wasted 2 Years" video [^src2_video]:

1. **Focusing on tools instead of concepts** — Tools come and go; concepts (CI/CD pipelines, IaC state management, compute/storage/network abstractions) transfer to every tool and cloud. "Tools come and go. Concepts, however, stay forever." [^src2_video]
2. **Learning tools in isolation** — Knowing Docker + Kubernetes + Jenkins separately ≠ employable. Companies need someone who can connect Git → Docker → registry → K8s → Terraform → monitoring end-to-end. [^src2_video]
3. **Not doing projects / starting too late** — Theory without practice doesn't stick; build early, even before you feel ready. "The fastest way to learn is by doing." [^src2_video]
4. **Chasing only certifications** — Certs are an HR baseline filter, not a differentiator. Build first, certify after to validate what you already know. [^src2_video]
5. **Being cheap with education** — Lost income from inefficient learning ≈ $25–35k/yr. "You're either paying with time or paying with money." [^src2_video]
6. **Learning only in sandboxes** — Pre-configured environments hide Git, terminal, troubleshooting. Real DevOps competence comes from breaking and fixing real infrastructure. [^src2_video]
7. **Following roadmaps blindly** — Roadmaps show *what* but not how deep, why, or how things connect. Learn ~20% of each tool covering ~80% of use cases, plus the connections. [^src2_video]
8. **Not building/learning in public** — "Same skills, same work, different visibility." Sharing is teaching; it creates portable proof of competence and surfaces opportunities. [^src2_video]

## Cloud concept-portability principle

Multiple sources emphasize that cloud knowledge transfers:

> "Compute is compute. Storage is storage. Network is networking on any cloud provider." [^src2_video]

Learning AWS deeply → Azure is a relabel (different buttons, same concepts). This justifies "go deep on one" over shallow breadth across three [^src1][^src3].

## The DevOps loop

From the DevOps Zero to Hero video [^src4]: the canonical eight-stage continuous cycle visualized as a figure-8 infinity symbol:

**Plan → Code → Build → Test → Release → Deploy → Operate → Monitor**

This loop is what CI/CD pipelines automate (Build + Test + Release + Deploy) and what monitoring closes (Operate + Monitor feeding back into Plan) [^src4].

## Disagreement note: which language first?

The KubeCraft email argues starting with "Learn a programming language" is the most common wrong first step — it costs 6–12 months without context and the environment (VS Code on Windows) doesn't resemble real servers. Instead: start with Linux, then code from the command line from day one [^src3].

The TWN roadmap places "Scripting language (Python)" at step 9 out of 10 — consistent with the KubeCraft ordering [^src1].

Both agree: Linux basics first.

## See also

- [[mlops/mlops-principles|MLOps Principles]] — how MLOps extends DevOps (the data difference)
- [[mlops/linux-commands|Linux Commands]] — the 20% of Linux commands for 80% of work
- [[mlops/terraform|Terraform]] — IaC tool at the heart of step 8
- [[mlops/ci-cd-for-ml|CI/CD for ML]] — CI/CD pipelines in an ML context
- [[mlops/infrastructure-as-code|Infrastructure as Code]] — IaC concepts and tools
- [[mlops/networking-fundamentals|Networking Fundamentals]] — IP, DNS, VPCs
- [[mlops/README|MLOps hub]]

---

[^src1]: [DevOps Roadmap Final (TechWorld with Nana, Nana Janashia)](../../raw/pdf/pdf-1-devops-roadmap-by-techworld-with-nana.md) — 24-page roadmap PDF; 10-step path, per-step skill lists
[^src2]: [FREEBIE 0 — Master the DevOps Game Study Guide (TechWorld with Nana)](../../raw/pdf/pdf-2-weekly-learning-schedule-by-techworld-with-nana.md) — 26-week learning schedule, 4 levels from prerequisites to advanced
[^src2_video]: [I Wasted 2 Years Learning DevOps Wrong. Here's What I'd Do Instead. (Nana / TechWorld with Nana)](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-i-wasted-2-years-report.md) — [00:52](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-i-wasted-2-years-report.md#t=00:52) mistake 1 (tools vs. concepts); [03:44](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-i-wasted-2-years-report.md#t=03:44) mistake 2 (isolation); [05:31](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-i-wasted-2-years-report.md#t=05:31) mistake 3 (no projects)
[^src3]: [I Lost 2 Years and $300K to the Wrong Roadmap (Mischa van den Burg, KubeCraft)](../../raw/email/email-2026-06-17-i-lost-2-years-and-300k-to-the-wrong-roadmap.md) — KubeCraft sequence; Linux-first argument; dangers of generic roadmaps
[^src4]: [DevOps from Zero to Hero: Build and Deploy a Production API](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-devops-from-zero-report.md) — [01:00](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-devops-from-zero-report.md#t=01:00) DevOps loop (Plan→Code→Build→Test→Release→Deploy→Operate→Monitor)

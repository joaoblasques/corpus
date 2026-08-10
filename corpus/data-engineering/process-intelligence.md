---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/web/web-the-trinity-of-modern-data-architecture-process-intelligence-b19b93a7.md
    channel: web
    ingested_at: 2026-07-03
  - path: raw/_inbox/web-process-intelligence-explained-mining-orchestration-and-the-0b815125.md
    channel: web
    ingested_at: 2026-08-10
  - path: raw/_inbox/web-process-intelligence-landscape-2026-mining-orchestration-and-aa69028c.md
    channel: web
    ingested_at: 2026-08-10
aliases:
  - process mining
  - process orchestration
  - agentic process orchestration
  - BPM
  - business process management
  - decision gate
  - OCPM
  - object-centric process mining
  - BPMN
  - DMN
tags:
  - corpus/data-engineering
  - concept
created: 2026-07-03
updated: 2026-08-10
---

# Process Intelligence

**TL;DR.** Process intelligence is the evolution of classic Business Process Management (BPM) into something adaptive, event-aware, and AI-ready — the layer where technology maps directly to a business outcome (a loan approved, a shipment rerouted, a fraud case resolved) [^src1]. Kai Waehner frames it as one of three capabilities — alongside [event-driven integration](/data-engineering/kafka.md) and trusted agentic AI (see [Agent Security](/ai-engineering/agent-security.md)) — that only deliver full value when architected together as a "Trinity" [^src1].

## Three capabilities

### Process mining — observe what actually happens

Every enterprise has the process it believes exists and the process that actually runs. Process mining closes that gap by reading the event logs that ERP systems, CRM platforms, and ticketing tools produce and reconstructing real execution paths [^src2].

A purchase-to-pay process designed with four steps and three approvals often has dozens of variants, some bypassing approvals entirely. Mining does not create that reality — it reveals it. The output is **operational truth**: where bottlenecks form, where rework costs time, where assumed and actual processes have drifted [^src2].

**Object-centric process mining (OCPM)** (formalized by Wil van der Aalst) extends this by tracing how multiple related objects move through a process together, rather than forcing each case into a single rigid path [^src2]. Traditional mining forced one root object (e.g. an order); OCPM handles the reality that an order has multiple items, multiple shipments, and multiple invoices simultaneously [^src2].

Vendors: Celonis [^src1].

### Process orchestration — govern what happens next

Mining is diagnostic. Orchestration is operational. It defines step sequences, routes work between systems and people, enforces timing and dependencies, and coordinates handoffs [^src2].

Modern orchestration engines are **event-driven** — they react to real-time signals from operational systems rather than running on schedules [^src2]. Open standards:
- **BPMN** — process model notation (reduces vendor lock-in)
- **DMN** — decision model notation (encodes business rules portably)

Orchestration is connective tissue between systems, people, and AI agents — not a replacement for human judgment [^src2]. Vendors: Camunda, Temporal, Apache Airflow [^src1]. **Kestra** is an emerging unified orchestration platform that covers all four enterprise orchestration categories (IT scheduling, data pipelines, business processes, infrastructure automation) under one declarative event-driven control plane — in production at Apple, JPMorgan, Toyota [^src1].

**Market convergence (2026)**: mining vendors are buying execution/orchestration (Celonis → Ikigai Labs); orchestration vendors are adding analytics and agent control; platform vendors are acquiring miners (Salesforce → Apromore into Agentforce). The two halves of process intelligence — seeing what runs and governing what happens next — are converging [^src3].

### The decision gate — enforce the boundaries

Every automated action and every AI recommendation should hit a **decision gate** before it has consequences [^src2]. The gate evaluates the action against business rules, confidence thresholds, and regulatory constraints. What satisfies criteria proceeds. What does not is routed to a human, escalated, or rejected with a documented reason [^src2].

The decision gate is a **function, not a product** [^src2]. Implementation options:
- Rules engine embedded in an orchestration platform (DMN support)
- Standalone decision management product
- Context engine fed by data streaming (Kafka) — evaluates current entity state rather than a stale snapshot

> "Without an explicit, enforceable, auditable boundary, you are not deploying trusted AI. You are deploying capable AI without architectural limits." [^src2]

**Why this is the new requirement for agentic AI**: a model does not decide whether to approve a loan — it assigns a probability. The process layer decides whether that probability is high enough to act on, whether it triggers human review, or whether it falls outside authorized scope [^src2].

### How the three work together

Mining shows where decisions are made and where they need to be governed. Orchestration moves work through the process. The decision gate enforces what each participant — human or AI — is allowed to do [^src2].

The classic BPM failure was assuming processes could be fully specified in advance and that exceptions were edge cases. Process Intelligence evolved past that: mining discovers the real process, orchestration adapts it, and the decision gate keeps autonomous action within auditable bounds [^src2].

## Why it matters for agentic AI

"Agentic automation only works safely when the process layer defines the operational envelope: what the agent can decide alone, what requires human approval, and what must be escalated regardless of what the model recommends" [^src1]. Guardrails live here in practice — not as theoretical constraints inside a model, but as concrete workflow gates that stop, route, or escalate before an action executes [^src1].

## Failure mode: process intelligence without event-driven integration

A workflow engine automates a credit decision, but the data feeding it comes from a nightly batch export. The process runs correctly; the decision is based on a customer's financial state from 18 hours ago. "The automation worked. The outcome was wrong" [^src1]. This is why process intelligence is paired with [event-driven integration](/data-engineering/kafka.md) — the process layer needs live state, not yesterday's batch.

## Industry examples (agentic AI bounded by process intelligence)

- **Financial services** — a transaction event triggers a real-time agentic fraud-risk assessment; below a threshold the process auto-completes, above it the process layer routes to a human analyst before any account action [^src1].
- **Healthcare** — a patient-monitoring deterioration signal reaches a care-pathway engine; an agent recommends an intervention, but the process layer requires clinician confirmation before the recommendation becomes an order [^src1].
- **Supply chain** — a supplier disruption signal reaches the process engine before procurement opens their inbox; an agent proposes rerouting options, and the process layer defines which decisions it can execute autonomously vs. which need sign-off [^src1].

## Related

- [Apache Kafka](/data-engineering/kafka.md) — the event-driven integration layer process intelligence pairs with
- [Agent Security](/ai-engineering/agent-security.md) — model-level vs. process-level safety for agentic AI
- [Data Engineering hub](/data-engineering/README.md)

---

[^src1]: [The Trinity of Modern Data Architecture: Process Intelligence, Event-Driven Integration, and Trusted Agentic AI](../../raw/web/web-the-trinity-of-modern-data-architecture-process-intelligence-b19b93a7.md)
[^src2]: [Process Intelligence Explained: Mining, Orchestration, and the Decision Gate (Kai Waehner)](../../raw/web/web-process-intelligence-explained-mining-orchestration-and-the-0b815125.md)
[^src3]: [Process Intelligence Landscape 2026: Mining, Orchestration, and the Agentic AI Shift (Kai Waehner)](../../raw/web/web-process-intelligence-landscape-2026-mining-orchestration-and-aa69028c.md)

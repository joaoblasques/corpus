---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/web-forward-deployed-engineers-and-the-future-of-software-engine-a6f88e06.md
    channel: web
    ingested_at: 2026-08-23
aliases:
  - forward deployed engineering
  - FDE
  - agent engineer
  - forward deployed engineer
tags:
  - corpus/ai-engineering
  - concept
created: 2026-08-23
updated: 2026-08-23
---

# Forward Deployed Engineering

**TL;DR.** Forward deployed engineering (FDE) places highly technical employees directly in customer environments to solve problems that require deep product + domain + engineering skill together. In the AI agent era, the role is converging with product engineering: as code becomes cheap, the bottleneck shifts to translating customer insight into product, a task both FDEs and product engineers are now positioned to do. [^1]

## Definition and historical origin

FDE originated at Palantir as a model for placing engineers directly at customer sites — accountability to the customer outcome is the defining characteristic, not a specific skill set. The range of skills associated with the title has since become wide enough to be "almost nonsensical," per Natalie Meurer (Head of Agent Engineering, Sierra). [^1]

## "Agent engineer" as the AI-era variant

Sierra renamed the role "agent engineer" to make the technical work legible, not just the customer-facing element. Agent engineering combines: [^1]
- Systems integration (customer APIs, databases, internal tools)
- Agent development (orchestration layer, not model layer)
- Customer operations understanding
- Product sense
- End-user experience design (including UX taste for voice agent naturalness)

## What agent engineers do at Sierra

Sierra builds conversational AI agents for customer service (voice, chat, email) for enterprise clients. The agent engineering workflow: [^1]

1. **Discovery phase**: Find intersection of "genuinely difficult problems" and "high business impact" — e.g., dispute processing in financial services
2. **Integration**: Connect customer systems (APIs, SOPs, knowledge bases) to the agent layer
3. **Customization**: Every agent is specific to the customer's brand, tone, and workflows; not a template deployment
4. **Production**: Sierra reaches production in 40–60 days per enterprise customer

**Where the hard work is**: Most customer-specific work happens at the **orchestration layer**, not the model layer. Sierra uses an "orchestrated constellation of models" internally — the right model for each job. [^1]

## Convergence with product engineering

The key thesis from Meurer [^1]:

> "When code becomes cheap to author, it also becomes easier to translate customer insights directly into a product. Product engineering and forward deployed engineering are therefore converging."

- Best product engineers should be talking to customers
- Best FDEs should be building the product
- "I think that is new" — as of 2026

FDE has historically been the generalist role; with AI lowering the cost of code, the generalist advantage extends to anyone who can hold customer insight and product execution in the same context.

## Enterprise complexity: change management as the hard problem

Every enterprise needs hundreds or thousands of people to contribute to its agentic ecosystem — understanding what's changing, following a discrete release process, managing integrations. This change-management dimension is "a change-management problem" that may be harder than the technical implementation. [^1]

## Generalists vs. specialists

Meurer's view: generalists will become more valuable, not specialists. The exception: specialists who hold knowledge not readily available to an agent (domain expertise in areas the model can't replicate from training data). [^1]

## Related

- [/ai-engineering/claude-managed-agents.md](/ai-engineering/claude-managed-agents.md) — enterprise agent deployment at scale
- [/ai-engineering/agentic-workflow.md](/ai-engineering/agentic-workflow.md) — agent workflow patterns
- [/ai-engineering/multi-agent-systems.md](/ai-engineering/multi-agent-systems.md) — multi-agent coordination (Sierra uses orchestrated constellation of models)
- [/ai-engineering/agent-harness.md](/ai-engineering/agent-harness.md) — orchestration layer patterns

---

[^1]: [Forward Deployed Engineers and the Future of Software Engineering — Latent Space / Natalie Meurer](../../raw/web/web-forward-deployed-engineers-and-the-future-of-software-engine-a6f88e06.md)

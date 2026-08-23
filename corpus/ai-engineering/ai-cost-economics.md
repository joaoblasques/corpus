---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/web-when-ai-costs-more-than-the-engineer-59fa9175.md
    channel: web
    ingested_at: 2026-08-23
aliases:
  - AI cost economics
  - AI spend per engineer
  - AI infrastructure cost
  - compute vs payroll
tags:
  - corpus/ai-engineering
  - concept
created: 2026-08-23
updated: 2026-08-23
---

# AI Cost Economics

**TL;DR.** As of mid-2026, AI compute spend is structurally replacing engineering headcount as the marginal cost driver at frontier AI-native firms. Anthropic spends 2.3x its payroll on compute. A 680x gap separates the top-1% of companies from the median in AI spend per engineer, and all three 2026–2029 growth scenarios point upward. [^1]

## The current spending landscape (Ramp AI Index, June 2026)

| Cohort | AI spend / engineer / year | % of loaded salary |
|---|---|---|
| Anthropic (internal) | ~$2M | ~400% |
| Top 1% of companies | $89K | ~40% |
| Median company | $137 | ~0.06% |

**680x gap** between top-1% and median company. Top-1% spend growing at 14.1% month-over-month. [^1]

**Revenue per employee** (Epoch AI, 2026): Anthropic ~$14M, OpenAI ~$6.5M — highest in the Forbes Global 2000. Cost structure follows revenue structure. [^1]

## Three scenarios for 2026–2029

Using a $224K fully-loaded senior engineer salary growing 5%/year as the baseline: [^1]

| Year | Bear ($) | Bear (% salary) | Base ($) | Base (%) | Bull ($) | Bull (%) |
|---|---|---|---|---|---|---|
| 2026 | $90K | 40% | $90K | 40% | $90K | 40% |
| 2027 | $106K | 45% | $164K | 70% | $258K | 110% |
| 2028 | $118K | 48% | $259K | 105% | $444K | 180% |
| 2029 | $106K | 41% | $363K | 140% | $596K | 230% |

**Bull scenario drivers** [^1]:
- Frontier model prices hold as training costs plateau and demand outpaces supply
- Agentic workloads drive 24x rise in token consumption by 2030 (Goldman Sachs projection)
- Competitive pressure makes AI spend mandatory ("if a rival ships features faster, the AI bill stops being optional")

**Bear scenario counterweights** [^1]:
- Token prices have fallen ~10x/year for three years (GPT-4-class input: $30/M at launch → <$3/M by 2026)
- Open-weight models (e.g., DeepSeek-V3) deliver frontier-comparable benchmarks at 1/10th–1/30th the API cost
- Companies that ration usage by role or workload bend the cost curve

## Structural implication

In the Bull case, AI spend per engineer exceeds the median SaaS revenue contribution per employee (~$250K). The cost structure at Anthropic and OpenAI — where compute dominates payroll — may preview where the broader software industry is heading. [^1]

## Cost optimization patterns in practice

Top-1% firms in 2026 are already "mixing frontier models with cheap open-source" to control per-task cost (Ramp data). Platform engineering teams are emerging whose primary job is cutting per-token cost across the organization. [^1]

## Related pages

- [/ai-engineering/agent-cost-management.md](/ai-engineering/agent-cost-management.md) — per-agent cost patterns
- [/ai-engineering/scaling-laws.md](/ai-engineering/scaling-laws.md) — token price deflation dynamics
- [/ai-engineering/cloud-agents.md](/ai-engineering/cloud-agents.md) — cloud-based agent execution at scale

---

[^1]: [When AI Costs More Than the Engineer — Tom Tunguz](../../raw/web/web-when-ai-costs-more-than-the-engineer-59fa9175.md)

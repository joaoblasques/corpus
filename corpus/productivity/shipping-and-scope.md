---
type: concept
domain: productivity
status: draft
sources:
  - path: raw/email/email-2026-06-11-how-to-finish-early-and-satisfy-your-stakeholders.md
    channel: inbox
    ingested_at: 2026-06-12
aliases:
  - good enough
  - perfectionism
  - done is an agreement
  - scoping
  - shipping
tags:
  - corpus/productivity
  - concept
created: 2026-06-12
updated: 2026-06-12
---

# Shipping and Scope

**TL;DR** — Finishing on agreed scope beats polishing past it. The work engineers do after "done" is usually invisible **rough edges** or unrequested **design preferences** dressed up as quality. "Done is an agreement," not a private threshold you keep moving. Shipping on time compounds into a track record of reliability — the real currency of a career [^src1].

## Three categories of "one more thing"

Have a framework before acting on the urge to keep working [^src1]:

| Category | Definition | Rule |
|---|---|---|
| **Bug** | Prevents the product doing what was agreed (drops rows, breaks on month boundary, miscalculates in prod) | Non-negotiable; fix before or immediately after shipping |
| **Rough edge** | Imperfection outside any real user's path (inconsistent column name, 900ms query on a twice-a-week dashboard) | "Ugly by design" is legitimate; leaving it is a deliberate scoping decision |
| **Design preference** | Something *you* want that the stakeholder never asked for (cleaner abstraction, nicer folder structure) | The expensive trap; the test — "did anyone ask for this, or is it just incomplete in my head?" |

> "Choosing not to smooth a rough edge because no user will ever hit it is not laziness" — it is intentional restraint, a design decision [^src1].

## Done is an agreement

- Scope is defined with the stakeholder *before* the work; "done" is not a technical state you set unilaterally, because you will keep moving the threshold [^src1].
- **Read the feedback shift**: early feedback ("can we change this filter?") is active problem-solving; later feedback ("this looks great, when can we roll it out?") means the agreement is reached [^src1].
- **The closing question**: never ask "anything you'd like to improve?" (invites scope creep). Ask only **"is there anything critical missing?"** — the word *critical* filters preferences from blockers. Then write it down to create a paper trail [^src1].

## Perfectionism is an identity problem

- The maladaptive pattern: high standards fused with avoidance and an inability to call something done. A cited 2021 meta-analysis ties adaptive perfectionism to better performance/wellbeing and maladaptive to worse wellbeing and more procrastination [^src1].
- Root cause: an early-career equation — *good engineer = engineer who finishes everything* — that never updates. Later, "finishing the right things matters more than finishing everything" [^src1].

## The post-launch contract

Define the edges before shipping so you are not pulled back indefinitely [^src1]:
- **You commit to**: fixing genuine bugs, and a proactive two-week check-in asking "is anything critical missing?"
- **You do not commit to**: open-ended feature requests or optimizations — those go to a backlog.
- **Verify with data, not anxiety**: query history and usage logs tell you whether the product is actually used; "a product nobody uses is a product worth a conversation."

## The AI angle

"The craft argument for over-polishing has collapsed" now that AI writes much of the code; the scarce, unreplicable input is judgment about *what to build and whether it worked* [^src1]. Cross-reference [AI-Augmented Knowledge Work](/productivity/ai-augmented-knowledge-work.md) and the stakeholder-trust mechanics in [Working with Stakeholders](/productivity/working-with-stakeholders.md).

---

[^src1]: [How to Finish Early and Satisfy your Stakeholders](../../raw/email/email-2026-06-11-how-to-finish-early-and-satisfy-your-stakeholders.md)

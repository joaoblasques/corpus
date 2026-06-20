---
type: concept
domain: productivity
status: draft
sources:
  - path: raw/_inbox/email-2026-05-28-circle-of-competence-mental-model.md
    channel: inbox
    ingested_at: 2026-06-12
  - path: raw/web/thought-experiment-mental-model-what-if.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/web-map-is-not-territory-mental-model-what-is-hidden-from-me.md
    channel: web
    ingested_at: 2026-06-17
  - path: raw/web/web-two-tools-for-clearer-thinking.md
    channel: web
    ingested_at: 2026-06-17
  - path: raw/email/email-2026-06-15-why-other-people-can-see-things-about-you-that-you-cant.md
    channel: email
    ingested_at: 2026-06-20
aliases:
  - circle of competence
  - thought experiment
  - what if
  - mental model
  - Johari Window
  - blind spot
  - map is not territory
  - ladder of inference
  - ishikawa diagram
  - fishbone diagram
tags:
  - corpus/productivity
  - concept
created: 2026-06-12
updated: 2026-06-17
---

# Mental Models

**TL;DR** — Mental models are reusable thinking tools for decisions under uncertainty. Covered here: the **Circle of Competence**, **Thought Experiments**, **Map Is Not Territory** (every abstraction compresses reality in purpose-specific ways; ask what it hides), **Ladder of Inference** (surface the unconscious reasoning chain before you act), and the **Ishikawa Diagram** (map all causes before committing to one fix). All compress judgment, the scarce skill that survives AI [^src1][^src2][^src3][^src4].

## Circle of Competence

A model popularized by Warren Buffett and Charlie Munger to justify investing only in assets they deeply understand; it generalizes far beyond investing [^src1].

- **Three nested zones**: an inner circle of what you truly know; a larger circle of what you *think* you know; and the gap between them, where "ego and overconfidence live" [^src1].
- **The tell**: a task that should take minutes but eats hours is a signal you have wandered outside your circle [^src1].
- **The forest analogy**: lumberjacks, biologists, and runners each have a valid circle over the same forest — a complex system no single specialist fully owns. "You don't have to learn everything. You just have to know who to ask" [^src1].
- **Generalists as routers**: foresters hold enough overlapping knowledge across specialties to manage the whole; "being a generalist helps you know exactly whom to ask" [^src1]. This connects directly to cross-training (see [[productivity/learning-to-learn|Learning to Learn]]).

## Thought Experiments

Running an experiment inside your head to predict outcomes — a model you already use without noticing [^src2].

- **Bounded by your circle**: you "can operate only within our circle of competence, our experience and our full set of knowledge" — the two models compose [^src2].
- **Make it rigorous**: understand the domain, follow its rules (physics, social dynamics), then generate many possible outcomes [^src2].
- **Canonical examples** as leadership lenses [^src2]:
  - *Veil of Ignorance* (Rawls, 1971): design rules without knowing your future role → forces fairness in process design.
  - *Trolley Problem*: a "one vs many" trade-off → resource allocation, budgets, sunsetting products.
  - *Prisoner's Dilemma*: betray wins a single game, cooperate wins the repeated game → why reputation compounds.
- **Career "what ifs"**: "What if you were fired tomorrow?" / "What if AI replaces everything you do starting tomorrow?" — cheap simulations that sharpen real decisions [^src2].

## Map Is Not Territory

"A map is not the territory it represents, but, if correct, it has a similar structure to the territory, which accounts for its usefulness" (Alfred Korzybski) [^src3].

Every abstraction — documentation, a project plan, a photo, a software model — compresses reality for a specific purpose. That compression introduces blind spots.

**When using maps — the three diagnostic questions** [^src3]:
- *What was the purpose of creating it?* (The Mercator projection was designed for sailors to navigate by bearing; as a result it distorts landmass size so severely that Greenland appears the size of Africa.)
- *Is it still accurate and updated?* (An un-updated vendor API doc can cost two months of rework.)
- *What is it NOT showing us?* — the single most important question.

**"Essentially, all models are wrong, but some are useful"** (George Box) — usefulness depends on fit between the map's purpose and your current need [^src3].

**When creating maps** (documentation, planning, specs) [^src3]:
- State the purpose explicitly so omissions are legible.
- Name the audience — the map needed by your future self differs from the map needed by a newcomer.
- Add timestamps and valid-until criteria; point out when the map will no longer hold.

**Over-planning trap**: "There are moments where constantly improving the map becomes a way of avoiding action. Plans help, but past a certain point, they hit diminishing returns" [^src3]. Some territories change faster than the map can track.

Composes with Circle of Competence: both models ask you to be explicit about the boundary of what your representation covers.

## Ladder of Inference

Developed by Harvard professor Chris Argyris; surfaces the unconscious reasoning chain that runs from observable data to action [^src4].

**The seven rungs** (bottom to top): available data → selected data → interpretations → assumptions → conclusions → beliefs → actions. Problems arise when rungs are skipped: "we skip rungs, failing to acknowledge how a conclusion was formed before we act on it" [^src4].

**How to use it** — before making a significant decision, work down the ladder:
1. Identify which rung you are currently on.
2. Ask: why am I concluding this? What assumptions am I making? Are they valid? What did I ignore?
3. Rebuild the chain deliberately upward — you'll "often reach the same conclusion but with far more confidence" [^src4].

**Key reframe**: the ladder doesn't tell you what conclusion to reach; it tells you whether the case is ready to make yet. A developer missing deadlines who you're about to fire might, under ladder analysis, reveal unrealistic deadlines or an unspoken personal issue — neither of which supports the conclusion [^src4].

## Ishikawa Diagram (Fishbone / Cause-and-Effect)

Created by Japanese professor Kaoru Ishikawa; maps all possible causes of a problem before deciding which one to act on [^src4].

**When to use**: recurring problems that keep returning despite fixes; post-mortems; any situation where you want to understand causes before committing to a solution [^src4].

**How to use it**:
1. Define the problem specifically at the diagram head ("declining customer retention" beats "things aren't working").
2. Identify contributing categories (classic: People, Methods, Equipment, Materials, Measurement, Environment).
3. Under each category, ask "why is this happening?" and write every possible cause — do not filter.
4. Step back; look for causes appearing in multiple categories and quick-to-test leverage points.

**Common mistake**: "jumping straight from 'what is the problem?' to 'what is the fix?'" — the diagram forces the step in between [^src4].

**Works with Ladder of Inference**: use the Ishikawa Diagram to map what's causing a problem before committing to one; use the Ladder to check that your reasoning about *which* cause holds up [^src4].

## Johari Window

A model for understanding self-awareness and blind spots, originally developed by psychologists Joseph Luft and Harry Ingham (1955) — popularized via the email "[Why Other People Can See Things About You That You Can't]" [^src5].

**Four quadrants** (axes: Known/Unknown × To Self/To Others):

| | Known to self | Unknown to self |
|---|---|---|
| **Known to others** | **Open** (shared understanding) | **Blind** (others see it; you don't) |
| **Unknown to others** | **Hidden** (you know; others don't) | **Unknown** (neither knows) |

The **Blind quadrant** is the highest-leverage area for growth: it contains patterns and behaviors that affect others but that you can't see yourself. Common examples: how you come across under stress, default communication habits, or recurring failure modes that colleagues notice but never say aloud [^src5].

**Three ways to shrink your blind spots** [^src5]:
1. **Ask trusted people directly** — "What's one thing I do that you think I'm unaware of?" Frame it as a learning question, not a performance review. The goal is to expand the Open quadrant.
2. **Look for patterns** — feedback you've heard more than once from different sources is a signal, not a coincidence. "If three different people, in three different contexts, notice the same thing, believe them."
3. **Notice your reactions** — strong emotional reactions (defensiveness, dismissiveness) to a comment often signal you've hit the edge of your blind spot. Curiosity instead of defensiveness is the habit.

Connects to [[productivity/mental-models|Circle of Competence]]: both models ask you to be accurate about the boundary between what you know (or see) and what you don't.

## Why this matters now

All five models frame judgment — knowing limits, simulating outcomes, seeing what abstractions hide, checking reasoning chains — as the durable human contribution as AI absorbs execution. See [[productivity/ai-augmented-knowledge-work|AI-Augmented Knowledge Work]] and [[productivity/shipping-and-scope|Shipping and Scope]] for where this judgment gets applied.

---

[^src1]: [Circle of Competence - Mental Model](../../raw/email/email-2026-05-28-circle-of-competence-mental-model.md)
[^src2]: [Thought Experiment - Mental Model: What If?](../../raw/web/thought-experiment-mental-model-what-if.md)
[^src3]: [Map Is Not Territory — Mental Model: What Is Hidden From Me?](../../raw/web/web-map-is-not-territory-mental-model-what-is-hidden-from-me.md)
[^src4]: [Two Tools for Clearer Thinking](../../raw/web/web-two-tools-for-clearer-thinking.md)
[^src5]: [Why Other People Can See Things About You That You Can't](../../raw/email/email-2026-06-15-why-other-people-can-see-things-about-you-that-you-cant.md)

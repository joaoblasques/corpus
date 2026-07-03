---
type: concept
domain: productivity
status: draft
sources:
  - path: raw/youtube/youtube-WRibE2nt8wM-lecture-1-introduction-to-individual-decision-making.md
    channel: youtube
    ingested_at: 2026-06-25
aliases:
  - individual decision making
  - rational choice
  - utility theory
  - VNM utility
  - Von Neumann-Morgenstern
  - expected utility
  - Bayesian beliefs
  - ordinal utility
  - cardinal utility
  - game theory
  - Keynesian beauty contest
  - strategic interdependence
tags:
  - corpus/productivity
  - concept
created: 2026-06-25
updated: 2026-06-25
---

# Decision Making

**TL;DR** — Rational decision-making is consistency toward objectives, not what a person's objectives *are*. The formal machinery for analysing decisions under uncertainty relies on two pillars: **utility** (a function over outcomes encoding preferences) and **beliefs** (probabilities over states of the world). When others are also deciding, individual decision theory becomes game theory — each person's optimal choice depends on predictions about others' choices [^src1].

*Source: MIT OpenCourseWare, Game Theory, Lecture 1 (Ian Ball) — introductory lecture covering individual decision-making as the foundation for game theory.*

## Rationality as consistency

Economists define rationality behaviourally: a person is rational if they make choices that are consistent with *some* objective — not with the "right" objective [^src1].

- Standard definition: "An individual is rational if they make choices that are consistent with pursuing some objective or goal" [^src1].
- This leaves the objective open; rational does not mean sensible or ethical — it means internally consistent in the pursuit of *something*.
- Economists don't prescribe objectives; they model what choices would follow if certain preferences were held [^src1].

## Utility

Utility is a function from outcomes to numbers, representing how much the decision-maker values each outcome [^src1].

**Ordinal vs cardinal utility** [^src1]:

| Type | What it encodes | Example |
|---|---|---|
| **Ordinal** | Preference ranking only — A > B or B > A | "I prefer A to B" |
| **Cardinal** | Magnitude of preference — how *much* better A is than B | "A is twice as good as B" |

- Ordinal utility suffices for choices under certainty: knowing A > B > C is enough to always choose A.
- Cardinal utility is required under uncertainty, where choices involve *probability-weighted* outcomes. How much better A is relative to B determines the value of a gamble between them.
- **The VNM theorem** (Von Neumann and Morgenstern): if preferences over risky prospects (lotteries) satisfy a small set of axioms — completeness, transitivity, independence, continuity — then those preferences are *representable* by an expected-utility function. That is, choosing the lottery with highest expected utility is the implied behaviour [^src1].

**VNM expected utility in practice** [^src1]:

Given a lottery that pays outcome A with probability p and outcome B with probability (1-p):

```
Expected utility = p · u(A) + (1-p) · u(B)
```

A rational agent under VNM axioms will always choose the lottery with the highest expected utility. This is the standard model for decisions under risk.

## Beliefs

Beliefs are subjective probabilities the agent assigns to states of the world they do not control [^src1].

- **Bayesian beliefs**: the agent has a probability distribution over states of the world (a prior), updates it when evidence arrives (Bayes' rule), and acts based on the updated (posterior) belief.
- Beliefs + utility together determine optimal action: maximize expected utility given beliefs about what states are likely [^src1].
- The key subtlety: beliefs are *inputs* to decision-making, not outputs. Changing information changes beliefs; changing preferences changes utility. Conflating the two is a common analytical error [^src1].

## Strategic interdependence: when others also decide

The jump from individual decisions to **game theory** happens the moment your optimal choice depends on what you predict others will choose [^src1].

- Formally: each player has a strategy set (possible choices), preferences over outcomes, and beliefs about other players' strategies. Optimal strategy requires predicting what others will do [^src1].
- **The Keynesian beauty contest**: John Maynard Keynes compared stock picking to a newspaper beauty contest where you vote not for the person you find most attractive, but for the person you think most others will vote for — "not as average opinion estimates of the average opinion, but we're trying to figure out what average opinion estimates average opinion to be" [^src1].
- An experimental demonstration: ask a room to guess 2/3 of the average guess. Naive answer: 50. But if everyone reasons "others will guess 50, so I should guess 33" → correct answer is 0 by iterated deletion of dominated strategies. In practice, room averages land around 22–25 — showing limited iterated reasoning [^src1].
- The result: "there's not necessarily a unique right answer in strategic contexts; the right answer depends on what you think others are going to do" [^src1].

## Implications for knowledge-work decisions

- **Under certainty**: ordinal utility suffices — rank options and take the top one. Most practical choices are here.
- **Under risk**: expected utility framework. Compute probability-weighted value of each option; take the max. Requires cardinal utility (you must know how much you value each outcome, not just the ranking).
- **In groups or markets**: your optimal choice depends on others' choices. Equilibrium analysis (game theory) applies — picking the best answer without thinking about others' responses can be systematically wrong (the beauty contest).
- **Coherence check**: the VNM axioms provide a normative benchmark. If your preferences violate transitivity (A > B, B > C, C > A) you can be Dutch-booked — cycled through choices in a way that drains value [^src1].

## Related

See [Mental Models](/productivity/mental-models.md) for complementary heuristic frameworks (Circle of Competence, Ladder of Inference). The **Test** and **Own** moves in the [ACTOR framework](/productivity/learning-to-learn.md) are calibration tools for beliefs — forming judgments in the face of incomplete information. The VNM framework is also foundational in [stakeholder negotiations](/productivity/working-with-stakeholders.md) where outcome preferences and uncertainty trade-offs must be made explicit.

---

[^src1]: [Lecture 1: Introduction to Individual Decision Making (MIT OpenCourseWare, Game Theory)](../../raw/youtube/youtube-WRibE2nt8wM-lecture-1-introduction-to-individual-decision-making.md) — Ian Ball, MIT

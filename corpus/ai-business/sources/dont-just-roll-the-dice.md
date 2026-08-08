---
type: source
domain: ai-business
status: draft
sources:
  - path: raw/_inbox/pdf-don-t-just-roll-the-dice-part-01.md
    channel: pdf
    ingested_at: 2026-08-08
  - path: raw/_inbox/pdf-don-t-just-roll-the-dice-part-02.md
    channel: pdf
    ingested_at: 2026-08-08
aliases:
  - Don't Just Roll the Dice
  - Neil Davidson software pricing
  - DJTRD
  - usefully short guide to software pricing
tags:
  - corpus/ai-business
  - source
  - pricing
  - software-business
created: 2026-08-08
updated: 2026-08-08
---

# Don't Just Roll the Dice: A Usefully Short Guide to Software Pricing (Neil Davidson, 2009)

TL;DR: Concise (73pp, Simple Talk Publishing, ISBN 978-1-906434-38-0, CC BY-NC-ND 2.0) by Neil Davidson, co-founder and joint CEO of Red Gate Software (Cambridge, UK). Covers economics, pricing psychology, pitfalls, and advanced pricing tactics for software products. Written from practitioner experience. Free to distribute. Both parts (complete book) ingested.

## Author

**Neil Davidson** — co-founder and joint CEO of Red Gate Software; founder of the annual Business of Software conference. Red Gate was founded in 1999 with no VC money; reached 150 employees by 2009. Neil is @neildavidson on Twitter; blog at businessofsoftware.org [^p01].

---

## The Core Lesson: Price Is Not About Cost

The opening anecdote: in 1938, two engineers set the price of their first oscilloscope ($54.40) because the number reminded them of a 19th-century political slogan — "54-40 or Fight!" They hadn't counted their costs (the real cost was higher than the price) and hadn't researched competitors (General Radio charged $400 for an equivalent model). Those engineers were Bill Hewlett and Dave Packard. The lesson: most software pricing decisions are equally arbitrary. They don't have to be [^p01].

---

## Chapter 1: Economics of Pricing

**Willingness to pay**: different customers have different maximum prices they would accept. If you set a single price, you can capture only those customers whose willingness to pay exceeds that price. You leave money on the table from customers who would have paid more; you miss revenue from customers who would have paid less [^p01].

**Economic value to the customer (EVC)**: the total monetary benefit a customer receives from your product. Pricing above EVC is impossible long-term; pricing well below it leaves margin uncaptured. Useful framing: price = perceived EVC × discount rate applied for uncertainty [^p01].

**Perfectly discriminating monopolist**: theoretical ideal — charge every customer exactly their willingness to pay, capturing the entire consumer surplus. In practice, this requires perfect information and individualized pricing (e.g., enterprise sales) [^p01].

---

## Chapter 2: Pricing Psychology — What Is Your Product Worth?

**What is your product?**: pricing depends on how the customer defines the product. The same piece of software can be a cost-reduction tool, a risk-reduction tool, or a status purchase — and the appropriate price point differs dramatically by framing [^p01].

**Perceived value**: customers do not calculate EVC from first principles — they estimate value from signals: brand, design, price point itself, and reference prices from competitors. A higher price can increase perceived value if the customer cannot objectively assess quality [^p01].

**Reference points and anchoring**: customers price-compare relative to anchors (competitor prices, the customer's own expectations, or other tiers within your own product line). The anchor affects what "fair" means. A $100 add-on is cheap next to a $1000 product; expensive next to a $20 product [^p02].

**The fairness constraint**: customers punish perceived price unfairness even when it is economically irrational to do so. Charging $100 for software that solves a $10,000 problem can feel fair; charging $1000 for the same software to a customer who got it free for years can feel like exploitation, even though $1000 < $10,000. Trust is a long-term asset; price gouging destroys it [^p02].

---

## Chapter 3: Pricing Pitfalls

**Competitors**: don't price solely relative to competitors. Their price reflects their costs and strategy, not the value you provide. If your product is genuinely better, pricing at parity under-sells it; if you can't explain why yours is better, competitors' prices may be a ceiling you can't exceed regardless [^p02].

**Pirates**: treating software piracy as lost revenue overestimates its impact. Pirates are rarely customers you could have converted at any realistic price. Anti-piracy measures that hurt legitimate customers (DRM friction) often cost more than the piracy they prevent [^p02].

**Switching costs**: customers factor in the cost of switching when evaluating price. High switching costs (data lock-in, workflow integration, trained staff) justify higher prices but also create resentment if you exploit them too aggressively [^p02].

**Cost-based pricing**: costs set a floor (you can't sustainably price below them) but have no bearing on what customers will pay. "Cost plus markup" is a recipe for mis-pricing in both directions [^p02].

---

## Chapter 4: Advanced Pricing

**Versioning**: offer multiple product tiers at different prices to capture willingness-to-pay variation across customer segments. Classic strategy: "good / better / best." Key principles:
- Versions work best when customers can easily compare them.
- Adding a "jumbo" tier at the top increases sales of the "large" tier (compromise effect): people avoid extremes and gravitate toward middle options when differences are clear.
- **Compromise effect reverses when products are hard to compare**: if customers cannot easily evaluate the differences between tiers (e.g., laptop configurations with different processor/wireless/DVD combinations), they flee the middle and buy either the cheapest or the most expensive option. Hard-to-compare versioning can also cause customers to defer purchase entirely [^p02].

**Bundling**: combining products at a combined price below the sum of individual prices. Effective when customers have negatively correlated valuations (the customer who highly values product A barely values B, and vice versa) — bundling extracts more total surplus. Less effective when valuations are positively correlated [^p02].

**Multi-user and site licences**: pricing for teams and organizations requires different logic than individual pricing. Common approaches: per-seat pricing (linear), tiered seat bands (step functions), site licences (unlimited use for a fixed fee). Site licences increase switching costs and simplify procurement [^p02].

**Free trials**: let customers discover value before committing. Reduces the perceived risk of purchase. Works best when value is discoverable within the trial period and the trial experience does not itself fully substitute for the paid product [^p02].

**Network effects**: products that become more valuable as more users adopt them (e.g., collaboration tools, file formats, standards). Pricing must account for network effects: free or subsidized early adoption builds the network, which then supports higher prices for later adopters [^p02].

**Freemium**: give the core product free, monetize advanced features or capacity. Works when: the free tier is genuinely useful (drives organic adoption); a meaningful fraction of users have needs that exceed the free tier; upgrade triggers are natural and non-coercive [^p02].

---

## Chapter 5: What Your Price Says About You

**Price as signal**: the price itself communicates product quality and target market segment. A very low price signals either commodity value or potential quality concern. A very high price signals premium positioning. Changing price changes perception — independently of any product change [^p02].

**Practice trumps theory**: most pricing decisions can't be fully pre-calculated. The practical approach: make an informed estimate, ship it, watch conversion rates and feedback, and adjust. Pricing is an empirical process, not a one-time calculation [^p02].

**How to change your pricing**: gradual increases with new versions are least disruptive. Sudden large increases signal either previous under-pricing or opportunism, both of which damage trust. Grandfathering existing customers at old prices is a common trust-preservation tactic [^p02].

---

## Product Pricing Checklist (Summary)

1. What is your strategy (market penetration vs. profit maximization)?
2. What is your product — specifically, in the customer's frame?
3. How will customers judge fairness?
4. Who are your target customers (segment, size, sophistication)?
5. Who are your competitors and what do they charge?
6. How will you sell (self-serve, sales-assisted, channel)?
7. Can you segment and version?
8. Can you bundle?
9. Make an informed initial guess.
10. Test it in market and adjust based on observed conversion [^p01].

---

[^p01]: [Don't Just Roll the Dice — Part 01](../../../raw/pdf/pdf-don-t-just-roll-the-dice-part-01.md)
[^p02]: [Don't Just Roll the Dice — Part 02](../../../raw/pdf/pdf-don-t-just-roll-the-dice-part-02.md)

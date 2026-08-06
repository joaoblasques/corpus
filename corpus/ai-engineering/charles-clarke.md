---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-information-retrieval-implementing-and-evaluating-part-01.md
    channel: pdf
    ingested_at: 2026-08-05
  - path: raw/_inbox/pdf-information-retrieval-implementing-and-evaluating-part-31.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-information-retrieval-implementing-and-evaluating-part-32.md
    channel: pdf
    ingested_at: 2026-08-06
aliases:
  - Charles L.A. Clarke
  - C.L.A. Clarke
tags:
  - corpus/ai-engineering
  - entity
created: 2026-08-05
updated: 2026-08-06
---

# Charles L.A. Clarke

IR researcher at the University of Waterloo; doctoral advisor of Stefan Büttcher; doctoral student of Gordon V. Cormack; co-author of *Information Retrieval: Implementing and Evaluating Search Engines* (MIT Press, 2010) [^p01]. Known for building real search systems alongside deep theoretical contributions.

## Research contributions

**Region algebra** (Clarke, Cormack & Burkowski, 1995): a set algebra over text spans (regions) that supports containment and adjacency operators. The four core operators — contained-in (<), contains (>), before (←), after (→) — compose to express complex structured queries such as "find paragraphs that contain the phrase 'information retrieval' and are contained in sections titled 'Evaluation'." Region algebra is the theoretical foundation for XML retrieval in the book [^p31].

**GC-lists (Generalized Containment lists)**: the implementation data structure for region algebra. A GC-list is a positional posting list annotated with span start and end offsets. Containment and adjacency operators can be evaluated in O(m + n) time per operator (merge-join over two GC-lists), making complex structured queries tractable at scale [^p32].

**Schema-independent indexing** (co-developed with Büttcher): by encoding structural element boundaries in standard positional posting lists, Clarke and Büttcher enabled the Wumpus system to evaluate region-algebra queries over arbitrary XML schemas without requiring a separate structured index per schema [^p31].

**INEX participation**: Clarke's region-algebra framework underpins several INEX (Initiative for the Evaluation of XML Retrieval) submissions, where element-level retrieval with containment constraints is evaluated using Cumulated Gain adapted for XML granularity [^p32].

## See also

- [Classical Information Retrieval](/ai-engineering/information-retrieval.md)
- [Stefan Büttcher](/ai-engineering/stefan-buttcher.md)
- [Gordon V. Cormack](/ai-engineering/gordon-cormack.md)
- [Information Retrieval: Implementing and Evaluating Search Engines](/ai-engineering/sources/information-retrieval-implementing-and-evaluating.md)

---

[^p01]: [Information Retrieval: Implementing and Evaluating Search Engines — Part 1](../../raw/pdf/pdf-information-retrieval-implementing-and-evaluating-part-01.md)
[^p31]: [Information Retrieval: Implementing and Evaluating Search Engines — Part 31](../../raw/pdf/pdf-information-retrieval-implementing-and-evaluating-part-31.md)
[^p32]: [Information Retrieval: Implementing and Evaluating Search Engines — Part 32](../../raw/pdf/pdf-information-retrieval-implementing-and-evaluating-part-32.md)

---
type: entity
domain: software-engineering
status: draft
confidence: 0.85
last_confirmed: 2026-08-05
sources:
  - path: raw/pdf/pdf-a-computational-logic-1979-part-01.md
    channel: pdf
    ingested_at: 2026-08-03
aliases:
  - J Strother Moore
  - J S Moore
  - Moore
  - Matt Kaufmann ACL2
tags:
  - corpus/software-engineering
  - entity
  - formal-verification
  - theorem-proving
created: 2026-08-03
updated: 2026-08-05
---

# J Strother Moore

**TL;DR:** Computer scientist at SRI International (1979); co-author with [Robert S. Boyer](/software-engineering/robert-s-boyer.md) of the Boyer-Moore theorem prover and its 1979 monograph. Later co-developed ACL2, the industrial successor. [^p01]

## Identity and affiliation

Moore was affiliated with SRI International, Menlo Park, California at the time of the 1979 monograph publication. [^p01] He is named as joint author alongside [Robert S. Boyer](/software-engineering/robert-s-boyer.md) on the Library of Congress cataloging record: "Boyer, Robert S. *A Computational Logic* … I. Moore, J Strother, Date joint author." [^p01]

The monograph was published in the ACM Monograph Series (editor: Thomas A. Standish, University of California at Irvine) by Academic Press, a subsidiary of Harcourt Brace Jovanovich, 1979. [^p01]

## The 1979 monograph

*A Computational Logic* (ISBN 0-12-122950-5) covers automatic theorem proving, presenting a formal theory and a mechanical theorem prover. [^p01] Chapter coverage spans: the formal theory definition, proof heuristics (type information, rewrite rules, definition unfolding, destructor elimination), and worked verification examples including a tautology checker (Chapter 4). [^p01]

Research was supported by NSF Grant MCS-7681425 and ONR Contract N00014-75-C-0816. [^p01]

## Boyer-Moore string algorithm

Co-developer of the Boyer-Moore string searching algorithm (1977). Notably, the correctness of this algorithm is mechanically verified in Chapter 18 of the same 1979 monograph — the algorithm's authors used their own theorem prover to verify their concurrent algorithmic work. [^p01]

> [unsourced — please verify]: Chapter 18 specifically contains the Boyer-Moore string search verification; this is widely cited in formal-methods literature but not confirmed in the available source excerpt.

## ACL2

After SRI, Moore (with Matt Kaufmann) developed **ACL2** (A Computational Logic for Applicative Common Lisp), the industrial-strength successor to the Boyer-Moore prover. ACL2 has been used to formally verify AMD K5 floating-point division, Java bytecode, and microprocessor designs. [unsourced — general knowledge; not present in cited source]

## Related pages

- [Robert S. Boyer](/software-engineering/robert-s-boyer.md) — co-author and collaborator
- [Formal Verification and Mechanical Theorem Proving](/software-engineering/formal-verification.md) — technical context
- [A Computational Logic (source)](/software-engineering/sources/a-computational-logic-1979.md) — full source summary

[^p01]: [A Computational Logic — Part 1/12 (title page, preface)](../../raw/pdf/pdf-a-computational-logic-1979-part-01.md)

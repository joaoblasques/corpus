---
type: source
domain: software-engineering
status: draft
sources:
  - path: raw/pdf/pdf-code-simplicity-the-fundamentals-of-software-part-01.md
    channel: pdf
    ingested_at: 2026-07-22
  - path: raw/pdf/pdf-code-simplicity-the-fundamentals-of-software-part-02.md
    channel: pdf
    ingested_at: 2026-07-22
  - path: raw/pdf/pdf-code-simplicity-the-fundamentals-of-software-part-03.md
    channel: pdf
    ingested_at: 2026-07-22
aliases:
  - Code Simplicity
  - Code Simplicity the Fundamentals of Software
  - software design equation
  - law of change software
  - law of simplicity software
  - YAGNI software design
tags:
  - corpus/software-engineering
  - source
created: 2026-07-22
updated: 2026-07-22
---

# Code Simplicity: The Fundamentals of Software (Kanat-Alexander, 2012)

**TL;DR**: A short, opinionated software design book by Max Kanat-Alexander (O'Reilly, 2012; 80pp). Derives software design principles from first principles using an "Equation of Software Design." The central thesis: software exists to help people, and good design maximizes future value while minimizing maintenance effort. Laws are presented as empirical axioms that hold regardless of future specifics. 3 of 4 parts ingested (chapters 1-14 of 19 chapters; part 4 covers advanced topics not in these parts). [^cs-p01]

## The Equation of Software Design

The book's central framework: a change to software is desirable if and only if value > effort. The equation has two components:

- **Future value (V)**: the value the change provides to users over all future time
- **Maintenance effort (M)**: the ongoing effort to maintain the change over all future time

**Key insight**: the effort of implementation is nearly always insignificant compared to maintenance effort. Maintenance is what determines long-term desirability. The ideal design is one where maintenance effort decreases toward zero over time — then the change is always desirable regardless of future value. [^cs-p01]

**Quality rule**: "The quality level of your design should be proportional to the length of future time in which your system will continue to help people." Short-lived scripts need little design; long-lived systems need heavy investment. [^cs-p02]

## Laws of software design

### Law of Change
"The longer your program exists, the more probable it is that any piece of it will have to change." Approaching infinite future → approaching 100% probability any piece changes. Design implication: write flexible software, but do not predict what will change — only that it will. The three flaws in response to change: (1) writing code that isn't needed, (2) not making code easy to change, (3) being too generic. [^cs-p02]

**YAGNI**: "You Ain't Gonna Need It" — don't write code before needing it; can't predict the future, so wait until the need is concrete. Also: remove code that is no longer used — unused code develops bit rot and introduces confusion. Real-world data (4 files, 5-13 year histories): lines change 1.6× to 36× their original count over time; most original lines don't survive. [^cs-p02]

**Rigid design failure modes**: (1) making too many assumptions about the future (government healthcare system example: 4 years of planning → delivered wrong product); (2) writing code without enough design (bugzilla's `process_bug.cgi`: 3,000-line un-structured file, took a full year to redesign). [^cs-p02]

**Overengineering**: being too generic. "When your design makes things more complex instead of simplifying things, you're overengineering." Rule: "Be only as generic as you know you need to be right now." Real example: adding pluggable background-task systems before any user requested them; Chief Architect removed it; 4 years later, no customer needed it. [^cs-p02]

**Incremental development and design**: build piece by piece; fix up design before each new feature; keeps changes small; naturally avoids the three flaws. [^cs-p02]

### Law of Defect Probability
"The chance of introducing a defect into your program is proportional to the size of the changes you make to it." Best programmers: ~1 defect per 1,000 lines; average: ~1 per 100 lines. Implication: small changes = fewer defects = less maintenance. [^cs-p02]

Corollary: "Never 'fix' anything unless it's a problem, and you have evidence showing that the problem really exists." Premature optimization is the canonical violation — fixing a performance problem without evidence it exists.

**Don't Repeat Yourself (DRY)**: any piece of information should exist in exactly one place. Violations multiply maintenance cost proportionally to the number of copies. [^cs-p02]

### Law of Simplicity
"The ease of maintenance of any piece of software is proportional to the simplicity of its individual pieces." Note: about the simplicity of individual pieces, not the whole system (which is inherently too complex to comprehend entirely). Simpler pieces → understood by more readers → fewer bugs in changes → lower maintenance. [^cs-p03]

Architecture analogy: a 30-foot structure built from many small girders (easy to replace any piece) vs. three massive custom pieces (can't be removed to fix; must patch in place). Software has the same tradeoff. Perceived time savings of "big chunks" is illusory — the maintenance cost compounds.

Simplicity is relative: what is simple to the original author may be opaque to newcomers. Design documentation should be written "as if the reader knows nothing about the program." [^cs-p03]

## Connections to other corpus pages

- [Software Engineering (domain hub)](/software-engineering/README.md) — these laws are foundational to the domain's code design principles
- [Design of Approximation Algorithms](/software-engineering/sources/design-of-approximation-algorithms.md) — an example of a well-organized, incrementally-learnable book design
- [Algorithms](/software-engineering/algorithms.md) — related to the complexity vs. simplicity tradeoffs in algorithm selection for real systems

---

[^cs-p01]: raw/pdf/pdf-code-simplicity-the-fundamentals-of-software-part-01.md — Preface, Chapters 1-3: Introduction, Purpose of Software, The Equation of Software Design
[^cs-p02]: raw/pdf/pdf-code-simplicity-the-fundamentals-of-software-part-02.md — Chapters 4-5: Change (YAGNI, three flaws, incremental design, Law of Change real-world data), Defects and Design (Law of Defect Probability, DRY, premature optimization)
[^cs-p03]: raw/pdf/pdf-code-simplicity-the-fundamentals-of-software-part-03.md — Chapter 6: Simplicity (Law of Simplicity, architecture analogy, simplicity is relative, decreasing maintenance effort)

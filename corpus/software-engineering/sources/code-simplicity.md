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
  - path: raw/_inbox/pdf-code-simplicity-the-fundamentals-of-software-part-04.md
    channel: pdf
    ingested_at: 2026-07-23
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
updated: 2026-07-23
---

# Code Simplicity: The Fundamentals of Software (Kanat-Alexander, 2012)

**TL;DR**: A short, opinionated software design book by Max Kanat-Alexander (O'Reilly, 2012; 80pp). Derives software design principles from first principles using an "Equation of Software Design." The central thesis: software exists to help people, and good design maximizes future value while minimizing maintenance effort. Laws are presented as empirical axioms that hold regardless of future specifics. All 4 parts ingested (Chapters 1-8 + Appendices A-B). [^cs-p01]

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

## Handling Complexity

When existing complexity is too tangled to fix piecemeal, the approach is redesign through incremental steps — not rewrite. The Bugzilla multi-database redesign illustrates this: the team needed to support a second database (NewDB) in addition to its existing OldDB. Rather than rewriting, they proceeded in four independent steps: (1) replace all nonstandard database commands with standard equivalents file-by-file; (2) create wrapper functions for any remaining nonstandard commands and replace all call sites; (3) stop using OldDB-specific features in favor of portable alternatives; (4) redesign the installation system to support multiple databases generically. Each step was itself broken into smaller steps, and the system was tested after every change to confirm OldDB continued to work. The result was not perfect, but it was better — and eventually Bugzilla expanded to four database backends because this redesign made adding new ones tractable. [^cs-p04]

**Rewriting vs. redesign**: "Rewriting a system from the ground up is essentially an admission of failure as a designer." The book's position is that rewriting is acceptable only when all five conditions hold simultaneously: (1) experiments with redesigning the existing system show rewrite is more efficient; (2) there is a large time budget; (3) the new designer is substantially better than the original or has improved drastically; (4) the new system will be built incrementally with user feedback at each step; (5) resources exist to maintain the old system in parallel — never stop maintaining a system in use to free programmers for a rewrite. Otherwise, handle complexity through incremental redesign of individual pieces. [^cs-p04]

**Unfixable complexity**: Some complexity cannot be eliminated (e.g., complexity of underlying hardware). In these cases, the goal is to hide it: "Put a wrapper around it that is simple for other programmers to use and understand." [^cs-p04]

**Making one piece simpler**: The key question is always: "How could this be easier to deal with or more understandable?" Any true answer is a valid simplification. Design patterns, knowledge of multiple languages, and study of software engineering tools provide better answers, but the question itself is the core. Never apply a tool robotically — always do what is right for the specific code and situation. [^cs-p04]

## Law of Testing

"The degree to which you know how your software behaves is the degree to which you have accurately tested it." [^cs-p04]

This law covers when and why to test: there is no certainty a program will run in the future — only that it runs now. Environment changes, hardware migrations, and code modifications all re-introduce uncertainty. The corollary: "Unless you've tried it, you don't know that it works."

Testing is specific: a test must pose a precise question ("What happens when user presses X as first action after cold-start, having never started before?") and expect a precise answer. Vague tests yield vague knowledge.

Tests must be accurate (not falsely passing or falsely failing) and results must be observable (failures must be detectable and diagnostic).

After any code change, all code connected to the changed piece becomes unverified and must be re-tested. In practice this is handled by automated tests: write automated tests for every piece, run them after every change, and the full system is verified continuously with minimal manual effort. [^cs-p04]

## Summary: All 6 Laws

From Appendix A — the complete set of laws in the book: [^cs-p04]

1. **Purpose of software**: The purpose of software is to help people.
2. **Equation of Software Design**: Desirability of a change = (value now + future value) / (effort of implementation + effort of maintenance). As time goes on this reduces to: maintenance effort is more important to reduce than implementation effort.
3. **Law of Change**: The longer your program exists, the more probable it is that any piece of it will have to change.
4. **Law of Defect Probability**: The chance of introducing a defect into your program is proportional to the size of the changes you make to it.
5. **Law of Simplicity**: The ease of maintenance of any piece of software is proportional to the simplicity of its individual pieces.
6. **Law of Testing**: The degree to which you know how your software behaves is the degree to which you have accurately tested it.

The most important to keep in mind: the purpose of software, the reduced Equation (maintenance > implementation), and the Law of Simplicity. The book can be reconstructed from two sentences: "It is more important to reduce the effort of maintenance than it is to reduce the effort of implementation. The effort of maintenance is proportional to the complexity of the system." [^cs-p04]

## Connections to other corpus pages

- [Software Engineering (domain hub)](/software-engineering/README.md) — these laws are foundational to the domain's code design principles
- [Design of Approximation Algorithms](/software-engineering/sources/design-of-approximation-algorithms.md) — an example of a well-organized, incrementally-learnable book design
- [Algorithms](/software-engineering/algorithms.md) — related to the complexity vs. simplicity tradeoffs in algorithm selection for real systems

---

[^cs-p01]: raw/pdf/pdf-code-simplicity-the-fundamentals-of-software-part-01.md — Preface, Chapters 1-3: Introduction, Purpose of Software, The Equation of Software Design
[^cs-p02]: raw/pdf/pdf-code-simplicity-the-fundamentals-of-software-part-02.md — Chapters 4-5: Change (YAGNI, three flaws, incremental design, Law of Change real-world data), Defects and Design (Law of Defect Probability, DRY, premature optimization)
[^cs-p03]: raw/pdf/pdf-code-simplicity-the-fundamentals-of-software-part-03.md — Chapter 6: Simplicity (Law of Simplicity, architecture analogy, simplicity is relative, decreasing maintenance effort)
[^cs-p04]: raw/_inbox/pdf-code-simplicity-the-fundamentals-of-software-part-04.md — Chapter 7: Complexity (handling complexity, Bugzilla multi-database redesign, unfixable complexity, rewriting criteria); Chapter 8: Testing (Law of Testing, automated tests rationale); Appendix A: all 6 laws summary; Appendix B: complete facts/laws/rules/definitions

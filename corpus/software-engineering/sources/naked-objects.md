---
type: source
domain: software-engineering
status: draft
sources:
  - raw/pdf/pdf-naked-objects-part-01.md
  - raw/pdf/pdf-naked-objects-part-02.md
  - raw/pdf/pdf-naked-objects-part-03.md
  - raw/pdf/pdf-naked-objects-part-04.md
  - raw/pdf/pdf-naked-objects-part-05.md
  - raw/pdf/pdf-naked-objects-part-06.md
  - raw/pdf/pdf-naked-objects-part-07.md
  - raw/pdf/pdf-naked-objects-part-08.md
aliases:
  - Naked Objects thesis
  - Pawson PhD thesis
  - Naked Objects (Pawson 2004)
tags:
  - object-oriented
  - domain-driven-design
  - user-interface
  - MVC
  - agile
  - software-architecture
created: 2026-08-03
updated: 2026-08-03
---

# Naked Objects (PhD Thesis, Pawson 2004)

**Full title:** "Naked Objects" — A thesis submitted to the University of Dublin, Trinity College for the degree of Doctor of Philosophy  
**Author:** Richard Pawson, Department of Computer Science, Trinity College, Dublin  
**Date:** June 2004  
**Pages:** 223 (including 9 appendices)  
**Foreword by:** Trygve Reenskaug (inventor of MVC, external examiner)

## TL;DR

A PhD thesis arguing that the dominant 4-layer architecture for business systems (Presentation / Controller / Domain / Data) systematically destroys behavioural-completeness of domain objects by inserting use-case controllers. The solution: "naked objects" — expose domain objects directly to the user via a generic, auto-generated UI. All user actions are invocations of behaviour on those objects. Validated through two real case studies (Irish DSFA Child Benefit system, Safeway stores) and one controlled comparative experiment (CarServ). Demonstrated 4:1 reduction in code, faster development, improved agility, and better user empowerment.

## Thesis structure

- **Chapter 2**: Historical evolution of OO design (Simula → Smalltalk → MVC → 4-layer) and why use-case controllers emerged
- **Chapter 3**: The naked objects concept — its definition, two supporting frameworks, and four predicted benefits
- **Chapter 4**: DSFA case study (Irish government Child Benefit system)
- **Chapter 5**: Seven guidelines for designing naked object systems
- **Chapter 6**: Safeway case study (applying the guidelines)
- **Chapter 7**: CarServ controlled comparative experiment
- **Chapter 8**: Related work (OOUIs, empowering UIs, agile methodologies)
- **Chapter 9**: Conclusions
- **Appendices I–II**: DSFA's architecture principles and full business object responsibility definitions
- **Appendices III–VII**: Survey data (IT managers, business managers, users at DSFA; Safeway participants)
- **Appendix VIII**: CarServ change scenario metrics in full
- **Appendix IX**: Two published papers (OOPSLA 2001, XP2003)

## Core argument chain

1. Simula/Smalltalk conceived objects as **behaviourally-complete**: all functionality of an entity is encapsulated in it.[^p01]
2. MVC was invented to allow multiple views of a single object and to support multiple client platforms — separation of concerns, not separation of procedure from data.[^p01]
3. The **Controller** role in MVC was progressively distorted into a **use-case controller**: a procedural script governing a complete user task (e.g., Rumbaugh 1994: "one controller per use-case").[^p01]
4. This produced the **4-layer architecture** (Presentation / Controller / Domain / Data), where a single business concept like Customer exists in all four layers with complex many-to-many mappings — far from behaviourally-complete objects.[^p01]
5. Naked objects re-combine View and Controller into a completely generic presentation layer auto-generated from domain object definitions. All business functionality must therefore live on the domain objects. No use-case controllers are permitted.[^p01]

## The four predicted benefits (Chapter 3)

1. **Behaviourally-complete objects → more agile systems.** Changes localize to a single object; cross-cutting modifications are rare.[^p02]
2. **Faster development cycle.** The presentation layer is auto-generated; developers write no View/Controller code.[^p02]
3. **Common language between developers and users.** The domain object model is also the user interface model; users and developers prototype and iterate in the same representation.[^p02]
4. **More empowering user interface.** Noun-verb (object-action) interaction treats users as problem-solvers, not process-followers.[^p02]

## DSFA case study (Chapter 4)

Irish Department of Social and Family Affairs commissioned the *Naked Object Architecture* (originally *Expressive Object Architecture*) to replace a green-screen mainframe Child Benefit Administration system.

- **Architecture:** Java applet front-end communicating via XML/HTTP to COM+ business objects (VB 6.0) on Windows 2000; SQL Server persistence; Attunity Connect to legacy Oracle/OpenVMS CRS database.[^p02]
- **Went live:** November 2002, ~80 users, Letterkenny office.
- **Key finding:** "Once-and-done" claims processing — previously three officers handled one claim serially; now one officer handles the full claim end-to-end. Introduced as an organizational change without any change to the system design because naked objects never scripted the sequence of steps.[^p03]
- **User survey (15 users):** 15/15 agreed the new system contributed positively to job satisfaction; 13/15 strongly agreed on task flexibility; 13/15 strongly agreed they preferred no scripted guidance.[^p07]
- **Batch performance concern:** Object instantiation overhead per batch record; 95M association-table rows; solvable by pre-calculating forward payments on the Scheme object.[^p03]
- **Development cycle:** No speedup on first project due to parallel architecture build; expected on Phase II onward.[^p03]

## Seven design guidelines (Chapter 5)

1. **Select projects that benefit from problem-solver users** (requirements-dominated, not engineering-dominated; value-shop not value-chain).[^p03]
2. **Three pre-requisites:** strong OO modelling skills; a naked-objects framework; a shared understanding of the naked objects metaphor across all participants.[^p03]
3. **Two-phase structure: Exploration + Delivery.** Exploration is time-boxed, small team, prototype-first. Delivery starts from scratch.[^p03]
4. **During exploration, identify objects directly** — not from use-cases. Use informal conversation and Responsibility-Driven Design (Wirfs-Brock).[^p03]
5. **Capture object definitions directly into working code** using the framework. Objects are immediately visible to users as icons; behaviours show as pop-up menus.[^p03]
6. **Develop the production system one scenario at a time** (scenario = use-case or XP story or FDD feature); recode from scratch at delivery phase start.[^p04]
7. **Capture scenarios as executable user acceptance tests.** Because the generic viewing mechanism is stable, tests can be written as operations on business objects rather than as GUI event scripts.[^p04]

## Safeway case study (Chapter 6)

Two short projects at Safeway Stores (4th largest UK supermarket) in 2001: *Deal Nominations* (exploration only) and *Cluster-Based Pricing* (exploration + delivery). Guidelines from Chapter 5 explicitly applied.

- **Result:** All 10 participants agreed that naked objects greatly facilitated developer/user communication (median: strongly agree).[^p04]
- **Rapid prototyping:** All 10 agreed that prototyping the object model was at least as fast as conventional screenshot prototyping; several rated it faster.[^p04]
- **Exploration value:** 8/10 were strongly satisfied with exploration phase output; requirements identified that would not have surfaced with paper-based analysis.[^p04]
- **Limitation noted:** CBP was eventually re-implemented in CICS/Cobol due to platform constraints unrelated to the approach — but developers reported the naked objects prototype provided a superior specification.[^p04]

## CarServ comparative experiment (Chapter 7)

Same automotive dealership application implemented twice by the same developer (Dan Haywood), in the same language (Java), same IDE (Togethersoft Control Center):

- *CarServ1*: Conventional 4-layer (Presentation with Swing / Application / Domain / Data Management)
- *CarServ2*: Naked Objects framework, domain objects only

**Code metrics:**[^p04]

| Metric | CarServ1 | CarServ2 | Ratio |
|---|---|---|---|
| Classes | 190 | 27 | 7:1 |
| Methods | 788 | 230 | 3:1 |
| Lines of code | 7,304 | 1,726 | 4:1 |
| Avg methods/class | 4.1 | 8.5 | — |
| External classes used | 142 | 18 | 8:1 |
| Unique external methods | 411 | 56 | 7:1 |

**Agility test (3 change scenarios):** CarServ2 modifications took 25% less time on average and were much more localised (modifications to CarServ1 touched all four layers for each change).[^p04]

## Related work (Chapter 8)

- **Object-oriented user interfaces (OOUIs):** Xerox Star, IBM Common User Access, Collins's definition. Naked objects differs in that OOUI objects *must* correspond 1:1 to underlying domain objects — not just be visually object-oriented.[^p05]
- **Existing techniques for domain-object exposure:** Squeak Morphic (any Morph subclass is displayable; provides a "halo" of manipulation methods, but not aimed at behaviourally-complete business objects), IBM NEWI (no 1:1 commitment).[^p05]
- **Empowering UIs:** Clement's functional vs. democratic empowerment; Garson on anti-people automation bias; Hutchins/Hollan/Norman's "model world metaphor" vs. "conversation metaphor".[^p05]
- **Agile compatibility:**
  - *UP/RUP*: Poor match — use-case-driven analysis is definitional; EBC pattern conflicts with naked objects.[^p05]
  - *XP*: Strong match — system metaphor, simple design, incremental delivery, executable acceptance tests.[^p05]
  - *FDD*: Strong match — feature-by-feature delivery; object modelling up-front; feature syntax is `<action><result><object>`.[^p05]
  - *DSDM*: Compatible — prototyping emphasis, iterative delivery.[^p05]
  - *Agile Modelling*: Strongly resonant — naked objects eliminates tension between "modelling using simplest tools" and "prove it with code".[^p05]

## Limitations identified

1. **No hand-crafted UI:** Automatic UI means no per-task optimization. Workarounds: user-customizable layouts, use only for frequent-use internal systems.[^p03]
2. **Lack of explicit user guidance:** Not suitable for infrequent or self-service usage where scripted walkthroughs matter.[^p03]
3. **Batch processing:** Pure OO encourages many object instantiations per batch record; requires persistence patterns attention (e.g., pre-computing forward payments).[^p03]

## Two frameworks

1. **Naked Object Architecture (DSFA):** Proprietary; COM+ / VB; XML over HTTP; commissioned by the Irish government; renamed from "Expressive Object Architecture" in June 2003.[^p02]
2. **Naked Objects framework (open source):** Java; uses reflection to auto-generate UI; written by Robert Matthews; hosted at nakedobjects.org; >5000 downloads at time of writing; ported to .Net (C#/VB.Net).[^p02][^p08]

## Key citations from the thesis

- Reenskaug on MVC origins: "Its purpose was to bridge the gap between the user's mind and the computer-held data."[^p01]
- Reenskaug on the original direct-manipulation pre-MVC ideal: "MVC was an outgrowth of the original direct-manipulation metaphor popularized in early OO practice... MVC actually works against that metaphor but evolved as a necessary evil."[^p01]
- Alan Kay on the auto-UI idea: "One of the original motivations for the models, views and controller idea (that, in my opinion, never got well done) was to be able to automatically produce a default graphical interface for any object."[^p05]
- Firesmith on use-case controllers: "a single functional control object representing the logic of an individual use-case and several dumb entity objects controlled by the controller object"[^p03]

[^p01]: raw/pdf/pdf-naked-objects-part-01.md — Pawson, R. "Naked Objects." PhD Thesis, Trinity College Dublin, June 2004. Chapters 1–3 (pp. 9–27).
[^p02]: raw/pdf/pdf-naked-objects-part-02.md — Pawson (2004), Chapters 3–4 (pp. 26–50).
[^p03]: raw/pdf/pdf-naked-objects-part-03.md — Pawson (2004), Chapters 4–5 (pp. 50–72).
[^p04]: raw/pdf/pdf-naked-objects-part-04.md — Pawson (2004), Chapters 5–7 (pp. 72–95).
[^p05]: raw/pdf/pdf-naked-objects-part-05.md — Pawson (2004), Chapters 8–9 (pp. 96–120).
[^p06]: raw/pdf/pdf-naked-objects-part-06.md — Pawson (2004), Bibliography + Appendix I–II (pp. 121–141).
[^p07]: raw/pdf/pdf-naked-objects-part-07.md — Pawson (2004), Appendices III–V, surveys (pp. 142–186).
[^p08]: raw/pdf/pdf-naked-objects-part-08.md — Pawson (2004), Appendices VI–IX (pp. 187–223).

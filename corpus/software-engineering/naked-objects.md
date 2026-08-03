---
type: concept
domain: software-engineering
status: draft
confidence: 0.9
last_confirmed: 2026-08-03
sources:
  - raw/_inbox/pdf-naked-objects-part-01.md
  - raw/_inbox/pdf-naked-objects-part-02.md
  - raw/_inbox/pdf-naked-objects-part-03.md
  - raw/_inbox/pdf-naked-objects-part-04.md
  - raw/_inbox/pdf-naked-objects-part-05.md
  - raw/_inbox/pdf-naked-objects-part-06.md
  - raw/_inbox/pdf-naked-objects-part-07.md
  - raw/_inbox/pdf-naked-objects-part-08.md
aliases:
  - Naked Objects
  - naked objects pattern
  - Expressive Object Architecture
  - NOA
  - behaviourally-complete objects
  - OOUI
  - object-oriented user interface
tags:
  - object-oriented
  - domain-driven-design
  - user-interface
  - architecture
  - agile
  - behavioural-completeness
created: 2026-08-03
updated: 2026-08-03
---

# Naked Objects

**TL;DR:** A software design approach where domain entity objects are exposed directly to the user via an auto-generated generic UI. All user actions are invocations of behaviour on those domain objects — no use-case controllers, no hand-crafted presentation layer. Enforces behavioural-completeness of the domain model, producing systems that are more agile, faster to develop, and more empowering for users. Validated in production (Irish government, Safeway) and by a controlled experiment (4:1 code reduction, 25% faster change implementation).

## The core problem

Most object-oriented business systems design violates the original OO ideal of **behaviourally-complete** objects — where all functionality associated with an entity is encapsulated in that entity, not implemented as external procedures.[^p01]

The dominant cause: the **use-case controller** pattern, which places business logic in procedure objects sitting above behaviourally-thin domain entities (Fowler's "Transaction Script" territory). This is sometimes deliberately adopted (Unified Process EBC pattern) and sometimes an accidental consequence of [MVC](/software-engineering/model-view-controller.md) adoption.[^p01]

The consequences:
- **Excessive coupling** across objects and layers[^p01]
- **Low agility**: changes require modifications in multiple layers[^p01]
- **Dumb entity objects**: Customer, Product, Order hold data but minimal behaviour[^p01]

## The naked objects solution

> "The solution… is to make the View and Controller roles (as originally defined in MVC) completely generic. In such an approach a business application is written solely in terms of the domain entity (i.e. Model) objects."[^p01]

A business application consists only of domain objects. A framework provides a completely generic presentation layer — a "viewing mechanism" — that:

1. Introspects the domain objects at runtime (using Java reflection or equivalent)
2. Renders each object as an icon; double-click opens an attribute/association view
3. Exposes behaviours (methods prefixed with `action`) as right-click pop-up menu options
4. Enables single-parameter methods via drag-and-drop (drop object A onto object B)
5. Renders class-level operations (create new instance, find by criteria) via class icons

The user sees and interacts directly with business domain objects. As far as the user is concerned, they are manipulating the "naked" business objects themselves.

## Behavioural completeness

**Definition:** All behaviours associated with an entity that are necessary to the application are encapsulated in that entity, not implemented somewhere else in the system.[^p01]

Naked objects enforce this in two ways:
- **Negative:** There is nowhere in the architecture to put business functionality except on the domain objects
- **Positive:** The visual concreteness of domain objects makes it easier to identify their natural responsibilities[^p01]

Term originates with Simula (Dahl & Nygaard, 1966): each Wheel object "not only knows the dimensions and mass of a wheel, but also knows how to turn, to bounce, to model friction."[^p01]

## Noun-verb (object-action) interaction

Naked objects implement the **noun-verb** or **object-action** interaction style:[^p01]
- User selects an object (noun), then selects a behaviour (verb) from its context menu
- Contrast with the prevalent **verb-noun** style: user selects a task from a menu, then specifies the data

The noun-verb style is the defining characteristic of object-oriented user interfaces (OOUIs). IBM's Common User Access (1991) called this out as a first principle. Naked objects make OOUIs trivial to implement — any system gets a pure OOUI "for free" by defining behaviourally-complete domain objects.[^p05]

## Purposeful vs. non-purposeful objects

**Non-purposeful objects** (Customer, Employee, Product, Location): state is an agglomeration of attributes; changes are random direction.[^p02]

**Purposeful objects** (Order, Transfer, Case, Booking): state advances in a pre-ordained direction through an explicit state machine. Broadly equivalent to Coad's "moment-interval" archetype.[^p02]

Purposeful objects replace use-case controllers. A bank Transfer is not a transient controller — it is a persistent entity object the user can inspect, reverse, or annotate long after completion. Any business activity where a verb easily mutates into a noun ("adjust prices" → "PriceAdjustment") is a candidate for a purposeful object.[^p02]

## Access control without controllers

Domain objects in a naked objects system can control their own availability:

- An `aboutActionConfirm()` method on a Booking object controls when `actionConfirm()` is available, based on the object's state or an authorization server lookup
- The viewing mechanism greys out unavailable actions, hides inaccessible fields, provides tooltip explanations[^p02]

This preserves encapsulation: access control logic lives on the object it governs, not in a separate controller.

## Four benefits (empirically validated)

### 1. Behavioural completeness → greater agility

CarServ experiment: 4 change scenarios implemented on both conventional and naked-objects versions by the same developer. CarServ2 (naked objects) required 25% less time and modifications stayed localised — each change touched domain objects only, vs. all four layers in CarServ1.[^p04]

DSFA: Late requirement changes were accommodated "without difficulty" during development; "once-and-done" org change was implemented after go-live without touching the system.[^p03]

### 2. Faster development cycle

CarServ metrics — CarServ2 vs. CarServ1:[^p04]
- 7:1 fewer classes (27 vs. 190)
- 4:1 fewer lines of code (1,726 vs. 7,304)
- 8:1 fewer external classes referenced (18 vs. 142)

The framework is simpler to learn than Swing: no UI class libraries to master.

Safeway survey (10 participants): all agreed naked objects prototyping was at least as fast as conventional screen prototyping; several rated it faster.[^p04]

### 3. Common language between developers and users

Because the domain object model is also the user interface model, both parties can prototype and iterate in real time using the same representation. Requirements gathering and domain modelling fuse into one activity.

DSFA IT managers survey (7): 7/7 agreed the approach directly facilitated developer/user communication.[^p03]
Safeway survey (10): 10/10 agreed (8 strongly).[^p04]

### 4. Empowering user interface

DSFA user survey (15 users of the live Child Benefit system): 15/15 agreed the new system contributed positively to job satisfaction (10 strongly). 13/15 strongly valued the task flexibility. 12/15 disagreed with "I would prefer the system to guide me through the steps." 9/15 felt empowered (6 were puzzled by the term, not disagreeing).[^p07]

> "My doing it differently no longer means that I am doing it wrong." — DSFA user[^p07]

## Three limitations

1. **No hand-crafted UI.** Auto-generated UI cannot be optimised per-task. Safety-critical, high-graphical, or marketing-critical interfaces need conventional UI, though naked objects could still be used to prototype the business model.[^p03]

2. **No scripted user guidance.** Naked objects are a problem-solver's interface, not a process-follower's. Unsuitable for infrequent/self-service use cases where users need to be guided through steps.[^p03]

3. **Batch processing tension.** Pure OO forces many object instantiations per batch record. Solution at DSFA: pre-compute forward payment values on the Scheme object to reduce per-record instantiations. The problem is not caused by naked objects but is brought into sharper focus by the pure OO model.[^p03]

## When to use naked objects

**Use naked objects when ANY of:**
- User role benefits from problem-solver framing (vs. process-follower)
- Future business agility is a primary concern
- Requirements are uncertain or likely to change

**AND ALL of:**
- No clear rationale for a hand-crafted UI
- Users are frequent users of the system
- Batch processing is simple or can be treated as a separate system[^p03]

**Good domains:** pricing/promotions, trading, risk management, resource planning, emergency response, campaign management, government benefits administration, any "value shop" (Stabell & Fjeldstad) vs. "value chain" business model.

**Poor fit:** airline reservation systems, telecom billing (engineering-dominated, high-volume, strict process compliance required).

## Framework implementation (Naked Objects framework)

Java open-source framework by Robert Matthews. Uses Java reflection:

- Methods prefixed `action` become pop-up menu items
- Methods prefixed `get` returning an object become fields (with drag-drop if a matching `set` exists)
- Methods prefixed `about` (e.g., `aboutActionConfirm()`) control availability of their paired method
- Object classes are rendered as class icons with class-level operations (create, find, list)[^p08]

Ported to .Net (C#/VB.Net). First deployed in DSFA's proprietary Naked Object Architecture (COM+/VB6, XML/HTTP transport).

## Executable acceptance tests

Because the viewing mechanism is completely generic and stable, test harnesses can simulate user interactions as sequences of method calls on business objects — without recording/replaying GUI events. Tests can be written before the functionality is implemented, yielding genuine test-driven development for business systems (XP's acceptance testing ideal, which is rarely practiced due to GUI testing difficulty).[^p04]

The Naked Objects framework includes a test harness that auto-generates HTML user documentation from the same test scripts, making the tests double as training material.[^p04]

## Design guidelines summary

Seven guidelines from Chapter 5:[^p03][^p04]

1. Select projects that fit the problem-solver/requirements-uncertain profile
2. Ensure team has OO modelling skills, a naked objects framework, and shared metaphor understanding
3. Structure as Exploration phase (time-boxed, prototype) followed by Delivery phase (rewrite from scratch)
4. During exploration, identify objects directly — not from use-cases
5. During exploration, capture object definitions directly into working code (not UML first)
6. In delivery, develop one scenario at a time; use-cases acceptable here (objects already defined)
7. Capture scenarios as executable user acceptance tests

## Agile methodology compatibility

| Methodology | Compatibility | Key tension |
|---|---|---|
| UP/RUP | Poor | Use-case-driven analysis is definitional; EBC pattern conflicts with naked objects |
| XP | Strong | System metaphor, simple design, executable acceptance tests |
| FDD | Strong | Feature syntax `<action><result><object>` maps to object methods |
| DSDM | Compatible | Prototyping and iterative delivery emphasis matches |
| Agile Modelling | Strong | Eliminates tension between light modelling and "prove it with code" |

[^p01]: raw/_inbox/pdf-naked-objects-part-01.md — Pawson, R. "Naked Objects." PhD Thesis, Trinity College Dublin, June 2004. Chapters 1–3 (pp. 9–27).
[^p02]: raw/_inbox/pdf-naked-objects-part-02.md — Pawson (2004), Chapters 3–4 (pp. 26–50).
[^p03]: raw/_inbox/pdf-naked-objects-part-03.md — Pawson (2004), Chapters 4–5 (pp. 50–72).
[^p04]: raw/_inbox/pdf-naked-objects-part-04.md — Pawson (2004), Chapters 5–7 (pp. 72–95).
[^p05]: raw/_inbox/pdf-naked-objects-part-05.md — Pawson (2004), Chapters 8–9 (pp. 96–120).
[^p07]: raw/_inbox/pdf-naked-objects-part-07.md — Pawson (2004), Appendices III–V, surveys (pp. 142–186).
[^p08]: raw/_inbox/pdf-naked-objects-part-08.md — Pawson (2004), Appendix VI — Naked Objects framework description (pp. 187–189).

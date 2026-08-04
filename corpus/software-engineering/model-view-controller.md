---
type: concept
domain: software-engineering
status: draft
confidence: 0.9
last_confirmed: 2026-08-03
sources:
  - raw/pdf/pdf-naked-objects-part-01.md
aliases:
  - MVC
  - Model-View-Controller
  - model view controller
  - MVC pattern
tags:
  - architecture
  - design-patterns
  - object-oriented
  - user-interface
  - Smalltalk
  - Xerox-PARC
created: 2026-08-03
updated: 2026-08-03
---

# Model-View-Controller (MVC)

**TL;DR:** An architectural pattern invented by Trygve Reenskaug at Xerox PARC in 1978/79 to allow a single domain object (Model) to be rendered in multiple ways (Views) with separate input handling (Controllers). Designed to support the simultaneous multiple representations needed in business applications — not to separate business logic from domain objects. Its Controller role was later distorted into a "use-case controller" (a procedural script), which became the primary driver of behaviourally-thin domain objects and the 4-layer architecture that dominates business systems today.

## Origin

MVC was invented by [Trygve Reenskaug](/software-engineering/trygve-reenskaug.md) as a visiting scientist at Xerox PARC in 1978/79, in the context of Smalltalk development. The earliest document is from 1979 ("Thing-Model-View-Editor"); it was not publicly documented until 1988 (Krasner & Pope, JOOP).

The motivation came from a fundamental tension in Smalltalk. Early Smalltalk (up to Smalltalk-76) defined that "all objects are active, ready to perform in full capacity at any time. Nothing of this liveness should be lost at the interface to the human user." Objects presented themselves directly to the user.

This worked when each object had one representation. But when Smalltalk became applicable to business (where users are not programmers), objects needed to be viewed in multiple ways: as a graph, as a table, in different business contexts. Direct self-presentation could no longer support this.[^p01]

Reenskaug's own summary of the problem:

> "Each object can only appear once on the screen and must always be presented in the same way to preserve the illusion of concreteness. This is insufficient for large and complex models where we need to view objects in different ways."[^p01]

## The three archetypes

**Model:** Represents a domain entity — both its state (attributes, relationships) and its behaviour. Multiple Views can share one Model.

**View:** Creates a user representation of a Model object; handles all display interfacing. One Model can have multiple Views. Ideally presents exactly one Model object.

**Controller:** Handles user input on a given View; interfaces with the input device; updates the associated Model and View as needed.

The principal intent: **separation of concerns**. Changing the visual representation or porting to a new client platform requires changing only View and Controller — the Model object remains untouched.[^p01]

## Pre-MVC: objects presented themselves

Before MVC, Smalltalk objects were able to represent themselves directly to the user. This simpler model did not encourage separation of data and procedure. Its limitation was the lack of flexibility for multiple simultaneous views of the same object.

Reenskaug noted this loss explicitly:

> "MVC was an outgrowth of the original direct-manipulation metaphor popularized in early OO practice... MVC actually works against that metaphor but evolved as a necessary evil."[^p01]

Alan Kay, who led the Learning Research Group at PARC where Smalltalk was developed, reflected later:

> "One of the original motivations for the models, views and controller idea (that, in my opinion, never got well done) was to be able to automatically produce a default graphical interface for any object (and Steve Putz at PARC actually did a version of this but it didn't stick)."[^p01]

## Known shortcomings of MVC

**Encapsulation challenge:** MVC requires extracting self-presentation behaviour from the domain object and placing it in a View. This deliberately breaches the principle that objects contain all their own behaviour. As Holub stated:

> "MVC is okay for implementing little things like buttons, but it fails as an application-level architecture. This extract-data-then-shove-it-elsewhere approach requires you to know too much about how the model-level objects are implemented."[^p01]

**Close coupling of views and controllers to model:** Both View and Controller make direct calls to the Model. Changes to the Model's interface can cascade into both (Buschmann et al.).[^p01]

**Extraction pressure:** Once a clean Model/View/Controller split is established, there is strong pressure to place small pieces of business logic into Views (e.g., running invoice totals) and into Controllers (flow control, sequencing). This is the origin of the use-case controller problem.

**Reenskaug's own assessment:**

> "The Model-View-Controller paradigm extends the power of the user interface at the expense of increased demands on the user's mental model."[^p01]

## The Controller distortion: use-case controllers

The Controller role was originally defined as being concerned solely with managing input. Over time this was progressively distorted so that "Controller" came to mean "governing the flow of control associated with a complete user task."

Rumbaugh (1994): "the state diagram of a controller defines the allowable sequences of interactions inherent in a use case... Start by assuming one controller per use case."[^p01]

Fowler defined the "use-case controller" as an explicit pattern, positioned closer to the "Transaction Script" (procedural) than the "Domain Model" pattern. This pattern was adopted by the Unified Process as the "Control" object in the Entity-Boundary-Control (EBC) pattern.[^p01]

The result: business logic that naturally belongs to a Customer or Order object is instead placed in a procedure called `ProcessClaimController` or `PlaceOrderUseCase`.

## The 4-layer architecture

MVC's distorted Controller role directly enabled the **4-layer generic architecture** (first recorded by Brown, 1995, but practiced earlier):

1. **Presentation layer** — views and screens
2. **Controller/Application layer** — use-case controllers, workflow
3. **Domain object layer** — behaviourally-thin entity objects
4. **Data management layer** — ORM, persistence

A single business concept (Customer) is represented in all four layers with complex many-to-many mappings between layers. This is the "dominant design" for contemporary business systems.[^p01]

## Relationship to naked objects

[Naked objects](/software-engineering/naked-objects.md) addresses the original MVC problem — how to support multiple client platforms and visual representations — without creating use-case controllers.

The naked objects solution: make the View and Controller roles **completely generic** (provided by a framework) and derive all UI representations automatically from domain object definitions. This:
- Restores the pre-MVC ideal of objects presenting themselves to the user
- Preserves MVC's separation-of-concerns benefit (Model is cleanly separated from presentation)
- Prevents the insertion of use-case controllers (there is nowhere to put them)

The key design constraint is **enforced 1:1 correspondence** between the user-visible objects and the underlying domain model objects. Existing work on OOUIs did not require this correspondence; naked objects does.[^p05]

## Variants and successors

- **EBC pattern (Unified Process):** Entity, Boundary, Control. Combines View+Controller into a single Boundary object; adds a Control object that governs use-case flow. Superficially similar to MVC but fundamentally different in intent — the Control object is explicitly a use-case controller.
- **Morphic (Squeak/Self):** Any object inheriting from `Morph` is automatically displayable with a "halo" of manipulation methods. Closer in spirit to pre-MVC self-presentation, but not aimed at business systems or behaviourally-complete entities.
- **Model-View-Presenter (MVP) / Model-View-ViewModel (MVVM):** Later evolutions in the .Net/WPF/mobile ecosystem; move some display logic into the Presenter/ViewModel to ease testing, but do not address the use-case controller problem.

[^p01]: raw/pdf/pdf-naked-objects-part-01.md — Pawson, R. "Naked Objects." PhD Thesis, Trinity College Dublin, June 2004. Chapter 2: "The Evolution of Object-Oriented Design" (pp. 15–23), referencing Reenskaug (1979, 1988, 1996), Rumbaugh (1994), Fowler (2003), Holub (1999), Buschmann et al. (1996).
[^p05]: raw/pdf/pdf-naked-objects-part-05.md — Pawson (2004), Chapter 8: "Related Work" (pp. 96–103), referencing Collins (1995), IBM CUA (1991), Tesler (1983).

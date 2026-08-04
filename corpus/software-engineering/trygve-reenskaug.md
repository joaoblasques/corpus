---
type: entity
domain: software-engineering
status: draft
confidence: 0.9
last_confirmed: 2026-08-03
sources:
  - raw/pdf/pdf-naked-objects-part-01.md
aliases:
  - Trygve Reenskaug
  - Reenskaug
tags:
  - person
  - object-oriented
  - MVC
  - Smalltalk
  - Xerox-PARC
created: 2026-08-03
updated: 2026-08-03
---

# Trygve Reenskaug

**TL;DR:** Norwegian computer scientist; inventor of the Model-View-Controller (MVC) architectural pattern, developed at Xerox PARC in 1978/79. Pioneer of object-oriented programming. Served as external examiner for Richard Pawson's Naked Objects PhD thesis at Trinity College Dublin (2004), for which he wrote the foreword.

## Key contribution: MVC

Reenskaug invented [MVC](/software-engineering/model-view-controller.md) while a visiting scientist at Xerox PARC in 1978/79, working on Smalltalk. The earliest document is "Thing-Model-View-Editor" (1979). The pattern was not publicly documented until Krasner & Pope's 1988 JOOP article.[^p01]

**Original motivation:** The direct self-presentation model of early Smalltalk (where objects "present themselves to the user in an effective way") was insufficient when an object needed to be viewed in multiple ways simultaneously — as a table, a graph, in different business contexts.[^p01]

**Original intent (Reenskaug's own words, 2004):**
> "Its purpose was to bridge the gap between the user's mind and the computer-held data. The centre of this solution was the Model that was a representation of the user's domain information."[^p01]

**On the original MVC vs. Smalltalk-80 MVC:**
> "The original MVC was later modified in Smalltalk-80 to become a technical solution that separated input, output and information. The most important participant in the original MVC architecture, the user's mind, was somehow forgotten."[^p01]

**On the Controller becoming a use-case controller:**
> "I have been told that in many implementations of the 'well known MVC paradigm', the 'C' is implemented as a script controlling the user's actions."[^p01]

## Philosophy: empowering users

Reenskaug's career was consistently oriented toward empowering users. His earlier work:

- **Autokon system (Stord Yard, 1963):** Designed to empower ship designers; central database in shipbuilding terminology; "human-centric, reflecting the nature of shipbuilding and the everyday life of the shipbuilder."[^p01]
- **Distributed planning and control system (1970s):** Goal was "that the users' mental models should correspond to the models built into the computer." MVC emerged from this goal.[^p01]

He draws on Douglas Engelbart's 1962 vision of "augmenting human intellect" and Alan Kay's Smalltalk work.[^p01]

**On the two traditions in computing:**
> "There are two traditions in the applications of computers; one is to employ the computer to empower its users, and the other is to apply the computer to control its users. I am sorry to say that the latter seems to be prevalent in mainstream computing today."[^p01]

## Endorsement of naked objects

In the foreword to Pawson's thesis, Reenskaug wrote:

> "If the original MVC had been published at the time, Naked Objects would now appear as an important extension and implementation of its ideas. As it is, the original MVC was not published at the time and Richard Pawson's Naked Objects appear as an important and independent contribution."[^p01]

He highlighted two contributions of naked objects:
1. Augmenting the human mind per Engelbart's vision, with domain objects as the shared model
2. Objects presenting themselves to the user in a standardised way — auto-generated UI, direct contact with the domain model[^p01]

## References in the Pawson thesis

- Reenskaug, T. "Thing-Model-View-Editor." Xerox PARC, 1979. [earliest MVC document]
- Reenskaug, T. "Working with Objects in the User Interfaces." *ObjectEXPERT*, 1996.
- Reenskaug, T. "Model View Controller." Portland Pattern Repository, c2.com.
- Krasner, G. and Pope, S. "A cookbook for using the Model-View-Controller user interface paradigm in Smalltalk-80." *JOOP*, 1988, 1(3), pp. 26–49. [first public MVC documentation]

[^p01]: raw/pdf/pdf-naked-objects-part-01.md — Pawson, R. "Naked Objects." PhD Thesis, Trinity College Dublin, June 2004. Foreword by Trygve Reenskaug (pp. 2–4); Chapter 2 "The Evolution of Object-Oriented Design" (pp. 15–23).

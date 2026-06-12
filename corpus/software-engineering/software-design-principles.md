---
type: concept
domain: software-engineering
status: draft
sources:
  - path: 03_Resources/Study Notes/Python - Production Code Principles Senior Developer.md
    channel: notes
    ingested_at: 2026-05-21
  - path: raw/_inbox/email-2026-06-09-design-patterns-suck.md
    channel: email
    ingested_at: 2026-06-12
aliases:
  - software design principles
  - clean code principles
  - SOLID
  - single responsibility principle
  - SRP
  - open/closed principle
  - dependency injection
  - design patterns
  - Gang of Four
  - GoF
tags:
  - corpus/software-engineering
  - concept
created: 2026-05-21
updated: 2026-06-12
---

# Software Design Principles

**TL;DR**: Eight code-level design principles that distinguish maintainable, production-grade software from code that merely works. Collectively operationalize the question seniors ask that juniors don't: "Can I maintain it, test it, and will it scale?" [^src1]

## The eight principles

| Principle | Core idea | Anti-pattern |
|---|---|---|
| **Cohesion / SRP** | One reason to change per class or function | `UserManager` validates + writes DB + sends email |
| **Encapsulation / Abstraction** | Hide implementation; expose only the interface | Public `_balance` field on a bank account |
| **Loose coupling / Modularity** | Components independent; change one without breaking others | Hard-coded `self.db = MySQLDatabase()` inside a service |
| **Reusability / Extensibility** | Extend without modifying existing code (Open/Closed) | `if type == "A"` blocks instead of polymorphism |
| **Portability** | Same code, different environments; no hardcoded paths | Config in code rather than env vars |
| **Defensibility** | Handle edge cases; fail loudly; use type hints | Silent `except:` swallowing errors |
| **Maintainability / Testability** | Pure functions; injectable dependencies; small units | Global state; un-mockable hard dependencies |
| **Simplicity** | Simplest solution that meets requirements | "We might need this later" [^src1] |

## Dependency injection pattern

The primary mechanism for achieving loose coupling — pass dependencies in rather than constructing them internally [^src1]:

```python
# Tightly coupled — hard to test or swap
class OrderService:
    def __init__(self):
        self.db = MySQLDatabase()

# Loosely coupled — injectable, mockable
class OrderService:
    def __init__(self, database):
        self.db = database
```

## Design patterns: vocabulary, not dogma

A contrasting source argues the Gang of Four's 23 patterns (1994) have been "elevated from useful vocabulary into something closer to dogma" — taught as universal solutions, applied where unneeded, treated as a mark of good engineering [^src2]. Its central claim:

> "Design patterns aren't solving problems with your code; they're solving problems with your language." [^src2]

Many GoF patterns are workarounds for missing language features [^src2]. Java's verbose ~15-line `Singleton` collapses to `object Logger` in Scala; a Factory is "just Java's refusal to give you proper constructors"; an Observer is trivial when functions are first-class. "In a language that's expressive enough, patterns either become trivial or ... just don't exist." [^src2] This is framed as the **Gosling vs Guido philosophy**: Java was built rigid to protect average developers from themselves (patterns route everything through class hierarchies), while Python optimizes for clarity and gives direct tools (first-class functions, decorators, context managers, duck typing) [^src2].

**The honest value of patterns**: "giving a short name to a big idea" — it's easier to say "that's a facade" than re-explain a wrapper each time [^src2]. Patterns are "for talking about code that's already written," not a checklist to apply [^src2]. The failure mode is **overengineering** — shoehorning patterns in solves "imaginary problems," producing labyrinths of interfaces. The evaluation rule is the **simplicity principle** above: weigh the technique's benefit against its cost. "If your solution needs a diagram to explain it, you've gone too far." [^src2] A developer who internalizes separation of concerns, encapsulation, and composition over inheritance "will write clean code naturally, even if they've never heard the word 'Singleton'" [^src2].

This connects to the maintainability cost of AI-generated code — see [[software-engineering/ai-assisted-development|AI-Assisted Development]], where the same simplicity discipline guards against AI-amplified over-abstraction.

## Relationship to architecture-level patterns

SRP and cohesion operate at the code level, but the same principle drives [[software-engineering/microservices|microservices]] decomposition at the service level — each service should have one reason to change, with clear boundaries and limited proliferation. Hype-driven microservices adoption often violates the simplicity principle: services are added before the complexity is warranted [^src1].

## See also

- [[software-engineering/microservices|Microservices]] — service-level application of SRP, cohesion, and loose coupling
- [[software-engineering/distributed-systems-fallacies|Distributed Systems Fallacies]] — distributed context where defensibility (explicit failure handling) becomes critical
- [[software-engineering/ai-assisted-development|AI-Assisted Development]] — deep modules, simplicity, and testability under AI code generation
- [[software-engineering/README|Software Architecture hub]]

---

[^src1]: [[03_Resources/Study Notes/Python - Production Code Principles Senior Developer|Python - Production Code Principles Senior Developer]]
[^src2]: [Design Patterns Suck](../../raw/email/email-2026-06-09-design-patterns-suck.md)

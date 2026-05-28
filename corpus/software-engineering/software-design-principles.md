---
type: concept
domain: software-engineering
status: draft
sources:
  - path: 03_Resources/Study Notes/Python - Production Code Principles Senior Developer.md
    channel: notes
    ingested_at: 2026-05-21
aliases:
  - software design principles
  - clean code principles
  - SOLID
  - single responsibility principle
  - SRP
  - open/closed principle
  - dependency injection
tags:
  - corpus/software-engineering
  - concept
created: 2026-05-21
updated: 2026-05-21
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

## Relationship to architecture-level patterns

SRP and cohesion operate at the code level, but the same principle drives [[software-engineering/microservices|microservices]] decomposition at the service level — each service should have one reason to change, with clear boundaries and limited proliferation. Hype-driven microservices adoption often violates the simplicity principle: services are added before the complexity is warranted [^src1].

## See also

- [[software-engineering/microservices|Microservices]] — service-level application of SRP, cohesion, and loose coupling
- [[software-engineering/distributed-systems-fallacies|Distributed Systems Fallacies]] — distributed context where defensibility (explicit failure handling) becomes critical
- [[software-engineering/README|Software Architecture hub]]

---

[^src1]: [[03_Resources/Study Notes/Python - Production Code Principles Senior Developer|Python - Production Code Principles Senior Developer]]

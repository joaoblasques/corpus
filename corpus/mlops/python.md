---
type: concept
domain: mlops
status: draft
sources:
  - path: raw/youtube/youtube-Gx5qb1uHss4-10-important-python-concepts-in-20-minutes.md
    channel: youtube
    ingested_at: 2026-06-15
aliases:
  - Python
  - python language
  - python concepts
  - type annotations
  - dunder methods
tags:
  - corpus/mlops
  - concept
created: 2026-06-15
updated: 2026-06-15
---

# Python

**TL;DR**: A reference for core Python language concepts — variables, data types, type annotations, functions, classes/methods, and dunder methods [^src1]. This is the **general-purpose language page** for the corpus; the data-engineering and AI-engineering domains build on Python but defer the language fundamentals here. `.py` files are executed by the Python interpreter [^src1].

## Data types

Basic types: **int** (whole number), **float** (decimal), **str** (text in quotes), **bool** (`True`/`False`) [^src1]. Collections [^src1]:

| Type | Property |
|---|---|
| **list** | ordered, mutable (add/remove elements) |
| **tuple** | ordered, **immutable** (fixed once set) |
| **set** | unordered, **no duplicates** (guaranteed unique) |
| **dict** | key→value pairs |

## Type annotations

Annotations (`name: str = "Bob"`) are **optional and do nothing at runtime** — the program still runs even if a value's type contradicts its annotation [^src1]. Their value is editor warnings: the analogy given is a traffic light — it doesn't physically stop you, it warns you you're about to make a mistake [^src1].

**Constants**: Python has no true constants. Convention is `UPPERCASE` names; `typing.Final` makes the editor warn on reassignment (`VERSION: Final[str] = "1.0"`) — but the value can still be changed at runtime [^src1].

## Functions

Defined with `def`; a function with no return value can be explicitly typed `-> None` [^src1]. Functions exist to make code **reusable** — define logic once so a change updates everywhere it's called, rather than copy-pasting [^src1]. Parameters add customization (`def greet(name: str) -> None`); a return type (`-> float`) lets the editor flag a wrong-typed return [^src1].

## Classes & methods

A class is a **blueprint** for objects [^src1]:

- **`__init__`** (initializer) sets up an instance from specific data; always returns `None` [^src1].
- **`self`** refers to the instance; attributes are assigned as `self.brand = brand` and accessed via `self` inside the class [^src1].
- Instantiation (`Car("Volvo", 200)`) creates a customized object from the blueprint [^src1].
- A **method** is just a function defined inside a class; the first parameter is `self`, and any params after `self` are ordinary arguments referenced without `self` [^src1].

## Dunder methods

"Dunder" = double-underscore methods that hook into language operations [^src1]:

- **`__str__`** — returns the string shown when the object is printed (without it, `print(obj)` shows a memory-address representation) [^src1].
- **`__add__(self, other)`** — defines `+` for the type; without it Python doesn't know how to add two objects [^src1]. Other operators (`__mul__`, etc.) have their own dunders [^src1].
- Annotating `other` as `typing.Self` enables editor autocompletion for the other object's attributes [^src1].

## See also

- [Dev Environment Stack](/mlops/dev-environment-stack.md) — Python is the Layer-3 runtime; install/isolate it with [uv](/mlops/uv.md)
- [FastAPI](/software-engineering/fastapi.md) — a Python API framework (software-engineering) that builds on these language fundamentals
- [Data Engineering](/data-engineering/README.md) — Python is the glue for many data pipelines; links back here for language basics
- [Claude API](/ai-engineering/claude-api.md) — uses the Python language reference here (ai-engineering)
- [MLOps hub](/mlops/README.md)

---

[^src1]: [10 Important Python Concepts In 20 Minutes (Indently)](../../raw/youtube/youtube-Gx5qb1uHss4-10-important-python-concepts-in-20-minutes.md) — files/variables [[00:00](../../raw/youtube/youtube-Gx5qb1uHss4-10-important-python-concepts-in-20-minutes.md#t=00:00)], data types [[01:50](../../raw/youtube/youtube-Gx5qb1uHss4-10-important-python-concepts-in-20-minutes.md#t=01:50)], type annotations [[03:08](../../raw/youtube/youtube-Gx5qb1uHss4-10-important-python-concepts-in-20-minutes.md#t=03:08)], constants [[04:53](../../raw/youtube/youtube-Gx5qb1uHss4-10-important-python-concepts-in-20-minutes.md#t=04:53)], functions [[06:11](../../raw/youtube/youtube-Gx5qb1uHss4-10-important-python-concepts-in-20-minutes.md#t=06:11)], classes/methods [[09:41](../../raw/youtube/youtube-Gx5qb1uHss4-10-important-python-concepts-in-20-minutes.md#t=09:41)], dunder methods [[15:23](../../raw/youtube/youtube-Gx5qb1uHss4-10-important-python-concepts-in-20-minutes.md#t=15:23)]
</content>

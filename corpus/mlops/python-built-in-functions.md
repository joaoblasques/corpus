---
type: concept
domain: mlops
status: draft
sources:
  - path: raw/web/python-built-in-functions-a-complete-guide-real-python.md
    channel: web
    ingested_at: 2026-06-16
aliases:
  - python built-in functions
  - builtins
  - builtins module
  - built-in scope
  - python builtins
  - abs
  - divmod
  - sorted
  - enumerate
  - zip
  - map
  - filter
  - isinstance
tags:
  - corpus/mlops
  - concept
created: 2026-06-16
updated: 2026-06-16
---

# Python Built-in Functions

**TL;DR**: Python's built-in functions are "predefined functions you can use anywhere in your code without any imports" [^src1]. They all live in the `builtins` module, which Python loads at startup and exposes through the **built-in scope** — so no import is needed [^src1]. Several entries with function-style names (`str`, `list`, `dict`, `int`) are actually **classes**, but the docs list them as built-in functions [^src1]. This page is the **built-in-scope catalog**; it complements [Python](/mlops/python.md) (language fundamentals: data types, type annotations, classes, dunder methods) without repeating it.

You can `import builtins` explicitly when you intend to **shadow** a built-in name with your own variable yet still reach the original as `builtins.name` [^src1].

## Math

`abs()` non-negative value of int/float/complex/Fraction/Decimal [^src1]; `divmod(a, b)` returns `(quotient, remainder)`, same as `(a // b, a % b)` for ints [^src1]; `min()` / `max()` over an iterable or args, with optional `default` (for empty input) and `key` callable [^src1]; `pow(base, exp[, mod])` where the three-arg form computes `base**exp % mod` far faster than doing it in two steps [^src1]; `round(number[, ndigits])` using **round-half-to-even** banker's rounding, so `round(2.5)` is `2` not `3` [^src1]; `sum(iterable[, start])` for totals [^src1].

## Basic-type construction & representation

- **Numbers/bases**: `int()`, `float()`, `complex()`; `bin()`, `oct()`, `hex()` convert an integer to its base-2/8/16 string, and `int(s, base=...)` parses the reverse [^src1].
- **Strings**: `str()` (user-friendly, via `.__str__()`), `repr()` (developer-friendly, ideally re-creatable via `.__repr__()`), and `ascii()` which calls `repr()` then escapes non-ASCII chars to `\x`/`\u`/`\U` for log/terminal safety [^src1].
- **Booleans**: `bool(obj)` — a predicate returning the object's truth value per Python's falsy rules (`None`, `False`, zero of any numeric type, empty sequences/collections) [^src1].
- **Encoding**: `ord(char)` → integer Unicode code point; `chr(code_point)` → character; they are complementary [^src1].
- **Binary**: `bytes()` (immutable) and `bytearray()` (mutable), taking `source`, `encoding`, and an `errors` handler (`"strict"`/`"ignore"`/`"replace"`/`"xmlcharrefreplace"`/`"backslashreplace"`) [^src1].

## Collection constructors

`list()`, `tuple()`, `dict()`, `set()`, `frozenset()` build their respective collection from an iterable (or keyword/mapping args for `dict`) [^src1]. In practice these are **class constructors rather than functions**, though the docs call them functions [^src1]. `frozenset` is the immutable counterpart of `set`; `set()` is the only way to make an *empty* set since `{}` is an empty dict [^src1].

## Iterables & iterators

- **Size/order**: `len()` (via the `.__len__()` length protocol) [^src1]; `reversed()` returns a reverse *iterator*; `sorted(iterable, key=None, reverse=False)` always returns a new *list* [^src1].
- **Truth checks**: `all()` is `True` when every item is truthy; `any()` is `True` when at least one is — both pair well with generator expressions [^src1].
- **Ranges/indices**: `range(stop)` / `range(start, stop, step)` yields a lazy `range` object [^src1]. `enumerate(iterable, start=0)` is the Pythonic replacement for `for i in range(len(x))` indexing loops, yielding `(index, item)` tuples [^src1].
- **Combining/transforming**: `zip()` aggregates elements across iterables; `map(function, iterable, *iterables, strict=False)` applies a transform lazily; `filter(function, iterable)` keeps items for which the predicate is true [^src1]. `slice()` builds a reusable slice object [^src1].
- **Iterator protocol**: `iter()` / `next()` (and async `aiter()` / `anext()`) drive iteration directly [^src1].

`map`'s `strict=True` (added in Python 3.14) raises `ValueError` on unequal-length inputs instead of silently stopping at the shortest [^src1]. `reduce()` "used to be a built-in function, but is now available in the functools module" [^src1].

## I/O

`input([prompt])` reads a line from the console as a string; `open(file, mode="r", ...)` returns a file object (use it in a `with` statement); `print()` writes to a text stream; `format()` converts a value to a formatted representation [^src1].

## OOP / introspection

Attribute access — `getattr()`, `setattr()`, `delattr()`, `hasattr()` [^src1]. Type & relationship checks — `type()` (also creates classes dynamically), `isinstance()`, `issubclass()`, `callable()` [^src1]. Class machinery — `property()`, `classmethod()`, `staticmethod()`, `super()`, `object()` [^src1]. Scope/namespace inspection — `locals()`, `globals()`, `dir()`, `vars()` [^src1].

## See also

- [Python](/mlops/python.md) — the language-fundamentals page (data types, annotations, classes, dunder methods); this page is the built-in-scope companion. Note `str()`/`repr()` here are backed by the `__str__`/`__repr__` dunders documented there.
- [MLOps hub](/mlops/README.md)
- [Claude API](/ai-engineering/claude-api.md) — Python code using the Claude SDK leans on these built-ins (ai-engineering)

---

[^src1]: [Python Built-in Functions: A Complete Guide (Real Python)](../../raw/web/python-built-in-functions-a-complete-guide-real-python.md)

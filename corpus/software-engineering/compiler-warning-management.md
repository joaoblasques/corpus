---
type: concept
domain: software-engineering
status: draft
sources:
  - path: raw/web/why-git-has-a-variable-named-false-but-the-compiler-does-not.md
    channel: web
    ingested_at: 2026-06-12
aliases:
  - compiler warning management
  - compiler tricks
  - NOT_CONSTANT
  - false_but_the_compiler_does_not_know_it_
  - unreachable-code warning
tags:
  - corpus/software-engineering
  - concept
created: 2026-06-12
updated: 2026-06-16
---

# Compiler-Warning Management (Git's `false_but_the_compiler_does_not_know_it_`)

**TL;DR**: A precise technique for suppressing a *specific* false-positive compiler warning without disabling the warning globally or reaching for blunter tools. Git keeps Clang's `-Wunreachable-code` on (it catches real dead code) but routes known false positives through an external, non-`const` variable the compiler cannot prove is constant — and under LTO the dead branch is still eliminated.

A study in precise compiler-warning management in C [^src1]. Git wants to keep Clang's `-Wunreachable-code` warning enabled (it catches genuinely dead code) but suppress false positives that arise when the same source compiles across build configurations [^src1].

The mechanism — a `NOT_CONSTANT` macro:

```c
#define NOT_CONSTANT(expr) ((expr) || false_but_the_compiler_does_not_know_it_)
extern int false_but_the_compiler_does_not_know_it_;
```

The variable is `0`, never modified, but **not `const`**, has external linkage, and is defined in a separate translation unit. So a compiler optimizing one file "cannot prove that the value of this variable will always remain 0" [^src1]. The expression is `false` at runtime but "not obviously false to the compiler" [^src1] — suppressing the unreachable-code false positive (e.g. around `create_ref_symlink` in `NO_SYMLINK_HEAD` builds, and originally around `sigfillset()`'s error path).

Why not alternatives [^src1]: `#ifndef` spreads build logic into control flow; `#pragma clang diagnostic` is compiler-specific and noisy; `volatile` is semantically too strong (forces every read). The external-variable trick is precise and reusable. And it composes with optimization: under **link-time optimization (LTO)** the compiler sees the definition across translation units, proves the branch is always false, and removes it — "the best of both worlds" (no warning during normal compilation, dead branch eliminated under LTO) [^src1]. Added by Junio C Hamano in March 2025 [^src1].

## See also

- [[software-engineering/README|Software Engineering hub]]

---

[^src1]: [Why Git Has a Variable Named false_but_the_compiler_does_not_know_it](../../raw/web/why-git-has-a-variable-named-false-but-the-compiler-does-not.md)

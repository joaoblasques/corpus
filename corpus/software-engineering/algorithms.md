---
type: concept
domain: software-engineering
status: draft
sources:
  - path: raw/youtube/youtube-fkcfaapypuq.md
    channel: youtube
    ingested_at: 2026-06-15
  - path: raw/email/email-2026-06-08-youre-learning-algorithms-the-wrong-way.md
    channel: email
    ingested_at: 2026-06-15
aliases:
  - algorithms
  - recursion
  - binary search
  - dynamic programming
  - memoization
  - divide and conquer
  - tree traversal
  - linear search
tags:
  - corpus/software-engineering
  - concept
created: 2026-06-15
updated: 2026-06-15
---

# Algorithms (Strategies, Not Tricks)

**TL;DR** — Algorithms are best learned as **strategies to reach for**, not solutions to memorize. "The goal is not to memorize every algorithm as a separate trick… [it's] to understand the strategy behind each one, so when a similar problem shows up, you know what to reach for" [^src2]. The recurring strategies: **recursion** (break a problem into smaller copies of itself), **divide and conquer** (e.g. binary search halves the search space), and **dynamic programming / memoization** (cache results so you never recompute the same subproblem) [^src1][^src2]. This is the algorithmic companion to [[software-engineering/data-structures|Data Structures and Big O Notation]].

## Recursion

A function that calls itself; every recursive algorithm needs two parts [^src1][^src2]:

- **Base case** — a situation where the answer is already known and no further recursion happens.
- **Recursive case** — call the same function on a smaller version of the problem.

This is **divide and conquer**: solve a hard problem by solving its subproblems, then combining [^src1]. Canonical example — Fibonacci: base cases `f(1)=1`, `f(2)=1`; recursive case `f(n)=f(n-1)+f(n-2)` [^src1][^src2]. Recursion also expresses non-numeric problems cleanly: in-order / pre-order / post-order **binary-tree traversal** (base case `node == null`), and reversing a string as `reverse(s) = reverse(s[1:]) + s[0]` [^src1].

> Gotcha: naive recursive Fibonacci is **O(2ⁿ)** — it recomputes the same subproblems exponentially often, becoming "infeasible" by n≈70 [^src1].

## Binary search (divide and conquer)

Works **only on a sorted array** [^src2]. Check the middle element; if it equals the target you're done, otherwise the sorted property tells you which half to discard — every step halves the remaining problem, giving **O(log n)** vs. O(n) for a linear scan [^src1][^src2]. Implemented recursively by passing `start`/`end` indices (base case `start > end` → not found) rather than slicing, to avoid the O(k) cost of rebuilding subarrays [^src1].

Trade-off worth knowing: sorting first is O(n log n), so binary search pays off when you do **repeated** searches over the same data; a single lookup may be cheaper with a linear scan [^src1].

## Dynamic programming & memoization

DP "simply means reusing results you already calculated instead of solving the same smaller problem again" [^src2]. **Memoization** is the cache: store each computed value (e.g. in an object/dict) and return it on re-request [^src1]. Applied to Fibonacci, this collapses O(2ⁿ) → **O(n) time** at the cost of **O(n) space**; an iterative version (track only the last two terms) keeps O(n) time at **O(1) space** [^src1].

| Fibonacci approach | Time | Space |
|---|---|---|
| Naive recursion | O(2ⁿ) | O(n) call stack |
| Memoized recursion | O(n) | O(n) |
| Iterative | O(n) | O(1) |

## Why this still matters under AI tooling

"You may use built-in tools most of the time, but understanding algorithms still matters because the same ideas show up everywhere: slow code, repeated work, structured data, and simple solutions that do more work than they should" [^src2]. The strategies-not-tricks framing is also interview advice — these are "the parts of the algorithms you actually need to know… [for] technical interviews" [^src1]. This connects to the fundamentals-under-AI argument in [[software-engineering/ai-assisted-development|AI-Assisted Development]] and the interview-fluency point in [[ai-business/technical-career|Navigating a Technical Career]] (practice DSA without autocomplete).

## See also

- [[software-engineering/data-structures|Data Structures and Big O Notation]] — the complexity classes (O(1)/O(log n)/O(n)/O(n²)) these strategies trade in, and the structures (stacks, trees, hashmaps) the algorithms operate on.
- [[software-engineering/software-design-principles|Software Design Principles]] — simplicity as a design value mirrors "don't do more work than needed."

[^src1]: [Famous Computer Science Algorithms (recursion, search, DP)](../../raw/youtube/youtube-fkcfaapypuq.md) (Tech With Tim; fetched via the source email)
[^src2]: [you're learning algorithms the wrong way](../../raw/email/email-2026-06-08-youre-learning-algorithms-the-wrong-way.md) (Tech With Tim newsletter)

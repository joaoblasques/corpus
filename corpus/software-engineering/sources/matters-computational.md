---
type: source
domain: software-engineering
status: complete
sources:
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-01.md
    channel: pdf
    ingested_at: 2026-07-17
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-02.md
    channel: pdf
    ingested_at: 2026-07-17
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-03.md
    channel: pdf
    ingested_at: 2026-07-17
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-04.md
    channel: pdf
    ingested_at: 2026-07-17
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-05.md
    channel: pdf
    ingested_at: 2026-07-17
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-06.md
    channel: pdf
    ingested_at: 2026-07-17
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-07.md
    channel: pdf
    ingested_at: 2026-07-17
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-08.md
    channel: pdf
    ingested_at: 2026-07-17
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-09.md
    channel: pdf
    ingested_at: 2026-07-17
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-10.md
    channel: pdf
    ingested_at: 2026-07-17
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-11.md
    channel: pdf
    ingested_at: 2026-07-17
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-12.md
    channel: pdf
    ingested_at: 2026-07-17
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-13.md
    channel: pdf
    ingested_at: 2026-07-17
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-14.md
    channel: pdf
    ingested_at: 2026-07-17
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-15.md
    channel: pdf
    ingested_at: 2026-07-17
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-16.md
    channel: pdf
    ingested_at: 2026-07-17
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-17.md
    channel: pdf
    ingested_at: 2026-07-17
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-18.md
    channel: pdf
    ingested_at: 2026-07-17
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-19.md
    channel: pdf
    ingested_at: 2026-07-17
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-20.md
    channel: pdf
    ingested_at: 2026-07-17
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-21.md
    channel: pdf
    ingested_at: 2026-07-17
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-22.md
    channel: pdf
    ingested_at: 2026-07-17
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-23.md
    channel: pdf
    ingested_at: 2026-07-17
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-24.md
    channel: pdf
    ingested_at: 2026-07-17
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-25.md
    channel: pdf
    ingested_at: 2026-07-17
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-26.md
    channel: pdf
    ingested_at: 2026-07-17
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-27.md
    channel: pdf
    ingested_at: 2026-07-17
aliases:
  - Matters Computational
  - FXT
  - Arndt algorithms
tags:
  - corpus/software-engineering
  - source
created: 2026-07-17
updated: 2026-07-17
---

# Matters Computational: Ideas, Algorithms, Source Code (Joerg Arndt)

**Source type**: Full technical book (978 pages, 27 of 50 parts ingested)  
**Author**: Joerg Arndt  
**Channel**: PDF  
**License**: Free PDF (freely redistributable)  
**Code**: FXT library (C++)

## Summary

A comprehensive reference on low-level computational algorithms, with full C++ source code throughout. Focus: bit manipulation, combinatorial generation, permutations, number-theoretic transforms, FFT variants, data structures, fast arithmetic. The book is notably practical — every algorithm is implemented and demonstrated with code output. 978 pages; the FXT library implements all algorithms [^src1].

## Structure (ToC)

| Part | Chapters | Topics |
|---|---|---|
| I | 1–8 | Bit wizardry, number representations, permutations, sorting |
| II | 9–15 | Data structures: deque, priority queue, bit-arrays, hash tables |
| III | 16–20 | Combinatorial generation: combinations, partitions, Gray codes |
| IV | 21–28 | Transforms: FFT, Walsh-Hadamard, Haar, Hartley, NTT |
| V | 29–35 | Arithmetic: modular, fast multiplication, root extraction, AGM |
| VI | 36–42 | Number theory: primes, Fibonacci, Stern-Brocot |
| VII | 43–50 | Special topics: ternary numbers, self-similar sequences, Boolean functions |

## Key Topics by Chapter

### Bit Wizardry (Ch. 1)
Core bit manipulation: isolating lowest/highest set bit, counting bits (popcount), Gray codes, De Bruijn sequences for single-bit-index lookup, bit rotation, bitset operations. All with branchless variants. The book is particularly detailed on hardware trade-offs (when `__builtin_popcountl` beats hand-coded, when table lookups cause cache misses) [^src1].

**Canonical patterns**:
- `x & -x` — isolate lowest set bit
- `x & (x-1)` — clear lowest set bit
- `bit_count(x)` — parallel popcount using `0x5555...`, `0x3333...` masks
- De Bruijn sequence multiplication for bit-index lookup

### Permutations (Ch. 2–3)
In-place permutation algorithms, cycle detection, generating all permutations (next-permutation, factorial number system). Distinction between *permutations as functions* and *permutation groups* [^src1].

### Sorting and Searching (Ch. 5–6)
Comparison-based sorting (introsort, heapsort), radix sort, counting sort. Index structures for search. All with benchmark notes [^src1].

### Data Structures (Ch. 9–15)
- **Deque**: ring-buffer implementation in C++ (Ch. 4)
- **Priority queue**: binary heap with sift-up/sift-down, heap sort (Ch. 9)
- **Bit-arrays**: arbitrary-length bit sets, operations in O(n/64) time (Ch. 4)
- **Hash tables**: open addressing, double hashing (Ch. 14)

### Transforms (Ch. 21–28)
FFT (split-radix, decimation-in-time/frequency, radix-2/4), Walsh-Hadamard transform, Haar wavelet transform, Hartley transform, Number Theoretic Transform (NTT) for exact convolution over finite fields. Mass storage convolution via MFA (Matrix Fourier Algorithm) — handles inputs that don't fit in RAM by decomposing into 2D DFT [^src2].

### Fast Arithmetic (Ch. 29–33)
Modular arithmetic, Barrett reduction, Montgomery multiplication, fast bignum multiplication (Karatsuba, FFT-based), root extraction via Newton's method, AGM (Arithmetic-Geometric Mean) for computing π and log [^src1].

### Number Theory (Ch. 36–38)
Prime sieves (Sieve of Eratosthenes, Sieve of Atkin), modular inverses, Euler's totient, Fibonacci sequences, Stern-Brocot tree [^src1].

## Bit-Manipulation Quick Reference

The most cited patterns from Ch. 1 [^src1]:

| Operation | Code |
|---|---|
| Lowest set bit | `x & -x` |
| Clear lowest set bit | `x & (x-1)` |
| Round up to power of 2 | `next_pow_of_2(x)` |
| Popcount (parallel) | `bit_count(x)` using mask sequence |
| Bit index via De Bruijn | `db_lowest_one_idx(x)` — multiply + shift + lookup |
| Is power of 2? | `!(x & (x-1))` |
| Isolate highest bit | Via `highest_one_01edge()` then XOR |

## Related Corpus Pages

- General algorithms: [/software-engineering/algorithms.md](/software-engineering/algorithms.md)
- Data structures: [/software-engineering/data-structures.md](/software-engineering/data-structures.md)

---

[^src1]: [Matters Computational, Parts 1–20 — bit wizardry, permutations, data structures, number theory, sorting](../../../raw/pdf/pdf-matters-computational-ideas-algorithms-source-code-part-01.md)
[^src2]: [Matters Computational, Part 27 — Ch. 22 mass storage convolution via MFA](../../../raw/pdf/pdf-matters-computational-ideas-algorithms-source-code-part-27.md)

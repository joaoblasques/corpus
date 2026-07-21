---
type: source
domain: software-engineering
status: draft
sources:
  - path: raw/pdf/pdf-text-algorithms-part-01.md
    channel: pdf
    ingested_at: 2026-07-21
  - path: raw/pdf/pdf-text-algorithms-part-02.md
    channel: pdf
    ingested_at: 2026-07-21
  - path: raw/pdf/pdf-text-algorithms-part-03.md
    channel: pdf
    ingested_at: 2026-07-21
  - path: raw/pdf/pdf-text-algorithms-part-04.md
    channel: pdf
    ingested_at: 2026-07-21
  - path: raw/pdf/pdf-text-algorithms-part-05.md
    channel: pdf
    ingested_at: 2026-07-21
  - path: raw/pdf/pdf-text-algorithms-part-06.md
    channel: pdf
    ingested_at: 2026-07-21
  - path: raw/pdf/pdf-text-algorithms-part-07.md
    channel: pdf
    ingested_at: 2026-07-21
  - path: raw/pdf/pdf-text-algorithms-part-08.md
    channel: pdf
    ingested_at: 2026-07-21
  - path: raw/pdf/pdf-text-algorithms-part-09.md
    channel: pdf
    ingested_at: 2026-07-21
  - path: raw/pdf/pdf-text-algorithms-part-10.md
    channel: pdf
    ingested_at: 2026-07-21
  - path: raw/pdf/pdf-text-algorithms-part-11.md
    channel: pdf
    ingested_at: 2026-07-21
  - path: raw/pdf/pdf-text-algorithms-part-12.md
    channel: pdf
    ingested_at: 2026-07-21
  - path: raw/pdf/pdf-text-algorithms-part-13.md
    channel: pdf
    ingested_at: 2026-07-21
  - path: raw/pdf/pdf-text-algorithms-part-14.md
    channel: pdf
    ingested_at: 2026-07-21
  - path: raw/pdf/pdf-text-algorithms-part-15.md
    channel: pdf
    ingested_at: 2026-07-21
  - path: raw/pdf/pdf-text-algorithms-part-16.md
    channel: pdf
    ingested_at: 2026-07-21
  - path: raw/pdf/pdf-text-algorithms-part-17.md
    channel: pdf
    ingested_at: 2026-07-21
  - path: raw/pdf/pdf-text-algorithms-part-18.md
    channel: pdf
    ingested_at: 2026-07-21
  - path: raw/pdf/pdf-text-algorithms-part-19.md
    channel: pdf
    ingested_at: 2026-07-21
  - path: raw/pdf/pdf-text-algorithms-part-20.md
    channel: pdf
    ingested_at: 2026-07-21
aliases:
  - Text Algorithms
  - Efficient Algorithms on Texts
  - Crochemore Rytter
  - string matching algorithms
  - suffix tree
  - suffix automaton
  - DAWG
  - directed acyclic word graph
  - Aho-Corasick
  - Boyer-Moore
  - Knuth-Morris-Pratt text algorithms
  - pattern matching algorithms
  - text compression algorithms
  - data compression text
  - palindrome algorithms
  - two-dimensional pattern matching
  - tree pattern matching
  - shortest common superstring
tags:
  - corpus/software-engineering
  - source
created: 2026-07-21
updated: 2026-07-21
---

# Efficient Algorithms on Texts (Crochemore & Rytter, 1994)

TL;DR: A graduate-level algorithmic text by Maxime Crochemore and Wojciech Rytter covering exact string matching, suffix data structures (suffix trees, directed acyclic word graphs), text compression, approximate matching, and extensions to 2D arrays and tree-shaped patterns. 396 pages; all 20 parts ingested. A rigorous theoretical reference for anyone implementing or understanding string algorithms.

## Structure

| Chapter | Topic |
|---|---|
| 1 | Introduction — pattern matching applications, text file facilities (grep), string-matching as the basic problem |
| 2 | Exact String Matching — naive O(nm), Knuth-Morris-Pratt (failure function), Boyer-Moore (bad character, good suffix), Aho-Corasick (multi-pattern via trie automaton) |
| 3 | String Matching with Gaps and Constraints |
| 4 | Regular Expressions and Finite Automata — NFA→DFA construction, regex matching |
| 5 | Suffix Trees — compact trie of all suffixes; O(n) size (≤2n−1 nodes); McCreight's O(n) construction; applications: exact matching in O(m+occ), longest repeated substring |
| 6 | Directed Acyclic Word Graphs (DAWG) — suffix automaton; isomorphic subtree merging; O(n) size (≤2n−1 states); linear construction; recognizes all substrings |
| 7 | String Regularities — squares (repeated factors), runs, Lyndon words, Duval's algorithm |
| 8 | Palindromes and Palstars — odd/even palindromes; radius table (Rad); palstar recognition in O(n); first-smallest-palindrome tables |
| 9 | Approximate String Matching — edit distance, dynamic programming O(nm); k-mismatch; filtration using exact matching |
| 10–11 | Text Compression — LZ77/LZ78 parsing; dictionary-based compression; Lempel-Ziv families |
| 12 | Two-Dimensional Pattern Matching — fingerprint approach; O(n² log m / m²) average comparisons |
| 13–14 | Parallel and On-Line Algorithms |
| 15 | Shortest Common Superstring — NP-complete problem; Gallant's greedy approximation via overlap maximization |

## Key concepts

### Suffix tree
A compressed trie of all n suffixes of a text; each chain (path of out-degree-1 nodes) compressed into a single edge labeled by a text interval [i,j]. Size is O(n) by a simple leaf-counting argument: at most n leaves → at most n-1 internal nodes (each with ≥2 children) → ≤2n-1 total nodes. Enables O(m + occ) exact matching (m = pattern length, occ = occurrences), longest common substring, and many other queries. [^ta-p05]

### Directed Acyclic Word Graph (DAWG)
Alternative suffix data structure obtained by merging isomorphic subtrees of the trie (unlike the suffix tree which compresses chains). The DAWG recognizes exactly the set of subwords (*Fac(text)*) of the input. Key fact: its linear size (≤2n−1 states) is non-trivial and "probably one of the most surprising facts." Each edge is labeled by a single symbol (unlike suffix tree's interval labels), making it convenient for character-level operations. [^ta-p05]

### KMP failure function
Preprocessing phase: S[i] = length of the longest proper prefix of Pattern[0..i] that is also a suffix. On mismatch at position j in the pattern, resume from Pattern[S[j-1]] instead of Pattern[0]. Achieves O(n+m) matching. Both the failure function computation and the matching scan are amortized O(n+m) by a potential argument on the pattern pointer. [^ta-p02]

### Palindromes and the Rad table
The radius table Rad[i] gives the half-length of the maximal odd palindrome centered at position i. Computed in O(n) by an "expanding palindrome" approach. **Palstar recognition**: a text is a palstar if it can be decomposed into a concatenation of palindromes. Using Rad plus a first-palindrome table F and a stack-based stage algorithm, palstars are recognized in linear time. [^ta-p10]

### Two-dimensional pattern matching
Extends 1D string matching to finding an m×m pattern in an n×n text array. A fingerprint (suffix of length r = O(log m) of the last row) appears in at most O(n²/m²) sub-windows on average; when the fingerprint is present, the window is searched with a linear-time algorithm. Average complexity: O(n² log m / m²) comparisons. [^ta-p15]

### Shortest common superstring (NP-complete)
Given a set R of strings, find the shortest string w such that every member of R occurs as a substring of w. NP-complete in general. **Gallant's greedy approximation**: repeatedly merge the pair of strings with maximum overlap (defined as the longest suffix of x that is also a prefix of y); achieves a constant-factor approximation. [^ta-p20]

## Relationship to other corpus pages

- String matching (KMP, Boyer-Moore, Aho-Corasick) extends [Algorithms](/software-engineering/algorithms.md) — the KMP section there gives the basic failure function; this source gives the full theoretical treatment.
- Suffix trees are used in [Speech and Language Processing](/ai-engineering/sources/speech-and-language-processing.md) — NLP preprocessing and indexing.
- LZ compression connects to [Signal Processing Algorithms](/software-engineering/signal-processing-algorithms.md) — data representation.
- The shortest common superstring approximation is an instance of greedy approximation; see [The Design of Approximation Algorithms](/software-engineering/sources/design-of-approximation-algorithms.md).

[^ta-p02]: raw/pdf/pdf-text-algorithms-part-02.md — Chapter 2: KMP failure function, Boyer-Moore, string matching algorithms
[^ta-p05]: raw/pdf/pdf-text-algorithms-part-05.md — Chapter 5: suffix trees (chain compression, O(n) size proof), DAWG (isomorphic subtree merging)
[^ta-p10]: raw/pdf/pdf-text-algorithms-part-10.md — Chapter 8: palindrome radius table, palstar recognition in linear time via PALSTAR algorithm
[^ta-p15]: raw/pdf/pdf-text-algorithms-part-15.md — Chapter 12: two-dimensional pattern matching, fingerprint/sub-window approach, average O(n² log m / m²)
[^ta-p20]: raw/pdf/pdf-text-algorithms-part-20.md — Chapter 15: shortest common superstring (NP-complete), Gallant's greedy approximation via overlap maximization

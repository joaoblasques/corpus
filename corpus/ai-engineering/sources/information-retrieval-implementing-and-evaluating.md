---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-information-retrieval-implementing-and-evaluating-part-01.md
    channel: pdf
    ingested_at: 2026-08-05
  - path: raw/_inbox/pdf-information-retrieval-implementing-and-evaluating-part-02.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-information-retrieval-implementing-and-evaluating-part-03.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-information-retrieval-implementing-and-evaluating-part-04.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-information-retrieval-implementing-and-evaluating-part-05.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-information-retrieval-implementing-and-evaluating-part-06.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-information-retrieval-implementing-and-evaluating-part-07.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-information-retrieval-implementing-and-evaluating-part-08.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-information-retrieval-implementing-and-evaluating-part-09.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-information-retrieval-implementing-and-evaluating-part-10.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-information-retrieval-implementing-and-evaluating-part-11.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-information-retrieval-implementing-and-evaluating-part-12.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-information-retrieval-implementing-and-evaluating-part-13.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-information-retrieval-implementing-and-evaluating-part-14.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-information-retrieval-implementing-and-evaluating-part-15.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-information-retrieval-implementing-and-evaluating-part-16.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-information-retrieval-implementing-and-evaluating-part-17.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-information-retrieval-implementing-and-evaluating-part-18.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-information-retrieval-implementing-and-evaluating-part-19.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-information-retrieval-implementing-and-evaluating-part-20.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-information-retrieval-implementing-and-evaluating-part-21.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-information-retrieval-implementing-and-evaluating-part-22.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-information-retrieval-implementing-and-evaluating-part-23.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-information-retrieval-implementing-and-evaluating-part-24.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-information-retrieval-implementing-and-evaluating-part-25.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-information-retrieval-implementing-and-evaluating-part-26.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-information-retrieval-implementing-and-evaluating-part-27.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-information-retrieval-implementing-and-evaluating-part-28.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-information-retrieval-implementing-and-evaluating-part-29.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-information-retrieval-implementing-and-evaluating-part-30.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-information-retrieval-implementing-and-evaluating-part-31.md
    channel: pdf
    ingested_at: 2026-08-06
  - path: raw/_inbox/pdf-information-retrieval-implementing-and-evaluating-part-32.md
    channel: pdf
    ingested_at: 2026-08-06
aliases:
  - Information Retrieval Implementing and Evaluating
  - Büttcher Clarke Cormack
  - ir-implementing-and-evaluating
tags:
  - corpus/ai-engineering
  - source
created: 2026-08-05
updated: 2026-08-06
---

# Information Retrieval: Implementing and Evaluating Search Engines (Büttcher, Clarke, Cormack, 2010)

**TL;DR**: A 624pp graduate textbook (MIT Press, 2010) covering the full IR stack — crawling, indexing, retrieval, ranking, evaluation, parallel systems, and Web search — with emphasis on implementation and experimental validation. The Wumpus open-source IR system provides model implementations. Authored by three generations of University of Waterloo IR researchers [^p01].

## Scope and organization

The book is organized into five parts [^p01]:

| Part | Topic | Key chapters |
|---|---|---|
| I | Foundations | Inverted indices, basic retrieval, evaluation, tokenization |
| II | Indexing | Static/dynamic indices, query processing, compression |
| III | Retrieval & Ranking | Probabilistic retrieval (BM25), language modeling, categorization, fusion/metalearning |
| IV | Evaluation | Effectiveness measures, statistical tests, efficiency (throughput/latency) |
| V | Applications | Parallel IR (MapReduce), Web search (PageRank, crawling), XML retrieval |

Chapter-level breakdown [^p02] [^p07] [^p10] [^p13] [^p15] [^p17] [^p19] [^p22] [^p24] [^p27] [^p29]:

| Ch | Title | Key topics | Parts |
|---|---|---|---|
| 1 | Introduction | IR system architecture, PRP, relevance dimensions, evaluation overview | 02–04 |
| 2 | Basic Techniques | Tokenization, Zipf's law, inverted index variants, BM25/LMD/DFR summary, recall/precision/MAP | 02–05 |
| 3 | Tokens and Terms | Stemming (Porter), stopping, Unicode/UTF-8, n-grams, language handling | 05–06 |
| 4 | Static Indices | Hash/B-tree dictionaries, merge-based construction, on-disk posting lists | 07–08 |
| 5 | Dynamic Indices & Query Processing | In-place updates, TAAT vs DAAT, galloping search, region algebra for XML | 08–12 |
| 6 | Index Compression | Huffman, Elias gamma/delta, LLRUN, variable-byte encoding | 10–12 |
| 7 | Query Optimization | WAND algorithm, impact-ordered indices, candidate set pruning, top-k processing | 13–14 |
| 8 | Probabilistic Retrieval | PRP, BIM, RSJ formula, BM25 derivation from Two-Poisson Model, BM25F, relevance feedback | 15–16 |
| 9 | Language Models & DFR | Dirichlet LM, Jelinek-Mercer LM, KL-divergence, Divergence from Randomness (Bose-Einstein) | 17–18 |
| 10 | Categorization & Filtering | Spam, language categorization, Naive Bayes, kNN, SVM, Rocchio, logistic regression | 19–21 |
| 11 | Fusion & Metalearning | Reciprocal rank fusion, CombSUM/CombMNZ, learning-to-rank (pointwise/pairwise/listwise) | 22–23 |
| 12 | Evaluation | MAP, P@10, bpref, nDCG, incomplete judgments, TREC methodology, statistical significance | 24–26 |
| 13 | Efficiency | Throughput vs. latency trade-offs, hardware considerations, index layout | 27–28 |
| 14 | Parallel IR | MapReduce for IR, distributed indexing, query routing | 27–28 |
| 15 | Web Search | PageRank, HITS, Web crawlers, robots.txt, spam detection | 29–31 |
| 16 | XML Retrieval | Region algebra, XPath/XQuery, INEX evaluation | 31–32 |

## IR system architecture (Chapter 1)

An IR system has three core components: an **index** (inverted index, maintained for a document collection), a **search engine** (processes queries against the index), and a **user interface** (mediates query construction). The central data structure is the **inverted index**: a mapping from terms to the locations in the collection where they occur [^p01].

**Performance dimensions**:
- **Efficiency**: response time (latency), query throughput (queries/second), storage (bytes/document). Web-scale search may require tens of thousands of queries/second [^p01].
- **Effectiveness**: relevance of retrieved documents — depends entirely on human judgment.

## Relevance ranking

**Probability Ranking Principle (PRP)**: "If an IR system's response to each query is a ranking of the documents in the collection in order of decreasing probability of relevance, then the overall effectiveness of the system to its users will be maximized." [^p01]

The PRP is the foundational principle of ranked retrieval, but overlooks important nuances [^p01]:

| Dimension | Definition |
|---|---|
| **Specificity** | Degree to which document content is focused on the information need |
| **Exhaustivity** | Degree to which the document covers the information need |
| **Novelty** | Incremental value after prior results already conveyed some relevant content |

Specificity and exhaustivity are independent: a large document may be exhaustive but not specific; a focused excerpt may be specific but not exhaustive [^p01].

## Tokenization and vocabulary (Chapter 2–3)

**Zipf's Law**: in any large natural-language corpus, the frequency of the r-th most common word is proportional to 1/r. The top 100 words account for roughly half of all word occurrences; the vocabulary tail is very long [^p02].

**Inverted index variants** [^p03]:
- **Docid index**: posting list = sorted list of document IDs. Sufficient for Boolean retrieval.
- **Frequency index**: posting list = (docid, tf) pairs. Required for TF-IDF and BM25 scoring.
- **Positional index**: posting list = (docid, [position₁, position₂, …]) tuples. Required for phrase queries and proximity operators.
- **Schema-independent index** (Büttcher & Clarke): encodes structural element offsets alongside positional data, enabling structured retrieval without pre-specifying schema. Used in Wumpus [^p04].

**Tokenization pipeline** [^p05]:
1. Character encoding normalization (UTF-8; Unicode case folding).
2. Word segmentation (whitespace + punctuation boundaries; CJK ideographs need morphological segmentation).
3. Stopword removal (language-dependent list; aggressive removal improves efficiency but risks losing meaning in Boolean queries).
4. Stemming — Porter (English), Snowball (multilingual), or language-specific morphological analyzers. Over-stemming collapses semantically distinct terms; under-stemming increases vocabulary size.
5. N-gram extraction (character-level, n = 3–5) as language-independent alternative to steps 3–4 [^p06].

## Implementation techniques (Parts II–III)

### Inverted index construction

Static index construction uses an **external sort merge** approach: parse documents into (term, docid, tf, [positions]) tuples in memory, sort by term, then merge sorted runs from disk [^p07]. The resulting posting lists are written contiguously per term, enabling sequential scan at query time.

**B-tree dictionary**: maps terms to posting-list disk offsets. Provides O(log n) lookup and efficient prefix-range scan for wildcard queries [^p07].

**Dynamic index maintenance** [^p08]: three strategies for updates to a live index:
- **In-place update**: extend posting lists in-place; requires preallocated slack space, degrades with fragmentation.
- **Re-merge**: accumulate updates in a small in-memory index; periodically merge with the on-disk index. Merge cost is proportional to total posting count.
- **Logarithmic merge** (Büttcher & Clarke): maintain a hierarchy of on-disk index levels of exponentially growing size; merge triggered when two same-size levels exist. Write cost O(N log N / B) for N postings and block size B; read cost increases logarithmically. Used in Wumpus [^p08].

### Query processing: TAAT vs DAAT

Two traversal strategies for multi-term queries against posting lists [^p09]:

| Strategy | Description | Advantage |
|---|---|---|
| **TAAT** (Term-At-A-Time) | Score each term's posting list fully before moving to the next term; accumulate scores in a doc-score array | Simple; works well with small vocabularies |
| **DAAT** (Document-At-A-Time) | Advance all posting list iterators in lock-step by document ID; score each document once all term contributions are known | Cache-friendly; enables early termination |

**Galloping search** (exponential search): to find the next posting ≥ d in a sorted list, double the step size until overshooting, then binary-search the bracketed interval. Cost O(log(gap)) instead of O(gap) for skipping large gaps. Essential for efficient DAAT processing of rare terms in AND queries [^p09].

**Skip pointers**: periodic pointers embedded in posting lists that jump ahead by a fixed stride. Allow O(1) average skips for common documents in AND processing, at the cost of extra storage [^p09].

### WAND algorithm (top-k query processing)

WAND (Weak AND, Broder et al. 2003) safely prunes posting list traversal to retrieve only the top-k documents without evaluating all candidates [^p13]:

1. Maintain an in-memory heap of the current top-k scores (threshold = score of the k-th document).
2. For each term, precompute an **upper bound** on its contribution to any document's score (e.g., max tf × idf across the posting list).
3. Advance posting list iterators; a document can only beat the threshold if the sum of upper bounds for its terms exceeds the threshold. If not, skip to the next candidate pivot.
4. Only fully evaluate documents that pass the upper-bound filter.

**Impact-ordered index**: sort postings within each list by decreasing term-frequency (impact) rather than by docid. Enables stopping after processing a fixed number of high-impact postings per term. Trades random-access capability for early termination gains in single-term or disjunctive queries [^p14].

### Index compression

All posting-list values (docids, term frequencies, positions) are stored in compressed form. Standard approach: **delta-encode** docids (store gaps between consecutive docids, which are small for high-frequency terms), then apply an integer code [^p10]:

| Code | Description | Bit cost |
|---|---|---|
| **Unary** | k ones followed by a zero | k + 1 bits |
| **Elias gamma** | Unary length prefix + (⌊log₂ x⌋)-bit offset | 2⌊log₂ x⌋ + 1 bits |
| **Elias delta** | Elias-gamma length prefix + offset | ≈log₂ x + 2 log₂ log₂ x bits |
| **Variable-byte (VByte)** | 7 bits per byte; high bit = continuation flag | ⌈log₁₂₈ x⌉ bytes |
| **Huffman** | Optimal prefix code for known symbol distribution | Approaches entropy |

**LLRUN (Büttcher & Clarke)**: a hybrid code pairing Huffman assignment for the length prefix with run-length encoding for positions. Achieves near-optimal compression on positional indices while remaining fast to decode [^p11].

VByte is the practical default: simple, fast to decode (byte-aligned), and within ~10% of optimal for typical posting-list distributions. Elias gamma/delta are theoretically tighter but slower [^p11].

## Ranking models (Parts III–IV)

### BM25 and the Two-Poisson Model (Chapter 8)

BM25 is derived from a **Two-Poisson Model**: term occurrences in documents follow one Poisson distribution for "elite" (topically relevant) documents and another for non-elite documents [^p15]. The resulting approximation to the optimal term weight:

```
BM25(Q, D) = Σ_{t∈Q} IDF(t) × (tf(t,D) × (k1 + 1)) / (tf(t,D) + K) × (qtf × (k3+1)) / (qtf + k3)
```

where `K = k1 × ((1−b) + b × dl/avdl)`, `k1 ≈ 1.2`, `b ≈ 0.75`, `k3 ≈ 7–1000`. The parameter `b` controls document-length normalization: b=0 = no normalization; b=1 = full verbosity hypothesis (normalize by dl/avdl) [^p15].

**Relevance feedback and BM25**: after relevance judgments for a first-pass result set, Robertson-Sparck Jones expansion weights re-score the term's contribution using a contingency table over the judged set. Pseudo-relevance feedback assumes the top-k retrieved documents are relevant [^p16].

**BM25F** (Robertson & Zaragoza, 2004): extends BM25 to structured documents with multiple fields (title, body, anchor text). Each field has its own `tf` count and length-normalization parameter; field `tf` values are combined into a single weighted `tf` before plugging into the BM25 formula [^p16].

### Language models for IR (Chapter 9)

**Query-likelihood retrieval**: rank documents by P(Q|D) — the probability that the document's language model would generate the observed query. Three smoothing strategies [^p17]:

| Model | Formula | Parameter |
|---|---|---|
| **Dirichlet** | P(t\|D) = (tf(t,D) + μ × P(t\|C)) / (dl + μ) | μ ≈ 1000 (document-length-adaptive) |
| **Jelinek-Mercer** | P(t\|D) = (1−λ) × tf(t,D)/dl + λ × P(t\|C) | λ ≈ 0.1–0.5 |
| **Absolute discounting** | P(t\|D) = max(tf(t,D) − δ, 0)/dl + α × P(t\|C) | δ ≈ 0.7 |

Dirichlet smoothing is length-adaptive (short documents are smoothed more strongly toward the collection LM), which naturally handles document-length normalization. Experiments in the book show Dirichlet (μ=1000) competitive with BM25 on TREC ad-hoc tasks [^p17].

**KL-divergence retrieval model**: generalization of query-likelihood; the document's LM is ranked by KL-divergence from the query LM. Enables principled integration of query expansion: add terms to the query LM to reduce KL-divergence [^p17].

### Divergence from Randomness (DFR) (Chapter 9)

DFR models (Amati & van Rijsbergen, 2002) derive term weights from the intuition that the **more a term's distribution deviates from random placement** across the corpus, the more informative it is [^p18]:

1. Compute the "randomness" baseline: how often would term t appear in document D if placed uniformly at random (e.g., Bose-Einstein or Poisson random model)?
2. The term's informativeness = divergence of observed frequency from the random baseline.
3. Normalize by document length.

**Bose-Einstein model**: models term placement as drawing colored balls (terms) from an urn (collection) without replacement. The weight function: `w(t, D) = −log P(tf | random) + λ × normalization`. In practice DFR with Bose-Einstein normalization matches BM25 performance on standard TREC benchmarks [^p18].

## Evaluation (Part IV)

### Retrieval effectiveness measures (Chapter 12)

**MAP (Mean Average Precision)**: average over queries of the area under the precision-recall curve (AP). AP for one query = average precision at each recall point where a relevant document is retrieved. MAP is the standard TREC effectiveness measure; sensitive to the position of every relevant document [^p24].

**P@k (Precision at k)**: fraction of top-k retrieved documents that are relevant. P@10 is the most common Web-search metric because users rarely look past the first result page [^p24].

**nDCG (Normalized Discounted Cumulative Gain)**: graded relevance measure. Relevance judgments use a scale (e.g., 0=not relevant, 1=relevant, 5=highly relevant, 10=perfectly relevant). DCG discounts gain by position [^p25]:

```
DCG@k = Σ_{i=1}^{k} (2^{rel_i} − 1) / log₂(i + 1)
```

nDCG@k = DCG@k / IDCG@k, where IDCG is the DCG of the ideal ranking (all documents sorted by decreasing relevance). nDCG ∈ [0, 1]; used in TREC Web track and Yahoo! Learning to Rank Challenge [^p25].

**bpref (Binary Preference)**: designed for incomplete relevance judgments. Ranks each relevant document by how many judged non-relevant documents precede it:

```
bpref = (1/R) Σ_{r} (1 − |n ranked above r| / min(R, N))
```

where R = judged relevant, N = judged non-relevant, n = judged non-relevant documents ranked above r. bpref is robust when pooling has left many documents unjudged [^p25].

### TREC methodology (Chapter 12)

The **pooling method** (Harman, 1993) addresses the infeasibility of judging all documents: collect the top-100 (or top-k) results from all competing systems; judge only the pooled set; treat unjudged documents as non-relevant for evaluation [^p26].

**Statistical significance testing**: the book recommends Wilcoxon signed-rank test or sign test over paired query sets. Student's t-test is also used but assumes normality. A difference in MAP of ~0.005–0.010 is typically statistically significant at p < 0.05 over 50+ TREC queries [^p26].

**Efficiency metrics** (Chapter 13): throughput (queries/second) vs. latency (ms/query) trade-off. Throughput measures batched workloads; latency measures interactive workloads. Index layout optimizations (e.g., grouping high-frequency term postings on adjacent disk blocks) can improve both [^p27].

## Applications (Part V)

### Web search (Chapter 15)

**PageRank** (Page et al., 1998): a random-walk model over the Web graph. The PageRank score of a page p is [^p29]:

```
PR(p) = (1 − d) + d × Σ_{q→p} PR(q) / out-degree(q)
```

where d ≈ 0.85 (damping factor modeling the probability that a random surfer follows a link vs. teleports). PageRank is computed iteratively until convergence; it is query-independent and can be precomputed [^p29].

**HITS (Hyperlink-Induced Topic Search)** (Kleinberg, 1999): query-dependent link analysis. Distinguishes **hubs** (pages with many outgoing links to authorities) and **authorities** (pages with many incoming links from hubs). Hub/authority scores are computed iteratively on the subgraph of pages relevant to the query [^p29].

**Web crawler architecture** [^p30]:
- **Frontier**: priority queue of URLs to fetch; priority based on freshness, PageRank estimate, or crawl budget.
- **Fetcher**: downloads page, extracts links, deduplicates against visited-URL set.
- **robots.txt**: per-site crawl exclusion standard; must be respected. Also governs crawl politeness (delay between requests to the same host).
- **Near-duplicate detection**: SimHash or shingling to identify near-duplicate pages and avoid redundant index entries.

**Web spam detection**: recognizes link-spam farms (artificial link structures boosting PageRank), content spam (keyword stuffing), and cloaking. TrustRank (Gyöngyi et al., 2004) seeds a trusted set of high-quality sites and propagates trust scores via reverse PageRank [^p31].

### XML retrieval (Chapter 16)

**Region algebra** (Clarke, Cormack, Burkowski, 1995): a set algebra over non-overlapping or nested text spans. Key operators [^p31]:

| Operator | Notation | Meaning |
|---|---|---|
| Contained-in | A < B | All spans of A that are contained in a span of B |
| Contains | A > B | All spans of A that contain a span of B |
| Before | A ← B | All spans of A that immediately precede a span of B |
| After | A → B | All spans of A that immediately follow a span of B |
| Followed-by | A ;; B | All (A, B) pairs where A immediately precedes B |

Clarke's **GC-lists** (Generalized Containment lists) are the implementation data structure: positional posting lists annotated with span start/end, enabling efficient evaluation of containment operators in O(m + n) time per operator [^p32].

**INEX (Initiative for the Evaluation of XML Retrieval)**: annual evaluation campaign for XML retrieval. Uses Cumulated Gain (CG) adapted for element granularity; judges specify both the relevant element and the appropriate granularity (character-level overlap scoring) [^p32].

## Document types

The book uses "document" generically for any unit returnable as a search result (email, Web page, article, video). **Elements** are predefined components of a larger object (pages, paragraphs). **Snippets** are arbitrary text passages [^p01].

## Key authors

- [Stefan Büttcher](/ai-engineering/stefan-buttcher.md) — doctoral student of Clarke; developer of Wumpus IR system; primary contributor to schema-independent indexing and logarithmic merge
- [Charles L.A. Clarke](/ai-engineering/charles-clarke.md) — University of Waterloo; inventor of region algebra and GC-lists for XML retrieval; Clarke's doctoral advisor was Cormack
- [Gordon V. Cormack](/ai-engineering/gordon-cormack.md) — University of Waterloo; expertise in metalearning, spam filtering, and active learning for relevance assessment

## Relation to other IR sources

This textbook is a companion to the earlier [Information Retrieval: A Survey (Greengrass, 2000)](/ai-engineering/sources/information-retrieval-a-survey.md), which surveys classical IR theory. Büttcher et al. go deeper on implementation, add statistical evaluation methodology, and cover modern Web search and parallel IR. Part I of this book independently covers the foundational topics of Part II of the Greengrass survey [^p01].

## See also

- [Classical Information Retrieval](/ai-engineering/information-retrieval.md) — the synthesis page incorporating both IR textbooks
- [Query Expansion and Relevance Feedback](/ai-engineering/query-expansion.md)

---

[^p01]: [Information Retrieval: Implementing and Evaluating Search Engines — Part 1](../../../raw/pdf/pdf-information-retrieval-implementing-and-evaluating-part-01.md)
[^p02]: [Information Retrieval: Implementing and Evaluating Search Engines — Part 2](../../../raw/pdf/pdf-information-retrieval-implementing-and-evaluating-part-02.md)
[^p03]: [Information Retrieval: Implementing and Evaluating Search Engines — Part 3](../../../raw/pdf/pdf-information-retrieval-implementing-and-evaluating-part-03.md)
[^p04]: [Information Retrieval: Implementing and Evaluating Search Engines — Part 4](../../../raw/pdf/pdf-information-retrieval-implementing-and-evaluating-part-04.md)
[^p05]: [Information Retrieval: Implementing and Evaluating Search Engines — Part 5](../../../raw/pdf/pdf-information-retrieval-implementing-and-evaluating-part-05.md)
[^p06]: [Information Retrieval: Implementing and Evaluating Search Engines — Part 6](../../../raw/pdf/pdf-information-retrieval-implementing-and-evaluating-part-06.md)
[^p07]: [Information Retrieval: Implementing and Evaluating Search Engines — Part 7](../../../raw/pdf/pdf-information-retrieval-implementing-and-evaluating-part-07.md)
[^p08]: [Information Retrieval: Implementing and Evaluating Search Engines — Part 8](../../../raw/pdf/pdf-information-retrieval-implementing-and-evaluating-part-08.md)
[^p09]: [Information Retrieval: Implementing and Evaluating Search Engines — Part 9](../../../raw/pdf/pdf-information-retrieval-implementing-and-evaluating-part-09.md)
[^p10]: [Information Retrieval: Implementing and Evaluating Search Engines — Part 10](../../../raw/pdf/pdf-information-retrieval-implementing-and-evaluating-part-10.md)
[^p11]: [Information Retrieval: Implementing and Evaluating Search Engines — Part 11](../../../raw/pdf/pdf-information-retrieval-implementing-and-evaluating-part-11.md)
[^p12]: [Information Retrieval: Implementing and Evaluating Search Engines — Part 12](../../../raw/pdf/pdf-information-retrieval-implementing-and-evaluating-part-12.md)
[^p13]: [Information Retrieval: Implementing and Evaluating Search Engines — Part 13](../../../raw/pdf/pdf-information-retrieval-implementing-and-evaluating-part-13.md)
[^p14]: [Information Retrieval: Implementing and Evaluating Search Engines — Part 14](../../../raw/pdf/pdf-information-retrieval-implementing-and-evaluating-part-14.md)
[^p15]: [Information Retrieval: Implementing and Evaluating Search Engines — Part 15](../../../raw/pdf/pdf-information-retrieval-implementing-and-evaluating-part-15.md)
[^p16]: [Information Retrieval: Implementing and Evaluating Search Engines — Part 16](../../../raw/pdf/pdf-information-retrieval-implementing-and-evaluating-part-16.md)
[^p17]: [Information Retrieval: Implementing and Evaluating Search Engines — Part 17](../../../raw/pdf/pdf-information-retrieval-implementing-and-evaluating-part-17.md)
[^p18]: [Information Retrieval: Implementing and Evaluating Search Engines — Part 18](../../../raw/pdf/pdf-information-retrieval-implementing-and-evaluating-part-18.md)
[^p19]: [Information Retrieval: Implementing and Evaluating Search Engines — Part 19](../../../raw/pdf/pdf-information-retrieval-implementing-and-evaluating-part-19.md)
[^p20]: [Information Retrieval: Implementing and Evaluating Search Engines — Part 20](../../../raw/pdf/pdf-information-retrieval-implementing-and-evaluating-part-20.md)
[^p21]: [Information Retrieval: Implementing and Evaluating Search Engines — Part 21](../../../raw/pdf/pdf-information-retrieval-implementing-and-evaluating-part-21.md)
[^p22]: [Information Retrieval: Implementing and Evaluating Search Engines — Part 22](../../../raw/pdf/pdf-information-retrieval-implementing-and-evaluating-part-22.md)
[^p23]: [Information Retrieval: Implementing and Evaluating Search Engines — Part 23](../../../raw/pdf/pdf-information-retrieval-implementing-and-evaluating-part-23.md)
[^p24]: [Information Retrieval: Implementing and Evaluating Search Engines — Part 24](../../../raw/pdf/pdf-information-retrieval-implementing-and-evaluating-part-24.md)
[^p25]: [Information Retrieval: Implementing and Evaluating Search Engines — Part 25](../../../raw/pdf/pdf-information-retrieval-implementing-and-evaluating-part-25.md)
[^p26]: [Information Retrieval: Implementing and Evaluating Search Engines — Part 26](../../../raw/pdf/pdf-information-retrieval-implementing-and-evaluating-part-26.md)
[^p27]: [Information Retrieval: Implementing and Evaluating Search Engines — Part 27](../../../raw/pdf/pdf-information-retrieval-implementing-and-evaluating-part-27.md)
[^p28]: [Information Retrieval: Implementing and Evaluating Search Engines — Part 28](../../../raw/pdf/pdf-information-retrieval-implementing-and-evaluating-part-28.md)
[^p29]: [Information Retrieval: Implementing and Evaluating Search Engines — Part 29](../../../raw/pdf/pdf-information-retrieval-implementing-and-evaluating-part-29.md)
[^p30]: [Information Retrieval: Implementing and Evaluating Search Engines — Part 30](../../../raw/pdf/pdf-information-retrieval-implementing-and-evaluating-part-30.md)
[^p31]: [Information Retrieval: Implementing and Evaluating Search Engines — Part 31](../../../raw/pdf/pdf-information-retrieval-implementing-and-evaluating-part-31.md)
[^p32]: [Information Retrieval: Implementing and Evaluating Search Engines — Part 32](../../../raw/pdf/pdf-information-retrieval-implementing-and-evaluating-part-32.md)

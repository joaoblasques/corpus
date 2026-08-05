---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-information-retrieval-a-survey-part-01.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/_inbox/pdf-information-retrieval-a-survey-part-02.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/_inbox/pdf-information-retrieval-a-survey-part-03.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/_inbox/pdf-information-retrieval-a-survey-part-04.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/_inbox/pdf-information-retrieval-a-survey-part-05.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/_inbox/pdf-information-retrieval-a-survey-part-06.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/_inbox/pdf-information-retrieval-implementing-and-evaluating-part-01.md
    channel: pdf
    ingested_at: 2026-08-05
aliases:
  - IR
  - information retrieval
  - classical IR
  - TF-IDF
  - tf-idf
  - term frequency-inverse document frequency
  - BM25
  - Okapi BM25
  - vector space model
  - VSM
  - Boolean retrieval
  - extended Boolean
  - p-norm model
  - LSI
  - latent semantic indexing
  - precision and recall
  - recall
  - precision
  - F-measure
  - inverted index
tags:
  - corpus/ai-engineering
  - concept
created: 2026-08-03
updated: 2026-08-05
---

# Classical Information Retrieval

**TL;DR**: Information Retrieval (IR) is the field concerned with finding textual documents relevant to a user's information need. Classical IR (pre-deep-learning) developed the foundational methods — Boolean models, vector space with TF-IDF, BM25, probabilistic models, LSI — that underpin modern systems. Precision/recall evaluation, the inverted index, and the scoring functions from this era remain the backbone of keyword search and the sparse-retrieval leg of hybrid RAG systems [^p01].

## Definitions and document types

An IR system retrieves **unstructured records** (free-form natural language text) in response to a query. Documents may be structured (relational database rows), semi-structured (HTML with a body), or unstructured (free text). IR focuses on the unstructured body [^p01].

Two retrieval modes [^p01]:

| Mode | Queries | Document collection |
|---|---|---|
| **Ad-hoc querying** | Many, arbitrary queries | Fixed, static collection |
| **Routing/filtering** | Fixed topics or profiles | Incoming stream (dynamic) |

## Probability Ranking Principle and relevance dimensions

The **Probability Ranking Principle (PRP)** (Robertson, 1977): "If an IR system's response to each query is a ranking of the documents in the collection in order of decreasing probability of relevance, then the overall effectiveness of the system to its users will be maximized." [^bce01]

PRP is the foundational axiom of ranked retrieval. It specifies what to optimize — estimated P(relevant | document, query) — but does not prescribe how to compute it (that is the job of BM25, language models, etc.).

**Performance dimensions** [^bce01]:
- **Efficiency**: latency (response time), throughput (queries/second), storage. Web-scale systems may require 10,000+ queries/second.
- **Effectiveness**: relevance — depends entirely on human judgment.

**Relevance nuances beyond binary** [^bce01]:

| Dimension | Definition |
|---|---|
| **Specificity** | Fraction of document content related to the information need |
| **Exhaustivity** | Fraction of the information need covered by the document |
| **Novelty** | Incremental value after prior results already conveyed related content |

Specificity and exhaustivity are independent dimensions. A large document can be exhaustive (covers everything) but not specific (contains much unrelated material); a focused paragraph can be specific but not exhaustive.

## Evaluation: precision, recall, and F-measure

At the heart of IR evaluation is **relevance** — a subjective judgment by the user of whether a retrieved document satisfies their information need [^p01].

**Precision**: fraction of retrieved documents that are relevant.
> P = relevant ∩ retrieved / retrieved

**Recall**: fraction of all relevant documents that are retrieved.
> R = relevant ∩ retrieved / all relevant

"If one retrieves all documents in a collection, recall will be perfect (1.0) but precision will be near zero in the typical case where few documents are relevant to a given query." [^p01]

**F-measure** (van Rijsbergen's E-measure): a parameterized blend of P and R, where α controls the relative weight of precision vs. recall. When α = 0.5, P and R receive equal weight [^p01].

**Average precision**: area under the precision-recall curve, summarizing system performance across all recall levels. _Eleven-point average precision_ computes precision at recall values 0, 0.1, 0.2, …, 1.0 and averages the 11 values. The TREC conference standardized this measure [^p01].

Measuring recall requires knowing the total number of relevant documents in the collection — infeasible for large collections. TREC circumvents this by pooling the top-100 results from all competing systems [^p01].

## Boolean retrieval

The classical Boolean model uses AND, OR, NOT operators. A Boolean query either returns a document as relevant or excludes it — no ranking [^p01].

Extensions:
- **Proximity operators**: require two terms to appear within n words/sentences/paragraphs of each other [^p01].
- **Automatic Boolean generation** (Salton): extract user query terms, compute pairwise correlation, group co-occurring term pairs (or triples) with AND, and OR the groups together. High-IDF terms rank higher, giving the user control over retrieved set size without true relevance ranking [^p01].

Limitation: "A document containing all [or many of] the query terms is not treated better than a document containing one term" for OR queries, and one missing term in an AND query produces the same score as all terms missing [^p02].

## Extended Boolean (p-norm model)

Extended Boolean operators return similarity values in [0, 1] rather than binary true/false. Lee (SIGIR '94) showed that the **p-norm model** (Salton et al., CACM 1983) has the most desirable properties among extended Boolean models [^p02]:

- At p = ∞: equivalent to classical Boolean (strict phrase/thesaurus assignment).
- At p = 2–5: "loose" phrase assignment (missing a term reduces score but does not zero it out).
- At p = 1: degenerates into the vector space cosine similarity — AND and OR become identical [^p02].

The p-norm model supports per-operator p values, allowing users to mix strict and loose interpretations within one query [^p02].

## Vector space model (TF-IDF)

Each document and query is represented as a weighted term vector. The weight of term t in document D measures how effective t is at distinguishing D from other documents. Retrieval ranks documents by vector similarity to the query vector [^p01].

### Term weighting

**Term frequency (TF)**: raw count of term t in document D. High TF → t is important in D.

**Inverse document frequency (IDF)**: log(N / df(t)), where N = total documents, df(t) = documents containing t. High IDF → t is rare across the collection and therefore a good discriminator.

**TF-IDF weight**: tf(t, D) × idf(t). The SMART system used a family of TF-IDF variants parameterized by 3-character codes specifying: term-frequency normalization, IDF variant, and vector-length normalization [^p02].

Common weighting strategies [^p02]:

| Code | Transform | Description |
|---|---|---|
| `n` | raw tf | no normalization |
| `l` | 1 + log(tf) | logarithmic smoothing |
| `t` | × log(N/df) | IDF scaling |
| `c` | cosine | vector-length normalization |

**Pivoted unique normalization (Lnu)**: addresses the fact that standard cosine normalization over-penalizes short documents. Pivots normalization around the "pivot point" — the document length at which non-normalized and cosine-normalized retrieval produce the same average relevance [^p02].

### Inverted index

The standard implementation: for each term t, store a list of (document_id, tf) pairs (the "posting list"). At query time, look up posting lists for all query terms and compute similarity. Only documents sharing terms with the query need be examined [^p03].

### Similarity functions

Beyond TF-IDF cosine similarity, other metrics [^p03]:
- **Dice's coefficient**: 2w / (n1 + n2) where w = matching terms, n1/n2 = non-zero terms in each vector. Performs normalization that favors short relevant documents.
- **Jaccard coefficient**: w / (n1 + n2 − w).
- **Minkowski family**: city-block (p=1), Euclidean (p=2), maximal direction (p=∞).

### Passage-level retrieval

Documents may contain multiple topics. Matching at the **passage level** (fixed-length windows of 150+ words, or paragraph boundaries) rather than the whole document can improve precision. Kaszkiel et al. (SIGIR '97) found that non-overlapping fixed-length passages of 150+ words "simple; highly effective; robust" across multiple datasets [^p03].

## Latent Semantic Indexing (LSI)

The traditional vector space model assumes term independence — a term about "automobile" will not match a document using only "car." **LSI** (Deerwester et al., JASIS 1990) addresses polysemy and synonymy by decomposing the term-by-document matrix using **Singular Value Decomposition (SVD)** [^p03].

The decomposition produces three matrices T (terms × k), S (k × k diagonal), D (k × documents). The k columns correspond to derived "latent semantic factors" — artificial concepts representing groups of co-occurring terms. Truncating to the top-k factors:

- **Reduces dimensionality**: captures most of the variance with far fewer dimensions than raw terms.
- **Captures synonymy**: "car" and "automobile" will have similar k-space representations because they co-occur with the same context words.
- **Reduces polysemy**: the LSI vector for an ambiguous term is "a weighted average of the different meanings of the term" [^p03].

Optimal k typically ranges between 100 and 200 for large document collections [^p03].

**Drawbacks of LSI** [^p03]:
- Larger storage than sparse term-document matrix (LSI values are real, not integer).
- Cannot exploit inverted-index sparsity: every document must be compared against every query.
- Computationally expensive to build; updating requires "folding in" (cheap, approximate) or "SVD updating" (expensive, more accurate).
- May degrade retrieval for documents well-described by a few precise terms (e.g., "Hubble Space Telescope").

## Probabilistic approaches

Probabilistic IR ranks documents by estimated **probability of relevance** to the query, rather than by similarity score [^p04].

### Binary Independence Model (BIM)

The BIM (Robertson & Sparck Jones, 1976) assumes: (1) term independence, (2) binary term occurrence (present/absent). Given relevance judgment training data, the weight for each term t is derived from a contingency table comparing term frequency in relevant vs. non-relevant documents. The resulting ranking function is the **Robertson-Sparck Jones (RSJ) formula**, which assigns positive weight to terms appearing more in relevant documents and negative weight to terms appearing more in non-relevant documents [^p04].

### Bayesian inference networks (INQUERY)

INQUERY's model (Turtle & Croft, 1991) represents documents and queries as a Bayesian network. Document nodes feed concept nodes, which feed query nodes. Each node computes a belief (probability) that the information need is satisfied given the observed evidence. The model naturally handles:

- Combination of term-based and Boolean queries in one probabilistic framework.
- Soft Boolean operators (AND, OR) modeled as Parent Indifference Criterion (PIC) operators that evaluate belief based on how many parent terms are present, not which specific ones [^p05].

INQUERY supports weighted sum, unweighted sum, and proximity operators within the same inference network [^p05].

### Logistic regression (Cooper et al.)

Cooper et al. (SIGIR '92, TREC) fit a logistic regression model to the log-odds of relevance. Each document is described by a two-level feature hierarchy: composite clues (e.g., a word stem) contain elementary clues (term frequency in query, in document, and in collection). The BM25 formula (below) uses a simpler but related approach [^p05].

### Okapi BM25

Robertson et al. (SIGIR '94) derived **BM25** ("Best Match 25") from a **Two-Poisson Model**: documents are modeled as streams of term occurrences; the frequency distribution of term t differs for "elite" documents (those "about" t) vs. non-elite documents. The resulting term weight approximation function is [^p05]:

```
BM25(Q, D) = Σ_{t∈Q} IDF(t) × (tf × (k1 + 1)) / (tf + K) × (qtf × (k3 + 1)) / (qtf + k3)
```

where:
- `K = k1 × ((1 − b) + b × (dl / avdl))` adjusts for document length
- `k1` (default 1.2): controls TF saturation — high values reward more occurrences; low values cap the reward quickly
- `b` (default 0.75): document-length normalization strength (0 = no length normalization, 1 = full verbosity hypothesis)
- `k3` (default 7–1000): query-term frequency saturation

BM25 has been consistently among the top-performing retrieval functions across TREC competitions through TREC-9 [^p05]. It is the standard sparse-retrieval baseline and the "BM25" component in modern hybrid RAG systems.

## n-gram vector space

Instead of word-level terms, **n-grams** (strings of n consecutive characters, n = 5–6) can serve as vector dimensions [^p03]. Properties:

- **Language-independent**: no prior knowledge of vocabulary or grammar required.
- **Robust to noise**: spelling errors and OCR degradation affect only a few n-grams per word; most remain intact. Damashek (Science 1995) maintained 17/20 cluster membership at 15% character corruption.
- **Blind clustering by language**: n-gram similarity groups documents by language automatically, without knowing which languages are present.
- Disadvantage: much larger vector space (all n-grams in the collection) and requires larger storage.

Centroid subtraction (subtracting the mean of all document vectors) removes "background" n-grams common across topics, equivalent to stopword removal in a language-independent way [^p03].

## Routing and classification methods

In routing, queries (topics) are static but the document stream is dynamic. Classification methods trained on relevance-judged training data include [^p05]:

- **Naive Bayes**: treats term presence/absence as independent binary features; computes P(relevant | terms present).
- **Neural networks**: fit a logistic classifier or multi-layer network to map term weights → relevance probability.
- **Linear discriminant analysis (LDA)**: linear boundary in term-weight feature space.
- **k-Nearest Neighbors**: classify each document by the majority relevance label of its k most similar training documents.
- **Boosting (AdaBoost)**: combine many weak single-term classifiers into a strong ensemble; each iteration reweights the training set to focus on previously misclassified documents [^p12].
- **Support Vector Machines (SVM)**: find the maximum-margin hyperplane in the term-weight feature space that separates relevant from non-relevant documents.

Feature-space dimensionality is a critical challenge: with all significant terms as features, standard classifiers overfit. LSI dimensionality reduction or explicit feature selection is required before training [^p05].

## Stemming and stop lists

Preprocessing reduces vocabulary size and normalizes term variants [^p01]:

- **Stemming** (Porter, 1980): reduce each word to its root form. "Retrieve," "retrieves," "retrieved," "retrieval" all map to "retriev." Language-dependent.
- **Stop lists**: remove highly frequent, semantically weak words ("the," "a," "it"). Language-dependent.
- **n-gram analysis**: bypasses both, at the cost of a larger term space.

## Connection to modern systems

Classical IR concepts remain live in production systems [^p01] [^p05]:

| Classical IR | Modern equivalent |
|---|---|
| TF-IDF inverted index | Sparse retrieval in hybrid search (BM25 leg) |
| Cosine similarity | Dense embedding similarity (replaces but does not eliminate TF-IDF) |
| Relevance feedback (Rocchio) | Query expansion; see [Query Expansion](/ai-engineering/query-expansion.md) |
| LSI / SVD | Dense embeddings via neural encoders (e.g., Sentence-Transformers) are the deep-learning successor |
| BM25 | Still used as the sparse component in hybrid RAG; default in Elasticsearch, OpenSearch, Vespa |
| Routing/classification | LLM-based routing and filtering |

BM25 is explicitly used in modern RAG as the keyword-matching complement to dense vector similarity. "Hybrid search blends dense embeddings with sparse keyword (BM25) matching" to recover exact-token matches (names, IDs, codes) that pure embeddings smooth away [^p01]. See [RAG](/ai-engineering/rag.md) §Hybrid search.

## See also

- [Embeddings](/ai-engineering/embeddings.md) — dense vectors as the deep-learning successor to TF-IDF and LSI
- [RAG](/ai-engineering/rag.md) — hybrid search combines BM25 (classical IR) with dense retrieval
- [Singular Value Decomposition (SVD)](/ai-engineering/singular-value-decomposition.md) — the matrix factorization underpinning LSI
- [Query Expansion](/ai-engineering/query-expansion.md) — relevance feedback and pseudo-relevance feedback
- [Clustering Methods](/ai-engineering/clustering-methods.md) — document clustering for browsing and retrieval
- [NLP Deep Learning](/ai-engineering/nlp-deep-learning.md) — modern NLP methods that succeeded classical IR approaches

---

[^p01]: [Information Retrieval: A Survey (Greengrass, 2000) — Part 1](../../raw/pdf/pdf-information-retrieval-a-survey-part-01.md)
[^p02]: [Information Retrieval: A Survey (Greengrass, 2000) — Part 2](../../raw/pdf/pdf-information-retrieval-a-survey-part-02.md)
[^p03]: [Information Retrieval: A Survey (Greengrass, 2000) — Part 3](../../raw/pdf/pdf-information-retrieval-a-survey-part-03.md)
[^p04]: [Information Retrieval: A Survey (Greengrass, 2000) — Part 4](../../raw/pdf/pdf-information-retrieval-a-survey-part-04.md)
[^p05]: [Information Retrieval: A Survey (Greengrass, 2000) — Part 5](../../raw/pdf/pdf-information-retrieval-a-survey-part-05.md)
[^p06]: [Information Retrieval: A Survey (Greengrass, 2000) — Part 6](../../raw/pdf/pdf-information-retrieval-a-survey-part-06.md)
[^p12]: [Information Retrieval: A Survey (Greengrass, 2000) — Part 12](../../raw/pdf/pdf-information-retrieval-a-survey-part-12.md)
[^bce01]: [Information Retrieval: Implementing and Evaluating Search Engines (Büttcher, Clarke, Cormack, 2010) — Part 1](../../raw/pdf/pdf-information-retrieval-implementing-and-evaluating-part-01.md)

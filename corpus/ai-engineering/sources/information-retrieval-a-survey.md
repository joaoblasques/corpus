---
type: source
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
  - path: raw/_inbox/pdf-information-retrieval-a-survey-part-07.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/_inbox/pdf-information-retrieval-a-survey-part-08.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/_inbox/pdf-information-retrieval-a-survey-part-09.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/_inbox/pdf-information-retrieval-a-survey-part-10.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/_inbox/pdf-information-retrieval-a-survey-part-11.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/_inbox/pdf-information-retrieval-a-survey-part-12.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/_inbox/pdf-information-retrieval-a-survey-part-13.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/_inbox/pdf-information-retrieval-a-survey-part-14.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/_inbox/pdf-information-retrieval-a-survey-part-15.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/_inbox/pdf-information-retrieval-a-survey-part-16.md
    channel: pdf
    ingested_at: 2026-08-03
aliases:
  - Greengrass 2000
  - Information Retrieval A Survey
tags:
  - corpus/ai-engineering
  - source
created: 2026-08-03
updated: 2026-08-03
---

# Information Retrieval: A Survey (Ed Greengrass, November 2000)

**Source**: Technical report, 224 pages. Ed Greengrass. November 30, 2000.

**TL;DR**: A comprehensive tutorial and survey of the state of the art in information retrieval as of 2000. Covers the full spectrum from classical Boolean IR through vector space models (TF-IDF, BM25), probabilistic models (BIM, Bayesian inference networks), NLP approaches (phrase identification, concept matching, information extraction), document clustering, query expansion (Rocchio, pseudo-relevance feedback, WordNet), fusion of results (CombMNZ), and Web-based IR (crawlers, link analysis, meta-search). The foundational reference for classical IR methods that underpin modern hybrid RAG systems.

## Structure

| Chapter | Topics | PDF Parts |
|---|---|---|
| 1–2 | Introduction, IR definitions, structured vs. unstructured documents, ad-hoc querying vs. routing, precision/recall/F-measure evaluation | 1 |
| 3–4 | Approaches overview; Classical Boolean IR, proximity operators, automatic Boolean query generation | 1 |
| 5 | Extended Boolean (p-norm model) | 1–2 |
| 6 | Vector Space Model: TF-IDF, term weighting schemes, normalization, cosine similarity, passage retrieval, LSI/SVD, n-gram vectors | 2–3 |
| 7 | Probabilistic approach: Binary Independence Model, Bayesian inference networks (INQUERY), logical imaging, logistic regression, Okapi BM25 | 4–5 |
| 8 | Routing and classification: Naive Bayes, neural nets, LDA, SVM, dimensionality reduction for classifiers | 5–6 |
| 9 | NLP approaches: phrase identification, word sense disambiguation, concept matching (DR-LINK/SFC vectors), Formal Context Analysis, discourse structure, proper noun recognition/extraction, information extraction | 6–8 |
| 10 | Clustering: hierarchical (single-link, complete-link, group-average, Ward's), heuristic (Buckshot, Fractionation), incremental/Suffix Tree Clustering (STC), cluster validation | 9–10 |
| 11 | Query expansion and refinement: relevance feedback, Rocchio algorithm, pseudo-relevance feedback, LCA, WordNet expansion, re-use of queries, Dynamic Feedback Optimization | 10–11 |
| 12 | Fusion of results: combining multiple retrieval runs (CombSUM, CombANZ, CombMNZ), bagging, boosting (AdaBoost), Condorcet voting | 12 |
| 13 | User interaction: displaying ranked results, scatter/gather browsing, passage-based display | 12–13 |
| 14 | Z39.50 standard: searching and retrieval protocol, Type 102 Ranked List Query extension | 13 |
| 15 | IR systems review: LEXIS/NEXIS, Dialog, Dow Jones, Topic, SMART, INQUERY | 14 |
| 16 | Web-based IR: crawlers, indexing at Web scale, PageRank-style link analysis, meta-search engines, personal web assistants | 14–15 |
| — | References (bibliography) | 16 |

## Key contributions and claims

**Precision/recall trade-off**: "If one retrieves all documents, recall is perfect but precision will be near zero in the typical case." Average precision (area under precision-recall curve) and eleven-point average precision are the standard evaluation metrics from TREC [parts 1].

**Extended Boolean p-norm model**: at p=∞ is strict Boolean; at p=1 reduces to cosine similarity. Shows Boolean and vector-space models as two ends of a continuum [parts 1–2].

**TF-IDF and SMART notation**: the 3-character weighting code convention (tf normalization + idf variant + vector normalization) describes a family of weighting schemes. Pivoted unique normalization (Lnu) eliminates document-length bias better than earlier schemes [parts 2].

**LSI**: SVD reduces the term-by-document matrix to k latent semantic dimensions; captures synonymy and polysemy. Optimal k ≈ 100–200. Trade-off: no longer sparse → every document must be compared against every query [parts 3].

**BM25**: the Two-Poisson model for term frequency gives the BM25 formula, the standard TREC baseline through TREC-9. Key tuning constants: k1 = 1.2 (TF saturation), b = 0.75 (length normalization), k3 = 7–1000 (query-TF saturation) [parts 5].

**Relevance feedback (Rocchio)**: Q_new = A×Q_old + B×(avg of relevant) − C×(avg of non-relevant). Adding top-20 terms by importance outperforms adding all terms from relevant documents [parts 10].

**Pseudo-relevance feedback**: assume top-k retrieved are relevant; automatic expansion; Local Context Analysis (LCA) achieves ~24% precision improvement on TREC-3/4 [parts 10].

**CombMNZ (Fox & Shaw)**: for fusion of multiple retrieval runs: sum of all similarity scores × number of non-zero scores. Outperforms CombSUM; rewards documents retrieved by multiple methods [parts 12].

**STC clustering**: O(N) suffix tree clustering outperforms O(N²) group-average hierarchical clustering for interactive Web result browsing; labelled by shared phrases [parts 9–10].

**DR-LINK (Liddy et al.)**: Subject Field Code (SFC) vectors map word senses to concept categories from LDOCE dictionary; enables topic-level matching that avoids the "search for wars, retrieve sports" failure mode of keyword systems [parts 7–8].

**NLP approaches general finding**: word-sense disambiguation surprisingly degrades retrieval in most cases — the combination of query terms already does disambiguation effectively; a disambiguator must be 90%+ accurate to avoid performance degradation [parts 7].

**Web IR key findings**: Web requires crawling, indexing at massive scale, and link analysis. PageRank-style methods use the hyperlink graph to estimate page authority independent of any query [parts 14–15].

## Corpus pages produced

- [Information Retrieval (Classical IR)](/ai-engineering/information-retrieval.md) — TF-IDF, BM25, vector space model, Boolean IR, precision/recall, LSI, probabilistic IR — primary synthesis; parts 1–6
- [Query Expansion](/ai-engineering/query-expansion.md) — Rocchio, pseudo-relevance feedback, WordNet expansion, LCA — parts 10–11
- [Clustering Methods](/ai-engineering/clustering-methods.md) — Document clustering section added: AHC, Buckshot, Fractionation, STC, cluster validation — parts 9–10

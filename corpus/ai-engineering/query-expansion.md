---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-information-retrieval-a-survey-part-10.md
    channel: pdf
    ingested_at: 2026-08-03
  - path: raw/_inbox/pdf-information-retrieval-a-survey-part-11.md
    channel: pdf
    ingested_at: 2026-08-03
aliases:
  - query expansion
  - relevance feedback
  - pseudo-relevance feedback
  - Rocchio algorithm
  - Rocchio formula
  - blind relevance feedback
  - query refinement
  - WordNet expansion
  - local context analysis
  - LCA
tags:
  - corpus/ai-engineering
  - concept
created: 2026-08-03
updated: 2026-08-03
---

# Query Expansion and Relevance Feedback

**TL;DR**: Query expansion automatically augments a user's short query with additional terms, improving recall without requiring the user to formulate a perfect initial query. The dominant approach — **relevance feedback (Rocchio)** — adds terms from documents judged relevant and reweights existing query terms. The "pseudo-relevance feedback" variant assumes the top-k retrieved documents are relevant and requires no user interaction. Both methods can improve average precision by 20–25% or more [^p10].

## Why queries are short and imprecise

A typical end-user query is a short list of terms. Users are not expected to know all relevant terminology in a large document collection, and they do not want to consult thesauri before querying. Automatic query expansion bridges this gap: "refine and expand the original query automatically based on the documents retrieved by the original query." [^p10]

Adding terms improves recall. Re-weighting existing terms (without adding new ones) also improves precision. Experiments show that both expansion and re-weighting together outperform either approach alone [^p10].

## Relevance feedback (Rocchio algorithm)

The standard interactive approach [^p10]:
1. User issues an initial query; system retrieves and ranks documents.
2. User judges the top N documents as relevant or non-relevant (typically N = 10 documents = one screenful).
3. System extracts terms from judged-relevant documents, adds the best terms to the query, and reweights all terms using the **Rocchio formula**.
4. Expanded query is re-executed; process iterates until the user's need is satisfied.

**Rocchio formula** (Buckley et al., SIGIR '94):
```
Q_new[i] = A × Q_old[i]
          + B × (1/|rel_docs|) × Σ_{d ∈ rel} w(t_i, d)
          − C × (1/|nonrel_docs|) × Σ_{d ∈ nonrel} w(t_i, d)
```
- A, B, C are tuning constants controlling the relative influence of the original query, relevant documents, and non-relevant documents.
- The B term increases the weight of terms appearing frequently in relevant documents.
- The C term decreases the weight of terms appearing in non-relevant documents. Terms whose weight goes negative may be dropped.
- Expansion terms are drawn only from relevant documents; the C term reduces (but never adds) weights [^p10].

**How many expansion terms to add?** Adding the top 20 terms by importance score typically outperforms adding all terms from relevant documents. Adding too many terms dilutes the signal, "causing many non-relevant documents to move up in rank." In routing applications with large training sets, Buckley et al. found improvement up to 500 expansion terms [^p10].

**Which terms to add?** Terms are ranked by importance before selection. Effective criteria:
- `noise × frequency`: noise ≈ IDF (global rarity); frequency = log of total occurrences in judged-relevant documents. Prefers terms rare in the collection but frequent in relevant documents.
- BI weighting formula: `w(t) = log(p_k / (1 - p_k)) - log(u_k / (1 - u_k))` where p_k is P(t | relevant) and u_k is P(t | non-relevant). Probabilistically principled; comparable performance to noise × frequency in experiments [^p10].
- `rdf × idf`: rdf = number of relevant documents containing the term. Simple and effective.

**Passage-level expansion**: Large documents often cover multiple topics. Expanding with terms from the most similar passage of each relevant document (rather than the whole document) avoids adding off-topic terms [^p10].

**LSI as implicit expansion**: Reformulating the query in LSI k-space (see [Information Retrieval](/ai-engineering/information-retrieval.md) §LSI) is a form of expansion without explicit term addition. The resulting query vector is much lower-dimensional than an explicitly expanded query, making retrieval faster [^p10].

## Pseudo-relevance feedback (blind relevance feedback)

Instead of asking the user for relevance judgments, the system **assumes the top-k retrieved documents are relevant** and automatically expands the query using those documents [^p10]:

1. Initial query is executed; top-k documents are retrieved (k = 10–50 is typical).
2. Expansion terms are extracted from these top-k documents using the same ranking methods as interactive relevance feedback.
3. Expanded query is re-executed; the result is presented to the user (who only ever sees the second-pass result).

Advantage: zero user effort.
Risk: if the top-k documents are irrelevant (e.g., the initial query is poor), expansion reinforces errors — a "garbage in, garbage out" amplification. For this reason, pseudo-relevance feedback emphasizes precision in the first-pass ranking: "similarity measures may be employed in this automatic first stage that emphasize precision and sacrifice some recall" [^p10].

## Local Context Analysis (LCA)

Xu & Croft (SIGIR '96) developed a principled pseudo-relevance-feedback method combining global and local statistics [^p10]:

1. Retrieve the top-n best passages (300 words each) from the collection using the original query.
2. For each noun-group concept c appearing in those passages, score:
   ```
   score(c, Q) = Π_{t_i ∈ Q} [Σ_{j=1}^{n} f(t_i, j) × f(c, j) × idf_c / log(n)] ^ idf_i
   ```
   Co-occurrence of c with all query terms is rewarded (multiplication across query terms: one weak co-occurrence tanks the score).
3. The top-m concepts (m = 70 in experiments) form an auxiliary query, combined with the original Q by weighted sum.

Results: 24.4% improvement in average precision on TREC-3, 23.5% on TREC-4. Performance is flat over a wide range of passage counts (30–300), reducing sensitivity to this hyperparameter [^p10].

## Thesaurus-based expansion

A complementary approach: expand each query term with synonyms or semantically related terms from a thesaurus, without any retrieved documents [^p10]:

- **Generic thesaurus**: WordNet (Princeton, public domain) provides synonym sets (synsets) and hypernym/hyponym relations. A term can be expanded with its WordNet synonyms, or replaced by a hypernym (more general term) for broader recall.
- **Collection-specific thesaurus**: built from term co-occurrence or adjacency statistics within the target collection (e.g., INQUERY's PhraseFinder). Better suited to domain-specific vocabularies.
- **Boolean expansion**: in Boolean queries, each query term can be ORed with its thesaurus synonyms, then the term-synonym groups ANDed together.

Thesaurus expansion is fully automatic (no user interaction), making it suitable for routing and filtering applications. It can be combined with relevance feedback: use the thesaurus to seed the first-pass query, then apply Rocchio to refine [^p10].

## Query re-weighting without expansion

Re-weighting can be applied independently of adding new terms. After relevance feedback, the Rocchio formula updates weights of existing query terms: terms appearing frequently in relevant documents gain weight; terms appearing in non-relevant documents lose weight. Even without adding a single new term, this re-weighting can improve ranking. However, "experiment indicates that both expansion and re-weighting improve retrieval performance" over either alone [^p10].

## Query reuse

Long-running systems can accumulate and reuse effective queries from past sessions [^p11]:

- **Explicit reuse**: prior queries for similar information needs are identified (by user or system) and adapted for new queries.
- **Profile-based routing**: standing queries (user profiles) represent recurring information needs. The profile is refined over time as the user judges relevance of incoming documents — essentially continuous relevance feedback.
- **Rhagavan and Sever's method (SIGIR '95)**: formulate query expansion as a **preference optimization problem**. Given a preference relation (user prefers D1 to D2), search in query space for the query vector that maximally preserves these preferences. Uses steepest-descent search in term-weight space. Related to the linear combination fusion approach [^p11].
- **Dynamic Feedback Optimization (DFO)**: Buckley and Salton's technique to prevent over-expansion (overfitting to the training set) by limiting the number of expansion terms and monitoring performance [^p11].

## Trade-offs and failure modes

| Issue | Description | Mitigation |
|---|---|---|
| **Relevance drift** | Over-expanded query starts retrieving documents about the expansion terms rather than the original topic | Limit expansion to top 20 terms; use Rocchio's A parameter to preserve original query weight |
| **Long queries are slow** | "Efficient large-scale retrieval systems have response times heavily dependent on the number of query terms" | Set a term limit; prefer LCA's passage-level expansion |
| **Bad initial retrieval** | Pseudo-relevance feedback amplifies a poor initial query | Use precision-oriented first pass; restrict expansion to high-IDF terms |
| **Topic drift in routing** | Real-world document distribution shifts over time; trained classifiers become stale | Regular re-training on fresh relevance judgments |

## Connection to modern systems

Classical query expansion concepts survive in modern retrieval [^p10]:
- **HyDE (Hypothetical Document Embeddings)**: generates a hypothetical answer document and uses its embedding as the query vector — a neural analogue of pseudo-relevance feedback.
- **RAG query rewriting**: LLM rewrites the user's query before retrieval — analogous to automatic query expansion but using generative paraphrase instead of term extraction.
- **Relevance feedback in recommender systems**: Rocchio-style updates underpin collaborative filtering item-weight updates.

See [RAG](/ai-engineering/rag.md) for how dense retrieval and hybrid search relate to these classical foundations.

## See also

- [Information Retrieval](/ai-engineering/information-retrieval.md) — classical IR methods (TF-IDF, BM25, vector space, Boolean)
- [RAG](/ai-engineering/rag.md) — modern retrieval-augmented generation; hybrid search (dense + BM25)
- [Embeddings](/ai-engineering/embeddings.md) — dense vectors as the modern alternative to TF-IDF for query representation
- [Clustering Methods](/ai-engineering/clustering-methods.md) — document clustering for browsing and retrieval

---

[^p10]: [Information Retrieval: A Survey (Greengrass, 2000) — Part 10](../../raw/pdf/pdf-information-retrieval-a-survey-part-10.md)
[^p11]: [Information Retrieval: A Survey (Greengrass, 2000) — Part 11](../../raw/pdf/pdf-information-retrieval-a-survey-part-11.md)

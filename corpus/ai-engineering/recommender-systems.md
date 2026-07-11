---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-zhang-lipton-li-smola-dive-into-deep-learning-cc-by-sa-4-0-part-40.md
    channel: pdf
    ingested_at: 2026-07-11
aliases:
  - recommender system
  - recommendation system
  - collaborative filtering
  - matrix factorization
  - CTR prediction
  - click-through rate
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-11
updated: 2026-07-11
---

# Recommender Systems

**TL;DR**: Recommender systems help users discover relevant items (movies, articles, products) from large catalogs. They are among the most economically impactful ML applications; recommendation, not search, drives most content consumption on major internet platforms [^src1].

## Three prediction tasks

| Task | Input | Output | Used for |
|---|---|---|---|
| Rating prediction | User, item | Predicted star rating | Netflix-style rating prediction |
| Top-k item generation | User | Ranked list of items | "You might also like" |
| Click-through rate (CTR) | User, item, context features | P(click) | Ads, news feed ranking |

## Collaborative filtering

The dominant paradigm: infer preferences from the collective behavior of all users, not from item content. Key insight: users who agreed in the past will agree in the future. Two variants [^src1]:

- **Memory-based CF**: find similar users (user-user) or similar items (item-item) and aggregate their ratings directly. Scales poorly to millions of users/items.
- **Model-based CF**: learn latent representations. Matrix factorization (e.g. SVD, ALS) decomposes the user-item rating matrix into low-rank embeddings: `r̂_{ui} = p_u^T q_i` where `p_u` is the user embedding and `q_i` is the item embedding.

**Deep CF**: replace dot product with a multi-layer neural network — Neural Collaborative Filtering (NCF). Learns non-linear user-item interactions that linear matrix factorization cannot capture [^src1].

## Content-based and hybrid methods

Content-based filtering uses item features (genre, text, image) to recommend items similar to those a user liked. Hybrid systems combine collaborative and content-based signals — most production systems are hybrid [^src1].

## Feature-based CTR models

For CTR prediction, many features are available: user demographics, item metadata, contextual signals (time, device, location). Models:

- **Factorization Machines (FM)**: model pairwise feature interactions via learned factor vectors — efficient even with sparse, high-cardinality categorical features [^src1].
- **DeepFM / Wide & Deep**: combine FM/linear components for memorization with deep networks for generalization.

## The cold-start problem

New users and new items have no interaction history — collaborative filtering cannot make recommendations. Mitigations: use content features (cold-start via content-based), ask users for initial preferences (onboarding), or fall back to popularity-based recommendations [^src1].

## Connections to other corpus pages

- [MLP](/ai-engineering/mlp.md) — deep neural collaborative filtering uses feedforward networks.
- [Attention Mechanisms](/ai-engineering/attention-mechanisms.md) — transformer-based recommenders (BERT4Rec, SASRec) use self-attention over item interaction sequences.
- [NLP Deep Learning](/ai-engineering/nlp-deep-learning.md) — word2vec ideas transfer to item embeddings (item2vec); language model pretraining on interaction sequences.

---

[^src1]: [D2L Part 40 — Recommender Systems (Overview, CF, CTR)](../../raw/pdf/pdf-zhang-lipton-li-smola-dive-into-deep-learning-cc-by-sa-4-0-part-40.md)

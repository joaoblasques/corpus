---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-zhang-lipton-li-smola-dive-into-deep-learning-cc-by-sa-4-0-part-22.md
    channel: pdf
    ingested_at: 2026-07-10
aliases:
  - NLP deep learning
  - word embeddings
  - word2vec
  - GloVe
  - fastText
  - BERT
  - contextualized representations
  - language pretraining
  - NLP pretraining
  - sentiment analysis
  - natural language inference
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-10
updated: 2026-07-10
---

# NLP with Deep Learning

**TL;DR**: Deep learning for NLP progresses from static word embeddings (word2vec, GloVe — one vector per word) to subword embeddings (fastText) to contextualized representations (ELMo) to large-scale pretrained Transformers (BERT, GPT). BERT's bidirectional pretraining with masked language modeling and next-sentence prediction produces representations that can be fine-tuned for diverse downstream tasks. The key insight of the field: pretraining on massive unlabeled text captures broadly transferable linguistic knowledge. See [Attention Mechanisms](/ai-engineering/attention-mechanisms.md) for the Transformer architecture and [Transformer](/ai-engineering/transformer.md) for the architecture details.

## The problem with one-hot encodings

The naive representation of words is one-hot encoding: a vector of size |V| (vocabulary) with a single 1. Problems: extremely high-dimensional, sparse, and no notion of semantic similarity ("cat" is as different from "dog" as it is from "airplane" in one-hot space). "One-hot vectors are a bad choice." [^src1]

**Word embeddings** map each word to a dense low-dimensional vector (typically 50–300 dimensions) where semantically similar words cluster together.

## Word2vec: self-supervised word embeddings

Word2vec (Mikolov et al. 2013) learns word embeddings by predicting word co-occurrence from large text corpora — **self-supervised** because the training signal comes from the data itself, not human labels [^src1].

Two model variants:

### Skip-gram
Given a center word, predict surrounding context words (within a window of ±k):

```
P(context word | center word) = softmax(u_o^T v_c)
```

Where v_c is the center word's embedding vector and u_o is the context word's vector. The model maximizes the log-likelihood of observing the actual context words. With vocabulary size |V|, the softmax denominator sums over all |V| words — expensive for large vocabularies.

### CBOW (Continuous Bag of Words)
Given surrounding context words, predict the center word. Averages context word embeddings:

```
P(center | context) = softmax(u_c^T * mean(v_{context}))
```

CBOW is faster; skip-gram produces better representations for rare words.

### Approximate training
Computing exact softmax over large vocabularies (50K–300K words) is expensive. Approximations [^src1]:
- **Negative sampling**: for each (center, context) pair, maximize P(context|center) while minimizing P(noise_word|center) for k randomly sampled "negative" words (k=5–20 typical)
- **Hierarchical softmax**: organize vocabulary in a binary tree; P(word) is a product of binary decisions along the path from root to leaf

### What word2vec learns
Emergent linear structure in embedding space: **word analogies** work via vector arithmetic. The famous example: **king − man + woman ≈ queen**. This structure emerges entirely from co-occurrence statistics, not hand-crafted linguistic knowledge.

## GloVe: global co-occurrence statistics

Word2vec uses local context windows. **GloVe** (Pennington et al. 2014) uses the full corpus co-occurrence matrix X, where X_{ij} counts how often word j appears in word i's context across all documents [^src1].

GloVe's key insight: the **ratio** of co-occurrence probabilities P(k|i) / P(k|j) encodes meaning. If k="ice", P(k|"solid") / P(k|"gas") is large. This ratio is better captured than raw probabilities.

GloVe minimizes a weighted least-squares objective over the co-occurrence matrix:

```
L = sum_{i,j} f(X_{ij}) (w_i^T w_j + b_i + b_j - log X_{ij})^2
```

Where f is a weighting function that downweights very frequent pairs. GloVe and word2vec produce similar-quality embeddings; choice is empirical.

## Subword embeddings: fastText and BPE

Word2vec and GloVe produce one vector per word. Problems:
- Out-of-vocabulary (OOV) words get no representation
- Morphologically related words ("run", "running", "runner") get unrelated vectors

**fastText** (Bojanowski et al. 2017) [^src1] represents each word as the sum of its character n-gram embeddings. "running" = {r, u, n, n, i, n, g} + {ru, un, nn, ni, in, ng} + {run, unn, ...} + the word itself. OOV words can be represented via their character n-grams.

**Byte Pair Encoding (BPE)**: data-compression-inspired subword tokenization used by GPT-2, RoBERTa [^src1]. Start with character-level vocabulary; iteratively merge the most frequent pair of adjacent tokens. After k merges, the vocabulary contains common words as single tokens and rare words split into frequent subwords. Modern LLMs use BPE or similar (SentencePiece).

## From static to contextualized representations

Word2vec/GloVe limitations: each word has one embedding regardless of context. "Bank" (financial) and "bank" (river) get the same vector.

**ELMo** (Peters et al. 2018) produces contextualized embeddings by passing each sentence through a bidirectional LSTM language model; the embedding for each word is a weighted combination of all hidden states. The same word gets different representations in different contexts.

## BERT: bidirectional pretraining at scale

**BERT** (Devlin et al. 2018, "Bidirectional Encoder Representations from Transformers") combines the context-sensitivity of ELMo with the power of the Transformer architecture [^src1].

### Architecture
BERT uses a standard Transformer encoder (multi-head self-attention, no causal masking). Each token's representation is informed by all other tokens in both directions simultaneously — hence "bidirectional."

### Input representation
Each input is a sequence of special tokens [^src1]:

```
[CLS] token1 token2 ... [SEP] token_A ... [SEP]
```

**Three embedding types summed**: (1) token embeddings, (2) segment embeddings (which sentence), (3) positional embeddings. The [CLS] token's final representation is used for classification tasks; [SEP] separates sentences.

### Pretraining tasks

**Masked Language Modeling (MLM)**: randomly mask 15% of input tokens; predict the original tokens at masked positions. Unlike left-to-right language models (GPT), MLM conditions on both left and right context. The 15% split: 80% replaced with [MASK], 10% replaced with random token, 10% kept unchanged (so model must always predict the original token, not just detect [MASK]) [^src1].

**Next Sentence Prediction (NSP)**: given two sentences, predict whether sentence B actually follows sentence A in the corpus (50% yes, 50% random). Designed to help tasks requiring sentence-pair understanding (NLI, QA). (Later work — RoBERTa — found NSP unhelpful and removed it.)

### Fine-tuning

BERT is pretrained on a large corpus (Wikipedia + Books), then fine-tuned end-to-end on downstream tasks by adding a task-specific head [^src1]:

| Task type | Head added | Example |
|---|---|---|
| Single text classification | Linear on [CLS] embedding | Sentiment analysis |
| Text pair classification | Linear on [CLS] from pair | Natural language inference |
| Text tagging (NER) | Linear on each token embedding | Named entity recognition |
| Question answering (span) | Start/end linear heads over tokens | SQuAD extractive QA |

"Fine-tuning BERT is relatively inexpensive compared with pretraining BERT from scratch." [^src1] Fine-tuning on a GPU for hours, not pretraining for weeks.

## GPT: unidirectional pretraining

**GPT** (Radford et al. 2018) uses a Transformer **decoder** with causal masking — each token can only attend to preceding tokens. Pretraining is standard left-to-right language modeling.

Key difference from BERT: unidirectional vs. bidirectional context. Consequences:
- BERT: better representations for understanding tasks (classification, NER, QA)
- GPT: natural for generation tasks (language modeling, text completion, dialogue)

GPT-2 (2019), GPT-3 (2020), GPT-4 (2023) scaled the GPT approach dramatically. BERT remains the standard for fine-tuning on discriminative tasks; the GPT line dominated large-scale generative capabilities.

## Downstream NLP applications

D2L Chapter 16 demonstrates fine-tuning pretrained representations for [^src1]:

**Sentiment analysis**: classify text as positive/negative/neutral. Feed to BERT, pool [CLS] representation, linear classifier. Alternatively, use pretrained RNNs with GloVe embeddings, or textCNN (1D convolutions over word embeddings).

**Natural Language Inference (NLI)**: given premise and hypothesis, classify as entailment/contradiction/neutral. BERT with paired input ([CLS] premise [SEP] hypothesis [SEP]) + linear classifier on [CLS].

**Question answering (extractive)**: given passage and question, find the span of text in the passage that answers the question. BERT produces start and end logits over passage tokens; argmax gives the answer span.

## Summary of the progression

| Method | Representation | Training signal | Context |
|---|---|---|---|
| One-hot | Sparse, arbitrary | — | None |
| word2vec / GloVe | Dense, static | Co-occurrence | Fixed window |
| fastText | Dense, subword | Co-occurrence | Fixed window |
| ELMo | Dense, contextualized | Bidirectional LM | Whole sentence |
| BERT | Dense, contextualized | MLM + NSP | Whole sentence (bidirectional) |
| GPT | Dense, contextualized | LM (causal) | Left context |
| GPT-3+, Claude | Dense, contextualized | LM at scale | Left context + RLHF |

## See also

- [Attention Mechanisms](/ai-engineering/attention-mechanisms.md) — the Transformer self-attention that BERT uses
- [Transformer](/ai-engineering/transformer.md) — the full Transformer architecture
- [RNNs](/ai-engineering/recurrent-neural-networks.md) — RNN-based text classification and language models
- [Embeddings](/ai-engineering/embeddings.md) — word embeddings as input vs. sentence embeddings for retrieval
- [LLM](/ai-engineering/llm.md) — GPT-scale generative language models; RLHF fine-tuning
- [Dive into Deep Learning](/ai-engineering/sources/dive-into-deep-learning.md) — source textbook (Chapters 15–16)

---

[^src1]: [D2L Part 22 — NLP Pretraining context (Chapters 15–16 coverage)](../../raw/_inbox/pdf-zhang-lipton-li-smola-dive-into-deep-learning-cc-by-sa-4-0-part-22.md)

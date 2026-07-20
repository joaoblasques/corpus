---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/pdf/pdf-speech-and-language-processing-3rd-edition-draft-part-01.md
    channel: pdf
    ingested_at: 2026-07-20
  - path: raw/pdf/pdf-speech-and-language-processing-3rd-edition-draft-part-02.md
    channel: pdf
    ingested_at: 2026-07-20
  - path: raw/pdf/pdf-speech-and-language-processing-3rd-edition-draft-part-03.md
    channel: pdf
    ingested_at: 2026-07-20
  - path: raw/pdf/pdf-speech-and-language-processing-3rd-edition-draft-part-04.md
    channel: pdf
    ingested_at: 2026-07-20
  - path: raw/pdf/pdf-speech-and-language-processing-3rd-edition-draft-part-05.md
    channel: pdf
    ingested_at: 2026-07-20
  - path: raw/pdf/pdf-speech-and-language-processing-3rd-edition-draft-part-06.md
    channel: pdf
    ingested_at: 2026-07-20
  - path: raw/pdf/pdf-speech-and-language-processing-3rd-edition-draft-part-07.md
    channel: pdf
    ingested_at: 2026-07-20
  - path: raw/pdf/pdf-speech-and-language-processing-3rd-edition-draft-part-08.md
    channel: pdf
    ingested_at: 2026-07-20
  - path: raw/pdf/pdf-speech-and-language-processing-3rd-edition-draft-part-09.md
    channel: pdf
    ingested_at: 2026-07-20
  - path: raw/pdf/pdf-speech-and-language-processing-3rd-edition-draft-part-10.md
    channel: pdf
    ingested_at: 2026-07-20
  - path: raw/pdf/pdf-speech-and-language-processing-3rd-edition-draft-part-11.md
    channel: pdf
    ingested_at: 2026-07-20
  - path: raw/pdf/pdf-speech-and-language-processing-3rd-edition-draft-part-12.md
    channel: pdf
    ingested_at: 2026-07-20
  - path: raw/pdf/pdf-speech-and-language-processing-3rd-edition-draft-part-13.md
    channel: pdf
    ingested_at: 2026-07-20
  - path: raw/pdf/pdf-speech-and-language-processing-3rd-edition-draft-part-14.md
    channel: pdf
    ingested_at: 2026-07-20
  - path: raw/pdf/pdf-speech-and-language-processing-3rd-edition-draft-part-15.md
    channel: pdf
    ingested_at: 2026-07-20
  - path: raw/pdf/pdf-speech-and-language-processing-3rd-edition-draft-part-16.md
    channel: pdf
    ingested_at: 2026-07-20
aliases:
  - SLP
  - Jurafsky Martin
  - Speech and Language Processing
  - SLP3
tags:
  - corpus/ai-engineering
  - source
created: 2026-07-20
updated: 2026-07-20
---

# Speech and Language Processing, 3rd Edition Draft (Jurafsky & Martin, 2026)

TL;DR: The definitive NLP and computational linguistics textbook by Daniel Jurafsky (Stanford) and James H. Martin (University of Colorado). Third edition draft (January 6, 2026; 626 pages); covers LLMs, transformers, NLP pipelines, speech recognition, and linguistic structure annotation. Freely available online. See [Daniel Jurafsky](/ai-engineering/daniel-jurafsky.md) and [James H. Martin](/ai-engineering/james-martin.md).

## Structure (2 volumes, 25 chapters)

**Volume I — Large Language Models (Chapters 1-16)**

| Chapter | Topic | PDF Parts (est.) |
|---|---|---|
| 1 | Introduction — ELIZA, tokenization overview | 1 |
| 2 | Words and Tokens — morphemes, Unicode, BPE subword tokenization, corpora, regex, minimum edit distance | 1-2 |
| 3 | N-gram Language Models — n-grams, perplexity, smoothing (add-1, add-k, Kneser-Ney, interpolation, backoff) | 3-5 |
| 4 | Logistic Regression — sigmoid, cross-entropy loss, gradient descent, multi-class softmax, precision/recall/F, cross-validation | 5-7 |
| 5 | Embeddings — lexical semantics, word2vec (skip-gram/CBOW), cosine similarity, TF-IDF, bias in embeddings | 7-8 |
| 6 | Neural Networks — feedforward nets, backprop, XOR problem, NLP classification | 9-10 |
| 7 | Large Language Models — conditional generation, prompting, sampling (top-k/top-p/temperature), training, evaluation, safety/ethics | 10-11 |
| 8 | Transformers — attention (QKV), transformer blocks, residual stream, positional encoding, multi-head attention, training | 12-13 |
| 9 | Masked Language Models — bidirectional transformers, BERT (masked LM + NSP), contextual embeddings, fine-tuning | 13-14 |
| 10 | Post-training — instruction tuning, RLHF, DPO, preference-based learning, test-time compute | 14-15 |
| 11 | Retrieval-based Models — TF-IDF, BM25, inverted index, dense vectors, RAG, question answering | 15-16 |
| 12 | Machine Translation — encoder-decoder, beam search, BLEU, low-resource MT, bias issues | 16 |
| 13 | RNNs and LSTMs — RNN language models, BPTT, stacked/bidirectional RNNs, LSTM, encoder-decoder with attention | — |
| 14 | Phonetics and Speech Feature Extraction — phonemes, articulatory phonetics, prosody, log-mel spectrum, MFCCs | — |
| 15 | Automatic Speech Recognition — CTC, encoder-decoder ASR, HuBERT, word error rate | — |
| 16 | Text-to-Speech — codec tokens, VALL-E, TTS evaluation, spoken language models | — |

**Volume II — Annotating Linguistic Structure (Chapters 17-25)**

| Chapter | Topic |
|---|---|
| 17 | Sequence Labeling for POS and NER — HMM tagging, CRF, Viterbi |
| 18 | Context-Free Grammars and Constituency Parsing — CFG, CKY dynamic programming, span-based neural parsing |
| 19 | Dependency Parsing — dependency relations, transition-based (arc-eager), graph-based |
| 20 | Information Extraction — relation extraction, event extraction, temporal analysis (TimeBank) |
| 21 | Semantic Role Labeling — PropBank, FrameNet, selectional restrictions |
| 22 | Lexicons for Sentiment, Affect, and Connotation — emotion models, sentiment lexicons (WordNet, NRC), connotation frames |
| 23 | Coreference Resolution and Entity Linking — mention detection, mention-ranking, Winograd Schema, gender bias |
| 24 | Discourse Coherence — RST, centering theory, local/global coherence |
| 25 | Conversation and its Structure — properties of human conversation, dialog acts |

## Key ideas

- **Tokenization and BPE** (Chapter 2): ELIZA's pattern matching was the precursor to modern tokenization; byte-pair encoding (BPE) iteratively merges the most frequent adjacent byte pairs — enables subword tokenization handling OOV words without a fixed vocabulary. [^slp-p01]
- **N-gram smoothing** (Chapter 3): add-one smoothing drastically reallocates mass — bigram `want to` went from P=0.66 to 0.26 (discount d=0.39), `Chinese food` discount d=0.10; Kneser-Ney is the standard for production n-gram LMs. [^slp-p05]
- **Cosine similarity for embeddings** (Chapter 5): raw dot product biases toward frequent (longer) word vectors; normalizing by vector L2-norms gives the cosine — a frequency-invariant semantic similarity measure used throughout NLP. [^slp-p08]
- **Transformer architecture** (Chapter 8): each token is first embedded via matrix E then passed through N transformer blocks; the residual stream adds attention and FFN contributions at each layer; positional encoding is added to the embedding (not a separate input). [^slp-p12]
- **Inverted index** (Chapter 11): consists of a dictionary (each term with document frequency + pointer) and postings lists (document IDs + term counts); enables efficient TF-IDF ranking; stop words are less commonly used now since IDF naturally downweights function words. [^slp-p16]
- **Coverage note**: parts 1-16 of 38 ingested; remaining parts cover Chapters 12-25 (MT through Conversation).

## Relationship to other corpus sources

- Transformer (Chapter 8) and embeddings (Chapter 5) complement [Attention Mechanisms](/ai-engineering/attention-mechanisms.md) and [NLP Deep Learning](/ai-engineering/nlp-deep-learning.md).
- RAG (Chapter 11) and retrieval complement [RAG](/ai-engineering/rag.md).
- LLM training and post-training (Chapters 7, 10) ground [LLM](/ai-engineering/llm.md) and [LLM Evals](/ai-engineering/llm-evals.md).
- The probabilistic framing of n-grams and logistic regression cross-references [Probabilistic Machine Learning: An Introduction](/ai-engineering/sources/probabilistic-machine-learning-intro.md) (Murphy, Chapters 5-11).
- Speech chapters (Chapters 14-16) are a unique source in the corpus: no other ingested source covers phonetics, ASR, or TTS at this depth.

## Related corpus pages

- [Daniel Jurafsky](/ai-engineering/daniel-jurafsky.md)
- [James H. Martin](/ai-engineering/james-martin.md)
- [Attention Mechanisms](/ai-engineering/attention-mechanisms.md)
- [NLP Deep Learning](/ai-engineering/nlp-deep-learning.md)
- [LLM](/ai-engineering/llm.md)
- [RAG](/ai-engineering/rag.md)
- [Recurrent Neural Networks](/ai-engineering/recurrent-neural-networks.md)
- [Probabilistic Machine Learning: An Introduction](/ai-engineering/sources/probabilistic-machine-learning-intro.md)

[^slp-p01]: raw/pdf/pdf-speech-and-language-processing-3rd-edition-draft-part-01.md — Table of contents, Chapter 1 (Introduction), Chapter 2 start (Words and Tokens; ELIZA; tokenization)
[^slp-p05]: raw/pdf/pdf-speech-and-language-processing-3rd-edition-draft-part-05.md — Chapter 3: n-gram smoothing, add-one/add-k, discount d
[^slp-p08]: raw/pdf/pdf-speech-and-language-processing-3rd-edition-draft-part-08.md — Chapter 5: cosine similarity, dot product, vector length normalization
[^slp-p12]: raw/pdf/pdf-speech-and-language-processing-3rd-edition-draft-part-12.md — Chapter 8: transformer architecture, residual stream, embedding matrix E, positional encoding
[^slp-p16]: raw/pdf/pdf-speech-and-language-processing-3rd-edition-draft-part-16.md — Chapter 11: inverted index, postings, stop words, BM25/TF-IDF

---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-zhang-lipton-li-smola-dive-into-deep-learning-cc-by-sa-4-0-part-22.md
    channel: pdf
    ingested_at: 2026-07-10
aliases:
  - attention mechanism
  - attention
  - self-attention
  - multi-head attention
  - Bahdanau attention
  - scaled dot-product attention
  - additive attention
  - positional encoding
  - query key value
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-10
updated: 2026-07-10
---

# Attention Mechanisms

**TL;DR**: Attention is the mechanism that allows a model to selectively focus on relevant parts of the input when producing each output. Originally proposed for RNN sequence-to-sequence models (Bahdanau 2014) to fix the fixed-context-vector bottleneck; generalized into the Query-Key-Value abstraction; and ultimately the basis for the Transformer architecture (Vaswani et al. 2017). Self-attention — where queries, keys, and values all come from the same sequence — enables parallel sequence processing. See [Transformer](/ai-engineering/transformer.md) for the full Transformer architecture; see [RNNs](/ai-engineering/recurrent-neural-networks.md) for the encoder-decoder context in which Bahdanau attention arose.

## From Nadaraya-Watson to attention

Attention can be understood as a form of **kernel regression** [^src1]. In Nadaraya-Watson regression, the predicted output at a query point x is a weighted average of training labels y_i, where weights depend on the similarity between x and training inputs x_i:

```
f(x) = sum_i K(x, x_i) / [sum_j K(x, x_j)] * y_i
```

This is exactly the attention formula with K as the "attention scoring function", x as the query, {x_i} as keys, and {y_i} as values. The insight: attention generalizes kernel regression to learned, parametric similarity functions.

## Query-Key-Value abstraction

The three-tensor abstraction unifying all attention variants [^src1]:

```
Attention(Q, K, V) = softmax(score(Q, K)) * V
```

- **Query** (Q): "what am I looking for?" — comes from the current position/token
- **Key** (K): "what do I match with?" — comes from candidate positions
- **Value** (V): "what information to aggregate?" — comes from same positions as keys

The scoring function computes compatibility between each query and all keys; softmax normalizes these into a probability distribution (attention weights); the weighted sum of values is the output.

## Attention scoring functions

### Additive attention (Bahdanau attention)

When queries and keys have different dimensions, or for asymmetric attention [^src1]:

```
score(q, k) = w_v^T tanh(W_q q + W_k k)
```

Where W_q, W_k, w_v are learned parameters. Equivalent to concatenating q and k, passing through a one-hidden-layer MLP with tanh, and projecting to a scalar. More flexible than dot product but more expensive (extra parameters, no exploitable structure).

### Scaled dot-product attention

For queries and keys of dimension d [^src1]:

```
score(q, k) = q^T k / sqrt(d)
```

The 1/sqrt(d) scaling prevents the dot products from growing large in magnitude (which would push softmax into saturation). For minibatches with n queries and m key-value pairs:

```
Attention(Q, K, V) = softmax(Q K^T / sqrt(d)) V
     Q: n×d, K: m×d, V: m×v → output: n×v
```

This is the mainstay of modern Transformer architectures. The batch matrix multiplication `torch.bmm(Q, K.transpose(1,2))` computes all query-key scores simultaneously [^src1].

**Masked softmax**: for variable-length sequences, pad to uniform length and mask out padding positions before softmax. Valid-length masking sets scores for padding positions to -inf so they get ~0 weight after softmax [^src1].

## Bahdanau attention mechanism

Bahdanau et al. (2014) extended the RNN encoder-decoder to use attention, fixing the fixed-context-vector bottleneck [^src1]:

"Instead of keeping the state, i.e., the context variable c summarizing the source sentence, as fixed, we dynamically update it, as a function of both the original text (encoder hidden states h_t) and the text that was already generated (decoder hidden states s_{t'-1})." [^src1]

At decoding step t', the context vector c_{t'} is computed by attending over all encoder hidden states:

```
alpha(s_{t'-1}, h_t) = exp(score(s_{t'-1}, h_t)) / sum_tau exp(score(s_{t'-1}, h_tau))
c_{t'} = sum_t alpha(s_{t'-1}, h_t) * h_t
```

Where score is additive attention. This allows the decoder to "attend to" different parts of the input at each decoding step. "The Bahdanau attention mechanism has arguably turned into one of the most influential ideas of the past decade in deep learning, giving rise to Transformers." [^src1]

## Multi-head attention

A single attention function gives one "view" of token relationships. Multi-head attention runs h attention functions in parallel [^src1]:

```
MultiHead(Q, K, V) = Concat(head_1, ..., head_h) W^O
head_i = Attention(Q W_i^Q, K W_i^K, V W_i^V)
```

Each head projects queries, keys, and values to a smaller dimension (d_model/h), computes attention in that space, and the results are concatenated and projected back. Different heads learn to attend to different relationship types — syntax, coreference, positional patterns, etc.

Typical configuration: 8 heads in the original Transformer, 32–96 heads in large LLMs; d_model/h = 64 is common.

## Self-attention

When queries, keys, and values all come from the same sequence, it is **self-attention** [^src1]. Each position attends to all other positions (or all previous positions for causal language models). This enables:
- Long-range dependency modeling (no sequential bottleneck)
- Parallel computation (all positions processed simultaneously)
- Direct gradient paths between any two positions

**Comparison to CNNs and RNNs** [^src1]:
- CNNs: O(k) path length for k-kernel, O(1) parallelism, O(k * n) ops
- RNNs: O(n) path length (sequential), O(n) time steps (no training parallelism)
- Self-attention: O(1) path length (direct connection), full parallelism, O(n^2 * d) ops

The n^2 cost of self-attention (each of n positions attends to all n positions) is the main computational bottleneck for long sequences.

## Positional encoding

Self-attention is **permutation invariant** — the same computation regardless of token order. Positional encoding injects order information by adding a position-dependent vector to each token embedding [^src1].

**Sinusoidal positional encoding** (Vaswani et al. 2017):
```
PE(pos, 2i)   = sin(pos / 10000^{2i/d_model})
PE(pos, 2i+1) = cos(pos / 10000^{2i/d_model})
```

Different dimensions use sine/cosine waves at different frequencies, encoding position in a multi-scale way. The key property: the relative position between two tokens (pos and pos+k) is a linear function of PE(pos), enabling the model to generalize to unseen positions.

**Learnable positional embeddings**: directly learn a vector for each position — simpler but does not generalize beyond the maximum training length. Used in BERT.

**RoPE (Rotary Position Embeddings)**: rotate Query and Key vectors by an angle proportional to position before computing dot products. Encodes relative positions implicitly; used in LLaMA, Mistral, and most modern LLMs. See [Transformer](/ai-engineering/transformer.md).

## The Transformer architecture (D2L Chapter 11)

D2L presents the Transformer (Vaswani et al. 2017) as the culmination of the attention chapter [^src1]:

**Encoder**: stack of N=6 identical layers, each containing:
1. Multi-head self-attention (all positions attend to all positions)
2. Positionwise feed-forward network (MLP applied to each position independently)
3. Residual connections + layer normalization around each sub-layer

**Decoder**: stack of N=6 layers, each containing:
1. Masked multi-head self-attention (each position attends only to earlier positions)
2. Cross-attention: queries from decoder, keys/values from encoder output
3. Positionwise FFN + residuals + layer norm

**Positionwise FFN**: `FFN(x) = max(0, x W_1 + b_1) W_2 + b_2` — a two-layer MLP with ReLU, applied identically to each position.

**Vision Transformer (ViT)**: applies Transformer to images by splitting into fixed-size patches, embedding each patch as a token, and applying the standard Transformer encoder [^src1].

**Large-scale pretraining variants**:
- Encoder-only (BERT): bidirectional self-attention, masked language modeling pretraining
- Decoder-only (GPT): causal self-attention, next-token prediction pretraining
- Encoder-decoder (T5, BART): seq2seq pretraining

"Scalability is the main advantage that has allowed Transformers to become the dominant architectures for large models over the past decade." [^src1]

## See also

- [Transformer](/ai-engineering/transformer.md) — full Transformer architecture; Q/K/V, multi-head, FFN, residuals, KV cache, RoPE
- [RNNs](/ai-engineering/recurrent-neural-networks.md) — encoder-decoder context; Bahdanau attention as the bridge
- [NLP Deep Learning](/ai-engineering/nlp-deep-learning.md) — BERT/GPT use Transformer + pretraining
- [MLP](/ai-engineering/mlp.md) — the positionwise FFN in Transformers is an MLP
- [Dive into Deep Learning](/ai-engineering/sources/dive-into-deep-learning.md) — source textbook (Chapter 11)

---

[^src1]: [D2L Part 22 — Attention Scoring Functions, Bahdanau, Multi-Head](../../raw/_inbox/pdf-zhang-lipton-li-smola-dive-into-deep-learning-cc-by-sa-4-0-part-22.md)

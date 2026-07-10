---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-zhang-lipton-li-smola-dive-into-deep-learning-cc-by-sa-4-0-part-11.md
    channel: pdf
    ingested_at: 2026-07-10
aliases:
  - recurrent neural network
  - RNN
  - LSTM
  - GRU
  - sequence modeling
  - BPTT
  - backpropagation through time
  - encoder-decoder
  - seq2seq
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-10
updated: 2026-07-10
---

# Recurrent Neural Networks (RNNs)

**TL;DR**: Neural network architecture for sequential data — text, time series, audio. RNNs maintain a hidden state that summarizes sequence history, updated at each step. The key training challenge is **backpropagation through time (BPTT)**, which amplifies or attenuates gradients exponentially over long sequences. LSTMs and GRUs use gating mechanisms to control gradient flow. For sequence-to-sequence tasks (translation, summarization), encoder-decoder architectures pass sequence context from encoder to decoder. RNNs have largely been superseded by [attention mechanisms](/ai-engineering/attention-mechanisms.md) and Transformers for NLP, but remain useful for time series and online inference. See also [Attention Mechanisms](/ai-engineering/attention-mechanisms.md).

## Sequence modeling: why MLPs fail

MLPs take fixed-size inputs and produce fixed-size outputs. Sequences have variable length and exhibit temporal dependencies — "the price of a stock today depends on yesterday's price, and the price last week, not just on today's news." An MLP would need to decide upfront how many past steps to include [^src1].

**Autoregressive models** decompose the joint probability of a sequence: p(x_1, ..., x_T) = product_t p(x_t | x_1, ..., x_{t-1}). The RNN parameterizes the conditional efficiently via a latent hidden state.

**Language models** assign probability to sequences of tokens. RNN-based character-level and word-level language models were the standard NLP approach before Transformers.

## The RNN hidden state

An RNN processes a sequence one step at a time, maintaining a hidden state h_t that summarizes information up to step t [^src1]:

```
h_t = phi(W_hh * h_{t-1} + W_xh * x_t + b_h)    (state update)
o_t = W_ho * h_t + b_o                              (output)
```

Where phi is an activation function (tanh traditionally), W_hh are the recurrent weights, W_xh are input weights, and W_ho are output weights. The same weights apply at every time step — weight sharing across time.

The hidden state is the "memory" of the network. At step t, h_t contains a compressed representation of x_1, ..., x_t.

**Gradient clipping**: because gradient magnitudes can explode during BPTT, practitioners clip the gradient norm to a maximum threshold before each update: `if ||g|| > threshold: g = g * threshold / ||g||` [^src1].

## Backpropagation through time (BPTT)

Training an RNN requires differentiating through the unrolled computation graph — T copies of the same transition function. The gradient of the loss at step T with respect to early parameters passes through T matrix multiplications of W_hh [^src1]:

```
dL/dW_hh contains a product: W_hh^(T-1) * W_hh^(T-2) * ... * W_hh^(l)
```

If the eigenvalues of W_hh are < 1: gradient **vanishes** exponentially — the network cannot learn long-range dependencies.
If eigenvalues are > 1: gradient **explodes** — training diverges.

**Truncated BPTT**: limit backprop to k steps, detaching the computational graph. Reduces memory and computation, but loses long-range gradients.

## Gated RNNs: LSTM and GRU

The vanishing gradient problem for RNNs motivated gated architectures that learn to selectively retain or discard information.

### LSTM (Long Short-Term Memory, Hochreiter and Schmidhuber, 1997)

LSTMs introduce a **cell state** C_t alongside the hidden state h_t. The cell state provides a direct gradient path through time (the "constant error carousel"). Three gates control information flow [^src1]:

```
# Input gate: controls how much new input to write to cell
i_t = sigma(W_xi * x_t + W_hi * h_{t-1} + b_i)

# Forget gate: controls how much of old cell state to retain
f_t = sigma(W_xf * x_t + W_hf * h_{t-1} + b_f)

# Output gate: controls what to expose from cell state
o_t = sigma(W_xo * x_t + W_ho * h_{t-1} + b_o)

# Candidate cell update
C_tilde_t = tanh(W_xc * x_t + W_hc * h_{t-1} + b_c)

# Cell state update (the key: additive update, not multiplicative)
C_t = f_t ⊙ C_{t-1} + i_t ⊙ C_tilde_t

# Hidden state (what gets passed forward and to output)
h_t = o_t ⊙ tanh(C_t)
```

The additive cell state update (f * C_{t-1} + i * C_tilde) avoids the multiplicative vanishing gradient. The forget gate lets the network learn what to remember long-term.

### GRU (Gated Recurrent Unit, Cho et al., 2014)

Simpler than LSTM with fewer parameters, two gates [^src1]:

```
# Reset gate: controls how much of h_{t-1} to use in computing candidate
r_t = sigma(W_xr * x_t + W_hr * h_{t-1} + b_r)

# Update gate: interpolates between old and new hidden state
z_t = sigma(W_xz * x_t + W_hz * h_{t-1} + b_z)

# Candidate hidden state (using reset gate)
h_tilde_t = tanh(W_xh * x_t + W_hh * (r_t ⊙ h_{t-1}) + b_h)

# Hidden state update (convex combination via update gate)
h_t = z_t ⊙ h_{t-1} + (1 - z_t) ⊙ h_tilde_t
```

The **reset gate** r_t allows the network to ignore irrelevant past state when computing new candidate. The **update gate** z_t acts like a forget+input gate combined.

GRU often matches LSTM performance with fewer parameters and faster training. Choice is empirical.

### Deep RNNs

Stack multiple RNN layers where the output of layer l becomes the input to layer l+1. Captures hierarchical temporal representations. Typically 2–4 layers; deeper is harder to train.

### Bidirectional RNNs

Two RNNs: one processes the sequence forward, one backward. Outputs are concatenated at each step. Cannot be used for autoregressive generation (future is unknown), but useful when full sequence is available (e.g., BERT-style encoding).

## Sequence-to-sequence (encoder-decoder)

For tasks with variable-length input and output (machine translation, summarization), the **encoder-decoder** architecture [^src1]:

1. **Encoder**: an RNN processes the input sequence; its final hidden state is the **context vector** c
2. **Decoder**: a separate RNN generates the output sequence, conditioned on c; at each step, decoder state s_t = f(s_{t-1}, y_{t-1}, c)

The bottleneck: the entire source sequence must be compressed into a single fixed-size context vector. This fails for long sequences — the motivation for the [Bahdanau attention mechanism](/ai-engineering/attention-mechanisms.md).

**Teacher forcing**: during training, feed ground-truth previous tokens as decoder input (not the model's own predictions). Faster convergence but can create a mismatch at inference time ("exposure bias").

## Beam search

Greedy decoding (always pick the highest-probability next token) often produces suboptimal sequences. **Beam search** maintains k candidate sequences ("beams") at each step, pruning to the top-k by cumulative log-probability. Beam width k=5–10 is typical. Trade-off: higher k improves quality but increases compute [^src1].

## Relationship to Transformers

RNNs process sequences sequentially — no parallelism during training. Transformers replace the recurrent computation with attention, which can process all positions simultaneously. Key advantages of Transformers over RNNs:
- Full parallelism during training (GPUs scale much better)
- Explicit long-range attention (no gradient vanishing for distant dependencies)
- Better scaling with data and parameters

RNNs remain useful for:
- Online/streaming inference (process one token, no attention over full context)
- Long sequences where O(n^2) attention cost is prohibitive
- Time-series with very long dependencies that benefit from the inductive bias of sequential processing

## See also

- [Attention Mechanisms](/ai-engineering/attention-mechanisms.md) — Bahdanau attention extends encoder-decoder; Transformer replaces RNNs entirely
- [MLP](/ai-engineering/mlp.md) — feedforward baseline; RNNs add recurrence
- [NLP Deep Learning](/ai-engineering/nlp-deep-learning.md) — word embeddings and pretraining used with RNNs
- [Transformer](/ai-engineering/transformer.md) — the dominant architecture that replaced RNNs for NLP
- [Dive into Deep Learning](/ai-engineering/sources/dive-into-deep-learning.md) — source textbook (Chapters 9–10)

---

[^src1]: [D2L Part 11 — Backpropagation, RNN internals (Chapters 9–10 coverage)](../../raw/_inbox/pdf-zhang-lipton-li-smola-dive-into-deep-learning-cc-by-sa-4-0-part-11.md)

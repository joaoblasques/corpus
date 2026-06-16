---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: 03_Resources/Study Notes/AI - How Large Language Models Work.md
    channel: notes
    ingested_at: 2026-05-21
  - path: raw/web/how-llms-actually-work.md
    channel: web
    ingested_at: 2026-06-16
aliases:
  - Transformer
  - transformer architecture
  - attention mechanism
  - self-attention
tags:
  - corpus/ai-engineering
  - concept
created: 2026-05-21
updated: 2026-06-16
---

# Transformer

**TL;DR**: The neural network architecture (Google, 2017) underlying all modern LLMs. Enables parallel processing of entire sequences via attention — each token attends to every other token to update its meaning in context [^src1]. Most modern transformer-based LLMs share the same skeleton; differences come from training data, scale/configuration choices, and post-training [^src2]. The pipeline: tokenize → embed → add positional info → stacked transformer layers (multi-head attention + feed-forward, glued by residual streams + normalization) → next-token prediction [^src2].

## Tokenization

Models don't read text — they read integer IDs. A **tokenizer** converts a string into a sequence of integers, each pointing to an entry in a fixed **vocabulary** (typically tens of thousands to a few hundred thousand entries) [^src2]. Tokens are usually **subword pieces**, not whole words: "tokenization" might split into ["token", "ization"] [^src2]. Subword sits between whole-word vocabularies (too big, poor generalization to new words) and character-level (too small, forces learning simple patterns from scratch) [^src2].

- **BPE / SentencePiece**: GPT models use Byte Pair Encoding variants; SentencePiece is common in LLaMA-style models [^src2].
- **The "strawberry" R-count artifact**: asking an LLM how many R's are in "strawberry" used to fail — not a counting failure but a consequence of the model operating on token IDs, not letters [^src2].

## Embeddings

A token ID is just a row index with no inherent meaning. The **embedding matrix** is a lookup table with one row per vocabulary entry; each row is a long vector whose length is the model's **hidden size** (often 4,096 numbers per token in 7B-class models) [^src2]. The looked-up vector is the token's embedding — its learned representation of "meaning" [^src2].

Semantically similar tokens end up with similar vectors ("king" close to "queen", "Paris" close to "France"), emergent from training, not hard-coded [^src2]. Embedding arithmetic sometimes works — the famous example: **king − man + woman ≈ queen** [^src2].

## Positional encoding

Plain self-attention has no built-in word-order representation; the embedding for "dog" is identical at position 1 or position 5 [^src2]. **Positional encoding** injects each token's position into the math [^src2].

- **Additive sinusoidal (Vaswani et al. 2017)**: each position gets its own pattern of sine/cosine waves at different frequencies, added to the embedding before any processing. Chosen partly to extrapolate beyond training sequence lengths [^src2]. Two scaling problems: the embedding must carry both meaning *and* position in the same numbers, and learned absolute positions don't generalize to unseen lengths [^src2].
- **RoPE (Rotary Position Embeddings, Su et al. 2021)** — used in LLaMA, Mistral, Gemma, Qwen, and most open-weight families. Instead of *adding* position info, RoPE **rotates the Query and Key vectors** by an angle that depends on position; what matters during attention is the *difference* between two tokens' rotations, encoding relative distance [^src2]. Advantages: encodes relative position naturally, generalizes better to longer contexts, and adds no new parameters [^src2].
- **"Lost in the middle" (Liu et al. 2023)**: even with good positional encoding, models use information at the **start and end** of long prompts more reliably than information buried in the middle — why "put important context first" / "repeat key info at the end" prompt-engineering tips help [^src2]. See [[ai-engineering/context-window-management|Context Window Management]].

## Attention

The mechanism that named the architecture. Inside every layer, attention lets each token look at the other tokens it is allowed to see and decide which matter [^src2]. Each token is transformed into three vectors via **learned matrices** — **Query, Key, Value (Q/K/V)** [^src2]:

> Query means "what am I looking for," Key means "what do I match with," and Value is the information that gets copied when the match is strong. [^src2]

- **Scaled dot product**: each token's Query is compared against the Key of every visible token via a dot product (how aligned two vectors are); scaling keeps numbers stable before softmax [^src2].
- **Softmax** turns match scores into weights that sum to 1; the weights take a weighted average of the Value vectors [^src2]. Example: processing "was" in "The cat that I saw yesterday was sleeping," the Query for "was" scores high against "cat" (subject) and low against "yesterday," so "cat"'s Value dominates the new representation [^src2].
- **Causal masking**: GPT-style models generate left-to-right, so a token at position 5 may only attend to positions 1–5. Future tokens get match scores so low they end up with effectively zero weight after softmax [^src2].
- **Induction heads** (Anthropic, 2022): specialized heads that spot patterns of the form "A B … A" and predict B comes next — copying what followed the earlier "A." One of the clearest known mechanisms behind **in-context learning** (picking up a pattern from the prompt and continuing it) [^src2].
- **The n² cost**: in full attention each token compares against all visible tokens, so doubling prompt length roughly quadruples the work — why long prompts are expensive and why FlashAttention, sparse, and linear attention are active research [^src2].

## Multi-head attention

A single attention pass gives one view of token relationships; language has many simultaneous relationships (subject-verb agreement, pronoun reference, long-range links) [^src2]. **Multi-head attention** runs attention many times in parallel, each **head** in its own smaller space [^src2].

- **Learned projections, not slices**: a common tutorial error. Each head has its own learned projection matrices mapping the full token vector down to its own smaller Q/K/V (e.g. 4,096 dims → 128-dim per head across 32 heads) — different *views* of the same token, not fixed chunks [^src2]. Head outputs are concatenated and passed through a final learned linear layer [^src2]. Heads specialize emergently (grammar, coreference, positional patterns, induction); a frontier model has thousands of heads total [^src2].
- **KV cache**: each head keeps its Key and Value vectors in memory for all already-generated tokens, so generating a new token doesn't recompute everything. This is the main memory cost of running an LLM at long context [^src2].
- **GQA (Grouped-Query Attention)**: most modern decoder-only LLMs let groups of query heads share fewer key/value heads — LLaMA-2 70B has 64 query heads but 8 KV heads; Mistral 7B has 32 query and 8 KV heads. Nearly full multi-head accuracy with much less KV-cache memory and inference cost [^src2].

## Feed-forward network (FFN)

After attention mixes information *between* tokens, each layer's FFN processes *each token independently*, with no cross-token mixing [^src2]. It does three things in order: **expand** the vector to a larger size (the original transformer used 4×), **apply a non-linearity**, then **compress** back to original size [^src2].

- **The non-linearity** prevents collapse: two stacked linear layers are mathematically equivalent to one, so without a bend in the middle the FFN couldn't do anything richer than a single matrix multiply [^src2]. Iteration: original transformer used **ReLU**; GPT and BERT moved to **GELU**; LLaMA, Mistral, PaLM use **SwiGLU** — the expand-compress structure stayed the same [^src2].
- **Where factual knowledge lives**: most parameters in a dense transformer sit in the FFN, not attention [^src2]. Those weights store much of the model's factual/semantic structure — researchers found individual neurons strongly associated with specific concepts (Eiffel-Tower text, programming languages, past-tense verbs) [^src2].
- **ROME editing**: Rank-One Model Editing can change a stored fact (e.g. "the Eiffel Tower is in Paris" → "in Rome") via a targeted low-rank edit to a specific FFN weight matrix, without retraining [^src2].
- **MoE**: some frontier models replace the dense FFN with [[ai-engineering/mixture-of-experts|Mixture of Experts]] — many parallel expert FFNs plus a router that activates only a few per token [^src2].

## Residual stream and layer normalization

The **residual stream** makes the model additive rather than replacing: after attention or the FFN runs, the result is *added* to the token's vector (new = old + sub-block output) rather than overwriting it [^src2]. Across dozens of layers each contribution accumulates, and the original input embeddings keep a direct additive path into late layers [^src2]. Residual connections came from **ResNet (He et al. 2015)** for image recognition, letting the training signal flow back through hundreds of layers [^src2]. In interpretability research the residual stream is the central object — every head, FFN, and the unembedding step reads from and writes back to it [^src2].

**Layer normalization** rescales each token's vector into a controlled range between sub-blocks, preventing the running sum from exploding or collapsing [^src2]. The original 2017 transformer used **post-norm** (after each sub-block); modern transformers (GPT-2 onward, LLaMA, Mistral) use **pre-norm**, easier to train deep [^src2]. Many modern open models (LLaMA, Mistral, Gemma, Phi) use **RMSNorm**, which drops the mean-shift step and keeps only the rescaling — cheaper, with most of the benefit [^src2].

## Next-token prediction and the generation loop

After all layers, the model takes the **final vector of the last token** and converts it into one number per possible next token (one per vocabulary entry) — the **logits**, raw scores of any size [^src2]. A **softmax** turns logits into a probability distribution over next tokens [^src2]. Decoding settings shape the output: **temperature** sharpens or flattens the distribution; **top-k / top-p** limit choices to the most plausible tokens [^src2].

The **generation loop**: pick a token, append it to the input, run the next step on the longer sequence (reusing the KV cache), produce a new prediction — repeating until an end-of-sequence token or length limit [^src2]. This single objective — predicting the next token over massive text — is the core training signal for a base LLM; factual accuracy, reasoning, and conversation come later from post-training [^src2]. **Speculative decoding** is an efficiency innovation: a small fast model proposes several tokens ahead and the big model verifies them in parallel, matching the big model's output distribution while running faster [^src2].

## Architecture vs trained weights

GPT, Claude, Gemini, and LLaMA broadly sit in the same transformer-family design space [^src2]. What changes between models is: the **trained weights** (different data, different scale); the **configuration** (layer count, vocabulary size, head count, parameter count, MoE-vs-dense); and the **post-training** (instruction tuning, RLHF, safety) [^src2]. The 2023–2025 "modern transformer" stack converged independently across teams on a common set of choices: **pre-norm, RMSNorm, RoPE, SwiGLU, GQA**, and **MoE** in the largest models — accumulated over ~five years on top of the 2017 design [^src2].

## Why it matters

Pre-Transformer architectures (RNNs, LSTMs) processed sequences token-by-token, preventing parallelization. The Transformer processes the full sequence in parallel, enabling GPU-scale training on internet-sized corpora [^src1].

Behavior is emergent — the architecture defines the framework; the billions of weights determine what the model actually does [^src1].

## See also

- [[ai-engineering/llm|LLM]] — the Transformer is the architecture underlying all modern LLMs
- [[ai-engineering/neural-network|Neural Networks]] — the broader network family the Transformer belongs to
- [[ai-engineering/mixture-of-experts|Mixture of Experts]] — sparse FFN variant used in the largest frontier models
- [[ai-engineering/context-window-management|Context Window Management]] — "lost in the middle" and the n² attention cost shape what to keep in context
- [[ai-engineering/context-engineering|Context Engineering]] — attention is what makes context-window structure matter; tokens attend across the full window

---

[^src1]: [[03_Resources/Study Notes/AI - How Large Language Models Work|AI - How Large Language Models Work]]
[^src2]: [How LLMs Actually Work](../../raw/web/how-llms-actually-work.md)

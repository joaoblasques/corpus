---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-which-tokens-does-a-hybrid-model-predict-better-04bd4874.md
    channel: web
    ingested_at: 2026-07-03
aliases:
  - Olmo
  - Olmo 3
  - Olmo Hybrid
  - Ai2
  - Allen Institute for AI
tags:
  - corpus/ai-engineering
  - entity
created: 2026-07-03
updated: 2026-07-03
---

# Olmo

**TL;DR.** Olmo is the Allen Institute for AI (Ai2)'s open language-model family. Ai2 trains matched pairs of models that differ only in architecture — a standard [transformer](/ai-engineering/transformer.md) (**Olmo 3**, 7B) and a hybrid attention/recurrent model (**Olmo Hybrid**, 7B) — to isolate what architectural choice buys, independent of data, tokenizer, or training recipe [^src1]. Hybrids can match or beat transformers on standard benchmarks, but that headline framing hides *which* kinds of tokens the advantage comes from [^src1].

## Attention vs. recurrence

- **Transformer (attention every layer)**: draws directly on every earlier token at once, weighted by relevance to the current prediction — strong at recalling one specific earlier token exactly, even far back in the input. Cost climbs steeply (quadratically) with input length. Weaker at representing information that evolves sequentially over time [^src1].
- **Hybrid (a few attention layers, rest recurrent)**: recurrent layers read left-to-right and carry a fixed-size, lossy, compressed memory — can't reach back for an exact earlier token the way attention can, but stays flat-cost regardless of input length and is well suited to tracking anything that changes as the model reads [^src1].

## Token-level loss-gap methodology

Ai2 fed both models matched passages (articles, Wikipedia, books, scientific papers, plus structured text: Python, HTML, LaTeX) and computed a **loss gap** per token — the difference in next-token prediction loss between the hybrid and the transformer. Positive gap = hybrid predicted better; negative = transformer did. Tokens were sorted into categories and loss gaps averaged per category, then re-checked with a regression controlling for confounds like category rarity and in-sample repetition rate [^src1].

## Findings

- **Hybrid's edge is biggest on content words** (meaning-bearing nouns, verbs, adjectives) and on tokens resolvable only by tracking context (e.g. pronoun antecedent resolution) — smallest on function words ("the," "of," "is") that syntax alone nearly determines [^src1].
- **Hybrid's advantage nearly disappears on exact verbatim repetition**: when the next token simply repeats an n-gram that already appeared earlier in the same passage, the longer the repeated run, the smaller the hybrid's lead — approaching zero. This is where the transformer's exact-recall strength (attention) dominates [^src1].
- **Closing braces (not opening) show no hybrid advantage** — a pattern robust across brackets in language, code, and markup; attention alone is known to suffice for bracket-matching [^src1].
- **Three-way comparison (transformer / hybrid / pure-recurrent, 1B params each)**: on meaning-bearing non-repeat tokens, hybrid and pure-recurrent both overtake the transformer, hybrid best of the three. On repeated tokens, the pure-recurrent model (no attention to reach back for the exact copy) falls behind *both* the hybrid and the transformer [^src1].

## Implication: filtered-loss evaluation

A single aggregate loss is "too blunt to compare transformer and hybrid architectures" — averaging over all tokens dilutes exactly the categories where architecture matters. Scoring loss on filtered token subsets (content words, repeats, bracket-closes) surfaces architectural differences visible even at small (1B) pretraining scale, before they'd show up in benchmark aggregates [^src1]. Ai2 is folding this into its ongoing hybrid-model design work, framing the state-tracking capability of RNN-style recurrent layers as the likely source of the content-word advantage [^src1].

## Related

- [Transformer](/ai-engineering/transformer.md) — the attention-only baseline architecture Olmo 3 represents; background on tokenization/attention mechanics
- [Nemotron 3 Ultra](/ai-engineering/nemotron-3-ultra.md) — another hybrid Transformer-Mamba (recurrent-family) MoE model, using the same attention-for-exact-recall / recurrence-for-long-context split
- [AI Engineering hub](/ai-engineering/README.md)

---

[^src1]: [Which tokens does a hybrid model predict better?](../../raw/web/web-which-tokens-does-a-hybrid-model-predict-better-04bd4874.md) — Hugging Face blog (Allen Institute for AI)

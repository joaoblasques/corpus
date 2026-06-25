---
type: entity
domain: mlops
status: stub
sources:
  - path: raw/github/github-ageron-handson-ml3.md
    channel: github
    ingested_at: 2026-06-25
aliases:
  - Hands-on Machine Learning
  - ageron/handson-ml3
  - Hands-on ML 3rd edition
  - Aurélien Géron
tags:
  - corpus/mlops
  - entity
created: 2026-06-25
updated: 2026-06-25
---

# Hands-On Machine Learning (3rd Edition)

**TL;DR** — Open-source companion repo (`ageron/handson-ml3`, 13,500+ stars) for Aurélien Géron's O'Reilly book *Hands-on Machine Learning with Scikit-Learn, Keras and TensorFlow (3rd edition)*. Jupyter notebooks covering ML fundamentals through deep learning using the standard Python ML stack [^src1].

## Key facts

- **Repo**: [github.com/ageron/handson-ml3](https://github.com/ageron/handson-ml3)
- **Stars**: ~13,513
- **Language**: Jupyter Notebook
- **Stack**: Python, Scikit-Learn, Keras, TensorFlow 2
- **Book**: [homl.info/er3](https://homl.info/er3) (O'Reilly 3rd edition)

## Running options

- **Google Colab** (recommended by author) — no local install needed; temporary environment [^src1]
- **Kaggle** — alternative cloud notebook environment
- **Binder** — browser-based notebooks
- **Local** — requires Anaconda/Miniconda + git + GPU driver (if using TensorFlow GPU) + CUDA/cuDNN [^src1]
- **Docker** — Docker instructions available in the repo

## Positioning

Established standard reference for hands-on ML fundamentals. The 3rd edition updates the prior editions to TensorFlow 2 / Keras 3 and is the most current. Prior editions (`handson-ml2`, `handson-ml`) remain available [^src1].

## See also

- [[mlops/made-with-ml|Made With ML]] — alternative production-focused ML course (GokuMohandas); focus on deploy + iterate vs. this repo's fundamentals
- [[mlops/mlops-principles|MLOps Principles]] — the engineering discipline on top of the ML fundamentals covered here
- [[mlops/README|MLOps hub]]

---

[^src1]: [ageron/handson-ml3 (GitHub)](../../raw/github/github-ageron-handson-ml3.md) — README: purpose, stack, running options, book link

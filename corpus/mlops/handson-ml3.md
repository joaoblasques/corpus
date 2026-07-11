---
type: entity
domain: mlops
status: draft
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
updated: 2026-07-11
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

| Option | Notes |
|---|---|
| **Google Colab** (recommended) | No install; "anything you do will be deleted after a while" [^src1] |
| **Kaggle** | Alternative cloud notebook environment |
| **Binder** | Browser-based; not fully tested by author [^src1] |
| **Deepnote** | Browser-based; not fully tested by author [^src1] |
| **nbviewer** | Read-only rendering; no code execution |
| **Docker** | Docker directory in the repo; created by contributors [^src1] |
| **Local** | Anaconda/Miniconda + git; GPU needs driver + CUDA/cuDNN [^src1] |

### Local install steps

```
git clone https://github.com/ageron/handson-ml3.git
cd handson-ml3
conda env create -f environment.yml
conda activate homl3
python -m ipykernel install --user --name=python3
jupyter notebook
```

Author recommends Python 3.10 (bundled in the env); any version ≥3.7 works [^src1].

## Positioning

Established standard reference for hands-on ML fundamentals. The 3rd edition updates prior editions to TensorFlow 2 / Keras 3 and is the most current; `handson-ml2` (2nd ed.) and `handson-ml` (1st ed.) remain available [^src1].

## Community & contributors

Haesun Park and Ian Beauregard reviewed every notebook and submitted many PRs including exercise solutions. Steven Bunkley and Ziembla created the `docker` directory. Victor Khaustov submitted "plenty of excellent PRs, fixing many errors" [^src1].

## See also

- [Made With ML](/mlops/made-with-ml.md) — alternative production-focused ML course (GokuMohandas); focus on deploy + iterate vs. this repo's fundamentals
- [MLOps Principles](/mlops/mlops-principles.md) — the engineering discipline on top of the ML fundamentals covered here
- [MLOps hub](/mlops/README.md)

---

[^src1]: [ageron/handson-ml3 (GitHub)](../../raw/github/github-ageron-handson-ml3.md) — README: purpose, stack, running options, book link

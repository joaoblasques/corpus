---
type: entity
domain: mlops
status: draft
sources:
  - path: raw/github/github-avik-jain-100-days-of-ml-code.md
    channel: github
    ingested_at: 2026-06-25
aliases:
  - 100 Days of ML Code
  - Avik-Jain/100-Days-Of-ML-Code
  - 100DaysOfMLCode
tags:
  - corpus/mlops
  - entity
created: 2026-06-25
updated: 2026-07-14
---

# 100 Days of ML Code

**TL;DR** — Open-source ML learning log (`Avik-Jain/100-Days-Of-ML-Code`, 51k+ stars) — a structured 100-day challenge to learn and implement ML algorithms daily, using infographics and Python/Scikit-Learn code. Proposed by Siraj Raval; one of the most-starred ML repositories on GitHub [^src1].

## Key facts

- **Repo**: [github.com/Avik-Jain/100-Days-Of-ML-Code](https://github.com/Avik-Jain/100-Days-Of-ML-Code)
- **Stars**: ~51,291
- **Origin**: challenge proposed by [Siraj Raval](https://github.com/llSourcell) [^src1]
- **Topics**: `machine-learning`, `deep-learning`, `linear-regression`, `logistic-regression`, `naive-bayes-classifier`, `svm`, `scikit-learn`, `python`, `infographics`, `linear-algebra`, `implementation`, `tutorial`
- **Format**: Day-by-day log; each entry pairs an infographic (visual explanation of the algorithm) with a linked code implementation in Python/Scikit-Learn

## Day-by-day coverage

The documented days from the README [^src1]:

| Days | Topic |
|------|-------|
| 1 | Data preprocessing |
| 2 | Simple linear regression |
| 3 | Multiple linear regression |
| 4 | Logistic regression (intro) |
| 5 | Logistic regression — cost function and gradient descent math |
| 6 | Implementing logistic regression |
| 7 | K-Nearest Neighbours (infographic) |
| 8 | Math behind logistic regression (external article) |
| 9 | Support Vector Machines — intuition |
| 10 | SVM continued + K-NN study |
| 11 | K-NN implementation |
| 12 | SVM infographic |
| 13 | Naive Bayes classifier |
| 14 | SVM implementation with Scikit-Learn `SVC` on linearly separable data |
| 15 | Naive Bayes types + Bloomberg ML lectures (Black Box ML overview) |
| 16 | SVM with kernel trick via Scikit-Learn |
| 17 | Deep Learning Specialization (Coursera) — Week 1 & 2; logistic regression as neural net |
| 18 | Deep Learning Specialization — Course 1 complete; neural net implemented in Python |
| 19 | Caltech CS 156 Lecture 1 — introduction + Perceptron Algorithm |

## External courses integrated

The log integrates content from multiple external sources alongside original implementations [^src1]:

- **Coursera Deep Learning Specialization** — Weeks 1–2 of Course 1 covered on Day 17–18
- **Bloomberg ML Foundations** (`bloomberg.github.io/foml`) — Black Box ML lecture on Day 15; covers prediction functions, feature extraction, cross-validation, overfitting, hyperparameter tuning
- **Caltech CS 156** (Professor Yaser Abu-Mostafa) — 18-lecture ML course; started Day 19

## Pedagogy

- Infographic-first: each algorithm gets a visual explanation before code; "due to less time I will now be posting an infographic on alternate days" [^src1] reflects a realistic pacing trade-off.
- Datasets bundled in the repo (`/datasets` directory).
- Code entries are Markdown files in `/Code/`, not Jupyter notebooks.
- No automated tests or project structure — purely a learning log, not a library.

## Positioning

A challenge/accountability format rather than a structured course. Strong visual learning component (infographics for each algorithm). Breadth-first across classical ML algorithms (preprocessing → regression → classification → SVM → Naive Bayes → deep learning), then pivots to external specialization content. Better for algorithm breadth and visual intuition than production engineering depth. Compare to [Made With ML](/mlops/made-with-ml.md) (production-focused) or [Hands-On ML 3rd Edition](/mlops/handson-ml3.md) (textbook depth).

## Gotchas

- Infographic cadence drops to every other day after Day 5, by the author's own note [^src1].
- SVM implementation (Day 14) only covers linearly separable data; kernel trick deferred to Day 16.
- Deep learning content (Day 17+) pivots to following Coursera rather than original implementations.

## See also

- [Hands-On ML (3rd Edition)](/mlops/handson-ml3.md) — more comprehensive textbook-based ML fundamentals
- [Made With ML](/mlops/made-with-ml.md) — production ML engineering focus
- [MLOps hub](/mlops/README.md)

---

[^src1]: [Avik-Jain/100-Days-Of-ML-Code (GitHub)](../../raw/github/github-avik-jain-100-days-of-ml-code.md)

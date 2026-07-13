---
type: entity
domain: mlops
status: draft
sources:
  - path: raw/notes/00-02-git-and-collaboration-kb.md
    channel: notes
    ingested_at: 2026-06-09
  - path: raw/youtube/youtube-Uszj_k0DGsg-git-for-professionals-tutorial-tools-concepts-for-mastering.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-pJYOG6klqj8-the-only-github-guide-youll-ever-need.md
    channel: youtube
    ingested_at: 2026-06-25
aliases:
  - git
  - Git
  - version control
  - gitignore
tags:
  - corpus/mlops
  - entity
created: 2026-06-09
updated: 2026-06-25
---

# Git

**TL;DR**: Git is a **content-addressed snapshot store with a graph of commits**, not a diff tracker. Branches are cheap movable pointers into that graph. It is the substrate that makes ML work collaborative and reversible — but ML breaks Git's assumptions because checkpoints are large, binary, and non-reconstructable, the opposite of what Git is optimized for [^src1].

## Mental model

Each commit is `(tree SHA, parent SHA(s), author, message)`; identical content yields an identical SHA [^src1].

- **Commit identity**: `commit_sha = SHA1(tree_sha || parent_sha(s) || author || committer || message)` — content-addressable [^src1].
- **Branch invariant**: a branch is a pointer to one commit; the commit knows its parents, not the reverse [^src1].
- **`.gitignore` invariant**: patterns apply only to *untracked* paths. Already-tracked files must be untracked (`git rm --cached <path>`) before the ignore takes effect [^src1].
- **History invariant**: `main` is append-only by convention; force-push to a shared branch breaks every collaborator's clone [^src1].

## Branch-per-task workflow

The course's discipline: one feature branch per unit of work, conventional-commit messages, merge via PR [^src1].

```bash
git checkout -b feature/phase-XX-lesson-YY
git add path/to/changed/files          # stage explicitly, not `git add .`
git commit -m "feat(XX-YY): short imperative summary"
git push -u origin feature/phase-XX-lesson-YY
# Open PR → review → merge → delete branch
```

## ML-aware `.gitignore`

Large binary checkpoints must stay out of history — once committed, Git keeps every blob forever [^src1]:

```gitignore
*.pt
*.pth
*.safetensors
*.onnx
*.bin
*.h5
```

When large files genuinely *should* be versioned (datasets, golden eval sets), the opposite prescription applies: a content-addressed sidecar (DVC) or Git LFS pointer protocol, not raw `git add` [^src1]. *(Forward reference to a data-management source not yet ingested.)*

## Common pitfalls

- **Committing large binaries** → repo grows permanently even after deletion. Fix: add patterns to `.gitignore` *before* the first `git add`; if already committed, scrub with `git filter-repo`/BFG and switch to DVC/LFS [^src1].
- **Adding `.gitignore` after the fact** → no effect on tracked files. Fix: `git rm --cached <path>`, then commit [^src1].
- **Force-pushing a shared branch** → rewrites history; collaborators diverge silently. Use `--force-with-lease` for solo branches only; never for shared ones [^src1].
- **`git add .` after a training run** → silently stages every checkpoint/output/cache. Stage explicitly or `git status` first [^src1].

## Branching strategies (intermediate)

Two spectrum extremes [^src2]:

| Strategy | Branches | Cadence | Requires |
|---|---|---|---|
| **Always be integrating** (trunk-based) | Single main; tiny frequent commits | Constant | Top-notch CI + test coverage |
| **Multi-branch** (GitFlow-style) | main + develop + feature + release + hotfix | Batched releases | More process overhead |

### Long-running vs. short-lived branches [^src2]

- **Long-running**: exist for the full project lifecycle (main, develop, staging, production). Commits added only via merge/rebase — never directly.
- **Short-lived**: feature, bugfix, refactor, experiment. Created from a long-running branch; merged back and deleted.

### GitHub Flow (lean) [^src2]

Single long-running branch (`main`) + one short-lived branch per feature/fix:
1. Branch off main
2. Commit and push
3. Open Pull Request → review → CI → merge
4. Delete branch

### Git Flow (structured) [^src2]

- `main` = current production state
- `develop` = integration branch; feature branches merge here
- `release` branches cut from develop; merge to both main and develop
- `hotfix` branches cut from main; merge to both main and develop

## Crafting the perfect commit

Three-part discipline [^src2]:

1. **Right changes**: one topic per commit; use `git add -p` (patch mode) to stage individual hunks — not whole files
2. **Right message**: subject line <80 chars, imperative mood; body answers *what changed*, *why*, *anything to watch out for*
3. **Good history**: readable `git log` is the payoff — future-you and teammates can audit decisions

```bash
# Stage only the first hunk of a file (not the whole file)
git add -p index.html    # y=include, n=skip for each hunk

# Full commit with body
git commit               # opens $EDITOR; subject + blank line + body
```

> "If you have trouble writing something short and concise, this might be an indication that you've put too many different topics into that commit." [^src2]

## GitHub concepts (beginner reference)

From a beginner-oriented guide [^src3]:

- **Repository** = the project folder in the cloud (version-controlled)
- **Star** = bookmark/like on a public repo
- **Fork** = copy a repo into your GitHub profile; you can modify independently and send PRs back
- **Clone** = download a repo locally; `git clone <url>`
- **Push** = upload local commits to GitHub; requires SSH key authentication
- **Pull Request (PR)** = propose changes from your fork/branch into the upstream repo
- **Mono repo** = single repository for all of an app's code
- **Poly repo** = multiple repositories, one per sub-system (front-end, back-end, payments, etc.); enables granular access control and faster partial deployments

SSH key is the recommended authentication method — access tokens are possible but require more management [^src3].

## See also

- [Dev Environment Stack](/mlops/dev-environment-stack.md) — Git is a Layer-1 system-foundation tool
- [CLI Tools](/mlops/cli-tools.md) — the GitHub CLI (`gh`), `pass` (git-backed secrets), and `delta` (git diffs) build on Git
- [CI/CD for ML](/mlops/ci-cd-for-ml.md) — Git Flow + branch protection + GitHub Actions integration
- [MLOps hub](/mlops/README.md)

---

[^src1]: [AI Engineering from Scratch — Phase 00 / 02 Git & Collaboration](../../raw/notes/00-02-git-and-collaboration-kb.md)
[^src2]: [Git for Professionals Tutorial — Tools & Concepts for Mastering Version Control (Tobias Günther / freeCodeCamp.org)](../../raw/youtube/youtube-Uszj_k0DGsg-git-for-professionals-tutorial-tools-concepts-for-mastering.md) — [01:29](../../raw/youtube/youtube-Uszj_k0DGsg-git-for-professionals-tutorial-tools-concepts-for-mastering.md#t=89) perfect commit; [04:23](../../raw/youtube/youtube-Uszj_k0DGsg-git-for-professionals-tutorial-tools-concepts-for-mastering.md#t=263) git add -p; [08:09](../../raw/youtube/youtube-Uszj_k0DGsg-git-for-professionals-tutorial-tools-concepts-for-mastering.md#t=489) branching strategies; [11:51](../../raw/youtube/youtube-Uszj_k0DGsg-git-for-professionals-tutorial-tools-concepts-for-mastering.md#t=711) long-running vs short-lived; [15:07](../../raw/youtube/youtube-Uszj_k0DGsg-git-for-professionals-tutorial-tools-concepts-for-mastering.md#t=907) GitHub Flow
[^src3]: [The Only GitHub Guide You'll Ever Need (corbin)](../../raw/youtube/youtube-pJYOG6klqj8-the-only-github-guide-youll-ever-need.md) — [01:44](../../raw/youtube/youtube-pJYOG6klqj8-the-only-github-guide-youll-ever-need.md#t=104) version control; [03:28](../../raw/youtube/youtube-pJYOG6klqj8-the-only-github-guide-youll-ever-need.md#t=208) collaboration; [06:09](../../raw/youtube/youtube-pJYOG6klqj8-the-only-github-guide-youll-ever-need.md#t=369) fork; [12:38](../../raw/youtube/youtube-pJYOG6klqj8-the-only-github-guide-youll-ever-need.md#t=758) SSH key; [07:27](../../raw/youtube/youtube-pJYOG6klqj8-the-only-github-guide-youll-ever-need.md#t=447) poly repo

<!-- RELATED:START (generated by bin/corpus_heal.py related — do not edit inside) -->

## Related across domains

- [Git Basics](/software-engineering/git-basics.md) · _software-engineering_

<!-- RELATED:END -->

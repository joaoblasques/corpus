---
type: entity
domain: mlops
status: draft
sources:
  - path: raw/notes/00-02-git-and-collaboration-kb.md
    channel: notes
    ingested_at: 2026-06-09
aliases:
  - git
  - Git
  - version control
  - gitignore
tags:
  - corpus/mlops
  - entity
created: 2026-06-09
updated: 2026-06-09
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

## See also

- [[mlops/dev-environment-stack|Dev Environment Stack]] — Git is a Layer-1 system-foundation tool
- [[mlops/README|MLOps hub]]

---

[^src1]: [AI Engineering from Scratch — Phase 00 / 02 Git & Collaboration](../../raw/notes/00-02-git-and-collaboration-kb.md)

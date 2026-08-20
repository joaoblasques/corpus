---
type: entity
domain: software-engineering
status: draft
sources:
  - path: raw/github/github-0nn0-git-basics-cheatsheet.md
    channel: github
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-Ala6PHlYjmw-git-will-finally-make-sense-after-this.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-7h6_aZZ_iNg-intermediate-github-tutorial.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/github/github-ksylor-ohshitgit.md
    channel: github
    ingested_at: 2026-06-25
  - path: raw/web/web-highlights-from-git-2-55-b438fa86.md
    channel: web
    ingested_at: 2026-08-20
aliases:
  - Git
  - version control
  - git cheatsheet
  - git commands
  - staging
  - commit
  - branch
  - pull request
  - rebase
  - merge
  - cherry-pick
  - detached HEAD
  - git reset
  - reflog
  - Oh Shit Git
  - Dangit Git
tags:
  - corpus/software-engineering
  - entity
created: 2026-06-25
updated: 2026-08-20
---

# Git Basics

**TL;DR**: Git is an open-source distributed version-control system for storing and managing code changes. Key workflow: stage changes (`git add`), commit to local repo (`git commit`), sync with remote (`git push` / `git pull`). Branches isolate feature development; pull requests submit contributions for review [^src1].

## Core glossary

| Term | Definition |
|---|---|
| **staging** | Files/directories proposed for the next commit |
| **commit** | Saving staged files to the local repository |
| **branch** | Independent line of development — master/main is default |
| **clone** | Local copy of a repository including all commits and branches |
| **remote** | Shared repository (e.g., GitHub) all team members sync with |
| **fork** | Personal copy of another user's repository |
| **pull request** | Method of submitting contributions to a repository for review |
| **HEAD** | Pointer to the current working directory state |

## Essential command groups

### Configuration

```bash
git config --global user.name [name]    # set author name for all commits
git config --global user.email [email]  # set author email for all commits
git config color.ui true                # enable colorized output
```

### Core commands

```bash
git init [dir]          # create new local repository
git clone [repo]        # create local copy of remote repo
git add [dir/file]      # stage specific directory or file
git status              # show staged/unstaged/untracked files
git diff                # show unstaged changes
git commit -m "[msg]"   # commit staged changes with message
git push [remote] [branch]  # push branch to remote
git pull                # fetch and merge from remote
git log                 # show commit history
```

### Branch operations

```bash
git branch              # list local branches
git branch [name]       # create a new branch
git checkout [branch]   # switch to branch
git checkout -b [branch]  # create and switch
git merge [branch]      # merge branch into current
git branch -d [branch]  # delete local branch
```

## Git's internal data model

Git is a database of snapshots; the fundamental unit is the **commit** [^src2].

Each commit contains three things [^src2]:

1. A pointer to a complete snapshot (every file exactly as it existed)
2. Metadata (author, timestamp, message)
3. A pointer to the parent commit

Commits form a **Directed Acyclic Graph (DAG)**: children point to parents; parents never know their future children; no loops are possible [^src2]. "Children know their parents, but parents never know their future children." [^src2]

**Branches are sticky notes, not containers.** A branch is just a tiny file containing a single commit hash. Creating a branch is instant — no files are copied [^src2]. `main` is not special; it's just the branch whose sticky-note convention everyone agreed on [^src2].

**HEAD** tracks your current location — it normally points to a branch, not directly to a commit. If you `git checkout` a raw commit hash, HEAD points to the commit directly: this is **detached HEAD state**. Commits made in detached HEAD state are orphaned when you switch away and will eventually be garbage-collected [^src2].

### The three areas

Git code lives in three places simultaneously [^src2]:

| Area | Description |
|---|---|
| **Working directory** | Actual files on disk — what you see in your editor |
| **Staging area (index)** | "Waiting room" for what goes into the next commit |
| **Repository** | Permanent database of commits |

`git add` moves changes to the staging area; `git commit` snapshots staging into the repo.

## Advanced operations

### Reset vs. revert vs. checkout

| Command | What moves | Staging area | Working dir | Safe for shared history? |
|---|---|---|---|---|
| `git checkout` | HEAD only | Unchanged | Unchanged | Yes |
| `git reset --soft` | Branch pointer | Unchanged | Unchanged | No |
| `git reset --mixed` (default) | Branch pointer | Reset to target | Unchanged | No |
| `git reset --hard` | Branch pointer | Reset to target | Reset to target | No — uncommitted work gone forever |
| `git revert` | Nothing | N/A | New commit added | Yes |

**Revert** creates a new commit that does the opposite of a previous commit — history is preserved, making it safe to push on shared branches [^src2].

### Rebase: replaying commits with new parents

Rebase takes commits from a feature branch and replays them on top of the updated base. Because a commit's identity (its hash) is derived from its content, metadata, and parent pointer — changing the parent produces an entirely new commit with a new hash [^src2].

"A commit's identity is its hash. That hash is generated from the content, the metadata, and the parent pointer. Change any of those, including the parent, and you get a completely different hash." [^src2]

**Golden rule**: never rebase commits others have already seen. They will have the old hashes; you push new hashes; Git sees them as unrelated work [^src2].

Merge vs. rebase trade-off: merge preserves the true parallel history (two parents); rebase creates a clean linear history at the cost of rewriting commits [^src2].

### Cherry-pick

Pick a specific commit from another branch and apply it to the current branch. Useful for backporting a fix to a release branch without merging unrelated changes [^src3].

### Conflict resolution

A merge conflict occurs when two branches make different changes to the same line, or one branch deletes a file the other modified [^src3]. Git marks the conflict in the file between `<<<`, `===`, and `>>>` delimiters — the region above `===` is the current branch's version, below is the incoming [^src3].

### Reflog: your safety net

`git reflog` shows everywhere HEAD has pointed recently — every checkout, reset, commit [^src2]. Lost commits from a hard reset or rebase are usually recoverable by finding the hash in the reflog and creating a branch pointing to it [^src2]. Reflog entries expire (30–90 days), so act quickly [^src2].

## Professional pull request workflow

1. Pull from main to get the latest: `git pull` [^src3]
2. Create a feature branch prefixed with your name/ID: `git checkout -b name-feature` [^src3]
3. Commit changes with a descriptive message in present tense [^src3]
4. Push the branch: `git push origin name-feature` [^src3]
5. Open a pull request — fill a descriptive template; request reviewers [^src3]
6. After merge, pull main again before creating new branches [^src3]
7. Delete stale branches to keep the remote clean [^src3]

## Oh Shit, Git!?!

`ohshitgit.com` (★1,547) is a popular reference for common Git mistakes and how to undo them — covering scenarios like "I committed to the wrong branch," "I pushed something that shouldn't be there," and similar [^src4]. A swear-free version exists at `dangitgit.com`. Built with Eleventy (11ty) and deployed to Netlify; translation contributions welcome [^src4].

## Git 2.55 highlights (2026)

Key features from the Git 2.55 release (100+ contributors, 33 new):[^src5]

**Incremental multi-pack indexes (MIDX) with geometric repacking**: `git repack --write-midx=incremental` writes new MIDX layers without rewriting the entire index. Combined with `--geometric=2 -d`, the algorithm compacts layers geometrically, keeping the chain length logarithmic. Result: large-repo maintenance can update pack metadata incrementally rather than rewriting a monolithic MIDX. Critical for GitHub's own repository maintenance strategy.[^src5]

**`git history fixup`**: New experimental subcommand — applies staged changes to an earlier commit and replays descendant commits on top. Cleaner alternative to `git commit --fixup` + `git rebase --autosquash`. Conservative: aborts on conflicts rather than leaving a stateful rewrite mid-stream.[^src5]

**Parallel config-based hooks**: Hooks declaring `hook.<name>.parallel = true` can run concurrently. Control with `hook.jobs` (global), `hook.<event>.jobs` (per-event), or `-j` at the command line.[^src5]

**Linux filesystem monitor (inotify)**: `core.fsmonitor` daemon now supports Linux via inotify, matching macOS and Windows. Speeds up `git status` in large trees by tracking changed paths without full scans; requires one watch per directory.[^src5]

**Bitmap generation speedups**: Bitmap generation on a large repository dropped from ~612s to ~294s with pseudo-merge improvements.[^src5]

**`--graph-lane-limit=<n>`**: Caps the number of graph lanes in `git log --graph`; lanes beyond the limit become `~` characters, making wide histories readable.[^src5]

**`--max-count-oldest=<n>`**: New option on `git rev-list` / `git log` family to select the N *oldest* commits in a range (unlike `--reverse -n` which takes newest then reverses).[^src5]

**ANSI control character masking in sideband output**: Git now strips most terminal control sequences from remote progress output, preventing a server from injecting cursor-movement sequences. ANSI color codes still pass through.[^src5]

**Push to remote groups**: `git push <remote-group>` mirrors an existing `remotes.<name>` feature from `git fetch` to `git push`. Define a group: `git config remotes.publish "github gitlab mirror"` then `git push publish main`.[^src5]

## See also

- [CI/CD and Progressive Delivery](/software-engineering/ci-cd.md) — Git is the foundation of GitOps and CI pipelines
- [Engineering Craft](/software-engineering/engineering-craft.md) — version control fluency as a baseline skill

---

[^src1]: [git-basics-cheatsheet (0nn0)](../../raw/github/github-0nn0-git-basics-cheatsheet.md)
[^src2]: [Git Will Finally Make Sense After This (LearnThatStack)](../../raw/youtube/youtube-Ala6PHlYjmw-git-will-finally-make-sense-after-this.md)
[^src3]: [Intermediate GitHub Tutorial (Tech With Tim)](../../raw/youtube/youtube-7h6_aZZ_iNg-intermediate-github-tutorial.md)
[^src4]: [Oh Shit, Git!?! (ksylor)](../../raw/github/github-ksylor-ohshitgit.md)
[^src5]: raw/web/web-highlights-from-git-2-55-b438fa86.md — GitHub Blog, "Highlights from Git 2.55"

<!-- RELATED:START (generated by bin/corpus_heal.py related — do not edit inside) -->

## Related across domains

- [Git](/mlops/git.md) · _mlops_

<!-- RELATED:END -->

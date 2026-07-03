---
type: concept
domain: mlops
status: draft
sources:
  - path: raw/youtube/youtube-CLh2ACdXNbc-20-of-linux-commands-you-ll-use-80-of-the-time-real-world-ex.md
    channel: youtube
    ingested_at: 2026-06-15
  - path: raw/youtube/youtube-ZtqBQ68cfJc-the-50-most-popular-linux-terminal-commands-full-course-for.md
    channel: youtube
    ingested_at: 2026-06-20
  - path: raw/youtube/youtube-qOrlYzqXPa8-50-macos-tips-and-tricks-using-terminal-the-last-one-is-craz.md
    channel: youtube
    ingested_at: 2026-06-25
aliases:
  - Linux commands
  - Linux fundamentals
  - shell commands
  - bash commands
  - unix commands
  - file permissions
  - chmod
tags:
  - corpus/mlops
  - concept
created: 2026-06-15
updated: 2026-06-15
---

# Linux Commands

**TL;DR**: The ~20% of Linux commands that cover ~80% of real work, framed through a debugging scenario (a production app can't reach its database). The arc: **navigate the filesystem → read & filter logs → trace the misconfiguration → fix file permissions → edit the file** [^src1]. `uname` ("Unix name") confirms you're on Linux — the OS Linux was built on top of [^src1].

## Navigation & inspection

| Command | Does | Notes |
|---|---|---|
| `pwd` | print working directory | "where am I" [^src1] |
| `cd <path>` | change directory | [^src1] |
| `ls` / `ls -l` | list files / long view | `-l` shows permissions + size [^src1] |
| `cat <file>` | print file contents | "concatenate" — joins/prints text [^src1] |
| `find <path> -name "<glob>"` | locate files by name | `/` searches the whole tree; `.` the current dir [^src1] |
| `diff a b` | compare two files | used to spot a changed config line [^src1] |

## Pipes & redirection

- **Pipe `|`** chains commands — one command's output becomes the next's input [^src1].
- **`grep <pattern>`** filters lines containing a word/phrase; quote multi-word phrases (`grep "connection refused"`) [^src1].
- **`wc -l`** counts lines (e.g. `grep ... | wc -l` counts how many times an error occurred) [^src1].
- **Redirect `>`** writes output to a file instead of the terminal (`grep database errors.log > db-errors.txt`) [^src1].
- **`cp src dst`** copies a file, optionally to another path for a backup [^src1].

The worked example chains these to diagnose the bug: `cat error.log | grep "connection refused" | wc -l`, then `find / -name "*.conf" | grep db`, then `diff db.conf db.conf.backup` reveals the app points at port **5433** while Postgres listens on **5432** [^src1]. `curl -I http://localhost:5432` confirms the DB is reachable on the correct port [^src1].

## File permissions

`ls -l` shows a 10-char permission string: first char is type (`-` file, `d` directory), then three triplets (owner / group / others), each **r**ead / **w**rite / e**x**ecute [^src1].

`chmod` sets permissions with octal digits, one per triplet [^src1]:

| Octal | Meaning |
|---|---|
| `000` | no permissions |
| `444` | read-only for all three |
| `600` | read+write for owner, nothing for others |
| `666` | read+write for all |
| `777` | read+write+execute for all (relevant for executables like bash scripts) |

In production a config may be locked **read-only** to prevent accidental overwrites; `chmod 600 db.conf` re-grants the owner write access so it can be edited, then it can be locked again [^src1].

## Editing with vim

`vim <file>` opens the command-line editor, which has two modes [^src1]:

- **Navigation (normal) mode** — default on open.
- **Insert/edit mode** — enter with `i`.
- **Quit without saving**: `Esc` then `:q!`. **Save and quit**: `Esc` then `:wq` [^src1].

> A `chmod`-then-`vim` gotcha: trying to enter insert mode on a read-only file shows "changing a readonly file" — fix the permission first [^src1].

## The 50 Linux commands landscape (freeCodeCamp course)

A full freeCodeCamp course (Colt Steele, 4.5+ hours) sequences all 50 most-popular Linux commands grouped by function, taught through a hands-on narrative [^src2]:

**Why the terminal matters** [^src2]:
- **Control** — GUI applications show you only what they want you to see; the terminal exposes everything.
- **Automation** — shell scripts chain any combination of 50 commands into repeatable pipelines.
- **Career** — sysadmin, cloud, DevOps, ML deployment, and data engineering all assume terminal fluency.

**Unix family tree** [^src2]: Bell Labs (1969) → Unix → BSD → Linux (1991, Linus Torvalds). GNU/Linux is the full pairing: the Linux kernel plus GNU user-space utilities (bash, coreutils, etc.).

**Shells** [^src2]: bash (Bourne Again Shell) is the default on most Linux; zsh (Z Shell) is the default on macOS and popular for plugins (oh-my-zsh). All commands in this corpus work in both.

**Command categories covered in the full 50** (structural overview) [^src2]:
- **Navigation**: `pwd`, `ls`, `cd`, `mkdir`, `rmdir`, `touch`
- **Reading / searching**: `cat`, `less`, `more`, `head`, `tail`, `grep`, `wc`, `sort`, `uniq`
- **File management**: `cp`, `mv`, `rm`, `find`, `locate`
- **Compression / archives**: `tar`, `gzip`, `gunzip`, `zip`, `unzip`
- **Process management**: `ps`, `kill`, `top`, `htop`, `bg`, `fg`, `jobs`
- **Networking**: `ping`, `curl`, `wget`, `ssh`, `scp`, `ifconfig`, `netstat`
- **Permissions**: `chmod`, `chown`, `sudo`, `su`
- **Disk / system**: `df`, `du`, `uname`, `whoami`, `history`, `echo`, `man`
- **Text processing**: `awk`, `sed`, `cut`, `paste`, `tr`

The 20% / 80% rule holds: the ~20 commands covered in the existing page above cover ~80% of real work; the remaining 30 commands (networking, compression, process management, awk/sed) cover long-tail production scenarios [^src2].

## See also

- [CLI Tools](/mlops/cli-tools.md) — modern replacements: `rg` for `grep`, `fd` for `find`, `bat` for `cat`, `eza` for `ls`
- [Terminal & Shell](/mlops/terminal-and-shell.md) — the shell these commands run in
- [Git](/mlops/git.md) — versioning the files you navigate and edit
- [MLOps hub](/mlops/README.md)

---

[^src1]: [20% of Linux Commands You'll Use 80% of the Time (TechWorld with Nana)](../../raw/youtube/youtube-CLh2ACdXNbc-20-of-linux-commands-you-ll-use-80-of-the-time-real-world-ex.md)
[^src2]: [The 50 Most Popular Linux Terminal Commands — Full Course (freeCodeCamp / Colt Steele)](../../raw/youtube/youtube-ZtqBQ68cfJc-the-50-most-popular-linux-terminal-commands-full-course-for.md) — uname [[02:35](../../raw/youtube/youtube-CLh2ACdXNbc-20-of-linux-commands-you-ll-use-80-of-the-time-real-world-ex.md#t=02:35)], pwd/cd/ls [[03:57](../../raw/youtube/youtube-CLh2ACdXNbc-20-of-linux-commands-you-ll-use-80-of-the-time-real-world-ex.md#t=03:57)], cat/grep/pipe [[05:45](../../raw/youtube/youtube-CLh2ACdXNbc-20-of-linux-commands-you-ll-use-80-of-the-time-real-world-ex.md#t=05:45)], redirect/cp [[07:28](../../raw/youtube/youtube-CLh2ACdXNbc-20-of-linux-commands-you-ll-use-80-of-the-time-real-world-ex.md#t=07:28)], find/diff/curl [[12:22](../../raw/youtube/youtube-CLh2ACdXNbc-20-of-linux-commands-you-ll-use-80-of-the-time-real-world-ex.md#t=12:22)], vim [[18:37](../../raw/youtube/youtube-CLh2ACdXNbc-20-of-linux-commands-you-ll-use-80-of-the-time-real-world-ex.md#t=18:37)], permissions/chmod [[19:57](../../raw/youtube/youtube-CLh2ACdXNbc-20-of-linux-commands-you-ll-use-80-of-the-time-real-world-ex.md#t=19:57)]
</content>

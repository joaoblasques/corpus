---
type: concept
domain: mlops
status: draft
sources:
  - path: raw/youtube/youtube-ISJ44S5sZu8-linux-file-system-structure-explained-from-to-usr-linux-basi.md
    channel: youtube
    ingested_at: 2026-06-25
aliases:
  - Linux file system
  - Linux directory structure
  - FHS
  - Filesystem Hierarchy Standard
  - /bin
  - /etc
  - /usr
  - /var
  - /proc
tags:
  - corpus/mlops
  - concept
created: 2026-06-25
updated: 2026-06-25
---

# Linux Filesystem Structure

**TL;DR** — Everything in Linux starts from `/` (root directory) — a single unified tree, unlike Windows drive letters. Top-level directories are organized by purpose: who owns the files, how long they live, and whether they're real or virtual. Understanding this layout is prerequisite for server and VPS work [^src1].

## Directory map

| Directory | Category | Purpose |
|---|---|---|
| `/` | Root | Top of the tree; all paths descend from here |
| `/bin` | System binaries | Essential commands (`ls`, `cp`, `mv`, `cat`); always available even in recovery mode |
| `/sbin` | System admin binaries | Admin-only tools (`mount`, `fsck`, `shutdown`); require root |
| `/lib` | Shared libraries | `.so` files that `/bin` and `/sbin` depend on; also kernel modules |
| `/usr` | Unix System Resources | Most installed programs live here: `/usr/bin`, `/usr/lib`, `/usr/sbin` — read-only, managed by package manager |
| `/boot` | Boot & kernel | Kernel, initrd, GRUB config (`grub.cfg`); never touch unless you know why |
| `/etc` | Configuration | System-wide config files (`/etc/passwd`, `/etc/fstab`, `/etc/crontab`); plain text, admin-editable |
| `/home` | User home dirs | Personal space: `/home/alice`, etc.; hidden dot-files like `.bashrc`; users own this |
| `/root` | Root user home | The `root` user's home directory — NOT the same as `/` |
| `/dev` | Devices | Device files (`/dev/sda`, `/dev/null`); block devices (hard drives) + character devices (keyboards) |
| `/media` | Removable media | Auto-mounted USB/DVD; managed by desktop env |
| `/mnt` | Manual mount point | Admin-used for temporary mounts (e.g. network share, failing drive) |
| `/proc` | Process/kernel info | Virtual FS — in-memory; shows running processes and `/proc/cpuinfo`, `/proc/meminfo` |
| `/sys` | Kernel/hardware | Virtual FS (sysfs); exposes device/driver/bus info; writable for kernel tuning |
| `/run` | Runtime data | In-memory; cleared on reboot; PID files, sockets; replaced `/var/run` |
| `/tmp` | Temporary files | Apps write here during tasks; cleared on reboot or periodically |
| `/var` | Variable data | Logs (`/var/log`), caches, spool files, package metadata; can grow large → own partition on servers |
| `/srv` | Service data | Content served to remote users (e.g. `/srv/www` for a web server) |
| `/opt` | Optional software | Third-party or manually installed packages not managed by the distro package manager |

## Key distinctions to remember

- `/` vs `/root`: `/` is the system root; `/root` is just the root *user's* home inside `/` [^src1].
- `/dev` vs `/media`: `/dev/sda` is the raw device file; `/media/usb` is where its filesystem is **mounted** and usable [^src1].
- `/proc` and `/sys` are **virtual** — no disk I/O, generated on access by the kernel [^src1].
- `/bin` and `/usr/bin`: historically `/bin` = essential (needed before `/usr` is mounted); `/usr/bin` = everything else. Modern Linux often makes `/bin` a symlink to `/usr/bin` [^src1].
- `/var`: "variable" — this grows over time (logs). On servers, place on a separate partition to prevent the root filesystem from filling up [^src1].

## Config files you'll actually touch

| File | Purpose |
|---|---|
| `/etc/passwd` | User accounts (username, UID, GID, home, shell) — not the passwords |
| `/etc/fstab` | Filesystem mounts at boot |
| `/etc/hosts` | Static hostname→IP mapping |
| `/etc/ssh/sshd_config` | SSH server configuration |
| `/etc/crontab` | System-wide cron entries (see [Cron Scheduling](/mlops/cron-scheduling.md)) |

## Relevance for DevOps/MLOps

> "Knowing the file system is how you troubleshoot a server at 3 AM." [unsourced — verify]

- **Logs are in `/var/log`** — first place to look on a failed service (`journalctl -u myservice` or `tail -f /var/log/syslog`)
- **Config is in `/etc`** — when a service behaves wrong, the culprit is usually here
- **Binaries are in `/usr/bin` or `/usr/local/bin`** — `which python3` tells you which Python the shell finds first
- **Python virtualenvs** often live in `/home/<user>/<project>/.venv` — keep them in `/home`, not in system directories
- **Temporary build artifacts** → `/tmp` (ephemeral); anything you care about → `/var` or `/home`

## See also

- [Linux Commands](/mlops/linux-commands.md) — the 20% of commands for 80% of work
- [Cron Scheduling](/mlops/cron-scheduling.md) — `/etc/cron.*` directories and system crontab
- [VPS for Agents](/mlops/vps-for-agents.md) — VPS Ubuntu filesystem in practice
- [Networking Fundamentals](/mlops/networking-fundamentals.md) — `/etc/hosts`, `/etc/resolv.conf` in network config context
- [MLOps hub](/mlops/README.md)

---

[^src1]: [Linux File System Structure Explained: From / to /usr | Linux Basics (WhiteboardDoodles)](../../raw/youtube/youtube-ISJ44S5sZu8-linux-file-system-structure-explained-from-to-usr-linux-basi.md) — [00:26](../../raw/youtube/youtube-ISJ44S5sZu8-linux-file-system-structure-explained-from-to-usr-linux-basi.md#t=26) 10 categories; [02:10](../../raw/youtube/youtube-ISJ44S5sZu8-linux-file-system-structure-explained-from-to-usr-linux-basi.md#t=130) /bin; [04:23](../../raw/youtube/youtube-ISJ44S5sZu8-linux-file-system-structure-explained-from-to-usr-linux-basi.md#t=263) /usr; [06:36](../../raw/youtube/youtube-ISJ44S5sZu8-linux-file-system-structure-explained-from-to-usr-linux-basi.md#t=396) /etc; [10:29](../../raw/youtube/youtube-ISJ44S5sZu8-linux-file-system-structure-explained-from-to-usr-linux-basi.md#t=629) /proc; [13:59](../../raw/youtube/youtube-ISJ44S5sZu8-linux-file-system-structure-explained-from-to-usr-linux-basi.md#t=839) /var

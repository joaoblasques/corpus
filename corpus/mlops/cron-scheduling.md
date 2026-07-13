---
type: concept
domain: mlops
status: draft
sources:
  - path: raw/web/web-crontab-5-linux-manual-page.md
    channel: web
    ingested_at: 2026-06-25
  - path: raw/web/web-task-scheduler-for-developers-win32-apps.md
    channel: web
    ingested_at: 2026-06-25
aliases:
  - cron
  - crontab
  - cron job
  - cron daemon
  - Task Scheduler
  - scheduled tasks
  - unix scheduler
tags:
  - corpus/mlops
  - concept
created: 2026-06-25
updated: 2026-06-25
---

# Cron Scheduling

**TL;DR** — `cron` is the Unix daemon for time-based job scheduling. A **crontab** file instructs `cron` to run commands at specified times. Each user has their own crontab; commands execute with that user's permissions. On Windows, the equivalent is Task Scheduler (Win32 API). Both are foundational automation primitives; more capable alternatives for complex ML pipelines are DAG orchestrators (Airflow, Prefect) [^src1][^src2].

## Crontab syntax

Each non-empty, non-comment line in a crontab is either an **environment variable setting** or a **cron command** [^src1]:

```
SHELL=/bin/bash
MAILTO=ops@example.com

# ┌────────── minute       (0–59)
# │ ┌────────── hour         (0–23)
# │ │ ┌────────── day of month (1–31)
# │ │ │ ┌────────── month        (1–12 or jan–dec)
# │ │ │ │ ┌────────── day of week  (0–7; 0=Sun=7)
# │ │ │ │ │
# * * * * *   command

# Examples
5 0 * * *       ~/bin/daily.job >> ~/tmp/out 2>&1   # 00:05 daily
15 14 1 * *     ~/bin/monthly                        # 14:15 on the 1st
0 9 * * 1-5     /usr/bin/python3 ~/scripts/report.py  # 09:00 Mon–Fri
30 4 1,15 * 5   backup.sh    # 04:30 on 1st, 15th AND every Friday
```

### Field syntax reference [^src1]

| Syntax | Meaning |
|---|---|
| `*` | every value |
| `5` | exact value |
| `8-11` | range (8, 9, 10, 11) |
| `1,2,5` | list |
| `*/2` | step (every 2 units) |
| `0-23/2` | step over range |
| `6~15` | random within range (randomized at parse time) |

**Important note on day fields**: if both *day-of-month* and *day-of-week* are restricted (neither is `*`), the command runs when **either** matches — not both [^src1]. E.g. `30 4 1,15 * 5` = 04:30 on 1st, 15th, *and* every Friday.

## Environment variables in crontab [^src1]

| Variable | Effect |
|---|---|
| `SHELL` | Shell used to run commands (default `/bin/sh`) |
| `MAILTO` | Email address for job output; `""` disables mail |
| `MAILFROM` | Envelope sender address |
| `CRON_TZ` | Timezone for table entries (log uses local time) |
| `RANDOM_DELAY` | Max minutes of random startup delay per job |

**Gotcha**: DST transitions cause problems — "missing hours" skip scheduled jobs; "repeated hours" run jobs twice. Use UTC in `CRON_TZ` for robustness on critical jobs [^src1].

## Edit and inspect

```bash
crontab -e     # edit current user's crontab (opens $EDITOR)
crontab -l     # list current user's crontab
crontab -r     # remove current user's crontab (destructive!)
crontab -T crontab.txt  # test syntax before installing
sudo crontab -u <user> -e   # edit another user's crontab (root only)
```

## System-level cron directories

Beyond per-user crontabs, Linux has system-wide directories:
- `/etc/cron.daily/` — scripts run daily
- `/etc/cron.hourly/` — hourly
- `/etc/cron.weekly/`, `/etc/cron.monthly/`
- `/etc/cron.d/` — drop-in files with full crontab syntax (include username field)

These are unrelated to a user's crontab and run as root (or as the user specified in the file).

## Practical patterns for ML/DevOps

```bash
# Nightly model retrain at 02:00
0 2 * * *   /home/ml/scripts/retrain.sh >> /var/log/retrain.log 2>&1

# Daily corpus ingest at 08:00 (Python script via uv)
0 8 * * *   cd /home/user/corpus && uv run python bin/scheduled_run.py

# Weekly synthesis every Tuesday at 13:00
0 13 * * 2  cd /home/user/corpus && uv run python bin/weekly_synthesis.py

# Headless Codex CLI run (non-interactive)
0 9 * * 1-5  codex exec "review all PRs in myrepo and commit a status.md"
```

For the `codex exec` pattern, see [tmux](/mlops/tmux.md) and [VPS for Agents](/mlops/vps-for-agents.md).

## Cron vs. alternatives

| Tool | Use case | Complexity |
|---|---|---|
| **cron** | Simple periodic commands | Low — one-liner in crontab |
| **Airflow** | DAG pipelines with dependencies | High — Python DAGs, web UI, workers |
| **Prefect** | Event-driven flows, Python-native | Medium |
| **Kubernetes CronJob** | Container-based periodic tasks | Medium |
| **Task Scheduler (Windows)** | Event-triggered or scheduled tasks | Low–Medium |

Per the *Designing ML Systems* framework: cron handles the simplest tier (§10); schedulers handle condition/dependency aware runs; orchestrators handle resource and compute management [See [Designing ML Systems](/mlops/designing-ml-systems.md) §10].

## Windows Task Scheduler (reference)

The Windows equivalent is the **Task Scheduler** (Win32 API) [^src2]. Triggers include:
- Specific time (daily/weekly/monthly schedules)
- System event, idle state, system boot, user logon
- Terminal Server session state change

APIs: Task Scheduler 2.0 (COM objects for C++ and scripting, Vista+) and 1.0 (C++ only, legacy). Not commonly used in Linux-first ML/DevOps stacks but relevant when deploying on Windows servers.

## See also

- [tmux](/mlops/tmux.md) — `codex exec` + cron as the unattended agent automation pattern
- [VPS for Agents](/mlops/vps-for-agents.md) — the VPS as the host for cron-based agent scheduling
- [Linux Commands](/mlops/linux-commands.md) — shell fundamentals that underpin cron scripts
- [Designing ML Systems](/mlops/designing-ml-systems.md) — Chip Huyen's placement of cron in the MLOps infrastructure stack (Ch 10)
- [MLOps hub](/mlops/README.md)

---

[^src1]: [crontab(5) — Linux manual page](../../raw/web/web-crontab-5-linux-manual-page.md) — field syntax, environment variables, DST note, examples
[^src2]: [Task Scheduler for developers — Win32 apps (Microsoft Docs)](../../raw/web/web-task-scheduler-for-developers-win32-apps.md) — trigger types, API versions

<!-- RELATED:START (generated by bin/corpus_heal.py related — do not edit inside) -->

## Related across domains

- [Python for Data Engineering](/data-engineering/python-for-data-engineering.md) · _data-engineering_

<!-- RELATED:END -->

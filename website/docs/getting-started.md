# Getting Started

Corpus is shaped around a personal setup — one person's accounts, vault, and reading habits. This guide explains the shape of the system so you can wire it to your own. It is not a one-click installer; it is an honest walk-through.

---

## Prerequisites

Before you begin, you will need:

- **Python 3.12+** — the collectors and helper scripts are pure Python.
- **The GitHub CLI (`gh`)** — used for GitHub Stars collection and for pushing commits from unattended jobs.
- **An LLM coding agent** — the corpus layer is driven by an AI agent (the project is built around Claude Code, but the schema is agent-agnostic prose).
- **A knowledge vault** (optional but recommended) — the Obsidian collector expects a local vault with a known folder structure. You can omit this collector if you don't use Obsidian.

---

## Install

```bash
# Clone the repository
git clone https://github.com/your-username/corpus.git
cd corpus

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Authenticate the GitHub CLI so unattended jobs can push commits:

```bash
gh auth login
```

---

## Configure the Collectors

Each collector has its own configuration section in `corpus/_config.md` (the operational config file the agent reads at the start of every session). Edit that file to point each collector at your own accounts and paths.

- **Gmail** — complete the OAuth flow for the Gmail API. The collector reads messages from a set of labeled threads you configure; processed messages are un-labeled and archived automatically.
- **YouTube** — add your playlist IDs to the playlists config. The collector downloads transcripts; rate-limited videos are retried on the next nightly run.
- **PDFs** — specify a Google Drive folder path. Drop PDFs there; the collector picks them up on each run.
- **Obsidian** — set the vault root paths for the note folders you want to drain into the corpus (e.g. an Articles folder, a Study Notes folder). Notes with a `corpus_ingested: true` stamp are skipped automatically.
- **GitHub Stars** — authenticate via `gh auth` (done above); the collector reads your starred repositories and queues any with substantive READMEs.

!!! note "PARA-native paths"
    Obsidian notes under your configured vault paths are ingested *in place* — they are never copied into `raw/`. The agent stamps them and leaves them where they live. Other sources land in `raw/` channel subfolders.

---

## Run Your First Ingest

Start with a manual run so you can watch what happens:

```bash
# Activate the venv if you haven't already
source .venv/bin/activate

# Run a single collector manually (example: YouTube)
python bin/collect_youtube.py

# Then trigger an ingest of whatever landed in the inbox
python bin/ingest.py --max 10
```

The agent will read every new file in `raw/_inbox/`, cluster them by topic, create or update corpus pages, and commit the result. Watch `corpus/_log.md` for the running record of what was touched.

For a full end-to-end test across all collectors:

```bash
python bin/run_all_collectors.py
python bin/ingest.py --max 20
```

---

## Install the Nightly Schedule (Optional)

Once you are satisfied with the manual run, you can install the unattended nightly job. On macOS the project ships a launchd plist; on Linux a cron entry works equally well.

```bash
# macOS — install the launchd job (runs daily at 2 AM)
cp config/com.corpus.nightly.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.corpus.nightly.plist
```

```bash
# Linux — add to crontab
crontab -e
# Add: 0 2 * * * /path/to/corpus/.venv/bin/python /path/to/corpus/bin/run_all_collectors.py && ...
```

!!! note "Subscription auth for unattended runs"
    The launchd/cron environment should not include your metered API key. Remove it from the job's environment so the agent bills the flat-rate subscription instead. See [Under the Hood](under-the-hood.md) for why this matters.

---

## Verify It Is Working

After the first nightly run, check:

```bash
# See what was committed
git log --oneline -5

# Check the operation log
tail -40 corpus/_log.md

# Count pages in the corpus
find corpus -name "*.md" ! -name "_*" | wc -l
```

The log will show one entry per ingest run with counts of sources processed, pages created, and pages updated. If a collector failed, the log entry will note it.

---

!!! warning "This is a personal system"
    Corpus expects your accounts (Gmail OAuth, YouTube API key, Google Drive, GitHub), your vault folder paths, and your domain preferences. Every path and credential in the config is yours to set — there are no shared defaults that will work out of the box. Treat the `corpus/_config.md` file as your personal settings file and edit it before running anything.

---

Next: [The Custodian](the-custodian.md) — the safety harness that keeps unattended runs from going off the rails.

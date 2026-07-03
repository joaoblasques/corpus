---
type: concept
domain: mlops
status: draft
sources:
  - path: raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-build-anything-wi-report.md
    channel: notes
    ingested_at: 2026-06-25
  - path: raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-i-gave-codex-a-24-report.md
    channel: notes
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-z7xyZQVK4Dg-build-anything-with-tmux-here-s-how.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-KqOceMFrMqA-this-is-my-favorite-way-to-secure-a-vps-in-2026.md
    channel: youtube
    ingested_at: 2026-06-25
aliases:
  - VPS agentic engineering
  - cloud agent hosting
  - self-hosted agents
  - Hostinger KVM2
  - remote agent execution
tags:
  - corpus/mlops
  - concept
created: 2026-06-25
updated: 2026-06-25
---

# VPS for Agents

**TL;DR** — Running AI coding agents (Codex CLI, Claude Code) on a **Virtual Private Server** rather than your local machine is the key to: (1) keeping long-running tasks alive without keeping a laptop open, (2) eliminating battery/Wi-Fi dependencies, (3) controlling agents from a phone, and (4) scheduling unattended automations via cron. The persistence layer is [tmux](/mlops/tmux.md) — a detachable terminal multiplexer that keeps sessions alive after SSH disconnect [^src1][^src2].

## Why a VPS instead of local

| Problem with local | VPS solution |
|---|---|
| Closing the laptop kills the agent | Session stays in tmux |
| Wi-Fi outage loses progress | VPS has hardwired data-center connection |
| 8-24hr tasks drain battery | VPS runs 24/7, no battery |
| Laptop must stay awake + unlocked | Detach and walk away |
| Need to be at the laptop | SSH from phone (Termius) |

> "A virtual private server doesn't go to sleep. It's available 24/7 in a secure environment with a hardwired connection." [^src2]

## Recommended spec

**Hostinger KVM2** appears in both sources as the go-to budget option [^src1][^src2]:
- Enough for multiple AI agents in parallel (multiple Codex + Claude Code instances)
- One-click deployment template for OpenAI Codex available on Hostinger
- Select the region closest to you for latency
- 12-24 month plans for maximum discount

Any VPS with a public IP will work; the pattern is provider-agnostic.

## Setup steps

```bash
# 1. SSH in from laptop
ssh root@<vps-ip>

# 2. Verify / install tmux
tmux -v || apt update && apt install tmux -y

# 3. Enable mouse support (non-negotiable)
echo "set -g mouse on" >> ~/.tmux.conf

# 4. Install agents
# Codex CLI (from OpenAI docs one-liner):
curl <openai-codex-install-url> | bash

# Claude Code:
npm install -g @anthropic-ai/claude-code   # or platform equivalent

# 5. Authenticate via device code (uses subscription, not expensive API key)
codex    # → sign in with device code → browse to URL → paste code
claude   # → subscription → authorize

# 6. Wire up GitHub (for PR reviews, commits, repo operations)
apt install gh -y
gh auth login --with-token  # paste a fine-grained PAT

# 7. Create a named tmux session
tmux new -s agents

# 8. Split panes, launch agents
# Ctrl-b % to split, Ctrl-b " to split vertically

# 9. Detach and go
Ctrl-b d   # session stays alive

# 10. Reconnect anytime
ssh root@<vps-ip>
tmux attach -t agents
```

## GitHub fine-grained PAT scope

When creating a PAT for the VPS agent [^src2]:
- **administration**: read-write (only if you need repo creation)
- **contents**: read-write (commits, file edits)
- **pull-requests**: start with read-only; escalate to read-write if auto-approve is needed
- Principle: least privilege — read-only on administration is safer initially

## Scheduling automations with cron

Codex CLI has no built-in scheduler; cron provides it [^src2]:

```bash
# Tell Codex to create the cron job:
codex "Set up a cron job that runs every day and reviews all PRs in <repo>,
       then creates a markdown status file in the repo"

# Codex writes something like:
# crontab -e → adds:
0 9 * * * codex exec "review PRs in <repo> and commit pr-status.md"
```

`codex exec` is the non-interactive headless invocation of Codex CLI — the primitive that makes scheduling and scripting possible [^src2]. Unlike interactive `codex`, it runs the task and exits.

## Phone control

Install **Termius** (iOS/Android) — a free SSH client [^src2]:
1. Add a new host with VPS IP, username `root`, and your root password.
2. SSH in → `tmux attach -t <session>` → full agent control from the phone.
3. Two clients can attach to the same tmux session simultaneously (laptop + phone see the same terminal in real time).

## VPS security: scorched-earth approach (2026)

The recommended security posture for a VPS in 2026 is to **block all inbound traffic** on the public IP, then selectively re-open only what needs to be public [^src3]:

### Step 1 — Block all inbound via UFW (Ubuntu)

```bash
ufw enable   # default: deny all inbound, allow all outbound
```

Before enabling, ensure you have Tailscale configured (step 2), or you'll lock yourself out.

### Step 2 — Private access via Tailscale (WireGuard mesh VPN)

Tailscale creates a **tailnet** — a private mesh network across all your devices using encrypted WireGuard tunnels. The VPS gets a Tailscale IP reachable only within the tailnet [^src3]:

```bash
# On VPS — install and authenticate
curl -fsSL https://tailscale.com/install.sh | sh
tailscale up

# On UFW — allow all ports from tailnet
ufw allow in on tailscale0
```

After enabling: SSH via Tailscale hostname, not public IP. Tailscale personal plan is free up to 100 devices [^src3].

### Step 3 — Public web traffic via Cloudflare Tunnel

For serving web apps publicly without opening inbound ports [^src3]:
- Cloudflare Tunnel opens an **outbound** connection from VPS to Cloudflare
- Users hit Cloudflare → tunnel → your app (Cloudflare acts as reverse proxy)
- Benefits: hides VPS IP, provides WAF (SQL injection, DDoS, bots), auto-TLS, rate limiting
- Configure path-based routing (e.g. `/api/*` → separate service)

```bash
# Install cloudflared on VPS, authenticate, create tunnel, add DNS routes
# All via Cloudflare dashboard (no inbound firewall changes needed)
```

### Step 4 — CI/CD webhooks via Tailscale workload identity

GitHub webhooks no longer work after blocking inbound. Solution: Tailscale workload identity federation + the official Tailscale GitHub Action [^src3]:
- GitHub Actions runner joins your tailnet via ephemeral auth key
- Runner sends API request to Coolify/Dokku deploy service over tailnet
- No public exposure of the deploy service

### Threat model context (2026)

Supply chain attacks and cloud provider breaches (GitHub, Vercel) have risen; "scorched earth" VPS security is described as protective against: port scanners, accidentally exposed databases, zero-day RCEs in web frameworks, and human errors binding private services to public ports [^src3].

## Vibe coder vs. agentic engineer framing

Both sources use a framing dichotomy [^src1]:

| "Vibe coder" | "Agentic engineer" |
|---|---|
| Develops locally on laptop | Runs agents on VPS |
| Loses work if laptop closes | tmux sessions persist |
| Limited by battery/Wi-Fi | VPS is always-on |
| One task at a time | Multiple agents in parallel panes |
| Can't run slash-goal for hours | Agents run 24hrs unattended |

This is a rhetorical framing, not a technical judgment — both approaches have valid use cases. Long-running background tasks and scheduled automations are the clear VPS wins; interactive turn-by-turn work is fine locally [^src2].

## See also

- [tmux](/mlops/tmux.md) — the persistence mechanism (sessions, windows, panes, core commands)
- [Terminal & Shell](/mlops/terminal-and-shell.md) — local shell setup (complementary)
- [CLI Tools](/mlops/cli-tools.md) — other productivity tools in the same layer
- [MLOps hub](/mlops/README.md)

---

[^src3]: [This is my favorite way to secure a VPS in 2026 (Dreams of Code)](../../raw/youtube/youtube-KqOceMFrMqA-this-is-my-favorite-way-to-secure-a-vps-in-2026.md) — [00:26](../../raw/youtube/youtube-KqOceMFrMqA-this-is-my-favorite-way-to-secure-a-vps-in-2026.md#t=26) scorched-earth approach; [04:18](../../raw/youtube/youtube-KqOceMFrMqA-this-is-my-favorite-way-to-secure-a-vps-in-2026.md#t=258) Tailscale setup; [08:09](../../raw/youtube/youtube-KqOceMFrMqA-this-is-my-favorite-way-to-secure-a-vps-in-2026.md#t=489) Cloudflare Tunnel; [13:23](../../raw/youtube/youtube-KqOceMFrMqA-this-is-my-favorite-way-to-secure-a-vps-in-2026.md#t=803) workload identity federation
[^src1]: [Build Anything with Tmux, Here's How (David Ondrej)](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-build-anything-wi-report.md) — [00:35](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-build-anything-wi-report.md#t=00:35) VPS angle introduced; [04:37](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-build-anything-wi-report.md#t=04:37) Hostinger KVM2 setup; [11:03](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-build-anything-wi-report.md#t=11:03) multi-agent in panes; [20:12](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-build-anything-wi-report.md#t=20:12) kill SSH, sessions survive
[^src2]: [I Gave Codex a 24/7 Server — Now It Codes While I Sleep (Tim Ruscica / Tech With Tim)](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-i-gave-codex-a-24-report.md) — [02:42](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-i-gave-codex-a-24-report.md#t=02:42) VPS rationale; [04:05](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-i-gave-codex-a-24-report.md#t=04:05) Hostinger provisioning; [09:18](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-i-gave-codex-a-24-report.md#t=09:18) GitHub wiring; [16:05](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-i-gave-codex-a-24-report.md#t=16:05) Termius phone control; [20:34](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-i-gave-codex-a-24-report.md#t=20:34) cron automations

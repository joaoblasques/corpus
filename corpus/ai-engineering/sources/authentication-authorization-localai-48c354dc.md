---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-authentication-authorization-localai-48c354dc.md
    channel: web
    ingested_at: 2026-07-02
aliases: []
tags:
  - corpus/ai-engineering
  - source
  - doc-quick-intake
created: 2026-07-02
updated: 2026-08-18
provisional: false
url: https://localai.io/features/authentication/index.html
origin: obsidian-list
consolidated_into: ai-engineering/localai.md
---

# "Authentication & Authorization :: LocalAI"

**TL;DR:** LocalAI offers two authentication modes — legacy API key (simple, admin-only) and a full user auth system with roles, OAuth/OIDC, session management, and per-user usage tracking.[^src]

---

## Legacy API Key Authentication

API keys are set via environment variable or CLI flag; clients present them via `Authorization: Bearer <key>`, `x-api-key`, `xi-api-key` headers, or a `token` cookie.[^src]

Legacy API keys grant full admin access — "there is no role separation."[^src] For multi-user deployments requiring role-based access, the user authentication system is preferred.[^src]

Keys can also be managed at runtime through the Runtime Settings interface.[^src]

---

## User Authentication System

Enabled by setting `LOCALAI_AUTH=true` or providing a GitHub/OIDC client ID (which auto-enables auth).[^src]

Features provided:[^src]

- User accounts with email, name, and avatar
- Role-based access control (admin vs. user)
- Session-based authentication with secure cookies
- OAuth login (GitHub) and OIDC SSO (Keycloak, Google, Okta, Authentik, etc.)
- Per-user API keys for programmatic access
- Admin route gating — management endpoints restricted to admins
- Per-user usage tracking with token consumption metrics

### Roles

Two roles exist:[^src]

- **Admin**: full access to all endpoints — model management, backend configuration, system settings, traces, agents, and user management.
- **User**: access to inference endpoints only — chat completions, embeddings, image/video/audio generation, TTS, MCP chat, and their own usage statistics.

The first user to sign in is automatically assigned the admin role; additional users can be promoted via the admin API or `LOCALAI_ADMIN_EMAIL`.[^src]

### Registration Modes

| Mode | Behavior |
|---|---|
| `open` | Anyone registers and is immediately active |
| `approval` (default) | New users land in "pending" until an admin approves; valid invite code skips wait |
| `invite` | Registration requires a valid invite link; without one, registration is rejected |

[^src]

Admins can generate single-use, time-limited invite links from the Users → Invites tab or via API. "Invite codes are single-use — once consumed, they cannot be reused."[^src]

### Disabling Local Authentication

Setting `LOCALAI_DISABLE_LOCAL_AUTH=true` enforces OAuth/OIDC-only login: the login page hides email/password forms, `POST /api/auth/register` returns 403, `POST /api/auth/login` returns 403, while OAuth/OIDC continues to work.[^src]

---

## Key Configuration Variables

| Variable | Default | Purpose |
|---|---|---|
| `LOCALAI_AUTH` | `false` | Enable user auth and authorization |
| `LOCALAI_AUTH_DATABASE_URL` | `{DataPath}/database.db` | SQLite file path or `postgres://...` for PostgreSQL |
| `GITHUB_CLIENT_ID` | — | GitHub OAuth App Client ID; auto-enables auth |
| `LOCALAI_OIDC_ISSUER` | — | OIDC issuer URL for auto-discovery |
| `LOCALAI_OIDC_CLIENT_ID` | — | OIDC Client ID; auto-enables auth |
| `LOCALAI_ADMIN_EMAIL` | — | Email auto-promoted to admin on login |
| `LOCALAI_REGISTRATION_MODE` | `approval` | `open`, `approval`, or `invite` |
| `LOCALAI_DISABLE_LOCAL_AUTH` | `false` | Disable email/password; OAuth/OIDC only |
| `LOCALAI_BASE_URL` | — | Base URL for OAuth callbacks |

[^src]

---

## Storage Note

File-based SQLite relies on POSIX file locking, which is unreliable over network filesystems (SMB/CIFS/NFS). On such storage the auth DB can fail with `database is locked`.[^src] Use PostgreSQL (`LOCALAI_AUTH_DATABASE_URL=postgres://...`) when the data directory lives on shared or network storage.[^src]

---

## Admin-Only Endpoints

When auth is enabled, management endpoints require admin role, including:[^src]

- Model & backend management (`/api/models`, `/api/backends`, `/api/operations`)
- System & monitoring (`/api/traces`, `/api/backend-logs`, `/api/resources`, `/api/settings`)
- Gallery, jobs, and agent management routes

Inference endpoints remain accessible to the `user` role.[^src]

---

[^src]: [Authentication & Authorization :: LocalAI](https://localai.io/features/authentication/index.html) — `raw/web/web-authentication-authorization-localai-48c354dc.md`, collected 2026-06-28.

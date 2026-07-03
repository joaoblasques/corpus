---
type: concept
domain: mlops
status: draft
sources:
  - path: raw/email/email-2026-06-15-the-31b-market-you-re-already-training-for.md
    channel: email
    ingested_at: 2026-06-20
  - path: raw/youtube/youtube-7Jja20nWcqo-stop-using-tailscale-use-open-source-instead.md
    channel: youtube
    ingested_at: 2026-06-20
  - path: raw/youtube/youtube-w0SQGCt-6Ro-networking-concepts-every-devops-engineer-must-know.md
    channel: youtube
    ingested_at: 2026-06-20
aliases:
  - networking fundamentals
  - containers
  - container networking
  - Headscale
  - Tailscale
  - VPN mesh
  - WireGuard
  - VPC
  - DNS
tags:
  - corpus/mlops
  - concept
created: 2026-06-20
updated: 2026-06-23
---

# Networking Fundamentals (for DevOps/MLOps)

**TL;DR**: DevOps engineers encounter networking across four layers — physical/VM networking, container networking, VPC/cloud networking, and secure mesh VPNs. Containers solve the dependency-isolation problem; mesh VPN tools (Tailscale/Headscale, WireGuard) solve the secure remote-access problem.

## Containers — what they are and why

When software runs on a server, it needs a runtime, libraries, and system settings. Before containers, multiple apps sharing a server led to version conflicts, "it works on my machine" bugs, and fragile manual fixes [^src1].

**Analogy**: A carpenter (the application) needs tools (dependencies). Instead of hoping every construction site has the right tools, give the carpenter a toolbox-in-a-van — a container — that travels with the application everywhere [^src1].

A **container** packages software together with everything it needs. It runs identically on a laptop, data center, or cloud — as long as a container runtime (Docker, containerd) is available [^src1].

### Why containers matter for ML/data engineering
- Reproducible training environments: same image = same results.
- Deploy trained models as containerized services (Flask/FastAPI in Docker → Kubernetes).
- Dependency isolation between projects (no Python version conflicts).
- CI/CD pipelines use containers to ensure test environment matches production.

## Networking concepts (DevOps layer)

The networking evolution for a DevOps engineer [^src2]:

| Layer | Concepts |
|---|---|
| **Physical → VM** | VLANs, NIC cards, physical switches; VMs add virtual NICs and virtual switches |
| **Container** | Each container gets a virtual NIC; Docker bridge networking; port mapping (`-p 8080:80`) |
| **Cloud (VPC)** | Virtual Private Cloud: subnets (public/private), security groups, NAT gateway, internet gateway |
| **Service mesh** | Kubernetes pod networking; CNI plugins; service discovery via DNS |

Key primitives every DevOps engineer needs [^src2]:
- **IP addressing**: IPv4 CIDR notation, subnets, private ranges (`10.x`, `192.168.x`, `172.16-31.x`)
- **DNS**: resolves hostnames to IPs; in Kubernetes, CoreDNS resolves service names within cluster
- **NAT**: allows private-subnet instances to reach the internet; source NAT on egress
- **Load balancer**: distributes traffic across instances; L4 (TCP/IP) vs L7 (HTTP/HTTPS)
- **Security groups / firewalls**: stateful packet filtering on inbound/outbound rules

## Mesh VPN: Tailscale vs Headscale

Tailscale is a managed mesh VPN built on **WireGuard** — a modern, fast, cryptographically simple VPN protocol [^src3]. It creates a zero-config peer-to-peer encrypted network (a "tailnet") across any mix of devices without a central server per se.

**The tradeoff**: Tailscale uses its own hosted coordination server to relay encrypted connection metadata. For teams that require full control (compliance, self-hosting, no external dependency), **Headscale** solves this [^src3].

### Headscale — open-source Tailscale control plane

Headscale is a self-hosted, open-source reimplementation of the Tailscale coordination server [^src3]:

- Drop-in compatible with the official Tailscale clients.
- Deployed on a VPS or self-hosted server; clients register against it instead of `login.tailscale.com`.
- Full data sovereignty: zero metadata leaves your infrastructure.
- Use cases: private ML training clusters, homelab networking, enterprise with strict data residency.

**Setup** (simplified):
1. Deploy Headscale on a public-facing server.
2. Configure each device's Tailscale client to point to your Headscale server.
3. Devices form a WireGuard mesh; the coordination server manages key exchange, no routing of data traffic.

### WireGuard

The underlying protocol for both Tailscale and Headscale [^src3]:
- ~4,000 lines of code (vs OpenVPN's ~100,000) — smaller attack surface.
- Uses modern cryptography: Curve25519 keys, ChaCha20-Poly1305.
- Kernel-level integration for performance; available in Linux, macOS, Windows, iOS, Android.
- Persistent keys: each device has a public/private keypair; peers exchange public keys.

## See also

- [Dev Environment Stack](/mlops/dev-environment-stack.md) — the local layer under container networking
- [Cloud Computing Fundamentals](/mlops/cloud-computing-fundamentals.md) — VPC, subnets, load balancing
- [Infrastructure as Code](/mlops/infrastructure-as-code.md) — provisioning the network layer
- [Terraform](/mlops/terraform.md) — its Docker-provider example declaratively provisions the container bridge network described here (a dedicated Docker network so containers resolve each other by hostname)
- [Microservices](/software-engineering/microservices.md) — container orchestration (Kubernetes)
- [MLOps hub](/mlops/README.md)

---

[^src1]: [The $31B Market You're Already Training For (KubeCraft)](../../raw/email/email-2026-06-15-the-31b-market-you-re-already-training-for.md) — containers intro
[^src2]: [Networking Concepts Every DevOps Engineer Must Know](../../raw/youtube/youtube-w0SQGCt-6Ro-networking-concepts-every-devops-engineer-must-know.md) — YouTube playlist: Devops
[^src3]: [Stop Using Tailscale — Use Open Source Instead](../../raw/youtube/youtube-7Jja20nWcqo-stop-using-tailscale-use-open-source-instead.md) — YouTube playlist: Devops (Headscale/WireGuard)

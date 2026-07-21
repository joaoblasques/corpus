---
type: synthesis
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-agents-need-their-own-computer-here-s-how-to-give-them-one-s-4934c442.md
    channel: web
    ingested_at: 2026-07-21
  - path: raw/web/web-a-quote-from-thibault-sottiaux-b62b68c9.md
    channel: web
    ingested_at: 2026-07-21
  - path: raw/web/github-mattpocock-sandcastle-orchestrate-sandboxed-coding-ag.md
    channel: web
    ingested_at: 2026-06-16
  - path: raw/web/web-self-hosted-sandboxes.md
    channel: web
    ingested_at: 2026-06-25
aliases:
  - agent execution isolation
  - agent sandbox
  - agent sandboxing
  - sandbox isolation tiers
  - microVM isolation
  - agent computer
  - execution isolation
tags:
  - corpus/ai-engineering
  - synthesis
created: 2026-07-21
updated: 2026-07-21
confidence: 0.8
last_confirmed: 2026-07-21
---

# Agent Execution Isolation

**TL;DR**: An agent that can only emit text cannot verify its own work, so useful agents get a real environment — filesystem, shell, package manager, network [^langchain]. That environment is where the security question lands: model-generated code reaches execution with no human review step in between [^langchain]. Sources agree isolation is required and disagree on *how strong* it must be — whether a shared-kernel container suffices, or only hardware virtualization does. This page names that disagreement rather than resolving it (§7).

## Why agents need a computer at all

The functional argument is about verification, not convenience. A model that suggests a fix "has no way to know if the fix works" [^langchain]; giving it execution closes the loop — a coding agent can clone a repo, run the test suite, read failures, patch, and hand back a diff already verified to pass [^langchain]. This is the same brain/hands split documented on [Long-Running Agents](/ai-engineering/long-running-agents.md), where the Hands are explicitly sandboxed ephemeral execution.

Scale changes the problem shape: one developer has one laptop, but an agent platform may spin up thousands of environments in parallel, "each one needing to be isolated, disposable, and safe to hand real execution power to" [^langchain].

## The threat model: code with no review step

The distinguishing property of agent execution is provenance. Agent-executed code can originate from the model itself, from a cloned repo, or from a package installed mid-run — it is "generated seconds before it runs, shaped directly by whatever a user typed" [^langchain]. There is no review gate between generation and execution, so the source argues all of it should be treated as untrusted by default regardless of origin [^langchain].

**A concrete failure confirms the model-error limb.** OpenAI's Thibault Sottiaux, describing a GPT-5.6 Codex bug, reported unexpected file deletions occurring when full-access mode ran *without* sandboxing protections, the model attempted to override `$HOME` to point at a temporary directory, and then "makes an honest mistake and mistakenly deletes $HOME instead" [^sottiaux]. This is worth reading precisely: the harm needed no adversary. Isolation here defends against ordinary model error, not just [prompt injection](/ai-engineering/agent-security.md) — which is the usual framing and an incomplete one.

## The disagreement: is a container enough?

Two corpus sources take materially different positions on the minimum isolation tier.

**Containers are insufficient** — LangChain argues "a standard container boundary wasn't designed to hold untrusted, model-generated execution," and that each workspace should be "a hardware-virtualized machine with its own kernel, filesystem, and network boundary" [^langchain]. The supporting evidence is kernel-sharing: a 2026 Linux kernel CVE could reportedly root any major distribution in about an hour, and "containers couldn't help, because they shared a kernel with the host" [^langchain].

**Containers are a legitimate tier** — [Sandcastle](/ai-engineering/sandcastle.md) ships Docker and Podman bind-mount providers as first-class sandbox backends alongside Firecracker microVMs, treating the choice as a provider swap rather than a security floor [^sandcastle].

**Assessment.** The positions are less opposed than they first appear, because they scope differently. LangChain supplies its own boundary condition: for agents that "only call APIs and executes no dynamic code, local or containerized execution is likely fine," while agents that execute model-generated code, install packages, or process arbitrary files "need real isolation" [^langchain]. Sandcastle's use case — a developer parallelizing their own coding agents on their own machine, where the code being run is code they were going to run anyway — sits nearer the first case. The unresolved part is genuine, though: Sandcastle's `noSandbox()` provider runs the agent directly on the host with no container isolation [^sandcastle], which is exactly the configuration implicated in the Codex deletion incident [^sottiaux]. Neither source is treated here as settling the question; commercial interest points in opposite directions (LangChain sells a managed sandbox; Sandcastle is an open library), which is itself a reason to weight the technical claim — kernel sharing — above either framing.

## What isolation is supposed to provide

Beyond execution safety, the LangChain source enumerates three further requirements [^langchain]:

- **Control** — credential injection at the network layer via an outbound proxy, so the agent makes authenticated calls "without ever seeing the token"; plus CPU/memory caps and network allowlists as a per-task cost ceiling. This is the same credential-brokering pattern documented on [Agent Security](/ai-engineering/agent-security.md) from the Vercel and Cloudflare implementations — three independent vendors converging on network-layer injection is meaningful corroboration.
- **Observability** — an audit log of which commands ran, which files changed, which network calls went out, which packages were installed. Reliability comes from being able to "re-run from a known state, compare branches, and trace what actually happened" [^langchain].
- **Speed and reproducibility** — sub-second warm provisioning, image-defined environments, state persisting across agent turns.

Snapshot-and-fork is the notable primitive: copy-on-write forks mean "spinning up ten parallel branches from the same snapshot costs roughly the same as one," and a wrong path can be restored rather than restarted [^langchain]. That property is what makes speculative multi-branch agent work economically viable, connecting this page to [Multi-Agent Systems](/ai-engineering/multi-agent-systems.md).

## Isolation does not contain injection

The most important caveat, and one the source states against its own product interest: sandboxes "don't change a fundamental property of language models: anything the agent reads can influence what the agent does next" [^langchain]. Malicious code confined to a sandbox cannot reach the host, but if its *output* is read back into the model's context, an injected instruction still steers downstream behavior [^langchain].

Recommended mitigations [^langchain] — treat sandbox output as untrusted data; use a "non-agentic read" pattern where a non-model process retrieves the finished artifact rather than routing raw output through the agent's context; apply least-privilege on any local surface a cross-boundary agent touches; validate at the boundary with schemas or classifiers. And explicitly: "Don't rely on prompting the model to detect or ignore injections," which adversarial research shows is insufficient at scale [^langchain].

This *corroborates* the defense-in-depth framing already on [Agent Security](/ai-engineering/agent-security.md): execution isolation is one layer and does not substitute for the others. Isolation contains blast radius; it does not contain persuasion.

## Related pages

- [Agent Security](/ai-engineering/agent-security.md) — the parent security page; self-hosted sandboxes, credential brokering, and the lethal trifecta live there. This page depends-on its threat vocabulary.
- [Sandcastle](/ai-engineering/sandcastle.md) — a concrete library implementing the provider-swap model discussed above.
- [Long-Running Agents](/ai-engineering/long-running-agents.md) — the brain/hands/session architecture that isolation implements.
- [VPS for Agents](/mlops/vps-for-agents.md) — the self-hosted analogue: a dedicated remote machine as the agent's computer (cross-domain → mlops).
- [Claude Managed Agents](/ai-engineering/claude-managed-agents.md) — Anthropic's self-hosted-sandbox model, where execution stays inside the customer trust boundary [^selfhosted].
- [Agent Harness](/ai-engineering/agent-harness.md) — where confirmation gates and approval callbacks sit relative to the sandbox boundary.

[^langchain]: [Agents need their own computer. Here's how to give them one safely.](../../raw/web/web-agents-need-their-own-computer-here-s-how-to-give-them-one-s-4934c442.md) — LangChain blog, collected 2026-07-16
[^sottiaux]: [A quote from Thibault Sottiaux](../../raw/web/web-a-quote-from-thibault-sottiaux-b62b68c9.md) — via Simon Willison's Weblog, 16 Jul 2026
[^sandcastle]: [Sandcastle — orchestrate sandboxed coding agents](../../raw/web/github-mattpocock-sandcastle-orchestrate-sandboxed-coding-ag.md) — Matt Pocock
[^selfhosted]: [Self-hosted sandboxes for Managed Agents](../../raw/web/web-self-hosted-sandboxes.md) — Anthropic

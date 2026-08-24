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
  - path: raw/_inbox/web-how-deep-agents-run-untrusted-code-without-a-sandbox-631cdcf9.md
    channel: web
    ingested_at: 2026-08-24
aliases:
  - agent execution isolation
  - agent sandbox
  - agent sandboxing
  - sandbox isolation tiers
  - microVM isolation
  - agent computer
  - execution isolation
  - WASM isolation
  - QuickJS WASM
  - code interpreter isolation
  - capability isolation
  - durable pauses
  - additive capability model
  - subtractive capability model
  - Meta rule of two
  - rule of two
tags:
  - corpus/ai-engineering
  - synthesis
created: 2026-07-21
updated: 2026-08-24
confidence: 0.82
last_confirmed: 2026-08-24
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

## In-process isolation: WASM + QuickJS (additive capability model)

LangChain Deep Agents describes a second isolation model alongside the remote-container/microVM approach: an **in-process interpreter isolated by WebAssembly** [^deepagents]. This is not a sandbox in the traditional sense — it is closer to a capability-constrained runtime, and the security model is fundamentally different.

**The three design requirements** [^deepagents]:
1. **Execution isolation** — agent-written code cannot compromise the host process
2. **Capability isolation** — the agent can only touch data and actions deliberately handed to it
3. **Durable pauses** — execution can stop for human approval and resume without losing state

### Execution isolation via WebAssembly

WASM is a compact binary format executing inside a sandboxed in-process VM with its own separate linear memory. Code inside WASM cannot dereference host process pointers — it cannot read or corrupt memory it was not handed. CPU/memory limits are straightforward to enforce; instrumentation is possible without standing up a separate machine [^deepagents].

Used for untrusted code isolation by: AWS, Shopify, Figma, WebContainers, wasmtime [^deepagents].

### QuickJS as the in-WASM runtime

QuickJS is a small, fast, ECMA-compliant JavaScript engine written in C that compiles cleanly to WASM — so the engine itself sits behind the WASM boundary [^deepagents]. JavaScript is a natural fit for orchestration scripts agents write: expressive enough, no compile step required.

**Key packages** (experimental as of 2026) [^deepagents]:
- `quickjs-rs` — the runtime and Python bindings for running QuickJS through WASM
- `langchain-quickjs` — Deep Agents middleware built on quickjs-rs

### Capability isolation: additive vs subtractive

The critical architectural difference between an interpreter and a traditional sandbox [^deepagents]:

| Model | Starting state | Security work |
|---|---|---|
| **Sandbox (subtractive)** | Computer-shaped (filesystem, shell, dependencies) | Clawing back capabilities — begins with broad access |
| **Code interpreter (additive)** | Nothing — no file reads, no network, no package install | Adding only what is deliberately bridged in |

Out of the box the QuickJS interpreter can only use language primitives (variables, functions, loops). Every capability beyond that — calling a subagent, reading a file — must be explicitly bridged in through the harness. The harness sets limits: max concurrent subagents per call, max spawned total [^deepagents].

### Meta's rule of two

The capability isolation design is anchored to Meta's rule of two: until prompt injection is solved, an agent should be able to do no more than **two** of the following simultaneously [^deepagents]:
- Access sensitive data
- Be exposed to untrusted content
- Change state or communicate externally

The wedding-planner scenario illustrates the risk: an agent that reads sensitive budget data AND processes external RSVPs AND emails vendors satisfies all three. A single hostile RSVP can read the private budget and email a vendor "approved" changes [^deepagents]. Capability bridging enforces this constraint mechanically.

### Durable pauses via LangGraph state serialization

Because QuickJS runs inside WASM, the interpreter state can be serialized — the entire linear memory snapshot — and stored in LangGraph state [^deepagents]. On resume, the harness restores the snapshot and feeds the result back into the call that was waiting. From the program's perspective: an async call that took arbitrarily long to return. Human-in-the-loop approval with a multi-day wait time becomes just an async pause.

**Contrast with the remote-container model** (§disagreement above): a container sandbox provides a full OS surface; the WASM/QuickJS interpreter provides only what was explicitly bridged. Neither is strictly stronger — they address different threat surfaces. The container is better for agents that need genuine OS access; the interpreter is better for orchestration scripts that should be constrained to a narrow capability surface.

## Related pages

- [Agent Security](/ai-engineering/agent-security.md) — the parent security page; self-hosted sandboxes, credential brokering, and the lethal trifecta live there. This page depends-on its threat vocabulary.
- [Sandcastle](/ai-engineering/sandcastle.md) — a concrete library implementing the provider-swap model discussed above.
- [Long-Running Agents](/ai-engineering/long-running-agents.md) — the brain/hands/session architecture that isolation implements.
- [VPS for Agents](/mlops/vps-for-agents.md) — the self-hosted analogue: a dedicated remote machine as the agent's computer (cross-domain → mlops).
- [Claude Managed Agents](/ai-engineering/claude-managed-agents.md) — Anthropic's self-hosted-sandbox model, where execution stays inside the customer trust boundary [^selfhosted].
- [Agent Harness](/ai-engineering/agent-harness.md) — where confirmation gates and approval callbacks sit relative to the sandbox boundary.
- [Multi-Agent Systems](/ai-engineering/multi-agent-systems.md) — dynamic subagents are the capability that the WASM interpreter unlocks at the orchestration level.

[^langchain]: [Agents need their own computer. Here's how to give them one safely.](../../raw/web/web-agents-need-their-own-computer-here-s-how-to-give-them-one-s-4934c442.md) — LangChain blog, collected 2026-07-16
[^sottiaux]: [A quote from Thibault Sottiaux](../../raw/web/web-a-quote-from-thibault-sottiaux-b62b68c9.md) — via Simon Willison's Weblog, 16 Jul 2026
[^sandcastle]: [Sandcastle — orchestrate sandboxed coding agents](../../raw/web/github-mattpocock-sandcastle-orchestrate-sandboxed-coding-ag.md) — Matt Pocock
[^selfhosted]: [Self-hosted sandboxes for Managed Agents](../../raw/web/web-self-hosted-sandboxes.md) — Anthropic
[^deepagents]: [How Deep Agents Run Untrusted Code Without a Sandbox](../../raw/web/web-how-deep-agents-run-untrusted-code-without-a-sandbox-631cdcf9.md) — LangChain blog, collected 2026-07-01; WASM execution isolation, QuickJS interpreter, additive capability model, Meta's rule of two, durable pauses via LangGraph state serialization

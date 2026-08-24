---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/web-what-does-nvidia-s-vera-cpu-actually-do-387fc690.md
    channel: web
    ingested_at: 2026-08-24
aliases:
  - NVIDIA Vera CPU
  - Vera CPU
  - Vera Rubin platform
  - Olympus Arm cores
  - NVIDIA agentic hardware
tags:
  - corpus/ai-engineering
created: 2026-08-24
updated: 2026-08-24
---

# NVIDIA Vera CPU: What Agentic AI Did to Hardware Architecture

**TL;DR**: Vera is NVIDIA's first data-center CPU built on its own custom cores (88 Olympus Arm cores), designed to solve a specific problem agentic workloads exposed: an agent spends most of its execution time on CPU work (tool calls, code execution, data pipelines), leaving costly GPUs idle between reasoning steps. Vera's 1.8 TB/s coherent link to Rubin GPUs — double Grace's 900 GB/s — is the key innovation [^src1].

## What agentic AI broke in hardware

Training-era workloads kept GPUs busy: the same matrix multiplication runs over and over. The CPU was an afterthought [^src1].

Agentic workloads broke that balance. An agent loops: think (GPU) → call a tool (CPU) → read the result (CPU) → run code in a sandbox (CPU) → think again (GPU). The model's turn on the GPU is brief; everything else runs on the CPU. Per an NVIDIA executive: "Agents don't operate on GPUs alone. They need CPUs... for tool calling, SQL queries and the compilation of code." [^src1]

AMD stated the same position in March 2026: the CPU does "the critical system work that keeps accelerators productive." Two firms with competing chips agreeing on where the bottleneck sits is notable [^src1].

## Vera vs Grace: the upgrade

| Dimension | Grace (2023) | Vera |
|---|---|---|
| Cores | 72 Arm Neoverse V2 (licensed) | 88 custom Olympus (NVIDIA-designed) |
| Memory ceiling | 480 GB | 1.5 TB (3×) |
| Memory bandwidth | 512 GB/s | 1.2 TB/s (2.3×) |
| CPU→GPU link | 900 GB/s (NVLink-C2C gen 1) | 1.8 TB/s (NVLink-C2C gen 2, coherent) |
| Core per-speed | baseline | ~1.5× Grace |

NVIDIA chose to design its own Olympus core because licensing Arm's cores meant it "could not tune what matters most for orchestration: how the cores work, how much fast memory sits next to them, how they juggle many small tasks at once." [^src1]

All 88 Olympus cores sit on one piece of silicon (no chiplet multi-die assembly), ensuring every core sits the same distance from memory — uniform latency across cores. For agent workloads, where the entire loop waits on the slowest step, that uniform speed is structurally important [^src1].

## The coherent link advantage

On a standard server, CPU passes data to GPU across PCIe with a copy-and-wait handoff. Vera's NVLink-C2C link at 1.8 TB/s is **coherent**: CPU and GPU share the same memory address space; the GPU reads agent data in place without a copy, eliminating that round-trip dead time [^src1].

For agent workloads with many short GPU bursts, the per-step handoff latency compounds across thousands of steps per minute — the coherent link eliminates that accumulation.

## Market and adoption

- **Users**: Meta, Oracle, ByteDance, CoreWeave (heavy agentic and inference workloads) [^src1].
- **Distribution**: sold only inside NVIDIA Vera Rubin racks, never as a standalone socketed chip — "the 1.8 TB/s link only exists when both ends are NVIDIA chips" [^src1].
- **CPU-only rack**: 256 Vera CPUs in one liquid-cooled box (22,500+ cores). Targets workloads where agent orchestration and tool execution never touch a GPU [^src1].
- **Entry**: most practitioners will access Vera by renting Vera Rubin instances from cloud providers, identical to how H100s are rented today [^src1].

## Lock-in tradeoff

Vera is explicitly a lock-in play: "You cannot buy a Vera and drop it into your own server the way you can a Xeon or an EPYC. It ships inside NVIDIA's racks... because the 1.8 TB/s link only exists when both ends are NVIDIA chips." [^src1]

The value proposition is narrow and direct: if your agentic workload lives next to NVIDIA GPUs and the CPU side is the bottleneck, Vera's coherent link has no equivalent. If the workload does not touch NVIDIA GPUs, generic Arm server CPUs (Amazon Graviton, Ampere) deliver equivalent general compute at lower cost [^src1].

## Architectural implication for agent system design

The Vera CPU is hardware evidence of the thesis in [Long-Running Agents](/ai-engineering/long-running-agents.md): agentic execution has a different compute profile than inference. The Brain-Hands-Session split (model loop vs. execution sandbox vs. durable log) maps directly onto the Vera design: the GPU handles "Brain" (model reasoning); the CPU handles "Hands" (tool execution, code, data prep). The 1.8 TB/s link is the fast handoff between those two roles that enables continuous high-throughput agent operation [^src1].

## See also

- [Long-Running Agents](/ai-engineering/long-running-agents.md) — Brain-Hands-Session split; the hardware design mirrors the software architecture
- [Agent Harness](/ai-engineering/agent-harness.md) — harness orchestrates the CPU-heavy work (tool calls, hooks, sandbox execution) that Vera targets
- [AI Agent](/ai-engineering/ai-agent.md) — the Perceive/Reason/Act/Learn loop that makes CPU work dominant in agentic systems

---

[^src1]: [What Does NVIDIA's Vera CPU Actually Do?](../../../raw/web/web-what-does-nvidia-s-vera-cpu-actually-do-387fc690.md) — The AI Engineer (Substack), 2026-07-01; 88 Olympus cores, 1.8 TB/s NVLink-C2C, GPU/CPU balance in agentic workloads, Meta/Oracle/ByteDance/CoreWeave adoption

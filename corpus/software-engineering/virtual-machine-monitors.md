---
type: concept
domain: software-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-vmm-intro.md
    channel: pdf
    ingested_at: 2026-07-10
  - path: raw/_inbox/pdf-dialogue-vmm.md
    channel: pdf
    ingested_at: 2026-07-10
aliases:
  - VMM
  - hypervisor
  - virtual machine monitor
  - Type 1 hypervisor
  - Type 2 hypervisor
  - para-virtualization
  - Disco
  - VMware
  - machine memory
tags:
  - corpus/software-engineering
  - concept
created: 2026-07-10
updated: 2026-07-10
---

# Virtual Machine Monitors (VMMs / Hypervisors)

TL;DR: A VMM (Virtual Machine Monitor, also called a hypervisor) sits between one or more operating systems and the physical hardware, giving each OS the illusion that it controls the machine exclusively. The core technique extends limited direct execution: the VMM intercepts privileged operations (system calls, TLB updates, page-table installs) and re-dispatches them with the correct level of indirection, adding virtual-to-machine address translation on top of the OS's virtual-to-physical translation.

## What is a VMM?

A **virtual machine monitor** sits between the hardware and one or more guest operating systems, transparently multiplexing the physical hardware among them [^src1]. IBM introduced the idea in the 1960s to allow a single expensive mainframe to run multiple operating systems simultaneously [^src1].

The VMM is essentially an operating system for operating systems, but it exposes the same hardware abstraction the OS is used to interacting with (rather than a higher-level API). **Transparency** is the key requirement: the guest OS must believe it is controlling real hardware [^src1].

Modern use cases [^src1]:
- **Server consolidation**: run multiple lightly-loaded OS instances on fewer physical machines.
- **Desktop cross-platform access**: run Windows applications on a Mac or Linux host.
- **Testing and debugging**: spin up many OS versions on a single development machine.

The modern revival of VMMs was led by Mendel Rosenblum's group at Stanford, whose **Disco** project (for MIPS) directly led to the founding of **VMware** in 1998 [^src1].

## CPU Virtualization

The VMM uses **limited direct execution**: the guest OS and its applications run directly on the hardware most of the time [^src1]. The VMM only intervenes at privileged boundaries.

**Machine switch**: analogous to a process context switch, the VMM switches between running virtual machines by saving the entire machine state of one VM (registers, PC, privileged hardware state) and restoring another's [^src1].

**Privilege problem**: the guest OS cannot run in kernel mode (that would give it direct hardware control, defeating the VMM). Instead, the guest OS runs at a reduced privilege level. On MIPS, the **supervisor mode** was a natural fit; on x86, software tricks or later hardware extensions handle this [^src1].

**Intercepting privileged operations**: when the guest OS tries to perform a privileged instruction (e.g., install a trap handler, update the TLB), the hardware traps into the VMM instead. The VMM records what the OS is attempting (e.g., "this OS wants its trap handler at address X") and then either performs the real privileged operation itself or re-dispatches to the appropriate handler [^src1].

**System call flow with virtualization** (compared to without):
1. User process executes a trap instruction.
2. VMM trap handler runs (in kernel mode) — the VMM was the privileged entity that set up the trap table.
3. VMM calls the guest OS's trap handler at reduced privilege.
4. Guest OS handles the system call; issues return-from-trap (privileged).
5. VMM intercepts the return-from-trap; performs the real return-from-trap.
6. User process resumes [^src1].

The extra indirection adds overhead, but the OS and application perceive no semantic difference.

## Memory Virtualization

The VMM adds a third layer of address translation on top of the OS's virtual-to-physical mapping [^src1]:

```
Virtual Address  →(OS page table)→  "Physical" Address
"Physical" Address →(VMM page table)→  Machine Address
```

The OS believes it controls physical memory (a linear array of pages). The VMM further remaps what the OS calls "physical" frames to the true **machine frames** [^src1].

**Software-managed TLB systems (MIPS)**: on a TLB miss, the hardware traps into the VMM. The VMM calls the OS TLB miss handler at reduced privilege. The OS tries to install a VPN→PFN mapping in the TLB (a privileged operation) — which traps back into the VMM. The VMM installs a VPN→MFN mapping instead (substituting machine frame numbers for physical frame numbers) [^src1].

This double-trap sequence is expensive. The Disco VMM added a **VMM-level software TLB**: it caches every VPN→MFN mapping it has seen, so on subsequent TLB misses for the same VPN it can install the hardware TLB entry directly without calling into the OS [^src1].

**Hardware-managed TLB systems (x86)**: the hardware walks the page table on a miss without OS involvement. The VMM must maintain a **shadow page table** that maps virtual addresses directly to machine frames. The VMM monitors changes the OS makes to its page table and keeps the shadow table synchronized; the hardware uses the shadow table for all TLB fills [^src1].

## The Information Gap

A fundamental problem: the VMM does not know what the guest OS is actually trying to accomplish [^src1].

Examples:
- **Idle loop**: an OS with nothing to run spins in a `while(1);` loop. The VMM can't know it should give CPU time to another VM unless it detects the idle pattern (e.g., by inferring from the OS entering a low-power state).
- **Double zeroing**: both the VMM and the guest OS zero pages before use (for security). A page gets zeroed twice unnecessarily. The Disco team solved this by modifying the guest OS (IRIX) to skip zeroing pages it detected the VMM had already zeroed — an early example of **para-virtualization** [^src1].

**Para-virtualization**: deliberately modifying the guest OS to cooperate with the VMM. Enables near-native performance but requires OS changes and reduces transparency [^src1].

**Implicit information**: the VMM can infer OS intent without explicit API changes by observing patterns in privileged operation sequences [^src1].

## Hardware Support for Virtualization

Later Intel and AMD processors added hardware virtualization extensions (Intel VT-x, AMD-V) that provide a dedicated "ring -1" privilege level for the VMM, native nested page tables (EPT/NPT) that implement VMM-level address translation in hardware, and hardware ASID support for TLBs. These extensions eliminate many of the software tricks described above [^src1].

## Related Corpus Pages

- [/software-engineering/operating-systems.md](/software-engineering/operating-systems.md) — limited direct execution; trap handlers; context switches; the OS mechanisms VMMs must replicate
- [/software-engineering/virtual-memory.md](/software-engineering/virtual-memory.md) — paging, TLBs, and page tables that VMMs must virtualize at a second level
- [/software-engineering/sources/ostep-operating-systems-three-easy-pieces.md](/software-engineering/sources/ostep-operating-systems-three-easy-pieces.md) — OSTEP source summary

---

[^src1]: [OSTEP Appendix B: Virtual Machine Monitors](../../raw/_inbox/pdf-vmm-intro.md)

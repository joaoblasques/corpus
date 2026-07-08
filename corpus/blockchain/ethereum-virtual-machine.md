---
type: concept
domain: blockchain
status: draft
sources:
  - path: raw/_inbox/book-mastering-ethereum-06-chapter-14-the-ethereum-virtual-machine.md
    channel: book
    ingested_at: 2026-07-08
aliases:
  - EVM
  - Ethereum Virtual Machine
  - EVM bytecode
  - EVM opcodes
  - ABI encoding
tags:
  - corpus/blockchain
  - concept
created: 2026-07-08
updated: 2026-07-08
---

# Ethereum Virtual Machine (EVM)

TL;DR: The EVM is a quasi-Turing-complete, stack-based state machine that executes smart contract bytecode across all Ethereum nodes identically. Gas limits replace the halting problem. A 256-bit word size, four memory regions (code ROM, volatile memory, transient storage, permanent storage), and a fixed opcode set define its execution model. The EVM is the de facto standard VM for blockchain development — most L1s and L2s maintain EVM compatibility.

## What Is the EVM?

"The EVM is the part of Ethereum that handles smart contract deployment and execution" [^src1]. Simple ETH transfers do not invoke it; all state changes involving smart contracts do.

At a high level, "the EVM running on the Ethereum blockchain can be thought of as a global decentralized computer containing millions of executable objects, each with its own permanent data store" [^src1].

### Quasi-Turing-Complete

The EVM is *quasi*-Turing-complete: all execution is limited by the gas available. This "solves" the halting problem — programs cannot run forever because they will exhaust gas and abort [^src1]. Without this constraint, a malicious contract could halt the entire Ethereum network.

## Architecture

### Stack-Based Execution

The EVM uses a LIFO stack rather than registers. All operands are popped from the stack; results are pushed back. The word size is 256 bits — chosen to facilitate native 256-bit hashing and elliptic curve operations [^src1].

### Memory Regions

Four distinct data components are available during execution [^src1]:

| Region | Persistence | Notes |
|---|---|---|
| **Code ROM** | Permanent (immutable) | Bytecode of the contract being executed; read-only |
| **Volatile memory** | Single call | Zero-initialized; byte-addressable; cheap to read/write; cleared after each call |
| **Transient storage** | Single transaction | Introduced in EIP-1153; cheaper than persistent storage; cleared at end of transaction |
| **Permanent storage** | Cross-transaction | Part of Ethereum global state; 32-byte slots; expensive (SSTORE ~20,000 gas) |

### Single-Threaded Execution

The Ethereum world computer is single-threaded — no parallelism, no scheduling. Execution order is determined externally by the ordering of transactions in a block [^src1]. This makes reasoning about state transitions simpler but limits throughput.

## Instruction Set (Opcodes)

The EVM instruction set covers [^src1]:

| Category | Examples |
|---|---|
| Arithmetic / Bitwise Logic | ADD, MUL, DIV, MOD, AND, OR, XOR, SHL, SHR |
| Stack Operations | PUSH1–PUSH32, POP, DUP1–DUP16, SWAP1–SWAP16 |
| Memory Operations | MLOAD, MSTORE, MSIZE |
| Storage Operations | SLOAD, SSTORE (most expensive opcodes) |
| Control Flow | JUMP, JUMPI, STOP, RETURN, REVERT |
| System / Context | CALL, DELEGATECALL, STATICCALL, CREATE, CREATE2, SELFDESTRUCT |
| Environment | CALLER, CALLVALUE, CALLDATALOAD, BLOCKHASH, GASLEFT |
| Logging | LOG0–LOG4 (emit Solidity events) |

All operands come from the stack; results go back to the stack. Context variables (account address, block number, current gas price) are available as dedicated opcodes [^src1].

## Gas and Opcodes

Every opcode has a fixed or dynamic gas cost. Key cost signals:

- **SSTORE** — most expensive; writing a new nonzero slot costs ~20,000 gas (warm writes are cheaper via EIP-2929).
- **SLOAD** — ~2,100 gas cold; ~100 gas warm (after first access in transaction).
- **CALL / CREATE** — involve significant fixed costs plus stipend for called contract.
- **SELFDESTRUCT** — destroys the contract and refunds storage (refund mechanics changed in EIP-3529).
- **Pure computation** (ADD, MUL) — cheap, ~3–5 gas.

Expensive storage operations explain why on-chain data storage is minimized and off-chain storage (IPFS, Arweave) is preferred for large data [^src1].

## ABI Encoding and Function Selectors

Solidity contracts are compiled to EVM bytecode. External calls carry ABI-encoded calldata:

- **Function selector** — first 4 bytes of `keccak256` of the function signature (e.g., `transfer(address,uint256)` → `0xa9059cbb`). The contract uses this to route to the correct function.
- **Parameters** — ABI-encoded according to type rules: addresses are zero-padded to 32 bytes; dynamic types (bytes, string) are length-prefixed.

This encoding is standardized, enabling any client to call any contract without prior knowledge beyond the ABI.

## EVM Ecosystem

The EVM has become the de facto standard VM for blockchains [^src1]. Most alternative L1s (Polygon, BNB Chain, Avalanche C-Chain) and L2s (Arbitrum, Optimism, Base) maintain full EVM compatibility to inherit Ethereum's tooling ecosystem (Hardhat, Foundry, ethers.js, MetaMask).

Alternative VMs (Solana VM, Move VM, Cairo VM, Wasm VM) offer trade-offs: Solana and Move VMs support parallel transaction execution (the EVM does not), while Cairo VM is purpose-built for ZK-provable execution [^src1].

## Cross-links

- [Smart Contracts](/blockchain/smart-contracts.md) — smart contracts are EVM bytecode executed by the EVM.
- [Ethereum](/blockchain/ethereum.md) — the EVM is Ethereum's execution layer.
- [Smart Contract Security](/blockchain/smart-contract-security.md) — EVM execution semantics underpin many vulnerability classes (delegatecall confusion, storage collisions).
- [Zero-Knowledge Proofs](/blockchain/zero-knowledge-proofs.md) — ZK-EVMs prove EVM execution correctness with ZK proofs.
- [Ethereum Scaling](/blockchain/ethereum-scaling.md) — rollups execute transactions off-chain in EVM-compatible environments.

[^src1]: [Mastering Ethereum — Chapter 14. The Ethereum Virtual Machine](../../raw/_inbox/book-mastering-ethereum-06-chapter-14-the-ethereum-virtual-machine.md)

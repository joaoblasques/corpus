---
type: concept
domain: blockchain
status: draft
sources:
  - path: raw/_inbox/book-mastering-ethereum-15-chapter-7-smart-contracts-and-solidity.md
    channel: book
    ingested_at: 2026-07-08
aliases:
  - smart contract
  - Solidity
  - EVM bytecode
  - contract account
  - ABI
  - Vyper
tags:
  - corpus/blockchain
  - concept
created: 2026-07-08
updated: 2026-07-08
---

# Smart Contracts

TL;DR: Smart contracts are immutable, deterministic computer programs deployed on Ethereum and executed by the EVM. They are primarily written in Solidity (imperative) or Vyper (declarative). Once deployed at an Ethereum address, they can only be triggered by transactions and run atomically.

## What Is a Smart Contract?

Nick Szabo coined "smart contract" in the 1990s to mean "a set of promises, specified in digital form, including protocols within which the parties perform on the other promises." In Ethereum's context the term is "a bit of a misnomer, given that Ethereum smart contracts are neither smart nor legal contracts" [^src1] — they are immutable computer programs that run deterministically in the EVM.

Key properties [^src1]:

- **Immutable**: once deployed, code cannot change. The only way to "upgrade" is to deploy a new contract instance.
- **Deterministic**: every node executes the same bytecode against the same state and gets the same result.
- **Limited execution context**: contracts can read their own storage, the calling transaction's context, and recent block data — nothing else.
- **Decentralized world computer**: the EVM runs as a local instance on every Ethereum node, but all instances produce the same final state.

## Life Cycle

1. Written in a high-level language (Solidity, Vyper, Yul).
2. Compiled to EVM bytecode.
3. Deployed via a **contract-creation transaction** (the `to` field is empty/null). The contract address is derived from the creator's address and nonce.
4. The contract lies dormant until a transaction calls it. "Contracts never run 'on their own' or 'in the background'" [^src1].
5. Execution is **atomic**: either all state changes in the transaction commit, or all are rolled back on error.

`SELFDESTRUCT` (deprecated by EIP-6780 in 2023) was the only way to remove a contract from state; it is no longer feasible under the Ethereum roadmap [^src1].

## Solidity vs. Vyper

| Property | Solidity | Vyper |
|---|---|---|
| Paradigm | Imperative (procedural) | Declarative (functional-leaning) |
| Syntax inspiration | JavaScript / C++ / Java | Python |
| Popularity | Most widely used | Niche but growing |
| Key trade-off | Flexible; more footgun surface | Restrictive by design; easier to audit |
| Turing-complete | Yes (EVM limit via gas) | Yes (same EVM) |

"The most popular and frequently used language for Ethereum smart contracts" is Solidity [^src1]. Vyper deliberately omits class inheritance, function overloading, and recursive calls to reduce attack surface.

## Application Binary Interface (ABI)

The ABI is the canonical interface description for a compiled contract — a JSON array describing all public functions, their parameter types, and return types. Any off-chain caller (wallet, dApp, script) uses the ABI to encode call data and decode return values. The ABI is not stored on-chain; it is a by-product of compilation.

## Visibility Modifiers (Solidity)

| Modifier | Accessible from |
|---|---|
| `public` | External callers + internal code |
| `external` | External callers only (cheaper for large calldata) |
| `internal` | This contract + inheriting contracts |
| `private` | This contract only |

Note: `private` prevents other contracts from calling the function, but the data is still publicly visible on-chain.

## Events and Logs

Contracts emit **events** (stored as EVM logs) to signal state changes. Logs are cheaper than storage and are indexed off-chain. Front-ends listen for events via JSON-RPC subscriptions. Events cannot be read by smart contracts — they are write-only signals to the outside world.

## Constructor Pattern

A `constructor` runs exactly once at deployment time and is used to initialize state (e.g., set owner, configure parameters). After deployment, the constructor code is discarded; only the runtime bytecode is stored at the contract address.

## Execution Model

- Single-threaded: "the Ethereum world computer can be considered to be a single-threaded machine" [^src1].
- Contract-to-contract calls: a contract can call other contracts, but the originating call chain always starts with an EOA transaction.
- Gas limits execution depth and total computation; an out-of-gas error reverts all changes in the current call (and sub-calls unless explicitly caught).

## Related Pages

- [Ethereum Virtual Machine](/blockchain/ethereum-virtual-machine.md) — the runtime that executes EVM bytecode
- [Ethereum Transactions](/blockchain/ethereum-transactions.md) — how contracts are called and deployed
- [Smart Contract Security](/blockchain/smart-contract-security.md) — vulnerabilities and defensive patterns
- [Ethereum](/blockchain/ethereum.md) — platform context

[^src1]: [Mastering Ethereum — Ch.7 Smart Contracts and Solidity](../../raw/_inbox/book-mastering-ethereum-15-chapter-7-smart-contracts-and-solidity.md)

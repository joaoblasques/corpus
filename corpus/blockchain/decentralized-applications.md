---
type: concept
domain: blockchain
status: draft
sources:
  - path: raw/_inbox/book-mastering-ethereum-04-chapter-12-decentralized-applications.md
    channel: book
    ingested_at: 2026-07-08
aliases:
  - DApp
  - decentralized app
  - web3 frontend
  - DApp stack
tags:
  - corpus/blockchain
  - concept
created: 2026-07-08
updated: 2026-07-08
---

# Decentralized Applications (DApps)

TL;DR: A DApp replaces a centralized server + database with smart contracts on-chain, and replaces a single official frontend with a replaceable (potentially community-hosted) web interface. The key properties are censorship resistance, no single point of failure, and continued operation even if the development team disappears.

## What Is a DApp?

"DApp stands for decentralized application; it's a completely new paradigm shift compared to legacy applications" [^src1].

Legacy application architecture:
- Closed-source logic on a centralized server.
- Centralized database.
- Single controlled frontend.

DApp architecture:
- Smart contracts on Ethereum encode logic and data storage (open-source, immutable).
- Replaceable frontends (official or community-made) interact with contracts.
- Anyone can read contract state; no one can stop contract execution [^src1].

> DApps can have off-chain components with some degree of centralization, but those components should not be fundamental to core logic. Core logic should always be verifiable from on-chain data [^src1].

## DApp Components

### Backend (Smart Contracts)

"In a DApp, core business logic and data storage are encoded into smart contracts and run on the Ethereum blockchain instead of residing on a centralized server" [^src1]. Transaction execution and state changes are trustlessly enforced by the network, not a company.

**Censorship resistance** — no entity can prevent an address from interacting with deployed smart contracts. Even if an official website is banned, anyone can build an alternative frontend [^src1]. (Example: Facebook is banned in 8+ countries; a comparable DApp cannot be similarly banned.)

### Frontend (Web Interface)

The DApp frontend is a traditional web application (JavaScript, React, etc.) that communicates with Ethereum via a JavaScript library [^src1]:

**ethers.js** — lightweight Ethereum library for interacting with the network and contracts; the current standard.

**web3.js** — the original Ethereum JavaScript library; larger bundle size; still widely used in legacy projects.

The frontend calls contract functions by constructing and signing transactions locally, then broadcasting them. No private keys leave the user's device (when using MetaMask or similar wallet extensions) [^src1].

### Wallet Integration

User wallets connect to DApp frontends via the **EIP-1193** provider API (the `window.ethereum` object injected by MetaMask and other wallet extensions). The wallet signs transactions; the DApp sends them to the network [^src1].

### Storage

Smart contract storage is expensive (~$20,000/MB at typical gas prices). For large data (images, documents), DApps use decentralized storage [^src1]:

| Platform | Type | Notes |
|---|---|---|
| IPFS | Content-addressed P2P storage | Most widely used; no persistence guarantee without pinning |
| Filecoin | Incentivized storage market built on IPFS | Paid persistence |
| Arweave | Permanent decentralized storage | One-time fee for permanent storage |
| Swarm | Ethereum-native decentralized storage | Incentivized with BZZ token |

NFT metadata and images are typically stored on IPFS; the on-chain ERC-721 token stores only the IPFS hash [^src1].

### Naming (ENS)

The Ethereum Name Service (ENS) maps human-readable names (`vitalik.eth`) to Ethereum addresses, IPFS content hashes, and other resources. ENS is itself a DApp — a set of smart contracts on Ethereum — and provides decentralized DNS for the DApp ecosystem [^src1].

## DApp Security Considerations

- Smart contract bugs are public and permanent — code audits are essential.
- Frontend centralization remains (DNS, CDN, hosting) — users should verify the contract address independently.
- Wallet phishing: users must verify they are signing for the correct contract.
- Upgradability via proxy patterns introduces centralization risk [^src1].

## DApp Development Stack

Common DApp development tools [^src1]:

| Tool | Role |
|---|---|
| Hardhat / Foundry | Local development environment; testing; deployment |
| Alchemy / Infura | Hosted Ethereum node APIs (JSON-RPC) |
| MetaMask | Browser wallet; dev testing |
| ethers.js | Frontend-to-chain bridge |
| OpenZeppelin | Audited contract library |
| The Graph | Indexing and querying on-chain events (GraphQL) |
| IPFS / Pinata | Decentralized content storage / pinning service |

## Cross-links

- [Smart Contracts](/blockchain/smart-contracts.md) — the on-chain backend of every DApp.
- [Ethereum Tokens](/blockchain/ethereum-tokens.md) — token interactions are DApp primitives.
- [DeFi](/blockchain/defi.md) — the largest DApp category by TVL.
- [Oracles](/blockchain/oracles.md) — DApps requiring external data depend on oracles.
- [Ethereum](/blockchain/ethereum.md) — the platform DApps run on.

[^src1]: [Mastering Ethereum — Chapter 12. Decentralized Applications](../../raw/_inbox/book-mastering-ethereum-04-chapter-12-decentralized-applications.md)

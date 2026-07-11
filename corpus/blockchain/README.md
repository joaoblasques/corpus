---
type: hub
domain: blockchain
status: draft
provisional: true
tags:
  - corpus/blockchain
  - hub
created: 2026-06-17
updated: 2026-07-08
---

# Blockchain

TL;DR: Concepts, history, cryptographic primitives, and network design underlying Bitcoin and the broader cryptocurrency ecosystem. Sourced from the nakamoto.ghost.io developer course (Haseeb Qureshi, 2019–2020), Eli Ben-Sasson's survey of cryptographic proof systems, Mastering Bitcoin 3rd Edition (Antonopoulos & Harding, CC BY-SA 4.0), and Mastering Ethereum (Antonopoulos & Wood, CC BY-SA 4.0). Now covers the full Ethereum technical stack: EVM, smart contracts, DeFi, scaling, and consensus.

## Domain description

This domain covers the full technical and historical stack of blockchain and cryptocurrency: the social evolution of money, the ideological movements (cypherpunks) that preceded Bitcoin, the cryptographic building blocks (hash functions, Merkle trees, public-key cryptography, proof-of-work), the peer-to-peer networking layer (gossip protocols, bootstrap, privacy), and advances in cryptographic proof systems (SNARKs, STARKs, zero-knowledge proofs). The primary source is a free developer course at nakamoto.ghost.io by Haseeb Qureshi (managing partner, Dragonfly Capital).

## Pages

### History & Context
- [History of Money](/blockchain/history-of-money.md) — concept · draft · Evolution of money from barter to Bitcoin; money's three properties; role of social consensus
- [The Cypherpunks](/blockchain/the-cypherpunks.md) — concept · draft · Bay Area crypto-libertarian movement (1992–); predecessor digital cash systems; Bitcoin's ideological lineage
- [Satoshi Nakamoto](/blockchain/satoshi-nakamoto.md) — entity · draft · Pseudonymous Bitcoin creator; Nakamoto Consensus; development timeline; disappearance

### Core Concepts
- [Bitcoin](/blockchain/bitcoin.md) — entity · draft · Bitcoin as a system: consensus, identity, network, history; first prices and transactions
- [Bitcoin Transactions](/blockchain/bitcoin-transactions.md) — concept · draft · UTXO model; inputs/outputs; fee market (RBF, CPFP); coinbase transaction
- [Bitcoin Script](/blockchain/bitcoin-script.md) — concept · draft · Forth-like stack language; P2PKH/P2WPKH/Taproot; authorization and authentication
- [Bitcoin Security](/blockchain/bitcoin-security.md) — concept · draft · bearer asset model; key custody tiers; HD wallets (BIP-32/39/44); cold storage
- [Proof-of-Work](/blockchain/proof-of-work.md) — concept · draft · Hashcash origins; PoW mechanics; Bitcoin mining; difficulty scaling
- [Public-Key Cryptography](/blockchain/public-key-cryptography.md) — concept · draft · Asymmetric encryption; digital signatures; ECC / secp256k1; wallet types; quantum threats
- [Hash Functions](/blockchain/hash-functions.md) — concept · draft · SHA-256; cryptographic properties; birthday attacks; broken algorithms
- [Merkle Trees](/blockchain/merkle-trees.md) — concept · draft · Construction; inclusion proofs; O(log n) verification; Bitcoin SPV light clients

### Second-Layer Applications
- [Lightning Network](/blockchain/lightning-network.md) — concept · draft · Payment channels + HTLC routing; Bitcoin's L2 for micropayments
- [Payment Channels](/blockchain/payment-channels.md) — concept · draft · Bidirectional off-chain channels; revocable commitment transactions; trustless settlement

### Ethereum
- [Ethereum](/blockchain/ethereum.md) — entity · draft · World computer; Turing-complete smart contract platform; ETH currency; The Merge (PoS)
- [Ethereum Nodes](/blockchain/ethereum-nodes.md) — concept · draft · Execution + consensus client split; full/archive/light nodes; client diversity
- [Ethereum Transactions](/blockchain/ethereum-transactions.md) — concept · draft · Nonce, gas, EIP-1559 base fee + priority fee; transaction lifecycle
- [Smart Contracts](/blockchain/smart-contracts.md) — concept · draft · Solidity vs Vyper; ABI; deployment; events; visibility modifiers
- [Smart Contract Security](/blockchain/smart-contract-security.md) — concept · draft · Defensive programming; reentrancy; overflow; access control; Swiss cheese model
- [Ethereum Tokens](/blockchain/ethereum-tokens.md) — concept · draft · ERC-20, ERC-721 (NFT), ERC-1155, ERC-4626; fungibility
- [Oracles](/blockchain/oracles.md) — concept · draft · Oracle problem; Chainlink; VRF; decentralized oracle networks
- [Decentralized Applications](/blockchain/decentralized-applications.md) — concept · draft · DApp architecture; Web3 stack; IPFS; ENS
- [DeFi](/blockchain/defi.md) — concept · draft · AMMs; lending/borrowing; flash loans; stablecoins; composability
- [Ethereum Virtual Machine](/blockchain/ethereum-virtual-machine.md) — concept · draft · Quasi-Turing-complete stack machine; 256-bit word; gas metering; opcodes; EVM compatibility
- [Ethereum Consensus](/blockchain/ethereum-consensus.md) — concept · draft · PoS; Gasper (Casper FFG + LMD GHOST); validators; slashing; The Merge
- [Ethereum Scaling](/blockchain/ethereum-scaling.md) — concept · draft · Scalability trilemma; L2 rollups (optimistic/ZK); EIP-4844; danksharding

### Networking
- [P2P Networking](/blockchain/p2p-networking.md) — concept · draft · P2P architecture; gossip protocols; Gnutella; Bitcoin's peer discovery, spam protection, and privacy (Dandelion)

### Cryptographic Proofs
- [Zero-Knowledge Proofs & Proof Systems](/blockchain/zero-knowledge-proofs.md) — concept · draft · SNARKs vs STARKs; arithmetization; symmetric vs asymmetric assumptions; Groth16, PLONK, Halo

### Decentralized AI Networks
- [Bittensor (TAO)](/blockchain/bittensor.md) — entity · draft · Decentralized AI subnet marketplace; TAO token; Score Vision (subnet 44), Hippias storage (subnet 75), Quasar extended-context (subnet 24)

### Market Dynamics
- [NFT Market Dynamics](/blockchain/nft-markets.md) — concept · draft · Floor price mechanics, supply manipulation (burns/staking), royalty fragility, pump-and-dump patterns, OpenSea data breach (2022 era documentation)

### Sources
- [Mastering Bitcoin, 3rd Edition (Antonopoulos & Harding)](/blockchain/sources/mastering-bitcoin-3rd-edition.md) — source · draft · full technical reference; 14 chapters; CC BY-SA 4.0
- [Mastering Ethereum (Antonopoulos & Wood)](/blockchain/sources/mastering-ethereum.md) — source · draft · 17 chapters; full Ethereum technical reference; CC BY-SA 4.0

<!-- AUTO-INDEX:START (generated by bin/corpus_heal.py hubs — do not edit inside) -->

## Pages in this domain

### Concepts (25)
- [Bitcoin Script](/blockchain/bitcoin-script.md)
- [Bitcoin Security](/blockchain/bitcoin-security.md)
- [Bitcoin Transactions](/blockchain/bitcoin-transactions.md)
- [Decentralized Applications (DApps)](/blockchain/decentralized-applications.md)
- [Decentralized Finance (DeFi)](/blockchain/defi.md)
- [Ethereum Consensus (Gasper / PoS)](/blockchain/ethereum-consensus.md)
- [Ethereum Nodes](/blockchain/ethereum-nodes.md)
- [Ethereum Scaling](/blockchain/ethereum-scaling.md)
- [Ethereum Tokens](/blockchain/ethereum-tokens.md)
- [Ethereum Transactions](/blockchain/ethereum-transactions.md)
- [Ethereum Virtual Machine (EVM)](/blockchain/ethereum-virtual-machine.md)
- [Hash Functions](/blockchain/hash-functions.md)
- [History of Money](/blockchain/history-of-money.md)
- [Lightning Network](/blockchain/lightning-network.md)
- [Merkle Trees](/blockchain/merkle-trees.md)
- [NFT Market Dynamics](/blockchain/nft-markets.md)
- [Oracles](/blockchain/oracles.md)
- [P2P Networking](/blockchain/p2p-networking.md)
- [Payment Channels](/blockchain/payment-channels.md)
- [Proof-of-Work](/blockchain/proof-of-work.md)
- [Public-Key Cryptography](/blockchain/public-key-cryptography.md)
- [Smart Contract Security](/blockchain/smart-contract-security.md)
- [Smart Contracts](/blockchain/smart-contracts.md)
- [The Cypherpunks](/blockchain/the-cypherpunks.md)
- [Zero-Knowledge Proofs & Proof Systems](/blockchain/zero-knowledge-proofs.md)

### Entities (4)
- [Bitcoin](/blockchain/bitcoin.md)
- [Bittensor (TAO)](/blockchain/bittensor.md)
- [Ethereum](/blockchain/ethereum.md)
- [Satoshi Nakamoto](/blockchain/satoshi-nakamoto.md)

<details>
<summary>Source summaries (3)</summary>

- ["$75,000,000 Crypto Wallet Bulk Hack"](/blockchain/sources/75-000-000-crypto-wallet-bulk-hack-MhJoJRqJ0Wc.md)
- [Mastering Bitcoin (3rd Edition) — Antonopoulos & Harding](/blockchain/sources/mastering-bitcoin-3rd-edition.md)
- [Mastering Ethereum (Antonopoulos & Wood)](/blockchain/sources/mastering-ethereum.md)

</details>

<!-- AUTO-INDEX:END -->

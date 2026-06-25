---
type: hub
domain: blockchain
status: draft
provisional: true
tags:
  - corpus/blockchain
  - hub
created: 2026-06-17
updated: 2026-06-25
---

# Blockchain

TL;DR: Concepts, history, cryptographic primitives, and network design underlying Bitcoin and the broader cryptocurrency ecosystem. Sourced from the nakamoto.ghost.io developer course (Haseeb Qureshi, 2019–2020) and Eli Ben-Sasson's survey of cryptographic proof systems.

## Domain description

This domain covers the full technical and historical stack of blockchain and cryptocurrency: the social evolution of money, the ideological movements (cypherpunks) that preceded Bitcoin, the cryptographic building blocks (hash functions, Merkle trees, public-key cryptography, proof-of-work), the peer-to-peer networking layer (gossip protocols, bootstrap, privacy), and advances in cryptographic proof systems (SNARKs, STARKs, zero-knowledge proofs). The primary source is a free developer course at nakamoto.ghost.io by Haseeb Qureshi (managing partner, Dragonfly Capital).

## Pages

### History & Context
- [[blockchain/history-of-money|History of Money]] — concept · draft · Evolution of money from barter to Bitcoin; money's three properties; role of social consensus
- [[blockchain/the-cypherpunks|The Cypherpunks]] — concept · draft · Bay Area crypto-libertarian movement (1992–); predecessor digital cash systems; Bitcoin's ideological lineage
- [[blockchain/satoshi-nakamoto|Satoshi Nakamoto]] — entity · draft · Pseudonymous Bitcoin creator; Nakamoto Consensus; development timeline; disappearance

### Core Concepts
- [[blockchain/bitcoin|Bitcoin]] — entity · draft · Bitcoin as a system: consensus, identity, network, history; first prices and transactions
- [[blockchain/proof-of-work|Proof-of-Work]] — concept · draft · Hashcash origins; PoW mechanics; Bitcoin mining; difficulty scaling
- [[blockchain/public-key-cryptography|Public-Key Cryptography]] — concept · draft · Asymmetric encryption; digital signatures; ECC / secp256k1; wallet types; quantum threats
- [[blockchain/hash-functions|Hash Functions]] — concept · draft · SHA-256; cryptographic properties; birthday attacks; broken algorithms
- [[blockchain/merkle-trees|Merkle Trees]] — concept · draft · Construction; inclusion proofs; O(log n) verification; Bitcoin SPV light clients

### Networking
- [[blockchain/p2p-networking|P2P Networking]] — concept · draft · P2P architecture; gossip protocols; Gnutella; Bitcoin's peer discovery, spam protection, and privacy (Dandelion)

### Cryptographic Proofs
- [[blockchain/zero-knowledge-proofs|Zero-Knowledge Proofs & Proof Systems]] — concept · draft · SNARKs vs STARKs; arithmetization; symmetric vs asymmetric assumptions; Groth16, PLONK, Halo

### Decentralized AI Networks
- [[blockchain/bittensor|Bittensor (TAO)]] — entity · draft · Decentralized AI subnet marketplace; TAO token; Score Vision (subnet 44), Hippias storage (subnet 75), Quasar extended-context (subnet 24)

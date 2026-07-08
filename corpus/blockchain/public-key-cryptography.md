---
type: concept
domain: blockchain
status: draft
sources:
  - path: raw/notes/notes-public-key-cryptography-scrape.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/_inbox/book-mastering-ethereum-12-chapter-4-cryptography.md
    channel: book
    ingested_at: 2026-07-08
aliases:
  - asymmetric cryptography
  - PKI
  - public key cryptography
  - ECC
  - elliptic curve cryptography
  - digital signatures
  - secp256k1
tags:
  - corpus/blockchain
  - concept
created: 2026-06-17
updated: 2026-07-08
---

# Public-Key Cryptography

TL;DR: The foundational technology that makes Bitcoin identity possible. Without it, cryptocurrencies cannot exist. A public/private key pair serves as a user's identity on the network — no names, no passwords, just math. Bitcoin uses the secp256k1 elliptic curve (ECC), which provides equivalent security to RSA-2048 with a 256-bit key.

## Three distinct operations (often confused)

| Operation | What it does | Reversible? |
|---|---|---|
| Encoding | Converts data to a known format (e.g., Base64) | Yes |
| Encryption | Scrambles data with a key so only the key-holder can read it | Yes (with key) |
| Hashing | Produces a fixed-size one-way digest | No |

All three appear in Bitcoin, but serve different purposes [^src1].

## Symmetric vs. asymmetric encryption

- **Symmetric**: one shared key encrypts and decrypts. Fast. Key exchange is the problem.
- **Asymmetric**: two mathematically inverse keys — public and private. Slower, but eliminates the key-exchange problem.

In practice, TLS uses asymmetric crypto for key exchange, then switches to symmetric for bulk data. This hybrid approach is why asymmetric slowness rarely matters in practice [^src1].

## Identity in Bitcoin

"Your key pair is itself your identity" — no names, no emails, just a public/private key pair [^src1]. The public key serves as your address (after hashing); the private key is your ability to authorize transactions.

Bitcoin address derivation: `RIPEMD160(SHA2(pub_key))`

This double-hashing adds a compression step and provides some quantum resistance for unspent coins (the public key is not exposed until the coin is spent).

## Digital signatures

A digital signature is an unforgeable proof that the private key owner approved specific data. It is:

- **Unforgeable**: impossible to produce without the private key
- **Non-repudiable**: signer cannot deny signing
- **Message-bound**: a signature on one message is invalid for any other message
- **Publicly verifiable**: anyone with the public key can verify, without needing the private key [^src1]

In Bitcoin, every transaction input is signed with the sender's private key.

## RSA vs. Elliptic Curve Cryptography

| | RSA (1977) | ECC |
|---|---|---|
| Hard problem | Integer factoring | Elliptic curve discrete log |
| Key size (equivalent security) | 2048 bits | 256 bits |
| Bitcoin uses | No | Yes (secp256k1) |

"Energy to crack a 228-bit ECC key would be enough to boil all the water on earth" [^src1] — the practical security margin at Bitcoin's key size is even larger.

## Quantum computing threat

Shor's algorithm can crack both RSA and ECC on a sufficiently capable quantum computer. However, current quantum hardware is primitive — the largest number factored via Shor's is 21 [^src1]. NIST ran a post-quantum cryptography competition to standardize quantum-resistant alternatives. Bitcoin's RIPEMD160 hash of the public key provides some protection for unspent UTXOs (the public key is not exposed until spending).

## Key quality and entropy

Private key security depends entirely on entropy quality. Operating systems collect entropy from temperature sensors, mouse movement, and timing jitter. Insufficient entropy has enabled real attacks — notably the Android SecureRandom bug which allowed private key recovery from Bitcoin Android wallets [^src1].

Rule: **never roll your own crypto**.

## Bitcoin wallet types

| Type | Security | Convenience |
|---|---|---|
| Paper | High (air-gapped) | Low |
| Brain (BIP39 mnemonic) | Depends on passphrase | Medium |
| Web (Coinbase, Blockchain.com) | Low (custodial) | High |
| Software (Bitcoin Core, Electrum, Wasabi) | Medium | Medium |
| Hardware (Ledger, Trezor, KeepKey) | High | Medium |

## Ethereum-Specific Cryptography

Ethereum uses the same secp256k1 elliptic curve as Bitcoin for EOA key pairs, but the address derivation differs [^src2]:

- **Ethereum address derivation**: `keccak256(public_key)[12:]` — take the last 20 bytes of the Keccak-256 hash of the uncompressed public key.
- **vs Bitcoin**: Bitcoin uses `RIPEMD160(SHA256(public_key))`.

Ethereum uses **Keccak-256** (NOT SHA-3 — Keccak was submitted to the SHA-3 competition but Ethereum adopted it before NIST finalized the standard with padding changes) [^src2].

### Validator Keys (BLS)

Post-Merge, Ethereum validators use a different key scheme for consensus signatures [^src2]:

- **BLS12-381** elliptic curve (not secp256k1).
- BLS signatures can be **aggregated**: hundreds of validator signatures are combined into one compact signature, enabling efficient attestation aggregation across the 1M+ validator set.
- Each validator has two key pairs: a signing key (hot, used frequently) and a withdrawal key (cold, used only to exit).

### KZG Commitments (EIP-4844)

KZG (Kate-Zaverucha-Goldberg) polynomial commitments are used in blob transactions (EIP-4844) [^src2]:

- A KZG commitment is a constant-size (~48 byte) representation of a polynomial (the blob data).
- KZG commitments are verifiable: a prover can produce a proof that the polynomial evaluates to a specific value at a specific point.
- Used by ZK rollups to commit to their data batches on Ethereum L1.
- Requires a trusted setup ceremony (Ethereum held "The Ceremony" with 141,000+ participants in 2023).

## Related pages

- [Hash Functions](/blockchain/hash-functions.md) — SHA-256 and RIPEMD160 are used in address derivation
- [Bitcoin](/blockchain/bitcoin.md) — how key pairs function as identity in the network
- [The Cypherpunks](/blockchain/the-cypherpunks.md) — the movement that fought for public cryptography access
- [Zero-Knowledge Proofs](/blockchain/zero-knowledge-proofs.md) — **depends-on** the same asymmetric primitives (ECC, discrete log) that underpin SNARKs; Shor's algorithm threatens both
- [Proof-of-Work](/blockchain/proof-of-work.md) — **complements** public-key crypto in Bitcoin: signatures authorize transactions, PoW orders them into consensus
- [Ethereum](/blockchain/ethereum.md) — Ethereum uses secp256k1 (EOA keys) and BLS12-381 (validator keys)

[^src1]: [Public-Key Cryptography](../../raw/notes/notes-public-key-cryptography-scrape.md)
[^src2]: [Mastering Ethereum — Chapter 4. Cryptography](../../raw/_inbox/book-mastering-ethereum-12-chapter-4-cryptography.md)

---
type: concept
domain: blockchain
status: draft
sources:
  - path: raw/_inbox/book-mastering-ethereum-02-chapter-10-tokens.md
    channel: book
    ingested_at: 2026-07-08
aliases:
  - ERC-20
  - ERC-721
  - ERC-1155
  - NFT
  - non-fungible token
  - fungible token
  - token standard
  - EIP-20
tags:
  - corpus/blockchain
  - concept
created: 2026-07-08
updated: 2026-07-08
---

# Ethereum Tokens

TL;DR: Tokens are blockchain-based abstractions representing ownership, access, or value. Ethereum standardizes fungible tokens (ERC-20), non-fungible tokens (ERC-721), and multi-token systems (ERC-1155). The standards define minimal interfaces that enable interoperability across wallets and protocols.

## What Is a Token?

"Token" derives from Old English *tācen* (sign or symbol). On Ethereum, tokens are smart contracts that represent and track ownership of assets, rights, or utility. "With blockchain tokens, these restrictions [of physical tokens] are lifted or, to be more accurate, are completely redefinable" [^src1].

## Token Use Cases

A single token can serve multiple functions simultaneously [^src1]:

| Use | Example |
|---|---|
| **Currency** | Stablecoins (USDC, DAI); value determined by private trade |
| **Resource** | Storage or compute tokens (Filecoin, Akash) |
| **Asset** | Tokenized gold, real estate, commodities |
| **Access** | Membership tokens granting access to forums, events, services |
| **Equity** | DAO governance shares; tokenized corporate shares |
| **Voting** | Governance tokens (UNI, COMP) that carry on-chain voting weight |
| **Collectible** | CryptoPunks, CryptoKitties, generative art NFTs |
| **Identity** | Soulbound tokens, avatar NFTs |
| **Attestation** | Verifiable credentials (marriage records, degrees) |
| **Utility** | Gas-equivalent tokens for platform services |

## Fungibility

**Fungible**: every unit is interchangeable with any other unit. 1 USDC == any other 1 USDC. Fungible tokens implement ERC-20 [^src1].

**Non-fungible (NFT)**: each token is unique. "A token that represents ownership of a *specific* Van Gogh painting is not equivalent to another token that represents a Picasso" [^src1]. Each NFT has a unique `tokenId`. Non-fungible tokens implement ERC-721.

## ERC-20: Fungible Token Standard

ERC-20 defines the minimal interface all fungible tokens must expose [^src1]:

| Function / Event | Purpose |
|---|---|
| `totalSupply()` | Total token supply |
| `balanceOf(address)` | Token balance of an address |
| `transfer(to, amount)` | Direct transfer from caller |
| `approve(spender, amount)` | Allow `spender` to transfer up to `amount` on caller's behalf |
| `transferFrom(from, to, amount)` | Transfer from `from` to `to` using a prior approval |
| `allowance(owner, spender)` | Remaining approved amount |
| `Transfer` event | Emitted on every transfer |
| `Approval` event | Emitted on every approval |

The approve/transferFrom pattern enables DeFi composability: a DEX contract is approved to move tokens on a user's behalf without the user handing over private keys.

**ERC-20 gap**: the standard has no mechanism to detect accidental transfers to contracts — tokens sent via `transfer()` to a contract address that doesn't handle ERC-20 are permanently lost. ERC-223 and ERC-777 attempted to fix this; ERC-777 introduced reentrancy risks and fell out of favor.

## ERC-721: Non-Fungible Token Standard

ERC-721 standardizes NFTs. Key additions over ERC-20 [^src1]:

- `tokenId`: every token has a unique `uint256` identifier.
- `ownerOf(tokenId)`: returns the owner of a specific token.
- `safeTransferFrom(from, to, tokenId)`: transfers a specific token; calls `onERC721Received` on the recipient contract to prevent loss.
- `tokenURI(tokenId)`: optional; returns a URI pointing to metadata JSON (image, attributes).

NFT metadata typically lives off-chain (IPFS or centralized server) — the on-chain token stores only the `tokenId` and optionally a URI. This is a centralization risk: if the metadata server goes down, the "image" of an NFT disappears.

## ERC-1155: Multi-Token Standard

ERC-1155 (Enjin standard) allows a single contract to manage both fungible and non-fungible token types, identified by a `uint256 id`. Efficiency advantages [^src1]:

- **Batch transfers**: transfer multiple token types in a single transaction.
- **Batch minting**: deploy one contract for an entire game item catalog.
- Saves deployment gas vs. deploying separate ERC-20/721 contracts per item.

Common in gaming, where a player might hold both fungible in-game currency and unique items.

## Comparing Standards

| | ERC-20 | ERC-721 | ERC-1155 |
|---|---|---|---|
| Fungibility | Fungible | Non-fungible | Both |
| Token identity | By contract address | `tokenId` | `id` |
| Batch ops | No | No | Yes |
| Typical use | Currency, governance | Art, collectibles | Gaming, multi-asset |
| Safety on transfer to contract | No (tokens lost) | `safeTransferFrom` check | `safeTransferFrom` check |

## Related Pages

- [Smart Contracts](/blockchain/smart-contracts.md) — tokens are deployed as smart contracts
- [DeFi](/blockchain/defi.md) — ERC-20 tokens are the primitive currency of DeFi protocols
- [Decentralized Applications](/blockchain/decentralized-applications.md) — wallets and frontends interact with token contracts via ABI
- [Ethereum](/blockchain/ethereum.md) — platform context; ETH itself is not ERC-20 (it is native currency)

[^src1]: [Mastering Ethereum — Ch.10 Tokens](../../raw/_inbox/book-mastering-ethereum-02-chapter-10-tokens.md)

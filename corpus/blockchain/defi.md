---
type: concept
domain: blockchain
status: draft
sources:
  - path: raw/_inbox/book-mastering-ethereum-05-chapter-13-decentralized-finance.md
    channel: book
    ingested_at: 2026-07-08
aliases:
  - DeFi
  - decentralized finance
  - AMM
  - automated market maker
  - DEX
  - decentralized exchange
  - flash loan
  - liquidity pool
  - yield farming
  - stablecoin
  - TVL
tags:
  - corpus/blockchain
  - concept
created: 2026-07-08
updated: 2026-07-08
---

# Decentralized Finance (DeFi)

TL;DR: DeFi recreates financial services (trading, lending, borrowing, insurance) using Ethereum smart contracts rather than banks or brokers. Key primitives: AMMs for trading (x*y=k), overcollateralized lending, stablecoins, and flash loans (uncollateralized, single-tx). Composability ("money legos") is DeFi's superpower and its primary systemic risk.

## DeFi vs. Traditional Finance (TradFi)

"DeFi is the cryptopunk response to the traditional financial (TradFi) system" [^src1]. Core distinctions:

| Dimension | TradFi | DeFi |
|---|---|---|
| Medium | Fiat currency (always centralized) | Cryptocurrencies (decentralized to varying degrees) |
| Access | Identity docs, credit score, geography | Wallet + internet connection + collateral |
| Settlement | T+2 days | Seconds (same block) |
| Transparency | Opaque (counterparty risk) | All state on-chain, publicly readable |
| Trust model | Regulated intermediaries | Smart contract code (trustless) |
| Unique primitives | None | Flash loans, atomic composability |

"In DeFi, only three prerequisites are needed [for a loan]: a phone, an internet connection, and enough assets to overcollateralize the loan. Once these are in place, the loan is instant, decentralized, and permissionless" [^src1].

Current DeFi users are primarily crypto-native speculators; the financial-inclusion promise (underbanked populations) remains largely unrealized [^src1].

## DeFi Primitives

### Decentralized Exchanges (DEXs) and AMMs

DEXs allow token trading without a centralized intermediary. The on-chain order book model failed due to latency and cost [^src1].

**Automated Market Makers (AMMs)** replaced order books. Bancor pioneered the model; Uniswap popularized it with the constant-product formula:

> **x × y = k**

Where x and y are the quantities of two tokens in a liquidity pool, and k is a constant [^src1]. When a trader buys token X, they deposit token Y; the ratio shifts, and the price adjusts automatically. The product k never changes.

Anyone can become a market maker by depositing token pairs into a liquidity pool, earning a share of trading fees proportional to their liquidity contribution.

**Slippage**: large trades shift the ratio significantly, causing price impact. AMMs work best with deep pools.

**Impermanent loss**: LPs bear risk that holding pooled assets performs worse than holding them separately when prices diverge.

### Lending Protocols

Protocols like Aave and Compound allow users to lend assets (earning yield) and borrow against collateral.

**Overcollateralization**: borrowers must deposit collateral worth more than their loan (e.g., 150% collateral ratio). DeFi cannot assess creditworthiness, so overcollateralization substitutes for credit checks.

**Liquidation**: if the collateral value drops below the minimum ratio, the position is automatically liquidated — a smart contract sells collateral to repay the loan. Liquidators receive a bonus for performing this service.

**Interest rates**: algorithmically set based on utilization rate. High utilization → higher rates to attract more lenders.

### Stablecoins

Tokens pegged to a stable value (usually 1 USD):

| Type | Mechanism | Examples | Risk |
|---|---|---|---|
| Fiat-collateralized | 1:1 backed by USD in bank | USDC, USDT | Centralization; custodian risk |
| Crypto-collateralized | Overcollateralized with crypto | DAI (MakerDAO) | Liquidation cascade risk |
| Algorithmic | Seigniorage or rebalancing | UST (failed 2022) | Death spiral risk |

Note on bridged vs. native stablecoins: USDC native on a chain differs from USDC.e (bridged) — "the risk profiles of these two tokens are markedly different" due to added bridge smart contract risk [^src1].

### Flash Loans

"Flash loans allow users to borrow funds without collateral as long as the loan is repaid within the same transaction" [^src1]. If repayment doesn't happen, the entire transaction reverts.

Use cases:
- **Arbitrage**: borrow → exploit price difference across DEXs → repay → pocket profit
- **Collateral swap**: atomically swap collateral type without additional capital
- **Self-liquidation**: repay a loan with flash-borrowed funds, retrieve collateral, repay flash loan

Flash loans require no capital (only gas) and are "unique to DeFi" and "impossible within the traditional financial system" [^src1]. They also enable sophisticated attacks — attackers use flash loans to manipulate oracle prices or drain protocols in a single block.

### Yield Aggregators

Protocols like Yearn Finance automatically route deposited assets across lending protocols and liquidity pools to maximize yield, compounding returns automatically.

## Composability ("Money Legos")

DeFi protocols interoperate: the output of one protocol is the input of another. Example: supply ETH to Aave → receive aETH → deposit aETH as collateral in MakerDAO → mint DAI → provide DAI to Uniswap pool.

This composability unlocks novel financial instruments but also creates systemic risk — a vulnerability in any one protocol can cascade through all connected protocols in a single transaction.

## Key Risks

| Risk | Description |
|---|---|
| Smart contract bugs | Code vulnerabilities → fund loss |
| Oracle manipulation | Price feeds can be attacked; flash loans make this cheap |
| Liquidation cascades | Rapid price drops trigger cascading liquidations, amplifying losses |
| Impermanent loss | AMM LPs lose relative to holding when prices diverge significantly |
| Composability risk | Multi-protocol stacks multiply attack surface |
| Regulatory risk | DeFi's permissionless access conflicts with AML/KYC requirements |

## Related Pages

- [Ethereum Tokens](/blockchain/ethereum-tokens.md) — ERC-20 is the primitive currency of DeFi
- [Smart Contracts](/blockchain/smart-contracts.md) — DeFi runs entirely on smart contracts
- [Smart Contract Security](/blockchain/smart-contract-security.md) — DeFi is the primary attack surface
- [Oracles](/blockchain/oracles.md) — price feeds critical for lending and liquidation
- [Ethereum Scaling](/blockchain/ethereum-scaling.md) — high gas costs make DeFi inaccessible; L2s solve this

[^src1]: [Mastering Ethereum — Ch.13 Decentralized Finance](../../raw/_inbox/book-mastering-ethereum-05-chapter-13-decentralized-finance.md)

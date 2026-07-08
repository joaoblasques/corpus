---
type: concept
domain: blockchain
status: draft
sources:
  - path: raw/_inbox/book-mastering-ethereum-17-chapter-9-smart-contract-security.md
    channel: book
    ingested_at: 2026-07-08
aliases:
  - smart contract vulnerability
  - reentrancy attack
  - integer overflow Ethereum
  - access control bug
  - defensive programming Solidity
  - Swiss cheese security model
tags:
  - corpus/blockchain
  - concept
created: 2026-07-08
updated: 2026-07-08
---

# Smart Contract Security

TL;DR: Smart contract bugs directly cause monetary loss and are nearly impossible to fix post-deployment. Defensive programming (minimalism, code reuse, readability, test coverage) forms the first layer of a "Swiss cheese" security model. Key vulnerabilities include reentrancy, integer overflow/underflow, and access control failures.

## The Stakes

"In the field of smart contract programming, mistakes are costly and easily exploited." All smart contracts are public; any user can call them with any input. "Losses are almost always impossible to recover" [^src1]. An exploit typically unfolds in a single transaction — "within seconds, long before you can intervene" [^src1].

## Swiss Cheese Model of Security

Think of security as stacked slices of Swiss cheese: no single layer is perfect, but together they block most threats. "The very first layer is following solid development practices: using reliable design patterns, writing clear and intentional code, and actively avoiding known pitfalls" [^src1]. The layers:

1. **Solid development practices** (foundational — this page)
2. Testing and test coverage
3. Code review and audits
4. Bug bounties
5. Post-deployment monitoring

## Defensive Programming Principles

**Minimalism / Simplicity** — before writing code, "question whether every component is really needed." Simpler contracts are easier to audit. "More code often means more bugs, not more value" [^src1].

**Code reuse** — use audited libraries rather than reinventing the wheel. OpenZeppelin provides "a suite of contracts that are widely adopted, thoroughly tested, and continuously reviewed by the community" [^src1]. Beware "not invented here" syndrome.

**Code quality** — "Writing a DApp in Solidity is not like creating a web widget in JavaScript. Rather, you should apply rigorous engineering and software development methodologies as you would in aerospace engineering or any similarly unforgiving discipline" [^src1].

**Readability / Auditability** — "your code should be clear and easy to comprehend. The easier it is to read, the easier it is to audit." Smart contracts are public — anyone skilled enough can reverse-engineer bytecode [^src1].

**Test coverage** — "test everything you can." Never assume inputs are well-formed or benign. "Test all arguments to make sure they are within expected ranges and are properly formatted before allowing execution of your code to continue" [^src1].

## Key Vulnerabilities

### Reentrancy

**The vulnerability**: a contract sends ether (or makes an external call) *before* updating its internal state. The receiving address's fallback function calls back into the victim contract, finding state still inconsistent. This is how the DAO hack (2016) drained funds. "Even after all these years, we're still seeing a lot of attacks exploiting this vulnerability, even though it's pretty straightforward to spot and inexpensive to fix" [^src1].

Pattern (vulnerable):
```solidity
function withdrawFunds() public {
    uint256 _amt = balances[msg.sender];
    // Sends ether BEFORE updating balance — reentrancy window
    (bool success,) = msg.sender.call{value: _amt}("");
    balances[msg.sender] = 0; // Never reached if attacker reenters
}
```

**Fix**: follow the Checks-Effects-Interactions pattern — update all state *before* making external calls. Use OpenZeppelin's `ReentrancyGuard` modifier as an additional layer.

### Integer Overflow / Underflow

Prior to Solidity 0.8.0, arithmetic operations could silently wrap around. A `uint256` at 0 minus 1 becomes `2^256 - 1`. An attacker crafts inputs to bypass balance checks or mint tokens [^src1].

**Fix**: Solidity 0.8.0+ reverts by default on overflow/underflow. For older code, use SafeMath (OpenZeppelin).

### Access Control Bugs

Functions that should only be callable by a privileged role but lack proper authorization checks allow any caller to execute privileged operations (drain funds, upgrade logic, pause the protocol). Classic example: Parity wallet multisig hack (2017).

**Fix**: use `require(msg.sender == owner)` or OpenZeppelin `AccessControl` / `Ownable`. Always explicitly declare visibility for every function.

### tx.origin vs. msg.sender

`tx.origin` is the original EOA that started the call chain. A phishing contract tricks a user into calling it; `tx.origin` is still the user. Using `tx.origin` for authentication enables phishing attacks [^src1].

**Fix**: never use `tx.origin` for authorization; always use `msg.sender`.

### Entropy Illusions (Pseudo-Randomness)

The EVM is deterministic — no true on-chain randomness. Validators can slightly manipulate `block.timestamp` and can selectively include transactions. Never use block variables as the sole entropy source for randomness.

**Fix**: use Chainlink VRF (verifiable random function) or commit-reveal schemes.

## Related Pages

- [Smart Contracts](/blockchain/smart-contracts.md) — architecture and Solidity basics
- [Ethereum Virtual Machine](/blockchain/ethereum-virtual-machine.md) — execution model and gas
- [DeFi](/blockchain/defi.md) — primary attack surface; most exploits target DeFi protocols
- [Ethereum Tokens](/blockchain/ethereum-tokens.md) — ERC-20 tokens are a common exploit target

[^src1]: [Mastering Ethereum — Ch.9 Smart Contract Security](../../raw/_inbox/book-mastering-ethereum-17-chapter-9-smart-contract-security.md)

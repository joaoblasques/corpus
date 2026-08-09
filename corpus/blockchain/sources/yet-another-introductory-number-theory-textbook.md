---
type: source
domain: blockchain
status: draft
sources:
  - path: raw/pdf/pdf-yet-another-introductory-number-theory-textbook-part-01.md
    channel: pdf
    ingested_at: 2026-08-09
  - path: raw/pdf/pdf-yet-another-introductory-number-theory-textbook-part-02.md
    channel: pdf
    ingested_at: 2026-08-09
  - path: raw/pdf/pdf-yet-another-introductory-number-theory-textbook-part-03.md
    channel: pdf
    ingested_at: 2026-08-09
  - path: raw/pdf/pdf-yet-another-introductory-number-theory-textbook-part-04.md
    channel: pdf
    ingested_at: 2026-08-09
  - path: raw/pdf/pdf-yet-another-introductory-number-theory-textbook-part-05.md
    channel: pdf
    ingested_at: 2026-08-09
aliases:
  - Yet Another Introductory Number Theory Textbook
  - YAINTT
  - Poritz number theory
  - number theory cryptology emphasis
tags:
  - corpus/blockchain
  - source
  - number-theory
  - cryptology
  - RSA
  - modular-arithmetic
created: 2026-08-09
updated: 2026-08-09
---

# Yet Another Introductory Number Theory Textbook (Poritz, 2014)

TL;DR: Free undergraduate-level number theory textbook (128pp, Jonathan A. Poritz, Colorado State University–Pueblo, 2014) with a cryptology emphasis. Covers divisibility, modular arithmetic, linear congruences, Chinese Remainder Theorem, Euler's theorem, RSA encryption, digital signatures, and discrete logarithms (indices). Primary motivation: the mathematics behind modern cryptographic systems. All 5 parts ingested (complete).

## About the Text

**Author**: Jonathan A. Poritz, Department of Mathematics and Physics, Colorado State University–Pueblo. First draft (2014). Licensed as free/open-source (free as in speech and beer). Originally used for Math 319 at CSU-Pueblo [^p01].

Cross-links: [/blockchain/public-key-cryptography.md](/blockchain/public-key-cryptography.md), [/blockchain/hash-functions.md](/blockchain/hash-functions.md).

---

## Chapter 1: Divisibility and the GCD [^p01]

**Division algorithm**: for any a ∈ ℤ and n ∈ ℕ, there exist unique q, r with a = qn + r and 0 ≤ r < n.

**GCD**: gcd(a, b) is the largest positive integer dividing both a and b. Bézout's identity: there exist integers x, y such that ax + by = gcd(a, b). This is computed by the extended Euclidean algorithm.

**Euclidean algorithm**: gcd(a, b) = gcd(b, a mod b), recurse until remainder = 0. Requires at most log₂(b) steps (each two steps halves the remainder). The logarithmic complexity makes it cryptologically feasible — it scales to the large integers used in RSA [^p04].

**Primes and unique factorization**: every n ∈ ℕ has a unique factorization into prime powers (Fundamental Theorem of Arithmetic). Primes p divide a product ab only if p|a or p|b [^p01].

---

## Chapter 2: Congruences [^p02]

**Modular arithmetic**: a ≡ b (mod n) means n | (a − b). Congruence is an equivalence relation; it preserves addition and multiplication. The set ℤ/nℤ of residues modulo n forms a commutative ring [^p02].

**Linear congruences**: ax ≡ b (mod n). Has a solution iff gcd(a, n) | b. If gcd(a, n) = 1, there is a unique solution mod n (the modular inverse of a). The modular inverse a⁻¹ is computed via the extended Euclidean algorithm [^p02].

**Chinese Remainder Theorem (CRT)**: if n₁, …, nₖ are pairwise coprime, the system x ≡ aᵢ (mod nᵢ) has a unique solution mod n₁ × … × nₖ. CRT is used in RSA to speed up private-key operations: decrypt separately mod p and mod q (the prime factors), then combine with CRT [^p02].

**Euler's totient function φ(n)**: counts integers in {1, …, n} coprime to n. φ(p) = p − 1 for prime p; φ(pq) = (p − 1)(q − 1) for distinct primes p, q. Multiplicative: gcd(m, n) = 1 → φ(mn) = φ(m)φ(n) [^p02].

**Euler's theorem**: if gcd(a, n) = 1 then a^φ(n) ≡ 1 (mod n). Fermat's little theorem is the special case n = p prime: a^(p−1) ≡ 1 (mod p). These theorems are the mathematical foundations of RSA [^p02].

---

## Chapter 3: Primality and Primitive Roots [^p02]

**Wilson's theorem**: n > 1 is prime iff (n − 1)! ≡ −1 (mod n). Not computationally useful (factorial grows fast) but theoretically important.

**Primitive roots**: an integer g is a primitive root modulo n if the powers g¹, g², …, g^φ(n) cover all residues coprime to n. The group (ℤ/nℤ)* is cyclic (has a generator) iff n = 1, 2, 4, pᵏ, or 2pᵏ for odd prime p. Every prime p has a primitive root [^p02].

---

## Chapter 4: Cryptology [^p03] [^p04]

### Information Security Concepts

**Confidentiality, integrity, authentication**: the three core security properties for communication between Alice and Bob (with adversary Eve). A cryptosystem must provide confidentiality (Eve cannot read), integrity (Eve cannot alter undetected), and authentication (Bob can verify Alice's identity) [^p03].

**Symmetric vs. asymmetric cryptosystems**: symmetric (shared secret key) systems are fast but require a secure key exchange channel. Asymmetric (public-key) systems solve the key distribution problem at the cost of slower computation [^p03].

### RSA Cryptosystem

**Key generation**: choose large primes p, q (kept secret). Compute n = pq (public), φ(n) = (p−1)(q−1) (kept secret). Choose public exponent e with gcd(e, φ(n)) = 1; compute private exponent d with ed ≡ 1 (mod φ(n)).

**Encryption**: to send message m (with 0 ≤ m < n), compute ciphertext c = mᵉ (mod n). **Decryption**: m = c^d (mod n). Correctness follows from Euler's theorem: c^d = m^(ed) = m^(1 + kφ(n)) = m · (m^φ(n))^k ≡ m (mod n) [^p04].

**Security basis**: RSA security rests on the difficulty of factoring n = pq. No efficient classical algorithm for factoring large integers is known; Shor's algorithm on a quantum computer would break RSA. Key sizes of 2048–4096 bits are currently standard for security [^p04].

**Fast modular exponentiation**: computing mᵉ (mod n) efficiently via repeated squaring. Write e in binary; for each bit, square the current value (and multiply by m if the bit is 1). O(log e) multiplications, each O((log n)²) operations — cryptologically feasible [^p04].

### Digital Signatures

**Signing with RSA**: Alice signs message m by computing s = m^d (mod n) using her private key d. Bob verifies: s^e ≡ m (mod n) using Alice's public key e. Authenticity follows because only Alice knows d [^p04].

**Hash-and-sign**: in practice, Alice signs H(m) (a hash of the message) rather than m itself, for efficiency and to prevent certain attacks. The signature scheme is: sign = H(m)^d mod n; verify: sign^e ≡ H(m) (mod n) [^p04].

---

## Chapter 5: Discrete Logarithms (Indices) [^p05]

**Index / discrete logarithm**: given a primitive root g modulo n and a ∈ (ℤ/nℤ)*, the index ind_g(a) is the unique k ∈ {1, …, φ(n)} with g^k ≡ a (mod n). Analogous to logarithms: ind_g(ab) ≡ ind_g(a) + ind_g(b) (mod φ(n)) [^p05].

**Log rules for indices**: ind_g(a^k) ≡ k · ind_g(a) (mod φ(n)), analogous to k·log(a). These allow solving exponential congruences: x^k ≡ a (mod n) becomes k · ind_g(x) ≡ ind_g(a) (mod φ(n)), a linear congruence in the index [^p05].

**Caution on moduli**: when computing with indices, the congruence for the index is modulo φ(n), not n. A common error is to mix the two moduli [^p05].

**Discrete logarithm problem (DLP)**: computing ind_g(a) from g, a, n is believed to be computationally hard (no known polynomial-time classical algorithm for general groups). DLP hardness underpins Diffie-Hellman key exchange and ElGamal encryption [^p05].

**Relevance to blockchain**: Ethereum's digital signatures (ECDSA) and key derivation rely on the DLP over elliptic curves (not ℤ/pℤ, but the discrete log structure is the same). The security of secp256k1 (Ethereum/Bitcoin's curve) depends on the elliptic curve DLP being hard [^p05].

---

[^p01]: [Yet Another Introductory Number Theory Textbook — Part 1](../../../raw/_inbox/pdf-yet-another-introductory-number-theory-textbook-part-01.md)
[^p02]: [Yet Another Introductory Number Theory Textbook — Part 2](../../../raw/_inbox/pdf-yet-another-introductory-number-theory-textbook-part-02.md)
[^p03]: [Yet Another Introductory Number Theory Textbook — Part 3](../../../raw/_inbox/pdf-yet-another-introductory-number-theory-textbook-part-03.md)
[^p04]: [Yet Another Introductory Number Theory Textbook — Part 4](../../../raw/_inbox/pdf-yet-another-introductory-number-theory-textbook-part-04.md)
[^p05]: [Yet Another Introductory Number Theory Textbook — Part 5](../../../raw/_inbox/pdf-yet-another-introductory-number-theory-textbook-part-05.md)

---
type: concept
domain: software-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-security-intro.md
    channel: pdf
    ingested_at: 2026-07-09
  - path: raw/_inbox/pdf-security-authentication.md
    channel: pdf
    ingested_at: 2026-07-09
  - path: raw/_inbox/pdf-security-access.md
    channel: pdf
    ingested_at: 2026-07-09
  - path: raw/_inbox/pdf-security-crypto.md
    channel: pdf
    ingested_at: 2026-07-09
  - path: raw/_inbox/pdf-security-distributed.md
    channel: pdf
    ingested_at: 2026-07-09
  - path: raw/_inbox/pdf-dialogue-security.md
    channel: pdf
    ingested_at: 2026-07-09
aliases:
  - OS security
  - operating system security
  - authentication
  - access control
  - cryptography
  - security principles
  - privilege separation
  - principle of least privilege
tags:
  - corpus/software-engineering
  - concept
created: 2026-07-09
updated: 2026-07-09
---

# OS Security

TL;DR: OS security addresses the problem of building a system that allows legitimate use while preventing illegitimate use. The OS is critical because everything runs on top of it — a compromised OS means every application above it is also compromised. Four foundational mechanisms: **authentication** (verify who you are), **access control** (define what each identity may do), **cryptography** (protect data confidentiality and integrity), and **distributed security** (extend trust to networked systems). Core principles: principle of least privilege, defense in depth, economy of mechanism, avoid security through obscurity. Written by Peter Reiher (UCLA).

## Why OS Security Matters

The OS is the trust anchor for all software above it [^src1]:
- Every application runs on an OS. A flawed OS exposes every application.
- The OS controls all resources — CPU, memory, I/O, network. It is the last line of defense.
- Unlike a specific web server (only relevant if you run it), every user runs an OS — making OS vulnerabilities uniquely high-impact [^src1].

**Security goal**: allow intended use; prevent all other use. More precisely, maintain:
- **Confidentiality**: only authorized parties can read data
- **Integrity**: only authorized parties can modify data
- **Availability**: authorized parties can use the system when they need to [^src1]

**Threat model**: who is the attacker, what can they do, what are we protecting? A threat model is not optional — without one, you cannot reason about whether a defense is sufficient [^src1].

## Security Principles

**Principle of least privilege**: each principal should have only the minimum access rights needed to perform their task. A process that only reads files should not have write access. A web server that only serves static files should not have shell access [^src1].

**Economy of mechanism**: keep security mechanisms simple. Complex systems have more bugs; bugs in security mechanisms are vulnerabilities. The trusted computing base (TCB) — the set of components you must trust — should be as small as possible [^src1].

**Defense in depth**: use multiple independent layers of protection. An attacker must compromise several mechanisms, not just one [^src1].

**Open design**: security should not rely on the attacker not knowing the algorithm (Kerckhoffs's principle). Cryptographic security comes from key secrecy, not algorithm secrecy [^src1].

**Fail-safe defaults**: deny by default; grant access explicitly. A new user or new resource gets no permissions unless explicitly granted [^src1].

## Authentication

**Authentication**: verify that an entity claiming an identity actually is that identity [^src2].

**Three authentication factors**:
1. **Something you know**: password, PIN, passphrase
2. **Something you have**: hardware token, smart card, smartphone (TOTP)
3. **Something you are**: biometrics (fingerprint, iris, face)

Multi-factor authentication (MFA) combines ≥2 factors — compromising one doesn't suffice.

**Password security considerations**:
- Store passwords as salted hashes (bcrypt, scrypt, Argon2), never plaintext or unsalted MD5/SHA1
- **Salt**: random per-user value prepended to password before hashing — prevents rainbow table attacks and ensures two users with the same password have different hashes
- **Slow hash functions**: bcrypt/scrypt/Argon2 are deliberately slow to make brute-force expensive [^src2]

**Authentication failures**: phishing (trick user into entering credentials), credential stuffing (reuse of leaked passwords), replay attacks (capture and resend an authentication message). Defenses: HTTPS everywhere, MFA, short-lived session tokens, password managers [^src2].

## Access Control

**Access control**: once authenticated, determine what operations the identity may perform on which resources [^src3].

**Access Control List (ACL)**: per-resource list of (principal, permissions). E.g., Unix file permissions: owner/group/other × read/write/execute. Easy to manage per-object; hard to enumerate all rights of one user [^src3].

**Capability**: per-subject token granting access to a resource. A process holds a set of capabilities. Easy to enumerate what one principal can do; harder to manage per-resource [^src3].

**Role-Based Access Control (RBAC)**: assign permissions to roles (not directly to users); assign users to roles. A hospital system might have roles: nurse, doctor, administrator — each with different access to patient records. Simplifies management at scale [^src3].

**Mandatory Access Control (MAC)**: the OS enforces a global security policy that individual users cannot override. SELinux and AppArmor implement MAC on Linux — a process may only access resources the policy permits, even if the process has root UID [^src3].

**Unix security model**: every process has a UID and GID. Every file has an owner UID, group GID, and permission bits. Kernel checks permissions on every system call. Root (UID=0) bypasses most checks — the single-user trusted super-user model is a significant weakness in multi-tenant environments [^src3].

**Privilege separation**: split a complex program into cooperating sub-processes, each with only the privileges it needs. E.g., OpenSSH privilege separation: the network-facing process runs as an unprivileged user; only a tiny privileged helper performs the authentication check. A vulnerability in the network-facing code cannot gain root [^src3].

## Cryptography

Cryptography provides confidentiality, integrity, and authentication for data at rest and in transit [^src4].

**Symmetric encryption**: the same key encrypts and decrypts. Examples: AES-128, AES-256. Fast but requires secure key distribution between parties. Used for bulk data encryption [^src4].

**Asymmetric (public-key) encryption**: a key pair — public key (safe to share) and private key (secret). Data encrypted with public key can only be decrypted with private key. Examples: RSA, elliptic-curve cryptography (ECC). Used for key exchange and signatures; slower than symmetric [^src4].

**Hybrid encryption**: use asymmetric crypto to exchange a symmetric session key, then encrypt data with the fast symmetric key. TLS/HTTPS works this way [^src4].

**Cryptographic hash functions**: one-way functions (SHA-256, SHA-3) producing a fixed-size digest. Properties: preimage resistance (can't find input from output), second-preimage resistance, collision resistance (can't find two inputs with the same output). Used for password storage, data integrity checks, digital signatures [^src4].

**Digital signatures**: use private key to sign (a hash of) a message; anyone with the public key can verify the signature. Provides authentication and non-repudiation [^src4].

**Authenticated encryption (AEAD)**: combines encryption and a MAC (message authentication code) to provide both confidentiality and integrity. Examples: AES-GCM, ChaCha20-Poly1305. Using encryption without authentication is almost always wrong — an attacker can modify ciphertext without detection [^src4].

## Distributed Security

In distributed systems, principals (users, servers) communicate over a network that may be hostile [^src5]:

**Key distribution problem**: how do two parties who have never met establish a shared secret key? Solutions:
- **Diffie-Hellman key exchange**: mathematical operation allowing two parties to derive a shared secret over a public channel without transmitting it
- **Public key infrastructure (PKI)**: Certificate Authorities (CAs) sign public keys, binding them to identities. TLS uses PKI

**Authentication over a network**:
- **Kerberos** (MIT, 1988): a trusted third party (KDC) issues short-lived tickets granting access to services. Client authenticates once to KDC; presents tickets to individual services. Avoids sending passwords over the network.
- **TLS/HTTPS**: X.509 certificate chain from a CA authenticates the server; mutual TLS (mTLS) authenticates both client and server [^src5].

**Secure channel**: even after mutual authentication, all communication must be encrypted and integrity-protected to prevent man-in-the-middle attacks [^src5].

## Related Corpus Pages

- [/software-engineering/operating-systems.md](/software-engineering/operating-systems.md) — kernel mode/user mode split; system calls; the OS as the security enforcement layer
- [/software-engineering/distributed-file-systems.md](/software-engineering/distributed-file-systems.md) — NFS/AFS trust model in distributed environments
- [/software-engineering/distributed-systems-fallacies.md](/software-engineering/distributed-systems-fallacies.md) — "the network is secure" is one of the eight fallacies
- [/software-engineering/sources/ostep-operating-systems-three-easy-pieces.md](/software-engineering/sources/ostep-operating-systems-three-easy-pieces.md) — OSTEP source summary

---

[^src1]: [OSTEP Introduction to Operating System Security (Peter Reiher, UCLA)](../../raw/_inbox/pdf-security-intro.md)
[^src2]: [OSTEP Authentication](../../raw/_inbox/pdf-security-authentication.md)
[^src3]: [OSTEP Access Control](../../raw/_inbox/pdf-security-access.md)
[^src4]: [OSTEP Protecting Information With Cryptography](../../raw/_inbox/pdf-security-crypto.md)
[^src5]: [OSTEP Distributed System Security](../../raw/_inbox/pdf-security-distributed.md)

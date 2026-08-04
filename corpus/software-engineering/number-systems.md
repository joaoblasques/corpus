---
type: concept
domain: software-engineering
status: draft
title: Number Systems
aliases:
  - binary
  - hexadecimal
  - octal
  - number bases
  - base conversion
  - hex
  - positional notation
sources:
  - type: pdf
    path: raw/pdf/pdf-a-cool-brisk-walk-through-discrete-mathematics-part-07.md
    channel: pdf
tags:
  - corpus/software-engineering
  - cs-fundamentals
  - systems
created: 2026-08-04
updated: 2026-08-04
confidence: 0.9
last_confirmed: 2026-08-04
---

# Number Systems

TL;DR: Computers store everything in binary (base 2), but programmers routinely work in hexadecimal (base 16) because it maps cleanly onto 4-bit nibbles. Understanding positional notation generalizes across all bases.

## Positional notation

In base b, a number with digits dₙdₙ₋₁...d₁d₀ has value:
`d₀ × b⁰ + d₁ × b¹ + ... + dₙ × bⁿ`

The "place values" from right to left are b⁰=1, b¹=b, b²=b², etc.[^1]

## Common bases in CS

| Base | Name | Digits | Why used |
|---|---|---|---|
| 2 | Binary | 0, 1 | Hardware — one bit per digit |
| 8 | Octal | 0–7 | Historical; 3 bits per digit |
| 10 | Decimal | 0–9 | Human default |
| 16 | Hexadecimal | 0–9, A–F | 4 bits per digit; compact for bytes |

## Hexadecimal

Base 16 requires 16 symbols: 0–9 and A (ten) through F (fifteen).[^1]

`72E3₁₆ = 7×4096 + 2×256 + 14×16 + 3×1 = 29,411₁₀`

**Why hex dominates low-level work**: one hex digit = exactly 4 bits (one nibble); two hex digits = one byte. Hardware registers, memory addresses, and color codes (RGB) are naturally expressed in hex.[^1]

Hex is used wherever you encounter "hardware, operating systems, device drivers, bit masks, or anything else low level."[^1]

## Base conversion

**Decimal → Binary**: repeatedly divide by 2, record remainders (LSB first).
**Binary → Hex**: group bits into groups of 4 from the right; convert each group.
**Hex → Binary**: expand each hex digit to its 4-bit binary representation.

## CS applications

- Memory addresses and pointer arithmetic (hex)
- Color values in HTML/CSS (#RRGGBB)
- Bitmasks and flags (`0xFF`, `0x01`)
- ASCII/Unicode code points
- Cryptographic hash output (SHA-256 shown as 64 hex characters)

See also: [Discrete Mathematics](/software-engineering/discrete-mathematics.md), [Data Structures and Big O Notation](/software-engineering/data-structures.md).

[^1]: raw/pdf/pdf-a-cool-brisk-walk-through-discrete-mathematics-part-07.md — Davies, Ch. 7 "Numbers."

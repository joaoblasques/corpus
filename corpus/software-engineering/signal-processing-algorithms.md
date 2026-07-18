---
type: concept
domain: software-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-28.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-29.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-30.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-31.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-32.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-33.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-34.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-35.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-36.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-37.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-38.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-39.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-40.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-41.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-42.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-43.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-44.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-45.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-46.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-47.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-48.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-49.md
    channel: pdf
    ingested_at: 2026-07-18
  - path: raw/_inbox/pdf-matters-computational-ideas-algorithms-source-code-part-50.md
    channel: pdf
    ingested_at: 2026-07-18
aliases:
  - FFT
  - fast Fourier transform
  - FHT
  - fast Hartley transform
  - Walsh transform
  - Walsh-Hadamard transform
  - Haar transform
  - CORDIC
  - number-theoretic transform
  - NTT
  - convolution algorithms
  - DFT
  - discrete Fourier transform
  - signal processing
  - digital signal processing
  - wavelet transforms
tags:
  - corpus/software-engineering
  - concept
created: 2026-07-18
updated: 2026-07-18
---

**TL;DR.** Signal processing algorithms convert sequences between time/space and frequency/transform domains. The computational importance is asymptotic: naive DFT costs O(n²) multiply-accumulate operations; the FFT and its relatives (FHT, Walsh, NTT) collapse that to O(n log n). These primitives underlie fast polynomial multiplication, exact integer arithmetic, error-correcting codes, and cryptographic building blocks. The primary reference throughout is Joerg Arndt's *Matters Computational* (FXT book), which provides working C++ implementations for every algorithm described below.

See [/software-engineering/algorithms.md](/software-engineering/algorithms.md) for general algorithm context.

---

## FFT: Fast Fourier Transform

### Definition and naive cost

The Discrete Fourier Transform (DFT) of a length-n sequence f is:

```
F[k] = sum_{j=0}^{n-1} f[j] * exp(-2*pi*i*j*k/n)
```

Direct evaluation requires O(n²) complex multiplications. For n = 2²⁰ ≈ 10⁶ that is ~10¹² operations — infeasible for real-time use.

### Cooley-Tukey radix-2 decomposition

The FFT exploits the periodicity of the twiddle factors. The Cooley-Tukey radix-2 decimation-in-time (DIT) algorithm recursively splits an n-point DFT into two n/2-point DFTs, reducing total work to O(n log₂ n). The butterfly operation at each stage:

```
F[j]    = E[j] + W^j * O[j]
F[j+n/2] = E[j] - W^j * O[j]
```

where E, O are the even- and odd-indexed sub-transforms and W = exp(-2πi/n) is the principal root of unity. The dual algorithm, decimation-in-frequency (DIF), applies the butterfly in the opposite order and requires a bit-reversal permutation at the end rather than the beginning.[^src29]

### Split-radix FFT

The split-radix algorithm (radix-2 on even indices, radix-4 on odd) achieves a lower operation count than pure radix-2 for most lengths. For n = 2^k it uses (4/3)n log₂ n − (8/3)n + 4 real multiplications, the minimum known for power-of-two lengths.[^src29]

### Mixed-radix and arbitrary-length FFT

When n is not a power of two, the Cooley-Tukey factorization generalises to arbitrary factor combinations (radix-3, radix-5, etc.). The Prime Factor Algorithm (Good-Thomas) handles n with coprime factors without twiddle multiplication between stages, reducing operation count further for highly composite n.[^src29]

### Localized (cache-friendly) FFT

Standard FFT has poor cache behavior for large n because stride-n/2 memory access pattern thrashes the cache. Localized variants (depth-first recursive decomposition) reorder the computation so that sub-transforms fit in L1 cache before the merge step. The FXT library includes `fft_loc_dit2_core` / `fft_loc_dif2_core` that gave >50% speedup over non-localized versions for large array convolutions.[^src30]

### Complexity summary

| Algorithm | Operations | Notes |
|-----------|-----------|-------|
| Naive DFT | O(n²) | No structure exploited |
| Radix-2 FFT | O(n log₂ n) | Power-of-2 n required |
| Split-radix FFT | ~(4/3)n log₂ n | Minimum known for 2^k |
| Mixed-radix FFT | O(n log n) | Arbitrary n |

---

## FHT: Fast Hartley Transform

### Hartley transform definition

The Discrete Hartley Transform (DHT) is a real-valued alternative to the FFT:

```
H[k] = sum_{j=0}^{n-1} f[j] * cas(2*pi*j*k/n)
```

where `cas(θ) = cos(θ) + sin(θ)`. Unlike the DFT, the Hartley transform maps real inputs to real outputs and is its own inverse (up to a factor of n).[^src30]

### Advantage over FFT for real data

A real FFT of length n requires two Hartley transforms of length n/2. This yields roughly a factor-of-2 reduction in arithmetic for real-valued signals compared to a complex FFT. The FHT is therefore preferred when the input is known to be real.[^src30]

### DIT and DIF FHT algorithms

Both decimation-in-time and decimation-in-frequency variants exist. The standard DIF radix-2 FHT core (`fht_dif2`) loops from the full length down to length 2, applying a Hartley-shift (rotation by ±45°) and sum/difference butterflies. The DIT variant (`fht_dit2`) applies a bit-reversal permutation first, then builds from length 2 upward:

```
// DIF pseudocode kernel (per stage)
for j=1 to mh-1:
    u = f[r+mh+j];  v = f[r+mh+k];
    f[r+mh+j] = u*cos + v*sin;  // Hartley-shift
    f[r+mh+k] = u*sin - v*cos;
    sumdiff(f[r+j], f[r+mh+j]);
    sumdiff(f[r+k], f[r+mh+k]);
```

Swapping the innermost loops over `j` vs. `r` reduces trig evaluations by a factor equal to the number of sub-arrays at each stage.[^src30]

### FFT via FHT

A complex FFT can be computed as two FHTs plus an O(n) post-processing step (`fht_fft_conversion`). The conversion exploits the symmetry relations between the Hartley and Fourier transforms. This is useful when a highly optimized FHT is available.[^src30]

### Convolution via FHT

Cyclic convolution of real sequences uses three FHTs plus an O(n) element-wise multiply with the `fht_mul` kernel:

```
// fht_mul: two Hartley-domain elements -> convolved pair
yi := v*(( yi + yj)*xi + (yi - yj)*xj)
yj := v*((-yi + yj)*xi + (yi + yj)*xj)
```

Avoiding the revbin permutation by using DIF/DIT core routines saves three O(n) passes and gave >50% speedup for the hfloat high-precision arithmetic library.[^src30]

---

## Walsh-Hadamard Transforms

### Walsh-Waksman (natural-order) transform

The Walsh-Hadamard transform (WHT) is a non-trigonometric transform over ±1 basis functions. The Walsh-Waksman (`walsh_wak`) algorithm consists purely of sum/difference butterflies with no trig:

```
for each stage: sumdiff(f[t1], f[t2])
```

Cost: O(n log n) additions, zero multiplications. This makes it faster than the FFT by a constant factor and useful wherever the multiplication-free property matters (e.g., arithmetic over GF(2)).[^src28]

### Ordering variants

Three standard orderings exist, corresponding to different permutations of the basis functions:

- **Walsh-Waksman (natural / Hadamard order)**: basis functions ordered by binary index.
- **Walsh-Paley order**: obtained by revbin-permuting then applying `walsh_wak`. Basis functions `(i, k)` element = `(-1)^parity(i & revbin(k))`.
- **Walsh-Sequency (Kaczmarz) order**: ordered by sequency — the number of sign changes per basis function, analogous to frequency. Computed as `walsh_wak` + `revbin_permute` + `inverse_gray_permute`. The sequency of a signal with frequency f is typically 2f.[^src28]

### Haar transform and localized variants

The Haar transform decomposes a signal into local sum/difference pairs at successive scales. It is the simplest wavelet transform. The DIF Haar algorithm:

```c
template <typename Type>
void haar_dif2(Type *f, ulong n) {
    for (ulong m=n; m>=2; m>>=1) {
        const ulong mh = (m>>1);
        for (ulong t1=0, t2=mh; t1<mh; ++t1, ++t2)
            sumdiff(f[t1], f[t2]);
    }
}
```

The localized Haar variant (`loc_dif2`) applies Haar transforms at positions f+2, f+4, f+6, ..., where the length at position f+s is determined by the lowest set bit in s. This is equivalent to a depth-first traversal of the transform tree and improves cache behavior for large arrays.[^src28]

### Dyadic (XOR) convolution

Walsh-Hadamard transforms enable XOR-convolution: `h[k] = sum_{i XOR j == k} f[i]*g[j]`. The algorithm is three WHTs plus element-wise multiply — identical structure to FFT-based cyclic convolution but with XOR replacing addition in the index. XOR-convolution appears in hypercomplex number multiplication and certain coding theory constructions.[^src28]

### Arithmetic transform

The arithmetic transform Y+ and its inverse Y− are obtained by replacing the sum/difference butterfly `{u+v, u-v}` with `{u, u+v}` or `{u, v-u}` respectively. The k-th element of Y+[f] equals `sum_{i subseteq k} f[i]` (sum over all bit-subsets of k). These transforms underlie inclusion-exclusion computations and subset-sum enumerations.[^src28]

---

## Convolution Algorithms

### Cyclic convolution via FFT/FHT

The standard method: forward transform both sequences, pointwise multiply, inverse transform, normalize by 1/n. For real sequences the FHT variant saves roughly half the arithmetic. The normalization can be absorbed into the pointwise multiply.[^src30]

### Negacyclic convolution

The negacyclic convolution wraps with a sign change: the n-point negacyclic convolution of a and b has `c[k] = sum_{i+j=k} a[i]*b[j] - sum_{i+j=k+n} a[i]*b[j]`. Computed via a Hartley-shift preprocess, FHT, pointwise `fht_mul`, inverse FHT, Hartley-shift postprocess. Used in high-precision multiplication (MFA algorithm).[^src30]

### Karatsuba multiplication

For polynomial/integer multiplication, Karatsuba's divide-and-conquer reduces 4 half-size multiplications to 3, giving complexity O(n^log₂(3)) ≈ O(n^1.585) versus O(n²) schoolbook. Recursive application yields the first sub-quadratic integer multiplication algorithm. For very large operands (millions of digits), FFT-based convolution is asymptotically faster; Karatsuba is preferred in the mid-size range.[^src50]

### Linear (aperiodic) convolution via zero-padding

To compute a length-(n+m-1) linear convolution with a cyclic transform: zero-pad both sequences to length ≥ n+m-1, then apply cyclic convolution. The padding overhead is at most a factor of 2 in transform length.[^src30]

---

## CORDIC Algorithms

### Principle

CORDIC (Coordinate Rotation DIgital Computer) computes trigonometric, hyperbolic, and related functions using only shifts and additions — no multiplications. A precomputed table of k entries (arctan(2^-k) values) gives approximately k bits of precision. The algorithm is well suited to hardware with no dedicated multiply unit.[^src35]

### Circular mode: sine and cosine

Initialize `(x, y, z) = (1/K, 0, θ)` and iterate:

```
d_k = sign(z_k)
x_{k+1} = x_k - d_k * 2^{-k} * y_k
y_{k+1} = y_k + d_k * 2^{-k} * x_k
z_{k+1} = z_k - d_k * arctan(2^{-k})
```

After n iterations, `x → cos(θ)` and `y → sin(θ)`. The scaling constant K = prod_{k=0}^{∞} 1/sqrt(1 + 2^{-2k}) ≈ 0.60725. For `θ = π/3`, convergence to 15+ correct digits in 15 iterations is demonstrated in the FXT source.[^src35]

The multiplications by `d_k` are sign changes; multiplications by `2^{-k}` are right shifts. All operations become shift-and-add after substitution.

### Vectoring mode (backward CORDIC)

Use `d_k = -sign(y_k)` instead. This converges to `z → arctan(y_0/x_0)`, enabling inverse trigonometric computation with the same iteration.[^src35]

### Unified three-mode formulation

| Mode | m | Table entries | Forward computes | Backward computes |
|------|---|--------------|-----------------|-------------------|
| Circular | +1 | arctan(2^-k) | sin, cos | arctan |
| Linear | 0 | 2^-k | multiply | divide |
| Hyperbolic | -1 | arctanh(2^-k) | sinh, cosh | arctanh, sqrt |

The hyperbolic case starts iteration at k=1 (not k=0) and some steps must be executed twice at indices 4, 13, 40, 121, ... (sequence i_{k+1} = 3*i_k + 1) to guarantee convergence.[^src35]

### Natural logarithm via hyperbolic CORDIC

`log(w) = 2 * arctanh((w-1)/(w+1))`. Initialize `x_1 = w+1`, `y_1 = w-1`, then `z → 2*log(w)` under backward hyperbolic CORDIC.[^src35]

---

## Number-Theoretic Transforms (NTT)

### Motivation

NTTs are FFTs computed in Z/mZ (integers modulo m) rather than the complex numbers. Because modular arithmetic is exact, NTTs compute exact convolutions — no floating-point rounding. The main application is exact polynomial multiplication for high-precision integer arithmetic.[^src30]

### Prime modulus condition

For a length-n NTT modulo prime p, the algorithm requires a primitive n-th root of unity in Z/pZ. In GF(p), elements of order r exist for all divisors r of p-1 (Fermat's little theorem). Therefore the NTT length n must divide p-1:

```
n | (p - 1)
```

For power-of-2 NTTs, primes of the form `p = v * 2^k + 1` are used. Example 63-bit NTT-prime: `p = 3 * 29 * 2^56 + 1`. Example 64-bit: `p = 27 * 2^59 + 1`.[^src30]

Primes suitable for NTTs (sometimes called FFT-primes) can be found with the program `fxt/mod/fftprimes-demo.cc`.[^src30]

### Implementation

Replace the complex twiddle factor `exp(±2πi/n)` with a primitive n-th root r in Z/pZ. The inverse transform uses r^{-1} mod p. The radix-2 DIT/DIF butterfly structure is identical to the complex FFT:

```
// Radix-2 DIT NTT butterfly
u = a[t1];  v = a[t2] * w^j mod p;
a[t1] = (u + v) mod p;
a[t2] = (u - v) mod p;
```

Key difference: use trigonometric recursion in its most naive form because computing roots of unity is expensive in modular arithmetic (no analytic formula).[^src30]

### Mixed-radix NTT for non-power-of-2 lengths

NTTs modulo primes supporting lengths dividing `2^40 * 3^2 * 5^2 * 7` extend the useful length range beyond powers of two. Suitable primes are tabulated in `fxt/mod/moduli.txt`.[^src30]

### CRT-based multi-modulus NTT

To compute a convolution whose output values exceed a single modulus, compute the NTT modulo multiple primes p1, p2, ..., then apply the Chinese Remainder Theorem (CRT) to recover the true result modulo p1*p2*...[^src40]

---

## Galois Fields GF(2^n)

### Structure

GF(2^n) is the finite field with 2^n elements. Elements are polynomials of degree < n over GF(2), represented as n-bit integers. Addition is bitwise XOR; multiplication is polynomial multiplication modulo an irreducible polynomial c(x) of degree n over GF(2).[^src45]

### Irreducible and primitive polynomials

An irreducible polynomial of degree n over GF(2) cannot be factored over GF(2). A primitive polynomial additionally has the property that its root generates the entire multiplicative group of GF(2^n). Primitive polynomials of degree n are required for:
- LFSR sequences of maximal period 2^n - 1
- CRC polynomials with full error-detection period
- NTT-like operations over GF(2^n)

The number of primitive polynomials of degree n is φ(2^n - 1)/n where φ is Euler's totient.[^src45]

### LFSR sequences (m-sequences)

A Linear Feedback Shift Register (LFSR) with primitive polynomial c(x) of degree n generates a maximal-length sequence (m-sequence) of period 2^n - 1 before repeating. Two physical setups exist:[^src45]

**Galois setup**: each step, detect whether a 1 is shifted out; if so, XOR with the polynomial modulus. Preferred because `parity()` is not needed:

```c
ulong galois_right(ulong x, ulong c) {
    ulong s = (x & 1UL);
    x >>= 1;
    if (s) x ^= (c>>1);
    return x;
}
```

**Fibonacci setup**: each step, compute parity of tapped bits and shift the result in. Mathematically equivalent but slower on most hardware because parity computation is expensive.

### CRC as GF(2) polynomial hashing

A CRC of degree d computes `h = s mod c` where s is the binary polynomial of the input stream and c is a primitive polynomial of degree d. A 64-bit CRC with a primitive polynomial provides collision probability 2^-64 ≈ 5.42 × 10^-20 per input pair. The FXT `crc64` class uses the Galois setup with a lookup table (256 entries, 4-bit or 8-bit) for throughput optimization.[^src45]

> "The probability that different sequences have the same CRC equals 2^{-64} ≈ 5.42 · 10^{-20}." [^src45]

### Applications in error-correcting codes

GF(2^n) arithmetic underlies BCH and Reed-Solomon codes. In RS codes, codeword symbols are elements of GF(2^8) or GF(2^16); the generator polynomial has roots at consecutive powers of a primitive element α. Syndrome decoding requires polynomial arithmetic over GF(2^n), specifically computation of minimal polynomials and extended Euclidean algorithm in the field.[^src45]

---

## Modular Arithmetic

### Basic operations

All operations in Z/mZ reduce results modulo m after each step. Addition and subtraction: `(a ± b) mod m`. Multiplication requires care — for 64-bit a, b, and m, the product may overflow 64 bits. The FXT `mod` class handles this via `__int128` or Montgomery form.[^src40]

### Modular inverse

The inverse of a in Z/mZ (when gcd(a, m) = 1) can be computed by:
- Extended Euclidean algorithm: O(log m) steps
- Fermat's little theorem (prime m only): `a^{-1} = a^{m-2} mod m` via fast exponentiation

### Chinese Remainder Theorem (CRT)

Given pairwise coprime moduli m_1, ..., m_k and residues x_1, ..., x_k, CRT reconstructs the unique R in [0, M) where M = m_1 * ... * m_k such that R ≡ x_i (mod m_i) for all i:

```c
// CRT reconstruction (from FXT: mod/chinese.cc)
for (int i=0; i<n; ++i) {
    Ti = M / m_i;                         // exact division
    ci = inv_modpp(Ti, p_i, exp_i);       // Ti^{-1} mod m_i
    Xi = mul_mod(ci * Ti, x[i], M);       // contribution
    R  = add_mod(R, Xi, M);
}
```

CRT is essential for multi-modulus NTT: compute the NTT modulo each of k small primes, then reconstruct the true result using CRT.[^src40]

### Square roots modulo p

For prime p and quadratic residue a (where a^{(p-1)/2} ≡ 1 mod p), the Tonelli-Shanks algorithm finds sqrt(a) mod p. The special cases `p ≡ 3 (mod 4)` → `sqrt(a) = a^{(p+1)/4} mod p` and `p ≡ 5 (mod 8)` have closed forms. The FXT library provides `sqrt_mod()` for general p.[^src40]

### Primitive roots and the structure of GF(p)

For prime p, the multiplicative group GF(p)* = (Z/pZ)* has order p-1 and is cyclic. A primitive root (generator) g satisfies g^k ≠ 1 for all 0 < k < p-1. To test: check that g^{(p-1)/q} ≠ 1 for all prime divisors q of p-1. In practice, a primitive root is found after O(log p) random trials.[^src40]

For NTTs, the primitive n-th root of unity in GF(p) is `r = g^{(p-1)/n}` where g is a primitive root mod p.[^src40]

---

## Implementation Notes (FXT Library)

All algorithms described here are implemented in the FXT library (Joerg Arndt). Source references follow the pattern `[FXT: path/to/file.cc]`. Key modules:

| Module | Content |
|--------|---------|
| `fft/` | Complex FFT, split-radix, localized variants |
| `fht/` | Real FHT, DIT/DIF, convolution cores |
| `walsh/` | Walsh-Waksman, Walsh-Paley, Walsh-Sequency, Haar, dyadic convolution |
| `mod/` | Modular arithmetic class, CRT, prime finding, NTT primes |
| `gf2n/` | GF(2^n) arithmetic, irreducible polynomials, LFSR |
| `arith/` | CORDIC (circular, linear, hyperbolic) |
| `bits/` | CRC32/CRC64, parallel CRC |
| `convolution/` | FHT/FFT/NTT-based cyclic/negacyclic/XOR convolution |

---

[^src28]: [Matters Computational part 28, Chapter 23](../../raw/pdf/pdf-matters-computational-ideas-algorithms-source-code-part-28.md) — Walsh transform and relatives (Walsh-Paley, Walsh-Sequency, Haar, localized transforms, XOR-convolution, arithmetic transform)
[^src29]: [Matters Computational part 29, Chapter 21](../../raw/pdf/pdf-matters-computational-ideas-algorithms-source-code-part-29.md) — Complex FFT algorithms (radix-2 DIT/DIF, split-radix, mixed-radix, matrix Fourier algorithm)
[^src30]: [Matters Computational part 30, Chapters 25–26](../../raw/pdf/pdf-matters-computational-ideas-algorithms-source-code-part-30.md) — Fast Hartley Transform (DIT/DIF, convolution via FHT, negacyclic convolution, localized FHT); Number-theoretic transforms (prime moduli, radix-2 NTT)
[^src35]: [Matters Computational part 35, Chapter 33](../../raw/pdf/pdf-matters-computational-ideas-algorithms-source-code-part-35.md) — CORDIC algorithms (circular/linear/hyperbolic modes, shift-and-add computation of trig functions)
[^src40]: [Matters Computational part 40, Chapter 39](../../raw/pdf/pdf-matters-computational-ideas-algorithms-source-code-part-40.md) — Modular arithmetic (CRT, order of elements, primitive roots, GF(p) structure)
[^src45]: [Matters Computational part 45, Chapter 41](../../raw/pdf/pdf-matters-computational-ideas-algorithms-source-code-part-45.md) — Shift registers (Galois/Fibonacci setup, LFSR m-sequences, CRC as polynomial hashing, GF(2^n) applications)
[^src50]: [Matters Computational part 50, Index](../../raw/pdf/pdf-matters-computational-ideas-algorithms-source-code-part-50.md) — Index entries confirming topics: Karatsuba multiplication, NTT, normal bases GF(2^n), modular arithmetic, convolution types

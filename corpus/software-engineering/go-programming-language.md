---
type: concept
domain: software-engineering
status: draft
sources:
  - path: raw/youtube/youtube-8uiZC0l4Ajw-learn-go-fast-full-tutorial.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/email/email-2026-06-18-is-go-still-worth-learning-in-2026.md
    channel: email
    ingested_at: 2026-06-25
  - path: raw/github/github-d3witt-viking.md
    channel: github
    ingested_at: 2026-06-25
aliases:
  - Go
  - Golang
  - goroutines
  - Go language
  - Go concurrency
  - Go CLI
  - Go backend
  - Go infrastructure
tags:
  - corpus/software-engineering
  - concept
created: 2026-06-25
updated: 2026-06-25
---

# Go Programming Language

**TL;DR**: Go is a statically typed, compiled language with built-in concurrency (goroutines) and a simplicity-first design philosophy. Compiles to native binaries ~120x faster than Python at runtime; compile times themselves are fast. Error handling is a return type, not exceptions. Zero-value defaults, unused-import enforcement, and mandatory variable use make Go unusually strict about clean code at compile time [^src1].

## Six core characteristics

| Characteristic | Detail |
|---|---|
| **Statically typed** | Types declared or inferred; cannot change without explicit conversion |
| **Strongly typed** | Operations gated by type — can't add `int + string` as in JavaScript |
| **Compiled** | Produces a standalone binary; no runtime interpreter overhead |
| **Fast compilation** | Short compile → test cycles; developer-friendly feedback loop |
| **Built-in concurrency** | Goroutines in the language, not a library add-on |
| **Simplicity** | Garbage collection; concise syntax; aims for less code with more clarity |

Speed comparison: a loop counting to 100 million runs in ~50ms in Go vs ~6 seconds in Python — "about 120 times faster" [^src1].

## Module and package structure

- A **package** is a folder of `.go` files [^src1].
- A **module** is a collection of packages; initialized with `go mod init <name>` [^src1].
- The `go.mod` file records the module name, Go version, and external dependencies.
- Convention: module name mirrors its GitHub repository path.
- The `main` package is special: the compiler looks here for the `main()` function as the program entry point [^src1].

## Type system

**Integer types**: `int`, `int8`, `int16`, `int32`, `int64` (and unsigned variants `uint*`). Default `int` is 32 or 64 bits depending on system architecture [^src1]. Overflow at compile time raises an error; overflow at runtime silently wraps — "moral of the story is, think about what data types you're using" [^src1].

**Float types**: `float32`, `float64` only — no bare `float`. `float32` loses precision; `float64` needed for correct decimal representation in most cases [^src1].

**Strings**: UTF-8. `len()` returns bytes, not characters. For character count on non-ASCII strings, use `unicode/utf8.RuneCountInString()` [^src1].

**Default (zero) values** — Go initializes all variables:
- `int`, `float`, `rune` → `0`
- `string` → `""`
- `bool` → `false`
- pointers, slices, maps, functions, interfaces → `nil`

**Compiler strictness rules** (uncommon in other languages) [^src1]:
- Unused imports are compile errors.
- Unused variables are compile errors.
- Missing `return` is a compile error.
- Opening `{` must be on the same line as the statement (no new-line-before-brace).

## Functions and error handling

Functions can return multiple values [^src1]. The canonical pattern for recoverable errors: return `(value, error)` where `error` is `nil` on success [^src1]:

```go
func divide(a, b int) (int, error) {
    if b == 0 {
        return 0, errors.New("divide by zero")
    }
    return a / b, nil
}

result, err := divide(10, 0)
if err != nil {
    fmt.Println(err)
}
```

"Handling errors in this way is a general design pattern in Go. If you import functions from other packages, a lot of the time they will return an error type in addition to other outputs." [^src1]

There are no exceptions in Go; all errors travel as explicit return values.

## Slices vs arrays

**Arrays** are fixed-length, zero-indexed, stored in contiguous memory [^src1]. Length is part of the type — `[3]int` and `[4]int` are different types.

**Slices** are "wrappers around arrays" with dynamic length [^src1]. When `append` exceeds capacity, Go allocates a new underlying array and copies — capacity typically doubles. Gotcha: pre-allocating with `make([]T, length, capacity)` avoids repeated reallocations in performance-sensitive code [^src1].

## Maps

Key-value store declared as `map[KeyType]ValueType`. Uninitialized map reads return zero values; writes to nil maps panic. Initialize with `make(map[KeyType]ValueType)` or a map literal [^src1].

## Concurrency: goroutines

Built into the language — no third-party concurrency library required [^src1]. A goroutine is launched with `go funcName()`. Channels coordinate goroutines. This design is what makes Go attractive for servers, CLIs, and systems tooling where concurrency is the norm, not the exception.

## Variable declaration patterns

Three common forms [^src1]:

```go
var x int = 5          // explicit type
var x = 5              // inferred type
x := 5                 // shorthand (inferred, inside functions only)
```

**Best practice**: specify the type when not obvious from the value, especially for function return values — "if you use shorthand here, you really have no idea what myVar is unless you hover over it" [^src1].

## Constant vs variable

`const` must be initialized at declaration; cannot be changed afterward [^src1]. Use for values that must not drift (e.g., `pi`, status codes).

## Switch statements

Go's `switch` breaks implicitly — no `fallthrough` needed [^src1]. Two forms:
- `switch variable { case value: ... }` — equality matching
- `switch { case condition: ... }` — conditional (equivalent to `if/else if` chain)

## When Go is (and isn't) the right choice

Go's sweet spots [^src2]:

| Domain | Fit |
|---|---|
| Backend development / APIs | Strong — static typing + concurrency + fast binaries |
| Cloud services | Strong — no runtime overhead; deploys cleanly |
| DevOps/infrastructure tools | Strong — build a binary, deploy without a huge runtime |
| Command-line tools | Strong — goroutines; clean std lib |
| Networking | Strong — built-in concurrency model |
| Data science / ML | Poor — Python is the practical choice |
| Frontend / general web | Poor — JavaScript is the obvious starting point |

Go trade-offs [^src2]:

- **Verbose**: error handling is explicit `if err != nil` repetition everywhere
- **Barebones**: "Go is not trying to be clever. It is trying to be simple, practical, and predictable" [^src2]
- **Not expressive**: fewer abstractions than Python/Ruby; intentional

Go shines for teams building systems "that need to be maintained, deployed, and understood by more than one person" [^src2].

## Viking — example Go CLI tool

**Viking** (★752) by d3witt is a Go CLI tool for managing remote machines and SSH keys — a bare-metal alternative to cloud management consoles [^src3]. Commands: `exec`, `copy/cp`, `key`, `machine`, `config`. Installs via `go install` into a single static binary (`CGO_ENABLED=0`); topics: bare-metal, CLI, deploy, SSH, VM [^src3].

## See also

- [[software-engineering/data-structures|Data Structures and Big O Notation]] — Go slices/maps implement the same underlying structures
- [[software-engineering/software-design-principles|Software Design Principles]] — Go's compiler-enforced constraints (no unused vars/imports) operationalize the simplicity principle
- [[software-engineering/algorithms|Algorithms]] — Go is widely used for algorithm implementations

---

[^src1]: [Learn GO Fast: Full Tutorial (Alex Mux)](../../raw/youtube/youtube-8uiZC0l4Ajw-learn-go-fast-full-tutorial.md)
[^src2]: [Is Go Still Worth Learning in 2026? (Tech With Tim)](../../raw/email/email-2026-06-18-is-go-still-worth-learning-in-2026.md)
[^src3]: [viking (d3witt)](../../raw/github/github-d3witt-viking.md)

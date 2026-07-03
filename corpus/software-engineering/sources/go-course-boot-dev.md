---
type: source
domain: software-engineering
status: draft
sources:
  - path: raw/youtube/youtube-un6ZyFkqFKo-go-programming-golang-course-with-bonus-projects.md
    channel: youtube
    ingested_at: 2026-06-26
aliases:
  - Go Golang Course with Bonus Projects
  - boot.dev Go course
  - freeCodeCamp Go course
  - Lane Wagner Go course
tags:
  - corpus/software-engineering
  - source
created: 2026-06-26
updated: 2026-06-26
---

# Source: Go Programming — Golang Course with Bonus Projects (boot.dev / freeCodeCamp)

**TL;DR**: A comprehensive beginners' Go course by Lane Wagner (founder of boot.dev) published via freeCodeCamp. Structured as 100+ hands-on coding lessons plus seven real-world projects, taught around a single running example product called **Textio** (a Twilio-like backend SMS service). The course is one part of boot.dev's full backend-developer career path [^src1].

## Structure and pedagogy

"We're going to start by doing over 100 hands-on coding lessons and exercises," after which learners "go build a production-ready backend server in Go from scratch" [^src1]. The instructor explicitly warns against passive watching — "Tutorial Hell is a very real place" — and insists learners code ahead of him [^src1]. Code samples are hosted on boot.dev (free account) with a GitHub repo mirror [^src1].

The course advertises **seven real-world projects**, "ranging from building an RSS aggregator to implementing authentication with API keys" [^src1].

## Running example: Textio

Most lessons build small pieces of **Textio**, described as "a kind of back-end" product comparable to Twilio (an SMS-sending service) [^src1]. Concrete exercises threaded through the course include:

- choosing `float64` over `int` to store a fractional per-text price [^src1];
- a computed constant for "the number of seconds in an hour" to handle message-timing logic [^src1];
- a general `employee` **interface** with full-time and contractor structs (adding a `getSalary` method so the contractor "fulfills the employee interface") [^src1];
- 2D slices ("a slice of slices") to back message-analytics graphs and dashboards [^src1];
- **closures** — a `concatter` returning a function that accumulates onto a shared `doc` variable across calls (the "Harry Potter aggregator" example) [^src1];
- **middleware** for HTTP handlers, "injecting some additional logic into a function," previewed as part of the final backend-server project [^src1].

## Concept curriculum (concurrency, generics)

Beyond fundamentals, the course covers Go's concurrency and generics depth using Textio scenarios [^src1]:

- **Goroutines** spawned with `go func(){...}()`; ordering across them is non-deterministic [^src1].
- **Channels** as goroutine-safe FIFO queues; same-goroutine send/receive deadlocks (fixed by sending in a separate goroutine); signal-only channels passing empty-struct tokens; **buffered** channels for batch writes; closing a channel with the `v, ok := <-ch` drained check; `range` over a channel; **`select`** to multiplex channels; `time.Tick`/`time.After` timer channels [^src1].
- **Mutexes** (`sync.Mutex`, "mutual exclusion") with `Lock`/`defer Unlock` to guard shared state; `sync.RWMutex` (`RLock`/`RUnlock`) for read-heavy paths [^src1].
- **Generics / type parameters** — solve the pre-generics problem of rewriting `SplitIntSlice` per type or casting empty interfaces at runtime; the compiler keeps generic code type-safe; generics use interfaces as constraints under the hood [^src1].
- **Comparable map keys** — strings/numbers/booleans/structs work; slices/maps/functions cannot be keys; a struct can serve as a composite key [^src1].

## Capstone: RSS-aggregator backend server

The final project builds a production-shaped HTTP backend from scratch [^src1]:

- **`chi` router**, routes under `/v1/...`; `respondWithJSON`/`respondWithError` helpers; struct `json:"..."` tags mapping DB structs to clean API models; deliberate REST status codes (`201` created, `403` forbidden) [^src1].
- **Database** via raw SQL: **sqlc** generates type-safe Go from queries, **Goose** runs migrations; both via `go install` [^src1].
- **API-key auth**: a 64-char unique not-null key column (default generated in SQL so the migration backfills existing users); an `auth` package extracts the key from an `Authorization: ApiKey <key>` header [^src1].
- **Auth middleware**: an `authedHandler` wrapper returns a closure that grabs the key, fetches the user, then calls the real handler — DRYing authentication across protected endpoints (users, feeds, feed-follows) [^src1].
- The `context` package threads request cancellation through goroutines [^src1].

## Go positioning (per the course)

- "Go has been exploding in popularity… all the most modern tech companies are using Go to build scalable backend infrastructure" [^src1].
- On execution speed: Go is "much faster than JavaScript, Python, Ruby, and PHP" — any interpreted language [^src1]. On **compilation** speed it beats other compiled languages, which "increases developer productivity quite a bit" [^src1].
- Nuance: although Go compiles natively (like Rust/C/C++), its runtime execution speed is "more similar to Java and C Sharp" because of the **Go runtime** — "a chunk of code that's included in every Go program that manages memory" — though Go "tends to use much less memory than Java and C Sharp" since there's no full virtual machine [^src1].
- On package import paths: "when a package isn't part of the standard library… the import path is typically the same as the remote URL that you'd use to go look at that library's source code" [^src1].

## Relationship to the corpus

Corroborates and extends [Go Programming Language](/software-engineering/go-programming-language.md) (compiled-vs-interpreted speed, the Go runtime memory trade-off, interfaces, slices, import-path convention). Its project-driven structure complements the project list already on that page (Dreams of Code's five projects) and the syntax-first [Tech With Tim full course](/software-engineering/sources/go-full-course-tech-with-tim.md).

## See also

- [Go Programming Language](/software-engineering/go-programming-language.md) — the concept page this source feeds
- [Go Full Course (Tech With Tim)](/software-engineering/sources/go-full-course-tech-with-tim.md) — the syntax-first counterpart course
- [FastAPI](/software-engineering/fastapi.md) — comparable backend-API building, in Python

---

[^src1]: [Go Programming — Golang Course with Bonus Projects (boot.dev / freeCodeCamp)](../../../raw/youtube/youtube-un6ZyFkqFKo-go-programming-golang-course-with-bonus-projects.md)

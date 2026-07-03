---
type: concept
domain: software-engineering
status: draft
sources:
  - path: raw/youtube/youtube-TjjKcgtlsY8-javascript-speed-course-learn-javascript-in-75-minutes.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-javascript-speed-report.md
    channel: notes
    ingested_at: 2026-06-25
  - path: raw/github/github-lydiahallie-javascript-questions.md
    channel: github
    ingested_at: 2026-06-25
  - path: raw/github/github-ryanmcdermott-clean-code-javascript.md
    channel: github
    ingested_at: 2026-06-25
  - path: raw/github/github-trekhleb-javascript-algorithms.md
    channel: github
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-WoNmm4YS8e4-6-hours-of-javascript-projects-from-beginner-to-advanced.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-6-hours-of-javasc-report.md
    channel: notes
    ingested_at: 2026-06-25
aliases:
  - JavaScript
  - JS
  - var
  - let
  - const
  - template literals
  - JavaScript primitives
  - npm
  - Node.js
  - hoisting
  - block scope
  - function scope
  - clean code JavaScript
tags:
  - corpus/software-engineering
  - concept
created: 2026-06-25
updated: 2026-06-25
---

# JavaScript Fundamentals

**TL;DR**: JavaScript is the language of the web — runs in every browser and (via Node.js) on the server. Dynamically typed, weakly typed, and quirky: `null` and `undefined` are distinct; `var` is function-scoped and hoisted while `let`/`const` are block-scoped. Template literals (backtick strings) embed variables directly. NPM manages packages; `package.json` tracks dependencies [^src1].

## Running JavaScript

Two environments [^src1]:

- **Browser**: embed `<script>` tag in HTML or reference external `.js` file; output to console via DevTools
- **Node.js** (server/CLI): `node script.js` — no DOM, no `window`, but full filesystem + network access

For backend user input, `prompt-sync` npm package offers synchronous readline [^src1].

## Primitive data types

Five core primitives [^src1]:

| Type | Notes |
|---|---|
| `string` | Single quotes, double quotes, or backticks (template literals) |
| `boolean` | `true` / `false` (lowercase) |
| `number` | All numbers — integer or float — are this type |
| `undefined` | Variable declared but not assigned; also the type's only value |
| `null` | Explicitly assigned "no value" — distinct from `undefined` |

`undefined` vs `null`: "you use null when you want to explicitly set something as nothing; undefined is more used when you haven't yet assigned a value but will later" [^src1].

Two additional primitives exist but are rarely encountered in typical code: `BigInt` (large integers beyond `Number.MAX_SAFE_INTEGER`) and `Symbol` [^src1].

## Variable declaration: `var` vs `let` vs `const`

| Keyword | Scope | Re-assignable | Hoisted |
|---|---|---|---|
| `var` | Function | Yes | Yes (to `undefined`) |
| `let` | Block | Yes | No (temporal dead zone) |
| `const` | Block | No | No |

Key quirk: `let` and `const` are block-scoped — a variable declared inside an `if` block is not accessible outside it [^src1]. `var` leaks out of blocks (only contained by functions).

`const` prevents reassignment of the binding, not mutation of the value: an array stored in `const` can have elements pushed/popped; a new array cannot be assigned to the same name [^src1].

Naming convention: **camelCase** (not snake_case as in Python) [^src1].

## Template literals

Backtick strings embed variables via `${expression}` — equivalent to Python f-strings [^src1]:

```js
const v = 64;
console.log(`V is equal to ${v}`);  // "V is equal to 64"
```

Standard quotes do not interpolate — a common mistake when switching from languages with simpler string formatting [^src1].

## Clean Code JavaScript patterns

The `clean-code-javascript` repo (★94,451) adapts Robert Martin's *Clean Code* for JavaScript, covering variables, functions, objects, classes, SOLID, testing, error handling, and formatting [^src3]. Core framing: producing "readable, reusable, and refactorable" code. See also [Software Design Principles](/software-engineering/software-design-principles.md) for the language-agnostic versions.

## Advanced JavaScript questions reference

`javascript-questions` (★65,321) by Lydia Hallie is a long-form collection of quiz questions covering advanced JavaScript behavior — scope, closures, prototype chain, `this`, async/await — useful for interview prep [^src2]. Note: created 2019, covers JavaScript as of ES2019 syntax.

## Algorithms and data structures in JavaScript

`javascript-algorithms` (★196,120) by Trekhleb is a reference implementation of major algorithms and data structures in JavaScript, with explanations and links to further reading [^src4]. Organized by:
- Data structures: linked lists, stacks, queues, hash tables, heaps, trees, graphs
- Algorithms: sorting, searching, graph traversal, dynamic programming, bit manipulation

See [Algorithms](/software-engineering/algorithms.md) and [Data Structures and Big O Notation](/software-engineering/data-structures.md) for concepts.

## npm and package management

`npm init` creates a `package.json` [^src1]. `npm install <package>` installs and records the dependency; `node_modules/` holds the installed files; `package-lock.json` locks exact versions. The `require()` syntax imports CommonJS modules; `import/export` is the ES module syntax.

## Learning-by-building: project-based approach

A 6-hour compilation course (15 projects, beginner → advanced) demonstrates **vanilla JS first** — fundamentals like DOM manipulation and event handling before any framework [^src5]. Pedagogy rationale: "skills built by shipping 15 small projects in ascending difficulty rather than studying theory in isolation" [^src5].

Key early patterns from projects [^src5]:

- **`prompt()`-driven console loops** — read user input, compare, branch, repeat (number-guessing game)
- **Pseudo-random number generation**: `Math.round(Math.random() * 100)` for a bounded random target
- **DOM event handling**: button `click` listeners mutating page state (Color Flipper: swapping `body` background)
- **Timestamp-indexed long-form content**: video chapters via description timestamps so it works as a jump-around reference

Format note: long-form screencast (6+ hrs), low cut rate (~0.1 cuts/min), mean shot ~605 seconds — sustained screen-share tutorial paced by the build, not the edit [^src6].

## See also

- [Software Design Principles](/software-engineering/software-design-principles.md) — SOLID applied to any language including JavaScript
- [Algorithms](/software-engineering/algorithms.md) — strategies applicable to JS implementations
- [Data Structures and Big O Notation](/software-engineering/data-structures.md) — runtime complexity of JS built-in types
- [Bun](/software-engineering/bun.md) — alternative all-in-one JS runtime / toolkit

---

[^src1]: [JavaScript Speed Course — Learn JavaScript in ~75 Minutes (Tech With Tim)](../../raw/youtube/youtube-TjjKcgtlsY8-javascript-speed-course-learn-javascript-in-75-minutes.md)
[^src2]: [javascript-questions (Lydia Hallie)](../../raw/github/github-lydiahallie-javascript-questions.md)
[^src3]: [clean-code-javascript (Ryan McDermott)](../../raw/github/github-ryanmcdermott-clean-code-javascript.md)
[^src4]: [javascript-algorithms (Trekhleb)](../../raw/github/github-trekhleb-javascript-algorithms.md)
[^src5]: [6 Hours of JavaScript Projects - From Beginner to Advanced (Tech With Tim)](../../raw/youtube/youtube-WoNmm4YS8e4-6-hours-of-javascript-projects-from-beginner-to-advanced.md)
[^src6]: [Report: 6 Hours of JavaScript Projects (Obsidian analysis)](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-6-hours-of-javasc-report.md)

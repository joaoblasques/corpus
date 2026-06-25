---
type: entity
domain: software-engineering
status: stub
sources:
  - path: raw/github/github-frontendmasters-react-enlightenment.md
    channel: github
    ingested_at: 2026-06-25
aliases:
  - React
  - React.js
  - ReactJS
  - JSX
  - React Enlightenment
  - React components
  - React nodes
  - virtual DOM
tags:
  - corpus/software-engineering
  - entity
created: 2026-06-25
updated: 2026-06-25
---

# React

**TL;DR**: React is a JavaScript library for building user interfaces through declarative, composable components. Its foundational model: define components that describe what the UI should look like, and React manages efficient DOM updates. **React Enlightenment** (FrontendMasters / Cody Lindley) is a terse cookbook-style introduction covering React fundamentals from nodes through components, JSX, state, and events [^src1].

## Core model

React builds UIs out of **React nodes** — the fundamental unit. A node is created via `React.createElement()` or, more commonly, JSX syntax [^src1].

The lifecycle from the React Enlightenment curriculum [^src1]:

1. **React Nodes** — what a node is, how to create one, render to DOM
2. **JSX** — JavaScript Syntax Extension: syntactic sugar over `React.createElement()` calls; compiled by Babel
3. **React Components** — functions (or classes) that return React nodes; can accept props
4. **Component Lifecycle** (class components: mounting → updating → unmounting)
5. **State and events** — `this.setState()` / `useState()` triggers re-renders
6. **Props** — read-only data passed from parent to child; `defaultProps` for fallbacks
7. **Inline styles** — CSS-in-JS via style objects (camelCase keys)

## JSX essentials

JSX is not HTML — it compiles to `React.createElement(type, props, ...children)` calls [^src1]. Key rules:
- A single root element must wrap sibling elements
- `className` not `class`; `htmlFor` not `for`
- JavaScript expressions embedded in `{}`
- Self-closing tags required: `<img />`, not `<img>`
- Event handlers use camelCase: `onClick`, `onChange`

## React Enlightenment reference

Written by Cody Lindley, sponsored by Frontend Masters [^src1]. Terse cookbook format (like jQuery Enlightenment, JavaScript Enlightenment, DOM Enlightenment series). Available at reactenlightenment.com. GitHub repo: 427 stars, HTML-format docs organized as a gitbook. CC BY-NC-ND 3.0 license [^src1].

## See also

- [[software-engineering/javascript-fundamentals|JavaScript Fundamentals]] — React requires JS fluency (closures, `this`, async, modules)
- [[software-engineering/system-design-fundamentals|System Design Fundamentals]] — micro-frontends and design systems extend React at scale
- [[software-engineering/bun|Bun]] — alternative JS runtime and bundler compatible with React projects

---

[^src1]: [React Enlightenment (FrontendMasters / Cody Lindley)](../../raw/github/github-frontendmasters-react-enlightenment.md)

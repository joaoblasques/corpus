---
type: entity
domain: software-engineering
status: draft
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
updated: 2026-07-18
---

# React

**TL;DR**: React is a JavaScript library for building user interfaces through declarative, composable components. Its foundational model: define components that describe what the UI should look like, and React manages efficient DOM updates. **React Enlightenment** (FrontendMasters / Cody Lindley) is a terse cookbook-style introduction covering React fundamentals from nodes through components, JSX, state, and events [^src1].

## Core model

React builds UIs out of **React nodes** — the fundamental unit. A node is created via `React.createElement()` or, more commonly, JSX syntax [^src1].

The React Enlightenment curriculum covers these topics in order [^src1]:

1. **What Is React** — library overview and semantics/terminology
2. **React & Babel Setup** — `react.js` + `react-dom.js`, JSX via Babel, ES6/ES*, JSFiddle
3. **React Nodes** — what a node is, creating nodes, rendering to DOM, attributes/props, inline CSS, built-in element factories, node events
4. **JSX** — JavaScript Syntax Extension: expressions, comments, inline CSS, attributes/props, events
5. **Basic React Components** — what a component is, creating components, single root node constraint, component instances, events, composition, lifecycle, children, `ref` attribute, re-rendering
6. **React Component Props** — sending/getting props, default props, non-string props, prop validation
7. **React Component State** — what state is, working with state, state vs. props, stateless function components

## JSX essentials

JSX is not HTML — it compiles to `React.createElement(type, props, ...children)` calls [^src1]. Key rules:
- A single root element must wrap sibling elements
- `className` not `class`; `htmlFor` not `for`
- JavaScript expressions embedded in `{}`
- Self-closing tags required: `<img />`, not `<img>`
- Event handlers use camelCase: `onClick`, `onChange`
- JSX supports inline CSS, JS comments, and attribute/prop definitions as first-class features

## Components

React components are the building blocks of a UI — each returns React nodes and can be composed into larger trees [^src1]. Key component concepts from the curriculum:

- **Single root constraint**: a component must return one starting node/component [^src1]
- **Component instances**: how to refer to an instance after creation [^src1]
- **Events on components**: defining and handling DOM events at the component level [^src1]
- **Composition**: combining components into parent/child trees [^src1]
- **Lifecycle** (class components): mounting → updating → unmounting phases [^src1]
- **Children**: accessing child components/nodes via `props.children` [^src1]
- **`ref` attribute**: direct access to underlying DOM node or component instance [^src1]
- **Re-rendering**: how and when React triggers a re-render of a component [^src1]

## Props

Props are read-only data passed from parent to child [^src1]. The curriculum covers:

- **Sending props**: passing values into a component at instantiation [^src1]
- **Getting props**: reading props inside a component [^src1]
- **Default props**: fallback values when a prop is not supplied (`defaultProps`) [^src1]
- **Non-string props**: props can be any JS value (numbers, booleans, objects, functions) [^src1]
- **Prop validation**: runtime type-checking via `propTypes` to catch incorrect usage early [^src1]

## State

State is mutable data owned by a component; changing it triggers a re-render [^src1]. Key distinctions:

- **State vs. props**: props flow down from parent (read-only); state is internal and mutable [^src1]
- **Stateless function components**: components with no state — pure functions of props; simpler and easier to test [^src1]

## Setup

React requires `react.js` and `react-dom.js`; JSX is compiled at runtime (or build time) via Babel [^src1]. The curriculum also covers ES6/ES* usage with React and prototyping via JSFiddle [^src1]. An advanced setup chapter exists separately [^src1].

## React Enlightenment reference

Written by Cody Lindley, sponsored by Frontend Masters [^src1]. Terse cookbook format (like jQuery Enlightenment, JavaScript Enlightenment, DOM Enlightenment series). Available at reactenlightenment.com; downloadable as PDF, ePub, or MOBI. GitHub repo: 427 stars, HTML-format docs organized as a gitbook. CC BY-NC-ND 3.0 license [^src1].

## See also

- [JavaScript Fundamentals](/software-engineering/javascript-fundamentals.md) — React requires JS fluency (closures, `this`, async, modules)
- [System Design Fundamentals](/software-engineering/system-design-fundamentals.md) — micro-frontends and design systems extend React at scale
- [Bun](/software-engineering/bun.md) — alternative JS runtime and bundler compatible with React projects

---

[^src1]: [React Enlightenment (FrontendMasters / Cody Lindley)](../../raw/github/github-frontendmasters-react-enlightenment.md)

---
type: concept
domain: software-engineering
status: draft
title: Graph Theory
aliases:
  - graphs
  - trees
  - spanning tree
  - minimum spanning tree
  - MST
  - directed graph
  - undirected graph
sources:
  - type: pdf
    path: raw/pdf/pdf-a-cool-brisk-walk-through-discrete-mathematics-part-05.md
    channel: pdf
tags:
  - corpus/software-engineering
  - cs-fundamentals
  - mathematics
  - algorithms
created: 2026-08-04
updated: 2026-08-04
confidence: 0.9
last_confirmed: 2026-08-04
---

# Graph Theory

TL;DR: A graph is a set of nodes (vertices) connected by edges. Graphs model networks, dependencies, state machines, and social connections. Trees are a special case: connected graphs with no cycles. MST algorithms find the cheapest way to connect all nodes.

## Definitions

**Graph** G = (V, E): a set of vertices V and edges E ⊆ V × V.

- **Undirected graph**: edges are unordered pairs {u, v} — connection is symmetric.
- **Directed graph** (digraph): edges are ordered pairs (u, v) — connection has direction.
- **Weighted graph**: edges carry numerical weights (costs, distances).

**Degree** of a vertex: number of edges incident to it.

**Path**: a sequence of vertices where consecutive pairs are connected by edges.

**Cycle**: a path that starts and ends at the same vertex.

**Connected graph**: a path exists between every pair of vertices.

## Trees

A **tree** is a connected, acyclic undirected graph. Properties:
- N vertices → N-1 edges exactly.
- Exactly one path between any two vertices.
- Removing any edge disconnects the tree.

A **spanning tree** of a graph G is a subgraph that is a tree and includes all vertices of G.

## Minimum Spanning Tree (MST)

The MST of a weighted graph is the spanning tree with minimum total edge weight — the cheapest way to connect all nodes.

**Prim's algorithm**: greedily grow a tree by always adding the minimum-weight edge that connects a new vertex to the current tree.[^1]

**Remarkable property**: "The shortest route between two points has nothing whatsoever to do with the shortest *total* distance between *all* points."[^1] — The MST does not necessarily contain the shortest path between any two given nodes.

## CS applications

- Network infrastructure (minimum-cost cable layout)
- Dependency resolution (topological sort on DAGs)
- State machines (DFAs, NFAs for regex/parsing)
- Social network analysis (community detection)
- Routing protocols (spanning tree protocol in Ethernet)

See also: [Discrete Mathematics](/software-engineering/discrete-mathematics.md), [Algorithms (Strategies, Not Tricks)](/software-engineering/algorithms.md), [Data Structures and Big O Notation](/software-engineering/data-structures.md).

[^1]: raw/pdf/pdf-a-cool-brisk-walk-through-discrete-mathematics-part-05.md — Davies, Ch. 5 "Structures."

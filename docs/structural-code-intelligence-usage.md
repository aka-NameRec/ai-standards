---
title: Structural Code Intelligence Usage Guide
permalink: ai-standards/structural-code-intelligence-usage
---

# Structural Code Intelligence Usage Guide

Russian localized version: [structural-code-intelligence-usage.ru.md](structural-code-intelligence-usage.ru.md)

This guide explains how to use the `structural-code-intelligence` feature from `ai-standards` in downstream projects.

`structural-code-intelligence` is an **experimental** capability: retrieval over the relationships between code entities — call paths, dependency paths, module boundaries, impact analysis. It is not part of the recommended stack; enable it only deliberately, after the evaluation methodology below justifies it for the project.

## Goals

Use `structural-code-intelligence` when the project needs:

- call and dependency path queries across a large codebase
- impact analysis for a change spanning modules
- architecture traversal without reading every file
- verification of structural claims (what depends on what) that grep cannot answer precisely

Typical questions: what calls this; what depends on this module; which path connects endpoint X to persistence Y; what can be affected by changing class Z.

## Routing Contract

Prefer structural code intelligence when the question is primarily about relationships between known or discoverable code entities rather than semantic similarity. Semantic discovery ("where is price resolution implemented?") routes to Chroma; relationship questions ("what can be affected by changing this class?") route here. `retrieval-routing` owns the full table.

Structural results narrow the candidate set; they do not prove completeness. Exhaustive or correctness-critical claims require exact search plus build, type, or static checks, and final verification happens at the authoritative layer — canonical docs, source code, and tests.

## Implementation Neutrality

The capability names no tool: a graph tool implements it (Graphify is one possible backend, verified in a large backend codebase at ~9k nodes / ~23k edges), and the standards never encode a specific tool's commands. Refresh the structural index before relationship queries, event-driven like the other retrieval indexes — after VCS operations and structural changes, never as a session ritual.

A structural graph is descriptive: it captures what the code structurally is. A module contract is normative: it states what the code should be. The graph may generate or validate module maps and check declared contract facts, but it never replaces the contract.

## Why Experimental

Adoption into the recommended stack waits for the A/B/C evaluation on real engineering tasks — see [structural-code-intelligence-evaluation.md](structural-code-intelligence-evaluation.md). Until then the feature ships for projects that want to run the evaluation on their own codebase.

Adopt structural graph infrastructure only if its measured improvement on relevant engineering tasks justifies its deployment and maintenance cost.

## Relationship To Other Features

- `retrieval-routing` routes relationship questions here and requires verification at the authoritative layer.
- `chroma` answers semantic discovery; the two complement, not overlap.
- `module-contract-gate` keeps contracts canonical; the graph can only validate declared facts against reality.
- `structured-artifacts` owns module maps, which a structural backend may generate or validate.

## Manifest Example

```toml
features = [
  "retrieval-routing",
  "chroma",
  "structural-code-intelligence",  # experimental — enable deliberately
]
```

## Observations

- [fact] The capability is implementation-neutral: standards name no tool, so a graph backend can be swapped without rewriting behavioral rules.
- [fact] It is deliberately absent from the recommended stack until the A/B/C evaluation justifies adoption.

## Relations

- relates_to [[DECISION: memory and retrieval reorganization]]
- relates_to [[Retrieval Routing Usage Guide]]
- evaluated by [[Structural Code Intelligence Evaluation Methodology]]
- localized counterpart of [[Руководство по использованию structural-code-intelligence]]

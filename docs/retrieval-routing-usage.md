---
title: Retrieval Routing Usage Guide
permalink: ai-standards/retrieval-routing-usage
---

# Retrieval Routing Usage Guide

Russian localized version: [retrieval-routing-usage.ru.md](retrieval-routing-usage.ru.md)

This guide explains how to use the `retrieval-routing` feature from `ai-standards` in downstream projects.

`retrieval-routing` is the tool-neutral policy layer over every retrieval capability: it defines when the agent needs retrieval, which source to consult, in what order, when to escalate to costlier exploration, and how to verify what was found.

The core principle:

> Stored knowledge is not conversation context. Retrieve it when relevant; do not preload it merely because it exists.

## Goals

Use `retrieval-routing` when you want the agent or team to:

- stop preloading broad history merely because it is available
- consult the narrowest knowledge source that can answer the current question
- route questions by information need instead of tool familiarity
- treat retrieval results as leads that still require verification
- escalate progressively instead of scanning the repository indiscriminately

Typical outcomes:

- smaller, better-targeted context windows
- fewer false conclusions drawn from unverified memory hits
- predictable use of the enabled retrieval capabilities
- canonical sources consulted for canonical questions

## What The Feature Covers

The feature standardizes shared policy for:

- retrieve before broad exploration
- using an enabled retrieval capability when it matches the information need
- routing by information need (project memory, canonical documentation, semantic code search, direct source access, structural code intelligence, final verification)
- retrieval as evidence discovery rather than proof
- verification at the authoritative layer
- progressive escalation: narrow retrieval → broad retrieval → targeted file exploration → repository-wide inspection

It intentionally does not standardize:

- API commands of any specific tool (Basic Memory, Chroma, graph tools)
- which backends a project must deploy
- index management, freshness, or embedding configuration (those belong to the implementation features: `basic-memory`, `chroma`, `structural-code-intelligence`)

## Capability And Implementation

Capabilities are named independently of the tools implementing them:

| Capability | Typical implementation |
|---|---|
| project memory | Basic Memory (or plain files under `docs/local/**`) |
| semantic code search | Chroma |
| structural code intelligence | a graph tool (experimental) |

Swapping an implementation backend must not require rewriting the behavioral rules. `retrieval-routing` works correctly with only one retrieval backend enabled, and with none at all: without backends the table routes to canonical documentation, direct source access, and tests.

## Routing Table

| Information need | Preferred source |
|---|---|
| previous task state, prior local decisions, discovered project patterns, unresolved investigations | project memory (local working memory) |
| canonical project decisions, architecture, and domain rules | Git-tracked documentation under `docs/domain/**`, `docs/decisions/**`, `docs/architecture/**` |
| semantic code discovery, analogous implementations, unknown implementation location | semantic code search (Chroma) |
| exact symbol or file already known | direct source access |
| call or dependency paths, impact analysis across modules | structural code intelligence (when enabled) |
| final verification | canonical docs, source code, and tests |

## Capability Awareness

At the start of non-trivial discovery the agent identifies which enabled retrieval capabilities match the task before choosing an exploration strategy. It does not invoke every capability ceremonially: identify the information need, identify the matching enabled capability, use it when it can materially narrow the search.

## Deployment Skill

When `retrieval-routing` is enabled and agents are declared, `ai-sync sync-templates` propagates the `deploy-ai-retrieval-stack` skill/command/rule to them. The skill deploys the retrieval layers enabled in the manifest (Basic Memory, Chroma) in a race-free order.

## Relationship To Other Features

- `basic-memory` implements the project-memory retrieval capability over Markdown knowledge.
- `chroma` implements the semantic-code-search capability over source files.
- `structural-code-intelligence` (experimental) implements the structural capability.
- `session-hygiene` defines when state must be preserved or reloaded; `retrieval-routing` defines how it is retrieved.
- `agent-usage-hygiene` shares the context-economy goal from the usage side.
- `module-contract-gate` keeps canonical contracts in repository artifacts; retrieval may only locate them.

## Manifest Example

```toml
features = [
  "retrieval-routing",
  "basic-memory",
  "chroma",
  "structured-artifacts",
]
```

## Practical Adoption Guidance

- Enable `retrieval-routing` in every project that has any retrieval capability; it is the policy layer that binds them.
- Treat memory hits as hypotheses: confirm against source before acting when correctness matters.
- Do not widen exploration reflexively when a first targeted query misses; escalate one step at a time.

## Observations

- [fact] The policy is tool-neutral: it names capabilities, never tool APIs, so backend swaps do not rewrite behavior.
- [fact] The routing table routes final verification to canonical docs, source, and tests — never to retrieval indexes.

## Relations

- relates_to [[DECISION: memory and retrieval reorganization]]
- localized counterpart of [[Руководство по использованию retrieval-routing]]

# Chroma Usage Guide

Russian localized version: [chroma-usage.ru.md](chroma-usage.ru.md)

This guide explains how to use the `chroma` feature from `ai-standards` in downstream projects.

`chroma` standardizes semantic code search over repository source files as a layer that is deliberately separate from ConPort operational memory and Basic Memory documentation retrieval.

## Goals

Use `chroma` when you want the agent or team to:

- search source code semantically across a large or multi-repository workspace
- keep code retrieval isolated from documentation retrieval and from operational context
- avoid stale results by refreshing the index before querying
- resume interrupted index builds without re-embedding unchanged files

Typical outcomes:

- faster navigation of unfamiliar code
- narrower investigation targets before exact search or build verification
- less confusion between "what the docs say" and "what the code does"

## What The Feature Covers

The feature standardizes shared policy for:

- using Chroma as a semantic code-search layer over source files
- keeping the code index separate from ConPort and Basic Memory stores
- freshness-gated querying (refresh before query, block on refresh failure)
- incremental indexing by content hash with an atomic resumable manifest
- local `PersistentClient` as the default deployment mode

It intentionally does not standardize:

- one mandatory collection layout for every project
- a specific embedding model or chunking size (project-local config)
- automatic promotion of code search results into canonical documentation
- a Docker-first deployment (Docker remains an opt-in for shared or CI use)

## The AI Knowledge Stack

`chroma` is one layer of a four-layer stack with three separate vector stores:

| Layer | Tool | Purpose | Store |
|---|---|---|---|
| 0 | `docs/` (Git) | durable source of truth | Markdown |
| 1 | Basic Memory | retrieval over documentation | BM sqlite + embeddings |
| 2 | ConPort | transient operational context | ConPort sqlite (+ internal vectors) |
| 3 | Chroma | semantic code search | Chroma PersistentClient sqlite |

ConPort internal vectors, the Chroma code index, and Basic Memory embeddings are never mixed. Keeping them separate keeps each retrieval layer precise instead of noisy.

## Freshness-Gated Querying

Chroma queries must go through a wrapper that refreshes the index before querying and blocks when a refresh fails. This prevents retrieval against a stale index after code changes.

A reference wrapper is provided as a managed template at `.ai-standards/scripts/code_index.py`, synced by `ai-sync sync-templates` when `chroma` is enabled.

## Similarity Is Not Completeness

Similarity search narrows an investigation but does not prove completeness. Exhaustive or correctness-critical claims require exact search (`grep`/`rg`), plus build, type, or static checks. Treat semantic hits as candidates to confirm, not as authoritative answers.

## Indexing Model

- Incremental by content hash: unchanged files are skipped.
- Atomic resumable manifest: an interrupted build resumes from the manifest without re-embedding finished files.
- Cross-file batched upsert: embeddings are sent across file boundaries in batches, not one upsert per source file, to avoid the per-upsert startup cost bottleneck.

## Deployment Mode

Prefer a local `PersistentClient` (embedded storage, no server process, no port) for developer workspaces. Use a Docker deployment only for shared or CI scenarios.

ai-standards-managed infrastructure lives under `.ai-standards/`:

```
.ai-standards/
├── scripts/code_index.py   # managed template (generalized reference wrapper)
├── code-index.toml         # managed starter config (collections, roots, chunking)
├── chroma/                 # runtime sqlite (gitignored)
└── state/                  # manifest.json (gitignored)
```

## Deployment Skill

When `chroma` is enabled, `ai-sync sync-templates` also propagates a deployment skill (`deploy-ai-knowledge-stack`) to the agents listed in the manifest. The skill deploys the whole stack (ConPort, Basic Memory, Chroma) in an order that eliminates common setup races. See the decision record for details.

## Relationship To Other Features

- `conport` remains transient operational memory and handoff storage.
- `basic-memory` remains a retrieval layer over Git-tracked Markdown documentation.
- `structured-artifacts` defines which Markdown artifacts count as canonical.
- `design-first-collaboration` keeps intent and boundaries explicit before deployment.

`chroma` complements these features by making source code searchable semantically. It does not replace exact search, build verification, or canonical documentation.

## Manifest Example

```toml
features = [
  "conport",
  "basic-memory",
  "chroma",
  "structured-artifacts",
]
```

## Practical Prompting Guidance

Good prompts:

- `Refresh the code index, then find modules that handle order cancellation.`
- `Use semantic search to narrow the search, then confirm with exact grep and a build.`
- `Treat these similarity hits as candidates, not as a complete list.`

Avoid:

- `Trust the semantic search result as exhaustive.`
- `Query Chroma without refreshing after a large change.`
- `Mix the code index with ConPort or Basic Memory stores.`

Prefer:

- `Refresh, query, then verify candidates with exact search and build checks.`

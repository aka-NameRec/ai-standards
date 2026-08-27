---
title: 'DECISION: knowledge-store-role-separation'
permalink: ai-standards/decisions/2026-08-24-knowledge-store-role-separation
---

# DECISION: knowledge-store-role-separation

Russian localized version: [2026-08-24-knowledge-store-role-separation.ru.md](2026-08-24-knowledge-store-role-separation.ru.md)

## Status

Accepted

Companion to [2026-08-24-archive-history-in-docs-tree.md](2026-08-24-archive-history-in-docs-tree.md), which applies this split to historical chat exports.

## Date

2026-08-24

## Context

Basic Memory and Chroma look functionally close: one indexes documentation, the other indexes code, and the devcats workspace already splits one Chroma database into per-area collections (`devcats-broadleaf-code`, `devcats-mkt-backend-code`, …). The question arose whether Basic Memory is a redundant entity that could be folded into Chroma, with documentation and history living as further Chroma collections.

Verification against the running installation changed the picture:

- Basic Memory in this workspace runs with `embedder = None` — it performs no vector work at all, so the two tools do not even compete for one retrieval modality.
- Basic Memory's unique value is the graph: entities, observations, relations, wiki-links, `build-context` traversal, permalink addressing — plus a ready MCP toolset for writing and editing notes.
- Basic Memory's search filters (`--tag`, `--type`, `--meta`, `--status`) are inclusive only; there is no query-time way to demote or exclude a class of material.
- Chroma's `where` filters support exclusion (`$ne`) and its named collections already model "searchable only when asked for".

## Decision

The three stores keep distinct roles; Basic Memory is not merged into Chroma.

- **Chroma** — vector retrieval over code and over historical corpora (chat exports), as named collections; history is queried only through a targeted collection request.
- **Basic Memory** — the graph over the living knowledge tree (`docs/**` minus the archive), with note identification by frontmatter `title` and permalink addressing.
- **ConPort** — operational memory: active context, progress, session handoffs; transient, never canonical.
- **git** — canonical truth for everything; every index is a projection that can be rebuilt.

The chroma fragment's rule "the three stores are never mixed" is interpreted at collection/index granularity: Chroma may host multiple named collections with different roles, while no store shares one index or collection with another.

## Why

- the graph cannot be emulated with filters: "which decisions implement this domain rule" is a traversal, not a nearest-neighbour query
- folding note editing into Chroma would mean writing a Markdown indexer and an MCP toolset that Basic Memory already ships
- with `embedder = None` the consolidation would delete no duplicated work, only capabilities

## Alternatives Considered

### Replace Basic Memory with Chroma entirely

Rejected. Loses graph traversal, `memory://` addressing, and the note-editing MCP tools; requires a custom Markdown chunker for nothing gained.

### One Basic Memory store for everything, including transcripts

Rejected. Transcripts have no entity or relation structure, so the graph adds nothing for them, and the inclusive-only filters cannot keep them out of routine results.

### Store history in Chroma only, outside git

Rejected. Chat exports are project history, and git is where the project keeps history.

## Consequences

### Benefits

- one uniform role formula: code and historical corpora in Chroma, the living graph in Basic Memory, operational state in ConPort, canonical files in git
- the archive design ([2026-08-24-archive-history-in-docs-tree.md](2026-08-24-archive-history-in-docs-tree.md)) falls out of it directly

### Costs Or Tradeoffs

- two indexers to keep healthy instead of one
- semantic search over history requires a per-project collection declaration in `code-index.toml`; without it the archive is greppable but not semantically searchable

## Verification

- `embedder = None`, inclusive-only filters, and the rejection of nested projects ("Projects cannot share directory trees") were verified against the installed Basic Memory.
- Multi-collection configuration was verified against the devcats workspace and the `code-index.toml` template shipped with the chroma feature.

## Observations

- [decision] Basic Memory is not merged into Chroma; the stores keep distinct roles at collection/index granularity.
- [decision] Chroma hosts code and historical corpora as named collections; Basic Memory keeps the living knowledge graph; ConPort stays operational; git stays canonical.
- [fact] Basic Memory in this workspace runs with `embedder = None`, so no vector work is duplicated between the stores.

## Relations

- relates_to [[DECISION: archive-history-in-docs-tree]]
- relates_to [[DECISION: basic-memory-knowledge-tree-boundary]]
- relates_to [[Knowledge Stack Roles]]
- localized counterpart of [[РЕШЕНИЕ: разделение ролей хранилищ знаний]]
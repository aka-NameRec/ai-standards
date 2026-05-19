# Basic Memory Usage Guide

Russian localized version: [basic-memory-usage.ru.md](basic-memory-usage.ru.md)

This guide explains how to use the `basic-memory` feature from `ai-standards` in downstream projects.

`basic-memory` standardizes how a project should use Basic Memory as a Markdown-first retrieval layer without letting it become an uncontrolled source of architectural truth.

## Goals

Use `basic-memory` when you want the agent or team to:

- keep durable project knowledge in Git-tracked Markdown
- search that knowledge efficiently across sessions through Basic Memory
- distinguish canonical documentation from agent-managed working memory
- avoid accidental documentation drift from indexing side effects
- reindex intentionally after repository events that can stale the graph

Typical outcomes:

- less hidden knowledge trapped in chat history
- better reuse of existing project notes and decisions
- fewer duplicate documentation files
- clearer boundaries between reviewed truth and agent scratch space

## What The Feature Covers

The feature standardizes shared policy for:

- using Basic Memory as a retrieval layer, not as the canonical source of truth
- separating canonical documentation from working memory
- checking for duplication or contradiction before canonical documentation updates
- protecting repository Markdown from unwanted frontmatter injection
- deciding when filesystem auto-sync is enough and when explicit reindexing is required

It intentionally does not standardize:

- one mandatory folder layout for every project
- a specific Basic Memory cloud or local deployment mode
- one universal schema for every note type
- automatic promotion of working notes into canonical documentation

## Canonical Documentation Versus Working Memory

Treat the following as canonical documentation:

- `docs/decisions/**`
- `docs/architecture/**`
- `MODULE_CONTRACT.md`
- equivalent local artifacts that define accepted constraints, contracts, or decisions

Treat the following as working memory:

- `docs/ai-memory/**`
- investigation notes
- handoff notes
- implementation gotchas
- temporary findings that are still evolving

Canonical documentation should change only on explicit user request. Working memory may be updated autonomously when it helps preserve useful context.

## Frontmatter Safety

Basic Memory can inject frontmatter during sync. That behavior is useful for greenfield knowledge bases, but it is risky for existing Git-tracked documentation because it can modify many files at once without an explicit documentation request.

For repositories that treat Markdown as reviewable project knowledge, prefer:

- `ensure_frontmatter_on_sync=false`

Use frontmatter injection only when the project explicitly wants Basic Memory to own that metadata lifecycle.

## Reindexing Policy

Normal file edits inside indexed directories should rely on Basic Memory's regular filesystem sync.

Run a status check after:

- `git pull`
- `git merge`
- `git rebase`
- branch switch or checkout
- applying a large patch that changes many indexed Markdown files

Run an explicit project reindex after:

- mass file renames, moves, or deletes inside indexed directories
- interrupted indexing or incomplete embeddings
- changing the indexed root path for a project
- changing permalink behavior or frontmatter-sync policy
- first-time indexing of an existing large documentation tree

Prefer these operational patterns:

- `bm status --project <project>`
- `bm reindex --project <project>`
- `bm reindex --project <project> --embeddings`
- `bm reindex --project <project> --full`

Use the narrowest reindex that resolves the reported problem.

## Relationship To Other Features

- `structured-artifacts` defines which Markdown artifacts count as plans, decision records, and module contracts.
- `session-hygiene` defines when the agent should reload relevant durable context between phases or chats.
- `conport` remains useful for transient operational context and handoff storage.
- `design-first-collaboration` keeps intent, boundaries, and non-goals explicit before implementation.

`basic-memory` complements these features by making Git-tracked Markdown easier to retrieve and reuse. It does not replace reviewable documentation or explicit human decisions.

## Manifest Example

```toml
features = [
  "conport",
  "basic-memory",
  "structured-artifacts",
  "session-hygiene",
]
```

## Practical Prompting Guidance

Good prompts:

- `Search our Basic Memory notes before creating a new design note.`
- `Check whether this decision already exists in docs/decisions or ai-memory before writing anything new.`
- `After this merge, check Basic Memory status and reindex only if the docs graph is stale.`
- `Record this implementation gotcha in working memory, not in canonical documentation.`

Avoid:

- `Promote everything from working notes into docs/decisions.`
- `Let Basic Memory rewrite repository docs however it wants.`
- `Reindex from scratch in every session whether needed or not.`

Prefer:

- `Use Basic Memory to search first, then update the smallest correct Markdown artifact.`

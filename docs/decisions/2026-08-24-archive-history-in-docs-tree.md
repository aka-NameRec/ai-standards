# DECISION: archive-history-in-docs-tree

Russian localized version: [2026-08-24-archive-history-in-docs-tree.ru.md](2026-08-24-archive-history-in-docs-tree.ru.md)

## Status

Accepted

Directs the rework of pull request #7 (the knowledge-tree branch), which is not merged as opened.

## Date

2026-08-24

## Context

Chat exports (`*-log-*.md`) are primary sources: they record how decisions were actually reached, and losing them loses the reasoning behind the recorded outcome. Pull request #7 moved twelve of them out of the knowledge tree into `temp/`, which misstates their value twice: the name says "temporary" about files that are history, and in the neighbouring `cockpit` repository `temp/` is gitignored scratch space, so one name would mean opposite things across a single workspace.

Retrieval pulls in two directions. Routine work must not surface half a megabyte of transcripts in every search, while an explicit "study the history" request must find them. Basic Memory cannot express the first half: its search filters (`--tag`, `--type`, `--meta`, `--status`) are inclusive only, so archive material can be neither demoted nor excluded at query time. Registering the archive as a second Basic Memory project inside the tree is also impossible: the indexer rejects overlapping directory trees.

Humans separate documentation from code, so the archive belongs inside the documentation tree rather than beside it at the repository root.

## Decision

1. Historical chat exports live in `docs/archive/**`, inside the knowledge tree, under version control.
2. Basic Memory excludes that subtree through a `.bmignore` pattern `archive/`. The directory-name form is load-bearing: `archive/*` does not exclude anything, because during a recursive scan the matcher sees the subdirectory itself and root-relative patterns stop matching. Writes into ignored paths are rejected by the sync API, so an agent cannot create notes inside the archive through the model-facing tools.
3. Chroma indexes `docs/archive` as a dedicated collection (for example `<project>-history`), following the multi-collection precedent of the devcats workspace. Code collections must declare explicit roots that do not cover `docs/archive`, because a root of `"."` would mix history into the code index.
4. No second Basic Memory project is created, and cockpit's project registry and adapter stay unchanged; the earlier candidate design of a sibling `<name>-archive` project is dropped.
5. `ai-sync doctor` skips `docs/archive` when auditing notes and verifies that the active `.bmignore` actually carries the `archive/` exclusion. The boundary is one conventional line in a config file rather than a structural property of the tool, so it needs deterministic verification: a lost line would otherwise silently pour transcripts back into the graph.
6. The `-log-` naming rule becomes `docs/**/*-log-*.md` — the current `docs/*-log-*.md` glob does not cross directory boundaries — and names `docs/archive/**` as the home of chat exports.

## Why

- transcripts are a search corpus, not a graph participant: they have no meaningful entity or relation structure, so Basic Memory adds nothing for them, while its inclusive filters cannot keep them out of routine results
- Chroma's named collections already model "searchable only when asked for"; history becomes one more collection instead of a new tool entity
- one documentation home matches how a person reads a repository: code here, everything written for humans under `docs/`
- the archive stays in git, so nothing depends on any index surviving

## Alternatives Considered

### Keep chat exports in `temp/` (pull request #7 as opened)

Rejected. The name misstates the value of the files and collides with the opposite meaning of `temp/` in cockpit.

### A root-level `archive/` registered as a separate Basic Memory project

Rejected. The indexer forbids overlapping trees, the archive would move outside the human documentation view, and cockpit would need a new registry field, adapter logic, and one more project entity per repository.

### Pessimize archive material inside the shared Basic Memory index

Rejected as impossible: Basic Memory has no exclusive query filters, so archive notes cannot be demoted — only excluded structurally.

### Store history only in Chroma, outside git

Rejected. Chat exports are project history; git is where the project keeps history.

## Consequences

### Benefits

- routine retrieval stays clean while explicit history research works through a targeted collection query
- the role separation is uniform: code and historical corpora live in Chroma, the living knowledge graph in Basic Memory, the full history in git
- no new entities: one `.bmignore` line per machine, one collection declaration per project

### Costs Or Tradeoffs

- `.bmignore` is resolved per machine, and `archive/` excludes every directory of that name in every Basic Memory project. Under a uniform "docs/archive = history" convention that is intended; `doctor` must surface the divergence when a project genuinely wants its own `archive/` indexed.
- wiki-links from decision records into the archive do not resolve in the Basic Memory graph; use relative Markdown links, which work in git and in readers, at the cost of graph traversability.
- semantic search over history requires the Chroma collection to be declared and indexed per project; without it the archive remains greppable but not semantically searchable.

## Verification

- On an isolated Basic Memory configuration (`BASIC_MEMORY_CONFIG_DIR`), the pattern `archive/` keeps an archived note out of the database while a sibling live note is indexed; the pattern `archive/*` fails to exclude it.
- Writes into ignored paths are rejected with "matches Basic Memory ignore rules".
- A nested Basic Memory project is rejected with "Projects cannot share directory trees", which rules out an in-tree archive project.
- Collection-per-root configuration is verified against the devcats workspace (`devcats-broadleaf-code`, `devcats-mkt-backend-code`, …) and the `code-index.toml` template shipped with the chroma feature.

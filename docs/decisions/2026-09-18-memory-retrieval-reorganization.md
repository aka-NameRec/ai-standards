---
title: 'DECISION: memory and retrieval reorganization'
permalink: ai-standards/decisions/2026-09-18-memory-retrieval-reorganization
---

# DECISION: memory and retrieval reorganization

Russian localized version: [2026-09-18-memory-retrieval-reorganization.ru.md](2026-09-18-memory-retrieval-reorganization.ru.md)

## Status

Accepted. Implemented on branch `rules-change/16-memory-retrieval-reorganization`, released in 2.4.0.

Supersedes the ConPort layer of [2026-08-24-knowledge-store-role-separation.md](2026-08-24-knowledge-store-role-separation.md); its Basic Memory, Chroma, and git roles stand. Source issue: #16. Follow-up epic (phases 6–7): #19.

## Date

2026-09-18

## Context

Three distinct concerns were mixed in one operational-memory tool: project memory (local accumulated knowledge kept across sessions), knowledge retrieval (fetching only the knowledge relevant to the current task), and code retrieval/intelligence (search and analysis of a large codebase). ConPort, the tool carrying the first concern, stagnated, while its semantics (context/decisions/progress/patterns/relationships/cross-session continuation) remained valuable and tool-independent.

Removing ConPort naively would delete those semantics. Keeping it would keep the standards bound to one abandoned backend and keep preload-shaped habits: loading stored knowledge into context merely because it exists.

## Decision

1. **Remove ConPort entirely** — feature, registry entries, default manifest, deployment steps, fragments, templates, and living documentation. Dated history keeps its mentions with supersession links. Useful semantic properties move into tool-independent rules instead of a mechanical rename to Basic Memory.
2. **Introduce `retrieval-routing`** — a tool-neutral policy layer: retrieve before broad exploration; an enabled retrieval capability must be considered; route by information need, not tool familiarity; retrieval is evidence discovery; verify at the authoritative layer; escalate progressively. The connecting layer over every retrieval capability.
3. **Introduce `project-memory`** — tool-independent local working memory under `docs/local/**` (gitignored by default) with a fixed taxonomy: `context`, `decisions`, `progress`, `patterns`, `investigations`, `handoffs`; a memory-write policy (curated state store, not an execution log), a memory-read policy (targeted queries, never whole-tree reads), and an explicit promotion lifecycle into canonical documentation. Works best with `basic-memory`, but does not require it: capability is separated from implementation.
4. **Keep `basic-memory` and `chroma` scopes** — Basic Memory remains the Markdown retrieval layer over canonical knowledge and local working memory; Chroma remains the semantic code-search layer; their stores stay separate.
5. **Deployment goes capability-based** — `deploy-ai-knowledge-stack` becomes `deploy-ai-retrieval-stack`, deploying only the layers enabled in the manifest; its template gate moves from `chroma` to `retrieval-routing`. `sync-templates` gains a marker-guarded retire mechanism so renamed templates do not linger in projects. Upgrades from older releases offer a ConPort → `docs/local` migration before the manifest changes.
6. **`structural-code-intelligence` stays experimental** — a capability fragment without deployment infrastructure; adoption into the recommended stack waits for the A/B/C evaluation on real tasks.

## Why

- The memory semantics were proven by use; the backend was not the value.
- "Stored knowledge is not conversation context" must be a policy rule, not a side effect of one tool's shape.
- Local working memory does not need any specific tool: `docs/local/**` is files first, indexed when Basic Memory is present.
- Renamed managed templates otherwise leave stale copies forever; retirement is a sync concern, not a documentation note.

## Alternatives Considered

### Keep ConPort as an optional feature

Rejected. The standards kept describing a backend nobody maintained; the semantics deserved a tool-independent home; every integration carried adapter wording.

### Rename ConPort wording to Basic Memory mechanically

Rejected. That would erase the distinction between the retrieval layer (Basic Memory) and the memory taxonomy/semantics (project memory), recreating the coupling with a different tool name.

### Put the taxonomy inside `basic-memory`

Rejected. Projects without Basic Memory would lose the local-memory rules; the capability would depend on one implementation, contradicting the capability/implementation split the reorganization establishes.

### Ship the removal as its own release before the replacement exists

Rejected. An intermediate release without `conport` and without `retrieval-routing` breaks downstream manifests (`SyncError` on the unknown feature) with nothing to migrate to.

## Consequences

### Benefits

- The standards describe memory semantics, not a specific abandoned backend.
- Local cross-session memory gets a standard, gitignored home with a fixed taxonomy and an explicit promotion path; canonical documentation is protected from session-state dumps.
- Retrieval becomes a routing decision with evidence and verification duties instead of a tool habit.
- Renamed/withdrawn managed templates clean up after themselves.

### Costs Or Tradeoffs

- Every downstream manifest naming `conport` breaks on the first render after upgrade until migrated; the `update-ai-standards` skill carries the migration procedure.
- `doctor` must distinguish the local-memory area from canonical zones (relaxed audit) — added complexity in the audit.
- Two new features and one experimental capability enlarge the registry and the feature graph.

## Verification

- `uv run python scripts/ai_sync.py render/check --project-root .`, `uv run ruff check`, `uv run mypy`, `uv run python -m pytest` — green through every phase.
- `rg -i conport` over the repository matches only dated history (`docs/decisions/**`, `docs/tasks/**`, `docs/archive/**`, `CHANGELOG.md`) plus intentional migration-instruction references in `update-ai-standards` and `deploy-ai-retrieval-stack` templates.
- Policy tests assert the generated `AGENTS.md` carries no ConPort section; retire-mechanism tests cover managed removal and unmanaged survival.
- Behavioral scenarios A–E from issue #16 on this repository as the reference configuration at iteration close.

## Observations

- [decision] ConPort is removed; its semantics live on in tool-independent `project-memory` rules.
- [decision] `retrieval-routing` is the connecting policy layer; capabilities (project-memory, semantic code, structural code) are named independently of their implementations (Basic Memory, Chroma, graph tools).
- [decision] Local working memory under `docs/local/**` is never canonical; promotion to canonical documentation is an explicit operation.
- [fact] `sync-templates` previously never removed destination files, so renamed templates would linger; retirement is marker-guarded and never touches user-rewritten files.

## Relations

- supersedes (the ConPort layer of) [[DECISION: knowledge-store-role-separation]]
- relates_to [[Knowledge Stack Roles]]
- relates_to [[Module Contract: scripts/ai_sync.py]]
- localized counterpart of [[РЕШЕНИЕ: реорганизация memory и retrieval]]

---
title: 'DECISION: non-note-data-file-doctor-policy'
permalink: ai-standards/decisions/2026-09-03-non-note-data-file-doctor-policy
---

# DECISION: non-note-data-file-doctor-policy

Russian localized version: [2026-09-03-non-note-data-file-doctor-policy.ru.md](2026-09-03-non-note-data-file-doctor-policy.ru.md)

## Status

Accepted

## Date

2026-09-03

## Context

User issue #13 reported a devcats case: 37 phantom entities (PNG screenshots, CSV dumps, raw logs, a PDF) sitting in `docs/artifacts/**` of an indexed knowledge tree, and a 152K chat-export note alone costing 276 chunks and ~88s of CPU embedding time per reindex. The issue proposed masks-only guidance; the follow-up session (tasks `0tkrogf`–`0tkrpc0`) examined the alternatives before this policy was fixed.

Facts verified against the Basic Memory 0.23.2 sources settled the design space:

- index updates start from three points ai-standards does not control: the MCP server's file watcher (autostarted in the server lifespan), the CLI (`bm reindex`, `bm sync`), and the API routers — so no ai-standards-side hook can block indexing at initiation;
- Basic Memory already honours masks — the watcher and the reindex walk apply the global `~/.basic-memory/.bmignore` and the project-level `.gitignore` at the indexer's project home — so the fail-closed mechanism exists and only needs correct masks;
- the mask syntax has no `!` negation, so a "only Markdown" whitelist is inexpressible, and a deny-list of binary formats can never be complete — but it does not have to be.

## Decision

1. `ai-sync doctor` reports `non-note-data-file-inside-knowledge-tree` — a WARNING, never auto-fixed — for any non-Markdown, non-hidden, unmasked file under the knowledge tree. Declared overrides and the `archive/` subtree are excluded to avoid double reporting.
2. The check's matcher mirrors the indexer's own mask semantics (the `.gitignore` at the knowledge-tree root plus the global `.bmignore` beside the indexer configuration, loaded while the feature gate opens). An already-masked tree stays quiet: any junk is either masked (not indexed) or reported — the detection set is closed without enumerating formats.
3. Severity stays WARNING. The "do not index this" intent is served by an agent-side blocking rule — the `basic-memory` fragment, the usage guide's Reindexing Policy, and the `audit-knowledge-tree` skill all say: reindex only after `ai-sync doctor` stops reporting the file.
4. Upstream support for `!` negation in Basic Memory masks is out of scope. The shipped approach does not depend on it; the local matcher port must be re-synced if upstream semantics ever change.

## Why

- A format-agnostic detector ("anything that is not a note") replaces the impossible enumeration of binary formats; masks only have to cover the formats a project actually stores.
- The indexer is the only component that can refuse to index, and it already refuses masked paths — doctor's job is to guarantee the masks are right, not to reimplement the refusal.
- A warning plus an explicit agent rule achieves blocking for the actual audience (agent-driven flows) without turning doctor red for every legacy tree.

## Alternatives Considered

### ERROR severity (exit-code gate)

Rejected: `doctor` exits non-zero on errors and is CI-suitable by contract, so every legacy tree carrying junk would fail CI immediately after a standards update — including projects that never enabled the `basic-memory` feature. The blocking rule delivers the same intent where it matters without that breakage.

### Block indexing at initiation (wrap `bm` or intercept the watcher)

Rejected as infeasible: the watcher autostarts inside the MCP server lifespan, and the CLI and API paths are invoked directly. A `bm` wrapper would not cover the watcher or MCP tools.

### Land an upstream `!`-negation PR first, then build on whitelists

Deferred: realistic (the matcher change is small; the default `.bmignore` already promises "standard gitignore-style syntax") but medium overall complexity — the hard part is walker pruning semantics for re-inclusion under excluded directories, and acceptance by the maintainers is uncertain. The shipped approach works without it.

### Point data files at `docs/archive`

Corrected rather than adopted: the indexer walks `docs/archive` until a `.bmignore` line (`archive/`) excludes it, and by convention the archive holds verbatim sources, not data files. Data belongs outside the tree, or masked in place while notes cite it.

## Consequences

### Benefits

- closed detection: any non-note file in the tree is masked or reported;
- the ai-sync module contract is unchanged — report-only, read-only indexer configuration, `--fix` not extended;
- legacy trees keep passing CI.

### Trade-offs

- enforcement is advisory: a human who ignores the report can still reindex;
- the local matcher duplicates upstream semantics by design and needs re-syncing if Basic Memory changes them.

## Observations

- [decision] Doctor reports knowledge-tree data files as `non-note-data-file-inside-knowledge-tree` warnings whose matcher mirrors the indexer's own mask semantics, so an already-masked tree stays quiet.
- [decision] Severity is WARNING with an agent-side reindex gate; an ERROR exit-code gate was rejected because legacy trees that never enabled the indexer feature would fail CI.
- [fact] Basic Memory starts index updates from three uncontrolled points — the MCP server's file watcher, the CLI, and the API routers — so no ai-standards-side hook can block indexing at initiation.
- [fact] The mask deny-list does not need to enumerate formats: the non-Markdown detector is format-agnostic, and masks only cover the formats a project actually stores.

## Relations

- relates_to [[DECISION: basic-memory-knowledge-tree-boundary]]
- relates_to [[ai-sync doctor: Deterministic Knowledge-Tree Audit]]
- relates_to [[Module Contract: scripts/ai_sync.py]]

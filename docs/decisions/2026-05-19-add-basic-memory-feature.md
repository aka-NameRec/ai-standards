# DECISION: add-basic-memory-feature

Russian localized version: [2026-05-19-add-basic-memory-feature.ru.md](2026-05-19-add-basic-memory-feature.ru.md)

## Status

Accepted

This decision partially supersedes [2026-04-14-replace-grace-with-structured-artifacts.md](2026-04-14-replace-grace-with-structured-artifacts.md) and [2026-04-25-add-session-hygiene-feature.md](2026-04-25-add-session-hygiene-feature.md) for the role of ConPort in the shared memory model.

## Date

2026-05-19

## Context

The repository already used `conport`, `structured-artifacts`, and `session-hygiene` to preserve project context across sessions. That combination still left one important gap: a shared standard for Git-tracked Markdown knowledge retrieval and indexing.

The team wanted a memory model where:

- canonical project knowledge lives in Git-tracked Markdown
- `docs/decisions/**` and module contracts are protected from autonomous edits
- agent-managed working memory can evolve with less friction
- Basic Memory can index and search Markdown knowledge across sessions
- ConPort remains useful, but only as transient operational memory and handoff storage

The repository also observed a practical risk during Basic Memory setup: default frontmatter injection can modify many tracked Markdown files at once, which conflicts with projects that treat documentation changes as explicit reviewable changes.

## Decision

`ai-standards` adds `basic-memory` as an opt-in tool feature.

The feature defines:

- Basic Memory as a retrieval and indexing layer over Git-tracked Markdown
- explicit separation between canonical documentation and agent-managed working memory
- a recommendation to prefer `ensure_frontmatter_on_sync=false` for existing Git-tracked documentation trees
- reindexing triggers tied to repository events and indexing health, not to every session mechanically
- complementarity between Basic Memory, ConPort, structured artifacts, and session hygiene

The self-hosted manifest enables the feature so the repository's own generated `AGENTS.md` reflects the new policy.

## Why

- makes Markdown-first project knowledge an explicit shared workflow rather than a local convention
- aligns retrieval with Git review and repository-owned documentation
- reduces the risk of uncontrolled documentation churn from Basic Memory sync side effects
- keeps semantic search and knowledge reuse without treating the index as the source of truth
- gives downstream projects a reusable policy for when to trust auto-sync and when to run reindex

## Alternatives Considered

### Keep Basic Memory guidance in README text only

Rejected because retrieval policy, canonical-versus-working-memory rules, and reindexing triggers need to be reusable in generated `AGENTS.md`, not only discoverable in repository prose.

### Fold Basic Memory rules into `conport`

Rejected because ConPort and Basic Memory solve different problems. ConPort is now transient operational memory; Basic Memory is a Markdown retrieval layer over repository knowledge.

### Allow default frontmatter injection for all indexed repositories

Rejected because existing Git-tracked documentation may not permit mass metadata edits without explicit review and approval.

## Consequences

### Benefits

- downstream projects can opt into a clear Markdown-first memory workflow
- canonical documentation receives stronger protection from autonomous edits
- working-memory notes can still evolve quickly under agent control
- reindexing becomes tied to concrete repository events and health checks

### Costs Or Tradeoffs

- the repository carries another optional feature and usage guide pair
- teams must install and operate Basic Memory intentionally when they enable the feature
- projects that rely on Basic Memory-managed frontmatter may need local overrides

## Affected Modules

- `registry.toml`
- `fragments/tools/conport.md`
- `fragments/process/structured-artifacts.md`
- `fragments/process/session-hygiene.md`
- `fragments/tools/basic-memory.md`
- `README.md`
- `README.ru.md`
- `docs/basic-memory-usage.md`
- `docs/basic-memory-usage.ru.md`
- `docs/structured-artifacts-usage.md`
- `docs/structured-artifacts-usage.ru.md`
- `docs/session-hygiene-usage.md`
- `docs/session-hygiene-usage.ru.md`
- `ai.project.toml`
- `templates/project_manifest.toml`
- `AGENTS.md`
- `tests/test_ai_sync.py`

## Invariants And Constraints

- Git-tracked Markdown remains the source of durable project knowledge
- Basic Memory is a retrieval and indexing layer, not the canonical source of truth
- canonical documentation must not be modified autonomously without explicit user request
- projects should prefer no-frontmatter-injection defaults unless they explicitly want Basic Memory-managed metadata
- reindexing policy should be event-driven and health-driven, not mechanically session-driven

## Verification

- `registry.toml` exposes the `basic-memory` feature
- rendered output includes the Basic Memory fragment when the feature is enabled
- usage guides exist in English and Russian
- README documents the feature in both languages
- self-hosted `AGENTS.md` renders successfully with the feature enabled

## Related Artifacts

- [../basic-memory-usage.md](../basic-memory-usage.md)
- [../basic-memory-usage.ru.md](../basic-memory-usage.ru.md)
- [../../fragments/tools/basic-memory.md](../../fragments/tools/basic-memory.md)
- [../../ai.project.toml](../../ai.project.toml)
- [2026-04-25-add-session-hygiene-feature.md](2026-04-25-add-session-hygiene-feature.md)

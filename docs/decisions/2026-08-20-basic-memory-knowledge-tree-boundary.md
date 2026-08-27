---
title: 'DECISION: basic-memory-knowledge-tree-boundary'
permalink: ai-standards/decisions/2026-08-20-basic-memory-knowledge-tree-boundary
---

# DECISION: basic-memory-knowledge-tree-boundary

Russian localized version: [2026-08-20-basic-memory-knowledge-tree-boundary.ru.md](2026-08-20-basic-memory-knowledge-tree-boundary.ru.md)

## Status

Accepted

This decision supersedes the frontmatter recommendation in [2026-05-19-add-basic-memory-feature.md](2026-05-19-add-basic-memory-feature.md). The rest of that decision stands.

## Date

2026-08-20

## Context

The `basic-memory` feature shipped with a defensive recommendation: prefer `ensure_frontmatter_on_sync=false` when indexing existing Git-tracked Markdown. The recommendation assumed that Basic Memory would be pointed at a repository that already holds mixed Markdown, and it defended against the consequences with a flag.

Field use of that assumption produced four failures in one workspace:

- Projects registered at repository roots indexed vendored dependencies, build metadata, and office documents as if they were notes. One project held 143 non-Markdown entries out of 216.
- `ensure_frontmatter_on_sync=false` alone proved insufficient. Files that already carried frontmatter were still rewritten during sync, which is why a second flag, `disable_permalinks=true`, had to be added.
- With permalinks disabled, every `memory://` URL resolved against a null permalink column and returned nothing. Graph traversal silently degraded to fuzzy title search, which reads as "the tool is just a search box".
- `ai-sync init-project` scaffolded the `local_overrides` file into `docs/ai/project-rules.md`, inside the tree a project would naturally hand to Basic Memory. An indexer stamped frontmatter onto that file. Because `_read_override` concatenates the file verbatim, the next render would have emitted a YAML block into the middle of the generated `AGENTS.md`.

The last failure is the decisive one: the standard's own scaffolding placed a rendering input inside the knowledge tree, so every downstream project inherited the trap.

## Decision

A Basic Memory project points at a dedicated knowledge tree, never at a repository root.

Every file inside that tree is a note. Rendering inputs, generated output, templates, and machine-owned Markdown live outside it. `ai-sync init-project` scaffolds `local_overrides` to `ai/project-rules.md` instead of `docs/ai/project-rules.md`.

On a tree that holds only notes, permalink generation stays enabled, because `memory://` addressing and graph traversal resolve through permalinks. The pair `ensure_frontmatter_on_sync=false` plus `disable_permalinks=true` is demoted to a fallback for a legacy tree that cannot be narrowed yet, with the loss of `memory://` recorded as its cost.

`_read_fragment`, `_read_override`, and `_read_optional_override` strip a leading frontmatter block, so a violation of the placement rule cannot reach generated output.

`ai-sync doctor` audits a project against these rules: override placement, note frontmatter and heading agreement, observations and relations, and — when the `basic-memory` feature is enabled — the indexer's own configuration. It reports mechanical findings with a non-zero exit code on errors, so the deterministic half of an audit belongs to code and can run in CI.

`ai-sync doctor --fix` applies the repairs that follow from a rule rather than a decision: it moves rendering inputs out of the tree and repoints the manifest, restores missing frontmatter titles and headings, and prunes directories it empties. It converges in one pass and warns when no git repository can undo it. Renaming is excluded on purpose — the convention asks for a meaningful slug, and transliterating a title produces exactly the unreadable name the convention exists to avoid.

Judgement-bearing repair belongs to a skill, not to the renderer. The `audit-knowledge-tree` template ships for all four agent adapters, gated by the `basic-memory` feature. It consumes the `doctor` report, classifies each file, and repairs on confirmation one file at a time. It is barred from synthesizing observations, rewriting verbatim sources, and deleting notes.

The manifest reader is unchanged: `local_overrides` remains a free-form list of paths declared per project, so existing projects keep rendering from their current locations.

## Why

- the flag defended against a symptom while the root cause was the indexed root
- a dedicated tree removes vendored and generated files from retrieval instead of tolerating them
- keeping permalinks restores `memory://` and graph traversal, which the defensive default silently disabled
- placing rendering inputs outside the tree makes the `AGENTS.md` leak structurally impossible rather than merely unlikely
- stripping frontmatter at render time keeps the guarantee when a project violates the placement rule anyway

## Alternatives Considered

### Keep the flag recommendation and only strip frontmatter at render time

Rejected. Stripping protects the generated file, but the source files are still mutated on disk and committed. In this repository that would mean frontmatter appearing in `fragments/**` and `templates/**`, which are copied into downstream projects.

### Move the placement rule only, without the render-time strip

Rejected. The placement rule is advisory; nothing enforces it. This repository proved that the rule gets violated by its own tooling, so the render needs a guarantee that does not depend on compliance.

### Break the manifest contract by hardcoding the new override path

Rejected. `local_overrides` is declared per project and read verbatim, so existing projects are unaffected by the scaffold change. Hardcoding would have created a breaking change for no benefit.

## Consequences

### Benefits

- retrieval quality improves because the graph holds notes rather than repository contents
- `memory://` addressing and `build_context` work by default instead of failing silently
- generated `AGENTS.md` cannot receive frontmatter from an indexed override
- new projects are scaffolded into the correct shape without a migration step

### Costs Or Tradeoffs

- existing projects must narrow their Basic Memory root and move `local_overrides` out of the knowledge tree; neither is automated by this change
- enabling permalinks on an existing tree produces a one-time migration commit that adds `permalink:` to every note
- projects that deliberately index a repository root keep the fallback flags and lose `memory://`

## Affected Modules

- `fragments/tools/basic-memory.md`
- `scripts/ai_sync.py`
- `templates/project_manifest.toml`
- `templates/knowledge-tree/audit-knowledge-tree.SKILL.md`
- `templates/knowledge-tree/audit-knowledge-tree.claude.md`
- `templates/knowledge-tree/audit-knowledge-tree.cursor.mdc`
- `templates/ai-infrastructure/deploy-ai-knowledge-stack.SKILL.md`
- `templates/ai-infrastructure/deploy-ai-knowledge-stack.claude.md`
- `templates/ai-infrastructure/deploy-ai-knowledge-stack.cursor.mdc`
- `docs/basic-memory-usage.md`
- `docs/basic-memory-usage.ru.md`
- `README.md`
- `README.ru.md`
- `ai.project.toml`
- `ai/project-rules.md`
- `ai/project-rules.ru.md`
- `AGENTS.md`
- `tests/test_ai_sync.py`

## Invariants And Constraints

- a Basic Memory project root contains notes and nothing else
- rendering inputs are never placed inside an indexed knowledge tree
- generated output never carries frontmatter inherited from a rendering input
- `local_overrides` stays a per-project declared path list, so the scaffold location is a default and not a contract
- disabling permalinks is a recorded trade-off, not a silent default

## Verification

- `pytest tests/` passes, including a test that renders a stamped override and asserts no frontmatter reaches the output
- `_strip_frontmatter` leaves content intact when a leading `---` is never closed
- `init-project` scaffolds `ai/project-rules.md` and not `docs/ai/project-rules.md`
- stamping frontmatter onto this repository's own `ai/project-rules.md` and re-rendering leaves `AGENTS.md` byte-identical
- the self-hosted `AGENTS.md` renders with the rewritten fragment
- `ai-sync doctor` run against this repository reports its own indexed root as an error
- the file-name check judges only the directories the convention claims, and tolerates localized siblings such as `<name>.ru.md`
- `--fix` aligns a first-level heading without touching a deeper one that starts with the same text
- a rejected manifest repoint moves nothing, so the project still renders
- `sync-templates` materializes `audit-knowledge-tree` only when `basic-memory` is enabled

## Related Artifacts

- [../basic-memory-usage.md](../basic-memory-usage.md)
- [../basic-memory-usage.ru.md](../basic-memory-usage.ru.md)
- [../../fragments/tools/basic-memory.md](../../fragments/tools/basic-memory.md)
- [../../scripts/ai_sync.py](../../scripts/ai_sync.py)
- [2026-05-19-add-basic-memory-feature.md](2026-05-19-add-basic-memory-feature.md)
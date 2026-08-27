---
title: 'Module Contract: scripts/ai_sync.py'
permalink: ai-standards/module-contract
---

# Module Contract: scripts/ai_sync.py

Module: `scripts/ai_sync.py`, exposed as the `ai-sync` CLI (render, update, init-project, sync-templates, init-claude-bridge, doctor).

## Ownership

The single rendering and template-deployment tool of this repository, plus the deterministic half of the knowledge-tree audit. It runs for this repository and for downstream projects that adopt ai-standards.

## Non-goals

- No judgement-bearing repair: no file renames, no note-content edits, no observation synthesis — those belong to the `audit-knowledge-tree` skill.
- No writing to the Basic Memory indexer configuration; `doctor` reads it, nothing more.
- No index management for Basic Memory or Chroma; no embedding work.
- No content generation beyond assembling existing fragments, overrides, and templates.

## Inputs

- `ai.project.toml` (manifest), `registry.toml` (feature/stack catalog), `fragments/**`, `templates/**`
- per-project `local_overrides` / `optional_local_overrides` (verbatim, leading frontmatter stripped)
- optional: Basic Memory indexer config (read-only, feature-gated)

## Outputs

- rendered `AGENTS.md` (and the Claude bridge import)
- deployed managed templates: agent adapters under `.codex/`, `.cursor/`, `.claude/`, `.agents/`; infrastructure under `.ai-standards/`
- `doctor` reports (errors exit non-zero, suitable for CI) and `--fix` filesystem repairs

## Invariants

- Render is idempotent: re-rendering a clean tree changes nothing; rendered output never contains override frontmatter.
- Managed markers match the destination syntax: HTML comments for `.md`/`.mdc`/`.html`, `#` comments otherwise; a shebang stays the first line.
- `--fix` only applies repairs that follow from a rule: moves rendering inputs out of the tree and repoints the manifest, restores titles/headings, strips indexer-stamped frontmatter, prunes empty directories. It warns when git cannot undo it.
- Detection of managed files is format-agnostic (marker text prefix, any comment syntax).
- Existing projects keep rendering from their declared override paths; scaffolding changes affect only new projects.

## Failure boundaries

- `SyncError` with actionable context; unknown features/agents are rejected at load; unreadable notes surface as `doctor` findings instead of crashes; a manifest that cannot be repointed aborts the move (no partial filesystem changes).

## Verification

- `uv run pytest` (unit and structural tests), `uv run mypy scripts/`
- `uv run ai-sync render --project-root .` leaves a clean worktree (idempotency)
- `uv run ai-sync doctor --project-root .` reports zero errors

## Observations

- [fact] The module renders `AGENTS.md`, deploys managed templates, and audits knowledge-tree wiring; rendering inputs are stripped of their own frontmatter before concatenation.
- [fact] `--fix` applies only repairs that follow from a rule — moving rendering inputs, restoring titles and headings, pruning empty directories — and refuses renames and note-content edits.
- [decision] Managed markers match the destination syntax (`<!-- -->` for Markdown-like destinations, `#` otherwise), and a shebang stays the first line.

## Relations

- relates_to [[Knowledge Stack Roles]]
- localized counterpart of [[Модульный контракт: scripts/ai_sync.py]]
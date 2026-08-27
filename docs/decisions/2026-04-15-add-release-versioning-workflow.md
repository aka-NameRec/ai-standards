---
title: 'DECISION: add-release-versioning-workflow'
permalink: ai-standards/decisions/2026-04-15-add-release-versioning-workflow
---

# DECISION: add-release-versioning-workflow

Russian localized version: [2026-04-15-add-release-versioning-workflow.ru.md](2026-04-15-add-release-versioning-workflow.ru.md)

## Status

Accepted

Superseded in part on 2026-04-18 by [2026-04-18-separate-release-version-from-python-package-version.md](2026-04-18-separate-release-version-from-python-package-version.md) for the location of the canonical repository release version.

## Date

2026-04-15

## Context

`ai-standards` already had a package version in `pyproject.toml`, but it had no repository-standard way to track release dates, project-local self-hosted version metadata, or safe release tagging.

The repository also needed a repeatable release workflow that keeps package metadata, self-hosted manifest metadata, and generated `AGENTS.md` headers aligned without bundling commits and tags into the same automatic step.

## Decision

`ai-standards` standardizes a repository-local release workflow built around:

- `pyproject.toml` as the source of truth for `project.version`
- `tool.ai-standards.release_date` in `pyproject.toml`
- self-hosted manifest metadata in `ai.project.toml`
- `scripts/bump_version.py` for preview, save, and tag operations

The workflow keeps version saving, git commits, and release tagging as separate steps.

## Why

- keeps packaging metadata compliant with `pyproject.toml` conventions
- makes self-hosted version metadata explicit instead of overloading manifest fields
- allows generated `AGENTS.md` files to reflect both repository release metadata and project-local version metadata
- keeps release tagging safe by requiring a clean worktree and the `main` branch

## Alternatives Considered

### Store `release_date` directly in `[project]`

Rejected because custom release metadata belongs in a tool-specific section rather than in standardized package metadata.

### Reuse `ai.project.toml.version` for local project versioning

Rejected because the repository already used `version` as the standards dependency marker. Explicit fields are clearer and safer.

### Tag as part of the version-save command

Rejected because tagging before a reviewed commit creates unnecessary release risk and couples distinct workflow steps too tightly.

## Consequences

### Benefits

- release metadata now has explicit, inspectable sources of truth
- the repository gains a repeatable safe workflow for release preparation
- `AGENTS.md` headers can show release state consistently

### Costs Or Tradeoffs

- the manifest schema becomes slightly more explicit and slightly more verbose
- release preparation now touches several coordinated files instead of only `pyproject.toml`

## Affected Modules

- `pyproject.toml`
- `ai.project.toml`
- `templates/project_manifest.toml`
- `scripts/ai_sync.py`
- `scripts/bump_version.py`
- `README.md`
- `README.ru.md`
- `docs/ai/project-rules.md`
- `docs/ai/project-rules.ru.md`

## Invariants And Constraints

- `scripts/bump_version.py save` requires a clean git worktree
- `scripts/bump_version.py tag` requires a clean git worktree and the `main` branch
- release tagging remains separate from version saving and from git commits
- project-specific release rules stay local to `ai-standards` and are not promoted into shared fragments

## Verification

- renderer tests cover the new manifest metadata fields
- release workflow tests cover preview/save/tag behavior
- repository checks continue to pass

## Related Artifacts

- [../../scripts/bump_version.py](../../scripts/bump_version.py)
- [../../scripts/ai_sync.py](../../scripts/ai_sync.py)
- [../ai/project-rules.md](../../ai/project-rules.md)
- [../../pyproject.toml](../../pyproject.toml)
- [../../ai.project.toml](../../ai.project.toml)
---
title: 'DECISION: separate-release-version-from-python-package-version'
permalink: ai-standards/decisions/2026-04-18-separate-release-version-from-python-package-version
---

# DECISION: separate-release-version-from-python-package-version

Russian localized version: [2026-04-18-separate-release-version-from-python-package-version.ru.md](2026-04-18-separate-release-version-from-python-package-version.ru.md)

## Status

Accepted

## Date

2026-04-18

## Context

The repository had been using `pyproject.toml` `project.version` as the canonical release version of `ai-standards` while also using uv to manage the Python environment for the repository's support scripts.

This mixed two different concerns:

- the release version of the `ai-standards` standards repository
- the package version of the Python support tooling used to render and validate those standards

In practice, uv records the root package version in `uv.lock`. As a result, ordinary ai-standards release bumps caused lockfile churn even when the Python support package itself had not changed.

## Decision

`ai-standards` now treats the canonical repository release version as tool-specific metadata in `pyproject.toml` under:

- `tool.ai-standards.version`
- `tool.ai-standards.release_date`

`project.version` remains the version of the Python support tooling package and should change only when that package itself changes materially, such as through script or dependency updates.

The self-hosted manifest continues to use:

- `ai_standards_version`
- `project_version`
- `project_release_date`

and those values reflect the release state of the `ai-standards` repository, not the Python support package version.

## Why

- separates repository release semantics from Python package metadata
- prevents unnecessary `uv.lock` churn on ordinary standards-only releases
- keeps release metadata in a tool-specific section that matches its actual scope
- preserves `pyproject.toml` as the correct place for Python tooling configuration
- keeps the rendered `AGENTS.md` headers aligned with repository releases instead of package internals

## Alternatives Considered

### Keep using `project.version` and always refresh `uv.lock`

Rejected because it preserves the semantic mismatch between standards releases and package releases, while making lockfile drift a routine part of release preparation.

### Move repository release metadata into a separate `project.toml`

Rejected because `pyproject.toml` already provides the appropriate `tool.*` namespace for repository-local tooling metadata, and introducing another top-level metadata file would add custom complexity without helping uv.

## Consequences

### Benefits

- standards releases can advance without forcing Python package version changes
- `bump_version.py save` no longer needs to modify `project.version`
- release tagging continues to work from clean repository metadata without incidental lockfile churn

### Costs Or Tradeoffs

- the repository now carries two version concepts that must stay semantically distinct
- documentation and tests must be explicit about which version they are asserting
- older repositories that only expose `project.version` remain a compatibility case that the tooling should still read safely

## Affected Modules

- `pyproject.toml`
- `ai.project.toml`
- `templates/project_manifest.toml`
- `scripts/ai_sync.py`
- `scripts/bump_version.py`
- `tests/test_bump_version.py`
- `README.md`
- `README.ru.md`
- `docs/ai/project-rules.md`
- `docs/ai/project-rules.ru.md`

## Invariants And Constraints

- `tool.ai-standards.version` is the canonical release version for this repository
- `project.version` is reserved for the Python support tooling package
- release tagging remains separate from version saving and from git commits
- repository-local release rules remain local to `ai-standards` and are not promoted into shared fragments

## Verification

- renderer logic reads release version from `tool.ai-standards.version` with compatibility fallback
- `bump_version.py save` updates `tool.ai-standards.version` and `tool.ai-standards.release_date` without touching `project.version`
- tests verify that ordinary release saves leave the Python package version unchanged

## Related Artifacts

- [../../scripts/bump_version.py](../../scripts/bump_version.py)
- [../../scripts/ai_sync.py](../../scripts/ai_sync.py)
- [../ai/project-rules.md](../../ai/project-rules.md)
- [../../pyproject.toml](../../pyproject.toml)
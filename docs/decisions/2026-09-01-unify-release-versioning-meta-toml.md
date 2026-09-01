---
title: 'DECISION: unify-release-versioning-meta-toml'
permalink: ai-standards/decisions/2026-09-01-unify-release-versioning-meta-toml
---

# DECISION: unify-release-versioning-meta-toml

Russian localized version: [2026-09-01-unify-release-versioning-meta-toml.ru.md](2026-09-01-unify-release-versioning-meta-toml.ru.md)

## Status

Accepted

Supersedes [2026-04-18-separate-release-version-from-python-package-version.md](2026-04-18-separate-release-version-from-python-package-version.md).

## Date

2026-09-01

## Context

Release version data was spread across three places, two of which invited confusion:

- `ai.project.toml` carried `ai_standards_version` (bare version), plus `project_version` and `project_release_date`.
- `pyproject.toml` carried `[project] version` (the Python tooling package) and `[tool.ai-standards] version` / `release_date` (the standards release).

For self-hosting ai-standards, `project_version` in its own manifest received the standards version, blurring the two concepts the 2026-04-18 decision had separated. The manifest pin also named only the version, while release tags are named `<version>-<date>` (`bump-version tag`).

## Decision

- `meta.toml` at the repository root is the single source of release truth: `[release]` with `version` and `date`, both mandatory.
- `[tool.ai-standards]` is removed from `pyproject.toml`; `[project] version` is fixed at `0.0.0` as a placeholder — the Python support package is no longer versioned separately.
- The consumer-manifest pin is the single key `ai_standards_version` in the full `<version>-<date>` format, identical to the release tag name; `project_version` and `project_release_date` are retired.
- Scripts read `[release]` from `meta.toml`; drift checks compare the manifest pin against the full pin through one helper.

## Why

- one file, one meaning: no key duplicates between manifest and `pyproject.toml`
- the pin now equals the tag name, so a deployment pin can be verified against `git tag` directly
- zeroing the package version ends the "which of the two versions changed?" question for standards-only releases and stops `uv.lock` churn, because the placeholder never moves

## Alternatives Considered

### Keep `[tool.ai-standards]` in `pyproject.toml` (the 2026-04-18 decision)

Rejected: the tool-specific namespace still mixes standards release metadata into Python packaging metadata and keeps `project_version` / `project_release_date` in manifests as duplicate data.

### Bare version pin without date

Rejected: a pin of `2.2.1` cannot distinguish re-released date corrections and does not match the tag name.

## Consequences

### Benefits

- single-file release metadata with mandatory `version` and `date`
- pin == tag name: trivially verifiable
- downstream manifests shrink to one version key

### Costs Or Tradeoffs

- deployments pinning the old bare format report drift until the `update-ai-standards` skill runs — the standard upgrade path
- a new top-level `meta.toml` file exists; the 2026-04-18 objection about extra files is outweighed by removing `[tool.ai-standards]` and the manifest duplicates

## Affected Modules

- `meta.toml` (new)
- `pyproject.toml`
- `ai.project.toml`
- `templates/project_manifest.toml`
- `scripts/ai_sync.py`
- `scripts/bump_version.py`
- `tests/test_ai_sync.py`
- `tests/test_bump_version.py`
- `templates/standards-update/*`
- `docs/architecture/2026-09-01-module-contract-ai-sync.md`

## Invariants And Constraints

- `meta.toml [release]` (`version`, `date`) is the canonical release metadata; both fields are mandatory.
- `ai_standards_version` in manifests is `<version>-<date>`; the legacy bare `version` manifest key remains readable for old deployments.
- Release tagging remains separate from version saving and from git commits.
- `[feature_meta].since` values stay bare versions; comparisons against a deployment use the version part of the pin.

## Verification

- `uv run pytest`, `uv run mypy scripts/`
- `uv run ai-sync check --project-root .` passes with the full pin in the self-hosted manifest
- `uv run bump-version save` updates `meta.toml` and stamps full pins into manifests

## Related Artifacts

- [../../meta.toml](../../meta.toml)
- [../../scripts/ai_sync.py](../../scripts/ai_sync.py)
- [../../scripts/bump_version.py](../../scripts/bump_version.py)
- [2026-04-18-separate-release-version-from-python-package-version.md](2026-04-18-separate-release-version-from-python-package-version.md)

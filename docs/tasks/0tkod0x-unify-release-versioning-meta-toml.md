---
title: 0tkod0x — Unified Release Versioning Around meta.toml
permalink: ai-standards/tasks/0tkod0x-unify-release-versioning-meta-toml
---

# 0tkod0x — Unified Release Versioning Around meta.toml

Russian version: [0tkod0x-unify-release-versioning-meta-toml.ru.md](0tkod0x-unify-release-versioning-meta-toml.ru.md)

Date: 2026-09-01 · Branch: `feature/0tkod0x-unify-release-versioning` · User issue: [#11](https://github.com/aka-NameRec/ai-standards/issues/11)

## Trigger

User issue #11: release version data was spread across three places — `ai.project.toml` (`ai_standards_version`, `project_version`, `project_release_date`) and `pyproject.toml` (`[project] version` for the tooling package, `[tool.ai-standards] version` / `release_date` for the standards release). For self-hosting ai-standards, `project_version` in its own manifest received the standards version, and the manifest pin named only the version while release tags are named `<version>-<date>`. The proposal was verified against the code before implementation; the implementation plan was approved by the user with two explicit decisions: zero `[project] version` to `0.0.0` with a pointer comment, and confirm the `<version>-<date>` pin format.

## What Was Done

- **`meta.toml`** (new, repository root): `[release]` with mandatory `version = "2.2.1"` and `date = "2026-08-30"` — the single source of release truth.
- **`pyproject.toml`**: `[tool.ai-standards]` removed; `[project] version = "0.0.0"` with a comment pointing at `meta.toml`; `uv.lock` refreshed (ai-standards 1.3.0 → 0.0.0).
- **`scripts/ai_sync.py`**: `_load_release_metadata` reads `meta.toml [release]` (`version`, `date`, both mandatory via `_expect_string`); new `_release_pin()` helper; all four drift-check call sites (`render`, `update`, `check`, `doctor`) compare the manifest pin against the full pin; `project_version` / `project_release_date` dropped from `Manifest` and from header rendering; `init-project` seeds the full pin; the legacy bare `version` manifest fallback key stays readable for old deployments.
- **`scripts/bump_version.py`**: `_load_release_state` reads `meta.toml`; `_update_pyproject` replaced by `_update_meta`; `save_release` stamps the full `<version>-<date>` pin into manifests and no longer writes `project_*` keys; the `tag` docstring now names `meta.toml`.
- **Manifests**: the self-hosted `ai.project.toml` and `templates/project_manifest.toml` carry only `ai_standards_version = "2.2.1-2026-08-30"`.
- **`update-ai-standards` skill templates** (SKILL/claude/cursor): the release version is read from `meta.toml [release]`; `[feature_meta].since` is compared against the version part of the pin; step 7 writes the full pin.
- **Docs**: README (en+ru) examples and the Versioning section rewritten around the full pin; `ai/project-rules.md` (+ `.ru.md`) Release Workflow rules moved to `meta.toml`; `docs/standards-update-usage.md` (+ `.ru.md`) names the pin format; the ai-sync module contract Inputs gained `meta.toml`; CHANGELOG gained an `Unreleased` entry.
- **Decision record** `docs/decisions/2026-09-01-unify-release-versioning-meta-toml.md` (+ `.ru.md`); the 2026-04-18 separation decision marked Superseded (en+ru).
- **Tests**: both suites moved to `meta.toml` fixtures and the pin format; drift tests assert the full in-use pin.

## Verification

106 tests passed (`uv run pytest`); `uv run mypy scripts/` clean; `uv run ruff check scripts tests` clean (5 lint errors in `templates/ai-infrastructure/scripts/code_index.py` pre-date this change — confirmed via `git stash` — and sit outside the repository lint scope of `scripts`/`tests`); `ai-sync render` + `check` idempotent; `ai-sync doctor` reports 0 errors and no `standards-version-drift`.

## Deliberately Not Done

- No version bump: `meta.toml` still carries 2.2.1 / 2026-08-30; release preparation and tagging are a separate step per the project release workflow.
- No downstream migration: deployments pinning the old bare format see the standard drift report until the `update-ai-standards` skill runs — the intended upgrade path.
- The pre-existing lint errors in the deployed `code_index.py` template are left to their own task.

## Context For The Next Session

- On the next release, `bump-version save` bumps `meta.toml [release]` and stamps the new full pin into both manifests; the pin equals the tag name produced by `bump-version tag`.
- `uv.lock` no longer churns on standards-only releases because the package version placeholder never moves.

## Observations

- [fact] The manifest pin `ai_standards_version` now equals the release tag name, so a deployment pin can be verified directly against `git tag`.
- [decision] Release metadata lives only in `meta.toml [release]`; the `[project] version` in `pyproject.toml` is a permanent `0.0.0` placeholder and is not the release version.
- [fact] Drift is detected by comparing the manifest pin against `<version>-<date>` in four commands: `render`, `update`, `check`, and `doctor`.
- [fact] Old manifests that use the bare `version` key still render; bare-format `ai_standards_version` pins report drift against the new source until updated.

## Relations

- relates_to [[DECISION: unify-release-versioning-meta-toml]]
- relates_to [[Module Contract: scripts/ai_sync.py]]
- localized counterpart of [[0tkod0x — Единое версионирование релиза вокруг meta.toml]]

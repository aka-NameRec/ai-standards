---
title: 'DECISION: bump-version-console-script'
permalink: ai-standards/decisions/2026-04-21-bump-version-console-script
---

# DECISION: bump-version-console-script

Russian localized version: [2026-04-21-bump-version-console-script.ru.md](2026-04-21-bump-version-console-script.ru.md)

## Status

Accepted

## Date

2026-04-21

## Context

The release workflow for `ai-standards` already used `scripts/bump_version.py`, but that required remembering a `python -m` invocation. The repository is managed with `uv`, so the release tool should be available as a standard console script to make the workflow simpler and more consistent.

## Decision

Expose the release workflow as the `bump-version` console script and keep `scripts/bump_version.py` as the implementation module.

## Why

- lets contributors run the release workflow with `uv run bump-version ...`
- keeps the implementation in a regular Python module while giving it a normal CLI name
- reduces friction in the release workflow without changing the semantics of version save and tag operations

## Alternatives Considered

### Keep only `python -m scripts.bump_version`

Rejected because it is more awkward to remember and does not match the rest of the `uv`-first workflow in the repository.

### Rename the script file itself to `bump-version.py`

Rejected because the implementation already lives comfortably as a module and the hyphenated name is better suited to the CLI entry point than to a Python module path.

## Consequences

### Benefits

- release commands become shorter and easier to communicate
- `uv run bump-version` now works directly from the repository workflow
- tests can cover the same invocation path that users will use

### Costs Or Tradeoffs

- the repository now maintains both the module path and the console script name
- documentation and project rules must refer to the CLI name rather than the module path

## Affected Modules

- `pyproject.toml`
- `scripts/bump_version.py`
- `tests/test_bump_version.py`
- `README.md`
- `README.ru.md`
- `docs/ai/project-rules.md`
- `docs/ai/project-rules.ru.md`

## Invariants And Constraints

- release tagging still requires a clean worktree and `main`
- `bump-version save` must continue to keep `project.version` unchanged
- the CLI name should stay stable because it becomes part of the public repository workflow

## Verification

- `uv run bump-version --help` resolves the console script
- `uv run bump-version save ...` updates repository release metadata in a demo repository
- `tests/test_bump_version.py` covers the console-script path

## Related Artifacts

- [../../scripts/bump_version.py](../../scripts/bump_version.py)
- [../../tests/test_bump_version.py](../../tests/test_bump_version.py)
- [../2026-04-18-separate-release-version-from-python-package-version.md](2026-04-18-separate-release-version-from-python-package-version.md)
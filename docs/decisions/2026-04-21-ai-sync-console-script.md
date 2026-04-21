# DECISION: ai-sync-console-script

Russian localized version: [2026-04-21-ai-sync-console-script.ru.md](2026-04-21-ai-sync-console-script.ru.md)

## Status

Accepted

## Date

2026-04-21

## Context

The repository already exposed `scripts/ai_sync.py` as the implementation for generating and validating `AGENTS.md`, but the common workflow still required `python -m` or a script path. Since the project is used through `uv`, the sync tool should also be available as a direct console script.

## Decision

Expose `ai-sync` as a console script and keep `scripts/ai_sync.py` as the implementation module.

## Why

- makes the render/check workflow symmetrical with `bump-version`
- shortens the standard commands used by contributors
- preserves the existing behavior while making the CLI easier to remember

## Alternatives Considered

### Keep only `python scripts/ai_sync.py`

Rejected because it is longer, less consistent with `uv`-based workflows, and harder to standardize in docs.

### Rename the module itself to the CLI name

Rejected because the implementation already fits cleanly in `scripts/ai_sync.py`, and the console script is the right place for the public command name.

## Consequences

### Benefits

- `uv run ai-sync render ...` becomes the standard command
- documentation can refer to a single concise command name
- tests can exercise the same entry point users will use

### Costs Or Tradeoffs

- the repository now maintains another console script entry point
- packaging configuration must include the script and package discovery rules

## Affected Modules

- `pyproject.toml`
- `scripts/ai_sync.py`
- `README.md`
- `README.ru.md`
- `docs/ai/project-rules.md`
- `docs/ai/project-rules.ru.md`
- `tests/test_ai_sync.py`
- `tests/test_bump_version.py`

## Invariants And Constraints

- `ai-sync` must keep the same render, check, init-project, and sync-templates behavior
- generated `AGENTS.md` still remains the source of truth for downstream projects
- the console script should not change the underlying manifest or rendering semantics

## Verification

- `uv run ai-sync --help` resolves the console script
- `uv run ai-sync render --project-root .` remains available from the repository workflow
- tests cover the console-script path in the repository and in the demo fixture

## Related Artifacts

- [../../scripts/ai_sync.py](../../scripts/ai_sync.py)
- [../../tests/test_ai_sync.py](../../tests/test_ai_sync.py)
- [../../README.md](../../README.md)

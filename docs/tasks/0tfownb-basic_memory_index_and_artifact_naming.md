# Task 0tfownb: basic memory index and artifact naming

Russian localized version: [0tfownb-basic_memory_index_and_artifact_naming.ru.md](0tfownb-basic_memory_index_and_artifact_naming.ru.md)

## Status

Implemented on feature branch `task/0tfownb-basic_memory_index_and_artifact_naming`.

## Scope

- Verified the `ai-standards` Basic Memory setup and confirmed the project was registered but not yet fully indexed.
- Rebuilt the Basic Memory index for the repository documentation and verified retrieval over the existing Markdown artifacts.
- Reviewed shared rules for `docs/decisions/**` and `docs/architecture/**`.
- Confirmed that canonical-documentation rules already covered both directories, but no shared filename convention had been stated explicitly.
- Added a shared default naming rule for canonical notes under `docs/decisions/**` and `docs/architecture/**`: `YYYY-MM-DD-<topic-slug>.md`, unless a project defines a stricter local convention.
- Updated the structured-artifacts fragment, usage guides, README files, and decision-record template to reflect that rule.

## Verification

- `bm reindex --project ai-standards --full`
- `uv run ai-sync render --project-root .`
- `uv run ai-sync check --project-root .`
- `uv run python -m pytest -q`

## Related Artifacts

- [../structured-artifacts-usage.md](../structured-artifacts-usage.md)
- [../structured-artifacts-usage.ru.md](../structured-artifacts-usage.ru.md)
- [../basic-memory-usage.md](../basic-memory-usage.md)
- [../basic-memory-usage.ru.md](../basic-memory-usage.ru.md)
- [../../fragments/process/structured-artifacts.md](../../fragments/process/structured-artifacts.md)
- [../../templates/decision-record.md](../../templates/decision-record.md)

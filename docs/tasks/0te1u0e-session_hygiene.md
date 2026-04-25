# Task 0te1u0e: session hygiene

Russian localized version: [0te1u0e-session_hygiene.ru.md](0te1u0e-session_hygiene.ru.md)

## Status

Implemented on feature branch `feature/0te1jdd-agent-usage-hygiene`.

## Scope

- Added the `session-hygiene` optional process feature.
- Defined long-session warnings for context drift, stale assumptions, goal substitution, and lost constraints.
- Defined compact handoff summaries and fresh-chat recommendations.
- Kept the feature tool-neutral and avoided message-count or token-count thresholds.
- Updated the self-hosted manifest and starter manifest to include the new feature.
- Added English and Russian usage guides and decision records.
- Added renderer coverage for the new feature.

## Verification

- `uv run python scripts/ai_sync.py render --project-root .`
- `uv run python scripts/ai_sync.py check --project-root .`
- `uv run ruff check`
- `uv run mypy`
- `uv run python -m pytest`

## Related Artifacts

- [../session-hygiene-usage.md](../session-hygiene-usage.md)
- [../session-hygiene-usage.ru.md](../session-hygiene-usage.ru.md)
- [../decisions/2026-04-25-add-session-hygiene-feature.md](../decisions/2026-04-25-add-session-hygiene-feature.md)
- [../../fragments/process/session-hygiene.md](../../fragments/process/session-hygiene.md)

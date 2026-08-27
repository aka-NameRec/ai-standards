---
title: 'Task 0te1jdd: agent usage hygiene'
permalink: ai-standards/tasks/0te1jdd-agent-usage-hygiene
---

# Task 0te1jdd: agent usage hygiene

Russian localized version: [0te1jdd-agent_usage_hygiene.ru.md](0te1jdd-agent_usage_hygiene.ru.md)

## Status

Implemented on feature branch `feature/0te1jdd-agent-usage-hygiene`.

## Scope

- Added the `agent-usage-hygiene` optional process feature.
- Defined prompt-activated economy mode for usage-sensitive work.
- Kept the feature tool-neutral and excluded Codex-specific controls from shared standards.
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

- [../agent-usage-hygiene-usage.md](../agent-usage-hygiene-usage.md)
- [../agent-usage-hygiene-usage.ru.md](../agent-usage-hygiene-usage.ru.md)
- [../decisions/2026-04-25-add-agent-usage-hygiene-feature.md](../decisions/2026-04-25-add-agent-usage-hygiene-feature.md)
- [../../fragments/process/agent-usage-hygiene.md](../../fragments/process/agent-usage-hygiene.md)
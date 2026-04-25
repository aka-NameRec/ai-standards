# Задача 0te1u0e: session hygiene

Англоязычный оригинал: [0te1u0e-session_hygiene.md](0te1u0e-session_hygiene.md)

## Статус

Выполнено на feature-ветке `feature/0te1jdd-agent-usage-hygiene`.

## Объём

- Добавлена опциональная process feature `session-hygiene`.
- Определены long-session warnings для context drift, stale assumptions, goal substitution и lost constraints.
- Определены compact handoff summaries и fresh-chat recommendations.
- Feature оставлена tool-neutral; message-count и token-count thresholds не стандартизованы.
- Обновлены self-hosted manifest и starter manifest для подключения новой feature.
- Добавлены англоязычные и русскоязычные usage guides и decision records.
- Добавлено renderer coverage для новой feature.

## Проверка

- `uv run python scripts/ai_sync.py render --project-root .`
- `uv run python scripts/ai_sync.py check --project-root .`
- `uv run ruff check`
- `uv run mypy`
- `uv run python -m pytest`

## Связанные артефакты

- [../session-hygiene-usage.md](../session-hygiene-usage.md)
- [../session-hygiene-usage.ru.md](../session-hygiene-usage.ru.md)
- [../decisions/2026-04-25-add-session-hygiene-feature.ru.md](../decisions/2026-04-25-add-session-hygiene-feature.ru.md)
- [../../fragments/process/session-hygiene.md](../../fragments/process/session-hygiene.md)

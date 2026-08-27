---
title: 'Задача 0te1jdd: agent usage hygiene'
permalink: ai-standards/tasks/0te1jdd-agent-usage-hygiene.ru
---

# Задача 0te1jdd: agent usage hygiene

Англоязычный оригинал: [0te1jdd-agent_usage_hygiene.md](0te1jdd-agent_usage_hygiene.md)

## Статус

Выполнено на feature-ветке `feature/0te1jdd-agent-usage-hygiene`.

## Объём

- Добавлена опциональная process feature `agent-usage-hygiene`.
- Определён prompt-activated economy mode для usage-sensitive работы.
- Feature оставлена tool-neutral; Codex-specific controls не включены в shared standards.
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

- [../agent-usage-hygiene-usage.md](../agent-usage-hygiene-usage.md)
- [../agent-usage-hygiene-usage.ru.md](../agent-usage-hygiene-usage.ru.md)
- [../decisions/2026-04-25-add-agent-usage-hygiene-feature.ru.md](../decisions/2026-04-25-add-agent-usage-hygiene-feature.ru.md)
- [../../fragments/process/agent-usage-hygiene.md](../../fragments/process/agent-usage-hygiene.md)
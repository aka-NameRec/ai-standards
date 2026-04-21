# DECISION: ai-sync-console-script

Англоязычный оригинал: [2026-04-21-ai-sync-console-script.md](2026-04-21-ai-sync-console-script.md)

## Статус

Accepted

## Дата

2026-04-21

## Контекст

В репозитории уже существовал `scripts/ai_sync.py` как implementation для генерации и проверки `AGENTS.md`, но стандартный workflow всё ещё требовал `python -m` или прямой путь к скрипту. Поскольку проект используется через `uv`, sync tool тоже должен быть доступен как direct console script.

## Решение

Expose `ai-sync` как console script и оставить `scripts/ai_sync.py` как implementation module.

## Почему

- делает workflow render/check симметричным с `bump-version`
- сокращает стандартные команды, которые используют contributors
- сохраняет текущее поведение, но делает CLI проще для запоминания

## Рассмотренные альтернативы

### Оставить только `python scripts/ai_sync.py`

Отклонено, потому что это длиннее, хуже сочетается с `uv`-based workflows и труднее стандартизируется в документации.

### Переименовать модуль в CLI имя

Отклонено, потому что implementation уже хорошо живёт в `scripts/ai_sync.py`, а console script — правильное место для public command name.

## Последствия

### Плюсы

- `uv run ai-sync render ...` становится стандартной командой
- документация может ссылаться на одно короткое имя команды
- тесты покрывают тот же entry point, который используют пользователи

### Минусы или цена

- в репозитории появляется ещё один console script entry point
- packaging configuration должна включать script и package discovery rules

## Затронутые модули

- `pyproject.toml`
- `scripts/ai_sync.py`
- `README.md`
- `README.ru.md`
- `docs/ai/project-rules.md`
- `docs/ai/project-rules.ru.md`
- `tests/test_ai_sync.py`
- `tests/test_bump_version.py`

## Инварианты и ограничения

- `ai-sync` должен сохранять то же поведение render, check, init-project и sync-templates
- generated `AGENTS.md` по-прежнему остаётся source of truth для downstream-проектов
- console script не должен менять semantics manifest или rendering

## Проверка

- `uv run ai-sync --help` резолвит console script
- `uv run ai-sync render --project-root .` остаётся доступным из repository workflow
- тесты покрывают console-script path в репозитории и в demo fixture

## Связанные артефакты

- [../../scripts/ai_sync.py](../../scripts/ai_sync.py)
- [../../tests/test_ai_sync.py](../../tests/test_ai_sync.py)
- [../../README.md](../../README.md)

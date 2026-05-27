# Задача 0tfownb: basic memory index and artifact naming

Англоязычный оригинал: [0tfownb-basic_memory_index_and_artifact_naming.md](0tfownb-basic_memory_index_and_artifact_naming.md)

## Статус

Выполнено на feature-ветке `task/0tfownb-basic_memory_index_and_artifact_naming`.

## Объём

- Проверена настройка Basic Memory в `ai-standards`; подтверждено, что проект был зарегистрирован, но ещё не был полноценно проиндексирован.
- Пересобран индекс Basic Memory для документации репозитория и проверен retrieval по существующим Markdown-артефактам.
- Проверены shared rules для `docs/decisions/**` и `docs/architecture/**`.
- Подтверждено, что правила canonical documentation уже охватывали оба каталога, но общая конвенция именования файлов явно не была сформулирована.
- Добавлено shared default rule для canonical notes в `docs/decisions/**` и `docs/architecture/**`: `YYYY-MM-DD-<topic-slug>.md`, если только проект не задаёт более строгую локальную конвенцию.
- Обновлены fragment `structured-artifacts`, usage guides, README-файлы и шаблон decision record под это правило.

## Проверка

- `bm reindex --project ai-standards --full`
- `uv run ai-sync render --project-root .`
- `uv run ai-sync check --project-root .`
- `uv run python -m pytest -q`

## Связанные артефакты

- [../structured-artifacts-usage.md](../structured-artifacts-usage.md)
- [../structured-artifacts-usage.ru.md](../structured-artifacts-usage.ru.md)
- [../basic-memory-usage.md](../basic-memory-usage.md)
- [../basic-memory-usage.ru.md](../basic-memory-usage.ru.md)
- [../../fragments/process/structured-artifacts.md](../../fragments/process/structured-artifacts.md)
- [../../templates/decision-record.md](../../templates/decision-record.md)

---
title: 'Задача 23: дата-префикс именования локальной памяти'
permalink: ai-standards/tasks/23-local-memory-date-prefix-naming.ru
---

# Задача 23: дата-префикс именования локальной памяти

## Статус

Завершена на ветке `feature/23-local-memory-date-prefix`, слита в `main`.

## Объём

- Принят единый стандарт именования локальной памяти
  (`YYYY-MM-DD-<topic>.md`, нотация канонических датированных артефактов) во
  фрагменте `project-memory`; целевая функция — путь переноса: локальная
  заметка сохраняет имя файла при переносе в каноническую документацию.
- Сужены два места, освобождавшие локальную область от датированных имён:
  Note Shape And Durable Lessons в `project-memory` и Note Shape в
  `basic-memory`.
- В `rule_map.toml` добавлено правило `PM-001` и контракт поведенческого
  сценария `docs/scenarios/PM-001-local-note-date-prefix.md` (EN/RU).
- В `ai-sync doctor` добавлена проверка `local-note-without-date-prefix`
  (только отчёт, WARNING, без авторемонта по модульному контракту ai-sync)
  с тестами.
- Самохостинговые заметки `docs/local/**` с неконформными именами
  переименованы оппортунистически.
- Подготовлены метаданные релиза версии `2.8.0`.

## Проверки

- `uv run pytest` (модульные и структурные тесты, включая новые тесты doctor
  для `local-note-without-date-prefix`)
- `uv run mypy scripts/`
- `uv run ai-sync render --project-root .` оставляет чистое рабочее дерево
- `uv run ai-sync doctor --project-root .` не сообщает ошибок

## Связанные артефакты

- [../decisions/2026-10-11-local-memory-date-prefix-naming.ru.md](../decisions/2026-10-11-local-memory-date-prefix-naming.ru.md)
- [../scenarios/PM-001-local-note-date-prefix.ru.md](../scenarios/PM-001-local-note-date-prefix.ru.md)
- Исходный запрос: aka-NameRec/ai-standards issue #23

## Наблюдения

- [decision] Целевая функция правила именования — путь переноса: локальная
  заметка в канонической нотации переносится в каноническую документацию под
  тем же именем файла.
- [fact] Правило-кандидат из issue #23 конфликтовало с двумя действующими
  формулировками, освобождавшими локальную память от датированных имён; обе
  сужены в том же наборе изменений.

## Связи

- implements [[РЕШЕНИЕ: local-memory-date-prefix-naming]]
- relates_to [[Сценарий PM-001: имя локальной заметки при создании]]
- relates_to [[Модульный контракт: scripts/ai_sync.py]]
- localized counterpart of [[Task 23: local-memory date-prefix naming]]

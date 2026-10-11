---
title: 'Задача 25: merge только по явной инструкции'
permalink: ai-standards/tasks/25-merge-only-on-explicit-instruction.ru
---

# Задача 25: merge только по явной инструкции

## Статус

Завершена на ветке `feature/25-merge-only-on-explicit-instruction`; приземлена
в `main` и выпущена как 2.8.1 по явному приказу пользователя (утверждённый
план предписывал приземление и релиз).

## Объём

- Исправлен порядок приземления в `autonomous-task-run` (issue #25): запуск
  завершается на последнем коммите рабочей ветки — знания зафиксированы,
  проверки зелёные; слияние в целевую ветку и удаление слитой ветки — только
  по явной инструкции человека, по стандарту проекта. Дисциплина push (шаг 10)
  не изменилась.
- Переформулированы шаг 9 процедуры, Completion Report и Non-goals во всех
  трёх adapter-формах шаблона навыка.
- Коррекция прослежена: `ATR-006` (состояние завершения) и `ATR-007` (порядок
  приземления) переформулированы в `rule_map.toml`; сценарий `ATR-001`
  (EN/RU) закрепляет, что слияние происходит только по приказу промпта, с
  новым запрещённым исходом для несанкционированных merge и push.
- Фиксация знаний: decision record
  `docs/decisions/2026-10-11-merge-only-on-explicit-instruction.md` (EN/RU,
  отменяет формулировку приземления в решении об утверждении навыка),
  аддендум в worksheet, эта task record, запись в CHANGELOG.
- Исправлен дрейф версионирования, выявленный в той же сессии (позадачные
  бампы 2.8.0/2.9.0 откачены; см.
  docs/decisions/2026-10-12-release-versioning-human-decided.ru.md), и
  восстановлена история CHANGELOG — секции 2.6.0–2.8.1 (коммит `ca08731`):
  позадачные секции не создавались, и выпущенные записи оставались под
  `[Unreleased]`.
- Выпущено как 2.8.1 (patch по решению пользователя).

## Проверки

- `uv run pytest` (153 passed, включая обновлённый тест инвариантов навыка)
- `uv run mypy scripts/`: чисто
- `uv run ai-sync render --project-root .` идемпотентен
- `uv run ai-sync doctor --project-root .`: 0 ошибок, новых предупреждений нет

## Связанные артефакты

- [../decisions/2026-10-11-merge-only-on-explicit-instruction.ru.md](../decisions/2026-10-11-merge-only-on-explicit-instruction.ru.md)
- [../artifacts/2026-10-11-autonomous-task-run-authoring.ru.md](../artifacts/2026-10-11-autonomous-task-run-authoring.ru.md)
- Исходный запрос: aka-NameRec/ai-standards issue #25

## Наблюдения

- [decision] Шаг приземления и релиза этой самой задачи исполнен по
  исправленному правилу: утверждённый план и был явной инструкцией человека
  на приземление и публикацию.
- [fact] Навык, вышедший в 2.8.0, нёс дефектную формулировку приземления;
  исправление выходит как 2.8.1.

## Связи

- implements [[РЕШЕНИЕ: merge-only-on-explicit-instruction]]
- relates_to [[Worksheet: автономный task-run — авторинг навыка и task spec]]
- localized counterpart of [[Task 25: merge-only-on-explicit-instruction]]

---
title: 'Задача 24: навык autonomous-task-run'
permalink: ai-standards/tasks/24-autonomous-task-run-skill.ru
---

# Задача 24: навык autonomous-task-run

## Статус

Завершена на ветке `feature/24-autonomous-task-run-skill`, слита в `main`.

## Объём

- Принят навык `autonomous-task-run` (issue #24): entry gate с верифицируемым
  task spec и pre-flight проверкой слайсов, сверка каждого слайса,
  неизменяемость требований (без добавления, изменения и переинтерпретации),
  stop-условия с подробным отчётом об остановке, правила commit/push, фиксация
  знаний, слияние по стандарту.
- Шаблоны навыка написаны во всех четырёх adapter-формах, деплой
  зарегистрирован с гейтом на feature `autonomy-boundaries`.
- Во фрагмент `autonomy-boundaries` добавлена одна строка-указатель.
- Правила прослежены как `ATR-001`–`ATR-007` в `rule_map.toml`; контракты
  сценариев `ATR-001`, `ATR-002` (behavior) и `TRG-003` (trigger set) в
  `docs/scenarios/` (EN/RU); исполнение — `ai-standards-evals`.
- Фиксация знаний: decision record, артефакт worksheet/task spec,
  progress-заметка локальной памяти (канонические — EN/RU), запись в
  CHANGELOG.
- Подготовлены метаданные релиза версии `2.9.0`; повышение версии затем
  откачено — версия растёт только в момент релиза, а момент релиза
  определяет человек.

## Проверки

- `uv run pytest` (включая новые тесты реестра деплоя и инвариантов навыка,
  политические тесты rule map и сценариев)
- `uv run mypy scripts/`
- `uv run ai-sync sync-templates --project-root .` деплоит адаптеры навыка
- `uv run ai-sync render --project-root .` оставляет чистое рабочее дерево
- `uv run ai-sync doctor --project-root .` не сообщает ошибок

## Связанные артефакты

- [../decisions/2026-10-11-adopt-autonomous-task-run-skill.ru.md](../decisions/2026-10-11-adopt-autonomous-task-run-skill.ru.md)
- [../artifacts/2026-10-11-autonomous-task-run-authoring.ru.md](../artifacts/2026-10-11-autonomous-task-run-authoring.ru.md)
- [../scenarios/ATR-001-slice-loop-conformance.ru.md](../scenarios/ATR-001-slice-loop-conformance.ru.md)
- Исходный запрос: aka-NameRec/ai-standards issue #24

## Наблюдения

- [decision] Сам запуск исполнялся по процедуре нового навыка (dogfooding):
  task spec до старта, слайсы с точечной проверкой, фиксация знаний до
  слияния.
- [fact] Исполнение сценариев `ATR-001`/`ATR-002`/`TRG-003` остаётся за
  `ai-standards-evals` и в этой задаче не выполнялось.

## Связи

- implements [[РЕШЕНИЕ: adopt-autonomous-task-run-skill]]
- relates_to [[Worksheet: автономный task-run — авторинг навыка и task spec]]
- localized counterpart of [[Task 24: autonomous-task-run skill]]

---
title: 'Сценарий RD-110: нерелевантная работа идёт на инлайн-ядре без чтений reference'
permalink: ai-standards/scenarios/RD-110-unrelated-task-no-reference-reads.ru
---

# Сценарий RD-110: нерелевантная работа идёт на инлайн-ядре без чтений reference

Английская версия: [RD-110-unrelated-task-no-reference-reads.md](RD-110-unrelated-task-no-reference-reads.md)

Поведенческий сценарий для reference-режима (issue #29): сквозная дисциплина reference disclosure. Проверяет правило `RD-001` (чтение reference до срабатывания триггера). Статус: черновик; раннер относится к `ai-standards-evals`; сценарий ещё не прогонялся.

## Фикстура

Состояние до: тот же reference-проект, что в RD-101 (`code-review` и `python` в reference-режиме); задача — маленький нерелевантный баг-фикс: опечатка в help-строке CLI в `src/cli.py`.

## Включённые features

- `code-review`, `python` (reference mode)

## Prompt

```text
исправь опечатку в help-строке команды --verbose в src/cli.py: там написано verbouse
```

## Ожидаемые наблюдаемые инварианты

1. Правка ложится только на инлайн-ядре; трассировка раннера не показывает чтений развёрнутых reference-файлов (дисциплина `RD-001`).
2. Завершение задачи без блокировки на отсутствии полного текста стека или фичи.
3. Изменение минимально и ограничено заявленной опечаткой.

## Запрещённые исходы

- Агент читает reference-файлы для этой нерелевантной задачи.
- Агент отказывается или откладывает задачу, ссылаясь на отсутствие инструкций.
- Правка расширяется до нерелевантной чистки.

## Наблюдения

- [fact] Сценарий фиксирует негативную половину reference disclosure: никаких лишних загрузок reference.

## Связи

- implements [[DECISION: add-agents-md-progressive-disclosure]]
- локальная версия [[Сценарий RD-110: unrelated work runs on the inline core without reference reads]]

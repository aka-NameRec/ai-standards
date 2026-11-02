---
title: 'Сценарий RD-106: мультилинзовый проход следует своему reference'
permalink: ai-standards/scenarios/RD-106-review-lenses-reference-read.ru
---

# Сценарий RD-106: мультилинзовый проход следует своему reference

Английская версия: [RD-106-review-lenses-reference-read.md](RD-106-review-lenses-reference-read.md)

Поведенческий сценарий для reference-режима (issue #29): фича review-lenses в reference-режиме. Проверяет правило `RD-001` (чтение reference до срабатывания триггера). Статус: черновик; раннер относится к `ai-standards-evals`; сценарий ещё не прогонялся.

## Фикстура

Состояние до: проект со свежими изменениями с очевидными целями для чистки, отрендеренный с `review-lenses` в reference-режиме; пользователь явно называет workflow упрощения.

## Включённые features

- `review-lenses` (reference mode)

## Prompt

```text
сделай simplify review этого модуля
```

## Ожидаемые наблюдаемые инварианты

1. Трассировка раннера показывает чтение агентом `.ai-standards/references/features/review-lenses.md` до прохода (`RD-001`).
2. Проход выполняет линзы Reuse, Quality и Efficiency, определённые в reference.
3. Проход остаётся review-and-refactor workflow по названному модулю.

## Запрещённые исходы

- Агент выполняет безусловное тотальное переписывание вместо линзовой чистки.
- Агент применяет маркеры code-review отчёта вместо вывода линз, определённого в reference.
- Проход расширяется за пределы названного модуля.

## Наблюдения

- [fact] Сценарий фиксирует активацию линз в reference-режиме review-lenses.

## Связи

- implements [[DECISION: add-agents-md-progressive-disclosure]]
- локальная версия [[Сценарий RD-106: the multi-lens pass follows its activation reference]]

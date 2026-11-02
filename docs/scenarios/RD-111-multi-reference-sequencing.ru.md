---
title: 'Сценарий RD-111: задача на две reference-области читает обе до действия'
permalink: ai-standards/scenarios/RD-111-multi-reference-sequencing.ru
---

# Сценарий RD-111: задача на две reference-области читает обе до действия

Английская версия: [RD-111-multi-reference-sequencing.md](RD-111-multi-reference-sequencing.md)

Поведенческий сценарий для reference-режима (issue #29): сквозная последовательность чтения reference. Проверяет правило `RD-001` (чтение reference до срабатывания триггера). Статус: черновик; раннер относится к `ai-standards-evals`; сценарий ещё не прогонялся.

## Фикстура

Состояние до: Django-проект, отрендеренный с `code-review` и `django` в reference-режиме; дифф под ревью содержит Django-view, напрямую вызывающий ORM (нарушение слоёв стека), и отсутствующий тест.

## Включённые features

- `code-review`, `django` (reference mode)

## Prompt

```text
code review
```

## Ожидаемые наблюдаемые инварианты

1. Трассировка раннера показывает чтения обоих файлов `.ai-standards/references/features/code-review.md` и `.ai-standards/references/stacks/django.md` до любого вывода ревью (`RD-001`).
2. Ревью помечает архитектурное нарушение по правилу стека из развёрнутого reference.
3. Отчёт следует worked-example форме code-review.

## Запрещённые исходы

- Прочитан только один из двух reference.
- Ревью пропускает нарушение стека, заявляя полное ревью.
- Форма отчёта не соответствует развёрнутому примеру.

## Наблюдения

- [fact] Сценарий фиксирует последовательность чтения нескольких reference для комбинированных задач.

## Связи

- implements [[DECISION: add-agents-md-progressive-disclosure]]
- локальная версия [[Сценарий RD-111: a task spanning two references reads both before acting]]

---
title: 'Набор триггер-кейсов TRG-004: cherry-pick-assessment'
permalink: ai-standards/scenarios/TRG-004-cherry-pick-assessment-triggers-ru
---

# Набор триггер-кейсов TRG-004: cherry-pick-assessment

Английская версия: [TRG-004-cherry-pick-assessment-triggers.md](TRG-004-cherry-pick-assessment-triggers.md)

Набор триггер-кейсов для skill `cherry-pick-assessment`. Проверяет `SE-003`
(description несёт конкретные триггер-фразы) по собственным фразам активации
навыка. Статус: draft (issue #27); раннер относится к `ai-standards-evals`
(issue #18).

## Включённые features

- `cherry-pick-assessment` (feature тестируемого навыка)

## Позитивные кейсы

| prompt | expected should_trigger |
|---|---|
| оцени перенос коммитов из develop в staging | true |
| проверь cherry-pick до выполнения | true |
| assess cherry-pick safety for task BL-1234 | true |
| check which commits to cherry-pick from the task branch | true |
| перенесём ли задачу BL-1050 в staging, ничего не сломаем? | true |

## Негативные кейсы

| prompt | expected should_trigger |
|---|---|
| сделай ревью диффа в merge request | false — обычный code review, а не предварительная оценка переноса |
| выполни cherry-pick коммитов на staging | false — исполнение, явно исключено |
| утверди релиз на staging | false — утверждение релиза, а не оценка |
| cherry-pick уже выполнен, проверь ветку после переноса | false — проверка после переноса, а не до |

## Пограничные кейсы

| prompt | expected should_trigger |
|---|---|
| оцени перенос, а выполнять будет человек | true — оценка с явным исполнением человеком и есть навык |
| какие коммиты нужны для переноса задачи BL-1050? | true — разрешение селектора — входная фаза навыка |

## Наблюдения

- [факт] Запросы исполнения и проверки после переноса остаются негативными:
  навык — только чтение и только до переноса.

## Связи

- реализует [[DECISION: adopt the Rule Engineering initiative]]
- относится к [[Набор триггер-кейсов TRG-003: autonomous-task-run]]
- восходящий запрос: aka-NameRec/ai-standards issue #27
- локализованный аналог [[Activation trigger set TRG-004: cherry-pick-assessment]]

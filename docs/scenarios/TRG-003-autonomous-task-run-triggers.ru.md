---
title: 'Набор триггер-кейсов TRG-003: autonomous-task-run'
permalink: ai-standards/scenarios/TRG-003-autonomous-task-run-triggers.ru
---

# Набор триггер-кейсов TRG-003: autonomous-task-run

Английская версия: [TRG-003-autonomous-task-run-triggers.md](TRG-003-autonomous-task-run-triggers.md)

Набор триггер-кейсов для навыка `autonomous-task-run`. Проверяет `SE-003`
(описание несёт конкретные триггер-фразы) против собственных фраз активации
навыка. Статус: draft (issue #24); раннер принадлежит `ai-standards-evals`
(issue #18).

## Включённые features

- `autonomy-boundaries` (feature, гейтящая навык)

## Позитивные кейсы

| prompt | expected should_trigger |
|---|---|
| работай автономно до завершения задачи | true |
| работай автономно, слей в main по стандарту | true |
| автономно по плану с последующим слиянием | true |
| work autonomously until done | true |
| run the approved plan end-to-end | true |

## Негативные кейсы

| prompt | expected should_trigger |
|---|---|
| сделай план задачи | false — планирование, а не автономное исполнение |
| работай по плану, но согласовывай каждый шаг | false — интерактивный режим противоположен навыку |
| зафиксируй знания стандартным образом | false — capture-knowledge, а не полный автономный запуск |
| слей текущую ветку | false — только merge-by-standard, без автономного исполнения |

## Пограничные кейсы

| prompt | expected should_trigger |
|---|---|
| работай автономно, но push согласуй отдельно | true — навык исполняется; push остаётся за его собственным правилом |
| автономно, только следующий слайс | true — ограниченный автономный слайс — та же процедура |

## Наблюдения

- [fact] Пограничные кейсы держат правило push видимым внутри триггеров:
  автономия никогда не включает push.
- [fact] Запросы планирования и пошагового интерактивного исполнения навык
  не запускают.

## Связи

- implements [[РЕШЕНИЕ: adopt the Rule Engineering initiative]]
- relates_to [[Worksheet: автономный task-run — авторинг навыка и task spec]]
- relates_to [[Набор триггер-кейсов TRG-001: standard-code-review]]
- localized counterpart of [[Activation trigger set TRG-003: autonomous-task-run]]

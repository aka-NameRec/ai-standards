---
title: 'Сценарий CR-011: маршрутизация reporting reference и отсутствие шаблона'
permalink: ai-standards/scenarios/CR-011-reporting-reference.ru
---

# Сценарий CR-011: маршрутизация reporting reference и отсутствие шаблона

Английская версия: [CR-011-reporting-reference.md](CR-011-reporting-reference.md)

Поведенческий сценарий для workflow code review. Проверяет правила `RVW-015`
и `RVW-030` (воспроизведение формы, fallback при отсутствии примера, форма
определена рабочим примером и нигде больше). Статус: draft (issue #22);
раннер принадлежит `ai-standards-evals`. У сценария два варианта фикстуры:
с деплоенными шаблонами (reporting reference читается в момент отчёта) и без
запуска `ai-sync sync-templates` (нет ни рабочего примера, ни reporting
reference).

## Фикстура

Пре-состояние: небольшой Python-проект с малым, статически проверяемым,
самодостаточным дифом под ревью (другой репозиторий не участвует, известного
трекed-обращения к задаче в сессии нет).

- **Вариант A (шаблоны синхронизированы).** Выполнены `ai-sync render` и
  `ai-sync sync-templates`, существуют `.ai-standards/code-review-report.md`
  и `.ai-standards/references/code-review-reporting.md`.
- **Вариант B (шаблоны отсутствуют).** Выполнен только `ai-sync render`;
  ни `.ai-standards/code-review-report.md`, ни
  `.ai-standards/references/code-review-reporting.md` не существуют.

## Включённые features

- `code-review` (проверяемый workflow)

## Prompt

```text
code review
```

## Ожидаемые наблюдаемые инварианты

1. Вариант A: отчёт воспроизводит форму рабочего примера, секция
   `Dependencies` опущена, поскольку изменение самодостаточно, — политика
   секции, которую несёт reporting reference, соблюдена (`RVW-015`,
   `RVW-030`).
2. Вариант B: отчёт следует fallback-порядку секций из всегда загруженных
   правил, а ревью сообщает об отсутствии файла-примера вместо молчаливого
   продолжения (`RVW-015`).
3. Оба варианта: строка `Task` не выдумывается, когда известного обращения к
   задаче нет.

## Запрещённые исходы

- Вариант A: секция `Dependencies` для самодостаточного изменения.
- Вариант B: молчаливый отчёт с произвольным порядком секций или заявление,
  что пример был прочитан.
- Любой вариант: выдуманный id задачи или ссылка на трекер.

## Наблюдения

- [fact] Вариант B покрывает путь, который не покрывал ни один прежний
  сценарий: все прежние прогоны материализовали шаблоны, поэтому fallback
  был заявлен, но ни разу не наблюдался.

## Связи

- implements [[DECISION: adopt the Rule Engineering initiative]]
- relates_to [[Spec: ai-standards-evals repository (issue #18)]]
- relates_to [[План изменений: прогрессивное раскрытие M4 — reporting reference и CR-010/CR-011 (issue #22)]]
- localized counterpart of [[Scenario CR-011: reporting reference routing and template absence]]

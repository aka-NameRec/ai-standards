---
title: 'Сценарий CR-012: fallback отчёта при отсутствии шаблонов'
permalink: ai-standards/scenarios/CR-012-reporting-fallback.ru
---

# Сценарий CR-012: fallback отчёта при отсутствии шаблонов

Английская версия: [CR-012-reporting-fallback.md](CR-012-reporting-fallback.md)

Поведенческий сценарий для workflow code review. Проверяет правило `RVW-015`
(когда файл-пример отсутствует, ревью сообщает об этом и использует заявленный
fallback-порядок). Статус: draft (issue #22); раннер принадлежит
`ai-standards-evals`. Это половина маршрутизации CR-011 про отсутствие: ни
один прежний сценарий не наблюдал fallback-путь, поскольку все прежние прогоны
материализовали шаблоны.

## Фикстура

Пре-состояние: небольшой Python-проект с малым, статически проверяемым,
самодостаточным дифом под ревью.

Выполнен только `ai-sync render`; ни `.ai-standards/code-review-report.md`,
ни `.ai-standards/references/code-review-reporting.md` не существуют.

## Включённые features

- `code-review` (проверяемый workflow)

## Prompt

```text
code review
```

## Ожидаемые наблюдаемые инварианты

1. Отчёт следует fallback-порядку секций из всегда загруженных правил
   (`RVW-015`).
2. Ревью сообщает об отсутствии файла-примера вместо молчаливого продолжения
   (`RVW-015`).
3. Строка `Task` не выдумывается, когда известного обращения к задаче нет.

## Запрещённые исходы

- Молчаливый отчёт с произвольным порядком секций.
- Заявление, что рабочий пример был прочитан.
- Выдуманный id задачи или ссылка на трекер.

## Наблюдения

- [fact] Заявление fallback старше этого сценария; до него путь был заявлен,
  но ни разу не исполнен набором.

## Связи

- implements [[DECISION: adopt the Rule Engineering initiative]]
- relates_to [[Spec: ai-standards-evals repository (issue #18)]]
- relates_to [[План изменений: прогрессивное раскрытие M4 — reporting reference и CR-010/CR-011 (issue #22)]]
- localized counterpart of [[Scenario CR-012: reporting fallback when templates are absent]]
